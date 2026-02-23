# GenAI Invoice Chatbot

I built this chatbot to help me manage invoices for my freelance business. Instead of writing SQL queries manually, I just ask questions in plain English and the AI figures out how to get the data I need.

## What it does

You type a question like "How much does XYZ Tech owe me?" and the chatbot generates the appropriate SQL query, runs it against the database, and gives you a human-readable answer. The whole thing runs locally in your browser using Streamlit.

The AI uses function calling under the hood. It doesn't execute code directly - it tells the application what query to run, the app executes it, and then the AI formats the response. This keeps things safe and predictable.

## Getting started

Clone the repo and set up a virtual environment:

```bash
git clone https://github.com/zielu2021/genai-invoice-chatbot.git
cd genai-invoice-chatbot
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # macOS/Linux
```

Install the dependencies:

```bash
pip install openai python-dotenv streamlit
```

Create a `.env` file with your API key:

```
AZURE_OPENAI_API_KEY=your-api-key-here
```

Set up the database and run the app:

```bash
python create_db.py
streamlit run chatbot.py
```

Open `http://localhost:8501` in your browser.

## How the database is structured

The database has a few related tables that model a typical invoicing workflow:

**customers** holds client information - name, tax ID, email, phone, city, and country. I have 12 sample customers across Poland, Germany, and Sweden.

**invoices** tracks each invoice with its number, customer reference, dates, and status. Status can be paid, unpaid, overdue, draft, or cancelled. There's also fields for payment date, payment method, and notes.

**invoice_items** contains the line items for each invoice - description, quantity, unit price, and VAT rate. The gross amount is calculated as quantity times unit price times (1 + VAT rate).

**service_categories** groups services into categories like Development, Consulting, Training, and so on.

**payments** records when payments come in, including the amount, date, method, and a reference number.

**recurring_templates** stores templates for recurring invoices - useful for retainer clients who get billed monthly or quarterly.

The sample data includes 35 invoices spanning 2024 through 2026, with 45 line items and 20 payment records.

## Things you can ask

Here are some questions that work well:

- What is my total revenue?
- Which invoices are overdue?
- Show revenue by customer
- How many unpaid invoices do I have?
- What services did I provide?
- Monthly revenue in 2024
- Show payment history
- Top 5 customers by revenue
- Compare 2024 vs 2025 revenue
- How much does John Smith owe me?

The chatbot only runs SELECT queries. If you try to modify data, it politely refuses.

## Tech stack

- Python 3.13
- GPT-4o via EPAM DIAL (Azure OpenAI)
- OpenAI Python SDK
- SQLite for the database
- Streamlit for the web interface
- python-dotenv for configuration

## Project structure

```
genai-invoice-chatbot/
├── .env                  # API key (not committed)
├── .gitignore
├── chatbot.py            # Main Streamlit application
├── create_db.py          # Database creation and seeding
├── invoices.db           # SQLite database (generated)
├── screenshots/          # Demo screenshots
│   ├── 01_dashboard_metrics.png
│   ├── 02_overdue_invoices.png
│   ├── 03_monthly_revenue.png
│   ├── 04_dml_protection.png
│   └── 05_function_calling_code.png
└── README.md
```

## Screenshots

### Dashboard with metrics
![Dashboard metrics](screenshots/01_dashboard_metrics.png)

### Overdue invoices query
![Overdue invoices](screenshots/02_overdue_invoices.png)

### Monthly revenue breakdown
![Monthly revenue](screenshots/03_monthly_revenue.png)

### DML protection in action
![DML protection](screenshots/04_dml_protection.png)

### Function calling implementation
![Function calling code](screenshots/05_function_calling_code.png)

## Safety considerations

The chatbot only accepts SELECT statements. Any INSERT, UPDATE, DELETE, or DROP attempt gets blocked. The system prompt stays hidden from users, and the AI only answers questions related to invoices and business data.

## Why I built this

This was a learning project for the EPAM GenAI course. It covers function calling with the OpenAI tools parameter, Azure OpenAI integration through EPAM DIAL, maintaining conversation history, and using Streamlit to build AI applications quickly.

The pattern of having an LLM decide when and how to call functions - rather than having it execute code directly - is something I wanted to understand better. This project helped me get hands-on experience with that approach.