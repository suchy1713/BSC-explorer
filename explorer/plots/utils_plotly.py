import plotly.graph_objects as go
from plotly.colors import hex_to_rgb, convert_to_RGB_255, find_intermediate_color
import numpy as np

field_color = '#6e6e6e'
field_dark_color = '#595959'
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

bg_color_rgb = (31, 30, 28)


def node_color(color, ratio):
    rgb = hex_to_rgb(color)

    return f"rgb{tuple(map(int, find_intermediate_color(bg_color_rgb, rgb, ratio)))}"


def hex_to_rgba(hex_val, a):
    if a < 1e-5:
        a = 0

    rgb = hex_to_rgb(hex_val)
    rgb += (a,)

    return f'rgba{str(rgb)}'


def ellipse_arc(x_center, y_center, a, b, start_angle, end_angle, n=100, closed=False):
    t = np.linspace(start_angle, end_angle, n)
    x = x_center + a*np.cos(t)
    y = y_center + b*np.sin(t)
    path = f'M {x[0]}, {y[0]}'
    for k in range(1, len(t)):
        path += f'L{x[k]}, {y[k]}'
    if closed:
        path += ' Z'
    return path


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
            x=[0, -goal_height, -goal_height, 0],
            y=[field_width / 2 - goal_length / 2, field_width / 2 - goal_length / 2, field_width / 2 + goal_length / 2,
               field_width / 2 + goal_length / 2],
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
            x=[field_length, field_length + goal_height, field_length + goal_height, field_length],
            y=[field_width / 2 - goal_length / 2, field_width / 2 - goal_length / 2, field_width / 2 + goal_length / 2,
               field_width / 2 + goal_length / 2],
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

    # Pitch Outline & Centre Line
    plot_line(fig, [0, 0], [0, field_width])
    plot_line(fig, [0, field_length], [field_width, field_width])
    plot_line(fig, [field_length, field_length], [field_width, 0])
    plot_line(fig, [field_length, 0], [0, 0])
    plot_line(fig, [field_length / 2, field_length / 2], [0, field_width])

    # Left Penalty Area
    plot_line(fig, [pen_area_width, pen_area_width],
              [field_width / 2 - pen_area_length / 2, field_width / 2 + pen_area_length / 2])
    plot_line(fig, [0, pen_area_width], [field_width / 2 + pen_area_length / 2, field_width / 2 + pen_area_length / 2])
    plot_line(fig, [pen_area_width, 0], [field_width / 2 - pen_area_length / 2, field_width / 2 - pen_area_length / 2])

    # Right Penalty Area
    plot_line(fig, [field_length, field_length - pen_area_width],
              [field_width / 2 + pen_area_length / 2, field_width / 2 + pen_area_length / 2])
    plot_line(fig, [field_length - pen_area_width, field_length - pen_area_width],
              [field_width / 2 + pen_area_length / 2, field_width / 2 - pen_area_length / 2], )
    plot_line(fig, [field_length - pen_area_width, field_length],
              [field_width / 2 - pen_area_length / 2, field_width / 2 - pen_area_length / 2])

    # Left 6-yard Box
    plot_line(fig, [0, goal_area_width],
              [field_width / 2 + goal_area_length / 2, field_width / 2 + goal_area_length / 2])
    plot_line(fig, [goal_area_width, goal_area_width],
              [field_width / 2 + goal_area_length / 2, field_width / 2 - goal_area_length / 2])
    plot_line(fig, [goal_area_width, 0],
              [field_width / 2 - goal_area_length / 2, field_width / 2 - goal_area_length / 2])

    # Right 6-yard Box
    plot_line(fig, [field_length, field_length - goal_area_width],
              [field_width / 2 + goal_area_length / 2, field_width / 2 + goal_area_length / 2])
    plot_line(fig, [field_length - goal_area_width, field_length - goal_area_width],
              [field_width / 2 + goal_area_length / 2, field_width / 2 - goal_area_length / 2])
    plot_line(fig, [field_length - goal_area_width, field_length],
              [field_width / 2 - goal_area_length / 2, field_width / 2 - goal_area_length / 2])

    # Left Goal
    plot_line(fig, [0, -goal_height], [field_width / 2 - goal_length / 2, field_width / 2 - goal_length / 2])
    plot_line(fig, [0, -goal_height], [field_width / 2 + goal_length / 2, field_width / 2 + goal_length / 2])
    plot_line(fig, [-goal_height, -goal_height], [field_width / 2 - goal_length / 2, field_width / 2 + goal_length / 2])

    # Right Goal
    plot_line(fig, [field_length, field_length + goal_height],
              [field_width / 2 - goal_length / 2, field_width / 2 - goal_length / 2])
    plot_line(fig, [field_length, field_length + goal_height],
              [field_width / 2 + goal_length / 2, field_width / 2 + goal_length / 2])
    plot_line(fig, [field_length + goal_height, field_length + goal_height],
              [field_width / 2 - goal_length / 2, field_width / 2 + goal_length / 2])

    # Centre Circle
    fig.add_trace(
        go.Scatter(
            x=[105 / 2], y=[68 / 2],
            mode='markers',
            marker=dict(
                color=hex_to_rgba(field_color, 0),
                size=60,
                opacity=1,
                line=dict(
                    width=1,
                    color=field_color
                )
            ),
            showlegend=False,
            hoverinfo='none'
        )
    )

    # Spots
    fig.add_trace(
        go.Scatter(
            x=[11, 105 / 2, 105 - 11], y=[68 / 2] * 3,
            mode='markers',
            marker=dict(
                color=field_color,
                size=6,
                opacity=0.65
            ),
            showlegend=False,
            hoverinfo='none'
        )
    )

    # left arc
    fig.add_shape(
        type="path",
        path=ellipse_arc(
            x_center=pen_spot-0.5,
            y_center=field_width/2,
            a=10,
            b=10,
            start_angle=-np.pi/3.37,
            end_angle=np.pi/3.37,
            n=60),
        line_color=field_color,
        line_width=1
    )

    # right arc
    fig.add_shape(
        type="path",
        path=ellipse_arc(
            x_center=105 - (pen_spot - 0.5),
            y_center=field_width / 2,
            a=10,
            b=10,
            start_angle=np.pi - (-np.pi / 3.37),
            end_angle=np.pi - (np.pi / 3.37),
            n=60),
        line_color=field_color,
        line_width=1
    )

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

    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        range=(-2, field_length + 2),
        visible=False
    )

    fig.update_yaxes(
        showgrid=False,
        zeroline=False,
        range=(-0.5, field_width + 0.5),
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
