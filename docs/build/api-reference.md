# API reference

DD's data is available through a public, read-only JSON API. It's the same API the website uses.

> **Status:** early and evolving. Response shapes may change as the data model grows. If you're building on it, tell us so we can give you notice of changes.

## Basics

**Base URL**

```
https://app.democracydistributed.com/api/gateway
```

- All requests are `GET`. No authentication is needed.
- All responses are JSON.
- IDs are long numeric strings, e.g. `388481829130272769`.
- A field with no data returns `null`. Fields are never left out.
- CORS is open, so you can call the API from a browser.

## Endpoints

| Endpoint | Returns | Parameters |
|---|---|---|
| `GET /orgs` | All publicly listed organizations | none |
| `GET /org` | One organization's details | `orgId` |
| `GET /sankey` | An organization's revenue and spending, as a nested tree | `orgId` |
| `GET /trace` | The accountability chain behind one payment | `transactionId` |
| `GET /items` | An organization's decisions | `orgId`, optional `status` |
| `GET /item` | One decision | `itemId` |
| `GET /projects` | An organization's projects | `orgId` |
| `GET /project` | One project | `projectId` |
| `GET /people` | An organization's officials and members | `orgId`, optional `limit` |

## Examples

### `GET /org`

```
GET /api/gateway/org?orgId=388481829130272769
```

```json
{
  "orgId": "388481829130272769",
  "name": "Riverdale Community Board",
  "type": "Community Board",
  "subType": null,
  "jurisdiction": "Toronto, ON",
  "description": "A volunteer-run board managing parks and community services in Riverdale.",
  "status": "Active",
  "website": null
}
```

*Sample data for illustration.*

### `GET /sankey`

Returns `revenue_data` and `spending_data` as trees. Each level follows the organization's budget categories. The deepest level holds individual entries:

```json
{
  "org": "Riverdale Community Board",
  "revenue": 143000,
  "spending": 52000,
  "revenue_data": {
    "name": "Revenue",
    "children": [
      { "name": "…", "children": [
        { "name": "…", "amount": 8200, "transactionID": "TXN-001", "ledgerID": "LDG-001", "hasChain": false }
      ]}
    ]
  },
  "spending_data": { "name": "Spending", "children": ["…same shape…"] }
}
```

- `hasChain: true` means the entry has a linked decision chain, which you can look up with `/trace`.
- Empty categories are left out.

### `GET /trace`

```json
{
  "transactionId": "490999320024186999",
  "description": "ABC Paving Co. — Invoice 3",
  "amount": 15000,
  "date": "2024-03-10",
  "chain": {
    "suggestion": { "id": "SGG-01", "text": "The path on the east side of Riverdale Park is deteriorating." },
    "item": { "id": "ITM-2024-001", "title": "Authorize tender for park path resurfacing — $50,000 budget" },
    "vote": { "date": "2024-02-12", "result": "Passed", "inFavour": 8, "against": 1 },
    "project": { "id": "PRJ-2024-001", "title": "Park Path Resurfacing" }
  }
}
```

*Sample data for illustration.*

- `chain` is `null` when nothing has been linked yet.
- Any single link can be `null`. That's a gap a contributor can fill.
- A **partial chain** is common: a payment linked to a project, but not yet to the decision that authorized it.

### `GET /people`

Returns two lists:

- `officials`: roles in the real-world organization. Each row has a `status`:
  - `recorded`: we know who holds the role
  - `holder_not_recorded`: the role exists, but the holder is unknown
  - `role_not_recorded`: the person is known, but their role isn't
- `members`: people who have joined the organization on DD

It also includes `counts` for totals. Use `limit` to cap the officials list.

## Planned

- `/meetings`: meetings and what was decided at each
- Revenue-side trace: linking tax and fee revenue to the by-law that authorizes it
- Year filtering on `/sankey`

**Questions or ideas?** See [Get involved](../contribute/get-involved.md).
