import sqlite3
import pandas as pd 
conn=sqlite3.connect("Farm_data.db")                  # Create a connection to the database

query="SELECT * FROM sensor_data"              # write the query 

df=pd.read_sql(query,conn)                              #Read the sql query at required connection and close the connection

print(df)

# Check the total row count
count_query = "SELECT COUNT(*) as total_rows FROM sensor_data"

count_df = pd.read_sql(count_query, conn)

print(f"\nTotal rows currently in DB: {count_df['total_rows'][0]}")






conn.close()