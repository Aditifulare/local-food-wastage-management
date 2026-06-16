# 🍱 Local Food Wastage Management System

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://local-food-wastage-management-4y77gbgytmwykvtku4d6jc.streamlit.app/)

A data-driven web application to reduce food wastage by connecting surplus food providers with those in need.

---

## 📌 Project Overview

Food wastage is a major issue — restaurants and households discard surplus food while many people struggle with food insecurity. This system bridges that gap by:

- Allowing restaurants and individuals to list surplus food
- Enabling NGOs and individuals to claim available food
- Storing and managing data using MySQL
- Providing an interactive Streamlit web app for real-time interaction

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Backend logic & data processing |
| MySQL | Database storage & querying |
| Streamlit | Web application UI |
| Pandas | Data manipulation |

---

## 📂 Dataset

| File | Description |
|------|-------------|
| `providers_data.csv` | Food providers (restaurants, grocery stores, etc.) |
| `receivers_data.csv` | Food receivers (NGOs, individuals, community centers) |
| `food_listings_data.csv` | Available food items with quantity and expiry |
| `claims_data.csv` | Food claims made by receivers |

---

## ⚙️ Features

- **Home Dashboard** — Key metrics (total providers, receivers, listings, claims)
- **SQL Query Results** — 15 analytical queries with interactive output
- **Food Listings** — Filter by city, food type, and meal type with provider contact details
- **CRUD Operations** — Add, update, and delete food listings in real time

---

## 📊 SQL Queries Covered

1. Providers & receivers count per city
2. Provider type with most food contributions
3. Provider contact info by city
4. Receivers with most claims
5. Total quantity of food available
6. City with highest food listings
7. Most common food types
8. Claims per food item
9. Provider with most successful claims
10. Claims percentage (Completed vs Pending vs Cancelled)
11. Average quantity claimed per receiver
12. Most claimed meal type
13. Total food donated per provider
14. Food expiring soon (next 30 days)
15. City-wise total food claimed

---

## 🚀 How to Run

1. Clone the repository:
```
git clone https://github.com/Aditifulare/local-food-wastage-management.git
```

2. Install dependencies:
```
pip install streamlit pandas mysql-connector-python
```

3. Set up MySQL database:
- Create database `food_waste_db`
- Run `data_load.py` to load CSV data into MySQL

4. Run the Streamlit app:
```
python -m streamlit run app.py
```

---

## 📁 Project Structure

```
📦 local-food-wastage-management
 ┣ 📄 app.py                  # Main Streamlit application
 ┣ 📄 data_load.py            # Script to load CSV data into MySQL
 ┣ 📄 providers_data.csv      # Providers dataset
 ┣ 📄 receivers_data.csv      # Receivers dataset
 ┣ 📄 food_listings_data.csv  # Food listings dataset
 ┗ 📄 claims_data.csv         # Claims dataset
```

---

## 👩‍💻 Author

**Aditi Fulare**  
B.Sc. Computer Science | Data Analyst Enthusiast  
[GitHub](https://github.com/Aditifulare) | [LinkedIn](https://www.linkedin.com/in/aditi-fulare)
