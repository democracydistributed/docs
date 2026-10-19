# Architecture overview

How DD is put together: the three layers, and how one data model serves both WikiGov and POD.

## Three layers

| Layer | What it is | Who uses it |
|---|---|---|
| **Web app** | A Next.js site at [democracydistributed.com](https://democracydistributed.com): the public organization pages, the money chart, and item and project pages. Source code is on [GitHub](https://github.com/democracydistributed/democracy-distributed). | Everyone |
| **Gateway** | Public, read-only endpoints that the web app calls to get its data. See the [API reference](api-reference.md). | The web app, and anyone who wants the data |
| **Corteza** | The database and admin interface, built on [Corteza](https://cortezaproject.org), an open-source low-code platform. Records, relationships and automations live here. | Contributors and maintainers |

**Why Corteza?** New modules, fields and automations can be added through a visual interface, without writing code. That keeps the data model open to contributors who aren't developers.

**Writing data (planned).** Today the Gateway is read-only, and data is entered in Corteza. A write path through the web app, with a review step before anything goes live, is planned.

## One data model, two directions

WikiGov and POD use the same records: Suggestion → Item → Vote → Project → Transaction → Ledger. What differs is where a decision is made.

| | WikiGov (observed) | POD (native) |
|---|---|---|
| **Where the decision happens** | Outside DD, e.g. at Toronto City Council | Inside DD, in the group itself |
| **What DD does** | Records it and connects it to the money | Hosts it: members propose, discuss and vote here |
| **Records are** | Read-only history | Interactive |

Which direction a record belongs to follows from its organization: records under a government are observed, and records under a community group are native. There's no separate flag on each record. Because the shapes are the same, features like the money chart work for both.

### How the web app tells them apart

The web app decides which direction to show from the organization's **type**:

- **Community Group** and **DD Government** (DD's own internal bodies, such as DD Central Government) get the community layout.
- Every other type, including a missing one, gets the government layout.

| | Government layout | Community layout |
|---|---|---|
| **Tabs** | Finances, Items, Projects, People | Suggestions, Items, Projects, Finances, Rules, People |
| **Accent colour** | Amber | Teal |

The Suggestions tab is currently hidden rather than blocked for governments: the server accepts a suggestion for any organization. The Rules tab is a placeholder for now.

See [Key concepts](key-concepts.md) for what each record type means.

**Next:** [The money chart (Sankey) →](sankey.md)
