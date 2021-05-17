import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.mplot3d import axes3d, Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

import numpy as np 
import math, sys


def LayoutMesh_From_axi(axi="", limit=10000, output="" ):
    print (" AXI FILE : %s"%(axi))
    with open(axi) as I: 
        lines = I.readlines()
    fp = open(output, 'w')
    fp.write("**************************************\n")
    fp.write("** TIRE MESH from AXI to debug P3DM\n")
    fp.write("**************************************\n")

    SectorNodes = 0;     AllNodes = 0;     Node_Sectors = 0; 
    SectorEls = 0; AllElements = 0; EL_Sectors = 0 

    nodes=[]
    elements=[]

    cmd=None 
    for line in lines: 
        if "**" in line  :
            continue 
        if "*" in line: 

            if "*NODE" in line.upper(): 
                cmd ="ND"
                fp.write("*NODE, SYSTEM=R\n")
            elif "*ELEMENT" in line.upper() and "M3D4" in line.upper(): 
                cmd = 'RB'
                fp.write("*ELEMENT, TYPE=MGAX1\n")
            elif "*ELEMENT" in line.upper() and "C3D6" in line.upper(): 
                cmd = 'C6'
                fp.write("*ELEMENT, TYPE=CGAX3H\n")
            elif "*ELEMENT" in line.upper() and "C3D8" in line.upper(): 
                cmd = 'C8'
                fp.write("*ELEMENT, TYPE=CGAX4H\n")
            elif "*ELSET," in line.upper() and "ELSET=" in line.upper(): 
                cmd = 'ES'
                fp.write(line)
            elif "*SURFACE," in line.upper() and "NAME=PRESS" in line.upper(): 
                cmd = 'PS'
                fp.write(line)
            elif "*SURFACE," in line.upper() and "NAME=RIC_R" in line.upper(): 
                cmd = 'PR'
                fp.write(line)
            elif "*SURFACE," in line.upper() and "NAME=RIC_L" in line.upper(): 
                cmd = 'PL'
                fp.write(line)
            elif "*SURFACE," in line.upper() and "NAME=TIREBODY" in line.upper(): 
                cmd = 'BD'
                fp.write(line)
            elif "*SURFACE," in line.upper() and ("NAME=TIE_M" in line.upper() or ("NAME=" in line.upper() and "_TIE" in line.upper())): 
                cmd = 'TM'
                fp.write(line)
            elif "*SURFACE," in line.upper() and ("NAME=TIE_S" in line.upper() or ("NAME=" in line.upper() and "_TIE" in line.upper())):  
                cmd = 'TS'
                fp.write(line)
            elif "*TIE," in line.upper() : 
                cmd = 'TD'
                fp.write(line)
            elif "NIDOFFSET" in line.upper(): 
                cmd = None 
            else: 
                cmd = None 

            print ("%s, %s"%(line.strip(), cmd))

        

        else: 
            # SectorNodes = 0;     AllNodes = 0;     Node_Sectors = 0; 
            # SectorEls = 0; AllElements = 0; EL_Sectors = 0 

            if cmd=="ND" : 
                data = line.split(",")
                if int(data[0]) < limit: 
                    fp.write("%s, %s, %s, %s\n"%(data[0], data[3].strip(), data[2], data[1]))
                    SectorNodes += 1 
                AllNodes += 1 
                nodes.append([int(data[0].strip()), float(data[1].strip()), float(data[2].strip()), float(data[3].strip())])
            elif cmd =="RB": 
                data = line.split(",")
                if int(data[0]) < limit:
                    fp.write("%s, %s, %s\n"%(data[0], data[1], data[2].strip()))
                    SectorEls+= 1
                AllElements += 1  
                elements.append([int(data[0].strip()), int(data[1].strip()), int(data[2].strip()), int(data[3].strip()), int(data[4].strip()), 0, 0, 0, 0])  
            elif cmd =="C6": 
                data = line.split(",")
                if int(data[0]) < limit:
                    fp.write("%s, %s, %s, %s\n"%(data[0], data[4], data[5].strip(), data[6].strip()))
                    SectorEls+= 1
                AllElements += 1  

                elements.append([int(data[0].strip()), int(data[1].strip()), int(data[2].strip()), int(data[3].strip()), int(data[4].strip()), int(data[5].strip()), int(data[6].strip()), 0, 0])
            elif cmd =="C8": 
                data = line.split(",")
                if int(data[0]) < limit:
                    fp.write("%s, %s, %s, %s, %s\n"%(data[0], data[5], data[6].strip(), data[7].strip(), data[8].strip()))
                    SectorEls+= 1
                AllElements += 1  
                elements.append([int(data[0].strip()), int(data[1].strip()), int(data[2].strip()), int(data[3].strip()), int(data[4].strip()), int(data[5].strip()), int(data[6].strip()), int(data[7].strip()), int(data[8].strip())])
            elif cmd =="ES": 
                data = line.split(",")
                cnt = 0 
                for d in data: 
                    d = d.strip()
                    if d != "": 
                        if int(d) < limit: 
                            cnt += 1
                            fp.write("%s,"%(d))
                if cnt > 0: fp.write("\n")

            elif cmd =="PS": 
                data = line.split(",")
                if int(data[0]) < limit: 
                    if "S3" in data[1]: fp.write("%s, S1\n"%(data[0]))
                    if "S4" in data[1]: fp.write("%s, S2\n"%(data[0]))
                    if "S5" in data[1]: fp.write("%s, S3\n"%(data[0]))
                    if "S6" in data[1]: fp.write("%s, S4\n"%(data[0]))
            elif cmd =="PR": 
                data = line.split(",")
                if int(data[0]) < limit: 
                    if "S3" in data[1]: fp.write("%s, S1\n"%(data[0]))
                    if "S4" in data[1]: fp.write("%s, S2\n"%(data[0]))
                    if "S5" in data[1]: fp.write("%s, S3\n"%(data[0]))
                    if "S6" in data[1]: fp.write("%s, S4\n"%(data[0]))
            elif cmd =="PL": 
                data = line.split(",")
                if int(data[0]) < limit: 
                    if "S3" in data[1]: fp.write("%s, S1\n"%(data[0]))
                    if "S4" in data[1]: fp.write("%s, S2\n"%(data[0]))
                    if "S5" in data[1]: fp.write("%s, S3\n"%(data[0]))
                    if "S6" in data[1]: fp.write("%s, S4\n"%(data[0]))
            elif cmd =="BD": 
                data = line.split(",")
                if int(data[0]) < limit: 
                    if "S3" in data[1]: fp.write("%s, S1\n"%(data[0]))
                    if "S4" in data[1]: fp.write("%s, S2\n"%(data[0]))
                    if "S5" in data[1]: fp.write("%s, S3\n"%(data[0]))
                    if "S6" in data[1]: fp.write("%s, S4\n"%(data[0]))
            elif cmd =="TM": 
                data = line.split(",")
                if int(data[0]) < limit: 
                    if "S3" in data[1]: fp.write("%s, S1\n"%(data[0]))
                    if "S4" in data[1]: fp.write("%s, S2\n"%(data[0]))
                    if "S5" in data[1]: fp.write("%s, S3\n"%(data[0]))
                    if "S6" in data[1]: fp.write("%s, S4\n"%(data[0]))
            elif cmd =="TS": 
                data = line.split(",")
                if int(data[0]) < limit: 
                    if "S3" in data[1]: fp.write("%s, S1\n"%(data[0]))
                    if "S4" in data[1]: fp.write("%s, S2\n"%(data[0]))
                    if "S5" in data[1]: fp.write("%s, S3\n"%(data[0]))
                    if "S6" in data[1]: fp.write("%s, S4\n"%(data[0]))
            elif cmd =="TD": 
                fp.write(line)
            else: 
                continue 
            
    fp.close()

    Node_Sectors = AllNodes / SectorNodes 
    EL_Sectors = AllElements / SectorEls 

    print ("\n ** Sector No. check ")
    print (" All Nodes = %d, Nodes a Sector = %d, Sectors = %.1f"%(AllNodes, SectorNodes, Node_Sectors))
    print (" All ELs   = %d, ELs a Sector   = %d, Sectors = %.1f"%(AllElements, SectorEls, EL_Sectors))

    nodes = np.array(nodes)
    elements = np.array(elements)

    idx = np.where(nodes[:,0]<limit)[0]
    sectornodes = nodes[idx]

    idx = np.where(elements[:,0]<limit)[0]
    s1els = elements[idx]

    sectornodes = nodes 
    return sectornodes 

def PatternMesh_from_trd(axi="", limit=10000, output="", treadNo=10**7 ):
    with open(axi) as I: 
        lines = I.readlines()
    fp = open(output, 'w')
    fp.write("**************************************\n")
    fp.write("** TIRE MESH from AXI to debug P3DM\n")
    fp.write("**************************************\n")

    SectorNodes = 0;     AllNodes = 0;     Node_Sectors = 0; 
    SectorEls = 0; AllElements = 0; EL_Sectors = 0 

    nodes=[]
    elements=[]

    cmd=None 
    for line in lines: 
        if "**" in line  :
            continue 
        if "*" in line: 

            if "*NODE" in line.upper(): 
                cmd ="ND"
                fp.write("*NODE, SYSTEM=R\n")
            elif "*ELEMENT" in line.upper() and "M3D4" in line.upper(): 
                cmd = 'RB'
                fp.write("*ELEMENT, TYPE=MGAX1\n")
            elif "*ELEMENT" in line.upper() and "C3D6" in line.upper(): 
                cmd = 'C6'
                fp.write("*ELEMENT, TYPE=CGAX3H\n")
            elif "*ELEMENT" in line.upper() and "C3D8" in line.upper(): 
                cmd = 'C8'
                fp.write("*ELEMENT, TYPE=CGAX4H\n")
            elif "*ELSET," in line.upper() and "ELSET=" in line.upper(): 
                cmd = 'ES'
                fp.write(line)
            elif "*SURFACE," in line.upper() and "NAME=XTRD" in line.upper(): 
                cmd = 'PS'
                fp.write(line)
            elif "*SURFACE," in line.upper() and "NAME=YTIE" in line.upper(): 
                cmd = 'PR'
                fp.write(line)
            elif "*SURFACE," in line.upper() and "NAME=CONT" in line.upper(): 
                cmd = 'PL'
                fp.write(line)
            elif "*SURFACE," in line.upper() and "NAME=TIREBODY" in line.upper(): 
                cmd = 'BD'
                fp.write(line)
            elif "*SURFACE," in line.upper() and ("NAME=TIE_M" in line.upper() or ("NAME=" in line.upper() and "_TIE" in line.upper())): 
                cmd = 'TM'
                fp.write(line)
            elif "*SURFACE," in line.upper() and ("NAME=TIE_S" in line.upper() or ("NAME=" in line.upper() and "_TIE" in line.upper())):  
                cmd = 'TS'
                fp.write(line)
            elif "*TIE," in line.upper() : 
                cmd = 'TD'
                fp.write(line)
            elif "NIDOFFSET" in line.upper(): 
                cmd = None 
            elif "TREADPTN_NIDSTART_NIDOFFSET_EIDSTART_EIDOFFSET" in line.upper(): 
                cmd = None
                data = line.split("=")[1]
                limit = data.split(",")[1]
                limit = int(limit)
                treadNo = int(data.split(",")[0])
            else: 
                cmd = None 

            print ("%s, %s"%(line.strip(), cmd))

        

        else: 
            # SectorNodes = 0;     AllNodes = 0;     Node_Sectors = 0; 
            # SectorEls = 0; AllElements = 0; EL_Sectors = 0 

            if cmd=="ND" : 
                data = line.split(",")
                if int(data[0]) < limit+treadNo: 
                    fp.write("%s, %s, %s, %s\n"%(data[0], data[3].strip(), data[2], data[1].strip()))
                    SectorNodes += 1 
                AllNodes += 1 
                nodes.append([int(data[0].strip()), float(data[1].strip()), float(data[2].strip()), float(data[3].strip())])
            elif cmd =="RB": 
                data = line.split(",")
                if int(data[0]) < limit+treadNo:
                    fp.write("%s, %s, %s\n"%(data[0], data[1], data[2].strip()))
                    SectorEls+= 1
                AllElements += 1  
                elements.append([int(data[0].strip()), int(data[1].strip()), int(data[2].strip()), int(data[3].strip()), int(data[4].strip()), 0, 0, 0, 0])  
            elif cmd =="C6": 
                data = line.split(",")
                if int(data[0]) < limit+treadNo:
                    fp.write("%s, %s, %s, %s\n"%(data[0], data[4], data[5].strip(), data[6].strip()))
                    SectorEls+= 1
                AllElements += 1  

                elements.append([int(data[0].strip()), int(data[1].strip()), int(data[2].strip()), int(data[3].strip()), int(data[4].strip()), int(data[5].strip()), int(data[6].strip()), 0, 0])
            elif cmd =="C8": 
                data = line.split(",")
                if int(data[0]) < limit+treadNo:
                    fp.write("%s, %s, %s, %s, %s\n"%(data[0], data[5], data[6].strip(), data[7].strip(), data[8].strip()))
                    SectorEls+= 1
                AllElements += 1  
                elements.append([int(data[0].strip()), int(data[1].strip()), int(data[2].strip()), int(data[3].strip()), int(data[4].strip()), int(data[5].strip()), int(data[6].strip()), int(data[7].strip()), int(data[8].strip())])
            elif cmd =="ES": 
                data = line.split(",")
                cnt = 0 
                for d in data: 
                    d = d.strip()
                    if d !='': 
                        if int(d) < limit+treadNo: 
                            cnt += 1
                            fp.write("%s,"%(d))
                if cnt > 0: fp.write("\n")

            elif cmd =="PS": 
                data = line.split(",")
                if int(data[0]) < limit+treadNo: 
                    if "S3" in data[1]: fp.write("%s, S1\n"%(data[0]))
                    if "S4" in data[1]: fp.write("%s, S2\n"%(data[0]))
                    if "S5" in data[1]: fp.write("%s, S3\n"%(data[0]))
                    if "S6" in data[1]: fp.write("%s, S4\n"%(data[0]))
            elif cmd =="PR": 
                data = line.split(",")
                if int(data[0]) < limit+treadNo: 
                    if "S3" in data[1]: fp.write("%s, S1\n"%(data[0]))
                    if "S4" in data[1]: fp.write("%s, S2\n"%(data[0]))
                    if "S5" in data[1]: fp.write("%s, S3\n"%(data[0]))
                    if "S6" in data[1]: fp.write("%s, S4\n"%(data[0]))
            elif cmd =="PL": 
                data = line.split(",")
                if int(data[0]) < limit+treadNo: 
                    if "S3" in data[1]: fp.write("%s, S1\n"%(data[0]))
                    if "S4" in data[1]: fp.write("%s, S2\n"%(data[0]))
                    if "S5" in data[1]: fp.write("%s, S3\n"%(data[0]))
                    if "S6" in data[1]: fp.write("%s, S4\n"%(data[0]))
            elif cmd =="BD": 
                data = line.split(",")
                if int(data[0]) < limit+treadNo: 
                    if "S3" in data[1]: fp.write("%s, S1\n"%(data[0]))
                    if "S4" in data[1]: fp.write("%s, S2\n"%(data[0]))
                    if "S5" in data[1]: fp.write("%s, S3\n"%(data[0]))
                    if "S6" in data[1]: fp.write("%s, S4\n"%(data[0]))
            elif cmd =="TM": 
                data = line.split(",")
                if int(data[0]) < limit+treadNo: 
                    if "S3" in data[1]: fp.write("%s, S1\n"%(data[0]))
                    if "S4" in data[1]: fp.write("%s, S2\n"%(data[0]))
                    if "S5" in data[1]: fp.write("%s, S3\n"%(data[0]))
                    if "S6" in data[1]: fp.write("%s, S4\n"%(data[0]))
            elif cmd =="TS": 
                data = line.split(",")
                if int(data[0]) < limit+treadNo: 
                    if "S3" in data[1]: fp.write("%s, S1\n"%(data[0]))
                    if "S4" in data[1]: fp.write("%s, S2\n"%(data[0]))
                    if "S5" in data[1]: fp.write("%s, S3\n"%(data[0]))
                    if "S6" in data[1]: fp.write("%s, S4\n"%(data[0]))
            elif cmd =="TD": 
                fp.write(line)
            
            else: 
                continue 
            
    fp.close()

    Node_Sectors = AllNodes / SectorNodes 
    EL_Sectors = AllElements / SectorEls 

    print ("\n ** Sector No. check ")
    print (" All Nodes = %d, Nodes a Sector = %d, Sectors = %.1f"%(AllNodes, SectorNodes, Node_Sectors))
    print (" All ELs   = %d, ELs a Sector   = %d, Sectors = %.1f"%(AllElements, SectorEls, EL_Sectors))

    nodes = np.array(nodes)
    elements = np.array(elements)

    idx = np.where(nodes[:,0]<limit+treadNo)[0]
    s1nodes = nodes[idx]

    idx = np.where(elements[:,0]<limit+treadNo)[0]
    s1els = elements[idx]

    ix = np.where(nodes[:,0]<limit+treadNo)[0]
    pitchnodes = nodes[ix]

    # figure = plt.figure()
    # ax = Axes3D(figure)
    
    # # ix2 = np.where(nodes[ix,1]<0)[0]
    # # ix = np.intersect1d(ix, ix2)
    # Xs=nodes[ix,1]
    # Ys=nodes[ix,2]
    # Zs=nodes[ix,3]
    # ax.scatter(Xs, Ys, Zs, c='b', marker='o')

    # # for n in ix: 
    # #     ax.text(nodes[n][1], nodes[n][2], nodes[n][3], str(int(nodes[n][0]-10**7)), color='b', size=8)

    # # Xs = points[:,0]
    # # Ys = points[:,1]
    # # Zs = points[:,2]
    # # ax.scatter(Xs, Ys, Zs, c='gray', marker='*')

    # plt.show()

    pitchnodes = nodes 
    return pitchnodes 

def drawNodes(lnd=None, pnd=None, nodes=None, xy=23, D3=0): 

    x = int(xy/10)
    y = int(xy%10)
    if (x ==2 and y ==3) or (x ==3 and y ==2): z =1 
    elif (x ==1 and y ==3) or (x ==3 and y ==1): z =2 
    else: z = 3 

    figure = plt.figure()
    ax = figure.add_subplot(111)
    ax.axis('equal')

    if D3 ==0: 

        if not isinstance(lnd, type(None)): 
            xs=[]; ys=[]
            for n in lnd: 
                r = math.sqrt(n[y]**2 + n[z]**2)
                xs.append(r)
                ys.append(n[x])

            plt.scatter(np.array(ys), np.array(xs), c='gray', marker="o", s=10, edgecolors=None)

        if not isinstance(pnd, type(None)): 
            xs=[]; ys=[]
            for n in pnd: 
                r = math.sqrt(n[y]**2 + n[z]**2)
                xs.append(r)
                ys.append(n[x])

            plt.scatter(np.array(ys), np.array(xs), c='r', marker=",", s=1)

        if not isinstance(nodes, type(None)): 
            xs=[]; ys=[]
            for n in nodes: 
                r = math.sqrt(n[y]**2 + n[z]**2)
                xs.append(r)
                ys.append(n[x])

            plt.scatter(np.array(ys), np.array(xs), c='b', marker="1", s=10)
    else: 
        if not isinstance(lnd, type(None)): 
            xs=[]; ys=[]
            for n in lnd: 
                xs.append(n[x])
                ys.append(n[y])

            plt.scatter(np.array(ys), np.array(xs), c='gray', marker="o", s=10, edgecolors=None)

        if not isinstance(pnd, type(None)): 
            xs=[]; ys=[]
            for n in pnd: 
                xs.append(n[x])
                ys.append(n[y])

            plt.scatter(np.array(ys), np.array(xs), c='r', marker=",", s=1)

        if not isinstance(nodes, type(None)): 
            xs=[]; ys=[]
            for n in nodes: 
                xs.append(n[x])
                ys.append(n[y])

            plt.scatter(np.array(ys), np.array(xs), c='b', marker="1", s=10)



    plt.show()


def Comparing(m1='', m2='', out=''): 
    M1, N1, ES1, SF1 = readModel(m1)
    M2, N2, ES2, SF2 = readModel(m2)

    M1E4=M1[0]; M1E6=M1[1]; M1E8=M1[2]
    M2E4=M2[0]; M2E6=M2[1]; M2E8=M2[2]

    err= open(out, 'w')
    skip =1 
    if skip ==1: 
        for m in M1E4: 
            ix = np.where(M2E4[:,0]==m[0])[0]
            if len(ix) > 1 : 
                for x in ix: 
                    err.write("MULT %s // %s\n"%(str(m), str(M2E4[x])))
            elif len(ix) ==0: 
                err.write("NONE %s - \n"%(str(m)))
            else: 
                x = ix[0]
                if m[1] == M2E4[x][1] and m[2] == M2E4[x][2] and m[3] == M2E4[x][3] and m[4] == M2E4[x][4] : 
                    continue 
                else: 
                    err.write("  E4 %10d, %10d/%10d, %10d/%10d, %10d/%10d, %10d/%10d\n"%(m[0], m[1], M2E4[x][1], m[2], M2E4[x][2], m[3], M2E4[x][3], m[4], M2E4[x][4]))
        
        for m in M1E6: 
            ix = np.where(M2E6[:,0]==m[0])[0]
            if len(ix) > 1 : 
                for x in ix: 
                    err.write("MULT %s // %s\n"%(str(m), str(M2E6[x])))
            elif len(ix) ==0: 
                err.write("NONE %s - \n"%(str(m)))
            else: 
                x = ix[0]
                if m[1] == M2E6[x][1] and m[2] == M2E6[x][2] and m[3] == M2E6[x][3] and m[4] == M2E6[x][4] and m[5] == M2E6[x][5] and m[6] == M2E6[x][6]: 
                    continue 
                else: 
                    err.write("  E6 %10d, %10d/%10d, %10d/%10d, %10d/%10d, %10d/%10d, %10d/%10d, %10d/%10d\n"%(m[0], m[1], M2E6[x][1], m[2], M2E6[x][2], m[3], M2E6[x][3], m[4], M2E6[x][4], m[5], M2E6[x][5], m[6], M2E6[x][6]))

        for m in M1E8: 
            ix = np.where(M2E8[:,0]==m[0])[0]
            if len(ix) > 1 : 
                for x in ix: 
                    err.write("MULT %s // %s\n"%(str(m), str(M2E8[x])))
            elif len(ix) ==0: 
                err.write("NONE %s - \n"%(str(m)))
            else: 
                x = ix[0]
                if m[1] == M2E8[x][1] and m[2] == M2E8[x][2] and m[3] == M2E8[x][3] and m[4] == M2E8[x][4] and m[5] == M2E8[x][5] and m[6] == M2E8[x][6] and m[7] == M2E8[x][7] and m[8] == M2E8[x][8]: 
                    continue  
                else: 
                    err.write("  E8 %10d, %10d/%10d, %10d/%10d, %10d/%10d, %10d/%10d, %10d/%10d, %10d/%10d, %10d/%10d, %10d/%10d\n"%(m[0], m[1], M2E8[x][1], m[2], M2E8[x][2], m[3], M2E8[x][3], m[4], M2E8[x][4], m[5], M2E8[x][5], m[6], M2E8[x][6], m[7], M2E8[x][7], m[8], M2E8[x][8]))
        

        for n in N1: 
            ix = np.where(N2[:, 0]==n[0])[0]
            if len(ix) > 1: 
                for x in ix: 
                    err.write("NODE %s // %s\n"%(str(n), str(N2[x])))
            elif len(ix) ==0: 
                err.write("NODE %s // NONE\n"%(str(n)))
            else: 
                x = ix[0]
                if round(n[1], 5) == round(N2[x][1], 5) and  round(n[2], 5) == round(N2[x][2], 5) and  round(n[3], 5) == round(N2[x][3], 5): 
                    continue 
                else: 
                    err.write("  ND %10d, %10.6f/%10.6f, %10.6f/%10.6f, %10.6f/%10.6f\n"%(n[0], n[1], N2[x][1], n[2], N2[x][2], n[3], N2[x][3]))

        
        for es1 in ES1: 
            for es2 in ES2: 
                if es1[0] == es2[0]: 
                    e1 = np.array(es1[1]); e2 = np.array(es2[1])
                    for e in e1: 
                        ix = np.where(e2[:]==e)[0]
                        if len(ix) > 1: 
                            err.write("  ES %4s, %d, E2 %dEA \n"%(es1[0], e, len(ix)))
                        elif len(ix) ==0: 
                            err.write("  ES %4s, %d, 0 EA \n"%(es1[0], e))
                        else: 
                            continue 


    cnt = 0                         
    for BS1, BS2 in zip(SF1, SF2): 
        print ("SURFACE Comparison")
        cnt += 1 
        for sf1 in BS1: 
            for sf2 in BS2: 
                try: 
                    if sf1[0] == sf2[0]: 
                        s1 = np.array(sf1[1]); s2 = np.array(sf2[1]) 
                        for s in s1: 
                            ix1 = np.where(s2[:,0]==s[0])[0]
                            ix2 = np.where(s2[:,1]==s[1])[0]
                            ix = np.intersect1d(ix1, ix2)
                            if 'trd' in out: 
                                if cnt ==1:  sfname = 'XTRD1001'
                                elif cnt ==2: sfname = 'CONT' 
                                elif cnt ==2: sfname = 'YTIE1001' 
                            else: 
                                if cnt ==1:  sfname = 'TIREBODY'
                                elif cnt ==2: sfname = 'PRESS' 
                                elif cnt ==2: sfname = 'RIC' 
                                    

                            if len(ix) > 1: 
                                err.write("%10d - dup %s surface\n"%(s[0], sfname))
                            elif len(ix) ==0: 
                                err.write("%10d - no %s surface\n"%(s[0], sfname))
                            else: 
                                x = ix[0]
                                if s[1] != s2[x][1]: 
                                    err.write("%10d, S%d/S%d\n"%(s[0], s[1], s2[x][1]))
                except: 
                    print ("SF1", sf1)
                    print ("SF2", sf2)

    
    err.close()


def readModel(f):

    with open(f) as m: 
        lines = m.readlines()
    
    E4=[]; E6=[]; E8=[]; ND=[]; ESET=[]
    S_BD=[]; S_PR=[]; S_RC=[]
    cmd = None 
    for line in lines: 
        if "**" in line: continue 
        if '*' in line : 
            if "*ELEMENT" in line.upper() and "M3D4" in line.upper():           cmd = 'e4'
            elif "*ELEMENT" in line.upper() and "C3D6" in line.upper():           cmd = 'e6'
            elif "*ELEMENT" in line.upper() and "C3D8" in line.upper():           cmd = 'e8'
            elif "*NODE" in line.upper(): cmd = 'nd'
            elif "ELSET" in line.upper(): 
                cmd = 'es'
                words = line.split(",")
                for word in words: 
                    if not "*" in word and 'ELSET' in line: 
                        ws = word.split("=")
                        TMP = [ws[1].strip().upper()]
                mem =[]
                ESET.append([TMP, mem])
            elif "*SURFACE" in line.upper() and ("TIREBODY" in line.upper() or "XTRD1001" in line.upper() ): 
                cmd = 's_bd'
                words = line.split(",")
                for word in words: 
                    if "=" in word and 'NAME' in line: 
                        ws = word.split("=")
                        TMP = [ws[1].strip().upper()]
                mem =[]
                S_BD.append([TMP, mem])
            elif "*SURFACE" in line.upper() and ("PRESS" in line.upper() or "CONT" in line.upper() ): 
                cmd = 's_pr'
                words = line.split(",")
                for word in words: 
                    if "=" in word and 'NAME' in line: 
                        ws = word.split("=")
                        TMP = [ws[1].strip().upper()]
                mem =[]
                S_PR.append([TMP, mem])
            elif "*SURFACE" in line.upper() and ("RIC" in line.upper() or "YTIE1001" in line.upper() ): 
                cmd = 's_rc'
                words = line.split(",")
                for word in words: 
                    if "=" in word and 'NAME' in line: 
                        ws = word.split("=")
                        TMP = [ws[1].strip().upper()]
                mem =[]
                S_RC.append([TMP, mem])
            else: cmd = None

        else: 
            if cmd == 'nd': 
                words = line.split(",")
                ND.append([int(words[0].strip()), float(words[1].strip()), float(words[2].strip()), float(words[3].strip())])
            if cmd =='e4': 
                words = line.split(",")
                E4.append([int(words[0].strip()), int(words[1].strip()), int(words[2].strip()), int(words[3].strip()), int(words[4].strip())])
            if cmd =='e6': 
                words = line.split(",")
                E6.append([int(words[0].strip()), int(words[1].strip()), int(words[2].strip()), int(words[3].strip()), int(words[4].strip()), int(words[5].strip()), int(words[6].strip())])
            if cmd =='e8': 
                words = line.split(",")
                E8.append([int(words[0].strip()), int(words[1].strip()), int(words[2].strip()), int(words[3].strip()), int(words[4].strip()), int(words[5].strip()), int(words[6].strip()), int(words[7].strip()), int(words[8].strip())])
            if cmd == 'es': 
                words = line.split(",")
                for w in words: 
                    w = w.strip()
                    if w!='' and w !='\n': 
                        ESET[-1][1].append(int(w))
            if cmd == 's_bd': 
                ws = line.split(",")
                S_BD[-1][1].append([int(ws[0].strip()), int(ws[1][2])])
            if cmd == 's_pr': 
                ws = line.split(",")
                S_PR[-1][1].append([int(ws[0].strip()), int(ws[1][2])])
            if cmd == 's_rc': 
                ws = line.split(",")
                S_RC[-1][1].append([int(ws[0].strip()), int(ws[1][2])])


    ELS=[np.array(E4), np.array(E6), np.array(E8)]
    SF=[S_BD, S_PR, S_RC]

    return ELS, np.array(ND), ESET, SF

if __name__ == "__main__": 
    
    axi = "D:\\01_ISLM_Scripts\\03_P3DM_TB\\test_mesh\\StandardMesh_inp\\TBR\AL26\\TBR_Pattern_Expansion_verification\\AL26_NewMesh\\255_70\\3003739VT00010-P.axi"
    trd = "D:\\01_ISLM_Scripts\\03_P3DM_TB\\test_mesh\\StandardMesh_inp\\TBR\AL26\\TBR_Pattern_Expansion_verification\\AL26_NewMesh\\255_70\\3003739VT00010-P.trd"
    output = trd[:-3]+"out"

    axi = "D:\\01_ISLM_Scripts\\10_StandardMesh\\temp_inp\\1030335VT00001-manual.axi"
    axi1 = "D:\\01_ISLM_Scripts\\10_StandardMesh\\temp_inp\\1030335VT00001-islm.axi"

    trd = "D:\\01_ISLM_Scripts\\10_StandardMesh\\temp_inp\\1030335VT00001-manual.trd"
    trd1 = "D:\\01_ISLM_Scripts\\10_StandardMesh\\temp_inp\\1030335VT00001-islm.trd"

    limit = 10000

    # trd = "D:\\01_ISLM_Scripts\\10_StandardMesh\\temp_inp\\1030335VT00001-manual.trd"
    # output = trd[:-4]+"-Manual_TD.inp"
    # nodes1 = PatternMesh_from_trd(trd, output=output, limit=limit)
    # trd = "D:\\01_ISLM_Scripts\\10_StandardMesh\\temp_inp\\1030335VT00001-islm.trd"
    # output = trd[:-4]+"-ISLM_TD.inp"
    # nodes2 = PatternMesh_from_trd(trd, output=output, limit=limit)

    trd = "D:\\01_ISLM_Scripts\\03_P3DM_TB\\test_mesh\\expanded_pattern\\1022896VT00004-0.trd"
    output = trd[:-4]+"-P3DM_TD.inp"
    nodes2 = PatternMesh_from_trd(trd, output=output, limit=limit)
    axi = "D:\\01_ISLM_Scripts\\03_P3DM_TB\\test_mesh\\expanded_pattern\\1022896VT00004-0.axi"
    output = axi[:-4]+"-P3DM_BD.inp"
    nodes2 = LayoutMesh_From_axi(axi, output=output, limit=limit)

    sys.exit()
    draw=0
    if draw ==1: 
        axi = "D:\\01_ISLM_Scripts\\10_StandardMesh\\temp_inp\\1030335VT00001-manual.axi"
        output = axi[:-4]+"-Manual_2D.inp"
        nodes1 = LayoutMesh_From_axi(axi, output=output, limit=limit)
        # nodes1 = PatternMesh_from_trd(trd, output=output, limit=limit)
        axi = "D:\\01_ISLM_Scripts\\10_StandardMesh\\temp_inp\\1030335VT00001-islm.axi"
        output = axi[:-4]+"-ISLM_2D.inp"
        nodes2 = LayoutMesh_From_axi(axi, output=output, limit=limit)
        # nodes2 = PatternMesh_from_trd(trd, output=output, limit=limit)

        nd1 = np.array(nodes1)
        nd2 = np.array(nodes2)

        limit = 2*10**7
        idx = np.where(nd1[:,0]<limit)
        nd1 = nd1[idx]

        idx = np.where(nd2[:,0]<limit)
        nd2 = nd2[idx]


        drawNodes(D3=1, lnd=nd1, pnd=nd2, xy=13)
        drawNodes(D3=1, lnd=nd1, pnd=nd2, xy=23)
        drawNodes(D3=1, lnd=nd1, pnd=nd2, xy=12)

    comparing=1
    if comparing ==1: 
        # Comparing(axi, axi1, 'axi.txt')
        Comparing(trd, trd1, 'trd.txt')


    
    node=0

    if node ==1: 
        cnt = 0 
        
        mg = 0.0001
        c0=0; c1=0; c2=0

        
        for n in nd1: 
            if int(cnt % 100) == 0: 
                print (" %d : No match=%d, 1 match=%d, over2=%d"%(n[0], c0, c1, c2))
            cnt += 1

            ix1 = np.where(nd2[:,1]>n[1]-mg)[0]
            ix2 = np.where(nd2[:,1]<n[1]+mg)[0]
            ix = np.intersect1d(ix1, ix2)

            ix1 = np.where(nd2[:,2]>n[2]-mg)[0]
            ix2 = np.where(nd2[:,2]<n[2]+mg)[0]
            iy = np.intersect1d(ix1, ix2)

            ix1 = np.where(nd2[:,3]>n[3]-mg)[0]
            ix2 = np.where(nd2[:,3]<n[3]+mg)[0]
            iz = np.intersect1d(ix1, ix2)

            idx = np.intersect1d(ix, iy)
            idx = np.intersect1d(idx, iz)

            if len(idx) == 0: c0+=1
            elif len(idx) == 1: c1+=1
            else: c2 += 1

        print (" total nodes=%d"%(len(nd1)))

        print (" No match=%d, 1 match=%d, over2=%d"%(c0, c1, c2))

    







    trd = "D:\\01_ISLM_Scripts\\10_StandardMesh\\temp_inp\\1030335VT00001-manual.trd"
    output = trd[:-4]+"-Manual_TD.inp"
    ptnNodes = PatternMesh_from_trd(trd, output=output, limit=limit)
    trd = "D:\\01_ISLM_Scripts\\10_StandardMesh\\temp_inp\\1030335VT00001-islm.trd"
    output = trd[:-4]+"-ISLM_TD.inp"
    ptnNodes1 = PatternMesh_from_trd(trd, output=output, limit=limit)

    

    # drawNodes (lnd=layoutNodes1, pnd=layoutNodes)

    # ptnNodes = PatternMesh_from_trd(trd, output=output, limit=limit)

    # drawNodes (lnd=ptnNodes2, pnd=ptnNodes, nodes=layoutNodes)
    # drawNodes (lnd=ptnNodes, nodes=layoutNodes)

