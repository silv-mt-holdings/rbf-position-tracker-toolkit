# rbf-position-tracker-toolkit

RBF position tracking toolkit - Detects existing RBF payments, calculates stacking risk, and payment patterns.

## Features

- Identify RBF payments in transaction history
- Calculate payment frequency (daily, weekly, monthly)
- Estimate remaining balance
- Calculate stacking risk score
- Group payments by lender
- Detect payment irregularities

## Installation

```bash
pip install git+https://github.com/silv-mt-holdings/rbf-position-tracker-toolkit.git
```

## Quick Start

```python
from tracker.position_analyzer import PositionTracker

tracker = PositionTracker()
positions = tracker.find_positions(classified_transactions)

for pos in positions:
    print(f"RBF: {pos.rbf_name}")
    print(f"Payment: ${pos.payment_amount:,.2f} {pos.payment_frequency}")
    print(f"Monthly Obligation: ${pos.avg_monthly_payment:,.2f}")

stacking_analysis = tracker.analyze_stacking(positions)
print(f"Stacking Risk Score: {stacking_analysis.stacking_risk_score:.1f}/100")
```
