
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.mplot3d import axes3d, Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import numpy as np 


def plot_Edges(edges=None, nodes=None, surfaces=None, points=None, point=None, figure=None, clear=True, xy=23, multi=1.0, pt_print=False ): 
    
    x = int(xy/10); y=int(xy%10)


    for nd in nodes: 
        nd[1]*=multi 
        nd[2]*=multi 
        nd[3]*=multi 

    border = 0.05

    figure = plt.figure()
    if clear : 
        figure.clear()

    ax = figure.add_subplot(111)
    ax.axis('equal')
    xs =[]; ys=[]
    if not isinstance(edges, type(None)):
        for edge in edges: 
            ix = np.where(nodes[:,0]==edge[0])[0][0]; n1=nodes[ix]
            ix = np.where(nodes[:,0]==edge[1])[0][0]; n2=nodes[ix]
            polygon = plt.Polygon([[n1[x], n1[y]], [n2[x], n2[y]]], color='red', alpha=0.8, lw=0.5, ec='red')
            ax.add_patch(polygon)
            xs.append(n1[x]); ys.append(n1[y])
            xs.append(n2[x]); ys.append(n2[y])

    xs=np.array(xs); ys=np.array(ys)

    if not isinstance(points, type(None)): 
        px=points[:,x]*multi
        py=points[:,y]*multi
        plt.scatter(px, py, c='green', marker='o', edgecolor=None, s=1.0)
        if pt_print: 
            print ("points ")
            print ("xs:", px)
            print ("ys:", py)
        xs=np.concatenate((xs, px))
        ys=np.concatenate((ys, py))
    
    if not isinstance(point, type(None)): 
        px=point[x]
        py=point[y]
        plt.scatter([px], [py], c='black', marker='+', edgecolor='red', s=10.0)
        xs = np.append(xs, px); ys = np.append(ys, py)

        if pt_print: 
            print ("point ")
            print ("x:", px)
            print ("y:", py)

    if not isinstance(surfaces, type(None)):
        xss=[]; yss=[]
        for sf in surfaces: 
            ix = np.where(nodes[:,0]==sf[7])[0][0]; n1=nodes[ix]
            ix = np.where(nodes[:,0]==sf[8])[0][0]; n2=nodes[ix]
            ix = np.where(nodes[:,0]==sf[9])[0][0]; n3=nodes[ix]
            if sf[10] > 0: 
                ix = np.where(nodes[:,0]==sf[10])[0][0]; n4=nodes[ix]
                polygon = plt.Polygon([[n1[x], n1[y]], [n2[x], n2[y]], [n3[x], n3[y]], [n4[x], n4[y]]], \
                    color='lightblue', alpha=0.4, lw=1.0, ec='blue')
            else: 
                polygon = plt.Polygon([[n1[x], n1[y]], [n2[x], n2[y]], [n3[x], n3[y]] ], \
                    color='lightblue', alpha=0.4, lw=1.0, ec='blue')
            ax.add_patch(polygon)
            xss.append(n1[x]); yss.append(n1[y])
            xss.append(n2[x]); yss.append(n2[y])

            xs=np.concatenate((xs, xss))
            ys=np.concatenate((ys, yss))
    
    upX = np.max(xs); downX = np.min(xs)
    upY = np.max(ys); downY = np.min(ys)
    gapx = upX - downX 
    gapy = upY - downY 
    plt.xlim(downX-gapx*border, upX+gapx*border)
    plt.ylim(downY-gapy*border, upY+gapy*border)

    
    plt.show()




if __name__ =="__main__": 

    edges = [   [10000381, 10000330,        1, 10001963] ,
                [10000330, 10000329,        1, 10001962] 
            ]
    nodes = [[10000381, 0, 0, 0], 
            [10000330, 0, 1, 0], 
            [10000329, 0, 0, 1], 

    ]

    plot_Edges(edges, np.array(nodes), points=np.array(nodes))