import numpy as np
import Gnuplot


def plot(datasets, title=None, normalize=True, filename=None, display=False):
    g = Gnuplot.Gnuplot(persist=1)
    if title is not None:
        g.title(title)
    dlist = []
    for dataset in datasets:
        x = dataset[0]
        y = dataset[1]
        if normalize:
            x = x / np.linalg.norm(x)
            y = y / np.linalg.norm(y)
        dlist.append(Gnuplot.Data(x, y, with_='l', title=dataset[2]))
    g('set grid')
    g('set key left')
    if not display:
        g('set terminal svg size 1600,800')
        g('set output "' + filename + '"')
    if len(dlist) == 1:
        __plot_1(g, dlist[0])
    elif len(dlist) == 2:
        __plot_2(g, dlist[0], dlist[1])
    elif len(dlist) == 3:
        __plot_3(g, dlist[0], dlist[1], dlist[2])
    else:
        print "Unsupported number of dataset!"
    if filename is not None and display:
        g.hardcopy(filename, terminal='svg', size=[1600,800])


def __plot_1(gnuplot, d1):
    gnuplot.plot(d1)


def __plot_2(gnuplot, d1, d2):
    gnuplot.plot(d1, d2)


def __plot_3(gnuplot, d1, d2, d3):
    gnuplot.plot(d1, d2, d3)
