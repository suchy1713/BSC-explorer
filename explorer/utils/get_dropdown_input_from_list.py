def get_dropdown_input_from_list(l):
    # sanitize input
    l = list(l)

    opt = []
    for item in l:
        opt.append({'label': item, 'value': item})

    return opt
