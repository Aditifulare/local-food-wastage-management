import pandas as pd
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="aditi140505",  # apna password daal
    database="food_waste_db"
)
cursor = conn.cursor()

import os
path = r"C:\Users\aditi\OneDrive\good garbage" # jahan CSV files hain woh path daal

# Providers
df = pd.read_csv(os.path.join(path, "providers_data.csv"))
for _, row in df.iterrows():
    cursor.execute("INSERT IGNORE INTO providers VALUES (%s,%s,%s,%s,%s,%s)",
                   tuple(row))

# Receivers
df = pd.read_csv(os.path.join(path, "receivers_data.csv"))
for _, row in df.iterrows():
    cursor.execute("INSERT IGNORE INTO receivers VALUES (%s,%s,%s,%s,%s)",
                   tuple(row))

# Food Listings
df = pd.read_csv(os.path.join(path, "food_listings_data.csv"))
df['Expiry_Date'] = pd.to_datetime(df['Expiry_Date']).dt.strftime('%Y-%m-%d')
for _, row in df.iterrows():
    cursor.execute("INSERT IGNORE INTO food_listings VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                   tuple(row))

# Claims
df = pd.read_csv(os.path.join(path, "claims_data.csv"))
df['Timestamp'] = pd.to_datetime(df['Timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')
for _, row in df.iterrows():
    cursor.execute("INSERT IGNORE INTO claims VALUES (%s,%s,%s,%s,%s)",
                   tuple(row))

conn.commit()
cursor.close()
conn.close()
print("Data loaded successfully!")

