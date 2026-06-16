
import streamlit as st
import pandas as pd
import mysql.connector
 
# Database connection
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="aditi140505",
        database="food_waste_db"
    )
 
def run_query(query):
    conn = get_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df
 
# Page config
st.set_page_config(page_title="Local Food Wastage Management", layout="wide")
st.title("🍱 Local Food Wastage Management System")
 
# Sidebar
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to", [
    "Home",
    "SQL Query Results",
    "Food Listings",
    "CRUD Operations"
])
 
if menu == "Home":
    st.subheader("Welcome!")
    st.write("This system connects surplus food providers with those in need.")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Providers", run_query("SELECT COUNT(*) as c FROM providers")['c'][0])
    col2.metric("Total Receivers", run_query("SELECT COUNT(*) as c FROM receivers")['c'][0])
    col3.metric("Food Listings", run_query("SELECT COUNT(*) as c FROM food_listings")['c'][0])
    col4.metric("Total Claims", run_query("SELECT COUNT(*) as c FROM claims")['c'][0])
 
elif menu == "SQL Query Results":
    st.subheader("📊 SQL Query Results")
 
    queries = {
        "Q1: Providers & Receivers count per city": "SELECT city, COUNT(*) AS provider_count FROM providers GROUP BY city ORDER BY provider_count DESC LIMIT 10",
        "Q2: Provider type with most food": "SELECT p.Type, SUM(f.Quantity) AS total_food FROM providers p JOIN food_listings f ON p.Provider_ID = f.Provider_ID GROUP BY p.Type ORDER BY total_food DESC",
        "Q3: Provider contact info by city": "SELECT Name, Type, Address, Contact FROM providers WHERE City = 'New Jessica'",
        "Q4: Receivers with most claims": "SELECT r.Name, r.Type, COUNT(c.Claim_ID) AS total_claims FROM receivers r JOIN claims c ON r.Receiver_ID = c.Receiver_ID GROUP BY r.Receiver_ID, r.Name, r.Type ORDER BY total_claims DESC LIMIT 10",
        "Q5: Total food available": "SELECT SUM(Quantity) AS total_food_available FROM food_listings",
        "Q6: City with most food listings": "SELECT Location, COUNT(*) AS total_listings FROM food_listings GROUP BY Location ORDER BY total_listings DESC LIMIT 10",
        "Q7: Most common food types": "SELECT Food_Type, COUNT(*) AS count FROM food_listings GROUP BY Food_Type ORDER BY count DESC",
        "Q8: Claims per food item": "SELECT f.Food_Name, COUNT(c.Claim_ID) AS total_claims FROM food_listings f LEFT JOIN claims c ON f.Food_ID = c.Food_ID GROUP BY f.Food_ID, f.Food_Name ORDER BY total_claims DESC LIMIT 10",
        "Q9: Provider with most successful claims": "SELECT p.Name, p.Type, COUNT(c.Claim_ID) AS successful_claims FROM providers p JOIN food_listings f ON p.Provider_ID = f.Provider_ID JOIN claims c ON f.Food_ID = c.Food_ID WHERE c.Status = 'Completed' GROUP BY p.Provider_ID, p.Name, p.Type ORDER BY successful_claims DESC LIMIT 10",
        "Q10: Claims percentage by status": "SELECT Status, COUNT(*) AS count, ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM claims), 2) AS percentage FROM claims GROUP BY Status",
        "Q11: Avg quantity claimed per receiver": "SELECT r.Name, ROUND(AVG(f.Quantity), 2) AS avg_quantity_claimed FROM receivers r JOIN claims c ON r.Receiver_ID = c.Receiver_ID JOIN food_listings f ON c.Food_ID = f.Food_ID GROUP BY r.Receiver_ID, r.Name ORDER BY avg_quantity_claimed DESC LIMIT 10",
        "Q12: Most claimed meal type": "SELECT f.Meal_Type, COUNT(c.Claim_ID) AS total_claims FROM food_listings f JOIN claims c ON f.Food_ID = c.Food_ID GROUP BY f.Meal_Type ORDER BY total_claims DESC",
        "Q13: Total food donated per provider": "SELECT p.Name, p.Type, SUM(f.Quantity) AS total_donated FROM providers p JOIN food_listings f ON p.Provider_ID = f.Provider_ID GROUP BY p.Provider_ID, p.Name, p.Type ORDER BY total_donated DESC LIMIT 10",
        "Q14: Food expiring soon": "SELECT Food_Name, Quantity, Expiry_Date, Location FROM food_listings WHERE Expiry_Date BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 30 DAY) ORDER BY Expiry_Date ASC",
        "Q15: City wise total food claimed": "SELECT p.City, SUM(f.Quantity) AS total_food_claimed FROM claims c JOIN food_listings f ON c.Food_ID = f.Food_ID JOIN providers p ON f.Provider_ID = p.Provider_ID WHERE c.Status = 'Completed' GROUP BY p.City ORDER BY total_food_claimed DESC LIMIT 10",
    }
 
    selected_query = st.selectbox("Select a Query", list(queries.keys()))
    if st.button("Run Query"):
        result = run_query(queries[selected_query])
        st.dataframe(result)
 
elif menu == "Food Listings":
    st.subheader("🥗 Food Listings")
 
    col1, col2, col3 = st.columns(3)
 
    cities = run_query("SELECT DISTINCT Location FROM food_listings ORDER BY Location")['Location'].tolist()
    food_types = run_query("SELECT DISTINCT Food_Type FROM food_listings")['Food_Type'].tolist()
    meal_types = run_query("SELECT DISTINCT Meal_Type FROM food_listings")['Meal_Type'].tolist()
 
    with col1:
        selected_city = st.selectbox("Filter by City", ["All"] + cities)
    with col2:
        selected_food_type = st.selectbox("Filter by Food Type", ["All"] + food_types)
    with col3:
        selected_meal_type = st.selectbox("Filter by Meal Type", ["All"] + meal_types)
 
    query = """
        SELECT f.Food_ID, f.Food_Name, f.Quantity, f.Expiry_Date,
               f.Food_Type, f.Meal_Type, f.Location,
               p.Name as Provider_Name, p.Contact as Provider_Contact
        FROM food_listings f
        JOIN providers p ON f.Provider_ID = p.Provider_ID
        WHERE 1=1
    """
    if selected_city != "All":
        query += f" AND f.Location = '{selected_city}'"
    if selected_food_type != "All":
        query += f" AND f.Food_Type = '{selected_food_type}'"
    if selected_meal_type != "All":
        query += f" AND f.Meal_Type = '{selected_meal_type}'"
 
    result = run_query(query)
    st.write(f"Total records: {len(result)}")
    st.dataframe(result)
 
elif menu == "CRUD Operations":
    st.subheader("⚙️ CRUD Operations")
    operation = st.radio("Select Operation", ["Add Food Listing", "Update Food Listing", "Delete Food Listing"])
 
    if operation == "Add Food Listing":
        st.markdown("### Add New Food Listing")
        food_name = st.text_input("Food Name")
        quantity = st.number_input("Quantity", min_value=1)
        expiry_date = st.date_input("Expiry Date")
        provider_id = st.number_input("Provider ID", min_value=1)
        provider_type = st.selectbox("Provider Type", ["Restaurant", "Grocery Store", "Supermarket", "Catering Service"])
        location = st.text_input("Location (City)")
        food_type = st.selectbox("Food Type", ["Vegetarian", "Non-Vegetarian", "Vegan"])
        meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Snacks"])
 
        if st.button("Add Listing"):
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO food_listings (Food_Name, Quantity, Expiry_Date, Provider_ID, Provider_Type, Location, Food_Type, Meal_Type)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (food_name, quantity, expiry_date, provider_id, provider_type, location, food_type, meal_type))
            conn.commit()
            conn.close()
            st.success("Food listing added successfully!")
 
    elif operation == "Update Food Listing":
        st.markdown("### Update Food Listing")
        food_id = st.number_input("Enter Food ID to Update", min_value=1)
        new_quantity = st.number_input("New Quantity", min_value=1)
 
        if st.button("Update"):
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE food_listings SET Quantity = %s WHERE Food_ID = %s", (new_quantity, food_id))
            conn.commit()
            conn.close()
            st.success(f"Food ID {food_id} updated successfully!")
 
    elif operation == "Delete Food Listing":
        st.markdown("### Delete Food Listing")
        food_id = st.number_input("Enter Food ID to Delete", min_value=1)
 
        if st.button("Delete"):
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM food_listings WHERE Food_ID = %s", (food_id,))
            conn.commit()
            conn.close()
            st.success(f"Food ID {food_id} deleted successfully!")
            