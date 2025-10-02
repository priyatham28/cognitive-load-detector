from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI(title="Cognitive Load Detector")

class InferenceRequest(BaseModel):
    audio_feats: Optional[List[float]] = None
    video_feats: Optional[List[float]] = None
    clicks_per_min: Optional[float] = None

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/infer")
def infer(req: InferenceRequest):
    # TODO: load model and fuse features; placeholder score/confidence
    score = 0.42
    conf = 0.77
    return {"load_score": score, "confidence": conf}