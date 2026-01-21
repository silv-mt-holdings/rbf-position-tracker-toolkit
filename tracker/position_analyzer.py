"""
RBF Position Analyzer

Detects and analyzes RBF positions from classified bank transactions.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict
from datetime import date, timedelta
from collections import defaultdict


@dataclass
class RBFPosition:
    """Represents an identified RBF position"""
    rbf_name: str
    aka_name: str
    payment_amount: float = 0.0
    payment_frequency: str = "unknown"
    estimated_balance: Optional[float] = None
    transaction_count: int = 0
    first_seen: Optional[date] = None
    last_seen: Optional[date] = None
    flags: List[str] = field(default_factory=list)
    avg_monthly_payment: float = 0.0

    def calculate_monthly_payment(self):
        """Calculate average monthly payment based on frequency"""
        if self.payment_frequency == "daily":
            self.avg_monthly_payment = self.payment_amount * 21
        elif self.payment_frequency == "weekly":
            self.avg_monthly_payment = self.payment_amount * 4
        else:
            self.avg_monthly_payment = self.payment_amount


@dataclass
class StackingAnalysis:
    """Stacking risk analysis"""
    position_count: int
    total_monthly_obligation: float
    stacking_risk_score: float
    positions: List[RBFPosition]


class PositionTracker:
    """
    Tracks RBF positions from classified transactions.
    """

    def find_positions(self, classified_transactions) -> List[RBFPosition]:
        """
        Identify RBF positions from classified transactions.

        Args:
            classified_transactions: List of ClassifiedTransaction objects

        Returns:
            List of RBFPosition objects
        """
        # Group by RBF name
        rbf_groups = defaultdict(list)

        for txn in classified_transactions:
            if txn.mca_match:
                rbf_groups[txn.mca_match].append(txn)

        # Analyze each RBF
        positions = []
        for rbf_name, txns in rbf_groups.items():
            if not txns:
                continue

            # Calculate stats
            amounts = [abs(t.amount) for t in txns]
            avg_amount = sum(amounts) / len(amounts)
            dates = sorted([t.date for t in txns])

            # Detect frequency
            frequency = self._detect_frequency(dates)

            # Create position
            position = RBFPosition(
                rbf_name=rbf_name,
                aka_name=txns[0].description[:50],
                payment_amount=avg_amount,
                payment_frequency=frequency,
                transaction_count=len(txns),
                first_seen=min(dates),
                last_seen=max(dates)
            )

            position.calculate_monthly_payment()
            positions.append(position)

        return positions

    def analyze_stacking(self, positions: List[RBFPosition]) -> StackingAnalysis:
        """
        Analyze stacking risk from multiple positions.

        Args:
            positions: List of RBF positions

        Returns:
            StackingAnalysis object
        """
        total_monthly = sum(p.avg_monthly_payment for p in positions)

        # Calculate stacking risk score (0-100)
        # 1 position = 0, 2 = 30, 3 = 60, 4+ = 90
        if len(positions) <= 1:
            risk_score = 0.0
        elif len(positions) == 2:
            risk_score = 30.0
        elif len(positions) == 3:
            risk_score = 60.0
        else:
            risk_score = 90.0

        return StackingAnalysis(
            position_count=len(positions),
            total_monthly_obligation=total_monthly,
            stacking_risk_score=risk_score,
            positions=positions
        )

    def _detect_frequency(self, payment_dates: List[date]) -> str:
        """
        Detect payment frequency from dates.

        Args:
            payment_dates: Sorted list of payment dates

        Returns:
            Frequency string: 'daily', 'weekly', 'monthly', or 'unknown'
        """
        if len(payment_dates) < 2:
            return "unknown"

        # Calculate gaps between payments
        gaps = []
        for i in range(1, len(payment_dates)):
            gap = (payment_dates[i] - payment_dates[i-1]).days
            gaps.append(gap)

        avg_gap = sum(gaps) / len(gaps)

        # Classify
        if avg_gap <= 2:
            return "daily"
        elif 5 <= avg_gap <= 9:
            return "weekly"
        elif 25 <= avg_gap <= 35:
            return "monthly"
        else:
            return "unknown"
