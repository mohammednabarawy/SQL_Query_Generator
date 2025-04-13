
# README for Ollama MSSQL Query Generator

This project provides a Python script to generate SQL queries using the Ollama AI model (Llama 3) for Microsoft SQL Server databases. It combines AI-powered query generation with direct SQL execution, making database querying more efficient and accessible.

## Purpose

The main goal of this project is to simplify the process of querying SQL Server databases by leveraging the power of the Ollama AI model. Users can input natural language queries, and the script will automatically generate the corresponding SQL queries and execute them against the database.

### Features

- Connects to an MSSQL database using PyODBC.
- Generates SQL queries based on user input and the database schema.
- Executes the generated SQL queries directly on the database.
- Supports both English and Arabic documentation and instructions.

## Prerequisites

Before using this script, ensure you have the following installed:

1. Python 3.10+.
2. PyODBC library: Install via pip:
   ```bash
   pip install pyodbc
   ```
3. Requests library: Install via pip:
   ```bash
   pip install requests
   ```
4. Ollama server running locally or remotely.

## Installation

To set up the project, install the required dependencies by running the following command:

```bash
pip3 install pyodbc requests
```

## How to Use

1. **Run the Script**:

   ```bash
   python ollama_mssql.py
   ```
2. **Enter Your Query**: After running the script, you will be prompted to enter your query in natural language (e.g., "Show all employees hired this year"). Press Enter to submit.
3. **AI-Generated SQL**: The script will use Ollama to generate the corresponding SQL query based on your input and will execute the query against the database.

### Example Queries:

- Retrieve top 10 sales from last month: `Show top 10 sales from last month`
- List all tables in the database: `List all tables in the database`

## Notes

- Make sure your database has a user with appropriate permissions to execute queries.
- Always validate user input to avoid SQL injection risks.
- The script uses Ollama as an AI assistant but does not replace professional SQL expertise.

---

## الوثائق باللغة العربية

يُقدم هذا المشروع سكربت بلغة بايثون لتوليد استعلامات SQL باستخدام نموذج Ollama AI (Llama 3) لقاعدة بيانات Microsoft SQL Server. يجمع هذا السكربت بين توليد الاستعلامات باستخدام الذكاء الاصطناعي وتنفيذ SQL المباشر، مما يجعل عملية الاستعلام أكثر كفاءة وسهولة.

### الغرض من المشروع

الهدف الرئيسي من هذا المشروع هو تبسيط عملية استعلام قواعد البيانات عبر SQL Server باستخدام قوة نموذج Ollama AI. يمكن للمستخدمين إدخال استعلامات باللغة الطبيعية، وسيقوم السكربت بتوليد الاستعلامات SQL المقابلة وتنفيذها على قاعدة البيانات.

### المزايا

- الاتصال بقاعدة بيانات MSSQL باستخدام PyODBC.
- توليد استعلامات SQL بناءً على إدخال المستخدم وبيانات قاعدة البيانات.
- تنفيذ الاستعلامات المُولدة مباشرة على قاعدة البيانات.
- يدعم الوثائق والتعليمات باللغتين الإنجليزية والعربية.

## المتطلبات المبدئية

قبل استخدام السكربت، تأكد من أنك قد قمت بتثبيت ما يلي:

1. Python 3.10+.
2. مكتبة PyODBC: يمكنك تثبيتها عبر pip:
   ```bash
   pip install pyodbc
   ```
3. مكتبة Requests: يمكنك تثبيتها عبر pip:
   ```bash
   pip install requests
   ```
4. خادم Ollama يعمل محليًا أو عن بُعد.

## التثبيت

لتثبيت المتطلبات اللازمة، قم بتشغيل الأمر التالي:

```bash
pip3 install pyodbc requests
```

## كيفية الاستخدام

1. **تشغيل السكربت**:

   ```bash
   python ollama_mssql.py
   ```
2. **أدخل الاستعلام**: بعد تشغيل السكربت، سيتم مطالبتك بإدخال استعلامك باللغة الطبيعية (على سبيل المثال، "عرض جميع الموظفين الذين تم تعيينهم هذا العام"). اضغط على "إدخال" لإرسال الاستعلام.
3. **توليد SQL باستخدام الذكاء الاصطناعي**: سيقوم السكربت باستخدام Ollama لتوليد استعلام SQL المقابل بناءً على إدخالك ثم تنفيذ الاستعلام على قاعدة البيانات.

### أمثلة على الاستعلامات:

- استرجاع أعلى 10 مبيعات من الشهر الماضي: `عرض أعلى 10 مبيعات من الشهر الماضي`
- عرض جميع الجداول في قاعدة البيانات: `عرض جميع الجداول في قاعدة البيانات`

## ملاحظات

- تأكد من أن قاعدة البيانات تحتوي على مستخدم لديه صلاحيات مناسبة لتنفيذ الاستعلامات.
- تحقق دائمًا من صحة المدخلات لتجنب مخاطر هجمات SQL Injection.
- يستخدم السكربت Ollama كمساعد ذكي، لكنه لا يحل محل الخبرات المهنية في SQL.

## Thanks

Thanks to the developers of PyODBC, Requests, and Ollama for their excellent libraries!
