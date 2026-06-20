import sqlite3

conn = sqlite3.connect("traffic.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS traffic_predictions (
    grid_id TEXT PRIMARY KEY,
    timestamp TEXT,
    lat_grid REAL,
    lon_grid REAL,
    traffic_volume REAL,
    number_vehicle REAL,
    type_score REAL,
    violation_score REAL,
    traffic_live_score REAL,
    final_score REAL
)
""")

conn.commit()
conn.close()

print("Database ready")