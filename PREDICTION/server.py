from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3
import pandas as pd
import os

app = Flask(__name__)

# CORS: in production, restrict to the deployed frontend origin via FRONTEND_ORIGIN env var.
# Falls back to allowing all origins for local/dev use.
frontend_origin = os.environ.get("FRONTEND_ORIGIN")
if frontend_origin:
    CORS(app, origins=[frontend_origin])
else:
    CORS(app)

@app.route("/traffic")
def traffic():

    conn = sqlite3.connect("traffic.db")

    df = pd.read_sql(
        "SELECT * FROM traffic_predictions",
        conn
    )

    conn.close()

    return jsonify(
        df.to_dict(orient="records")
    )

if __name__ == "__main__":
    debug_mode = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=debug_mode
    )
