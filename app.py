import streamlit as st
import pandas as pd
import plotly.express as px
 
# Load data from CSV
@st.cache_data
def load_data():
    providers = pd.read_csv("providers_data.csv")
    receivers = pd.read_csv("receivers_data.csv")
    food_listings = pd.read_csv("food_listings_data.csv")
    claims = pd.read_csv("claims_data.csv")
    return providers, receivers, food_listings, claims
 
providers, receivers, food_listings, claims = load_data()
 
# Page config
st.set_page_config(page_title="Local Food Wastage Management", layout="wide", page_icon="🍱")
 
# Custom CSS
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .banner {
        background: linear-gradient(135deg, #1f4037, #99f2c8);
        padding: 40px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 30px;
    }
    .banner h1 { color: white; font-size: 2.8em; margin: 0; }
    .banner p { color: #e0ffe0; font-size: 1.2em; margin-top: 10px; }
    .metric-card {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border: 1px solid #0f3460;
        border-radius: 12px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .metric-card h2 { color: #99f2c8; font-size: 2.5em; margin: 0; }
    .metric-card p { color: #aaaaaa; font-size: 1em; margin-top: 5px; }
    .section-title {
        color: #99f2c8;
        font-size: 1.5em;
        font-weight: bold;
        margin: 20px 0 10px 0;
        border-left: 4px solid #99f2c8;
        padding-left: 10px;
    }
    </style>
""", unsafe_allow_html=True)
 
# Sidebar
st.sidebar.image("https://img.icons8.com/color/96/food-bank.png", width=80)
st.sidebar.title("🍱 Food Waste Manager")
st.sidebar.markdown("---")
menu = st.sidebar.radio("Navigate", [
    "🏠 Home",
    "📈 EDA - Analysis & Charts",
    "📊 SQL Query Results",
    "🥗 Food Listings",
    "⚙️ CRUD Operations"
])
 
# HOME
if menu == "🏠 Home":
    st.markdown("""
        <div class="banner">
            <h1>🍱 Local Food Wastage Management System</h1>
            <p>Connecting surplus food providers with those in need — reducing waste, fighting hunger.</p>
        </div>
    """, unsafe_allow_html=True)
 
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""<div class="metric-card"><h2>{len(providers)}</h2><p>🏪 Total Providers</p></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="metric-card"><h2>{len(receivers)}</h2><p>🤝 Total Receivers</p></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class="metric-card"><h2>{len(food_listings)}</h2><p>🍽️ Food Listings</p></div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""<div class="metric-card"><h2>{len(claims)}</h2><p>📋 Total Claims</p></div>""", unsafe_allow_html=True)
 
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">📌 About This System</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("🏪 **Providers** — Restaurants, grocery stores, and supermarkets list surplus food.")
    with col2:
        st.success("🤝 **Receivers** — NGOs, community centers, and individuals claim available food.")
    with col3:
        st.warning("📊 **Analytics** — Track food wastage trends and distribution patterns.")
 
# EDA
elif menu == "📈 EDA - Analysis & Charts":
    st.markdown('<div class="section-title">📈 Exploratory Data Analysis</div>', unsafe_allow_html=True)
 
    col1, col2 = st.columns(2)
 
    with col1:
        st.markdown("#### 1. Claims Distribution by Status")
        df1 = claims['Status'].value_counts().reset_index()
        df1.columns = ['Status', 'count']
        fig1 = px.pie(df1, names='Status', values='count', title='Claims by Status',
                      color_discrete_sequence=px.colors.sequential.Teal)
        st.plotly_chart(fig1, use_container_width=True)
 
    with col2:
        st.markdown("#### 2. Food Type Distribution")
        df2 = food_listings['Food_Type'].value_counts().reset_index()
        df2.columns = ['Food_Type', 'count']
        fig2 = px.pie(df2, names='Food_Type', values='count', title='Food Type Distribution',
                      color_discrete_sequence=px.colors.sequential.Mint)
        st.plotly_chart(fig2, use_container_width=True)
 
    st.markdown("#### 3. Meal Type wise Claims")
    merged = claims.merge(food_listings, on='Food_ID')
    df3 = merged['Meal_Type'].value_counts().reset_index()
    df3.columns = ['Meal_Type', 'total_claims']
    fig3 = px.bar(df3, x='Meal_Type', y='total_claims', color='Meal_Type',
                  title='Claims by Meal Type', color_discrete_sequence=px.colors.sequential.Teal)
    st.plotly_chart(fig3, use_container_width=True)
 
    st.markdown("#### 4. Provider Type wise Food Contribution")
    merged2 = food_listings.merge(providers, on='Provider_ID')
    df4 = merged2.groupby('Type')['Quantity'].sum().reset_index()
    df4.columns = ['Type', 'total_food']
    fig4 = px.bar(df4, x='Type', y='total_food', color='Type',
                  title='Food Contribution by Provider Type',
                  color_discrete_sequence=px.colors.sequential.Mint)
    st.plotly_chart(fig4, use_container_width=True)
 
    st.markdown("#### 5. Top 10 Cities with Most Food Listings")
    df5 = food_listings['Location'].value_counts().head(10).reset_index()
    df5.columns = ['Location', 'total_listings']
    fig5 = px.bar(df5, x='Location', y='total_listings', color='total_listings',
                  title='Top 10 Cities - Food Listings', color_continuous_scale='Teal')
    st.plotly_chart(fig5, use_container_width=True)
 
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 6. Receiver Type Distribution")
        df6 = receivers['Type'].value_counts().reset_index()
        df6.columns = ['Type', 'count']
        fig6 = px.pie(df6, names='Type', values='count', title='Receiver Types',
                      color_discrete_sequence=px.colors.sequential.Teal)
        st.plotly_chart(fig6, use_container_width=True)
 
    with col2:
        st.markdown("#### 7. Top 10 Food Items by Quantity")
        df7 = food_listings.groupby('Food_Name')['Quantity'].sum().reset_index().sort_values('Quantity', ascending=False).head(10)
        fig7 = px.bar(df7, x='Food_Name', y='Quantity', color='Quantity',
                      title='Top 10 Food Items by Quantity', color_continuous_scale='Mint')
        st.plotly_chart(fig7, use_container_width=True)
 
# SQL QUERIES
elif menu == "📊 SQL Query Results":
    st.markdown('<div class="section-title">📊 SQL Query Results</div>', unsafe_allow_html=True)
 
    query_name = st.selectbox("Select a Query", [
        "Q1: Providers count per city",
        "Q2: Provider type with most food",
        "Q3: Provider contact info by city",
        "Q4: Receivers with most claims",
        "Q5: Total food available",
        "Q6: City with most food listings",
        "Q7: Most common food types",
        "Q8: Claims per food item",
        "Q9: Provider with most successful claims",
        "Q10: Claims percentage by status",
        "Q11: Avg quantity claimed per receiver",
        "Q12: Most claimed meal type",
        "Q13: Total food donated per provider",
        "Q14: Food expiring soon",
        "Q15: City wise total food claimed",
    ])
 
    if st.button("▶ Run Query"):
        if query_name == "Q1: Providers count per city":
            result = providers.groupby('City').size().reset_index(name='provider_count').sort_values('provider_count', ascending=False).head(10)
        elif query_name == "Q2: Provider type with most food":
            merged = food_listings.merge(providers, on='Provider_ID')
            result = merged.groupby('Type')['Quantity'].sum().reset_index(name='total_food').sort_values('total_food', ascending=False)
        elif query_name == "Q3: Provider contact info by city":
            result = providers[['Name', 'Type', 'Address', 'Contact']].head(10)
        elif query_name == "Q4: Receivers with most claims":
            result = claims.groupby('Receiver_ID').size().reset_index(name='total_claims').merge(receivers, on='Receiver_ID').sort_values('total_claims', ascending=False).head(10)[['Name', 'Type', 'total_claims']]
        elif query_name == "Q5: Total food available":
            result = pd.DataFrame({'total_food_available': [food_listings['Quantity'].sum()]})
        elif query_name == "Q6: City with most food listings":
            result = food_listings['Location'].value_counts().head(10).reset_index()
            result.columns = ['Location', 'total_listings']
        elif query_name == "Q7: Most common food types":
            result = food_listings['Food_Type'].value_counts().reset_index()
            result.columns = ['Food_Type', 'count']
        elif query_name == "Q8: Claims per food item":
            result = claims.groupby('Food_ID').size().reset_index(name='total_claims').merge(food_listings[['Food_ID', 'Food_Name']], on='Food_ID').sort_values('total_claims', ascending=False).head(10)
        elif query_name == "Q9: Provider with most successful claims":
            completed = claims[claims['Status'] == 'Completed']
            merged = completed.merge(food_listings, on='Food_ID').merge(providers, on='Provider_ID')
            result = merged.groupby(['Name', 'Type']).size().reset_index(name='successful_claims').sort_values('successful_claims', ascending=False).head(10)
        elif query_name == "Q10: Claims percentage by status":
            result = claims['Status'].value_counts().reset_index()
            result.columns = ['Status', 'count']
            result['percentage'] = (result['count'] / result['count'].sum() * 100).round(2)
        elif query_name == "Q11: Avg quantity claimed per receiver":
            merged = claims.merge(food_listings, on='Food_ID').merge(receivers, on='Receiver_ID')
            result = merged.groupby('Name')['Quantity'].mean().reset_index(name='avg_quantity_claimed').sort_values('avg_quantity_claimed', ascending=False).head(10)
        elif query_name == "Q12: Most claimed meal type":
            merged = claims.merge(food_listings, on='Food_ID')
            result = merged['Meal_Type'].value_counts().reset_index()
            result.columns = ['Meal_Type', 'total_claims']
        elif query_name == "Q13: Total food donated per provider":
            merged = food_listings.merge(providers, on='Provider_ID')
            result = merged.groupby(['Name', 'Type'])['Quantity'].sum().reset_index(name='total_donated').sort_values('total_donated', ascending=False).head(10)
        elif query_name == "Q14: Food expiring soon":
            food_listings['Expiry_Date'] = pd.to_datetime(food_listings['Expiry_Date'])
            today = pd.Timestamp.today()
            result = food_listings[food_listings['Expiry_Date'] <= today + pd.Timedelta(days=30)][['Food_Name', 'Quantity', 'Expiry_Date', 'Location']].sort_values('Expiry_Date')
        elif query_name == "Q15: City wise total food claimed":
            completed = claims[claims['Status'] == 'Completed']
            merged = completed.merge(food_listings, on='Food_ID').merge(providers, on='Provider_ID')
            result = merged.groupby('City')['Quantity'].sum().reset_index(name='total_food_claimed').sort_values('total_food_claimed', ascending=False).head(10)
 
        st.dataframe(result, use_container_width=True)
 
# FOOD LISTINGS
elif menu == "🥗 Food Listings":
    st.markdown('<div class="section-title">🥗 Food Listings</div>', unsafe_allow_html=True)
 
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_city = st.selectbox("🏙️ Filter by City", ["All"] + sorted(food_listings['Location'].unique().tolist()))
    with col2:
        selected_food_type = st.selectbox("🥦 Filter by Food Type", ["All"] + sorted(food_listings['Food_Type'].unique().tolist()))
    with col3:
        selected_meal_type = st.selectbox("🍽️ Filter by Meal Type", ["All"] + sorted(food_listings['Meal_Type'].unique().tolist()))
 
    merged = food_listings.merge(providers[['Provider_ID', 'Name', 'Contact']], on='Provider_ID')
    merged.rename(columns={'Name': 'Provider_Name', 'Contact': 'Provider_Contact'}, inplace=True)
 
    result = merged.copy()
    if selected_city != "All":
        result = result[result['Location'] == selected_city]
    if selected_food_type != "All":
        result = result[result['Food_Type'] == selected_food_type]
    if selected_meal_type != "All":
        result = result[result['Meal_Type'] == selected_meal_type]
 
    st.success(f"Total records: {len(result)}")
    st.dataframe(result, use_container_width=True)
 
# CRUD
elif menu == "⚙️ CRUD Operations":
    st.markdown('<div class="section-title">⚙️ CRUD Operations</div>', unsafe_allow_html=True)
    st.info("💡 CRUD operations work on local MySQL database. Cloud version shows demo mode.")
 
    operation = st.radio("Select Operation", ["➕ Add Food Listing", "✏️ Update Food Listing", "🗑️ Delete Food Listing"])
 
    if operation == "➕ Add Food Listing":
        st.markdown("### Add New Food Listing")
        col1, col2 = st.columns(2)
        with col1:
            food_name = st.text_input("Food Name")
            quantity = st.number_input("Quantity", min_value=1)
            expiry_date = st.date_input("Expiry Date")
            provider_id = st.number_input("Provider ID", min_value=1)
        with col2:
            provider_type = st.selectbox("Provider Type", ["Restaurant", "Grocery Store", "Supermarket", "Catering Service"])
            location = st.text_input("Location (City)")
            food_type = st.selectbox("Food Type", ["Vegetarian", "Non-Vegetarian", "Vegan"])
            meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Snacks"])
 
        if st.button("➕ Add Listing"):
            st.success(f"✅ '{food_name}' listing added successfully!")
 
    elif operation == "✏️ Update Food Listing":
        st.markdown("### Update Food Listing")
        food_id = st.number_input("Enter Food ID to Update", min_value=1)
        new_quantity = st.number_input("New Quantity", min_value=1)
        if st.button("✏️ Update"):
            st.success(f"✅ Food ID {food_id} updated successfully!")
 
    elif operation == "🗑️ Delete Food Listing":
        st.markdown("### Delete Food Listing")
        food_id = st.number_input("Enter Food ID to Delete", min_value=1)
        if st.button("🗑️ Delete"):
            st.success(f"✅ Food ID {food_id} deleted successfully!")