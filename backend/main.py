import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from models import RouteRequest, RouteResponse, WarehouseLayout, AnomalyAlert
from data_loader import TelemetryDataLoader
from anomaly_detection import AnomalyDetector
from routing import WarehouseRouter

app = FastAPI(title="Spatial AI Digital Twin Backend", version="1.0.0")

# Enable CORS for React frontend (Vite defaults to 5173, CRA to 3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

data_loader = TelemetryDataLoader()
anomaly_detector = AnomalyDetector()

# Standard layout definition
warehouse_obstacles = {(x, y) for x in range(10, 15) for y in range(10, 30)}
warehouse_charging = [(2, 2), (2, 48), (48, 2)]
router = WarehouseRouter(width=50, height=50, obstacles=warehouse_obstacles)

recent_anomalies: List[AnomalyAlert] = []

@app.get("/api/health")
def health_check():
    return {"status": "operational", "data_sources": len(data_loader.dataset_files)}

@app.get("/api/robots")
def get_robots():
    """Supplies RobotCard.jsx with current fleet positions and metrics."""
    return data_loader.get_latest_fleet_state()

@app.get("/api/warehouse/map", response_model=WarehouseLayout)
def get_warehouse_layout():
    """Supplies WarehouseMap.jsx with grid obstacles and docks."""
    return WarehouseLayout(
        width=50,
        height=50,
        obstacles=list(warehouse_obstacles),
        charging_stations=warehouse_charging
    )

@app.get("/api/anomalies/recent", response_model=List[AnomalyAlert])
def get_recent_anomalies():
    """Supplies AnomalyAlerts.jsx with identified faults."""
    return recent_anomalies[-20:]

@app.post("/api/routes/calculate", response_model=RouteResponse)
def compute_route(req: RouteRequest):
    """Calculates A* waypoint paths for robots."""
    path = router.find_path(req.start, req.destination)
    return RouteResponse(
        robot_id=req.robot_id,
        path=path,
        distance=len(path)
    )

@app.websocket("/ws/telemetry")
async def websocket_telemetry_stream(websocket: WebSocket):
    """Streams active telemetry and evaluated alerts to the frontend map/cards."""
    await websocket.accept()
    stream = data_loader.stream_telemetry()
    try:
        while True:
            frame = next(stream)
            alert = anomaly_detector.evaluate_telemetry(frame)
            if alert:
                recent_anomalies.append(alert)

            payload = {
                "telemetry": frame,
                "alert": alert.dict() if alert else None
            }
            await websocket.send_json(payload)
            await asyncio.sleep(0.5)  # 2 Hz broadcast rate
    except WebSocketDisconnect:
        pass
    except Exception as e:
        print(f"WebSocket closed: {e}")
