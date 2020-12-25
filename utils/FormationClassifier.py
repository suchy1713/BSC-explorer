import numpy as np

class FormationClassifier():
    def __init__(self, predictions):
        self.positions = {
            'n_cb': predictions.loc[predictions['fixed_position'].isin(['LCB', 'RCB', 'CB'])].shape[0],
            'n_lb': predictions.loc[predictions['fixed_position'].isin(['LWB', 'LB'])].shape[0],
            'n_rb': predictions.loc[predictions['fixed_position'].isin(['RWB', 'RB'])].shape[0],
            'n_lw': predictions.loc[predictions['fixed_position'].isin(['LW'])].shape[0],
            'n_rw': predictions.loc[predictions['fixed_position'].isin(['RW'])].shape[0],
            'n_dm': predictions.loc[predictions['fixed_position'].isin(['DM', 'LDM', 'RDM'])].shape[0],
            'n_cm': predictions.loc[predictions['fixed_position'].isin(['LCM', 'CM', 'RCM'])].shape[0],
            'n_am': predictions.loc[predictions['fixed_position'].isin(['AM', 'LAM', 'RAM'])].shape[0],
            'n_st': predictions.loc[predictions['fixed_position'].isin(['LST', 'RST', 'ST'])].shape[0],
        }

    def get_vector(self):
        return list(self.positions.values())

    def get_label(self):
        n_players = []

        #defenders
        n_players.append(self.positions['n_cb'] + 2)

        #3 or 4 lines?
        if self.positions['n_am'] > 0:
            n_players.append(self.positions['n_cm'] + self.positions['n_dm'])
            n_players.append(self.positions['n_am'] + self.positions['n_lw'] + self.positions['n_rw'])
            n_players.append(self.positions['n_st'])
        else:
            n_mid = self.positions['n_cm'] + self.positions['n_dm']

            if n_mid >= 4:
                n_players.append('diamond')
            else:
                n_players.append(n_mid)
            n_players.append(self.positions['n_st'] + self.positions['n_lw'] + self.positions['n_rw'])

        n_players = np.array(n_players).astype(str)

        label = '-'.join(n_players)

        #disgusting, get rid of this asap
        if label == '4-2-4':
            label = '4-4-2'

        return label