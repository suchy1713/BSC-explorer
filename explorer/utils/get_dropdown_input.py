def get_dropdown_input(df, label_col, value_col):
    df['label'] = df[label_col]
    df['value'] = df[value_col]
    return df[['label', 'value']].to_dict('records')