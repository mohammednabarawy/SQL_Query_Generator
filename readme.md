# README for MSSQL Database AI Analyzer

This project provides a comprehensive solution for analyzing and querying Microsoft SQL Server databases using AI models from Ollama. It combines AI-powered query generation with direct SQL execution, making database querying more efficient and accessible through both command-line and web interfaces.

## Purpose

The main goal of this project is to simplify the process of querying SQL Server databases by leveraging the power of Ollama AI models. Users can input natural language queries, and the application will automatically generate the corresponding SQL queries and execute them against the database.

### Features

- Connects to an MSSQL database using PyODBC
- Generates SQL queries based on user input and the database schema
- Executes the generated SQL queries directly on the database
- **NEW: Web interface with Streamlit for easier interaction**
- **NEW: Dashboard for analyzing query history and patterns**
- **NEW: Support for multiple Ollama models (llama3, codellama, mistral, etc.)**
- **NEW: Enhanced schema extraction with primary keys, foreign keys, and indexes**
- **NEW: Query history tracking and analysis**
- Supports both English and Arabic documentation and instructions

## Prerequisites

Before using this application, ensure you have the following installed:

1. Python 3.10+
2. PyODBC library: `pip install pyodbc`
3. Requests library: `pip install requests`
4. Streamlit (for web interface): `pip install streamlit`
5. Pandas (for data handling): `pip install pandas`
6. Plotly (for dashboard): `pip install plotly`
7. Ollama server running locally or remotely

## Installation

To set up the project, install the required dependencies by running the following command:

```bash
pip install -r requirements.txt
```

Or install individual packages:

```bash
pip install pyodbc requests streamlit pandas plotly matplotlib
```

## How to Use

### Command Line Interface

1. **Run the Script**:

   ```bash
   python ollama_mssql.py
   ```
2. **Enter Your Query**: After running the script, you will be prompted to enter your query in natural language (e.g., "Show all employees hired this year"). Press Enter to submit.
3. **AI-Generated SQL**: The script will use Ollama to generate the corresponding SQL query based on your input and will execute the query against the database.

### Web Interface (NEW!)

1. **Start the Web Application**:

   ```bash
   streamlit run app.py
   ```
2. **Access the Web Interface**: Open your browser and navigate to `http://localhost:8501`
3. **Enter Your Query**: Type your natural language query in the text area and click "Generate SQL Query"
4. **View Results**: The generated SQL and query results will be displayed in the interface

### Dashboard (NEW!)

1. **Start the Dashboard**:

   ```bash
   streamlit run dashboard.py
   ```
2. **Access the Dashboard**: Open your browser and navigate to `http://localhost:8501`
3. **Analyze Query History**: View statistics about your query patterns, success rates, and most queried tables

### Example Queries:

- Retrieve top 10 sales from last month: `Show top 10 sales from last month`
- List all tables in the database: `List all tables in the database`
- Find customers with outstanding balances: `Show customers with unpaid invoices`

## Configuration (NEW!)

You can customize the application by editing the `config.py` file:

- Database connection settings
- Ollama API endpoint
- Default and recommended models
- Sample data limits

## Notes

- Make sure your database has a user with appropriate permissions to execute queries
- Always validate user input to avoid SQL injection risks
- The application uses Ollama as an AI assistant but does not replace professional SQL expertise

---

## الوثائق باللغة العربية

يُقدم هذا المشروع حلاً شاملاً لتحليل واستعلام قواعد بيانات Microsoft SQL Server باستخدام نماذج الذكاء الاصطناعي من Ollama. يجمع هذا التطبيق بين توليد الاستعلامات باستخدام الذكاء الاصطناعي وتنفيذ SQL المباشر، مما يجعل عملية الاستعلام أكثر كفاءة وسهولة من خلال واجهة سطر الأوامر وواجهة الويب.

### الغرض من المشروع

الهدف الرئيسي من هذا المشروع هو تبسيط عملية استعلام قواعد البيانات عبر SQL Server باستخدام قوة نماذج Ollama AI. يمكن للمستخدمين إدخال استعلامات باللغة الطبيعية، وسيقوم التطبيق بتوليد الاستعلامات SQL المقابلة وتنفيذها على قاعدة البيانات.

### المزايا

- الاتصال بقاعدة بيانات MSSQL باستخدام PyODBC
- توليد استعلامات SQL بناءً على إدخال المستخدم وبيانات قاعدة البيانات
- تنفيذ الاستعلامات المُولدة مباشرة على قاعدة البيانات
- **جديد: واجهة ويب باستخدام Streamlit للتفاعل بشكل أسهل**
- **جديد: لوحة تحكم لتحليل سجل الاستعلامات والأنماط**
- **جديد: دعم لنماذج Ollama متعددة (llama3, codellama, mistral، إلخ)**
- **جديد: استخراج مُحسّن لمخطط قاعدة البيانات مع المفاتيح الأساسية والخارجية والفهارس**
- **جديد: تتبع وتحليل سجل الاستعلامات**
- يدعم الوثائق والتعليمات باللغتين الإنجليزية والعربية

## Thanks

Thanks to the developers of PyODBC, Requests, Streamlit, Pandas, Plotly, and Ollama for their excellent libraries!
