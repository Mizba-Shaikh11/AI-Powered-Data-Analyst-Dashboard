# 📊 AI-Powered Data Analyst Dashboard

An interactive **AI-powered data analytics dashboard** built with Python, Pandas, Plotly, and Streamlit.

The application combines traditional data analytics with **Generative AI**, allowing users to explore business data through interactive dashboards and ask questions about the data using natural language.

---

## 🚀 Project Overview

This project demonstrates an end-to-end data analytics workflow:

**Data Cleaning → KPI Analysis → Visualization → Interactive Filtering → AI-Powered Q&A**

The dashboard helps users analyze sales performance and ask business questions in plain English while keeping responses grounded in the underlying dataset.

---

## ✨ Features

### 📊 Interactive Dashboard

* Total Sales
* Total Profit
* Average Order Value
* Order Count
* Profit Margin

### 🔎 Interactive Filters

* Region
* Product Category
* Date Range

### 📈 Data Visualizations

* Monthly Sales & Profit Trends
* Sales by Region
* Sales by Category
* Top-Performing Products

### 🧹 Data Cleaning

* Missing-value handling
* Data type conversion
* Derived columns
* Data aggregation

### 🤖 AI-Powered Q&A

Users can ask questions such as:

> **"Which region has the highest profit margin?"**

The application processes the currently filtered data, creates a compact summary, and provides it to the LLM along with the user's question.

The model generates a natural-language response based on the available data rather than receiving the entire dataset.

### 🔌 Offline-Friendly

The dashboard and data-analysis features can work without an API key. The AI Q&A feature requires a configured Groq API key.

---

## 🛠️ Tech Stack

| Category        | Technologies               |
| --------------- | -------------------------- |
| Programming     | Python                     |
| Data Processing | Pandas, NumPy              |
| Visualization   | Plotly                     |
| Dashboard       | Streamlit                  |
| Generative AI   | Groq API, Llama            |
| Environment     | Python Virtual Environment |
| Version Control | Git, GitHub                |

---

## 🏗️ Project Architecture

```text
User
 │
 ▼
Streamlit Dashboard
 │
 ├── Data Upload / Dataset
 │
 ├── Data Cleaning
 │
 ├── KPI Calculation
 │
 ├── Interactive Filters
 │
 ├── Data Visualizations
 │
 └── AI Q&A
       │
       ▼
 Filtered Data Summary
       │
       ▼
    LLM / Groq
       │
       ▼
 Natural-Language Answer
```

---

## 📂 Project Structure

```text
ai-data-analyst-project/
│
├── app.py
├── generate_data.py
│
├── utils/
│   └── data_utils.py
│
├── data/
│   └── sample_sales_data.csv
│
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🤖 How the AI Q&A Works

Instead of sending the complete dataset to the language model, the application follows a lightweight data-grounding approach:

### 1. Filter the Data

The user selects filters such as region, category, or date range.

### 2. Generate a Data Summary

The application calculates relevant KPIs, aggregations, and trends from the filtered data.

### 3. Send Context to the LLM

The summarized information and user's question are sent to the Groq LLM.

### 4. Generate the Answer

The model generates a natural-language response using the provided data context.

```text
User Question
      ↓
Filtered Dataset
      ↓
Data Aggregation
      ↓
Compact Data Summary
      ↓
LLM
      ↓
Business Answer
```

This approach reduces the amount of data sent to the model and helps keep responses focused on the available business data.

---

## 💡 Example Questions

Users can ask questions such as:

* Which region generated the highest profit?
* Which category has the highest sales?
* What is the average order value?
* Which products have the highest sales?
* How did sales change over time?
* Which region has the highest profit margin?

---

## 📊 Business Use Cases

This type of dashboard can support:

* Sales performance analysis
* Regional performance monitoring
* Product analysis
* Profitability analysis
* KPI monitoring
* Business reporting
* Natural-language data exploration

---

## ▶️ Running the Project

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/ai-data-analyst-project.git
cd ai-data-analyst-project
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Generate the Dataset

```bash
python generate_data.py
```

### 5. Configure the AI Feature

Create a `.env` file:

```text
GROQ_API_KEY=your_api_key_here
```

Keep your API key private and **never upload the `.env` file to GitHub**.

### 6. Run the Dashboard

```bash
streamlit run app.py
```

The application will open in your browser.

---

## 🔮 Future Improvements

* Replace the synthetic dataset with a real-world public dataset
* Add anomaly detection
* Add automated business insights
* Add downloadable Excel/PDF reports
* Add additional visualization options
* Add automated testing
* Deploy the application as a public web application

---

## 🎯 Skills Demonstrated

This project demonstrates practical experience in:

* Python
* Pandas & NumPy
* Data Cleaning
* Exploratory Data Analysis
* KPI Development
* Business Analytics
* Data Visualization
* Streamlit
* Generative AI
* LLM Integration
* Data Grounding
* Git & GitHub

---

## 📌 Project Goal

The goal of this project is to demonstrate how **traditional data analytics can be combined with Generative AI** to make business data easier to explore and understand.

> **Analyze the data → Ask the question → Generate the insight → Support the decision**
