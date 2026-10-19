# Key concepts

A plain-language glossary of the building blocks DD uses to describe any organization. The same concepts apply to a city council and to a tenant group.

## Who

| Concept | Meaning |
|---|---|
| **Organization** | Any body that decides and spends: a city, a department, an agency, a board, or a community group. Organizations can sit inside other organizations. |
| **Organization type** | What kind of body an organization is. *Community Group* and *DD Government* are treated as community (native) organizations; every other type is treated as government (observed). See [Architecture overview](architecture-overview.md#how-the-web-app-tells-them-apart). |
| **Department** | A unit inside an organization that does part of its work, such as Toronto Water inside the City of Toronto. It uses the organization's money and staff but doesn't own them, so it has no account of its own. |
| **Jurisdiction** | The geographic area an organization serves: city, province, or country. |
| **Position** | A role within an organization, such as "City Manager" or "Ward 14 Councillor". Positions stay the same while people change. |
| **Position Term** | Who held a position, and from when to when. |
| **Person** | An individual linked to one or more positions or organizations. |
| **Member** | Someone who has joined an organization *on DD* (the platform side, as opposed to the real-world role). |

## Rules

| Concept | Meaning |
|---|---|
| **Constitution** | A set of rules: a by-law, an act, a motion, or a community group's own rules. |
| **Amendment** | A change to a Constitution (insert, modify, or repeal), made by a decision. Rules change through Amendments, and the history is kept. |
| **Constitution Connector** | Who a Constitution applies to: which organizations or positions it covers, and which other rules it relates to. |

## Decisions

| Concept | Meaning |
|---|---|
| **Suggestion** | Public input or an idea. Anyone can make one. |
| **Item** | A formal proposal that goes to a meeting for a decision: a motion, report, or recommendation. |
| **Meeting** | When and where Items are decided. |
| **Vote** | The decision on an Item: the result and, where recorded, who voted which way. |
| **Decision Outcome** | What a decision produced, in plain words, e.g. "Contract awarded to ABC Paving for $45,000." |
| **Election** | How people are chosen to hold a position. |
| **Candidate** | A person standing in an Election. |

## Money

| Concept | Meaning |
|---|---|
| **Treasury Account** | An account where an organization holds money. |
| **Budget Category** | How money is classified, such as "Parks → Maintenance". Categories can nest several levels deep. |
| **Budget** | Planned amounts per category for a given year. It's optional, and when present it enables the planned vs. actual view. |
| **Funding Allocation** | Money a decision has committed to a purpose but not yet spent. |
| **Transaction** | A payment: who paid whom, how much, and when. It links to the Project or Item that authorized it. |
| **Ledger** | The accounting entries behind every Transaction (a debit and a credit). |

## Work

| Concept | Meaning |
|---|---|
| **Project** | An approved initiative with a scope and budget. |
| **Procurement Request** | A formal call for bids (RFQ, RFP, and so on) linked to a project. |
| **Bid** | A vendor's response to a Procurement Request. |
| **Job** | A task within a project, and on DD also a task for contributors. |
| **Reputation Event** | A record that credits someone for a contribution on DD, such as completing a Job. Together these build their public track record. |

**Next:** [The chain of accountability →](../understand/chain-of-accountability.md)
