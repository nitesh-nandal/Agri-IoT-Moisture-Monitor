# Agri-IoT Soil Moisture Pipeline

A simulated end-to-end IoT data pipeline for agricultural soil moisture monitoring. It generates noisy sensor data, cleans it, stores it in a SQLite database, and visualizes it in a real-time Streamlit dashboard.

## Architecture

```
Generator.py  →  raw_sensor_data.csv  →  pipeline.py  →  Farm_data.db  →  dashboard.py
     ↑                                                                          ↑
 (simulates                                                              (Streamlit UI)
  IoT sensor)
       └─────────────────── orchestrator.py (coordinates all) ──────────────────┘
```

## Files

| File | Description |
|------|-------------|
| `Generator.py` | Simulates a soil moisture sensor (sensor ID 101), writing one reading per second to `raw_sensor_data.csv`. Intentionally injects ~10% missing values and ~5% outliers (999.0) to mimic real-world sensor faults. |
| `pipeline.py` | Reads the raw CSV, detects and cleans faults (replaces outliers with NaN, fills gaps via linear interpolation), then upserts clean records into `Farm_data.db` using an `INSERT OR IGNORE` strategy to prevent duplicates. |
| `dashboard.py` | Streamlit app that reads from `Farm_data.db` and displays total readings, average moisture, a time-series line chart, and the 10 most recent rows. Includes a manual refresh button. |
| `orchestrator.py` | Entry point. Launches `Generator.py` and `dashboard.py` as background processes, then runs `pipeline.py` in a loop every 8 seconds. Cleanly terminates all processes on `Ctrl+C`. |
| `check_db.py` | Quick utility to print all rows and the total row count from `Farm_data.db`. |

## Setup

```bash
# Create and activate a virtual environment
python3 -m venv myenv
source myenv/bin/activate

# Install dependencies
pip install pandas numpy streamlit
```

## Usage

Run everything with a single command:

```bash
python orchestrator.py
```

This will:
1. Start the sensor simulator in the background
2. Open the Streamlit dashboard in your browser
3. Run the cleaning pipeline every 8 seconds

Press `Ctrl+C` to stop all processes.

To run components individually:

```bash
# Simulate sensor data only
python Generator.py

# Run the cleaning pipeline once
python pipeline.py

# Launch the dashboard only
streamlit run dashboard.py

# Inspect the database
python check_db.py
```

## Data Flow

1. **Generator** writes one row per second to `raw_sensor_data.csv` with fields: `sensor_id`, `timestamp`, `moisture_level`
2. **Pipeline** loads the CSV, flags nulls and 999.0 outliers, interpolates missing values linearly, and writes clean rows to the `sensor_data` table in `Farm_data.db`
3. **Dashboard** queries the database and renders live metrics and charts

## Database Schema

```sql
CREATE TABLE sensor_data (
    sensor_id     INTEGER,
    timestamp     DATETIME,
    moisture_level FLOAT,
    PRIMARY KEY (sensor_id, timestamp)
);
```

## Dependencies

- Python 3.12+
- pandas
- numpy
- streamlit
- sqlite3 (standard library)
