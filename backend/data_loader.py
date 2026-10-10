
from pathlib import Path
import pandas as pd

# Project root is the parent of the backend folder.
from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent / "Data"


def inspect_csv_files():
    results = []

    if not DATA_DIR.exists():
        raise FileNotFoundError(f"Data folder not found: {DATA_DIR}")

    csv_files = sorted(DATA_DIR.glob("*.csv"))

    for file_path in csv_files:
        try:
            df = pd.read_csv(file_path)

            results.append({
                "filename": file_path.name,
                "rows": len(df),
                "columns": df.columns.tolist(),
                "preview": df.head(3).fillna("").to_dict(
                    orient="records"
                ),
                "status": "loaded",
            })

        except Exception as exc:
            results.append({
                "filename": file_path.name,
                "status": f"error: {exc}",
            })

    return results


if __name__ == "__main__":
    for result in inspect_csv_files():
        print(f"\nFile: {result['filename']}")
        print(f"Status: {result['status']}")

        if result["status"] == "loaded":
            print(f"Rows: {result['rows']}")
            print(f"Columns: {result['columns']}")
            print("Preview:")
            print(pd.DataFrame(result["preview"]).to_string(index=False))
            
from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent / "Data"

def load_robot_telemetry():
    file_path = DATA_DIR / "robot_sensor_telemetry.csv"

    if not file_path.exists():
        raise FileNotFoundError(f"Dataset not found: {file_path}")

    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()

    return df.fillna("").to_dict(orient="records")