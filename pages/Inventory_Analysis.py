import streamlit as st
from database import get_connection
import pandas as pd
import plotly.express as px

if "logged_in" not in st.session_state:
    st.session_state.logged_in=False

if not st.session_state.logged_in:
    st.warning("Please login first")
    st.stop()
st.write("Hospital Inventory Dashboard")

db=get_connection()
cursor=db.cursor()

st.header("Drugs Inventory Analysis")

cursor.execute(
    """
    SELECT COUNT(*)
    FROM drug_inventory
    """
    )

total_drugs=cursor.fetchone()[0]

st.metric("Total Drugs💊:",total_drugs)

cursor.execute(
    """
    SELECT
        CASE
            WHEN current_stock=0 THEN 'Critical'
            WHEN current_stock<=reorder_level*0.20 THEN 'Critical'
            WHEN current_stock<reorder_level THEN 'Low Stock'
            ELSE 'Normal'
        END AS stock_status,
        COUNT(*) AS total
    FROM drug_inventory
    GROUP BY stock_status
    """
            )

stock_status_data=cursor.fetchall()


normal_drugs=0   #Creating variables
low_stock_drugs=0
critical_drugs=0

for row in stock_status_data:   #take each row inside stock_status_data,one at a time.loop happens 3 times
    if row[0]=="Normal":       #is the first value in this row equal to normal?
        normal_drugs=row[1]   #store the number of normal drugs
    elif row[0]=="Low Stock":
        low_stock_drugs=row[1]
    elif row[0]=="Critical":
        critical_drugs=row[1]

col1,col2,col3=st.columns(3)
with col1:
    st.metric("Normal🟢",normal_drugs)
with col2:
    st.metric("Low Stock🟡",low_stock_drugs)
with col3:
    st.metric("Critical🔴",critical_drugs)

status_df=pd.DataFrame(
    stock_status_data,
    columns=["Status","Count"]
)

st.subheader("Stock Analaysis📊")

fig=px.bar(
    status_df,
    x="Status",
    y="Count",
    title="Stock Analaysis"
)
st.plotly_chart(fig,width="stretch")

cursor.execute("""
    SELECT
        drugs.drug_category,
        SUM(drug_inventory.current_stock) AS total_stock
    FROM drugs
    JOIN drug_inventory
    ON drugs.drug_id = drug_inventory.drug_id
    GROUP BY drugs.drug_category
    ORDER BY total_stock DESC
""")

category_data = cursor.fetchall()

category_df = pd.DataFrame(
    category_data,
    columns=["Category", "Total Stock"]
)

fig=px.bar(
    category_df,
    x="Category",
    y="Total Stock",
    title="Category Stock Analaysis"
)

st.plotly_chart(fig,width="stretch")

cursor.execute("""
    SELECT
        drugs.drug_name,
        drug_inventory.current_stock
    FROM drugs
    JOIN drug_inventory
    ON drugs.drug_id = drug_inventory.drug_id
    ORDER BY drug_inventory.current_stock DESC
    LIMIT 5
""")

top_stock_data = cursor.fetchall()

top_stock_df=pd.DataFrame(
    top_stock_data,
    columns=["Drugs","Current Stock"]
)

fig=px.bar(
    top_stock_df,
    x="Drugs",
    y="Current Stock",
    title="Top 5 Drugs with Highest Stock"
)

st.plotly_chart(fig,width="stretch")

cursor.execute("""
    SELECT
        drugs.drug_name,
        drug_inventory.current_stock
    FROM drugs
    JOIN drug_inventory
    ON drugs.drug_id = drug_inventory.drug_id
    ORDER BY drug_inventory.current_stock ASC
    LIMIT 5
""")

lowest_stock_data = cursor.fetchall()

lowest_stock_df=pd.DataFrame(
    lowest_stock_data,
    columns=["Drugs","Lowest Stock"]
)

fig=px.bar(
    lowest_stock_df,
    x="Drugs",
    y="Lowest Stock",
    title="Top 5 Drugs with Lowest Stock"
)

st.plotly_chart(fig,width="stretch")

#inventory analysis for surgical supplies
#Total number of surgical supplies

st.header("Surgical Supplies Inventory Analysis")
cursor.execute("""
    SELECT COUNT(*)
    FROM surgical_inventory
""")

total_surgical = cursor.fetchone()[0]

st.metric("🩺 Total Surgical Supplies", total_surgical)

#total stock of all surgical supplies

cursor.execute(
    """
    SELECT SUM(current_stock)
    FROM surgical_inventory
    """
)
total_surgical_stock=cursor.fetchone()[0]

st.metric("Total Surgical Stock",total_surgical_stock)



#total stock by category
cursor.execute("""
    SELECT
        s.category,
        SUM(i.current_stock)
    FROM surgical_supplies s
    JOIN surgical_inventory i
        ON s.equipment_id = i.equipment_id
    GROUP BY s.category
    ORDER BY SUM(i.current_stock) DESC
""")

surgical_category_results = cursor.fetchall()


surgical_category_data = {
    "Category": [row[0] for row in surgical_category_results],
    "Total Stock": [row[1] for row in surgical_category_results]
}

surgical_category_df = pd.DataFrame(surgical_category_data)


st.subheader("📦 Surgical Stock by Category")


fig_category = px.bar(
    surgical_category_df,
    x="Category",
    y="Total Stock",
    title="Total Surgical Stock by Category",
    text="Total Stock"
)

fig_category.update_layout(
    xaxis_title="Category",
    yaxis_title="Total Stock"
)

st.plotly_chart(
    fig_category,
    use_container_width=True
)

# TOP 5 HIGH STOCK SURGICAL SUPPLIES

cursor.execute("""
    SELECT
        s.name,
        i.current_stock
    FROM surgical_supplies s
    JOIN surgical_inventory i
        ON s.equipment_id = i.equipment_id
    ORDER BY i.current_stock DESC
    LIMIT 5
""")

high_surgical_results = cursor.fetchall()

high_surgical_data = {
    "Supply": [row[0] for row in high_surgical_results],
    "Stock": [row[1] for row in high_surgical_results]
}

high_surgical_df = pd.DataFrame(high_surgical_data)

st.subheader("📈 Top 5 High Stock Surgical Supplies")

fig = px.bar(
    high_surgical_df,
    x="Supply",
    y="Stock",
    title="Top 5 High Stock Surgical Supplies",
    text="Stock"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# TOP 5 LOW STOCK SURGICAL SUPPLIES

cursor.execute("""
    SELECT
        s.name,
        i.current_stock
    FROM surgical_supplies s
    JOIN surgical_inventory i
        ON s.equipment_id = i.equipment_id
    ORDER BY i.current_stock ASC
    LIMIT 5
""")

low_surgical_results = cursor.fetchall()

low_surgical_data = {
    "Supply": [row[0] for row in low_surgical_results],
    "Stock": [row[1] for row in low_surgical_results]
}

low_surgical_df = pd.DataFrame(low_surgical_data)

st.subheader("📉 Top 5 Low Stock Surgical Supplies")

fig = px.bar(
    low_surgical_df,
    x="Supply",
    y="Stock",
    title="Top 5 Low Stock Surgical Supplies",
    text="Stock"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

#stock status distribution

cursor.execute("""
    SELECT
        inventory_status,
        COUNT(*)
    FROM surgical_inventory
    GROUP BY inventory_status
""")

surgical_status_results = cursor.fetchall()

surgical_status_data = {
    "Status": [row[0] for row in surgical_status_results],
    "Count": [row[1] for row in surgical_status_results]
}

surgical_status_df = pd.DataFrame(surgical_status_data)


st.subheader("⚠️ Surgical Stock Status Distribution")


fig = px.bar(
    surgical_status_df,
    x="Status",
    y="Count",
    title="Surgical Stock Status Distribution",
    text="Count"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

#total inventory value 

cursor.execute("""
    SELECT
        SUM(s.unit_cost * i.current_stock)
    FROM surgical_supplies s
    JOIN surgical_inventory i
        ON s.equipment_id = i.equipment_id
""")

total_surgical_value = cursor.fetchone()[0]

st.metric(
    "💰 Total Surgical Inventory Value",
    f"₹{total_surgical_value:,.2f}"
)
