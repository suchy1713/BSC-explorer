import numpy as np
import pandas as pd
import random
import warnings
warnings.simplefilter(action='ignore')

mutations = {
    'CB': ['CM', 'LB', 'RB'],
    'CM': ['CB', 'LB', 'RB', 'LW', 'RW', 'ST'],
    'LB': ['CB', 'LW', 'CM'],
    'RB': ['CB', 'RW', 'CM'],
    'LW': ['LB', 'ST', 'CM'],
    'RW': ['RB', 'ST', 'CM'],
    'ST': ['LW', 'RW', 'CM']
}

positions = ['CB', 'CM', 'LB', 'RB', 'LW', 'RW', 'ST']
ps = [0.25, 0.25, 0.1, 0.1, 0.075, 0.075, 0.15]

population_size_init = 50
n_generations = 2000

#PUT IT TOGETHER
pen = -500
low_pen = -70

def adaptive_scaling(probas, i):
    lower_p = np.percentile(probas, 50)
    upper_p = np.percentile(probas, 50)

    if i < 150:
        probas[(probas > upper_p) & (probas != 1)] = probas[(probas > upper_p) & (probas != 1)]*0.7
        probas[probas < lower_p] = probas[probas < lower_p]*1.42
    elif i > 300:
        probas[(probas > upper_p) & (probas != 1)] = probas[(probas > upper_p) & (probas != 1)]*1.17
        probas[probas < lower_p] = probas[probas < lower_p]*0.85

    return probas

def random_mix(X, Y):
    choice = np.random.randint(2, size = X.size).reshape(X.shape).astype(bool)
    return np.where(choice, X, Y)

def select(proba):
    return random.random() < proba

#TODO optimize
def mutate(assignment, i):
    for i in range(0, len(assignment)):
        if i < 300:
            if random.random() < 0.065:
                assignment[i] = np.random.choice(positions, 1)[0]
        if i > 300:
            if random.random() < 0.9:
                assignment[i] = np.random.choice(mutations[assignment[i]], 1)[0]

    return assignment

def fitness(proba_df, assignment, use_absolute=True):
    unique, counts = np.unique(assignment, return_counts=True)
    n_pos = dict(zip(unique, counts))

    if not 'LB' in unique:
        n_pos['LB'] = 0
    if not 'RB' in unique:
        n_pos['RB'] = 0
    if not 'CB' in unique:
        n_pos['CB'] = 0
    if not 'LW' in unique:
        n_pos['LW'] = 0
    if not 'RW' in unique:
        n_pos['RW'] = 0
    if not 'CM' in unique:
        n_pos['CM'] = 0
    if not 'ST' in unique:
        n_pos['ST'] = 0


    score = 0
    st_scores = []
    cm_scores = []
    cb_scores = []
    w_scores = []
    for i, row in proba_df.iterrows():
        score += row[assignment[i]]

        if assignment[i] == 'ST':
            st_scores.append(row[assignment[i]])

        if assignment[i] == 'CM':
            cm_scores.append(row[assignment[i]])

        if assignment[i] == 'CB':
            cb_scores.append(row[assignment[i]])

        if assignment[i] in ['LW', 'RW']:
            w_scores.append(row[assignment[i]])

            if row['CB'] > row[assignment[i]]*0.85:
                score += pen

        #penalize very improbable assignments
        min_pen, max_pen = 200, 500
        threshold = 5
        if row[assignment[i]] < threshold:
            score -= max_pen# - ((row[assignment[i]]-0)/((threshold-0)/(max_pen-min_pen)) + min_pen) +min_pen

    if len(st_scores) == 2:
        maxi = np.max(st_scores)
        mini = np.min(st_scores)

        if (maxi-mini) > maxi*0.45 and mini < 50:
           score += low_pen

    if len(cm_scores) == 4:
        cm_scores = np.array(cm_scores)
        mini = np.min(cm_scores)
        maxis = cm_scores[cm_scores != mini]
        maxi = np.mean(maxis)

        if (maxi-mini) > maxi*0.35 and mini < 50:
            score += low_pen

    if len(cm_scores) == 3:
        cm_scores = np.array(cm_scores)
        mini = np.min(cm_scores)
        maxis = cm_scores[cm_scores != mini]
        maxi = np.mean(maxis)

        if (maxi-mini) > maxi*0.65 and mini < 50:
            score += low_pen

    if len(cb_scores) == 3:
        cb_scores = np.array(cb_scores)
        mini = np.min(cb_scores)
        maxis = cb_scores[cb_scores != mini]
        maxi = np.mean(maxis)

        if (maxi-mini) > maxi*0.8 and mini < 50:
            score += low_pen

    if len(w_scores) == 2:
        maxi = np.max(w_scores)
        mini = np.min(w_scores)

        if (maxi-mini) > maxi*0.55 and mini < 50:
           score += low_pen

    if n_pos['LB'] == 0:
        score += pen
    if n_pos['RB'] == 0:
        score += pen
    if (n_pos['LW'] > 0 and n_pos['RW'] == 0) or (n_pos['LW'] == 0 and n_pos['RW'] > 0):
        score += pen
    if n_pos['LB'] > 1:
        score += pen
    if n_pos['RB'] > 1:
        score += pen
    if n_pos['LW'] > 1:
        score += pen
    if n_pos['RW'] > 1:
        score += pen
    if n_pos['CB'] > 3:
        score += pen
    if n_pos['CM'] > 4:
        score += pen
    if n_pos['CM'] < 2:
        score += pen
    if n_pos['ST'] > 2:
        score += pen
    if n_pos['ST'] < 1:
        score += pen
    if n_pos['CB'] <= 1:
        score += pen

    return score


#CREATE THE INITIAL POPULATION
def correct_preds(proba_df, verbosity=1, use_absolute=True):
    population = []
    for i in range(0, population_size_init):
        #population.append(proba_df['position'].values)
        population.append(np.random.choice(positions, proba_df.shape[0]))
    population = np.array(population)

    scoring_times = []
    other_times = []

    max_score = -np.inf
    max_score_iter = 0
    best_ass = []
    for i in range(0, n_generations+1):
        #SELECTION
        #scores = np.apply_along_axis(lambda x: fitness(proba_df, x, use_absolute), 1, population)
        scores = np.fromiter((fitness(proba_df, x, use_absolute) for x in population), dtype=float, count=len(population))

        if i%100 == 0 and i != 0 and verbosity:
            print(f'Generation {i}/{n_generations} \t Max Score: {np.round(max_score, 2)} \t Max Score Iter: {max_score_iter}')

        if scores.max() > max_score:
            max_score = scores.max()
            best_ass = population[scores.argmax()]
            max_score_iter = i

        proba_df['fixed_position'] = best_ass

        if i == n_generations:
            break

        if i-max_score_iter > 400:
            break
        
        if max(scores)-min(scores) != 0:
            n_scores = (scores - min(scores))/(max(scores)-min(scores))
            proba_of_selection = n_scores
            proba_of_selection = adaptive_scaling(n_scores, i)
        else:
            proba_of_selection = np.full_like(scores, 0.5)

        v_select = np.vectorize(select)
        selected = v_select(proba_of_selection)
        population = population[selected]

        #CROSSOVER
        children = []
        for _ in range(0, population_size_init-population.shape[0]):
            parents_idx = np.random.randint(population.shape[0], size=2)
            parents = population[parents_idx, :]

            child = random_mix(parents[0], parents[1])
            children.append(child)

        children = np.array(children)
        population = np.concatenate((population, children))

        #MUTATION
        population = np.apply_along_axis(lambda x: mutate(x, i), 1, population)   

    #RESULTS
    if verbosity:
        print(f'n_iter: {i}, score: {max_score}\n\n')
    # else:
    #     print(np.round(max_score, 0))

    # if roles:
    #     proba_df = assign_roles(proba_df)

    return proba_df, np.round(max_score, 0)