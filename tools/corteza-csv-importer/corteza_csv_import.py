#!/usr/bin/env python3
"""
Corteza CSV -> Compose Record API importer
==========================================

WHY THIS EXISTS
---------------
Corteza's built-in CSV import deliberately BYPASSES the automation engine, so
`compose:record / afterCreate` workflows (e.g. "Transaction: After Create",
which builds the Credit + Debit Ledger pair) NEVER fire on a CSV import.
Confirmed by the Corteza core team:
  https://forum.cortezaproject.org/t/workflow-trigger-on-import-csv/575

Records created through the REST API DO fire afterCreate. So instead of using
the GUI CSV import, this script reads your CSV and POSTs each row as a record.
Your existing workflow then runs untouched, per row, exactly as if you'd typed
the record in by hand.

It also solves the old record-selector pain
(https://forum.cortezaproject.org/t/how-to-import-records-with-record-selector-fields-populated/535):
a record-reference field is just the target recordID passed as a value. You can
either put the IDs directly in the CSV, or let this script look them up by name.

USAGE
-----
1.  pip install requests
2.  Fill in the CONFIG block below (or use a config.json — see README).
3.  Dry run first:   python corteza_csv_import.py --dry-run
4.  Real run:        python corteza_csv_import.py

The dry run resolves all IDs and prints the exact JSON payloads WITHOUT
creating anything, so you can eyeball the first few rows before committing.
"""

import argparse
import csv
import json
import os
import sys
import time

try:
    import requests
except ImportError:
    sys.exit("Missing dependency. Run:  pip install requests")


# ===========================================================================
# CONFIG  -- edit these, or override any of them in config.json (see README)
# ===========================================================================
CONFIG = {
    # --- Corteza instance ---
    "base_url": "https://app.democracydistributed.com",

    # --- Auth: pick ONE method ---
    # Method A (quickest): paste a bearer JWT copied from your browser dev tools.
    #   Expires in ~1 hour; fine for a one-off import.
    "bearer_token": "",
    # Method B (durable): OAuth2 client credentials from an Auth Client that has
    #   the "client_credentials" grant + "api" scope enabled.
    "client_id": "",
    "client_secret": "",

    # --- What to import into ---
    "namespace_handle": "DD",
    "module_handle": "Transaction",

    # --- Your CSV ---
    "csv_path": "transactions.csv",
    # Optional: CSV delimiter (default comma)
    "delimiter": ",",

    # --- Column -> Corteza field mapping ---
    # KEY   = column header in your CSV
    # VALUE = field handle in the Corteza module
    # Only listed columns are imported; unlisted CSV columns are ignored.
    # If your CSV headers already match the field handles exactly, you can leave
    # this empty ({}) and the script will use headers as field names.
    "field_map": {
        # "CSV Header":       "Field_Handle",
        # "Amount":           "Amount",
        # "Date":             "Date",
        # "From Account":     "From",
        # "To Account":       "To",
        # "Description":      "Description",
        # "Category":         "Category",
    },

    # --- Reference (record-selector) field resolution ---
    # For fields that point at another module, you can supply the target
    # recordID directly in the CSV (simplest), OR have this script look the
    # record up by a human-readable label.
    #
    # Each entry: target field handle -> how to resolve it.
    #   "module"     = handle of the module being referenced
    #   "match_field"= field handle on that module to match the CSV value against
    # If a field is NOT listed here, its CSV value is sent as-is (assumed to be
    # already a recordID, or a plain scalar value).
    "reference_lookups": {
        # "From": {"module": "Treasury_Account", "match_field": "Name"},
        # "To":   {"module": "Treasury_Account", "match_field": "Name"},
        # "Item": {"module": "Item",             "match_field": "Title"},
    },

    # --- Behaviour ---
    "rate_limit_seconds": 0.15,   # pause between record creates (be kind to the server)
    "stop_on_error": False,       # True = abort on first failed row
    "skip_empty_values": True,    # don't send fields whose CSV cell is blank
}
# ===========================================================================


def load_config():
    cfg = dict(CONFIG)
    # Optional config.json next to the script overrides the inline CONFIG.
    here = os.path.dirname(os.path.abspath(__file__))
    cfg_file = os.path.join(here, "config.json")
    if os.path.exists(cfg_file):
        with open(cfg_file, "r", encoding="utf-8") as f:
            cfg.update(json.load(f))
    return cfg


class Corteza:
    def __init__(self, cfg):
        self.base = cfg["base_url"].rstrip("/")
        self.cfg = cfg
        self.session = requests.Session()
        self.token = self._authenticate()
        self.session.headers.update({
            "Authorization": "Bearer " + self.token,
            "Content-Type": "application/json",
        })
        self._lookup_cache = {}  # (moduleID, match_field, value) -> recordID

    # --- auth -------------------------------------------------------------
    def _authenticate(self):
        if self.cfg.get("bearer_token"):
            return self.cfg["bearer_token"].strip()
        if self.cfg.get("client_id") and self.cfg.get("client_secret"):
            url = self.base + "/api/auth/oauth2/token"
            resp = requests.post(
                url,
                data={"grant_type": "client_credentials", "scope": "api"},
                auth=(self.cfg["client_id"], self.cfg["client_secret"]),
            )
            resp.raise_for_status()
            tok = resp.json().get("access_token")
            if not tok:
                sys.exit("OAuth2 succeeded but no access_token in response: " + resp.text)
            return tok
        sys.exit("No auth configured. Set bearer_token OR client_id+client_secret.")

    # --- generic GET helper ----------------------------------------------
    def _get(self, path, params=None):
        r = self.session.get(self.base + path, params=params)
        r.raise_for_status()
        body = r.json()
        return body.get("response", body)

    # --- resolve namespace + module + fields ------------------------------
    def resolve_namespace(self, handle):
        data = self._get("/api/compose/namespace/", {"limit": 500})
        for ns in data.get("set", []):
            if ns.get("slug") == handle or ns.get("name") == handle:
                return ns["namespaceID"]
        sys.exit("Namespace not found: " + handle)

    def resolve_module(self, namespace_id, handle):
        data = self._get("/api/compose/namespace/%s/module/" % namespace_id,
                         {"limit": 500})
        for m in data.get("set", []):
            if m.get("handle") == handle or m.get("name") == handle:
                return m
        sys.exit("Module not found: " + handle)

    # --- reference lookup -------------------------------------------------
    def lookup_reference(self, namespace_id, module_handle, match_field, value):
        key = (module_handle, match_field, value)
        if key in self._lookup_cache:
            return self._lookup_cache[key]
        module = self.resolve_module(namespace_id, module_handle)
        # Corteza query: string fields wrapped in single quotes
        safe = str(value).replace("'", "\\'")
        query = "%s = '%s'" % (match_field, safe)
        data = self._get(
            "/api/compose/namespace/%s/module/%s/record/" % (namespace_id, module["moduleID"]),
            {"query": query, "limit": 2},
        )
        recs = data.get("set", [])
        if not recs:
            raise ValueError("No %s record where %s = '%s'" % (module_handle, match_field, value))
        if len(recs) > 1:
            raise ValueError("Ambiguous: %d %s records where %s = '%s'"
                             % (len(recs), module_handle, match_field, value))
        rid = recs[0]["recordID"]
        self._lookup_cache[key] = rid
        return rid

    # --- create record ----------------------------------------------------
    def create_record(self, namespace_id, module_id, values):
        payload = {
            "namespaceID": str(namespace_id),
            "moduleID": str(module_id),
            "values": values,
        }
        r = self.session.post(
            self.base + "/api/compose/namespace/%s/module/%s/record/" % (namespace_id, module_id),
            data=json.dumps(payload),
        )
        if r.status_code >= 400:
            raise RuntimeError("HTTP %s: %s" % (r.status_code, r.text))
        body = r.json()
        if isinstance(body, dict) and body.get("error"):
            raise RuntimeError("API error: %s" % json.dumps(body["error"]))
        resp = body.get("response", body)
        return resp.get("recordID")


def build_values(row, cfg, corteza, namespace_id):
    """Turn one CSV row into a Corteza values array [{name, value}, ...]."""
    field_map = cfg.get("field_map") or {}
    ref_lookups = cfg.get("reference_lookups") or {}
    values = []
    for col, cell in row.items():
        if col is None:
            continue
        field = field_map.get(col, col)  # fall back to header as field handle
        if field_map and col not in field_map:
            continue  # explicit map given and this column isn't in it -> skip
        cell = (cell or "").strip()
        if cfg.get("skip_empty_values", True) and cell == "":
            continue
        if field in ref_lookups:
            spec = ref_lookups[field]
            cell = str(corteza.lookup_reference(
                namespace_id, spec["module"], spec["match_field"], cell))
        values.append({"name": field, "value": cell})
    return values


def main():
    ap = argparse.ArgumentParser(description="Import a CSV into Corteza via the record API.")
    ap.add_argument("--dry-run", action="store_true",
                    help="Resolve everything and print payloads, but don't create records.")
    ap.add_argument("--limit", type=int, default=0,
                    help="Only process the first N rows (0 = all).")
    args = ap.parse_args()

    cfg = load_config()
    csv_path = cfg["csv_path"]
    if not os.path.isabs(csv_path):
        csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), csv_path)
    if not os.path.exists(csv_path):
        sys.exit("CSV not found: " + csv_path)

    corteza = Corteza(cfg)
    namespace_id = corteza.resolve_namespace(cfg["namespace_handle"])
    module = corteza.resolve_module(namespace_id, cfg["module_handle"])
    module_id = module["moduleID"]
    valid_fields = {f["name"] for f in module.get("fields", [])}

    print("Namespace %s -> %s" % (cfg["namespace_handle"], namespace_id))
    print("Module    %s -> %s  (%d fields)" % (cfg["module_handle"], module_id, len(valid_fields)))
    print("Mode      %s" % ("DRY RUN (no records created)" if args.dry_run else "LIVE"))
    print("-" * 60)

    ok, failed = 0, 0
    with open(csv_path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter=cfg.get("delimiter", ","))
        for i, row in enumerate(reader, start=1):
            if args.limit and i > args.limit:
                break
            try:
                values = build_values(row, cfg, corteza, namespace_id)
                # sanity: warn on unknown field handles
                unknown = [v["name"] for v in values if valid_fields and v["name"] not in valid_fields]
                if unknown:
                    print("  row %d WARNING unknown field(s): %s" % (i, ", ".join(unknown)))

                if args.dry_run:
                    print("  row %d payload: %s" % (i, json.dumps(values, ensure_ascii=False)))
                    ok += 1
                else:
                    rid = corteza.create_record(namespace_id, module_id, values)
                    print("  row %d created recordID %s" % (i, rid))
                    ok += 1
                    time.sleep(cfg.get("rate_limit_seconds", 0.0))
            except Exception as e:
                failed += 1
                print("  row %d FAILED: %s" % (i, e))
                if cfg.get("stop_on_error", False):
                    print("Stopping on first error (stop_on_error=True).")
                    break

    print("-" * 60)
    print("Done. %d ok, %d failed." % (ok, failed))
    if not args.dry_run and ok:
        print("Each created record fired afterCreate -> your Ledger workflow ran per row.")


if __name__ == "__main__":
    main()
