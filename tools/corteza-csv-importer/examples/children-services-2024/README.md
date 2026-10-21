# Example: Toronto Children's Services, 2024

**A worked example. Before any live run, check whether `SFS-000` already exists in Corteza; if it does, this has been loaded and must not be run again.**

Source: Toronto's 2024 Financial Information Return (FIR), Schedule 40, line 1230 *Child Care and Early Years Learning*, column N (*Total Expenses Before Adjustments*), split across its seven spending columns. Total $926,768,606.

Why Children's Services: the City's 2024 Operating Variance Report (Appendix B) shows Children's Services actual gross spending of $930.4M, within 0.4% of the FIR line.

```
SFS-000  Social & Family Services          (parent)
└── SFS-100  Children's Services            $926,768,606
    ├── SFS-101 Salaries and Benefits       $129,842,016
    ├── SFS-102 Interest on Long Term Debt      $51,367
    ├── SFS-103 Materials                   −$32,942,351   (negative in the FIR itself)
    ├── SFS-104 Contracted Services         $825,933,041
    ├── SFS-105 Rents & Financial             $3,121,970
    ├── SFS-106 External Transfers                $2,702
    └── SFS-107 Amortization                    $759,861
```

Fields worth noticing in the CSVs: `Department` is set because a source links the line to the division; `Item` is blank because the authorizing decision isn't verified; every `Description` names the source line and column.
