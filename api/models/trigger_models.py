from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from uuid import UUID, uuid4
from datetime import datetime

class MarketingEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid4()))
    customer_id: str
    event_type: str  # e.g., "cart_abandoned", "price_drop_interest", "location_entry"
    platform: str
    metadata: Dict[str, Any] = {}
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class TriggerExecutionResponse(BaseModel):
    execution_id: UUID
    status: str
    action_taken: str
    target_channel: str
    personalized_content: Optional[str] = None
    timestamp: datetime