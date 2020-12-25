import plotly.graph_objects as go
from plotly.colors import hex_to_rgb, convert_to_RGB_255, find_intermediate_color

field_color = '#6e6e6e'
field_inside_color = '#1f1e1c'
field_linewidth = 1
field_alpha = 1

field_length = 105
field_width = 68

pen_area_length = 40.3
pen_area_width = 16.5

goal_area_length = 18.3
goal_area_width = 5.5

goal_length = 7.3
goal_height = 1

pen_spot = 11

import pandas as pd
corner_threshold = 2
ko_threshold=1
def exclude_corners(passes):
    corners = passes.loc[passes['StartX'] > 105-corner_threshold].loc[(passes['StartY'] > 68-corner_threshold) | (passes['StartY'] < corner_threshold)]
    passes = pd.concat([passes, corners]).drop_duplicates(keep=False)

    throw_ins = passes.loc[(passes['StartY'] == 0) | (passes['StartY'] == 68)]
    passes = pd.concat([passes, throw_ins]).drop_duplicates(keep=False)

    kick_offs = passes.loc[(52.5-ko_threshold < passes['StartX']) & (passes['StartX'] < 52.5+ko_threshold) & (34-ko_threshold < passes['StartY']) & (passes['StartY'] < 34+ko_threshold)]
    passes = pd.concat([passes, kick_offs]).drop_duplicates(keep=False)

    return passes

bg_color_rgb = (31, 30, 28)
def node_color(color, ratio):
    rgb = hex_to_rgb(color)

    return f"rgb{tuple(map(int, find_intermediate_color(bg_color_rgb, rgb, ratio)))}"
    
def hex_to_rgba(hex_val, a):
    rgb = hex_to_rgb(hex_val)
    rgb += (a,)

    return f'rgba{str(rgb)}'

def custom_line(fig, x, y, color, width):
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', hoverinfo='none', showlegend=False,
                         line=dict(color=color, width=width)))

def plot_line(fig, x, y):
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', hoverinfo='none', showlegend=False,
                         line=dict(color=field_color, width=field_linewidth)))

def plot_dot(fig, x, y, size):
    fig.add_trace(go.Scatter(x=x, y=y, mode='markers', hoverinfo='none', showlegend=False,
                         marker=dict(color=hex_to_rgba(field_color, 0.5), size=size)))

def draw_field(fig):
    fig.add_trace(
        go.Scatter(
            x=[0, -goal_height, -goal_height, 0], y=[field_width/2-goal_length/2, field_width/2-goal_length/2, field_width/2+goal_length/2, field_width/2+goal_length/2],
            mode='lines', 
            line=dict(
                color=hex_to_rgba('#ffffff', 0),
                width=2,
            ), 
            showlegend=False, 
            fill="tonext", 
            fillcolor=field_inside_color,
            hoverinfo='none'
        )
    )

    fig.add_trace(
        go.Scatter(
            x=[field_length, field_length+goal_height, field_length+goal_height, field_length], y=[field_width/2-goal_length/2, field_width/2-goal_length/2, field_width/2+goal_length/2, field_width/2+goal_length/2],
            mode='lines', 
            line=dict(
                color=hex_to_rgba('#ffffff', 0),
                width=2,
            ), 
            showlegend=False, 
            fill="tonext", 
            fillcolor=field_inside_color,
            hoverinfo='none'
        )
    )

    fig.add_trace(
        go.Scatter(
            x=[0, 0, 105, 105], y=[0, 68, 68, 0],
            mode='lines', 
            line=dict(
                color=hex_to_rgba('#ffffff', 0),
                width=2,
            ), 
            showlegend=False, 
            fill="tonext", 
            fillcolor=field_inside_color,
            hoverinfo='none'
        )
    )

    #Pitch Outline & Centre Line
    plot_line(fig, [0, 0], [0, field_width])
    plot_line(fig, [0, field_length], [field_width, field_width])
    plot_line(fig, [field_length, field_length], [field_width, 0])
    plot_line(fig, [field_length, 0], [0, 0])
    plot_line(fig, [field_length/2, field_length/2], [0, field_width])

    #Left Penalty Area
    plot_line(fig, [pen_area_width, pen_area_width], [field_width/2-pen_area_length/2, field_width/2+pen_area_length/2])
    plot_line(fig, [0, pen_area_width], [field_width/2+pen_area_length/2, field_width/2+pen_area_length/2])
    plot_line(fig, [pen_area_width, 0], [field_width/2-pen_area_length/2, field_width/2-pen_area_length/2])

    #Right Penalty Area
    plot_line(fig, [field_length, field_length-pen_area_width], [field_width/2+pen_area_length/2, field_width/2+pen_area_length/2])
    plot_line(fig, [field_length-pen_area_width, field_length-pen_area_width],[field_width/2+pen_area_length/2, field_width/2-pen_area_length/2],)
    plot_line(fig, [field_length-pen_area_width, field_length], [field_width/2-pen_area_length/2, field_width/2-pen_area_length/2])
    
    #Left 6-yard Box
    plot_line(fig, [0, goal_area_width],[field_width/2+goal_area_length/2, field_width/2+goal_area_length/2])
    plot_line(fig, [goal_area_width, goal_area_width],[field_width/2+goal_area_length/2, field_width/2-goal_area_length/2])
    plot_line(fig, [goal_area_width, 0],[field_width/2-goal_area_length/2, field_width/2-goal_area_length/2])

    #Right 6-yard Box
    plot_line(fig, [field_length, field_length-goal_area_width], [field_width/2+goal_area_length/2, field_width/2+goal_area_length/2])
    plot_line(fig, [field_length-goal_area_width, field_length-goal_area_width], [field_width/2+goal_area_length/2, field_width/2-goal_area_length/2])
    plot_line(fig, [field_length-goal_area_width, field_length], [field_width/2-goal_area_length/2, field_width/2-goal_area_length/2])

    #Left Goal
    plot_line(fig, [0, -goal_height],[field_width/2-goal_length/2, field_width/2-goal_length/2])
    plot_line(fig, [0, -goal_height],[field_width/2+goal_length/2, field_width/2+goal_length/2])
    plot_line(fig, [-goal_height, -goal_height],[field_width/2-goal_length/2, field_width/2+goal_length/2])

    #Right Goal
    plot_line(fig, [field_length, field_length+goal_height],[field_width/2-goal_length/2, field_width/2-goal_length/2])
    plot_line(fig, [field_length, field_length+goal_height],[field_width/2+goal_length/2, field_width/2+goal_length/2])
    plot_line(fig, [field_length+goal_height, field_length+goal_height],[field_width/2-goal_length/2, field_width/2+goal_length/2])

    # #Prepare Circles
    # centreCircle = plt.Circle((field_length/2, field_width/2), 9.15, color=field_color, fill=False, alpha=field_alpha, linewidth=field_linewidth)
    # centreSpot = plt.Circle((field_length/2, field_width/2), 0.4, color=field_color, alpha=field_alpha, linewidth=field_linewidth)
    # leftPenSpot = plt.Circle((pen_spot, field_width/2), 0.4, color=field_color, alpha=field_alpha, linewidth=field_linewidth)
    # rightPenSpot = plt.Circle((field_length-pen_spot, field_width/2), 0.4, color=field_color, alpha=field_alpha, linewidth=field_linewidth)
    
    # #Draw Circles
    # ax.add_patch(centreCircle)
    # ax.add_patch(centreSpot)
    # ax.add_patch(leftPenSpot)
    # ax.add_patch(rightPenSpot)

    # #Prepare Arcs
    # leftArc = Arc((pen_spot-0.5, field_width/2), height=18.3, width=18.3, angle=0, theta1=310, theta2=50, color=field_color, alpha=field_alpha, linewidth=field_linewidth)
    # rightArc = Arc((field_length-pen_spot+0.5, field_width/2), height=18.3, width=18.3, angle=0, theta1=130, theta2=230, color=field_color, alpha=field_alpha, linewidth=field_linewidth)

    # #Draw Arcs
    # ax.add_patch(leftArc)
    # ax.add_patch(rightArc)

    # #Prepare Corners
    # br_cor = Arc((field_length, 0),
    #     height=2,
    #     width=2,
    #     angle=0,
    #     theta1=90,
    #     theta2=180,
    #     color=field_color,
    #     alpha=field_alpha,
    #     linewidth=field_linewidth)

    # tr_cor = Arc((field_length, field_width),
    #     height=2,
    #     width=2,
    #     angle=0,
    #     theta1=180,
    #     theta2=270,
    #     color=field_color,
    #     alpha=field_alpha,
    #     linewidth=field_linewidth)

    # tl_cor = Arc((0, field_width),
    #     height=2,
    #     width=2,
    #     angle=0,
    #     theta1=270,
    #     theta2=0,
    #     color=field_color,
    #     alpha=field_alpha,
    #     linewidth=field_linewidth)
    
    # bl_cor = Arc((0, 0),
    #     height=2,
    #     width=2,
    #     angle=0,
    #     theta1=0,
    #     theta2=90,
    #     color=field_color,
    #     alpha=field_alpha,
    #     linewidth=field_linewidth)

    # ax.add_patch(br_cor)
    # ax.add_patch(tr_cor)
    # ax.add_patch(tl_cor)
    # ax.add_patch(bl_cor)

    # #Tidy Axes
    # ax.axis('off')
    # ax.set_xlim(-2, field_length+2)
    # ax.set_ylim(-0.5, field_width+0.5)

    # if arrow == True:
    #     if left_to_right:
    #         x = 105/3
    #         dx = 105/3
    #     else:
    #         x = 105/6*4
    #         dx = -105/3

    #     ax.arrow(
    #             x, 34,
    #             dx, 0,
    #             color=field_color,
    #             alpha=0.3,
    #             length_includes_head=True,
    #             zorder=50,
    #             head_width=15,
    #             head_length=12,
    #             width=5
    #         )
    # elif arrow == 'small':
    #     if left_to_right:
    #         x = 105/3
    #         dx = 105/3
    #     else:
    #         x = 105/6*4
    #         dx = -105/3
    #     ax.arrow(
    #             x, 0,
    #             dx, 0,
    #             color=field_color,
    #             alpha=0.3,
    #             length_includes_head=True,
    #             zorder=50,
    #             head_width=6,
    #             head_length=4.5,
    #             width=2
    #         )

    # if correct_aspect:
    #     ax.set_aspect(1)

    # field_width = 68
    # field_length = 105

    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        range=(-2, field_length+2),
        fixedrange=True,
        visible=False
    )

    fig.update_yaxes(
        showgrid=False,
        zeroline=False,
        range=(-0.5, field_width+0.5),
        fixedrange=True,
        visible=False
    )

def set_style(fig):
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="#242321",
        plot_bgcolor='rgba(0,0,0,0)',
        font_family="Lato",
        font_color="#d9d9d9",
        font_size=12,
        hoverlabel=dict(
            bgcolor="#1f1e1c",
            font_size=13,
            font_color=hex_to_rgba('#bdbdbd', 0.85),
            font_family="Lato",
            bordercolor='#bdbdbd'
        ),
        yaxis={
            'scaleanchor': 'x',
            'scaleratio': 1,
            'autorange': True
        },
        xaxis={
            'autorange': True
        }
)