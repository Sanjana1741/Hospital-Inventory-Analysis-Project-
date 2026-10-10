import streamlit as st
import pandas as pd 
from database import get_connection

if "logged_in" not in st.session_state:
    st.session_state.logged_in=False

drug_csv=pd.read_csv(r"C:/Users/mani-/Desktop/Sanjana_17/Final Hospital Dataset/drug.csv",)
drug_inventory_csv=pd.read_csv(r"C:/Users/mani-/Desktop/Sanjana_17/Final Hospital Dataset/drug_inventory.csv",)
# Credintials page code(1st page)
if not st.session_state.logged_in:
    st.title("Hospital Inventory")
    st.title("Welcome to Inventory Dashboard")
    
    files={"Doctor":r"C:\Users\mani-\Desktop\Sanjana_17\Final Hospital Dataset\doctor.csv","Nurse":r"C:\Users\mani-\Desktop\Sanjana_17\Final Hospital Dataset\nurse.csv","Inventory Staff":r"C:\Users\mani-\Desktop\Sanjana_17\Final Hospital Dataset\Inventory.csv"}
    
    Designation=st.selectbox("Select your role:",['Doctor','Nurse','Inventory Staff'])
    
    EmployeeID=st.text_input("Enter your Employee ID")
    Password=st.text_input("Enter your password")
    
    if st.button("Login"):
        selected_files=files[Designation]
        data=pd.read_csv(selected_files)
        
        entered_id = EmployeeID.strip()
        print("Login button clicked")
        
        if EmployeeID in data["employee_id"].astype(str).str.strip().values:
            user = data[data["employee_id"].astype(str).str.strip() == EmployeeID]
            
            if Password == user["password"].iloc[0]:
                st.session_state.logged_in=True
                st.rerun()
            else:
                st.error("Incorrect password")
        else:
            st.write("Employee ID not found")
else:
    st.write("Hosptial Inventory Dashboard")
    st.write("Login successfull")

# Check for low-stock drugs
    db = get_connection()
    cursor = db.cursor()

    cursor.execute(
        """
        SELECT drug_name, current_stock, reorder_level
        FROM drugs
        JOIN drug_inventory
        ON drugs.drug_id = drug_inventory.drug_id
        WHERE current_stock < reorder_level
        """
    )

    low_stock_drugs = cursor.fetchall()

    critical_drugs = []   #this creates a empty list ("I'm going to create a box called critical_drugs, and whenever I find a critically low drug, I'll put its name inside this box.")

    for row in low_stock_drugs:    #"Go through every row inside low_stock_drugs, one at a time."
        drug_name = row[0]      #"Take the first value from this row and store it in drug_name."
        current_stock = row[1]
        reorder_level = row[2]

        if current_stock <= reorder_level * 0.20:
            critical_drugs.append(drug_name)    #Create an empty list for critical drugs. Go through every low-stock drug. Get its name, current stock, and reorder level. If its current stock is 20% or less of its reorder level, add its name to the critical-drugs list."

    if critical_drugs:
        st.toast(
            f"🚨 {len(critical_drugs)} drugs are critically low!",
            icon="🔴"
        )

    low_drugs = len(low_stock_drugs) - len(critical_drugs)

    if low_drugs:
        st.toast(
            f"⚠️ {low_drugs} drugs are below their reorder level!",
            icon="🟠"
        )


    cursor.close()
    db.close()

        # Check for low-stock surgical supplies
    db = get_connection()
    cursor = db.cursor()

    cursor.execute(
        """
        SELECT s.name, i.current_stock, i.reorder_level
        FROM surgical_supplies s
        JOIN surgical_inventory i
        ON s.equipment_id = i.equipment_id
        WHERE i.current_stock < i.reorder_level
        """
    )

    low_stock_supplies = cursor.fetchall()

    # Find critically low surgical supplies
    critical_supplies = []

    for row in low_stock_supplies:
        supply_name = row[0]
        current_stock = row[1]
        reorder_level = row[2]

        if current_stock <= reorder_level * 0.20:
            critical_supplies.append(supply_name)

    # Critical surgical supply notification
    if critical_supplies:
        st.toast(
            f"🚨 {len(critical_supplies)} surgical supplies are critically low!",
            icon="🔴"
        )

    # Normal low-stock surgical supplies
    low_supplies = len(low_stock_supplies) - len(critical_supplies)

    if low_supplies:
        st.toast(
            f"⚠️ {low_supplies} surgical supplies are below their reorder level!",
            icon="🟠"
        )

    cursor.close()
    db.close()

    #Code for selecting which to manage
    option=st.selectbox(
        "What do you want to manage?",
        ["Drugs","Surgical supplies"]
    )
    
    if option=="Drugs":
        st.write("Drug Inventory")
        category=st.selectbox(
            "Select Drug Category",
            ["Antibiotic","Anitpyretic","Analgesic","Antacid","Anithypertensive","Vitamin","Seteroid","Antidiabetic"]
        )
        drug_name=st.text_input("Search for a Drug:")
#code which fetches the drug data from the database 
        if st.button("Search"):
            db=get_connection()
            cursor=db.cursor()

            cursor.execute(
                """
                SELECT
                d.drug_id,
                d.drug_name,
                d.brand_name,
                d.drug_category,
                d.unit_cost,
                
                m.manufacturer_name,
                m.country,
                m.reliability,
                m.contract_status,
                
                i.current_stock,
                i.reorder_level,
                i.inv_status,
                i.last_restock
            
            FROM drugs d
            
            JOIN drug_manufacturer m
                ON d.manufacturer_id = m.manufacturer_id
            JOIN drug_inventory i
                ON d.drug_id = i.drug_id
            WHERE d.drug_category = %s
            AND d.drug_name = %s
                """,
               (category, drug_name)  
            )
            result=cursor.fetchall()

            cursor.close()
            db.close()

            if result:
                row = result[0]
                drug_id = row[0]
                drug_name = row[1]
                brand_name = row[2]
                category = row[3]
                unit_cost = row[4]
                
                manufacturer_name = row[5]
                country = row[6]
                reliability = row[7]
                contract_status = row[8]
                
                current_stock = row[9]
                reorder_level = row[10]
                inventory_status = row[11]
                last_restock = row[12]
                
                st.subheader("💊 Drug Information")
                st.write("Drug Name:", drug_name)
                st.write("Brand Name:", brand_name)
                st.write("Category:", category)
                st.write("Unit Cost:", unit_cost)
                
                st.subheader("🏭 Manufacturer Information")
                st.write("Manufacturer:", manufacturer_name)
                st.write("Country:", country)
                st.write("Reliability:", reliability)
                st.write("Contract Status:", contract_status)
                
                st.subheader("📦 Inventory Information")
                st.write("Current Stock:", current_stock)
                st.write("Reorder Level:", reorder_level)
                st.write("Inventory Status:", inventory_status)
                st.write("Last Restock:", last_restock)


                #Caclulations
                stock_difference=current_stock-reorder_level

                if reorder_level>0:
                    stock_percentage=(current_stock/reorder_level)*100
                else:
                    stock_percentage=0
                if current_stock==0:
                    calculated_status="Out of Stock"
                elif current_stock < reorder_level:
                    calculated_status="Low Stock"
                else:
                    calculated_status="Normal" 


                if current_stock < reorder_level:
                    suggested_order = reorder_level - current_stock
                else:
                    suggested_order = 0   

                st.subheader("📊 Inventory Calculations")
                st.write("Stock Difference:", stock_difference)
                st.write("Stock Percentage:", f"{stock_percentage:.2f}%")
                st.write("Calculated Status:", calculated_status)
                st.write("Suggested Order Quantity:", suggested_order)
            else:
                st.error("Drug not Found")
    elif option.strip().lower() == "surgical supplies":
        st.write("i am inside surgical supply inventory")

        category=st.selectbox(
            "Select Surgical Supply category",
            ["Surgical Instrument","Suture","Protective Wear","Dressing","Drape and Linen","Disposable","Electrosurgical","Laparoscopic"]
        )
        surgical_supply_name=st.text_input("Search for Surgical supply")

        if st.button("Search"):
            db=get_connection()
            cursor=db.cursor()
            cursor.execute(
                  """
            SELECT
                s.equipment_id,
                s.name,
                s.brand_name,
                s.category,
                s.unit_cost,

                m.name,
                m.country,
                m.reliability_rating,
                m.contract_status,

                i.current_stock,
                i.reorder_level,
                i.inventory_status,
                i.last_restock_date

            FROM surgical_supplies s

            JOIN surgical_manufacturer m
                ON s.manufacturer_id = m.manufacturer_id

            JOIN surgical_inventory i
                ON s.equipment_id = i.equipment_id

            WHERE s.category = %s
            AND s.name = %s
            """,
            (category, surgical_supply_name)
        )
            result=cursor.fetchall()

            cursor.close()
            db.close()

            if result:
                row = result[0]
                
                equipment_id = row[0]
                supply_name = row[1]
                brand_name = row[2]
                category = row[3]
                unit_cost = row[4]
                
                manufacturer_name = row[5]
                country = row[6]
                reliability = row[7]
                contract_status = row[8]
                
                current_stock = row[9]
                reorder_level = row[10]
                inventory_status = row[11]
                last_restock = row[12]

                # Inventory calculations
                stock_difference = current_stock - reorder_level

                if reorder_level > 0:
                    stock_percentage = (current_stock / reorder_level) * 100
                else:
                    stock_percentage = 0

                if current_stock == 0:
                    calculated_status = "Out of Stock"
                elif current_stock < reorder_level:
                    calculated_status = "Low Stock"
                else:
                    calculated_status = "Normal"

                if current_stock < reorder_level:
                    suggested_order = reorder_level - current_stock
                else:
                    suggested_order = 0

                # Supply information
                st.subheader("🔧 Surgical Supply Information")
                st.write("Supply Name:", supply_name)
                st.write("Brand Name:", brand_name)
                st.write("Category:", category)
                st.write("Unit Cost:", unit_cost)

                # Manufacturer information
                st.subheader("🏭 Manufacturer Information")
                st.write("Manufacturer:", manufacturer_name)
                st.write("Country:", country)
                st.write("Reliability:", reliability)
                st.write("Contract Status:", contract_status)

                # Inventory information
                st.subheader("📦 Inventory Information")
                st.write("Current Stock:", current_stock)
                st.write("Reorder Level:", reorder_level)
                st.write("Inventory Status:", inventory_status)
                st.write("Last Restock:", last_restock)

                # Calculations
                st.subheader("📊 Inventory Calculations")
                st.write("Stock Difference:", stock_difference)
                st.write("Stock Percentage:", f"{stock_percentage:.2f}%")
                st.write("Calculated Status:", calculated_status)
                st.write("Suggested Order Quantity:", suggested_order)

            else:
                st.error("Surgical supply not found in this category.")
