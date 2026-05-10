import pandas as pd
import numpy as np
import sqlite3
import os

def run_pipeline():

        ## LOAD THE .CSV FILE ## 

    try:
        df=pd.read_csv("/Users/nitesh/Downloads/Pipeline_IoT_sensor/raw_sensor_data.csv")
        df = pd.read_csv("raw_sensor_data.csv")
       
        print(f"Before:{len(df)}")
    except FileNotFoundError:
        print("Error:Simulator must be run first to create data!")
        return
    
    ## DETECT THE ERRORS IN THE DATA FRAME ##
    df.columns = ['sensor_id', 'timestamp', 'moisture_level']
    print(f"--Pipeline Started: Processing {len(df)} rows--")
    moisture_level_null_count=df["moisture_level"].isna().sum()
    moisture_level_glitch_count=(df["moisture_level"]==999.0).sum()

    print(f"Detected:{moisture_level_null_count} null count")
    print(f"Detected:{moisture_level_glitch_count} glitch count")

    ## CLEAN OR HEALING PROCESS ##

    #CONVERT ALL 999.0 VALUES TO NULL(NaN) VALUES

    df["moisture_level"]=df["moisture_level"].replace(999.0,"")
    df["moisture_level"]=pd.to_numeric(df["moisture_level"],errors="coerce")

## interpolation guesses and fill all the NaN/missing values##

    df["moisture_level"]=round(df["moisture_level"].interpolate(method="linear") )
    
    
    ## to cross check if all null values were interpolated ##
    # After interpolation, check if any NaNs remain
    remaining_nulls = df['moisture_level'].isna().sum()

    if remaining_nulls > 0:
        print(f"⚠️ Warning: {remaining_nulls} values could not be interpolated (Edge Cases).")
    else:
        print("✅ Success: All gaps filled.")

    


    ##Validate -- to validate the data ensure data types are correct##

    df["timestamp"]=pd.to_datetime(df["timestamp"])


    ## Final check : Drop all the remaining NaNs at the very top/bottom ##
        # we use this because for interpolation we need two point(before,NaN,after)
        # it might be possible that when you started the simulator the sensor was off
        # it returned NaN, NaN, 20 (we dont have first end to interpolate)
        # before ending the simulator values might be 20, NaN, NaN, (we dont have last end to interpolate)
    # this is why we drop all the missing values at first and end so that we can send only 100% clean data to DB# 
    
    
    df= df.dropna()

    ## TO SAVE TO CSV FILE ###

    ## we write to a new cleaned data file ##
    #df.to_csv("cleaned_sensor_data.csv",index=False)
    #print("--Pipeline Finished: Cleaned Data is saved--")
    #print(f"After:{len(df)}")



    ## TO SAVE THE DATA INTO DATABASE AS AN SQL FILE ##
    # USING SQLITE3 WE MAKE A LOCAL DATABASE IN OUR FILE AND THERE WE STROE OUR SQL FILE#

    # Create table with Primary Key if it doesn't exist , it is important so that pipepline dont load duplicate data in case of failure

    conn=sqlite3.connect("Farm_data.db")
    cursor=conn.cursor()
    create_table="""CREATE TABLE IF NOT EXISTS sensor_data (
        sensor_id INTEGER,
        timestamp DATETIME,
        moisture_level FLOAT,
        PRIMARY KEY (sensor_id, timestamp)
    );"""
    cursor.execute(create_table)
    conn.commit() ## You can create this table in a seperate file and then ujust provide the conn of  

    try:
        df.to_sql("sensor_data", conn, if_exists="append", index=False,
          method=lambda table, conn, keys, data_iter:
              conn.executemany(
                  f"INSERT OR IGNORE INTO {table.name} ({','.join(keys)}) VALUES ({','.join(['?']*len(keys))})",
                  data_iter
              ))
    except Exception as e:
        print(f"sql error: {e}")
    finally:
        conn.close()


if __name__=="__main__":
    run_pipeline()