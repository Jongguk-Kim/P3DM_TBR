import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.mplot3d import axes3d, Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

import numpy as np 
import math 


def LayoutMesh_From_axi(axi="", limit=10000, output="" ):
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

def drawNodes(lnd=None, pnd=None, nodes=None): 

    figure = plt.figure()
    ax = figure.add_subplot(111)
    ax.axis('equal')

    if not isinstance(lnd, type(None)): 
        xs=[]; ys=[]
        for n in lnd: 
            r = math.sqrt(n[1]**2 + n[3]**2)
            xs.append(r)
            ys.append(n[2])

        plt.scatter(np.array(ys), np.array(xs), c='gray', marker="o", s=10, edgecolors=None)

    if not isinstance(pnd, type(None)): 
        xs=[]; ys=[]
        for n in pnd: 
            r = math.sqrt(n[1]**2 + n[3]**2)
            xs.append(r)
            ys.append(n[2])

        plt.scatter(np.array(ys), np.array(xs), c='r', marker=",", s=1)

    if not isinstance(nodes, type(None)): 
        xs=[]; ys=[]
        for n in nodes: 
            r = math.sqrt(n[1]**2 + n[3]**2)
            xs.append(r)
            ys.append(n[2])

        plt.scatter(np.array(ys), np.array(xs), c='b', marker="1", s=10)



    plt.show()


if __name__ == "__main__": 
    
    axi = "D:\\01_ISLM_Scripts\\03_P3DM_TB\\test_mesh\\StandardMesh_inp\\TBR\AL26\\TBR_Pattern_Expansion_verification\\AL26_NewMesh\\255_70\\3003739VT00010-P.axi"
    trd = "D:\\01_ISLM_Scripts\\03_P3DM_TB\\test_mesh\\StandardMesh_inp\\TBR\AL26\\TBR_Pattern_Expansion_verification\\AL26_NewMesh\\255_70\\3003739VT00010-P.trd"
    output = trd[:-3]+"out"

    axi = "Q:\\문서\\ISLM\\Virtual Submission\\ISLM_Manual_RR Difference\\RR 해석 차이\\1030335\Manual_0\\1030335VT00001-0.axi"
    output = axi[:-4]+"-Manual_2D.inp"
    layoutNodes = LayoutMesh_From_axi(axi, output=output, limit=10000)
    # ptnNodes = PatternMesh_from_trd(trd, output=output, limit=100000)
    axi = "Q:\\문서\\ISLM\\Virtual Submission\\ISLM_Manual_RR Difference\\RR 해석 차이\\1030335\ISLM_0\\1030335VT00001-0.axi"
    output = axi[:-4]+"-ISLM_2D.inp"
    layoutNodes1 = LayoutMesh_From_axi(axi, output=output, limit=10000)

    trd = "Q:\\문서\\ISLM\\Virtual Submission\\ISLM_Manual_RR Difference\\RR 해석 차이\\1030335\Manual_0\\1030335VT00001-0.trd"
    output = trd[:-4]+"-Manual_TD.inp"
    ptnNodes1 = PatternMesh_from_trd(trd, output=output, limit=10000)
    trd = "Q:\\문서\\ISLM\\Virtual Submission\\ISLM_Manual_RR Difference\\RR 해석 차이\\1030335\ISLM_0\\1030335VT00001-0.trd"
    output = trd[:-4]+"-ISLM_TD.inp"
    ptnNodes1 = PatternMesh_from_trd(trd, output=output, limit=10000)


    # drawNodes (lnd=layoutNodes1, pnd=layoutNodes)

    # ptnNodes = PatternMesh_from_trd(trd, output=output, limit=10000)

    # drawNodes (lnd=ptnNodes2, pnd=ptnNodes, nodes=layoutNodes)
    # drawNodes (lnd=ptnNodes, nodes=layoutNodes)

