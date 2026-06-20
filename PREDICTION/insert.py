import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "traffic.db"


def save_prediction(
    grid_id,
    timestamp,
    lat_grid,
    lon_grid,
    traffic_volume,
    number_vehicle,
    type_score,
    violation_score,
    traffic_live_score,
    final_score
):
    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR REPLACE INTO traffic_predictions (
        grid_id,
        timestamp,
        lat_grid,
        lon_grid,
        traffic_volume,
        number_vehicle,
        type_score,
        violation_score,
        traffic_live_score,
        final_score
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        str(grid_id),
        timestamp,
        lat_grid,
        lon_grid,
        traffic_volume,
        number_vehicle,
        type_score,
        violation_score,
        traffic_live_score,
        final_score
    ))

    conn.commit()
    conn.close()
