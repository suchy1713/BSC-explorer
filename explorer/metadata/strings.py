# Main Tabs
layout_filters_title = 'Customize'
team_filters_title = lambda x: f'Team {x}'

# Layout Filter Group
vertical_label = 'Vertical'
n_teams_label = 'Number of Teams'
preset_label = 'Preset'
save_preset_label = 'Save Current Selection'
save_preset_placeholder = 'Preset Name'
save_preset_button_label = 'Save as Preset'

# By Team Filter Group
team_filter_group_title = lambda x: f'Select Team {x}'
season_filter_label = 'Season'
league_filter_label = 'League'
club_filter_label = 'Team'
coach_filter_label = 'Coach'

# By Players Filter Group
players_filter_group_title = 'By Players'
include_players_filter_label = 'Include Line-ups With'
exclude_players_filter_label = 'Exclude Line-ups With'

# By Opposition Filter Group
opposition_filter_group_title = 'By Opposition'
opposition_name_filter_label = 'Team'
opposition_formation_filter_label = 'Formation'
possession_filter_label = 'Possession %'

# By Date Filter Group
date_filter_group_title = 'By Date'
start_date_filter_date = 'First Date to Include'
end_date_filter_date = 'Last Date to Include'

# By Plot Type Filter Group
plot_type_filter_group_title = 'Customize Plot'
formation_filter_label = 'Formation'
visual_filter_label = 'Visualization'

# Formation and Filters Labels
formation_label = lambda label, nineties: label + ' (' + round(nineties, 1).astype(str) + ' 90s)'

# Viz Types
passing_net = 'Pass Network'
attacking_territories = 'Territory Plot - Attack'
defensive_territories = 'Territory Plot - Defence'
heatmap_attack = 'Heatmap - Attack'
heatmap_defence = 'Heatmap - Defence'

# Viz Filters
phase_label = 'Location'
passes_label = 'Pass Type'
positions_label = 'Positions'
all_label = 'All'
build_up_label = 'Deep'
finishing_label = 'High'
progressive_label = 'Progressive'
long_label = 'Long'
weighted_by_xt_label = 'Weighted by xT'

default_passes = all_label
default_phase = all_label
