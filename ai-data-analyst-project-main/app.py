"""
app.py
------
AI-Powered Data Analyst Dashboard.

Run locally with:
    streamlit run app.py

Two parts:
  1. A standard BI dashboard (KPIs, filters, charts) built with pandas + Plotly.
  2. An "Ask your data" box that sends a natural-language question, plus a
     summary of the filtered data, to a free LLM API (Groq) and returns
     a plain-English answer. If no API key is set, this section still works
     in a limited "offline" mode using simple rule-based summaries.
"""

import os
import streamlit as st
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv

from utils.data_utils import (
    load_and_clean_data,
    compute_kpis,
    sales_by_dimension,
    monthly_trend,
    top_products,
)

load_dotenv()  # reads GROQ_API_KEY from a local .env file if present

st.set_page_config(page_title="AI Data Analyst Dashboard", layout="wide")

DATA_PATH = "data/sample_sales_data.csv"


@st.cache_data
def get_data():
    return load_and_clean_data(DATA_PATH)


df = get_data()

# ---------- Sidebar filters ----------
st.sidebar.header("Filters")
regions = st.sidebar.multiselect("Region", sorted(df["Region"].unique()), default=list(df["Region"].unique()))
categories = st.sidebar.multiselect("Category", sorted(df["Category"].unique()), default=list(df["Category"].unique()))
date_min, date_max = df["OrderDate"].min(), df["OrderDate"].max()
date_range = st.sidebar.date_input("Order date range", value=(date_min, date_max))

filtered = df[df["Region"].isin(regions) & df["Category"].isin(categories)]
if len(date_range) == 2:
    filtered = filtered[
        (filtered["OrderDate"] >= pd.Timestamp(date_range[0]))
        & (filtered["OrderDate"] <= pd.Timestamp(date_range[1]))
    ]

# ---------- Header + KPIs ----------
st.title("📊 AI-Powered Data Analyst Dashboard")
st.caption("Synthetic retail sales data · built with Streamlit, pandas, Plotly, and a free LLM API")

kpis = compute_kpis(filtered)
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Sales", f"${kpis['total_sales']:,.0f}")
c2.metric("Total Profit", f"${kpis['total_profit']:,.0f}")
c3.metric("Avg Order Value", f"${kpis['avg_order_value']:,.2f}")
c4.metric("Total Orders", f"{kpis['total_orders']:,}")
c5.metric("Avg Profit Margin", f"{kpis['avg_profit_margin']}%")

st.divider()

# ---------- Charts ----------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Monthly Sales & Profit Trend")
    trend = monthly_trend(filtered)
    fig = px.line(trend, x="Month", y=["Sales", "Profit"], markers=True)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Sales by Region")
    reg = sales_by_dimension(filtered, "Region")
    fig2 = px.bar(reg, x="Region", y="Sales", color="Region", text_auto=".2s")
    st.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    st.subheader("Sales by Category")
    cat = sales_by_dimension(filtered, "Category")
    fig3 = px.pie(cat, names="Category", values="Sales", hole=0.4)
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.subheader("Top 10 Products by Sales")
    top = top_products(filtered, 10)
    fig4 = px.bar(top, x="Sales", y="Product", orientation="h")
    st.plotly_chart(fig4, use_container_width=True)

st.divider()

# ---------- AI "Ask your data" section ----------
st.subheader("🤖 Ask your data")
st.caption(
    "Ask a question in plain English, e.g. "
    "\"Which region had the highest profit margin?\" or \"Summarize the sales trend.\""
)

question = st.text_input("Your question")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def build_data_context(data: pd.DataFrame) -> str:
    """Turn the filtered dataframe into a compact text summary an LLM can reason over,
    instead of sending the raw dataset (cheaper, faster, and keeps the prompt small)."""
    kpi = compute_kpis(data)
    by_region = sales_by_dimension(data, "Region").to_string(index=False)
    by_category = sales_by_dimension(data, "Category").to_string(index=False)
    trend = monthly_trend(data).to_string(index=False)
    return f"""
KPIs: {kpi}

Sales & Profit by Region:
{by_region}

Sales & Profit by Category:
{by_category}

Monthly Sales & Profit Trend:
{trend}
""".strip()


def ask_groq(user_question: str, context: str) -> str:
    """Call Groq's free-tier chat completion API."""
    from groq import Groq

    client = Groq(api_key=GROQ_API_KEY)
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a data analyst assistant. Answer questions using ONLY the "
                    "summarized data provided below. Be concise and specific, and cite "
                    "numbers from the data in your answer."
                ),
            },
            {"role": "user", "content": f"Data summary:\n{context}\n\nQuestion: {user_question}"},
        ],
        temperature=0.2,
    )
    return completion.choices[0].message.content


if st.button("Ask") and question:
    context = build_data_context(filtered)
    if GROQ_API_KEY:
        with st.spinner("Thinking..."):
            try:
                answer = ask_groq(question, context)
                st.success(answer)
            except Exception as e:
                st.error(f"Error calling the LLM API: {e}")
    else:
        st.warning(
            "No GROQ_API_KEY found, so this is running in offline mode. "
            "Here is the raw data summary the AI would have used — "
            "add a free Groq API key to your .env file to get a natural-language answer."
        )
        st.code(context)

with st.expander("How the AI Q&A works"):
    st.markdown(
        """
        1. The dashboard's filtered data is aggregated into a small text summary
           (KPIs, sales by region/category, monthly trend) — not the raw rows.
        2. That summary + your question are sent to **Groq's free API**
           (`llama-3.1-8b-instant`), which is fast and has a generous free tier.
        3. The model answers using only the numbers in that summary, so answers
           stay grounded in the actual filtered data instead of guessing.
        """
    )
