# Reading the Sankey (Financial Visualization)

Every organization page on WikiGov opens on its **Finances** tab: one chart showing where the organization's money comes from and where it goes. This page explains how to read it.

## The layout

| Where | What you see |
|---|---|
| **Left** | Revenue: where the money comes from, such as property tax, fees, or transfers from another level of government. |
| **Middle** | The organization itself. All revenue flows in, and all spending flows out. |
| **Right** | Spending: what the money pays for, broken down by category. |

- **Thicker flow, more money.** The height of each bar and the thickness of each flow match its dollar amount.
- **Amounts are on the chart.** Each bar shows its amount and name without hovering.
- **Columns follow the organization's own categories.** An organization with deeper budget categories gets more columns, for example *Parks* → *Construction Services* → individual payments.

## Small items are grouped, not hidden

When a column has many small items, their labels would overlap into an unreadable stack. Those items are drawn as one band labelled **"N more"**. Nothing is merged or dropped: click the band to see every item in it, each with its own name and amount.

On a phone, the chart starts as a simple list of bars you can tap. Use **View full chart** to see the full flow diagram.

## Click to go deeper

1. **Click a category** to open a side panel listing what's inside it.
2. **Keep clicking** to move down through sub-categories until you reach individual payments.
3. **Click a payment** to open its **trace**: the chain of decisions behind that money, as far as it has been linked.

## What a trace shows

Different kinds of money are authorized in different ways, so the trace looks different depending on what you click.

| You clicked | What the trace leads to |
|---|---|
| **Spending on a contract or project** (e.g. a construction award) | The Project the payment belongs to, then the council Item that approved it, and the vote. |
| **Tax revenue** (e.g. residential property tax) | The by-law that sets the tax. From there, the chain leads to the council decision that passed the by-law, where that link has been made. |
| **Revenue with no vote behind it** (e.g. payments in lieu of taxes, supplementary assessments) | Nothing, and that is correct. This money is set by formula, not by a decision, so there is no vote to show. |
| **A total** (all revenue, all spending) | A summary, not a single chain. |

## Gaps are part of the picture

Most chains are not complete yet. Official sources usually publish the decision at one end and the money at the other, and leave the steps in between unconnected.

When a link is missing, the trace shows the gap instead of guessing. A payment might show its Project, followed by **"Decision not linked"**, because no one has yet connected that Project to the council Item that approved it. Every gap is a piece of work someone can do. See [Get involved](../contribute/get-involved.md).

## Coming later

- **Planned vs. actual.** Where an organization has a budget, the chart will show the amount a decision authorized next to what has actually been spent, so you can see whether spending matched the plan.
- **Confidence labels.** Each figure will be labelled by how much is known about it: verified, estimated, not reported, or held by the government but not released.

**Next:** [How the money chart is built →](../build/sankey.md)
