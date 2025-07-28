import pandas as pd
import psycopg2
from psycopg2 import sql

# Step 1: Read the Excel file
excel_path = "VendorData.xlsx"  # Make sure this file is in the current directory
df = pd.read_excel(excel_path)

# Step 2: PostgreSQL (NeonDB) connection details
conn_str = "postgresql://neondb_owner:npg_98qZtiaRWBKN@ep-ancient-morning-a1t0645z-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

# Step 3: Connect to PostgreSQL
conn = psycopg2.connect(conn_str)
cursor = conn.cursor()

# Step 4: Create table dynamically
table_name = "VendorData"
columns = df.columns

# Drop table if it exists
cursor.execute(sql.SQL("DROP TABLE IF EXISTS {}").format(sql.Identifier(table_name)))

# Create table with NVARCHAR (as TEXT in PostgreSQL)
create_query = sql.SQL("CREATE TABLE {} ({})").format(
    sql.Identifier(table_name),
    sql.SQL(", ").join(
        sql.SQL("{} TEXT").format(sql.Identifier(col)) for col in columns
    )
)
cursor.execute(create_query)
conn.commit()

# Step 5: Insert data into the table
for _, row in df.iterrows():
    insert_query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
        sql.Identifier(table_name),
        sql.SQL(", ").join(map(sql.Identifier, columns)),
        sql.SQL(", ").join(sql.Placeholder() * len(columns))
    )
    cursor.execute(insert_query, tuple(row))

conn.commit()

# Step 6: Close connection
cursor.close()
conn.close()

print("✅ Excel data successfully inserted into NeonDB PostgreSQL database.")
