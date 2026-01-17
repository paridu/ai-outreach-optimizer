export interface Customer {
  id: string;
  name: string;
  segment: 'VIP' | 'Churn-Risk' | 'New-User' | 'Loyalist';
  affinityScore: number;
  lastInteraction: string;
  topInterests: string[];
}

export interface Campaign {
  id: string;
  name: string;
  status: 'active' | 'paused' | 'draft';
  triggerType: 'event_driven' | 'scheduled';
  performance: {
    conversionRate: number;
    clicks: number;
    impressions: number;
  };
}

export interface RealTimeEvent {
  id: string;
  customerId: string;
  eventType: string;
  timestamp: string;
  priority: 'low' | 'medium' | 'high' | 'critical';
}