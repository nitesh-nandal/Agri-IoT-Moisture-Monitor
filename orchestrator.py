import subprocess
import time
import sys

def start_system():
    print("--- AGRI-IOT ORCHESTRATOR STARTING ---")

    # 1. Start the Simulator in the BACKGROUND
    # Popen allows the script to continue without waiting for the simulator to finish
    simulator = subprocess.Popen([sys.executable, "Generator.py"])
    print("Simulator started (PID: {})".format(simulator.pid))

    # 2. Start the Dashboard in the BACKGROUND
    dashboard = subprocess.Popen(["streamlit", "run", "dashboard.py"])
    print(" Dashboard started in your browser.")

    print("\nStarting the Pipeline loop. Press Ctrl+C to shut down everything.\n")

    try:
        while True:
            print("--- ⏱️ Pipeline Triggered: {} ---".format(time.strftime("%H:%M:%S")))
            
            # 3. Run the Pipeline and WAIT for it to finish (run vs Popen)
            # This ensures we don't start a second pipeline before the first one finishes
            subprocess.run([sys.executable, "pipeline.py"])
            
            print("Done. Next update in 30 seconds...")
            time.sleep(8)
            
    except KeyboardInterrupt:
        print("\nShutting down system...")
        
        # 4. Clean up: Kill the background processes
        simulator.terminate()
        dashboard.terminate()
        
        print(" All processes closed. Goodbye!")

if __name__ == "__main__":
    start_system()