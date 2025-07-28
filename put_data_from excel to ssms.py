import pandas as pd
import pyodbc

# Step 1: Read the Excel file
excel_path = "VendorData.xlsx"  # Ensure the file is in the same directory
df = pd.read_excel(excel_path)

# Step 2: Set up SQL Server connection (Windows Authentication)
server = r'OMEN\SQLEXPRESS'
database = 'VendorDB'
conn_str = (
    f'DRIVER={{SQL Server}};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'Trusted_Connection=yes;'
)

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Step 3: Create table dynamically based on Excel columns
table_name = "VendorData"
columns_with_types = ", ".join([f"[{col}] NVARCHAR(MAX)" for col in df.columns])

# Drop table if it already exists
drop_query = f"IF OBJECT_ID('{table_name}', 'U') IS NOT NULL DROP TABLE {table_name}"
cursor.execute(drop_query)

# Create new table
create_query = f"CREATE TABLE {table_name} ({columns_with_types})"
cursor.execute(create_query)
conn.commit()

# Step 4: Insert Excel data into the table
for _, row in df.iterrows():
    placeholders = ", ".join("?" * len(row))
    insert_query = f"INSERT INTO {table_name} VALUES ({placeholders})"
    cursor.execute(insert_query, tuple(row))

conn.commit()

# Step 5: Close connections
cursor.close()
conn.close()

print("✅ Excel data successfully inserted into VendorDB database.")
