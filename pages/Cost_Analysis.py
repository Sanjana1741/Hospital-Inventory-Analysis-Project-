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

connection=get_connection()  #connect to mysql
cursor=connection.cursor()   #give me a way to communicate with mysql

cursor.execute(
    """
    SELECT SUM(unit_cost*current_stock)
    FROM drugs
    JOIN drug_inventory
    ON drugs.drug_id=drug_inventory.drug_id
    """
)
drug_inventory_value=cursor.fetchone()
st.metric("Total Cost of Drug Inventory:",drug_inventory_value[0])

cursor.execute(
    """
    SELECT SUM(unit_cost*current_stock)
    FROM surgical_supplies
    JOIN surgical_inventory
    ON surgical_supplies.equipment_id=surgical_inventory.equipment_id
    """
)
surgical_inventory_value=cursor.fetchone()
st.metric("Total Cost of Surgical Supply Inventory:",surgical_inventory_value[0])

total_inventory_value=drug_inventory_value[0]+surgical_inventory_value[0]
st.metric("Total Cost of Hospital Inventory:",total_inventory_value)

cost_data={
    "Category":["Drugs","Surgical Supplies"],
    "Value":[drug_inventory_value[0],surgical_inventory_value[0]]
}

cost_df=pd.DataFrame(cost_data)

fig=px.pie(   #creates a pie chart
    cost_df,  #the data we just prepared
    names="Category",    #tells plotly what each slice represents
    values="Value",  #tells it how large slice should be 
    title="Drug vs Surgical Inventory Value"  #heading of the chart

)

st.plotly_chart(fig,use_container_width=True)  #displays the chart

cursor.execute("""
    SELECT drug_category, SUM(unit_cost * current_stock)
    FROM drugs
    JOIN drug_inventory
    ON drugs.drug_id = drug_inventory.drug_id
    GROUP BY drug_category
    ORDER BY SUM(unit_cost * current_stock) DESC
""")

category_results = cursor.fetchall()

category_data={
    "Category":[row[0] for row in category_results],
    "Value":[float(row[1]) for row in category_results]
}

category_df=pd.DataFrame(category_data)

fig=px.bar(    #creates the bar chart
    category_df,
    x="Category",  #drug categories go along the bottom
    y="Value",     #inventory value determines the height
    title="Inventory Value by Drug Category"
)

st.plotly_chart(fig,width="stretch")   #displays it in streamlit 

cursor.execute(
    """
    SELECT category, SUM(unit_cost*current_stock)
    FROM surgical_supplies
    JOIN surgical_inventory
    ON surgical_supplies.equipment_id=surgical_inventory.equipment_id
    GROUP BY category
    ORDER BY SUM(unit_cost*current_stock) DESC
    """
)
category_results = cursor.fetchall()

category_data={
    "Category":[row[0] for row in category_results],
    "Value":[float(row[1]) for row in category_results]
}

category_df=pd.DataFrame(category_data)

fig=px.bar(    #creates the bar chart
    category_df,
    x="Category",  #drug categories go along the bottom
    y="Value",     #inventory value determines the height
    title="Inventory Value by Surgical Supply Category"
)

st.plotly_chart(fig,width="stretch")

cursor.execute(
    """
    SELECT drug_name,unit_cost*current_stock
    FROM drugs
    JOIN drug_inventory
    ON drugs.drug_id=drug_inventory.drug_id
    ORDER BY unit_cost*current_stock DESC
    LIMIT 5
    """
    )
drug_name_results=cursor.fetchall()

drug_name_data={
    "drug_name":[row[0] for row in drug_name_results],
        "Value":[float(row[1]) for row in drug_name_results]
    }
drug_name_df=pd.DataFrame(drug_name_data)

fig=px.bar(
    drug_name_df,
    x="drug_name",
    y="Value",
    title="Top 5 Most Expensive Drugs"
)
st.plotly_chart(fig,width="stretch")


cursor.execute(
    """
    SELECT name,unit_cost*current_stock
    FROM surgical_supplies
    JOIN surgical_inventory
    ON surgical_supplies.equipment_id=surgical_inventory.equipment_id
    ORDER BY unit_cost*current_stock DESC
    LIMIT 5
    """
    )

surgical_name_results=cursor.fetchall()

surgical_name_data={
    "name":[row[0] for row in surgical_name_results],
        "Value":[float(row[1]) for row in surgical_name_results]
    }
surgical_name_df=pd.DataFrame(surgical_name_data)

fig=px.bar(
    surgical_name_df,
    x="name",
    y="Value",
    title="Top 5 Most Expensive Surgical Supplies"
)
st.plotly_chart(fig,width="stretch")

cursor.execute(
    """
    SELECT drug_name,unit_cost*current_stock
    FROM drugs
    JOIN drug_inventory
    ON drugs.drug_id=drug_inventory.drug_id
    ORDER BY unit_cost*current_stock ASC
    LIMIT 5
    """
    )
drug_name_results=cursor.fetchall()

drug_name_data={
    "drug_name":[row[0] for row in drug_name_results],
        "Value":[float(row[1]) for row in drug_name_results]
    }
drug_name_df=pd.DataFrame(drug_name_data)

fig=px.bar(
    drug_name_df,
    x="drug_name",
    y="Value",
    title="Top 5 Least Expensive Drugs"
)
st.plotly_chart(fig,width="stretch")


cursor.execute(
    """
    SELECT name,unit_cost*current_stock
    FROM surgical_supplies
    JOIN surgical_inventory
    ON surgical_supplies.equipment_id=surgical_inventory.equipment_id
    ORDER BY unit_cost*current_stock ASC
    LIMIT 5
    """
    )

surgical_name_results=cursor.fetchall()

surgical_name_data={
    "name":[row[0] for row in surgical_name_results],
        "Value":[float(row[1]) for row in surgical_name_results]
    }
surgical_name_df=pd.DataFrame(surgical_name_data)

fig=px.bar(
    surgical_name_df,
    x="name",
    y="Value",
    title="Top 5 Least Expensive Surgical Supplies"
)
st.plotly_chart(fig,width="stretch")

