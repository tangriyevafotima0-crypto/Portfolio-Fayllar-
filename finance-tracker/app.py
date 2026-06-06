"""Streamlit main application for the Finance Tracker."""

import streamlit as st
from models import Transaction, TransactionType
from database import DatabaseManager, DatabaseError
from analytics import (
    create_expense_pie_chart,
    create_monthly_bar_chart,
    calculate_summary_stats
)
from utils import format_currency, validate_amount


def main() -> None:
    """Run the Finance Tracker Streamlit application."""
    st.set_page_config(
        page_title="Finance Tracker",
        page_icon="💰",
        layout="wide"
    )

    db = DatabaseManager()

    st.title("💰 Finance Tracker")

    page = st.sidebar.selectbox(
        "Navigation",
        ["Dashboard", "Add Transaction", "Transactions", "Analytics", "Export/Import"]
    )

    if page == "Dashboard":
        show_dashboard(db)
    elif page == "Add Transaction":
        show_add_transaction(db)
    elif page == "Transactions":
        show_transactions(db)
    elif page == "Analytics":
        show_analytics(db)
    elif page == "Export/Import":
        show_export_import(db)


def show_dashboard(db: DatabaseManager) -> None:
    """Display the dashboard with summary statistics.

    Args:
        db: Database manager instance.
    """
    st.header("Dashboard")

    transactions = db.get_all_transactions()
    stats = calculate_summary_stats(transactions)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Income", format_currency(stats["total_income"]))
    with col2:
        st.metric("Total Expenses", format_currency(stats["total_expenses"]))
    with col3:
        st.metric("Balance", format_currency(stats["balance"]))
    with col4:
        st.metric("Transactions", str(stats["transaction_count"]))

    if transactions:
        col_left, col_right = st.columns(2)
        with col_left:
            st.subheader("Expense Breakdown")
            expense_chart = create_expense_pie_chart(transactions)
            if expense_chart:
                st.plotly_chart(expense_chart, use_container_width=True)
            else:
                st.info("No expenses to display.")

        with col_right:
            st.subheader("Monthly Overview")
            monthly_chart = create_monthly_bar_chart(transactions)
            if monthly_chart:
                st.plotly_chart(monthly_chart, use_container_width=True)
    else:
        st.info("No transactions yet. Add your first transaction!")


def show_add_transaction(db: DatabaseManager) -> None:
    """Display the add transaction form.

    Args:
        db: Database manager instance.
    """
    st.header("Add Transaction")

    with st.form("transaction_form"):
        trans_type = st.selectbox(
            "Type",
            options=[TransactionType.INCOME.value, TransactionType.EXPENSE.value]
        )
        amount = st.number_input("Amount", min_value=0.01, step=0.01)
        category = st.selectbox(
            "Category",
            options=Transaction.get_default_categories(
                TransactionType(trans_type)
            )
        )
        description = st.text_input("Description", placeholder="Optional note")
        date = st.date_input("Date")

        submitted = st.form_submit_button("Add Transaction", type="primary")

        if submitted:
            try:
                validate_amount(amount)
                transaction = Transaction(
                    amount=amount,
                    category=category,
                    transaction_type=TransactionType(trans_type),
                    description=description,
                    date=date.isoformat()
                )
                db.add_transaction(transaction)
                st.success(f"Added {trans_type}: {format_currency(amount)} ({category})")
            except (ValueError, DatabaseError) as e:
                st.error(f"Error: {e}")


def show_transactions(db: DatabaseManager) -> None:
    """Display all transactions with filtering options.

    Args:
        db: Database manager instance.
    """
    st.header("Transaction History")

    transactions = db.get_all_transactions()

    if not transactions:
        st.info("No transactions found.")
        return

    filter_type = st.selectbox(
        "Filter by type:",
        ["All", TransactionType.INCOME.value, TransactionType.EXPENSE.value]
    )

    filtered = transactions
    if filter_type != "All":
        filtered = [t for t in transactions if t.transaction_type.value == filter_type]

    for t in filtered:
        icon = "🟢" if t.transaction_type == TransactionType.INCOME else "🔴"
        col1, col2, col3, col4 = st.columns([1, 2, 2, 1])
        with col1:
            st.write(f"{icon} {t.date}")
        with col2:
            st.write(f"**{t.category}**")
        with col3:
            st.write(t.description or "-")
        with col4:
            st.write(format_currency(t.amount))


def show_analytics(db: DatabaseManager) -> None:
    """Display analytics charts and insights.

    Args:
        db: Database manager instance.
    """
    st.header("Analytics")

    transactions = db.get_all_transactions()
    if not transactions:
        st.info("Add some transactions to see analytics.")
        return

    expense_chart = create_expense_pie_chart(transactions)
    if expense_chart:
        st.plotly_chart(expense_chart, use_container_width=True)

    monthly_chart = create_monthly_bar_chart(transactions)
    if monthly_chart:
        st.plotly_chart(monthly_chart, use_container_width=True)


def show_export_import(db: DatabaseManager) -> None:
    """Handle CSV export and import functionality.

    Args:
        db: Database manager instance.
    """
    st.header("Export / Import")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Export to CSV")
        if st.button("Export All Transactions"):
            csv_data = db.export_to_csv()
            if csv_data:
                st.download_button(
                    label="Download CSV",
                    data=csv_data,
                    file_name="transactions.csv",
                    mime="text/csv"
                )
            else:
                st.info("No transactions to export.")

    with col2:
        st.subheader("Import from CSV")
        uploaded = st.file_uploader("Choose a CSV file", type="csv")
        if uploaded is not None:
            try:
                content = uploaded.read().decode("utf-8")
                count = db.import_from_csv(content)
                st.success(f"Imported {count} transactions successfully!")
            except (DatabaseError, ValueError) as e:
                st.error(f"Import error: {e}")


if __name__ == "__main__":
    main()
