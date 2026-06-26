from pydantic import BaseModel
from typing import List, Dict

class ComposeRequest(BaseModel):
    assets: List[Dict] = []
    composition_spec: dict
    output_format: str = "mp4"
    correlation_id: str

class ComposeCompleted(BaseModel):
    asset_id: str
    storage_url: str
    duration_seconds: float
    format: str
    cost_usd: float
    correlation_id: str
