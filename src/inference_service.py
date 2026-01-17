"""
AGENT: ML Engineer
DESCRIPTION: Real-time inference bridge to serve recommendations 
             via the Decisioning Engine.
"""
import joblib
import numpy as np

class RecommenderService:
    def __init__(self, model_path, dataset_path):
        self.model = joblib.load(model_path)
        self.dataset = joblib.load(dataset_path)
        self.user_dict = self.dataset.mapping()[0]
        self.item_dict = {v: k for k, v in self.dataset.mapping()[2].items()}

    def get_recommendations(self, customer_id, n_recs=5):
        try:
            user_idx = self.user_dict[customer_id]
            n_items = len(self.item_dict)
            
            # Predict scores for all items for the specific user
            scores = self.model.predict(user_idx, np.arange(n_items))
            top_items_idx = np.argsort(-scores)[:n_recs]
            
            return [self.item_dict[i] for i in top_items_idx]
        except KeyError:
            # Cold start fallback: return popular items or empty
            return []

# Usage example for Real-Time Decisioning Engine
# service = RecommenderService('models/rec_model_latest.joblib', 'models/dataset_mapping_latest.joblib')
# print(service.get_recommendations('cust_999'))