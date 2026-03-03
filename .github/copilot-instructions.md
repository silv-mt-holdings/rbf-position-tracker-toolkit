# RBF Position Tracker Toolkit - AI Coding Guidelines

## Project Overview

**rbf-position-tracker-toolkit** is a pure functional library for detecting and analyzing existing RBF/MCA positions from transactions.

**Core Purpose**: Identify RBF payments, estimate balances, calculate stacking risk.

**Architecture Pattern**: **Functional Core** (Pure Functions, No I/O)

---

## Functional Core Principles

### ✅ What This Toolkit SHOULD Do
- Accept transaction lists as input
- Detect RBF payment patterns
- Calculate position estimates
- Return stacking analysis results

### ❌ What This Toolkit MUST NOT Do
- File I/O operations
- Database connections
- HTTP requests
- State mutations

---

## Architecture

```
rbf-position-tracker-toolkit/
├── tracker/
│   ├── position_analyzer.py    # Main position detection
│   └── payment_detector.py     # Payment pattern matching
├── models/
│   └── positions.py            # Position, StackingAnalysis
├── data/
│   └── lender_list.json        # Known RBF/MCA lenders
└── tests/
    └── test_tracker.py
```

---

## Core Models

```python
@dataclass(frozen=True)
class RBFPosition:
    lender_name: str
    payment_amount: Decimal
    frequency: str              # "daily", "weekly", "monthly"
    avg_monthly_payment: Decimal
    estimated_balance: Decimal
    payment_count: int

@dataclass(frozen=True)
class StackingAnalysis:
    total_positions: int
    total_monthly_payment: Decimal
    stacking_risk: str          # "low", "medium", "high"
    positions: List[RBFPosition]
```

---

## Key Functional Patterns

### Position Detection

```python
def find_positions(
    transactions: List[Transaction]
) -> List[RBFPosition]:
    """
    Detect RBF positions from transaction history.

    Args:
        transactions: List of classified transactions

    Returns:
        List of detected RBF positions
    """
    mca_payments = [
        t for t in transactions
        if t.type == TransactionType.MCA_PAYMENT
    ]

    positions = {}
    for payment in mca_payments:
        lender = extract_lender_name(payment.description)
        if lender not in positions:
            positions[lender] = []
        positions[lender].append(payment)

    return [
        analyze_position(lender, payments)
        for lender, payments in positions.items()
    ]
```

---

## Testing

```python
def test_detect_daily_payments():
    payments = [
        Transaction(date="2024-01-01", description="ONDK PAYMENT", amount=-450),
        Transaction(date="2024-01-02", description="ONDK PAYMENT", amount=-450),
        Transaction(date="2024-01-03", description="ONDK PAYMENT", amount=-450)
    ]
    position = analyze_position("ONDK", payments)
    assert position.frequency == "daily"
    assert position.avg_monthly_payment == Decimal("13500")  # 450 * 30
```

---

## Integration with Risk-Model-01

```python
# Risk-Model-01/api.py
from tracker.position_analyzer import PositionTracker

tracker = PositionTracker()
positions = tracker.find_positions(classified_transactions)
```

---

## Version

**v1.0** - Functional Core Extraction (January 2026)

**Author**: IntensiveCapFi / Silv MT Holdings
