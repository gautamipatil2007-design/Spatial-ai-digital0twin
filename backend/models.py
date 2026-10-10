from pydantic import BaseModel, Field
from typing import List, Tuple, Optional
from datetime import datetime

class TelemetryData(BaseModel):
    robot_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    x: float
    y: float
    speed: float = 0.0
    battery: float = 100.0
    temperature: float = 35.0
    vibration: float = 0.02
    status: str = "active"  # "active", "idle", "charging", "maintenance"

class AnomalyAlert(BaseModel):
    robot_id: str
    timestamp: datetime
    metric: str
    value: float
    threshold: float
    severity: str  # "warning", "critical"
    message: str

class RouteRequest(BaseModel):
    robot_id: str
    start: Tuple[int, int]
    destination: Tuple[int, int]

class RouteResponse(BaseModel):
    robot_id: str
    path: List[Tuple[int, int]]
    distance: int

class WarehouseLayout(BaseModel):
    width: int = 50
    height: int = 50
    obstacles: List[Tuple[int, int]] = []
    charging_stations: List[Tuple[int, int]] = []
