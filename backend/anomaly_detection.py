from typing import Optional, Dict, Any
from datetime import datetime
from models import AnomalyAlert

class AnomalyDetector:
    def __init__(
        self,
        temp_threshold: float = 65.0,
        vibration_threshold: float = 0.45,
        min_battery: float = 15.0
    ):
        self.temp_threshold = temp_threshold
        self.vibration_threshold = vibration_threshold
        self.min_battery = min_battery

    def evaluate_telemetry(self, telemetry: Dict[str, Any]) -> Optional[AnomalyAlert]:
        robot_id = telemetry.get("robot_id", "Unknown")
        ts = telemetry.get("timestamp", datetime.utcnow())
        if isinstance(ts, str):
            try:
                ts = datetime.fromisoformat(ts)
            except ValueError:
                ts = datetime.utcnow()

        temp = float(telemetry.get("temperature", 0))
        vib = float(telemetry.get("vibration", 0))
        battery = float(telemetry.get("battery", 100))

        if temp > self.temp_threshold:
            return AnomalyAlert(
                robot_id=robot_id,
                timestamp=ts,
                metric="temperature",
                value=temp,
                threshold=self.temp_threshold,
                severity="critical" if temp > 75.0 else "warning",
                message=f"Motor overheating detected: {temp:.1f}°C"
            )

        if vib > self.vibration_threshold:
            return AnomalyAlert(
                robot_id=robot_id,
                timestamp=ts,
                metric="vibration",
                value=vib,
                threshold=self.vibration_threshold,
                severity="critical",
                message=f"Abnormal vibration spike: {vib:.3f}g"
            )

        if battery < self.min_battery:
            return AnomalyAlert(
                robot_id=robot_id,
                timestamp=ts,
                metric="battery",
                value=battery,
                threshold=self.min_battery,
                severity="warning",
                message=f"Critical battery depletion: {battery:.1f}%"
            )

        return None
