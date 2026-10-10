import streamlit as st
from database import get_connection
import pandas as pd

connection=get_connection()  #connect to mysql
cursor=connection.cursor()   #give me a way to communicate with mysql

cursor.execute(
    """
    SELECT drug_name,current_stock,reorder_level
    FROM drugs
    JOIN drug_inventory
    ON drugs.drug_id=drug_inventory.drug_id
    WHERE current_stock<reorder_level
    """
)
low_stock_drugs=cursor.fetchall()



if low_stock_drugs:
    st.toast(
         f"🚨 {len(low_stock_drugs)} drugs are below their reorder level!",
        icon="⚠️"
    )
    