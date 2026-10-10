import streamlit as st
from database import get_connection

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

cursor.execute("SELECT COUNT(*) FROM drugs")   #ask mysql this question 
drug_result=cursor.fetchone()

cursor.execute("SELECT COUNT(*) FROM surgical_supplies")                
surgical_result=cursor.fetchone()#give me the answer 

cursor.execute("SELECT COUNT(*) FROM drug_inventory WHERE current_stock<reorder_level")
low_stock_result=cursor.fetchone()

cursor.execute("SELECT COUNT(*) FROM drug_inventory WHERE current_stock=0")
out_of_stock_result=cursor.fetchone()

cursor.execute("SELECT COUNT(*) FROM surgical_inventory WHERE current_Stock<reorder_level")
surgical_low_stock_result=cursor.fetchone()

cursor.execute("SELECT COUNT(*) FROM surgical_inventory WHERE current_stock=0")
surgical_out_of_stock_result=cursor.fetchone()

col1,col2,col3=st.columns(3) #this defines the col1 and col2
with col1:
    st.metric("Total Drugs:",drug_result[0])     #puts the string side by side 
with col2:
    st.metric("Low Stock Drugs:",low_stock_result[0])
with col3:
     st.metric("Out of Stock Drugs:",out_of_stock_result[0])


col4,col5,col6=st.columns(3)    
with col4:
     st.metric("Total Surgical Supplies",surgical_result[0])
with col5:
    st.metric("Low Stock Surgical Supplies:",surgical_low_stock_result[0])
with col6:
    st.metric("Out of Stock Surgical Supplies:",surgical_out_of_stock_result[0])


