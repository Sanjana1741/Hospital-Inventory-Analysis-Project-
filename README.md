 Hospital Inventory Analysis Project

A data-driven hospital inventory management and analysis dashboard developed using **Python, Streamlit, MySQL, Pandas, and Plotly**. The project helps monitor pharmaceutical and surgical supply inventory, analyze inventory costs, identify stock shortages, and determine recommended order quantities to support efficient inventory management.

 📌 Project Overview

Hospitals rely on the timely availability of medicines and surgical supplies to ensure smooth day-to-day operations. Poor inventory management can lead to stock shortages, excess inventory, and unnecessary expenditure.

The **Hospital Inventory Analysis Project** addresses these challenges through an interactive dashboard that combines database management, data analysis, and visualization. It provides inventory staff and other authorized users with a centralized interface to examine stock levels, track inventory status, evaluate costs, and identify items that require replenishment.

The project covers both **drug inventory and surgical supply inventory**, offering a consolidated view of important inventory information.

 🎯 Objectives

- Monitor the stock levels of medicines and surgical supplies.
- Identify items that have fallen below their defined reorder levels.
- Highlight critically low-stock items that require immediate attention.
- Analyze inventory value and costs across different categories.
- Identify high-stock and low-stock items for better inventory planning.
- Recommend order quantities to help replenish inventory.
- Present inventory information through interactive dashboards and visualizations.
- Provide role-based login access for different hospital personnel.

 ✨ Key Features

 1. Dashboard Overview
Provides a centralized overview of hospital inventory, including key inventory metrics and stock status information.

 2. Drug Inventory Analysis
Enables users to explore medicine details, including drug names, categories, manufacturers, unit costs, current stock, reorder levels, and inventory status. Category filtering and medicine search help users locate specific items.

 3. Surgical Supply Inventory Analysis
Extends inventory monitoring to surgical supplies and equipment. Users can examine supply details, categories, manufacturers, stock levels, reorder thresholds, and inventory status.

 4. Inventory Cost Analysis
Analyzes the financial value of hospital inventory using item costs and available stock quantities. Interactive charts help compare inventory value across categories and identify high-cost items.

 5. Smart Low-Stock Alerts
Identifies medicines and surgical supplies that fall below their reorder levels. Critically low-stock items are highlighted, and on-screen notifications help bring potential shortages to the user's attention.

 6. Recommended Order Quantity
Helps determine the quantity of items that may need to be ordered based on current stock and the defined reorder level, supporting more informed replenishment decisions.

 7. Role-Based Login
Provides a login interface for different hospital personnel, including doctors, nurses, and inventory staff, with access managed through the application's authentication logic.

 🛠️ Technology Stack

| Technology | Purpose |

| Python | Core application logic and data processing |
| Streamlit | Interactive web dashboard and user interface |
| MySQL | Relational database for inventory and related records |
| Pandas | Data manipulation, analysis, and processing |
| Plotly | Interactive charts and data visualizations |
| SQL | Querying, filtering, joining, and aggregating inventory data |
| Git and GitHub | Version control and project hosting |

 🗄️ Database Overview

The project uses a MySQL relational database to organize hospital inventory data and related information.

The database includes tables for:

- Drugs
- Drug inventory
- Drug manufacturers
- Surgical supplies
- Surgical inventory
- Surgical manufacturers
- Departments and other related hospital records

Primary keys and foreign key relationships help connect inventory items with their associated details.

 📊 Analysis and Insights

The dashboard supports analysis of:

- Current stock levels and reorder thresholds
- Normal, low-stock, and critical inventory status
- High-stock and low-stock items
- Inventory quantities across categories
- Total inventory value and category-wise costs
- Items that may require replenishment

These insights help make inventory information easier to interpret and can support more informed inventory planning.

 🏗️ Project Structure


Hospital-Inventory/
│
├── app.py
├── database.py
├── .gitignore
│
└── pages/
    ├── dashboard.py
    ├── Inventory_Analysis.py
    ├── Cost_Analysis.py
    └── Smart_stock_alert.py

- app.py — Main Streamlit application and login flow.
- database.py — Database connection functionality.
- pages/dashboard.py — Dashboard overview.
- pages/Inventory_Analysis.py — Inventory analysis.
- pages/Cost_Analysis.py — Inventory cost analysis.
- pages/Smart_stock_alert.py — Low-stock monitoring and alerts.

 ⚙️ Installation and Setup

 Prerequisites

- Python 3.10 or a compatible version
- MySQL Server
- pip package manager

 1. Clone the repository

```bash
git clone https://github.com/Sanjana1741/Hospital-Inventory-Analysis-Project-.git
cd Hospital-Inventory-Analysis-Project-
```

 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

 3. Install the required packages

```bash
pip install streamlit pandas plotly mysql-connector-python
```

 4. Configure the database

- Start your MySQL server.
- Create the database and tables required by the application.
- Update the database connection settings in `database.py` to match your local MySQL configuration.
- Ensure the required inventory data is available in the database.

**Security note:** Do not commit database passwords, API keys, or other sensitive credentials to GitHub.

 5. Run the application

```bash
streamlit run app.py
```

The application should open in your browser at the local Streamlit address displayed in the terminal.

 🔮 Future Enhancements

- Deploy the dashboard to a cloud hosting platform.
- Add downloadable inventory and cost analysis reports.
- Introduce inventory movement and historical stock tracking.
- Improve authentication and role-based authorization.
- Add configurable reorder rules and more advanced replenishment recommendations.

 👩‍💻 Project Purpose

This project demonstrates the practical application of **Python programming, SQL database management, data analysis, and interactive visualization** to a real-world hospital inventory management problem.

It was developed as an academic and portfolio project to explore how data-driven tools can improve inventory visibility, highlight potential shortages, and support operational decision-making.



Developed using Python, Streamlit, MySQL, Pandas, and Plotly.
