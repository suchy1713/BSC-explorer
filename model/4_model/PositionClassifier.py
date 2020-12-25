import numpy as np
from sklearn.base import BaseEstimator
import xgboost
import sys
sys.path.append('../../')
from utils.model import get_positions

class PositionClassifier(BaseEstimator):
    def __init__(self):
        self.brain = xgboost.XGBClassifier(
            objective='multi:softmax',
            colsample_bytree=0.5,
            learning_rate=0.01,
            max_depth=6,
            subsample=0.5,
            min_child_weight=1,
            n_estimators=450
        )

    def fit(self, X, y):
        self.brain.fit(X, y)

    def predict(self, X):
        n = 10 
        list_df = [X[i:i+n] for i in range(0, X.shape[0], n)]

        results = []
        for game in list_df:
            proba_df = get_positions(self.brain, game, verbosity=1, roles=False, only_predict=True)
            results.append(proba_df)

        return np.concatenate(results)