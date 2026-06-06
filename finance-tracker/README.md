# Finance Tracker

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.29-red?logo=streamlit)
![Plotly](https://img.shields.io/badge/Plotly-5.18-purple?logo=plotly)
![License](https://img.shields.io/badge/License-MIT-yellow)

A personal finance tracking application built with Streamlit. Track income and expenses, visualize spending patterns with interactive charts, and manage your budget effectively.

## Features

- Add income and expense transactions with categories
- Interactive dashboard with key financial metrics
- Expense breakdown pie chart by category
- Monthly income vs expenses bar chart
- Transaction history with type filtering
- CSV export and import functionality
- Data persistence using JSON storage
- Responsive design with clean UI

## Tech Stack

| Technology | Purpose |
|-----------|---------|
| Python 3.11 | Backend language |
| Streamlit | Web interface framework |
| Plotly | Interactive charts & graphs |
| Pandas | Data manipulation |
| JSON | Data persistence |

## Installation

1. Clone the repository:
```bash
git clone https://github.com/username/finance-tracker.git
cd finance-tracker
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
streamlit run app.py
```

## Usage

1. **Dashboard**: View summary stats (income, expenses, balance) and charts
2. **Add Transaction**: Record new income or expenses with categories
3. **Transactions**: Browse and filter all transactions
4. **Analytics**: Deep dive into spending patterns
5. **Export/Import**: Download CSV or import from other sources

## Project Structure

```
finance-tracker/
├── app.py              # Main Streamlit application
├── models.py           # Data models (Transaction, Category)
├── database.py         # DatabaseManager for persistence
├── analytics.py        # Chart generation with Plotly
├── utils.py            # Formatters and validators
├── data/
│   └── .gitkeep        # Data directory placeholder
├── tests/
│   ├── test_models.py
│   └── test_database.py
├── requirements.txt    # Python dependencies
└── README.md           # Documentation
```

## Screenshots

> Screenshots will be added after deployment.

## Running Tests

```bash
python -m pytest tests/ -v
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Open a Pull Request

## License

This project is part of my development portfolio.
