import streamlit as st
import pandas as pd
import sqlite3

# Here we setup the page configuration

st.set_page_config(page_title="Agri IoT ",layout="wide")
st.title(" Real-Time Soil Moisture Monitor")
st.markdown("This dashboard displays cleaned data from our SQL database.")

# Data Bridge or Data Loading

def load_data():
    conn=sqlite3.connect("Farm_data.db")
    query="SELECT * FROM sensor_data"
    df=pd.read_sql(query,conn)
    conn.close()
    return df

# 3. Build the UI

df=load_data()

if not df.empty:
    
    # Metric Row: Show high-level stats
    col1,col2,col3=st.columns(3)

    with col1:
        st.metric("Total Readings",len(df))
    with col2:
        average_moisture= round(df["moisture_level"].mean(),2)
        st.metric("Average Moisture Level",f"{average_moisture}")
    with col3:
        st.metric("System Status","Healthy")
    
    st.subheader("Moisture Trends over the Time") # To create a seperate Haeader or Container 
    st.line_chart(data=df, x="timestamp", y="moisture_level")

    
    st.subheader("Recent data") # To create another seperate Haeader or Container
    st.dataframe(df.tail(10))

        #If the if not df.empty check fails, the user sees a yellow warning box telling them what to do next#
else:
    st.warning("Your database is empty. Run Your Pipeline first!!") 

if st.button("Refresh Data"):
    st.rerun()