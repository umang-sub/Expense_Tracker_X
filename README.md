# Smart Expense Tracker

<p align="center">
  <img src="assets/expense-tracker-hero.svg" alt="Smart Expense Tracker — luminous finance dashboard" width="100%">
</p>

<p align="center">
  <strong>Turn everyday transactions into clear financial insight.</strong><br>
  A colourful, menu-driven Python expense tracker with validation, CSV persistence, analytics, filtering, reporting, and rich visualisations.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&amp;logo=python&amp;logoColor=white" alt="Python 3.10 or later">
  <img src="https://img.shields.io/badge/Data-Pandas%20%2B%20NumPy-150458?style=for-the-badge&amp;logo=pandas&amp;logoColor=white" alt="Pandas and NumPy">
  <img src="https://img.shields.io/badge/Charts-Matplotlib%20%2B%20Seaborn-7C3AED?style=for-the-badge" alt="Matplotlib and Seaborn">
  <img src="https://img.shields.io/badge/Interface-Terminal-34D399?style=for-the-badge&amp;logo=gnometerminal&amp;logoColor=white" alt="Terminal interface">
</p>

> **The big idea:** record an expense in seconds, then use totals, category trends, filters, and charts to make more intentional spending decisions.

## Why this project shines

| Capability | What it gives you |
| --- | --- |
| ✅ Reliable entry | Dates, positive amounts, and categories are validated before a record is accepted. |
| 💾 Durable data | Every successful addition is saved straight into `expenses.csv`. |
| 🧠 Useful analysis | NumPy calculates totals and averages; Pandas groups monthly and category-level insights. |
| 🔎 Flexible discovery | Filter by category, date, month, minimum amount, or maximum amount. |
| 📈 Visual storytelling | Choose bar, line, pie, and histogram views—or launch all four in sequence. |
| 🧾 Readable reporting | Get a ranked, percentage-based breakdown in the terminal. |

<p align="center">
  <img src="assets/data-flow.svg" alt="Log, persist, analyse, and visualise workflow" width="100%">
</p>

## Contents

- [Quick start](#quick-start)
- [What you can do](#what-you-can-do)
- [Visual analytics](#visual-analytics)
- [Data format](#data-format)
- [Project structure](#project-structure)
- [How it works](#how-it-works)
- [Troubleshooting](#troubleshooting)

## Quick start

### 1. Get into the project

```bash
cd /Users/umang/Documents/RW/expencse_tracker
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate       # macOS / Linux
# .venv\Scripts\activate        # Windows PowerShell
```

### 3. Install the data and charting tools

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Launch the tracker

```bash
python expense_tracker.py
```

You will be welcomed by the interactive menu:

```text
1. Log a New Expense
2. View Expense Summary
3. Generate Detailed Report
4. Filter Expenses
5. View Data Visualizations
6. Show All Raw Data
7. Exit Application
```

## What you can do

### Log an expense

Select **1** and enter a date, positive amount, recognised category, and description. Leaving the date blank uses today’s date; leaving the description blank stores `N/A`.

```text
Enter Date (YYYY-MM-DD) or press Enter for today: 2026-08-26
Enter Amount ($): 18.50
Valid Categories: Food, Transport, Utilities, Entertainment, Shopping, Health, Other
Enter Category: Food
Enter Description (optional): Breakfast
Expense added successfully.
```

Only these categories are accepted: `Food`, `Transport`, `Utilities`, `Entertainment`, `Shopping`, `Health`, and `Other`.

### Explore the numbers

| Menu option | Result |
| --- | --- |
| **2 — View Expense Summary** | Displays total spending, mean transaction value, and the leading category. |
| **3 — Generate Detailed Report** | Prints transaction count, total, average, highest and lowest expenses, monthly average, plus a ranked category table with percentages. |
| **4 — Filter Expenses** | Narrow the ledger by category, exact date, `YYYY-MM` month, or an amount threshold. |
| **6 — Show All Raw Data** | Prints the current cleaned dataset directly in the terminal. |

### Sample-data snapshot

The included sample ledger contains **250** transactions across **7** categories. Its figures will change as you add entries, but the starting data totals **$47,085.46**, with **Shopping** as the largest category.

## Visual analytics

<p align="center">
  <img src="assets/analytics-suite.svg" alt="Illustrated suite of the four available chart types" width="100%">
</p>

Choose **5 — View Data Visualizations** to open any of the following Matplotlib/Seaborn charts:

| View | Best question it answers |
| --- | --- |
| **Bar chart** | Which categories take the biggest share of my money? |
| **Line graph** | How is spending changing day by day? |
| **Pie chart** | What is the proportional split between categories? |
| **Histogram** | Which transaction sizes occur most often? |

> Charts open in a separate plotting window. Close that window to return to the menu; selecting “Show All” presents the charts one after another.

## Data format

`expenses.csv` is the project’s simple, portable storage layer. It must have these column names:

| Column | Format | Example | Notes |
| --- | --- | --- | --- |
| `Date` | `YYYY-MM-DD` | `2026-08-26` | Invalid or missing dates are removed when loading. |
| `Amount` | Positive number | `18.50` | Zero, negative, non-numeric, and missing amounts are removed when loading. |
| `Category` | Approved category | `Food` | A category is required; new interactive entries also have to use the approved list. |
| `Description` | Text | `Breakfast` | Optional context for the transaction. |

The loader cleans incomplete or invalid rows, normalises dates to `YYYY-MM-DD`, and resets the DataFrame index before the app is ready to use.

## Project structure

```text
expencse_tracker/
├── expense_tracker.py       # Application, validation, analysis, charts, and CLI menu
├── expenses.csv             # Starter expense ledger; updated when you add an expense
├── requirements.txt         # Runtime dependencies
├── README.md                # Project guide
└── assets/
    ├── expense-tracker-hero.svg  # README hero artwork
    ├── analytics-suite.svg       # Chart-suite illustration
    └── data-flow.svg             # Processing workflow illustration
```

## How it works

The program is deliberately organised into focused classes:

| Class | Responsibility |
| --- | --- |
| `ExpenseValidator` | Confirms date syntax, positive numerical amounts, and valid categories. |
| `ExpenseTracker` | Owns the DataFrame, loading/cleaning, saving, adding, analysis, filtering, and reporting. |
| `ExpenseVisualizer` | Generates the four charts from the current DataFrame. |
| `ExpenseAppUI` | Presents the interactive menu and translates user choices into tracker actions. |

When a new expense passes validation, it is appended to the in-memory Pandas DataFrame, written to `expenses.csv`, and immediately supplied to the visualiser. No restart is needed before viewing updated summaries or charts.

## Programmatic use

The tracker can be imported for quick experiments or automation too:

```python
from expense_tracker import ExpenseTracker

tracker = ExpenseTracker("expenses.csv")
tracker.add_expense("2026-08-26", "18.50", "Food", "Breakfast")

summary = tracker.get_summary()
print(summary["total_expense"])

august = tracker.filter_expenses("month", "2026-08")
print(august)
```

Available filter types are `category`, `date`, `month`, `amount_greater`, and `amount_less`.

## Requirements

- Python **3.10+** recommended
- `pandas>=2.2`
- `numpy>=1.26`
- `matplotlib>=3.9`
- `seaborn>=0.13`

The exact package requirements live in [`requirements.txt`](requirements.txt).

## Troubleshooting

| Symptom | Likely fix |
| --- | --- |
| `ModuleNotFoundError` | Activate the virtual environment and run `python -m pip install -r requirements.txt`. |
| A chart does not appear | Run from a local terminal with a graphical desktop session; close any earlier chart window before the next one appears. |
| “Invalid date format” | Use a real calendar date in `YYYY-MM-DD` form, such as `2026-08-26`. |
| “Invalid category” | Choose one of the seven listed categories, matching its spelling. |
| Data looks missing | Check that `expenses.csv` is in the same directory where you run `expense_tracker.py`. |

## Quality checklist

- [x] Object-oriented, modular organisation
- [x] Control-flow based validation and error handling
- [x] Pandas data loading, cleaning, filtering, and grouping
- [x] NumPy calculations for core summary metrics
- [x] Matplotlib and Seaborn visualisations
- [x] Sample CSV dataset included
- [x] Self-contained, high-resolution SVG documentation artwork

---

<p align="center">
  <strong>Log with intent. Read the pattern. Spend with clarity. ✨</strong>
</p>

## Project demonstration

Watch the complete project video: [Smart Expense Tracker demo](https://drive.google.com/file/d/10XmvjQaFzqHRRjjSg3e7P_88JZkqzwD4/view?usp=sharing)
