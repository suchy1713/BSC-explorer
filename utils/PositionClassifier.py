import pickle
import pandas as pd
import numpy as np
from utils.genetuning import correct_preds
from utils.roles import assign_roles

columns = [
     'right',
     'up',
     'local_right',
     'local_up',
     'angle',
     'hull_top',
     'hull_bottom',
     'centrality',
     'avg_pass_length',
     'avg_pass_angle',
     'avg_receival_angle',
     'def_actions',
     'min_hull_left',
     'min_hull_right',
     'y_deviation',
     'x_deviation',
     'up_defensive',
     'right_defensive'
]

class PositionClassifier():
    def __init__(self, model_path='../model/4_model/brain.xgb'):
        with open(model_path, 'rb') as handle:
            self.model = pickle.load(handle)

    def predict_proba(self, X, verbosity=0, roles=True):
        probas = self.model.predict_proba(X[columns])*100
        preds = self.model.predict(X[columns])
        labels = self.model.classes_
        proba_df = pd.DataFrame(probas, columns=labels).round(2)

        proba_df['name'] = X['name']
        proba_df['id'] = X['id']
        proba_df['x'] = X['x']
        proba_df['y'] = X['y']
        proba_df['position'] = preds
        proba_df['fixed_position'] = preds

        proba_df, score = correct_preds(proba_df, verbosity=verbosity)
        
        if roles:
           proba_df = assign_roles(proba_df)

        return proba_df, score

    def ensemble_predict_proba(self, Xs, coord_df, verbosity=0, roles=True):
        labels = self.model.classes_

        votes = np.zeros((10, len(labels)))
        names = []
        ids = []
        x_s = []
        y_s = []
        correct_idxs = []
        for X, i in zip(Xs, range(0, len(Xs))):
            probas = self.model.predict_proba(X[columns])*100
            preds = np.zeros_like(probas)
            preds[np.arange(0, probas.shape[0]), np.argmax(probas, axis=1)] = 1

            ##TODELETE if you want to use only vote, not proba
            probas = probas/np.sum(probas, axis=1)[:,None]
            #probas[preds == 0] = 0
            preds = probas

            if(len(ids) == 0 and preds.shape[0] < 10):
                continue

            proba_df = pd.DataFrame(preds, columns=labels)
            proba_df['name'] = X['name']
            proba_df['id'] = X['id']
            proba_df['x'] = X['x']
            proba_df['y'] = X['y']
            proba_df = proba_df.sort_values('name')
            if len(names) == 0: names = proba_df['name']
            if len(ids) == 0: ids = proba_df['id']
            

            if list(proba_df['name'].values) == list(names):
                x_s.append(proba_df['x'].values)
                y_s.append(proba_df['y'].values)
                proba_df = proba_df.drop(columns=['name', 'id', 'x', 'y'])
                votes += proba_df.values

        #votes /= len(x_s)
        votes = votes/np.sum(votes, axis=1)[:,None] ##TODELETE if you want to use only vote, not proba
        votes *= 100
            
        preds = labels[np.argmax(votes, axis=1)]

        coord_df = coord_df.sort_values('name')

        proba_df = pd.DataFrame(votes, columns=labels)
        proba_df['name'] = names.values
        proba_df['id'] = ids.values
        proba_df['x'] = coord_df['x'].values
        proba_df['y'] = coord_df['y'].values
        proba_df['position'] = preds
        proba_df['fixed_position'] = preds

        proba_df, score = correct_preds(proba_df, verbosity=verbosity)
        
        if roles:
           proba_df = assign_roles(proba_df)

        return proba_df, score