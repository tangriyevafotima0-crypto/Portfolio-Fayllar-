"""Analytics and chart generation module for the Finance Tracker."""

from collections import defaultdict
from typing import Optional
import plotly.graph_objects as go
import plotly.express as px
from models import Transaction, TransactionType


def calculate_summary_stats(transactions: list[Transaction]) -> dict:
    """Calculate summary statistics for all transactions.

    Args:
        transactions: List of Transaction objects.

    Returns:
        Dictionary containing total_income, total_expenses, balance,
        and transaction_count.
    """
    total_income = sum(
        t.amount for t in transactions
        if t.transaction_type == TransactionType.INCOME
    )
    total_expenses = sum(
        t.amount for t in transactions
        if t.transaction_type == TransactionType.EXPENSE
    )

    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "balance": total_income - total_expenses,
        "transaction_count": len(transactions)
    }


def create_expense_pie_chart(transactions: list[Transaction]) -> Optional[go.Figure]:
    """Create a pie chart showing expense distribution by category.

    Args:
        transactions: List of Transaction objects.

    Returns:
        Plotly Figure object, or None if no expenses exist.
    """
    expenses = [t for t in transactions if t.transaction_type == TransactionType.EXPENSE]

    if not expenses:
        return None

    category_totals: dict[str, float] = defaultdict(float)
    for t in expenses:
        category_totals[t.category] += t.amount

    fig = go.Figure(data=[go.Pie(
        labels=list(category_totals.keys()),
        values=list(category_totals.values()),
        hole=0.4,
        textinfo="label+percent"
    )])

    fig.update_layout(
        title="Expenses by Category",
        showlegend=True,
        height=400
    )

    return fig


def create_monthly_bar_chart(transactions: list[Transaction]) -> Optional[go.Figure]:
    """Create a grouped bar chart comparing monthly income and expenses.

    Args:
        transactions: List of Transaction objects.

    Returns:
        Plotly Figure object, or None if no transactions exist.
    """
    if not transactions:
        return None

    monthly_income: dict[str, float] = defaultdict(float)
    monthly_expenses: dict[str, float] = defaultdict(float)

    for t in transactions:
        month_key = t.date[:7]  # YYYY-MM format
        if t.transaction_type == TransactionType.INCOME:
            monthly_income[month_key] += t.amount
        else:
            monthly_expenses[month_key] += t.amount

    all_months = sorted(set(list(monthly_income.keys()) + list(monthly_expenses.keys())))

    fig = go.Figure()

    fig.add_trace(go.Bar(
        name="Income",
        x=all_months,
        y=[monthly_income.get(m, 0) for m in all_months],
        marker_color="#27ae60"
    ))

    fig.add_trace(go.Bar(
        name="Expenses",
        x=all_months,
        y=[monthly_expenses.get(m, 0) for m in all_months],
        marker_color="#e74c3c"
    ))

    fig.update_layout(
        title="Monthly Income vs Expenses",
        xaxis_title="Month",
        yaxis_title="Amount",
        barmode="group",
        height=400
    )

    return fig


def get_top_categories(
    transactions: list[Transaction],
    trans_type: TransactionType,
    limit: int = 5
) -> list[tuple[str, float]]:
    """Get top spending or earning categories.

    Args:
        transactions: List of Transaction objects.
        trans_type: Transaction type to filter.
        limit: Maximum number of categories to return.

    Returns:
        List of (category_name, total_amount) tuples sorted by amount.
    """
    filtered = [t for t in transactions if t.transaction_type == trans_type]

    category_totals: dict[str, float] = defaultdict(float)
    for t in filtered:
        category_totals[t.category] += t.amount

    sorted_categories = sorted(
        category_totals.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return sorted_categories[:limit]
