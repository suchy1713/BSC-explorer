import dash_html_components as html

def filter_group_title(text):
    return [html.H4(text, className='filter-group-title', style={'color': '#bdbdbd', 'margin-bottom': '0px'}), html.Hr()]