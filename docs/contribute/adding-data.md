# Adding financial data

This guide is for volunteers who want to add an organization's spending or revenue so it shows up on its money chart. It uses Toronto as the example, but the same steps work for any organization.

You don't need a finance background. You do need patience with spreadsheets, and a willingness to leave something blank rather than guess.

{% hint style="info" %}
**Status:** this guide is new and is being tested on Toronto's 2024 and 2025 data. If a step doesn't match what you see, that's useful feedback. Tell us.
{% endhint %}

## What "adding data" means

DD stores data in **Corteza**, an open-source database with an admin screen. The money chart is built from three kinds of records:

| Record | What it is | Example |
|---|---|---|
| **Budget Category** | A box on the chart. Categories nest inside each other. | Social & Family Services → Children's Services → Contracted Services |
| **Transaction** | An amount of money moving, attached to the lowest category. | $825,933,041, dated 2024-12-31 |
| **Ledger entry** | Created *automatically* from each Transaction. The chart reads these. | You never create these by hand. |

So adding a year of spending means: create the category tree, then one Transaction per lowest category.

## How a spending/revenue branch is built

Each branch follows the same pattern, so the chart stays consistent:

```
Function            Social & Family Services        (from the FIR, the province's standard report)
└── Division        Children's Services             (the City division that spends it)
    └── Spent on    Salaries, Materials, Contracted Services, External Transfers, …
```

- **Amounts** come from the source line's own columns, copied exactly in full dollars. For Ontario cities that's FIR Schedule 40, column N (*Total Expenses Before Adjustments*), split across its seven spending columns.
- **Date** is the last day of the fiscal year (for example `2024-12-31`).
- **From** is the organization's own treasury account.
- **Department** is set only when a source links the line to that division. Otherwise leave it blank.
- **Description** names the source, the line code and the column, so anyone can check the number.

## Before you start

1. **Create an account.** [Sign up here](https://www.democracydistributed.com). Click on the top right corner profile icon and hit `Create Account`.
2. **Ask for data-entry access.** Email [ajaymatharoo11@gmail.com](mailto:ajaymatharoo11@gmail.com) with the email you signed up with. You'll be given a role that can create Budget Categories and Transactions. In future, access will grow automatically as your contributions build reputation.
3. **Pick a task.** Ask what's open. We're trying to build a place where one can see what open tasks are there but is not yet fully developed [Platform Governance Org](https://www.democracydistributed.com/org/394662382766391297)
4. **Have the source document open.** It's good to have every number we enter come from a published document you can name.

## Detailed Guides

1. [City of Toronto Finances](adding-data-toronto.md)

## Choose how to enter records

| Method | Good for | Watch out for |
|---|---|---|
| **Type it into Corteza** | A handful of records | Slow for anything large. |
| **Corteza's built-in CSV import** | Budget Categories, Items, people, anything without automation | **Don't use it for Transactions.** It skips the automation that creates Ledger entries, so imported Transactions never appear on the chart. |
| **DD's bulk importer script** | Transactions, and any large batch | Needs Python and a sign-in token (below). |
| **Corteza's export** | Seeing what's already there, checking for duplicates, keeping a backup before a big load | Export first if you're unsure whether something exists. |

Corteza's import and export appear on a module's record list. In an import, a field that points to another record (like a parent category) needs that record's ID, not its name. That's one reason the bulk importer exists: it looks IDs up from names for you.

## Using the bulk importer

The importer is a small Python script. It reads a CSV and creates each row through Corteza's API, so the Ledger automation runs for every Transaction, as if you'd typed it in.

**One-time setup**

1. Install Python 3, then run `pip install requests`.
2. Download the [importer folder](https://github.com/democracydistributed/docs/tree/main/tools/corteza-csv-importer) from this repository. Its README has the details and a worked example.

**Each time**

1. **Get a sign-in token.** Log into Corteza in your browser, open the developer tools (F12) → **Network**, click anything in Corteza, find a request to `/api/…`, and copy the long value after `Authorization: Bearer`. It lasts about an hour.
2. **Paste it** into the `bearer_token` field of the config file for your task. The token can do exactly what your own account can do, no more. Never share it, post it or commit it to a repository.
3. **Load the categories first, then the Transactions.** Transactions point to categories, so the categories must exist.
4. **Always dry-run first.** A dry run resolves every lookup and shows what would be created, without creating anything. Fix any errors, then run it live.

Each task folder has a `run-….bat` file that walks you through these choices (Windows), and a README with the tree, the sources and the decisions made.

## Check your work

- **Before a live run:** export the Budget Category list and search for your category numbers, so you don't create duplicates.
- **After loading:** open the organization's page, pick the year, and find your branch on the chart. Click a box to see its Transactions.
- **Totals:** your branch should add up to the source line exactly. If the source and the audited statements differ, don't adjust your numbers.

## Rules that keep the data trustworthy

- **Copy negative numbers as they are.** They're real (usually money that came back).
- **Note anything odd.** A mismatch you report is more useful than one you quietly fix.

## Questions

Email [ajaymatharoo11@gmail.com](mailto:ajaymatharoo11@gmail.com), or ask in [#proj-dd](https://civictechto.slack.com/archives/C09A5S6B7QE) on the Civic Tech Toronto Slack.
