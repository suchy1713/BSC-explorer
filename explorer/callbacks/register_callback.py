from callbacks.filter_groups.by_team import by_team
from callbacks.filter_groups.by_players import by_players
from callbacks.filter_groups.by_opposition import by_opposition
from callbacks.filter_groups.by_date import by_date
from callbacks.filter_groups.plot_type import *
from callbacks.sections.layout_filters import layout_filters
from callbacks.modules.sidebar import sidebar
from callbacks.modules.content import content


def register_callbacks(app, db, seasons):
    by_team(app, db)
    by_players(app, db)
    by_opposition(app, db)
    by_date(app, db)
    layout_filters(app)
    sidebar(app, seasons)
    intermid_events(app, db)
    generate_viz_filters(app)
    intermid_version_dict(app)
    content(app)
    set_preset(app)

    for coords in ['00', '10', '01', '11']:
        plot_type(app, db, coords)
