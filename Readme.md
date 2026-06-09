AI Business Intelligence Agent
Overview

AI Business Intelligence Agent is an AI-powered analytics platform that allows users to interact with datasets using natural language.

Instead of writing SQL queries manually, users can ask business questions in plain English and receive:

SQL queries generated automatically
Data tables
Interactive visualizations
Business insights
Downloadable reports

The application supports both a built-in financial dataset and user-uploaded CSV/Excel files.

Features
Natural Language to SQL

Ask questions such as:

Top 10 companies by revenue
Highest net income companies
Revenue for NVDA

The AI converts the question into SQL and executes it automatically.

PostgreSQL Integration
Stores and queries financial data
Supports dynamic uploaded datasets
Executes AI-generated SQL queries safely
Interactive Visualizations

Automatically generates charts based on query results:

Bar Charts
Line Charts
Pie Charts
Scatter Plots

Built using Plotly.

Dataset Upload

Upload your own:

CSV files
Excel files (.xlsx)

The system automatically:

Detects schema
Creates a database table
Enables natural language querying
Business Insights

Generates automatic summaries including:

Top performers
Average values
Maximum values
Dataset statistics
Export Results

Download query results as:

CSV
Excel
Tech Stack
Component	Technology
Frontend	Streamlit
Database	PostgreSQL
AI Model	Gemini 2.5 Flash
Data Processing	Pandas
Visualization	Plotly
ORM/DB Connection	SQLAlchemy
Environment Variables	python-dotenv
Project Structure
AI-Business-Intelligence-Agent/
│
├── agents/
│   ├── sql_agent.py
│   ├── upload_agent.py
│   └── insight_agent.py
│
├── database/
│   ├── postgres.py
│   └── create_db.py
│
├── data/
│   └── corporate_income_statement.csv
│
├── utils/
│   ├── llm.py
│   ├── charts.py
│   ├── business_summary.py
│   └── data_loader.py
│
├── app.py
├── requirements.txt
├── .env
└── README.md
Installation
Clone Repository
git clone https://github.com/yourusername/AI-Business-Intelligence-Agent.git

cd AI-Business-Intelligence-Agent
Create Virtual Environment

Windows:

python -m venv venv

venv\Scripts\activate

Linux / Mac:

python3 -m venv venv

source venv/bin/activate
Install Dependencies
pip install -r requirements.txt
PostgreSQL Setup

Create a PostgreSQL database:

Database Name: ai_bi_agent

Create a .env file:

DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ai_bi_agent

GEMINI_API_KEY=your_gemini_api_key
Load Financial Dataset

Run:

python database/create_db.py

Expected output:

Database Created Successfully
Run Application
streamlit run app.py

Open:

http://localhost:8501
Example Questions
Financial Dataset
Top 10 companies by revenue
Top 10 companies by net income
Revenue for NVDA
Top EBITDA companies
Uploaded Dataset

Upload any CSV or Excel file and ask:

Top customers by sales
Average salary by department
Highest performing products
Monthly revenue trend
Author

Vikram Thakur

B.Tech Computer Science Engineering (Data Science)

Graduation Year: 2027

GitHub: (Add your GitHub profile)

LinkedIn: (Add your LinkedIn profile)