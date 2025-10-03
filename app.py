import streamlit as st
import pandas as pd

# =======================
# Load Excel Data
# =======================
file_path = "Output 2025-10-03.xlsx"


@st.cache_data
def load_data():
    # Read all sheets
    xls = pd.ExcelFile(file_path)
    data = {sheet: pd.read_excel(file_path, sheet_name=sheet) for sheet in xls.sheet_names}
    return data


data = load_data()

# =======================
# Sidebar Navigation
# =======================
st.sidebar.title("📊 Inventory Dashboard")
sheet_names = list(data.keys())
selected_sheet = st.sidebar.selectbox("Select Sheet", sheet_names)

df = data[selected_sheet]

st.title("📦 Monthly Inventory Dashboard")
st.subheader(f"Data from: {selected_sheet}")

st.dataframe(df.head(50))

# =======================
# KPIs
# =======================
if "Out Sum" in df.columns:
    total_out = df["Out Sum"].sum()
    avg_out = df["Out Sum"].mean()
    st.metric("Total Out (Monthly)", f"{total_out:,.0f}")
    st.metric("Average Out per Item", f"{avg_out:,.0f}")

# =======================
# Top Design Sales
# =======================
if "Design Name" in df.columns and "Out Sum" in df.columns:
    st.subheader("🔥 Top Selling Designs")
    top_designs = df.groupby("Design Name")["Out Sum"].sum().sort_values(ascending=False).head(25)
    st.bar_chart(top_designs)

# =======================
# Company-wise Sales
# =======================
if "Company Name" in df.columns and "Out Sum" in df.columns:
    st.subheader("🏢 Sales by Company")
    company_sales = df.groupby("Company Name")["Out Sum"].sum().sort_values(ascending=False)
    st.bar_chart(company_sales)

# =======================
# Month Selector (if multiple sheets)
# =======================
if len(sheet_names) > 1:
    st.sidebar.markdown("### Compare Months")
    compare_sheets = st.sidebar.multiselect("Select Months to Compare", sheet_names, default=sheet_names[:2])
    if compare_sheets:
        comp_df = []
        for s in compare_sheets:
            if "Out Sum" in data[s].columns:
                comp_df.append({"Month": s, "Total Out": data[s]["Out Sum"].sum()})
        comp_df = pd.DataFrame(comp_df)
        st.subheader("📅 Monthly Out Sum Comparison")
        st.bar_chart(comp_df.set_index("Month"))
