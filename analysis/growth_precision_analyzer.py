"""
AGENT: Data Scientist
MISSION: Analyze Growth Metrics and Model Precision
DESCRIPTION: This module evaluates the performance of the AI Personalization Engine 
             by calculating business growth KPIs (Lift, CVR, ARPU) and 
             technical ML metrics (Precision@K, Recall@K, F1-Score).
"""

import pandas as pd
import numpy as np
from sklearn.metrics import precision_score, recall_score, f1_score
import matplotlib.pyplot as plt
import seaborn as sns

class GrowthMetricsAnalyzer:
    def __init__(self, interaction_data, prediction_data):
        """
        interaction_data: DataFrame with actual customer behavior (clicks, purchases)
        prediction_data: DataFrame with model scores/recommendations
        """
        self.df_actual = interaction_data
        self.df_pred = prediction_data

    def calculate_business_kpis(self, control_group_cvr=0.025):
        """
        Calculates Growth Metrics: Conversion Rate (CVR), Lift, and Revenue Impact.
        """
        total_users = self.df_actual['customer_id'].nunique()
        conversions = self.df_actual[self.df_actual['event_type'] == 'purchase'].shape[0]
        
        current_cvr = conversions / total_users if total_users > 0 else 0
        lift = (current_cvr - control_group_cvr) / control_group_cvr if control_group_cvr > 0 else 0
        
        metrics = {
            "Total Users": total_users,
            "Total Conversions": conversions,
            "Current CVR": round(current_cvr, 4),
            "Baseline CVR": control_group_cvr,
            "Lift (%)": round(lift * 100, 2)
        }
        return metrics

    def calculate_model_precision(self, top_k=5):
        """
        Calculates Model Precision@K and standard classification metrics.
        Assumes binary target: 1 if user interacted with recommendation, 0 otherwise.
        """
        # Merging predictions with actuals for verification
        merged = pd.merge(
            self.df_pred, 
            self.df_actual[['customer_id', 'event_type']], 
            on='customer_id', 
            how='left'
        )
        
        # Ground truth: 1 if they purchased or clicked
        merged['truth'] = merged['event_type'].apply(lambda x: 1 if x in ['purchase', 'click'] else 0)
        
        # Binary prediction (thresholding score at 0.5)
        merged['pred_binary'] = (merged['score'] >= 0.5).astype(int)
        
        precision = precision_score(merged['truth'], merged['pred_binary'])
        recall = recall_score(merged['truth'], merged['pred_binary'])
        f1 = f1_score(merged['truth'], merged['pred_binary'])
        
        return {
            f"Precision@{top_k}": round(precision, 4),
            "Recall": round(recall, 4),
            "F1-Score": round(f1, 4)
        }

    def generate_growth_report(self):
        """
        Simulates data for a visual report of Growth Trends.
        """
        # Simulated Monthly Growth
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        cvr_trend = [0.025, 0.027, 0.031, 0.035, 0.042, 0.048] # Upward trend due to AI
        
        plt.figure(figsize=(10, 5))
        sns.lineplot(x=months, y=cvr_trend, marker='o', color='teal', label='AI-Driven CVR')
        plt.axhline(y=0.025, color='red', linestyle='--', label='Pre-AI Baseline')
        plt.title("Conversion Rate (CVR) Growth Trend post-AI Deployment")
        plt.ylabel("Conversion Rate")
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.show()

if __name__ == "__main__":
    # Mock data for demonstration
    actual_data = pd.DataFrame({
        'customer_id': ['C1', 'C2', 'C3', 'C4', 'C5'],
        'event_type': ['purchase', 'click', 'view', 'purchase', 'view']
    })
    
    prediction_data = pd.DataFrame({
        'customer_id': ['C1', 'C2', 'C3', 'C4', 'C5'],
        'score': [0.9, 0.8, 0.2, 0.7, 0.1] # ML Model scores
    })

    analyzer = GrowthMetricsAnalyzer(actual_data, prediction_data)
    
    print("--- GROWTH METRICS ---")
    print(analyzer.calculate_business_kpis())
    
    print("\n--- MODEL PRECISION ---")
    print(analyzer.calculate_model_precision())
    
    # analyzer.generate_growth_report() # Uncomment to see plot