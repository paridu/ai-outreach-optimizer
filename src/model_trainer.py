"""
AGENT: ML Engineer
MISSION: Train Recommendation Models for Personalized Content
DESCRIPTION: Hybrid Matrix Factorization model training pipeline using LightFM.
             Integrates with the Customer Interaction schema for real-time marketing.
"""

import os
import yaml
import logging
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from lightfm import LightFM
from lightfm.data import Dataset
from lightfm.evaluation import precision_at_k, auc_score
import joblib

# Logging Configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RecommendationTrainer:
    def __init__(self, config_path='config/model_params.yaml'):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.db_engine = create_engine(os.getenv('DATABASE_URL', 'postgresql://user:pass@localhost:5432/personalization_db'))
        self.model = None
        self.dataset = Dataset()

    def fetch_data(self):
        """Fetches interaction data based on the defined SQL schema."""
        query = """
            SELECT customer_id, event_type, 
                   (payload->>'item_id') as item_id,
                   CASE 
                       WHEN event_type = 'purchase' THEN 5
                       WHEN event_type = 'click' THEN 2
                       WHEN event_type = 'view' THEN 1
                       ELSE 0 
                   END as weight
            FROM event_logs
            WHERE timestamp > NOW() - INTERVAL '30 days'
        """
        logger.info("Fetching interaction data from database...")
        return pd.read_sql(query, self.db_engine)

    def prepare_dataset(self, df):
        """Maps interactions to LightFM dataset format."""
        logger.info("Building LightFM dataset and mapping...")
        self.dataset.fit(
            users=df['customer_id'].unique(),
            items=df['item_id'].unique()
        )
        
        (interactions, weights) = self.dataset.build_interactions(
            ((x['customer_id'], x['item_id'], x['weight']) for index, x in df.iterrows())
        )
        return interactions, weights

    def train(self, interactions, weights):
        """Trains a Hybrid Matrix Factorization model (WARP loss)."""
        logger.info(f"Training model with {self.config['model']['no_components']} components...")
        self.model = LightFM(
            no_components=self.config['model']['no_components'],
            loss=self.config['model']['loss'],
            learning_rate=self.config['model']['learning_rate'],
            random_state=42
        )
        
        self.model.fit(
            interactions,
            sample_weight=weights,
            epochs=self.config['model']['epochs'],
            num_threads=self.config['model']['threads']
        )
        return self.model

    def evaluate(self, interactions):
        """Evaluates model performance using Precision@K and AUC."""
        logger.info("Evaluating model...")
        p_at_k = precision_at_k(self.model, interactions, k=5).mean()
        auc = auc_score(self.model, interactions).mean()
        logger.info(f"Precision@5: {p_at_k:.4f}")
        logger.info(f"AUC Score: {auc:.4f}")
        return {"precision_at_5": p_at_k, "auc": auc}

    def save_artifacts(self, output_dir='models/'):
        """Saves the model and the mapping for real-time inference."""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        timestamp = pd.Timestamp.now().strftime('%Y%m%d_%H%M')
        joblib.dump(self.model, f"{output_dir}rec_model_{timestamp}.joblib")
        joblib.dump(self.dataset, f"{output_dir}dataset_mapping_{timestamp}.joblib")
        logger.info(f"Model artifacts saved to {output_dir}")

if __name__ == "__main__":
    # Note: In a production CI/CD environment, DATABASE_URL would be injected.
    # This script follows the Strategic Vision of Real-Time Personalization.
    trainer = RecommendationTrainer()
    data = trainer.fetch_data()
    if not data.empty:
        interactions, weights = trainer.prepare_dataset(data)
        trainer.train(interactions, weights)
        trainer.evaluate(interactions)
        trainer.save_artifacts()
    else:
        logger.warning("No data found for training.")