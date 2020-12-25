import plotly.graph_objects as go

from plots.utils_plotly import set_style, draw_field, hex_to_rgba, node_color
from plots.utils import reduce_vector

def plot_players(fig, xs, ys, positions, scores, infos, color):
    maxi, mini = scores['count'].max(), scores['count'].min()
    max_alpha, min_alpha = 1, 0.01
    alphas = (scores['count']-mini)/((maxi-mini)/(max_alpha-min_alpha)) + min_alpha
    colors = list(map(lambda alpha: node_color(color, alpha), alphas))

    fig.add_trace(
        go.Scatter(
            x=xs,
            y=ys,
            mode='markers+text',
            text='<b>' + positions + '</b>',
            marker=dict(
                color=colors,
                size=23,
                line=dict(
                    width=1,
                    color='#bdbdbd'
                )
            ),
            textfont=dict(
                size=8,
                color='#cdcdcd'
            ),
            customdata=infos,
            hovertemplate='%{customdata}<extra></extra>',
            showlegend=False
        )
    )

def plot_arrows(fig, counts, xs, ys, positions):
    max_width, min_width = 1.6, 0.5
    max_alpha, min_alpha = 0.85, 0.5
    maxi, mini = counts['count'].max(), counts['count'].min()

    if mini == maxi:
        mini = 0

    arrows = []
    for _, row in counts.iterrows():
        start = (xs[positions == row['PlayerPosition']][0], ys[positions == row['PlayerPosition']][0])
        end = (xs[positions == row['ReceiverPosition']][0], ys[positions == row['ReceiverPosition']][0])

        start, end = reduce_vector(start, end, 4, 4)

        width = (row['count']-mini)/((maxi-mini)/(max_width-min_width)) + min_width
        alpha = (row['count']-mini)/((maxi-mini)/(max_alpha-min_alpha)) + min_alpha

        arrows.append(
            go.layout.Annotation(dict(
                x=end[0],
                y=end[1],
                xref="x", yref="y",
                text="",
                showarrow=True,
                axref = "x", ayref='y',
                ax= start[0],
                ay= start[1],
                arrowhead = 2,
                arrowwidth=width,
                arrowcolor=hex_to_rgba('#cdcdcd', alpha))
            )
        )
    
    fig.update_layout(annotations=arrows)

def plot(counts, xs, ys, positions, scores, infos, color):
    fig = go.Figure()
    set_style(fig)

    draw_field(fig)

    plot_players(fig, xs, ys, positions, scores, infos, color)
    plot_arrows(fig, counts, xs, ys, positions)

    return fig