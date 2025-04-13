# 🔍 MSSQL Database AI Analyzer

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/Python-3.10+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

**Interact with your SQL Server database using natural language**

[Features](#-key-features) • 
[Installation](#-installation) • 
[Usage](#-usage) • 
[Contributing](#-contributing) • 
[Roadmap](#-roadmap)

</div>

---

## 🌟 Overview

This project bridges the gap between natural language and SQL queries by leveraging AI models from Ollama. Ask questions about your database in plain English (or Arabic), and get instant SQL queries and results - no SQL expertise required!

<div align="center">
<img src="https://img.shields.io/badge/Powered%20by-Ollama%20AI-blueviolet" alt="Powered by Ollama AI">
</div>

## 🚀 Key Features

- **Natural Language to SQL** - Ask questions in plain English and get SQL queries
- **Web Interface** - Beautiful Streamlit UI for easy interaction
- **Analytics Dashboard** - Track query patterns and database usage
- **Multi-Model Support** - Choose from various Ollama models (llama3, codellama, mistral)
- **Comprehensive Schema Analysis** - Detailed extraction of tables, relationships, and indexes
- **Query History** - Save and analyze past queries
- **Multilingual Support** - Documentation in English and Arabic

## 📋 Prerequisites

- Python 3.10+
- Microsoft SQL Server
- Ollama running locally or remotely
- Required Python packages (see [Installation](#-installation))

## 💻 Installation

### Quick Start

```bash
# Clone the repository
git clone https://github.com/mohammednabarawy/SQL_Query_Generator.git
cd mssql-ai-analyzer

# Install dependencies
pip install -r requirements.txt

# Configure your database connection in config.py
# Start the web interface
streamlit run app.py
```

### Detailed Installation

1. Ensure you have Python 3.10+ installed
2. Install the ODBC Driver for SQL Server
3. Install Ollama and start the service
4. Install the required Python packages:
   ```bash
   pip install pyodbc requests streamlit pandas plotly matplotlib
   ```
5. Configure your database connection in `config.py`

## 🔧 Usage

### Command Line Interface

```bash
python ollama_mssql.py
```

### Web Interface

```bash
streamlit run app.py
```

### Analytics Dashboard

```bash
streamlit run dashboard.py
```

### Example Queries

- "Show me the top 10 customers by total purchase amount"
- "Find all invoices that are overdue by more than 30 days"
- "What's the average order value by month for the last year?"
- "List all employees hired in 2024 with their department"

## ⚙️ Configuration

Edit `config.py` to customize:

- Database connection settings
- Ollama API endpoint
- Default and recommended models
- Sample data limits

## 🛠️ Contributing

We welcome contributions from the community! Here's how you can help:

1. **Fork the repository** - Create your own copy of the project
2. **Create a feature branch** - `git checkout -b feature/amazing-feature`
3. **Commit your changes** - `git commit -m 'Add some amazing feature'`
4. **Push to your branch** - `git push origin feature/amazing-feature`
5. **Open a Pull Request** - We'll review and merge your contribution

### Ideas for Contributions

- Add support for more database systems (PostgreSQL, MySQL, etc.)
- Implement query optimization suggestions
- Create visualization tools for query results
- Add support for more languages
- Improve the AI prompts for better SQL generation
- Write comprehensive tests

## 📝 Roadmap

- [ ] Support for more database systems
- [ ] Advanced query optimization
- [ ] User authentication and role-based access
- [ ] Export capabilities to various formats
- [ ] Integration with BI tools
- [ ] Scheduled queries and alerts

## 📊 Performance

The application uses Ollama's AI models locally, ensuring:
- Privacy - Your data never leaves your system
- Speed - No network latency for AI processing
- Customization - Fine-tune models for your specific database

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- Thanks to the developers of PyODBC, Requests, Streamlit, Pandas, Plotly, and Ollama
- Special thanks to all contributors who help improve this project

---

<div align="center">

## 📚 الوثائق باللغة العربية

**محلل قواعد بيانات MSSQL باستخدام الذكاء الاصطناعي**

</div>

يُقدم هذا المشروع حلاً شاملاً لتحليل واستعلام قواعد بيانات Microsoft SQL Server باستخدام نماذج الذكاء الاصطناعي من Ollama. يجمع هذا التطبيق بين توليد الاستعلامات باستخدام الذكاء الاصطناعي وتنفيذ SQL المباشر، مما يجعل عملية الاستعلام أكثر كفاءة وسهولة من خلال واجهة سطر الأوامر وواجهة الويب.

### 🎯 الغرض من المشروع

الهدف الرئيسي من هذا المشروع هو تبسيط عملية استعلام قواعد البيانات عبر SQL Server باستخدام قوة نماذج Ollama AI. يمكن للمستخدمين إدخال استعلامات باللغة الطبيعية، وسيقوم التطبيق بتوليد الاستعلامات SQL المقابلة وتنفيذها على قاعدة البيانات.

### ✨ المزايا

- **تحويل اللغة الطبيعية إلى SQL** - اطرح أسئلة باللغة العربية أو الإنجليزية واحصل على استعلامات SQL
- **واجهة ويب** - واجهة مستخدم جميلة باستخدام Streamlit للتفاعل السهل
- **لوحة تحليلات** - تتبع أنماط الاستعلام واستخدام قاعدة البيانات
- **دعم نماذج متعددة** - اختر من بين نماذج Ollama المختلفة (llama3, codellama, mistral)
- **تحليل شامل للمخطط** - استخراج مفصل للجداول والعلاقات والفهارس
- **سجل الاستعلامات** - حفظ وتحليل الاستعلامات السابقة
- **دعم متعدد اللغات** - وثائق باللغتين العربية والإنجليزية

---

<div align="center">
<p>Made with ❤️ by developers, for developers</p>
<p>Star ⭐ this repository if you find it useful!</p>
</div>
