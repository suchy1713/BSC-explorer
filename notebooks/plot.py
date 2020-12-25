import matplotlib.pyplot as plt
import matplotlib.style as style
from matplotlib.font_manager import FontProperties
import numpy as np
#from highlight_text.htext import fig_htext

def plot_table(ax, cell_text, raw_vals, col_labels, col_widths, title_fontsize, ascending=False):
    table = ax.table(cellText=cell_text, 
                    bbox=[0.016, 0, 0.968, 1],  
                    colLabels=col_labels,
                    colColours=['#131313']*len(col_labels),
                    cellLoc="center",
                    cellColours=np.full_like(cell_text, '#131313'),
                    edges='closed'
                    )

    table.auto_set_font_size(False)

    max_alpha = 0.8
    min_alpha = 0.55
    mini = raw_vals.min()
    maxi = raw_vals.max()

    real_row = 0
    for (row, col), cell in table.get_celld().items():
        cell._text.set_color('#cdcdcd')
        cell.set_edgecolor('0.28')
        cell.set_linewidth(2.5)
        cell.set_text_props(fontproperties=FontProperties(weight='regular', size=15.5/32*title_fontsize))

        if row > 0:
            if cell_text[row-1][1] == '-': 
                alpha = min_alpha
            else:
                alpha = (raw_vals[row-1]-mini)/((maxi-mini)/(max_alpha-min_alpha)) + min_alpha

            if ascending:
                alpha = max_alpha-alpha + min_alpha

            cell._text.set_alpha(alpha)

        if row == 0:
            cell.set_text_props(fontproperties=FontProperties(weight='600', size=16/32*title_fontsize))
            cell._text.set_alpha(0.8)

        cell.set_width(col_widths[col])

    ax.set_aspect(0.93)
    ax.axis('off')

def set_style():
    style.use("seaborn-dark")
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Lato']
    plt.rcParams['axes.facecolor'] = '#131313'
    plt.rcParams['axes.linewidth'] = 2
    plt.rcParams['axes.edgecolor'] = '#ababab'
    plt.rcParams['figure.facecolor'] = '#131313'
    plt.rcParams['savefig.facecolor'] = '#131313'
    plt.rcParams['text.color'] = '#cdcdcd'
    plt.rcParams['font.weight'] = 600
    plt.rcParams['axes.labelcolor'] = '#cdcdcd'

def plot_junk(fig, title, subtitle, instruction, title_font, axes_titles, title_coord=[0.035, 0.962], subtitle_y_dif=0.025, handle_coord=[0.81, 0.987], instr_title_coord=[0.035, 0.103], instr_y_dif=0.091, ax_title_pad=7, title_colors=None):
    if title_colors is None:
        fig.text(title_coord[0], title_coord[1], title,
                        fontsize=title_font,
                        horizontalalignment='left', alpha=0.8)
    else:
        texts = fig_htext(title, title_coord[0], title_coord[1], string_weight=600, color='#cdcdcd', fontsize=title_font, va='bottom', ha='left', highlight_colors=title_colors, highlight_weights=[600]*len(title_colors))
        for t in texts[0]:
            t.set_alpha(0.8)
            #t.set_weight(600)
            #t.set_position((t.get_position()[0], title_coord[1]))

    fig.text(title_coord[0], title_coord[1]-subtitle_y_dif, subtitle,
                    fontsize=20/32*title_font, weight='regular',
                    horizontalalignment='left', alpha=0.8)

    fig.text(handle_coord[0], handle_coord[1], f"Twitter:\n@pwawrzynow",
                    fontsize=24/32*title_font,
                    horizontalalignment='left',
                    va='top', alpha=0.8)

    if instruction != "":
        fig.text(instr_title_coord[0], instr_title_coord[1], f"How to read this?",
                        fontsize=25/32*title_font,
                        horizontalalignment='left', alpha=0.8)

    fig.text(instr_title_coord[0], instr_title_coord[1]-instr_y_dif, instruction,
                    fontsize=18/32*title_font, weight='regular',
                    linespacing=1.45,
                    horizontalalignment='left', alpha=0.8)

    for entry in axes_titles:
        entry[0].set_title(entry[1], fontsize=18/32*title_font, pad=ax_title_pad, alpha=0.8, weight=600)