# Corteza CSV importer

A small Python script that creates records in DD's Corteza database from a CSV file, one row at a time, through Corteza's API.

Use it for **Transactions** and any large batch. For how it fits into adding data, read [Adding financial data](../../docs/contribute/adding-data.md) first.

## Why not Corteza's own CSV import?

Corteza's built-in import skips its automations. DD relies on one: when a Transaction is created, a workflow creates its two Ledger entries, and the money chart reads those. Transactions imported through the built-in import never reach the chart. Records created through the API do trigger the workflow, so this script creates them that way.

It also looks up record IDs from names, so a CSV can say `SFS-100` instead of an 18-digit ID.

## What you need

- A Corteza account with **data-entry access** (see the guide).
- Python 3, plus one package: `pip install requests`

## Run it

1. **Copy a config.** Copy `config.example.json` (or a config from an example folder) and name the copy `config.json`, next to the script. Set `csv_path` to your CSV and `module_handle` to the module you're filling (`Budget_Category`, `Transaction`, `Item`, …).
2. **Get a sign-in token.** Log into Corteza in your browser, press F12 → **Network**, click anything in Corteza, find a request to `/api/…`, and copy the value after `Authorization: Bearer`. It expires in about an hour.
3. **Paste the token** into `bearer_token` in `config.json`.
4. **Dry run:** `python corteza_csv_import.py --dry-run` (add `--limit 3` to try three rows). Nothing is created; you see every lookup and the exact record that would be sent.
5. **Live run:** `python corteza_csv_import.py`

Load parent records before the records that point to them: categories before Transactions.

## Safety

- **The token is you.** It can do exactly what your Corteza account can do, nothing more. Never share it, paste it in chat, or commit it. `config.json` and log files are ignored by git for this reason.
- **The script only creates and reads.** It has no code that edits or deletes records.
- **Re-running creates duplicates.** There's no "update if it exists". If a run stops halfway, remove the rows that succeeded before running again.
- **Start small.** Try two or three rows, check them in Corteza, then run the rest.
- `stop_on_error: true` stops at the first failure instead of carrying on.

## Config fields

| Field | Meaning |
|---|---|
| `bearer_token` | Your sign-in token (step 2). |
| `module_handle` | The Corteza module to create records in. |
| `csv_path` | Path to the CSV, relative to the script. |
| `reference_lookups` | For fields that point to another record: which module to search and which field to match on. If the CSV already holds the record ID, leave the field out here. |
| `field_map` | Optional. Maps CSV headers to field handles when they differ. If headers already equal the handles, leave it out. |
| `skip_empty_values` | Leaves blank cells out instead of sending empty values. |

CSV headers must match Corteza field handles exactly (case-sensitive).

The script also supports an OAuth client (`client_id`, `client_secret`). Those belong to an admin-managed service account, not to volunteers; use the browser token.

## Example

`examples/children-services-2024/` loads Toronto's Children's Services spending for 2024 (FIR Schedule 40, line 1230): 9 Budget Categories, then 7 Transactions. Copy `config-1-budget-categories.example.json` to `config.json`, run it, then do the same with `config-2-transactions.example.json`.
It's here to show the shape of a real task. Check whether `SFS-000` already exists in Corteza before running it live; if it does, don't run it again.
