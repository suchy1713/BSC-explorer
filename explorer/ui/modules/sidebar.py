import dash_html_components as html

from ui.components.app_title import app_title
from ui.components.tabs import tabs
from ui.sections.layout_filters import layout_filters
from ui.sections.placeholder import get_placeholder
from metadata.strings import *


def sidebar(app, seasons):
    return html.Div([
        app_title(app),
        tabs(
            'main-tabs',
            [
                layout_filters,
                get_placeholder,
                lambda: None,
                lambda: None,
                lambda: None
            ],
            [
                layout_filters_title,
                team_filters_title(1),
                team_filters_title(2),
                team_filters_title(3),
                team_filters_title(4)
            ],
            [
                f'tab-{i}' for i in range(0, 5)
            ],
            1,
            display=[True, True, True, False, False]
        )
    ], id='sidebar', className='shadow')
