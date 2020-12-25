from datetime import datetime

def name_short(arr):
    return f'{arr[0][0]}. {arr[-1]}'

def split(arr):
    return list(map(lambda x: name_short(x.split(' ')), arr))

def coach_label(coaches, options_coaches):
    if len(coaches) == len(options_coaches):
        return ''
    else:
        text = ', '.join(split(coaches))
        return f'Coaches: {text}' if len(coaches) > 1 else f'Coach: {text}'

def include_label(include, options):
    if len(include) == 0:
        return '' 
    names = [x['label'] for x in options if x['value'] in include]
    text = ', '.join(split(names))
    return f'With: {text}'

def exclude_label(exclude, options):
    if len(exclude) == 0:
        return ''
    names = [x['label'] for x in options if x['value'] in exclude]
    text = ', '.join(split(names))
    return f'Without: {text}'

def get_short(name):
    splitted = name.replace('-',' ').replace(' & ',' ').split(' ')

    if len(splitted) == 1:
        return splitted[0][:3]
        
    elif len(splitted) == 2:
        return f'{splitted[0][0]}{splitted[1][:2]}'
        
    else:
        return f'{splitted[0][0]}{splitted[1][0]}{splitted[2][0]}'

def opposition(opp, options):
    if len(opp) == len(options):
        return ''
    names = [x['label'] for x in options if x['value'] in opp]
    text = ', '.join(list(map(lambda x: get_short(x), names)))

    return f'vs {text}'

def possession(vals, min, max):
    if vals[0] == min and vals[1] == max:
        return ''

    if vals[0] != min and vals[1] != max:
        return f'Possession: {vals[0]}%-{vals[1]}%'

    if vals[0] != min:
        return f'Possession: >{vals[0]}%'

    if vals[1] != max:
        return f'Possession: <{vals[1]}%'

def opposition_forma(opp_forma, options):
    if len(opp_forma) == len(options):
        return ''

    names = [x['label'].replace('-', '') for x in options if x['value'] in opp_forma]
    text = ', '.join(names)

    return f'vs {text}'

def sanitize(input):
    if len(input) > 10:
        return input[:10]
    return input

def date_label(first, last, mini, maxi):
    first = sanitize(first)
    last = sanitize(last)
    mini = sanitize(mini)
    maxi = sanitize(maxi)

    if first == mini and last == maxi:
        return ''
    elif first == mini and last != maxi:
        return f'Before {last}'
    elif first != mini and last == maxi:
         return f'After {first}'
    else:
        return f'{first} - {last}'

def get_filters_label(coaches, 
                      options_coaches,
                      include,
                      exclude,
                      options_include,
                      options_exclude,
                      poss_vals,
                      poss_min,
                      poss_max,
                      opp_forma,
                      options_opp_forma,
                      first_date,
                      last_date,
                      options_first_date,
                      options_last_date):
    labels = []
    labels.append(coach_label(coaches, options_coaches))
    labels.append(include_label(include, options_include))
    labels.append(exclude_label(exclude, options_exclude))
    labels.append(possession(poss_vals, poss_min, poss_max))
    labels.append(opposition_forma(opp_forma, options_opp_forma))
    labels.append(date_label(first_date, last_date, options_first_date, options_last_date))

    text = '; '.join(filter(None, labels))

    return text