import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Rectangle

def draw_field(ax, left_to_right=True, divide_halves=False, correct_aspect=False, arrow=True):
    field_color = '0.28'
    field_linewidth = 5
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

    #Pitch Outline & Centre Line
    ax.plot([0, 0], [0, field_width], color=field_color, alpha=field_alpha, linewidth=field_linewidth, zorder=130)
    ax.plot([0, field_length], [field_width, field_width], color=field_color, alpha=field_alpha, linewidth=field_linewidth, zorder=130)
    ax.plot([field_length, field_length], [field_width, 0], color=field_color, alpha=field_alpha, linewidth=field_linewidth, zorder=130)
    ax.plot([field_length, 0], [0, 0], color=field_color, alpha=field_alpha, linewidth=field_linewidth, zorder=130)
    ax.plot([field_length/2, field_length/2], [0, field_width], color=field_color, alpha=field_alpha, linewidth=field_linewidth)

    if divide_halves:
        ml = 1.25
        ml2 = 1.4
        ax.plot([field_length/2-ml2, field_length/2-ml2], [0, field_width], color=field_color, alpha=field_alpha, linewidth=field_linewidth, zorder=170)
        ax.plot([field_length/2+ml, field_length/2+ml], [0, field_width], color=field_color, alpha=field_alpha, linewidth=field_linewidth, zorder=170)
        ax.plot([105/2, 105/2], [0.3, field_width-0.3], linestyle='-', color='#131313', alpha=1, linewidth=10, zorder=150)

    #Left Penalty Area
    ax.plot([pen_area_width, pen_area_width], [field_width/2-pen_area_length/2, field_width/2+pen_area_length/2], color=field_color, alpha=field_alpha, linewidth=field_linewidth)
    ax.plot([0, pen_area_width], [field_width/2+pen_area_length/2, field_width/2+pen_area_length/2], color=field_color, alpha=field_alpha, linewidth=field_linewidth)
    ax.plot([pen_area_width, 0], [field_width/2-pen_area_length/2, field_width/2-pen_area_length/2], color=field_color, alpha=field_alpha, linewidth=field_linewidth)
    
    # #Right Penalty Area
    ax.plot([field_length, field_length-pen_area_width], [field_width/2+pen_area_length/2, field_width/2+pen_area_length/2], color=field_color, alpha=field_alpha, linewidth=field_linewidth)
    ax.plot([field_length-pen_area_width, field_length-pen_area_width],[field_width/2+pen_area_length/2, field_width/2-pen_area_length/2], color=field_color, alpha=field_alpha, linewidth=field_linewidth)
    ax.plot([field_length-pen_area_width, field_length], [field_width/2-pen_area_length/2, field_width/2-pen_area_length/2], color=field_color, alpha=field_alpha, linewidth=field_linewidth)

    #Left 6-yard Box
    ax.plot([0, goal_area_width],[field_width/2+goal_area_length/2, field_width/2+goal_area_length/2], color=field_color, alpha=field_alpha, linewidth=field_linewidth)
    ax.plot([goal_area_width, goal_area_width],[field_width/2+goal_area_length/2, field_width/2-goal_area_length/2], color=field_color, alpha=field_alpha, linewidth=field_linewidth)
    ax.plot([goal_area_width, 0],[field_width/2-goal_area_length/2, field_width/2-goal_area_length/2], color=field_color, alpha=field_alpha, linewidth=field_linewidth)
    
    #Right 6-yard Box
    ax.plot([field_length, field_length-goal_area_width], [field_width/2+goal_area_length/2, field_width/2+goal_area_length/2], color=field_color, alpha=field_alpha, linewidth=field_linewidth)
    ax.plot([field_length-goal_area_width, field_length-goal_area_width], [field_width/2+goal_area_length/2, field_width/2-goal_area_length/2], color=field_color, alpha=field_alpha, linewidth=field_linewidth)
    ax.plot([field_length-goal_area_width, field_length], [field_width/2-goal_area_length/2, field_width/2-goal_area_length/2], color=field_color, alpha=field_alpha, linewidth=field_linewidth)
    
    #Left Goal
    ax.plot([0, -goal_height],[field_width/2-goal_length/2, field_width/2-goal_length/2], color=field_color, alpha=field_alpha, linewidth=field_linewidth)
    ax.plot([0, -goal_height],[field_width/2+goal_length/2, field_width/2+goal_length/2], color=field_color, alpha=field_alpha, linewidth=field_linewidth)
    ax.plot([-goal_height, -goal_height],[field_width/2-goal_length/2, field_width/2+goal_length/2], color=field_color, alpha=field_alpha, linewidth=field_linewidth)

    #Right Goal
    ax.plot([field_length, field_length+goal_height],[field_width/2-goal_length/2, field_width/2-goal_length/2], color=field_color, alpha=field_alpha, linewidth=field_linewidth)
    ax.plot([field_length, field_length+goal_height],[field_width/2+goal_length/2, field_width/2+goal_length/2], color=field_color, alpha=field_alpha, linewidth=field_linewidth)
    ax.plot([field_length+goal_height, field_length+goal_height],[field_width/2-goal_length/2, field_width/2+goal_length/2], color=field_color, alpha=field_alpha, linewidth=field_linewidth)

    #Prepare Circles
    centreCircle = plt.Circle((field_length/2, field_width/2), 9.15, color=field_color, fill=False, alpha=field_alpha, linewidth=field_linewidth)
    centreSpot = plt.Circle((field_length/2, field_width/2), 0.4, color=field_color, alpha=field_alpha, linewidth=field_linewidth)
    leftPenSpot = plt.Circle((pen_spot, field_width/2), 0.4, color=field_color, alpha=field_alpha, linewidth=field_linewidth)
    rightPenSpot = plt.Circle((field_length-pen_spot, field_width/2), 0.4, color=field_color, alpha=field_alpha, linewidth=field_linewidth)
    
    #Draw Circles
    ax.add_patch(centreCircle)
    ax.add_patch(centreSpot)
    ax.add_patch(leftPenSpot)
    ax.add_patch(rightPenSpot)

    #Prepare Arcs
    leftArc = Arc((pen_spot-0.5, field_width/2), height=18.3, width=18.3, angle=0, theta1=310, theta2=50, color=field_color, alpha=field_alpha, linewidth=field_linewidth)
    rightArc = Arc((field_length-pen_spot+0.5, field_width/2), height=18.3, width=18.3, angle=0, theta1=130, theta2=230, color=field_color, alpha=field_alpha, linewidth=field_linewidth)

    #Draw Arcs
    ax.add_patch(leftArc)
    ax.add_patch(rightArc)

    #Prepare Corners
    br_cor = Arc((field_length, 0),
        height=2,
        width=2,
        angle=0,
        theta1=90,
        theta2=180,
        color=field_color,
        alpha=field_alpha,
        linewidth=field_linewidth)

    tr_cor = Arc((field_length, field_width),
        height=2,
        width=2,
        angle=0,
        theta1=180,
        theta2=270,
        color=field_color,
        alpha=field_alpha,
        linewidth=field_linewidth)

    tl_cor = Arc((0, field_width),
        height=2,
        width=2,
        angle=0,
        theta1=270,
        theta2=0,
        color=field_color,
        alpha=field_alpha,
        linewidth=field_linewidth)
    
    bl_cor = Arc((0, 0),
        height=2,
        width=2,
        angle=0,
        theta1=0,
        theta2=90,
        color=field_color,
        alpha=field_alpha,
        linewidth=field_linewidth)

    ax.add_patch(br_cor)
    ax.add_patch(tr_cor)
    ax.add_patch(tl_cor)
    ax.add_patch(bl_cor)

    #Tidy Axes
    ax.axis('off')
    ax.set_xlim(-2, field_length+2)
    ax.set_ylim(-0.5, field_width+0.5)

    if arrow == True:
        if left_to_right:
            x = 105/3
            dx = 105/3
        else:
            x = 105/6*4
            dx = -105/3

        ax.arrow(
                x, 34,
                dx, 0,
                color=field_color,
                alpha=0.3,
                length_includes_head=True,
                zorder=50,
                head_width=15,
                head_length=12,
                width=5
            )
    elif arrow == 'small':
        if left_to_right:
            x = 105/3
            dx = 105/3
        else:
            x = 105/6*4
            dx = -105/3
        ax.arrow(
                x, 0,
                dx, 0,
                color=field_color,
                alpha=0.3,
                length_includes_head=True,
                zorder=50,
                head_width=6,
                head_length=4.5,
                width=2
            )

    if correct_aspect:
        ax.set_aspect(1)

field_width = 68
field_length = 105