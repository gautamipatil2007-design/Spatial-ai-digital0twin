
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from data_loader import load_robot_telemetry

app = FastAPI(title="Spatial-AI Digital Twin API")

# Allow the React frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simulated robot data for dashboard demonstration
robots = [
    {
        "id": "AMR-01",
        "x": 18,
        "y": 25,
        "speed": 1.2,
        "temperature": 39.5,
        "status": "Normal",
        "anomaly": False,
        "battery": 87,
        "route": [[18, 25], [30, 25], [30, 40]],
    },
    {
        "id": "AMR-02",
        "x": 72,
        "y": 68,
        "speed": 0.4,
        "temperature": 57.8,
        "status": "Anomaly detected",
        "anomaly": True,
        "battery": 42,
        "route": [[72, 68], [60, 68], [60, 50]],
    },
    {
        "id": "AMR-03",
        "x": 45,
        "y": 80,
        "speed": 1.0,
        "temperature": 36.2,
        "status": "Normal",
        "anomaly": False,
        "battery": 65,
        "route": [[45, 80], [45, 60], [55, 60]],
    },
]


@app.get("/")
def home():
    return {
        "message": "Spatial-AI Digital Twin API is running",
        "docs": "/docs",
    }


@app.get("/api/health")
def health():
    return {"status": "healthy"}


@app.get("/api/robots")
def get_robots():
    return robots


@app.get("/api/summary")
def get_summary():
    return {
        "total_robots": len(robots),
        "active_robots": len(robots),
        "anomalies": sum(1 for robot in robots if robot["anomaly"]),
        "data_source": "simulated_demo_data",
    }


@app.get("/api/telemetry")
def get_telemetry():
    records = load_robot_telemetry()

    return {
        "data_source": "robot_sensor_telemetry.csv",
        "total_records": len(records),
        "telemetry": records,
    }