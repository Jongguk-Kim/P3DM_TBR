
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.mplot3d import axes3d, Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import numpy as np 
import time 
def timer(func): 
    def wrapper(*args, **kwargs): 
        start = time.time()
        rv = func(*args, **kwargs)
        total = time.time() - start
        print (" Time: %.2f"%(total))
        return rv 
    return wrapper 


def plot_Edges(edges=None, edgepoint=False, nodes=None, surfaces=None, points=None, point=None, ifigure=None, clear=True, xy=23, multi=1.0, pt_print=False ): 
    
    x = int(xy/10); y=int(xy%10)


    for nd in nodes: 
        nd[1]*=multi 
        nd[2]*=multi 
        nd[3]*=multi 

    border = 0.05

    t_figure = plt.figure()
    if clear : 
        t_figure.clear()

    t_ax = t_figure.add_subplot(111)
    t_ax.axis('equal')
    xs =[]; ys=[]
    if not isinstance(edges, type(None)):
        for edge in edges: 
            ix = np.where(nodes[:,0]==edge[0])[0][0]; n1=nodes[ix]
            ix = np.where(nodes[:,0]==edge[1])[0][0]; n2=nodes[ix]
            # polygon = plt.Polygon([[n1[x], n1[y]], [n2[x], n2[y]]], color='red', alpha=0.8, lw=1.0)
            # t_ax.add_patch(polygon)
            
            xs.append(n1[x]); ys.append(n1[y])
            xs.append(n2[x]); ys.append(n2[y])
        plt.plot(xs, ys, color='red', marker='o')
        if edgepoint: 
            plt.scatter(xs, ys, c='black', marker='+', edgecolor=None, s=4.0)


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
                    color='lightblue', alpha=0.4, lw=0.5, ec='blue')
            else: 
                polygon = plt.Polygon([[n1[x], n1[y]], [n2[x], n2[y]], [n3[x], n3[y]] ], \
                    color='lightblue', alpha=0.4, lw=0.5, ec='blue')
            t_ax.add_patch(polygon)
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

def meshgrid_in_Quadrilateral(xs, ys, num=10, endpoint=True, vs=None): 
    # xs=[x1, x2, x3, x4]; ys=[y1, y2, y3, y4]
    s = np.linspace(-1, 1, num)
    t = np.linspace(-1, 1, num)
    if not endpoint: 
        s = np.delete(s, 0, axis=0); s=np.delete(s, -1, axis=0)
        t = np.delete(s, 0, axis=0); t=np.delete(s, -1, axis=0)
    if isinstance(vs, type(None)): 
        px=[]; py=[]
        for m in s: 
            tx=[]; ty=[]
            for n in t: 
                tx.append( 0.25*((1-m)*(1-n)*xs[0] + (1+m)*(1-n)*xs[1] + (1+m)*(1+n)*xs[2] + (1-m)*(1+n)*xs[3]) )
                ty.append( 0.25*((1-m)*(1-n)*ys[0] + (1+m)*(1-n)*ys[1] + (1+m)*(1+n)*ys[2] + (1-m)*(1+n)*ys[3]) )
            px.append(tx)
            py.append(ty)

        return np.array(px), np.array(py)
    else: 
        px=[]; py=[]; vy=[]
        for m in s: 
            tx=[]; ty=[]; tv=[]
            for n in t: 
                tx.append( 0.25*((1-m)*(1-n)*xs[0] + (1+m)*(1-n)*xs[1] + (1+m)*(1+n)*xs[2] + (1-m)*(1+n)*xs[3]) )
                ty.append( 0.25*((1-m)*(1-n)*ys[0] + (1+m)*(1-n)*ys[1] + (1+m)*(1+n)*ys[2] + (1-m)*(1+n)*ys[3]) )
                tv.append( 0.25*((1-m)*(1-n)*vs[0] + (1+m)*(1-n)*vs[1] + (1+m)*(1+n)*vs[2] + (1-m)*(1+n)*vs[3]) )
            px.append(tx)
            py.append(ty)
            vy.append(tv)

        return np.array(px), np.array(py), np.array(vy)
    

def add_contour(x, y, z, cmap='Reds', fill=True): 
    if fill: cp = plt.contourf(x, y, z, cmap=cmap)
    else: cp = plt.contour(x, y, z, cmap=cmap)
    return cp 

@timer 
def contourplotting(): 
    
    ## contour graph는 mesh grid 형태로 x, y 좌표를 넘겨줘야함 
    ## plt.contour(x, y, z) ## x, y, z는 모두 2차원 np.array여야함
    ## 이때 x,y는 mesh grid형태의 좌표값으로 넘겨줘야함
    ## x, y = np.meshgrid([1,2,3], [1,2])
    ## x : 행이 반복, y는 열이 반복 
    # plt.figure()
    # i = 1; j=2
    # x, y = np.meshgrid(np.linspace(i, i+1, 10), np.linspace(j, j+1, 10))
    # z = np.sqrt(x**2 + y**2)
    # cp = plt.contourf(x, y, z)
    # plt.colorbar(cp)
    # plt.show()

  
    N = 4 
    num = 5
    for i in range(100): 
        for j in range(15): 
            xs = [i, i+1, i+1, i] 
            ys = [j, j, j+1, j+1]
            vs =[i+j, i*j, i**2+j, i+j**2]
            px, py, pv = meshgrid_in_Quadrilateral(xs, ys, num=num, vs=vs)
            cp = add_contour(px, py, pv, cmap="rainbow")
    # plt.show()


if __name__ =="__main__": 

    edges = [   [10000381, 10000330,        1, 10001963] ,
                [10000330, 10000329,        1, 10001962] 
            ]
    nodes = [[10000381, 0, 0, 0], 
            [10000330, 0, 1, 0], 
            [10000329, 0, 0, 1], 

    ]

    # plot_Edges(edges, nodes=np.array(nodes), points=np.array(nodes))
    contourplotting()

    
    