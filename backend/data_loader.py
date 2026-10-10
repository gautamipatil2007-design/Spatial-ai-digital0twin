import os
import glob
import pandas as pd
from datetime import datetime
from typing import Generator, Dict, Any, List

DATA_DIR = os.path.join(os.path.dirname(__file__), "Data")

class TelemetryDataLoader:
    def __init__(self, data_dir: str = DATA_DIR):
        self.data_dir = data_dir
        self.dataset_files = sorted(glob.glob(os.path.join(self.data_dir, "*.csv")))
        self.cached_data: List[Dict[str, Any]] = []
        self._load_all_records()

    def _load_all_records(self):
        records = []
        for file_path in self.dataset_files:
            try:
                df = pd.read_csv(file_path)
                # Normalize column headers
                df.columns = [col.strip().lower() for col in df.columns]

                # Identify robot identifier or assign default
                robot_id = os.path.basename(file_path).split(".")[0]

                for _, row in df.iterrows():
                    record = {
                        "robot_id": str(row.get("robot_id", robot_id)),
                        "timestamp": row.get("timestamp", datetime.utcnow().isoformat()),
                        "x": float(row.get("x", row.get("pos_x", 5.0))),
                        "y": float(row.get("y", row.get("pos_y", 5.0))),
                        "speed": float(row.get("speed", row.get("velocity", 1.2))),
                        "battery": float(row.get("battery", row.get("soc", 95.0))),
                        "temperature": float(row.get("temperature", row.get("temp", 36.5))),
                        "vibration": float(row.get("vibration", row.get("vib", 0.05))),
                        "status": str(row.get("status", "active")),
                    }
                    records.append(record)
            except Exception as e:
                print(f"Error loading {file_path}: {e}")

        # Fallback fixtures if CSV directory is empty
        if not records:
            for i in range(1, 4):
                records.append({
                    "robot_id": f"AGV-{i:02d}",
                    "timestamp": datetime.utcnow().isoformat(),
                    "x": float(10 * i),
                    "y": float(8 * i),
                    "speed": 1.5,
                    "battery": 88.0,
                    "temperature": 38.0,
                    "vibration": 0.03,
                    "status": "active"
                })

        self.cached_data = records

    def stream_telemetry(self) -> Generator[Dict[str, Any], None, None]:
        """Cycles infinitely over cached telemetry to emulate live edge feeds."""
        while True:
            for record in self.cached_data:
                yield {
                    **record,
                    "timestamp": datetime.utcnow().isoformat()
                }

    def get_latest_fleet_state(self) -> List[Dict[str, Any]]:
        latest = {}
        for rec in self.cached_data:
            latest[rec["robot_id"]] = rec
        return list(latest.values())
