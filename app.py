import streamlit as st
import pandas as pd
from openai import OpenAI

# ---------------- GROQ API ----------------

client = OpenAI(
    api_key=st.secrets["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"],
    base_url="https://api.groq.com/openai/v1"
)

# ---------------- TITLE ----------------

st.title("AI Root Cause Analysis Engine")

# ---------------- FILE UPLOAD ----------------

uploaded_file = st.file_uploader("Upload your dataset", type=["csv"])

if uploaded_file is not None:

    # Read CSV
    df = pd.read_csv(uploaded_file)

    # Create Total Sales
    df["Total_Sales"] = df["Quantity_sold"] * df["Price_per_unit"]

    # Show Dataset
    st.subheader("Dataset Preview")
    st.write(df.head())

    # ---------------- KPI SECTION ----------------

    total_sales = df["Total_Sales"].sum()
    total_quantity = df["Quantity_sold"].sum()
    average_sales = df["Total_Sales"].mean()

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Sales", f"${total_sales:,.2f}")
    col2.metric("Total Quantity", total_quantity)
    col3.metric("Average Sale", f"${average_sales:,.2f}")

    # ---------------- CHART ----------------

    st.subheader("Sales by Item")

    item_sales = df.groupby("Item_name")["Total_Sales"].sum()

    st.bar_chart(item_sales)

    # ---------------- ROOT CAUSE ----------------

    lowest_item = item_sales.idxmin()
    lowest_sales = item_sales.min()

    st.subheader("Root Cause Analysis")

    st.write(f"Lowest Performing Item: {lowest_item}")
    st.write(f"Sales Generated: ${lowest_sales:,.2f}")

    # ---------------- AI PROMPT ----------------

    prompt = f"""
    You are a business analyst AI.

    Analyze this sales data.

    Lowest performing item: {lowest_item}

    Sales generated: {lowest_sales}

    Total sales: {total_sales}

    Give:
    1. Root cause analysis
    2. Possible reasons
    3. Business recommendations

    Keep the answer simple and professional.
    """

    # ---------------- AI RESPONSE ----------------

    try:

        completion = client.chat.completions.create(

            model="llama-3.1-8b-instant",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.7
        )

        ai_response = completion.choices[0].message.content

        st.subheader("AI Business Insight")

        st.success(ai_response)

    except Exception as e:

        st.error(f"Error: {e}")
