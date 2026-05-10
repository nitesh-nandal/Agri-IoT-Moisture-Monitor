import pandas as pd
import numpy as np
import time
from datetime import datetime
import os


        ## PHASE 1: RANDOM VALUES GENERATOR ##
        



File_name= "raw_sensor_data.csv"

def generate_sensor_data():
    while True:
        #step1: create a time stamp
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        #step2: create random moisture value between 20.0 and 40.0
        moisture = round(np.random.uniform(20, 40), 2)

        #Step3: create chaos or bug intentionally . numbers will be between 0.0 and 1.0
        random_variable = np.random.random()
        if random_variable < 0.1: # 10% probability and simulates missing value
            moisture = None
        elif random_variable < 0.15: # 5% probability and simulates a outlier
            moisture = 999.0

        #step4 : Create a data frame of one-row to store all these values:
        new_data = pd.DataFrame([{
            "sensor_id": "101",
            "timestamp": now,
            "moisture_level": moisture,
        
        }])

        #Step5: write to the csv file we created at the start
        if not os.path.isfile(File_name):
            new_data.to_csv(File_name, index=False)
        else:
            new_data.to_csv(File_name, mode="a", header=False, index=False)

        print(f"Logged:{now} | Moisture:{moisture}%")
        time.sleep(1) # it sleeps or pauses for 5 seconds before generating another value

# this is our entry gate#
if __name__ == "__main__":
    print("Starting Agri-IoT Simulator... Press Ctrl+C to stop.")
    generate_sensor_data()