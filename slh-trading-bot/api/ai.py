from fastapi import APIRouter
import joblib, os

router = APIRouter(prefix="/api/ai", tags=["ai"])

@router.get("/status")
def ai_status():
    model_path = "ai_models/xgb_classifier.pkl"
    if os.path.exists(model_path):
        model = joblib.load(model_path)
        return {"model": "XGBoost", "loaded": True, "type": str(type(model).__name__)}
    return {"model": "none", "loaded": False}

@router.get("/confidence")
def ai_confidence():
    # In future, return live confidence from filter
    return {"confidence": None, "message": "Not available in current mode"}

@router.get("/rejections")
def ai_rejections():
    return {"rejections": 0}
