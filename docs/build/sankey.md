# The Sankey (Financial Visualization)

How the money chart on an organization page is built, how its trace finds the decision behind a payment, and the design rules anyone changing either should know. For how to *read* the chart, see [Reading the money chart](../use/reading-the-sankey.md).

## From records to chart

```
Corteza records                 Gateway endpoint              Web app
────────────────                ─────────────────             ─────────────
Budget Categories   ──┐
(the org's own tree)  │         GET /sankey?orgId=…           Turns the tree
                      ├──────►  returns a nested    ───────►  into flows and
Ledger entries      ──┘         revenue tree and              draws the chart
(each payment)                  spending tree
```

1. **Start from the organization's Budget Categories.** Each organization has its own category tree. Revenue categories form one side and spending categories the other. The tree can be any depth, and the chart grows a column for each level.
2. **Add up the payments.** Each payment has Ledger entries, and each entry belongs to a category. Payments are added up from the bottom of the tree to the top. Only the bottom level of the tree holds payments; higher levels are containers.
3. **Drop what's empty.** A category with no payments under it is left out.
4. **Return a nested tree.** The endpoint returns revenue and spending as two nested trees. The deepest level lists individual payments, each with a flag saying whether a decision chain is linked. The exact shape is in the [API reference](api-reference.md).
5. **Draw it.** The web app turns the tree into nodes and flows and lays them out. Small items are grouped into "N more" bands for readability. This is visual only: no data is merged, and clicking a band lists every item in it.

**Double-entry, counted once.** Every payment creates two Ledger entries, a debit and a credit. The chart counts only the entry that belongs to the organization's own accounts, so each payment appears once.

## How a trace finds its decision

When someone clicks a payment, the trace endpoint walks from that Ledger entry back to the decision behind it. Different kinds of money are authorized in different ways, so the trace follows different routes.

| Kind of money | Route | Example |
|---|---|---|
| **Spending on a project** | Ledger entry → Transaction → Project → the Item that approved the Project → Vote | A construction contract paid in milestones |
| **Spending straight from a decision** | Ledger entry → Transaction → Item → Vote | A grant or fund release where the vote itself is the trigger and no project is created |
| **Revenue under a standing rule** | Ledger entry → by-law → Amendment → Item → Vote | Property tax: the by-law sets the rate, and the Item that passed the by-law carries the vote |
| **Revenue with no rule behind it** | None | Payments in lieu of taxes: set by formula, so a blank authority is correct, not missing data |
| **Routine delegated spending** | No Item. Authority comes from the staff role of the person who recorded the payment (modelled, not yet shown in the trace) | Small operating purchases a staff role may make without a vote |

**Partial chains are normal.** If some links are missing, the trace returns what it has. For example, a payment can show its Project even when no one has yet linked that Project to its Item. The empty link is shown as a gap, not hidden. See [The chain of accountability](../understand/chain-of-accountability.md).

## Design rules

Rules the chart and trace depend on. Breaking one usually doesn't cause an error; it quietly produces a wrong answer.

**1. The rule is recorded when the money moves.** For revenue, the by-law in force is copied onto the payment at the moment it's recorded, and the trace reads that copy. It never looks up the category's *current* by-law. If the by-law changes later, older payments still show the rule that applied when they were made. A live lookup would quietly rewrite history.

- *Today:* each category holds its current by-law, which is copied onto new payments. A historical payment entered today is left as "authority pending" rather than given the wrong, current by-law.
- *Later:* a dated link between categories and by-laws, so a backdated payment picks up the by-law that was in force on its date.

**2. A category gets its authority one way, not two.** Each budget category is authorized by exactly one of:

| Route | When | Example |
|---|---|---|
| **A standing by-law** | The law compels the money without a fresh vote each year | Residential property tax |
| **Funding Allocations** | The money needs a decision each budget cycle. Each cycle gets its own allocation, so nothing goes stale year to year | A city's annual operating transfer to its library board |
| **Neither** | Set by formula, with no decision behind it | Payments in lieu of taxes |

Nothing in Corteza enforces this yet. The planned fix is an explicit authority-type field on the category (by-law / decision / none), so "none" is a deliberate choice rather than an ambiguous blank.

**3. A project already points to its decision.** Spending on a project reaches its Item through the Project. Never also copy an Item onto that payment from a Funding Allocation, or the payment ends up wired to its decision twice. Copy an Item from an allocation only when the payment has no Project and no Item set by hand.

**4. When both exist, the Project wins.** If a payment has a Project, the trace takes the Item from the Project. It falls back to an Item recorded directly on the payment only when there is no Project.

**5. Planned and actual meet at the category.** Planned amounts (Funding Allocations) and actual amounts (Ledger entries) are each added up per budget category and compared there. No payment needs to be linked to a specific allocation.

## Planned

These are designed but not live.

- **Planned vs. actual.** When a decision commits money to a purpose, a [Funding Allocation](key-concepts.md) records the amount. The chart will draw that amount as a grey flow, and fill it with colour as payments arrive. If spending runs past the allocation, the colour overflows the grey: an instant visual signal. Each allocation moves through these states:

  | Status | What the chart will show |
  |---|---|
  | Planned | A grey flow for the full amount. The decision passed, nothing spent yet. |
  | Committed | Grey, with a small mark of colour. A contract has been awarded. |
  | Active | Colour filling the grey as each payment arrives. |
  | Complete | Full colour. All expected spending recorded. |
  | Cancelled | The flow disappears. The decision failed or was withdrawn. |

  A decision that moves no money, such as a policy declaration, has no allocation and never appears on the chart.

- **Transfers to agencies.** A third trace route, for money a council allocates to an agency each year: from the payment's category to its Funding Allocation, then to the budget decision. Where a category has allocations from several budget cycles, the trace will need a rule for which one to use, likely the one closest in date to the payment.
- **Confidence labels.** Each figure labelled verified, estimated, not reported, or held by the government but not released, so gaps show as gaps instead of guesses.

**Next:** [API reference →](api-reference.md)
