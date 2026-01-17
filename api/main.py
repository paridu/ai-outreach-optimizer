from fastapi import FastAPI, HTTPException, BackgroundTasks
from .models.trigger_models import MarketingEvent, TriggerExecutionResponse
from .services.execution_engine import TriggerExecutionEngine
import uvicorn

app = FastAPI(
    title="Instant Marketing Trigger API",
    description="Real-time API to execute AI-driven marketing actions based on customer events.",
    version="1.0.0"
)

engine = TriggerExecutionEngine()

@app.post("/api/v1/trigger/execute", response_model=TriggerExecutionResponse)
async def execute_trigger(event: MarketingEvent):
    """
    Receives a real-time event and immediately evaluates marketing triggers.
    """
    try:
        result = await engine.evaluate_and_execute(event.model_dump())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/trigger/async-event")
async def process_event_async(event: MarketingEvent, background_tasks: background_tasks):
    """
    Endpoint for high-throughput ingestion where response time is critical.
    Processing happens in the background.
    """
    background_tasks.add_task(engine.evaluate_and_execute, event.model_dump())
    return {"status": "accepted", "event_id": event.event_id}

@app.get("/health")
async def health_check():
    return {"status": "online", "engine": "active"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)