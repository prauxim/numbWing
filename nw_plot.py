import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from numpy.polynomial.polynomial import polyfit
from numbWing import *
from nw_plot import *



def main():
    comp_plot()


def comp_plot():

    """Comparison ov 1v1 vs Squad results, WIP"""

    # plot_1v1()
    plot_squad()
    fig, ax = plt.subplots()

    df_1v1 = pd.read_csv('./results/benchmark_1v1_n49999_pp.csv')
    df_squad = pd.read_csv('./results/benchmark_squad_n14999_pp.csv')
    x_data = df_1v1['dmg_efficiency']
    y_data = df_squad['projected_dmg_at_200']
    colors = []
    for faction in df_1v1.faction:
        color = 'green'
        if 'Empire' in faction:
            color = 'blue'
        elif 'Rebel' in faction:
            color = 'red'
        colors.append(copy.copy(color))

    labels = df_1v1.index.values
    for i, txt in enumerate(labels):

        offset_x, offset_y = 0.15, 0.15

        special_offsets = {'ywing_scum':(0.15, -0.25),
                           'hwk_reb': (0.15, 0.05),
                           'hwk_scum': (0.15, -0.35),
                           'aggressor_ga':(0.15, -0.30),
                           'attackshu':(0.15, -0.30),
                           'z95_reb':(0.15, -0.30)}

        for term, offset in special_offsets.items():
            if term in txt:
                offset_x, offset_y = copy.copy(offset)
        ax.annotate(txt, (x_data[i]+offset_x, y_data[i]+offset_y))

    ax.scatter(x_data, y_data, c=colors)

    plt.xlabel('squad_cost')
    plt.ylabel('benchmark squad dmg')
    plt.grid(True)
    plt.savefig("./results/benchmark_comp.png")



def plot_squad():


    mode = 'squad'

    fig, ax = plt.subplots()

    fIn = './results/benchmark_squad_n14999.csv'
    df = pd.DataFrame.from_csv(fIn)
    # plt.scatter(df['cost'], df['1v1dmg'])

    cost = df['squad_cost'].values

    df['interp'] = (df['win_rate_1']-50) / (df['win_rate_1']-df['win_rate_2'])
    df['dmg'] = df['enemy_health_2'] - (1-df['interp'])*(df['enemy_health_2']-df['enemy_health_1'])

    dmg = df['dmg'].values

    labels = df.index.values
    colors = []
    for faction in df.faction:
        color = 'green'
        if 'Empire' in faction:
            color = 'blue'
        elif 'Rebel' in faction:
            color = 'red'
        colors.append(copy.copy(color))


    ax.scatter(cost, dmg, c=colors)
    for i, txt in enumerate(labels):
        squad_size = df['squad_size'][txt]
        txt = '%s x%s' % (txt, squad_size)

        offset_x, offset_y = 0.15, 0.15

        special_offsets = {'ywing_scum':(0.15, -0.25),
                           'hwk_reb': (0.15, 0.05),
                           'hwk_scum': (0.15, -0.35),
                           'aggressor_ga':(0.15, -0.30),
                           'attackshu':(0.15, -0.30),
                           'z95_reb':(0.15, -0.30)}

        for term, offset in special_offsets.items():
            if term in txt:
                offset_x, offset_y = copy.copy(offset)
        ax.annotate(txt, (cost[i]+offset_x, dmg[i]+offset_y))

    # import numpy as np
    # import matplotlib.pyplot as plt


    # polyfit

    p0, p1, p2 = polyfit(cost, dmg, 2)


    # print p0, p1, p2
    cost_fit = np.linspace(cost.min(), cost.max())
    dmg_poly = [p0 + p1 * x + p2 * x * x for x in cost_fit]

    poly_r = tuple([round(x,3) for x in [p0, p1, p2]])
    ax.annotate('dmg_fit=%s + %s*cost + %s*cost^2' % poly_r, (220, 25))
    plt.plot(cost_fit, dmg_poly, '-')


    typical_dmg = p0 + p1*200 + p2*200**2
    df['typical_dmg_for_cost'] = p0 + p1*df.squad_cost + p2*df.squad_cost**2
    df['projected_dmg_at_200'] = df['dmg'] - df['typical_dmg_for_cost'] + typical_dmg



    fig = plt.gcf()
    fig.set_size_inches(24, 16)

    plt.xlabel('squad_cost')
    plt.ylabel('benchmark squad dmg')
    plt.grid(True)
    plt.savefig("./results/benchmark_squad.png")


    pp_path =os.path.splitext(fIn)[0] + '_pp.csv'
    df.to_csv(pp_path)


def plot_1v1():
    fIn = './results/benchmark_1v1_n49999.csv'
    df = pd.DataFrame.from_csv(fIn)
    # plt.scatter(df['cost'], df['1v1dmg'])

    fig, ax = plt.subplots()
    cost = df['cost'].values


    dmg = df['1v1dmg'].values

    df['dmg_efficiency'] = df['1v1dmg']/df['cost']


    labels = df.index.values
    colors = []
    for faction in df.faction:
        color = 'green'
        if 'Empire' in faction:
            color = 'blue'
        elif 'Rebel' in faction:
            color = 'red'
        colors.append(copy.copy(color))

    ax.scatter(cost, dmg, c=colors)
    for i, txt in enumerate(labels):

        offset_x, offset_y = 0.15, 0.15

        special_offsets = {'phantom': (0.25, -0.05),
                           'x1': (0.15, -0.15),
                           'aggressor_gal': (-3.15, -0.95),
                           'sheath': (0.15, 0.15),
                           'hwk_reb': (0.15, 0.0),
                           'hwk_scum': (0.15, -0.2),
                           'ywing_scum': (0.15, -0.05),
                           'ywing_reb': (0.15, -0.25),
                           't65': (0.2, -0.25),
                           'bwing': (0.15, -0.15),
                           'awing': (0.15, -0.15),
                           'attacksh': (0.15, -0.15),
                           }

        for term, offset in special_offsets.items():
            if term in txt:
                offset_x, offset_y = copy.copy(offset)
        ax.annotate(txt, (cost[i]+offset_x, dmg[i]+offset_y))


    # import numpy as np
    # import matplotlib.pyplot as plt


    # polyfit

    p0, p1, p2 = polyfit(cost, dmg, 2)

    print p0, p1, p2
    cost_fit = np.linspace(cost.min(), cost.max())
    dmg_poly = [p0 + p1*x + p2*x*x for x in cost_fit]
    plt.plot(cost_fit, dmg_poly, '-')


    poly_r = tuple([round(x,3) for x in [p0, p1, p2]])
    ax.annotate('dmg_fit=%s + %s*cost + %s*cost^2' % poly_r, (76, 16))


    fig = plt.gcf()
    fig.set_size_inches(24, 16)

    plt.xlabel('ship_cost')
    plt.ylabel('benchmark 1v1 dmg')
    plt.grid(True)
    plt.savefig("./results/benchmark_1v1.png")


    pp_path =os.path.splitext(fIn)[0] + '_pp.csv'
    df.to_csv(pp_path)

if __name__ == '__main__':
    plot_main()
