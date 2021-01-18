# import matplotlib as mpl
# mpl.use('Agg')
import numpy as np

from math import *

import os, sys, time, json

import matplotlib.pyplot as plt
import subprocess

from numpy.lib.arraysetops import intersect1d 

import paramiko as FTP 
import PTN_LIBRARY.ptn_library as PTN 

PI = 3.14159265358979323846

TireRubberComponents = [
    # 'BEAD_R', 'BEAD_L', # 'BD1' ,  Bead
    'BD1', 
    'BEC' , # Belt Edge Cushion
    'BSW' , # Black SideWall Component
    'BTT' , # Belt rubber component (associated with BT components)
    'CCT' , # Carcass rubber component (associated with C components)
    'SCT' , 
    'NCT' ,
    'CHS' ,
    'CTB' , 'CTR', 'CTB1' , 'CTR1',# Tread Componet
    'ET'  , # Edge Tape
    'FIL' , 'BDF', # Bead Filler
    'HUS' , # Hump Strip
    'JBT' , # Rubber associated with JFC, JEC components
    'L11' , 'IL1', # Inner liner component
    'L12' , 'IL2', # #2 Innerliner
    'LBF' , # Lower Bead Filler
    'UBF' , # Upper Bead Filler
    'RIC' , # Rim Cushion
    'SIR' , # Sidewall Insert Rubber
    'SHW' , # Shoulder Wedge
    'SRTT', # Associated with PK1, PK2, RFM and FLI components
    'SUT' , 'UTR', 'SUT1' , 'UTR1',# SubTread
    'TRW' , # Tread Wing
    
    'WSW'  # While Sidewall
]
TireTreadComponents = [
    'CTB' , 'CTR',
    'SUT' , 'UTR',
    'TRW'
]
TireCordComponents = [
    'C01'  , 'CC1', # Carcass Cord 1 
    'C02'  , 'CC2', # Carcass Cord 2
    'C03'  , 'CC3', # Carcass Cord 3 
    'C04'  , 'CC4', # Carcass Cord 4
    'BT1'  , # Belt 1 
    'BT2'  , # Belt 2
    'BT3'  , # Belt 3
    'BT4'  , # Belt 4
    'JFC1' , 'JFC', # Jointless Full Cap 1
    'JFC2' , # Jointless Full Cap 2
    'JEC1' , 'JEC', # Jointless Edge Cap 1
    'OJEC1', # Overlapped Jointless Edge Cap
    'OJFC1', # Overlapped Jointless Full Cap
    'PK1'  , # Half Bead Packing
    'PK2'  , # Full Bead Packing
    'RFM'  , # Bead S(RFM)
    'FLI'  , # Bead Flipper
    'CH1'  , 'CH1_R', 'CH1_L',  # Steel Chafer 
    'CH2'  , 'CH2_R', 'CH2_L',  # 1st Nylon Chafer
    'CH3'  , 'CH3_R', 'CH3_L',  # 2nd Nylon Chafer
    'NCF'  , 'SCF'  , 'NF1'  , 'NF2',
    'BDC'  , # bead cover 
    'SPC'    ## spiral coil
    #'SWS'    # temporary component for Endurance simulation 
]

def GetCarcassDrumDia(group="PCR", inch=16.0, overtype=''): 
    if group != 'TBR':
        lstCDD = [[12.,337.],[13.,310.],[14.,335.],[15.,360.],[16.,385.],[17.,417.],[18.,442.],[19.,465.],[20.,490.],[21.,516.],[22.,542.],[23.,567.],[24.,592.],[26.,643.],[28.,694.]]
        for cdd in lstCDD:
            if cdd[0] == inch: 
                return cdd[1]
    else: 
        if overtype == 'SOT': 
            lstCDD = [[16.0,377.2],[17.5,407.4],[19.5,458.4],[20.0,483.8],[22.5,528.4],[24.5,576.1]]
        else:
            lstCDD = [[15.0,440.],[16.0,460.],[17.5,529.4],[18.0,526.],[20.0,571.5],[22.0,640.],[22.5,660.4],[24.0,686.],[24.5,711.2]]
        CcDia = 0 
        for cdd in lstCDD:
            if cdd[0] == inch: 
                return cdd[1]
        if CcDia ==0: 
            lstCDD = [[15.0,440.],[16.0,460.],[17.5,529.4],[18.0,526.],[20.0,571.5],[22.0,640.],[22.5,660.4],[24.0,686.],[24.5,711.2]]
            for cdd in lstCDD:
                if cdd[0] == inch: 
                    return cdd[1]

def GetCarcassDia (group="PCR", inch=16.0, layer=1, overtype='', ga=1.0, innerGa=0.0, centerMinR=0):
    cdd = GetCarcassDrumDia(group=group, inch=inch, overtype=overtype)
    ccr = cdd/2 
    CcDia = (ccr + ga*(layer-0.5) + innerGa * (centerMinR/ccr))*2.0
    # print (cdd, "inner Ga=", innerGa, layer, "cc ga", ga, "lift", centerMinR/cdd)
    return CcDia


# def Printlist(List, **kwargs): 
#     Print_list(List, **kwargs)

def Printlist(plist, head=5, tail=5, all=0, **kwargs): 
    if not isinstance(plist, list): 
        print ("## the instance is not a list")
        return 
    N = len(plist)
    cnt = 0 
    if all >= 0: 
        for i, pl in enumerate(plist): 
            
            if i < head: print ("%d"%(i), pl)
            elif i > N-tail-1: print ("%d"%(i), pl)
            else: 
                if cnt ==0: print (" ''''' ")
                cnt += 1
    else: 
        for pl in plist: 
            print ("%d"%(i), pl)
def Print_list(LIST, tail=0, head=0, mid=[], all=0, **kwargs): 
    if not isinstance(LIST, list): 
        print ("## the instance is not a list")
        return 

    N = len(LIST)

    if all ==1: 
        s = 0; e=N 
        for i in range(s, e): 
            txt = "(%d), [ "%(i)
            for j, e in enumerate(LIST[i]): 
                if j < len(LIST[i])-1:    txt += str(e) + ", "
                else: txt += str(e) + " ]"
            print (txt)
    elif tail ==0 and head ==0 and len(mid) ==0 : 
        if N <= 10: s=0; e=N 
        else: s=0; e=5
        for i in range(s, e): 
            txt = "(%d), [ "%(i)
            for j, e in enumerate(LIST[i]): 
                if j < len(LIST[i])-1:    txt += str(e) + ", "
                else: txt += str(e) + " ]"
            print (txt)
        if N > 10: 
            print (".....")
            s = N-5; e = N
            for i in range(s, e): 
                txt = "(%d), [ "%(i)
                for j, e in enumerate(LIST[i]): 
                    if j < len(LIST[i])-1:    txt += str(e) + ", "
                    else: txt += str(e) + " ]"
                print (txt)
    
    else: 
        
        if len(mid) == 0: 
            if tail + head >= N : 
                s=0; e=N
                for i in range(s, e): 
                    txt = "(%d), [ "%(i)
                    for j, e in enumerate(LIST[i]): 
                        if j < len(LIST[i])-1:    txt += str(e) + ", "
                        else: txt += str(e) + " ]"
                    print (txt)
            else: 
                s=0; e=head 
                if e >=N : e = N 
                for i in range(s, e): 
                    txt = "(%d), [ "%(i)
                    for j, e in enumerate(LIST[i]): 
                        if j < len(LIST[i])-1:    txt += str(e) + ", "
                        else: txt += str(e) + " ]"
                    print (txt)
                print (".....")
                s=N-tail; e=N 
                if s < 0: s=0 
                for i in range(s, e): 
                    txt = "(%d), [ "%(i)
                    for j, e in enumerate(LIST[i]): 
                        if j < len(LIST[i])-1:    txt += str(e) + ", "
                        else: txt += str(e) + " ]"
                    print (txt)
        else: 
            s=mid[0]; e=mid[1]

            if e >= N: e=N 
            if s >=e : s=e-1
            if s < 0:  e=0 

            if s>0: print (".....")

            for i in range(s, e): 
                txt = "(%d), [ "%(i)
                for j, e in enumerate(LIST[i]): 
                    if j < len(LIST[i])-1:    txt += str(e) + ", "
                    else: txt += str(e) + " ]"
                print (txt)
            if e < N-1: print (".....")

class NAME:
    def __init__(self, name): 
        self.name=name 
class EDGE:
    def __init__(self):
        self.Edge = []
    def __del__(Self): 
        # print ("EDGE IS DELETED")
        pass

    def Help(self):
        print ("*********************************************************************************")
        print ("EDGE : Node1, Node2, Elset_Name, FacdID, Element_No, D")
        print (" D : -1= Edge, 0 = Free Edge, -2 = not Free Edge, 1= outer edges, Above 1(2~) = Tie No")
        print ("***************************************************************************")

    def Add(self, edge):
        self.Edge.append(edge)

    def Print(self, tail=0, head=0, **kwargs):
        Print_list(self.Edge, tail=tail, head=head, **kwargs)
        
    def Combine(self, iEdge):
        N = len(iEdge.Edge)
        for i in range(N): 
            self.Add(iEdge.Edge[i])

    def Sort(self, reverse=False):
        edges=[]
        e1 =[]; e2=[]
        for i, e in enumerate(self.Edge):
            edges.append([e[0], e[1], i])
            e1.append(e[0])
            e2.append(e[1])
            # print("%d, %d, %d"%(e[0], e[1], e[4]))

        edges = np.array(edges)
        e1 = np.array(e1)
        e2 = np.array(e2)

        
        if reverse == False:        
            e = np.setdiff1d(e1, e2) ## it remains the 1st node at the first element 
            col = 0
            ncol =1 
        else:                       
            e = np.setdiff1d(e2, e1)  ## it remains the 2nd node at the last element 
            col = 1
            ncol = 0 
        

        ## if it's is closed, there will be nothing 

        srted=[] 
        idx = np.where(edges[:,col] == e) [0]
        while len(idx)>0: 
            i = edges[ idx[0] ][2]
            # print ("sorting", self.Edge[i])
            srted.append(self.Edge[i])

            idx = np.where(edges[:,col] == self.Edge[i][ncol])[0]
        self.Edge = srted 
        return srted 
class ELSET:
    def __init__(self):
        self.Elset = []

    def Print(self):
        print ("*************************************************************")
        print ("** [[Elset1, E11, E12, ..], {Elset2, E21, E22, ...], ...]")
        print ("*************************************************************")

    def AddName(self, name):
        exist = 0
        for i in range(len(self.Elset)):
            if self.Elset[i][0] == name:
                exist = 1
                break
        if exist == 0:
            self.Elset.append([name])

    def AddNumber(self, n, name):
        for i in range(len(self.Elset)):
            if self.Elset[i][0] == name:
                self.Elset[i].append(n)
    def Add(self, n, name): 
        exist = 0
        for i in range(len(self.Elset)):
            if self.Elset[i][0] == name:
                exist = 1
                self.Elset[i].append(n)
                break
        if exist == 0:
            self.Elset.append([name, n])


class SURFACE:
    # surf_: [node_id, face_id, No_nodes, 1.0(free_sf), center coord_1, center coord_2, center coord_3, n1, n2, n3, n4]
    def __init__(self): 
        self.Surface = []

    def AddName(self, name): 
        pre = 0 
        for surf in self.Surface:
            if surf[0] == name: 
                pre =1
                break 
        if pre == 0: 
            self.Surface.append([name])
    def AddSurface(self, name, number, face): 
        pre = 0 
        for i, surf in enumerate(self.Surface):
            if surf[0] == name: 
                self.Surface[i].append([number, face])
                pre =1 
                break 
        if pre ==0: 
            self.AddName(name)
            self.AddSurface(name, number, face)
    def Add(self, surf): 
        self.Surface.append(surf)
class TIE:
    def __init__(self):
        self.Tie = []
    def Add(self, name, slave, master):
        self.Tie.append([name, slave, master])
class NODE:
    def __init__(self):
        self.Node = []

    def Add(self, d):
        self.Node.append(d)

    def Delete(self, n):
        N = len(self.Node)
        for i in range(N):
            if self.Node[i][0] == n:
                del (self.Node[i])
                break

    def Sort(self, item=0, reverse=False):
        tmpNode = NODE()
        try:
            arr = self.Node[:, item]
        except:
            npNode = np.array(self.Node)
            arr = npNode[:, item]
        if reverse == False: args = np.argsort(arr)
        else:                args = np.argsort(arr)[::-1]
        for nd in self.Node:    tmpNode.Add(nd) 
        sortedlist = []
        for i, arg in enumerate(args):
            self.Node[i] = tmpNode.Node[int(arg)]
            sortedlist.append(tmpNode.Node[int(arg)])
        del(tmpNode)
        sortedlist = np.array(sortedlist)
        return sortedlist

    def DeleteDuplicate(self):
        npary = np.array(self.Node)
        uniques = np.unique(npary)
        N = len(uniques)
        for i, nd in enumerate(self.Node): 
            if i < N :             nd = uniques[i]
        i = N 
        while i < len(self.Node): del(self.Node[i])

    def Combine(self, node):
        N = len(node.Node)
        for i in range(N): 
            self.Add(node.Node[i])

    
    def NodeByID(self, n, SORT=0, **args):
        for key, value in args.items():
            if key == 'sort':
                SORT=int(value)

        if SORT ==1:
            sorted(self.Node, key=lambda x:x[0])
        
        nodes = np.array(self.Node)
        idx = np.where(nodes[:,0]==n)[0][0]
        return self.Node[idx]
    def NodeIDByCoordinate(self, PO, v, closest=0, **args):
    
        N = len(self.Node)
        
        if closest != 0:
            min = 1000000000.0
            
            if PO == 'x' or PO == 'X':
                for i in range(N):
                    if abs(self.Node[i][1]-v) < min:
                        min = self.Node[i][1]
                        ClosestNode = self.Node[i][0]
            elif PO == 'y' or PO == 'Y':
                for i in range(N):
                    if abs(self.Node[i][2]-v) < min:
                        min = self.Node[i][2]
                        ClosestNode = self.Node[i][0]
            elif PO == 'z' or PO == 'Z':
                for i in range(N):
                    if abs(self.Node[i][3]-v) < min:
                        min = self.Node[i][3]
                        ClosestNode = self.Node[i][0]
            else:
                print ("* Check INPUT x/y/z - you input %s"%(PO))
            return ClosestNode
        else: 
            IDs = []
            if PO == 'x' or PO == 'X':
                for i in range(N):
                    if self.Node[i][1] == v:
                        IDs.append(self.Node[i][0])
            elif PO == 'y' or PO == 'Y':
                for i in range(N):
                    if self.Node[i][2] == v:
                        IDs.append(self.Node[i][0])
            elif PO == 'z' or PO == 'Z':
                for i in range(N):
                    if self.Node[i][3] == v:
                        IDs.append(self.Node[i][0])
            else:
                print ("* Check INPUT x/y/z - you input", PO)
            if len(IDs) == 0:
                print ("* Matching Node (", PO, ":", v,")was not found!!")
            return IDs
    def Print(self, head=0, tail=0, **kwargs):
        Print_list(self.Node, tail=tail, head=head, **kwargs)
class ELEMENT:
    def __init__(self):
        self.Element = []
    def Add(self, e):
        self.Element.append(e)
    def Delete(self, n):
        N = len(self.Element)
        for i in range(N):
            if self.Element[i][0] == n:
                del (self.Element[i])
                break
    def DeleteDuplicate(self, id=1):
        npe = []
        for el in self.Element: 
            npe.append([el[0], el[2], el[3], el[4], el[6]])
        npe = np.array(npe)

        npe0 = npe[:,0]
        npe1 = np.unique(npe0)
        if len(npe0) != len(npe1): 
            i = 0 
            while i < len(self.Element): 
                idx = np.where(npe[:,0]==self.Element[i][0])[0]
                if len(idx) > 1: 
                    for ix in idx: 
                        if ix != i: 
                            del(self.Element[ix])
                            npe = np.delete(npe, ix, axis=0)
                            print (" >> Element %d was deleted."%(self.Element[i][0]))
                            i -= 1 
                            break 
                i += 1 

    def Nodes(self, **args):

        Node = NODE()
        for key, value in args.items():
            if key == 'Node' or key == 'node':
                Node = value


        I = len(self.Element)
        NL = []

        nds = []
        for el in self.Element: 
            nds.append(el[1]); nds.append(el[2]); 
            if el[3]>0: nds.append(el[3])
            if el[4]>0: nds.append(el[4])
        nds = np.array(nds, dtype=np.int32)
        NL = np.unique(nds)

        if len(Node.Node) == 0:  return NL
        
        npnd = np.array(Node.Node)
        NC = NODE() 
        for nd in NL: 
            ix = np.where(npnd[:,0] == nd) [0]
            if len(ix) == 1: 
                NC.Add([ int(npnd[ix[0]][0]), npnd[ix[0]][1], npnd[ix[0]][2], npnd[ix[0]][3]] )
        return NC 

    def Sort(self, item=0, reverse=False):
        sortedElement = ELEMENT()
        for i, element in enumerate(self.Element):
            sortedElement.Add(element)
            if i == 0:
                continue
            else:
                I = len(sortedElement.Element)
                for j, selement in enumerate(sortedElement.Element):
                    if reverse == True:
                        if selement[item] < element[item]:
                            del(sortedElement.Element[I-1])
                            sortedElement.Element.insert(j, element)
                            I = j 
                            break
                    else:
                        if selement[item] > element[item]:
                            del(sortedElement.Element[I-1])
                            sortedElement.Element.insert(j, element)
                            I = j 
                            break
        for i, element in enumerate(sortedElement.Element):
            self.Element[i] = element
        del(sortedElement)
    def Combine(self, element):
        N=len(element.Element)
        for i in range(N): 
            self.Add(element.Element[i])
    def AllEdge(self):
        Name = EDGE()
        N = len(self.Element)
        for i in range(N):
            if self.Element[i][6] == 4:
                Name.Add([self.Element[i][1], self.Element[i][2], self.Element[i][5], 'S1', self.Element[i][0], -1])
                Name.Add([self.Element[i][2], self.Element[i][3], self.Element[i][5], 'S2', self.Element[i][0], -1])
                Name.Add([self.Element[i][3], self.Element[i][4], self.Element[i][5], 'S3', self.Element[i][0], -1])
                Name.Add([self.Element[i][4], self.Element[i][1], self.Element[i][5], 'S4', self.Element[i][0], -1])
            elif self.Element[i][6] == 3:
                Name.Add([self.Element[i][1], self.Element[i][2], self.Element[i][5], 'S1', self.Element[i][0], -1])
                Name.Add([self.Element[i][2], self.Element[i][3], self.Element[i][5], 'S2', self.Element[i][0], -1])
                Name.Add([self.Element[i][3], self.Element[i][1], self.Element[i][5], 'S3', self.Element[i][0], -1])
        return Name
    def FreeEdge(self):
        edges = self.AllEdge()
        freeEdge = FreeEdge(edges)
        return freeEdge
    def OuterEdge(self, Node):
        FEdges = self.FreeEdge()
        OEdges = OuterEdge(FEdges, Node, self)
        return OEdges
        ## other method
        npn = np.array(Node.Node)
        free = self.FreeEdge()
        outer = EDGE()
        my = 10**7
        start = 0 
        for i, e in enumerate(free.Edge): 
            ix = np.where(npn[:,0] == e[0])[0][0]
            if npn[ix][2]> 0 and npn[ix][3]<my: 
                my = npn[ix][3]
                start = i 
        
        outer.Add(free.Edge[start])
        end = free.Edge[start][0]
        nxt = free.Edge[start]
        cnt = 0
        N=5
        while nxt[1] != end: 
            cnt +=1
            if cnt > 1000: 
                print(" Error to find outer edges")
                break 
            nt = self.NextEdge(nxt, free)
            if len(nt) ==1: 
                nxt = nt[0]
            elif len(nt) ==2: 
                fst = 0
                ne = nt[fst]
                ns = ne[0]
                for i in range(N): 
                    ne = self.NextEdge(ne, free)
                    if len(ne) ==2 : 
                        if ne[0][1] == ns or ne[1][1] == ns: 
                            fst = 1
                        break 
                    else: 
                        ne = ne[0]
                        if ne[1] == ns: 
                            fst = 1
                            break 
                nxt = nt[fst]
            outer.Add(nxt)
        return outer 
    def TieEdge(self, Node):
        FreeEdge = self.FreeEdge()
        OuterEdge(FreeEdge, Node, self)  # Don't Delete this line.
        TieNum = 1
        i = 0;        iTemp = 0;        j = 0
        connectedEdge = []
        TEdge = EDGE()
        while i < len(FreeEdge.Edge):
            if FreeEdge.Edge[i][5] < 1:
                TieNum += 1
                nodeStart = FreeEdge.Edge[i][0]
                FreeEdge.Edge[i][5] = TieNum
                TEdge.Add(FreeEdge.Edge[i])  # marked as TIE edge with No.
                iTemp = i
                while FreeEdge.Edge[iTemp][1] != nodeStart:
                    j += 1
                    if j > 100:
                        break  # in case infinite loop
                    connectedEdge = NextEdge(FreeEdge, iTemp)  # find next edge
                    if len(connectedEdge) == 1:  # in case of being found just 1 edge
                        iTemp = connectedEdge[0]
                    elif len(connectedEdge) == 2:  # when other tie is connected (2 ties are connected)
                        if FreeEdge.Edge[connectedEdge[0]][1] == nodeStart:
                            iTemp = connectedEdge[0]
                        elif FreeEdge.Edge[connectedEdge[1]][1] == nodeStart:
                            iTemp = connectedEdge[1]
                        else:
                            if FreeEdge.Edge[connectedEdge[0]][5] < 1 and FreeEdge.Edge[connectedEdge[1]][5] < 1:
                                iTemp = FindTieLoop(nodeStart, connectedEdge, FreeEdge)
                            elif FreeEdge.Edge[connectedEdge[0]][5] < 1:
                                iTemp = connectedEdge[0]
                            elif FreeEdge.Edge[connectedEdge[1]][5] < 1:
                                iTemp = connectedEdge[1]
                            else:
                                print ('[INPUT] {' + str(FreeEdge.Edge[connectedEdge[0]]) + ',' + str(FreeEdge.Edge[connectedEdge[1]]) + ' (0) TIE Conection InCompletion')
                                break
                    else:
                        print ('[INPUT] 2 or more Ties are Connected.')
                        break
                    # After finding next TIE Edge ################################
                    FreeEdge.Edge[iTemp][5] = TieNum
                    TEdge.Add(FreeEdge.Edge[iTemp])
                del connectedEdge
                connectedEdge = []
            i += 1
        return TEdge
    def MasterSlaveEdge(self, Node, Op = 0, **args):

        npn = np.array(Node.Node)
        for key, value in args.items():
            if key == 'op':
                Op = int(value)
        
        TieEdge = self.TieEdge(Node)
        iNum = 2
        mlength = 0 
        ErrRatio = 0.01
        
        NumTie = 0 
        N = len(TieEdge.Edge)
        for i in range(N):
            if TieEdge.Edge[i][5] > NumTie:
                NumTie = TieEdge.Edge[i][5]
            
        iMaster = []
        while iNum <=NumTie:
            MaxLength = 0.0
            SumLength = 0.0
            k = 0
            Save = 0
            while k < N:
                if TieEdge.Edge[k][5] == iNum:
                    # N1 = Node.NodeByID(TieEdge.Edge[k][0])
                    # N2 = Node.NodeByID(TieEdge.Edge[k][1])
                    ix = np.where(npn[:,0] == TieEdge.Edge[k][0])[0][0]; N1 = Node[ix]
                    ix = np.where(npn[:,0] == TieEdge.Edge[k][1])[0][0]; N2 = Node[ix]
                    Length = sqrt((N1[2]-N2[2])* (N1[2]-N2[2]) + (N1[3]-N2[3])*(N1[3]-N2[3]))
                    SumLength += Length
                    if Length > MaxLength:
                        MaxLength = Length
                        Save = k
                k += 1
            SumLength -= MaxLength
            if SumLength > MaxLength * (1+ErrRatio) or SumLength < MaxLength * (1-ErrRatio):
                print ('ERROR::PRE::TIE CREATION INCOMPLETE ON', TieEdge.Edge[Save][3])
            iMaster.append(Save)
            iNum += 1
        
        MasterEdge=EDGE()
        SlaveEdge =EDGE()
        M = len(iMaster)
        for i in range(N):
            exist = 0
            for j in range(M):
                if i == iMaster[j]:
                    MasterEdge.Add(TieEdge.Edge[i])
                    exist =1
                    break
            if exist == 0:
                SlaveEdge.Add(TieEdge.Edge[i])
        
        ## Op == 0 return MasterEdge and SlaveEdge
        ## Op == 1 return only Master Edge
        ## Op == 2 return Only Slave Edge
        if Op == 0:
            return MasterEdge, SlaveEdge
        elif Op == 1:
            return MasterEdge
        else:
            return SlaveEdge
    def Print(self, **kwargs): 
        Print_list(self.Element, **kwargs)
    def NextEdge(self, edge, edges, rev=0): 
        ed =[]
        if rev == 0: 
            for e in edges.Edge: 
                if e[0] == edge[1]: 
                    ed.append(e)
        else: 
            for e in edges.Edge: 
                if e[1] == edge[0]: 
                    ed.append(e)

        return ed 
def ReadMoldProfileFromPatternMeshFile(ptnfile): 

    with open(ptnfile) as PTN: 
        lines = PTN.readlines()

    scaling_factor = 0.001 
    Diameter = 0 
    tdw = 0
    GD = 0

    command = ""

    RightProfile=[]
    LeftProfile=[]

    nodes = []
    widths=[]

    for line in lines: 
        if "**" in line: 
            continue 
        if "*PROFILE_SCALING" in line: 
            word = list(line.split(":"))
            scaling_factor = float(word[1].strip())
            # print ("scaling factor=%f"%(scaling_factor))
            continue 
        if "*HALF_DIAMETER" in line: 
            word = list(line.split(":"))
            Diameter = float(word[1].strip()) * 2
            Diameter = round(Diameter *  scaling_factor, 6)
            continue 

        if "*PROFILE_LHS" in line: command="left"
        elif "*PROFILE_RHS" in line: command="right"
        elif "*NODE" in line or "*Node" in line: command="node"
        elif "*TREAD_DESIGN_WIDTH" in line.upper():
            data = line.split(":")
            tdw = float(data[1].strip()) * scaling_factor
        elif "GROOVE_DEPTH" in line.upper():
            data = line.split(":")
            GD = float(data[1].strip()) * scaling_factor
        elif "*" in line: command =""
        else: 
            if command == "left": 
                word = list(line.split(","))
                LeftProfile.append([round(float(word[0].strip())*scaling_factor, 5), round(float(word[1].strip())*scaling_factor, 9)])
            if command == "right": 
                word = list(line.split(","))
                RightProfile.append([round(float(word[0].strip())*scaling_factor, 5), round(float(word[1].strip())*scaling_factor, 9)])
            if command == "node": 
                word = list(line.split(","))
                nid = int(word[0].strip())
                nx = float(word[1].strip())
                ny = float(word[2].strip())
                nz = float(word[3].strip())
                nodes.append([nid, round(nx*scaling_factor, 10),  round(ny*scaling_factor, 10),  round(nz*scaling_factor, 10)])

    nodes = np.array(nodes)
    cz = nodes[:,3]
    mz = np.max(cz) 
    # Diameter = mz * 2 
    idxs = np.where(nodes[:,3] == mz)[0]
    wnds = nodes[idxs]
    widths = wnds[:,2]
    miny = np.min(widths)
    maxy = np.max(widths)

    TotalWidth = round((maxy-miny)*scaling_factor, 10)
    if GD ==0: GD = 1.0E-03 
    if tdw == 0: 
        tmp = 0
        sho = 0 
        for i, pf in enumerate(LeftProfile): 
            if pf[0] > 0.05 and i < len(LeftProfile)-1: 
                tdw += pf[1]
                sho =  1
            else: 
                tmp = pf[1]
                break 
        if sho ==1 : tdw -= tmp/3.0 *2
        tmp = 0
        sho = 0 
        for i, pf in enumerate(RightProfile): 
            if pf[0] > 0.05 and i < len(LeftProfile)-1: 
                tdw += pf[1]
                sho = 1
            else: 
                tmp = pf[1]
                break 
        if sho == 1: tdw -= tmp/3.0 *2

    tdw = round(tdw, 9)

    return LeftProfile, RightProfile, Diameter,  tdw, TotalWidth, GD

def FreeEdge(edge):
    FEdge = EDGE()
    edges = np.array(edge.Edge)
    for i, ed in enumerate(edges): 
        ix1 = np.where(edges[:,1] == ed[0])[0]
        ix2 = np.where(edges[:,0] == ed[1])[0]
        ix = np.intersect1d(ix1, ix2)
        if len(ix) ==0: 
            edge.Edge[i][5] = 0
            FEdge.Add(edge.Edge[i])
        else: 
            edge.Edge[i][5] = -2
    return FEdge
def OuterEdge(FreeEdge, Node, Element):
    N = len(FreeEdge.Edge)
    MinY = 9.9E20
    cNodes = [0]
    npn = np.array(Node.Node)
    for i in range(N):
        ix = np.where(npn[:,0]==FreeEdge.Edge[i][0])[0][0]; N1 = Node.Node[ix]
        ix = np.where(npn[:,0]==FreeEdge.Edge[i][1])[0][0]; N2 = Node.Node[ix]

        if N1[3] < MinY:
            MinY = N1[3]
            cNodes[0] = N1[0]
        if N2[3] < MinY:
            MinY = N2[3]
            cNodes[0] = N2[0]
    if cNodes[0] == 0:
        cNodes[0] = Node.NodeIDByCoordinate('z', 0.0, closest=1)

    MAX = 10000   ## max iteration for searching  error
    ShareNodePos = []
    #    connectedEdge = []
    outEdge = EDGE()

    ## Find a 1st surround edge (IL at the center)
    low = 9.9E20
    i = 0
    savei = 0
    while i < len(cNodes):
        j = 0
        while j < len(Node.Node):
            if cNodes[i] == Node.Node[j][0]:
                if Node.Node[j][3] < low:
                    low = Node.Node[j][3]
                    savei = j
            j += 1
        i += 1

    i = 0
    while i < len(FreeEdge.Edge):
        if Node.Node[savei][0] == FreeEdge.Edge[i][0]:
            break
        i += 1

    ## End of 1st Outer Edge finding (IL1)
    FreeEdge.Edge[i][5] = 1
    outEdge.Add(FreeEdge.Edge[i])
    iFirstNode = FreeEdge.Edge[i][0]

    count = 0
    #    i=  # i is no matter how big, because i is redefined when next edge is found
    while i < len(FreeEdge.Edge):
        count += 1
        if count > MAX:
            print ('[INPUT] CANNOT FIND OUTER EDGES IN THE MODEL')
            del (outEdge)
            outEdge = EDGE()
            return outEdge
        j = 0
        while j < len(FreeEdge.Edge):
            if i != j:
                if FreeEdge.Edge[i][1] == FreeEdge.Edge[j][0]:
                    # print ('edge[i][1], [j][0] ', FreeEdge.Edge[i], FreeEdge.Edge[j], 'i=', i)
                    ShareNodePos.append(j)
                    # print (ShareNodePos, FreeEdge.Edge[ShareNodePos[0]][0])
            j = j + 1
        if len(ShareNodePos) != 0:
            if FreeEdge.Edge[ShareNodePos[0]][0] == iFirstNode:
                break
        else:
            print ('[INPUT] CANNOT FIND CONNECTED FREE EDGE. CHECK TIE CONDITION')
            del (outEdge)
            outEdge = EDGE()
            return outEdge
        # print ('sharenodePos count = ', len(ShareNodePos))

        if len(ShareNodePos) == 1:
            FreeEdge.Edge[ShareNodePos[0]][5] = 1
            outEdge.Add(FreeEdge.Edge[ShareNodePos[0]])
            i = ShareNodePos[0]
            del ShareNodePos
            ShareNodePos = []
        else:
            if FreeEdge.Edge[i][4] == FreeEdge.Edge[ShareNodePos[0]][4]:
                tmpPos = ShareNodePos[1]
            else:
                SHARE = ShareEdge(FreeEdge.Edge[i][4], FreeEdge.Edge[ShareNodePos[1]][4], Element)
                if SHARE == 1:
                    tmpPos = ShareNodePos[0]
                else:
                    tmpPos = ShareNodePos[1]

                    #######################################################
                    nfe1 = 0; nfe2 = 0
                    for fe in FreeEdge.Edge:
                        if fe[4] == FreeEdge.Edge[tmpPos][4]:
                            # print (fe)
                            nfe1 += 1
                        if fe[4] == FreeEdge.Edge[ShareNodePos[0]][4]:
                            # print (fe)
                            nfe2 += 1
                    # print ("nfe=", nfe, FreeEdge[tmpPos])
                    if nfe1 < nfe2:
                        tmpPos = ShareNodePos[0]
                    elif nfe1 == nfe2:
                        tienode = FreeEdge.Edge[tmpPos][0]
                        nc = 0
                        for fe in FreeEdge.Edge:
                            if fe[4] == FreeEdge.Edge[tmpPos][4] and fe[1] == tienode: 
                                nc += 1
                                break
                        if nc == 0:   tmpPos = ShareNodePos[0]
                    ########################################################

            FreeEdge.Edge[tmpPos][5] = 1
            outEdge.Add(FreeEdge.Edge[tmpPos])
            i = tmpPos
            del ShareNodePos
            ShareNodePos = []
            
    return outEdge
def ShareEdge(m, n, Elements):
    p = ElementShape(m, Elements)
    q = ElementShape(n, Elements)
    lst = []
    if type(lst) != type(Elements): 
        N = len(Elements.Element)
        for i in range(N):
            if m == Elements.Element[i][0]:
                k = i
            if n == Elements.Element[i][0]:
                l = i

        count = 0
        for i in range(1, p+1):
            for j in range(1, q+1):
                if Elements.Element[k][i] == Elements.Element[l][j]:
                    count += 1
    else: 
        for i, el in enumerate(Elements): 
            if m == el[0]: k = i
            if n == el[0]: l = i
        count = 0 
        for i in range(1, p+1):
            for j in range(1, q+1):
                if Elements[k][i] == Elements[l][j]:
                    count += 1

    if count >= 2:
        return 1  # Edge shared
    else:
        return 0
def ElementShape(k, Elements):
    # k = element No.
    lst = []
    if type(lst) != type(Elements): 
        for el in Elements.Element: 
            if k == el[0]: return el[6]
    else: 
        for el in Elements: 
            if k == el[0]: 
                return el[6]

    print (k, 'Element was not found')
    return 0
def NextEdge(edge, alledges): 
    next = -1
    for i, ed in enumerate(alledges): 
        if ed[0] == edge[1]: 
            next = i
            break
    # if next == -1: print (f"no matching to Next edge       {edge}")
    return next 
def PreviousEdge(edge, alledges): 
    next = -1
    for i, ed in enumerate(alledges): 
        if ed[1] == edge[0]: 
            next = i
            break
    # if next == -1: print (f"no matching to Previous edge   {edge}")
    return next 
def Contact_relation_2Elements(e1, e2): 
    m1=[]; m2=[]
    for i in range(1, 5):
        if e1[i] ==0: continue 
        for j in range(1, 5): 
            if e2[j] == 0: continue 
            if e1[i] == e2[j] : 
                if i == 1: m1.append([e1[i], 0])
                else: m1.append([e1[i], i])
                m2.append([e2[j], j])

    if len(m1) == 0: 
        return None, 0 
    elif len(m1) ==1: 
        if m1[0][1] == 0: 
            pos = 1
        else: pos = m1[0][1] 
        return 'Point', pos 
    else:
        if int(e1[4]) != 0: 
            if m1[0][1] + m1[1][1] == 2 : face = 1
            if m1[0][1] + m1[1][1] == 5 : face = 2
            if m1[0][1] + m1[1][1] == 7 : face = 3
            if m1[0][1] + m1[1][1] == 4 : face = 4
        else: 
            if m1[0][1] + m1[1][1] == 2 : face = 1
            if m1[0][1] + m1[1][1] == 5 : face = 2
            if m1[0][1] + m1[1][1] == 3 : face = 3
        return 'Edge', face 
def Element2D_NextElement(el, solids, nodes, start=1, next=2): 
    ## solids = [No, N1, N2, N3, N4, No_of_nodes(3 or 4)]
    x =2; y=3 
    if el[5] == 4: 
        nf = start + next 
        if nf > 4 : nf -= 4  
        nfnode = [el[nf], el[nf+1]]
        if nf + 1 == 5 : nfnode = [ el[nf], el[1] ] 

        ix1 = np.where(solids[:, 1:5] == nfnode[0])[0] 
        ix2 = np.where(solids[:, 1:5] == nfnode[1])[0] 
        ix  = np.intersect1d(ix1, ix2)

        if len(ix) == 1: 
            n_solid = []
        elif len(ix) == 2: 
            if solids[ix[0]][0] == el[0] : n_solid = solids[ix[1]]
            else:                          n_solid = solids[ix[0]]
        else: 
            print ("!!!! ERROR. No FOUND NEXT 2D ELEMENT. ")
            sys.exit()
    elif el[5] ==3: 

        nf = start + next 
        if nf > 3 : nf -= 3  
        nfnode = [el[nf], el[nf+1]]
        if nf + 1 == 4  : nfnode = [ el[nf], el[1] ] 

        ix1 = np.where(solids[:, 1:5] == nfnode[0])[0] 
        ix2 = np.where(solids[:, 1:5] == nfnode[1])[0] 
        ix  = np.intersect1d(ix1, ix2)

        if len(ix) == 1: 
            n_solid = []
        elif len(ix) == 2: 
            if solids[ix[0]][0] == el[0] : n_solid = solids[ix[1]]
            else:                          n_solid = solids[ix[0]]
        else: 
            print ("!!!! ERROR. No FOUND NEXT 2D ELEMENT. ")
            sys.exit()
        
    return n_solid 
def ElementDuplicationCheck(AllElements):

    dup = 0 
    els = []
    for el in AllElements: 
        els.append([el[0], el[1], el[2], el[3], el[4], el[6]]) 
    els = np.array(els)    

    N0 = len(els)
    eln = els[:,0] 
    eln = np.unique(eln)

    if N0 > len(eln): 
        print ("##  %d elements are duplicates"%(N0-len(eln)))
        i = 0 
        cnt = 0 
        while i < len(AllElements): 
            idx = np.where(els[:,0]==AllElements[i][0])[0]
            if len(idx) > 1: 
                for ix in idx: 
                    if ix != i: 
                        del(AllElements[ix])
                        els = np.delete(els, ix, axis=0)
                        print (" >> Element %d was deleted."%(AllElements[i][0]))
                        i -= 1 
                        break 
            i += 1 

    idx = np.where(els[:,5] == 2)[0]
    el2 = els[idx]
    if len(idx) > 0: 
        el2 = els[idx]
        for el in el2: 
            ix1 = np.where(el2[:, 1:3] == el[1])[0]
            ix2 = np.where(el2[:, 1:3] == el[2])[0]
            ix = np.intersect1d(ix1, ix2)
            if len(ix) > 1: 
                print ('## Error! Rebar ' + str(el[0]) + ' is overlapped.')
                dup =  1
    
    idx = np.where(els[:,5] == 3)[0]
    if len(idx) > 0: 
        el3 = els[idx]
        for el in el3: 
            ix1 = np.where(el3[:, 1:4] == el[1])[0]
            ix2 = np.where(el3[:, 1:4] == el[2])[0]
            ix3 = np.where(el3[:, 1:4] == el[3])[0]

            ix = np.intersect1d(ix1, ix2)
            ix = np.intersect1d(ix, ix3)
            if len(ix) > 1: 
                print ('## Error! CGAX3H ' + str(el[0]) + ' is overlapped.')
                dup =  1
    idx = np.where(els[:,5] == 4)[0]
    if len(idx) > 0: 
        el4 = els[idx]
        for el in el4: 
            ix1 = np.where(el4[:, 1:5] == el[1])[0]
            ix2 = np.where(el4[:, 1:5] == el[2])[0]
            ix3 = np.where(el4[:, 1:5] == el[3])[0]
            ix4 = np.where(el4[:, 1:5] == el[4])[0]

            ix = np.intersect1d(ix1, ix2)
            ix = np.intersect1d(ix, ix3)
            ix = np.intersect1d(ix, ix4)
            if len(ix) > 1: 
                print ('## Error! CGAX4H ' + str(el[0]) + ' is overlapped.')
                dup =  1
    return dup 
def LayoutProfileDefineForExpansion(profiles, halfTDW, ShoR=0.05, t3dm=0):

    sl = 0 
    endTDW = -1
    decos = []
    Profiles=[]
    shocurve = 0 
    shoRad = 0.0
    shoLen = 0.0

    if t3dm ==1: 
        shocurve = 1 
        return profiles, shocurve, halfTDW, shoRad,  shoLen 

    for i, pf in enumerate(profiles): 
        if endTDW >=0 and len(profiles) - endTDW > 2: 
            decos.append(pf)
        else: 
            if round(pf[1]+sl, 4) == round(halfTDW,4): 
                endTDW = i 
            Profiles.append(pf)
            # print ("Add Profile ", pf)
            sl += pf[1]
            
    if endTDW >=0: 
        suml = 0.0
        for dc in decos: 
            suml += dc[1]
        avgr = 0 
        for dc in decos: 
            avgr += dc[0] * dc[1] / suml 
        if suml > 0.0001: 
            Profiles.append([avgr, suml])
            # print ("> Add Profile ", [avgr, suml])

        return Profiles, shocurve, halfTDW, shoRad,  shoLen 

    Profiles = []
    sl = 0.0 
    decos = []
    smallR = 0 
    for i, pf in enumerate(profiles): 
        if shocurve > 0: 
            decos.append(pf)
            if pf[0] < ShoR: smallR = -1 
            
        if sl < halfTDW and sl + pf[1] > halfTDW and pf[0] < ShoR: 
            shocurve =1 
            Profiles.append(pf)
            # print ("Add Profile ", pf)
            shoRad = pf[0]; shoLen = pf[1]
        elif sl < halfTDW: 
            Profiles.append(pf)
            # print ("Add Profile ", pf) 
            if pf[0] < ShoR: smallR = 1 

        
        sl += pf[1]
        
    
    if shocurve == 1: 
        suml = 0.0
        for dc in decos: 
            suml += dc[1]
        avgr = 0 
        for dc in decos: 
            avgr += dc[0] * dc[1] / suml 
        if suml > 0.0001: 
            Profiles.append([avgr, suml])
            # print ("> Add Profile ", [avgr, suml])

        return Profiles, shocurve, halfTDW, shoRad,  shoLen  

    print ("## Profile Info. is not correct")
    if smallR != 0: 
        curveL = 0.0 
        curveR = 0.0
        Profiles = []
        sl = 0.0 
        for i, pf in enumerate(profiles): 
            if pf[0] < ShoR: 
                curveR = pf[0]
                curveL = pf[1]
                Profiles.append(pf)
                # print (" adding", pf)
                hTDW = round(sl + pf[1]/2.0, 4) 
                print ("*  TDW Modified %.2f -> %.2f"%(halfTDW*2000, hTDW*2000))
                PF, sho, HTDW, shoRad,  shoLen = LayoutProfileDefineForExpansion(profiles, hTDW, ShoR=ShoR, t3dm=t3dm)
                return PF, sho, HTDW, shoRad,  shoLen 
            sl += pf[1]
    
    sl = 0 
    ldiff = 10000.00 
    mch = 0 
    for i, pf in enumerate(profiles): 
        sl += pf[1] 
        if abs(sl-halfTDW) < ldiff: 
            ldiff = abs(sl-halfTDW)
            mch = i 
    Profiles = []
    decos = []
    hTDW = 0.0 
    for i, pf in enumerate(profiles): 
        if i <=mch: 
            Profiles.append(pf)
            hTDW += pf[1]
        else: 
            decos.append(pf)

    print ("** TDW modified: %.2f -> %.2f"%(halfTDW*2000, hTDW*2000))
    suml = 0.0
    for dc in decos: 
        suml += dc[1]
    avgr = 0 
    for dc in decos: 
        avgr += dc[0] * dc[1] / suml 
    if suml > 0.0001: Profiles.append([avgr, suml])

    return Profiles, shocurve, hTDW, shoRad,  shoLen  
def FindSolidElementBetweenMembrane(m1, m2, Elements):
    # Data types of m1, m2 are string
    between = []
    Elm1 = []
    Elm2 = []

    for i, e in enumerate(m1): 
        if i ==0: continue 
        ix = np.where(Elements[:,0] == e)[0][0]
        Elm1.append(Elements[ix])
    for i, e in enumerate(m2): 
        if i ==0: continue 
        ix = np.where(Elements[:,0] == e)[0][0]
        Elm2.append(Elements[ix])

    s4 = np.where(Elements[:,5]==4)[0]
    solids = Elements[s4]

    for e in Elm1: 
        ix1 = np.where(solids[:,1:5]==e[1])[0]
        ix2 = np.where(solids[:,1:5]==e[2])[0]
        idx = np.intersect1d(ix1, ix2)

        for ix in idx: 
            for e2 in Elm2: 
                cnt = 0 
                if solids[ix][1] == e2[1] or solids[ix][1] == e2[2]: cnt += 1
                if solids[ix][2] == e2[1] or solids[ix][2] == e2[2]: cnt += 1
                if solids[ix][3] == e2[1] or solids[ix][3] == e2[2]: cnt += 1
                if solids[ix][4] == e2[1] or solids[ix][4] == e2[2]: cnt += 1
                if cnt ==2: 
                    between.append(solids[ix][0])
                    break 
            if cnt ==2: 
                break 
    return between     
def LayoutAlone3DModelGeneration(fname, nodes, elements, elset, surfaces, mesh="", sectors=240, offset=10000,\
     no_tread=10**7, abaqus=0, materialDir='', btAngles=[], overtype="SOT", PCIPress="", bdw=0 ): 

    tread=ELEMENT()
    body = ELEMENT()
    for el in elements.Element:
        td = 0 
        for td in TireTreadComponents: 
            if el[5].upper() == td: 
                td = 1
                break 
        if td ==1: 
            tread.Add(el)
        else:
            body.Add(el)

    Node_body = body.Nodes(node=nodes)
    Node_tread = tread.Nodes(node=nodes)

    body_TieMaster, body_TieSlave, body_outer, body_centerNodes, body_FreeEdges, body_allEdges, TieError = TieSurface(body.Element, Node_body.Node)

    delta =  2*PI / float(sectors)

    f=open(fname+".axi", 'w')
    if abaqus ==0:  f.write("*TIREBODY_NIDSTART_NIDOFFSET_EIDSTART_EIDOFFSET= 1, %5d, 1, %5d\n"%(offset, offset))
    f.write("*NODE\n")
    for i in range(sectors): 
        sec = float(i)
        for n in Node_body.Node:
            f.write("%8d, %.6e, %.6e, %.6e\n"%(n[0]+offset*sec, n[3]*sin(delta * sec), n[2], n[3]*cos(delta*sec)))
            ## [nd[0]+offset*i, nd[3]*sin(delta * f), nd[2], nd[3]*cos(delta*f)]

    el2=[]; el3=[]; el4=[]
    for i in range(sectors): 
        for el in body.Element: 
            en = el[0] + offset*i
            if i < sectors -1: 
                n1 = el[1] + offset*i
                n2 = el[2] + offset*i
                n3 = el[3] + offset*i
                n4 = el[4] + offset*i
                n5 = el[1] + offset*(i+1)
                n6 = el[2] + offset*(i+1)
                n7 = el[3] + offset*(i+1)
                n8 = el[4] + offset*(i+1)
            else: 
                n1 = el[1] + offset*i
                n2 = el[2] + offset*i
                n3 = el[3] + offset*i
                n4 = el[4] + offset*i
                n5 = el[1] 
                n6 = el[2] 
                n7 = el[3] 
                n8 = el[4] 
            if el[6] == 2: el2.append([en, n1, n2, n6, n5])
            elif el[6] == 3: el3.append([en, n5, n6, n7, n1, n2, n3])
            elif el[6] == 4: el4.append([en, n5, n6, n7, n8, n1, n2, n3, n4])

    if len(el2)>0: 
        f.write("*ELEMENT, TYPE=M3D4R\n")
        for e in el2:
            f.write("%6d, %6d, %6d, %6d, %6d\n"%(e[0], e[1], e[2], e[3], e[4]))

    if len(el3)>0: 
        f.write("*ELEMENT, TYPE=C3D6\n")
        for e in el3:
            f.write("%6d, %6d, %6d, %6d, %6d, %6d, %6d\n"%(e[0], e[1], e[2], e[3], e[4], e[5], e[6]))
    if len(el4)>0: 
        f.write("*ELEMENT, TYPE=C3D8R\n")
        for e in el4:
            f.write("%6d, %6d, %6d, %6d, %6d, %6d, %6d, %6d, %6d\n"%(e[0], e[1], e[2], e[3], e[4], e[5], e[6], e[7], e[8]))
    
    for es in elset.Elset:
        td = 0 
        for en in TireTreadComponents:
            if es[0].upper() == en:
                td = 1
                break 
        if td ==0: 
            N = len(es)
            if N > 1: 
                f.write("*ELSET, ELSET=%s\n"%(es[0]))
                
                for k in range(sectors): 
                    ret = 0 
                    for i in range(1, N):
                        if i%10 == 0: 
                            f.write("%6d\n"%(es[i]+offset*k))
                            ret = 1 
                        elif i == N-1: 
                            f.write("%6d\n"%(es[i]+offset*k))
                            ret =1 
                        else: 
                            f.write("%6d,"%(es[i]+offset*k))
                            ret = 0 
                    if ret == 0: 
                        f.write("\n")

    for es in surfaces.Surface:
        if es[0] !="CONT" and not 'Tie' in es[0]: 
            N = len(es)
            if N > 1: 
                f.write("*SURFACE,TYPE=ELEMENT,NAME=%s\n"%(es[0]))
                for k in range(sectors): 
                    for i in range(1, N):
                        f.write("%6d, %s\n"%(es[i][0]+offset*k, Change3DFace(es[i][1])))
    f.write("*SURFACE,TYPE=ELEMENT,NAME=TIREBODY\n")
    for i in range(sectors): 
        for ed in body_outer: 
            f.write("%6d, %s\n"%(ed[4]+offset*i, Change3DFace(ed[3])))
    cnt = 0 
    for ts, tm in zip(body_TieSlave, body_TieMaster): 
        cnt +=1 
        f.write("*SURFACE,TYPE=ELEMENT,NAME=TIE_M%d\n"%(cnt))
        for i in range(sectors): 
            f.write("%6d, %s\n"%(tm[4]+offset*i, Change3DFace(tm[3])))
        f.write("*SURFACE,TYPE=ELEMENT,NAME=TIE_S%d\n"%(cnt))
        for i in range(sectors): 
            for t in ts: 
                f.write("%6d, %s\n"%(t[4]+offset*i,  Change3DFace(t[3])))
        f.write("*TIE, POSITION TOLERANCE=0.001, NAME=TIE%d\n"%(cnt))
        f.write(" TIE_S%d, TIE_M%d\n"%(cnt, cnt))

    f.close()

    tread_TieMaster, tread_TieSlave, tread_outer, tread_centerNodes, tread_FreeEdges, tread_allEdges, TieError=  TieSurface(tread.Element, Node_tread.Node)


    f=open(fname+".trd", 'w')
    if abaqus ==0: f.write("*TREADPTN_NIDSTART_NIDOFFSET_EIDSTART_EIDOFFSET= %d, %d, %d, %d\n"%(no_tread, offset, no_tread, offset))

    f.write("*NODE\n")
    for i in range(sectors): 
        sec = float(i)
        for n in Node_tread.Node:
            f.write("%8d, %.6e, %.6e, %.6e\n"%(n[0]+offset*sec + no_tread, n[3]*sin(delta * sec), n[2], n[3]*cos(delta*sec)))

    el2=[]; el3=[]; el4=[]
    for i in range(sectors): 
        for el in tread.Element: 
            en = el[0] + offset*i  + no_tread
            if i < sectors -1: 
                n1 = el[1] + offset*i + no_tread
                n2 = el[2] + offset*i + no_tread
                n3 = el[3] + offset*i + no_tread
                n4 = el[4] + offset*i + no_tread
                n5 = el[1] + offset*(i+1) + no_tread
                n6 = el[2] + offset*(i+1) + no_tread
                n7 = el[3] + offset*(i+1) + no_tread
                n8 = el[4] + offset*(i+1) + no_tread
            else: 
                n1 = el[1] + offset*i + no_tread
                n2 = el[2] + offset*i + no_tread
                n3 = el[3] + offset*i + no_tread
                n4 = el[4] + offset*i + no_tread
                n5 = el[1]  + no_tread
                n6 = el[2]  + no_tread
                n7 = el[3]  + no_tread
                n8 = el[4]  + no_tread
            if el[6] == 2: el2.append([en, n1, n2, n6, n5])
            elif el[6] == 3: el3.append([en, n5, n6, n7, n1, n2, n3])
            elif el[6] == 4: el4.append([en, n5, n6, n7, n8, n1, n2, n3, n4])

    if len(el2)>0: 
        f.write("*ELEMENT, TYPE=M3D4R\n")
        for el in el2:
            f.write("%6d, %6d, %6d, %6d, %6d\n"%(e[0], e[1], e[2], e[3], e[4]))

    if len(el3)>0: 
        f.write("*ELEMENT, TYPE=C3D6\n")
        for e in el3:
            f.write("%6d, %6d, %6d, %6d, %6d, %6d, %6d\n"%(e[0], e[1], e[2], e[3], e[4], e[5], e[6]))
    if len(el4)>0: 
        f.write("*ELEMENT, TYPE=C3D8R\n")
        for e in el4:
            f.write("%6d, %6d, %6d, %6d, %6d, %6d, %6d, %6d, %6d\n"%(e[0], e[1], e[2], e[3], e[4], e[5], e[6], e[7], e[8]))
    
    for es in elset.Elset:
        td = 0 
        for en in TireTreadComponents:
            if es[0].upper() == en:
                td = 1
                break 
        if td ==1: 
            N = len(es)
            if N > 1: 
                f.write("*ELSET, ELSET=%s\n"%(es[0]))
                
                for k in range(sectors): 
                    ret = 0 
                    for i in range(1, N):
                        if i%10 == 0: 
                            f.write("%6d\n"%(es[i]+offset*k + no_tread))
                            ret = 1 
                        elif i == N-1: 
                            f.write("%6d\n"%(es[i]+offset*k + no_tread))
                            ret =1 
                        else: 
                            f.write("%6d,"%(es[i]+offset*k + no_tread))
                            ret = 0 
                    if ret == 0: 
                        f.write("\n")

    for es in surfaces.Surface:
        if es[0] =="CONT" : 
            N = len(es)
            if N > 1: 
                f.write("*SURFACE,TYPE=ELEMENT,NAME=%s\n"%(es[0]))
                for k in range(sectors): 
                    for i in range(1, N):
                        f.write("%6d, %s\n"%(es[i][0]+offset*k + no_tread, Change3DFace(es[i][1])))

    f.write("*SURFACE,TYPE=ELEMENT,NAME=XTRD1001\n")
    for k in range(sectors): 
        for ed in tread_outer: 
            f.write("%6d, %s\n"%(ed[4]+offset*k + no_tread, Change3DFace(ed[3])))
   
    Tire_Outer = elements.OuterEdge(nodes)
    f.write("*SURFACE,TYPE=ELEMENT,NAME=YTIE1001\n")
    for ed in tread_outer: 
        fd = 0 
        for te in Tire_Outer.Edge:
            if te[0] == ed[0] and te[1] == ed[1]: 
                fd =1 
                break 
        for te in tread_TieSlave:
            if te[0] == ed[0] and te[1] == ed[1]: 
                fd =1 
                break 
        for te in tread_TieMaster:
            if te[0] == ed[0] and te[1] == ed[1]: 
                fd =1 
                break 
        if fd ==0: 
            for i in range(sectors): 
                f.write("%6d, %s\n"%(ed[4]+offset*i + no_tread, Change3DFace(ed[3]))) 

    cnt = 0 
    for ts, tm in zip(tread_TieSlave, tread_TieMaster): 
        cnt +=1 
        f.write("*SURFACE,TYPE=ELEMENT,NAME=TIE_M%d\n"%(cnt+1000))
        for i in range(sectors): 
            f.write("%6d, %s\n"%(tm[4]+offset*i + no_tread, Change3DFace(tm[3])))
        f.write("*SURFACE,TYPE=ELEMENT,NAME=TIE_S%d\n"%(cnt+1000))
        for i in range(sectors): 
            for t in ts: 
                f.write("%6d, %s\n"%(t[4]+offset*i + no_tread,  Change3DFace(t[3])))
        f.write("*TIE, POSITION TOLERANCE=0.001, NAME=TIE%d\n"%(cnt+1000))
        f.write(" TIE_S%d, TIE_M%d\n"%(cnt+1000, cnt+1000))


    f.write("*TIE, NAME=TBD2TRD, ADJUST=YES, POSITION TOLERANCE= 0.0001\n")
    f.write(" YTIE1001, TIREBODY\n")

    f.close()
    
    if abaqus ==0: 
        SmartMaterialInput(axi=fname+".axi", trd=fname+".trd", layout=mesh, elset=elset.Elset, node=nodes.Node, element=elements.Element,\
             materialDir=materialDir, btAngles=btAngles, overtype=overtype, PCIPress=PCIPress, bdw=bdw)
    # else:
    #     AbaqusMaterialInput(axi=fname+".axi", trd=fname+".trd", layout=mesh, elset=elset.Elset, node=nodes.Node, element=elements.Element)


def Equivalent_density_calculation(cute_mesh, filename=""): 
    # print ("\n************************************************** ")
    # print ("** Equilivalent Density Calculation")
    # print ("************************************************** ")
    mat_solids =[]
    mat_cords = []
    with open(cute_mesh) as MS: 
        lines = MS.readlines()
    cmd = ''
    start = 0 
    solid=[]
    bdc = []
    roll = []
    tireGroup = "PCR"
    bt_gauge = 4.61E-04
    bsd = 0.0
    rw = 0.0 
    rd = 16.0
    size = ''
    btLift = 1.03
    for line in lines: 
        if "**" in line : 
            if "WEIGHT" in line: continue 
            if "CLASS_CODE" in line: tireGroup = line 
            if "BEAD SET DISTANCE" in line : 
                data = line.split(":")[1]
                try:
                    bsd = float(data.strip())
                except:
                    print(line)

            if "LAYOUT RIM WIDTH" in line : 
                data = line.split(":")[1]
                try:
                    rw = float(data.strip())
                except:
                    print(line)
            if "RIM DIA" in line : 
                data = line.split(":")[1]
                try:
                    rd = float(data.strip())
                except:
                    print(line)
            if "SIZE" in line and not 'mm' in line: 
                data = line.split(":")[1]
                try:
                    size = data.strip()
                except:
                    print(line)
            if "BELT LIFT RATIO" in line : 
                data = line.split(":")[1]
                try:
                    btLift = float(data.strip())
                except:
                    print(line)

            if "END OF MATERIAL INFO" in line : 
                # print ("ENDING*********************")
                break 
            if "MATERIAL INFO" in line: 
                start = 1

            if "***" in line: continue

            if "COMPONENTS EXTRUDED" in line and start ==1: 
                cmd = 'solid'
                continue 
            if "BEAD CORE" in line and start ==1: 
                cmd = 'bead'
                continue 
            if "COMPONENTS ROLLED" in line and start ==1: 
                cmd = 'rolled'
                continue 

            if cmd == 'solid': 
                data = line.split(",")
                tmp = []
                for dt in data: 
                    tmp.append(dt.strip())
                solid.append(tmp)
                # print ("SOLID", tmp)

            if cmd == 'bead': 
                data = line.split(",")
                tmp = []
                for dt in data: 
                    tmp.append(dt.strip())
                bdc.append(tmp)
                # print ("BEAD", tmp)
                
            if cmd == 'rolled': 
                data = line.split(",")
                tmp = []
                for dt in data: 
                    tmp.append(dt.strip())
                roll.append(tmp)
                # print ("ROLLED", tmp)
    
    # f = open(filename, "w") 
    if len(solid) ==0 and len(bdc) ==0 and len(roll) ==0: 
        return mat_solids, mat_cords, tireGroup, bt_gauge, bsd, rw, rd, size, btLift
    print ("\n## Equivalent Density Saved'\n")
    # f.write("*SOLID\n")
    if len(solid) > 0: 
        for sd in solid: 
            name = sd[0].split("(")[0].strip()
            name = name[2:]
            compound = sd[1]
            density = float(sd[2]) * float(sd[3]) 
            # f.write("%6s, %7s, %.5f, %.3e, %.5f\n"%(name, compound, density, float(sd[5])/10**9, float(sd[6])))
            mat_solids.append([name, compound, density, float(sd[5])/10**9, float(sd[6]) ])
    if len(bdc) > 0: 
        for sd in bdc: 
            name = sd[0].split("(")[0].strip()
            name = name[2:]
            compound = sd[1]
            density = float(sd[3]) / float(sd[2]) * 10**9 /1000
            # f.write("%6s, %7s, %.5f, %.3e, %.5f\n"%(name, compound, density, float(sd[2]) / 10**9, float(sd[3]) ))
            mat_solids.append([name, compound, density, float(sd[2]) / 10**9, float(sd[3] ) ])
    # f.write("** CMP, CODE, density, Volume(m3), Weight(kg)\n")

    # f.write("*REBAR\n")
    CCT = [];     BTT = [];     JEC = []; JFC=[]; OJFC=[]
    BDC = [];     SCT = [];     NCT = []
    if len(roll) > 0: 
        for sd in roll: 
            name = sd[0].split("(")[0].strip()
            name = name[2:]
            code =sd[1]
            structure = sd[2]
            # try: 
            EPI = float(sd[3])
            dia = float(sd[4])/1000.0
            topping = sd[5]
            ga = float(sd[6]) /1000
            cf = float(sd[7])
            rf = float(sd[8])
            
            try: 
                wt = float(sd[11])
            except:
                wt = 1.0
            if "ES" in code and not "D/" in structure: 
                Area = Area_steel_cord(structure)
            else: 
                if dia ==0: 
                    dia = ga - 0.7e-3
                Area = PI * dia**2 / 4.0 
                

            toping_density = rf*10.0 / ga /1000
            if Area != 0.0 : 
                cord_density =  cf / 100.0 / Area / 39.37 / EPI
            else: 
                cord_density =  cf / 100.0 / Area / 39.37 / EPI

            line_density = cf * 10.0 /39.37 / EPI 
            real_rubber_volume = ga - Area * 39.37 * EPI 
            topping_real_density = rf*10 / real_rubber_volume /1000

            

            # f.write("%6s, %8s, %.5f, %.5f, %.5e, %.5f, %.5f, %.5f, %.3f, %.3f, %.3e\n"%(\
            #         name, code, toping_density, cord_density, line_density, topping_real_density, rf, cf, wt * cf/(cf+rf), wt * rf/(cf+rf), Area))
            
            if cf + rf == 0.0: 
                mat_cords.append([name, code, toping_density, cord_density, line_density, 0.0, Area, topping, ga])
                rubber_weight = 0.0
                cord_weight =0.0
            else: 
                mat_cords.append([name, code, toping_density, cord_density, line_density, wt * cf/(cf+rf), Area, topping, ga])
                rubber_weight = wt * rf/(cf+rf)
                cord_weight = wt * cf/(cf+rf)

            # print ("%6s, %8s, %.5f, %.5f, %.5e, %.5f, %.5f, %.5f, %.3f, %.3f, %.3e\n"%(\
            #          name, code, toping_density, cord_density, line_density, topping_real_density, rf, cf, cord_weight, rubber_weight, Area))


            if "C01" in name:   CCT = [name, topping, toping_density, float(sd[10])/10**9, rubber_weight]
            if "BT2" in name:   
                BTT = [name, topping, toping_density, float(sd[10])/10**9, rubber_weight]
                bt_gauge = dia / 2.0 * 1.772454
            if "JEC" in name:   JEC = [name, topping, toping_density, float(sd[10])/10**9,  rubber_weight]
            if "JFC" in name:   JFC = [name, topping, toping_density, float(sd[10])/10**9, rubber_weight]
            if "OJFC" in name:   OJFC = [name, topping, toping_density, float(sd[10])/10**9, rubber_weight]
            # if "BDC" in name:   BDC = [name, topping, toping_density, float(sd[10])/10**9, rubber_weight]
            if "CH1" in name:   SCT = [name, topping, toping_density, float(sd[10])/10**9, rubber_weight]
            if "CH2" in name:   NCT = [name, topping, toping_density, float(sd[10])/10**9, rubber_weight]
                
            # except:
            #     pass 

    # f.write("** CMP, CODE, Equi-Toping Density, Equi-Cord Dentidy, Line Density, Real-topping density, Rubber factor, cord factor, volume, cord_wt, rubber_wt, area\n")

    # f.write("*SOLID\n")
    if len(CCT) > 0: 
        mat_solids.append(['CCT', CCT[1], CCT[2], CCT[3], CCT[4]])
        # f.write("%6s, %7s, %.5f, %.3e, %.5f\n"%('CCT', CCT[1], CCT[2], CCT[3], CCT[4] ))
    if len(BTT) > 0: 
        mat_solids.append(['BTT', BTT[1], BTT[2], BTT[3], BTT[4]])
        # f.write("%6s, %7s, %.5f, %.3e, %.5f\n"%('BTT', BTT[1], BTT[2], BTT[3], BTT[4] ))
    if len(JEC) > 0 and len(JFC) ==0 : 
        mat_solids.append(['JBT', JEC[1], JEC[2], JEC[3], JEC[4]])
        # f.write("%6s, %7s, %.5f, %.3e, %.5f\n"%('JBT', JEC[1], JEC[2], JEC[3], JEC[4] ))
    if len(JFC) > 0  and len(OJFC) ==0 : 
        # f.write("%6s, %7s, %.5f, %.3e, %.5f\n"%('JBT', JFC[1], JFC[2], JFC[3], JFC[4] ))
        mat_solids.append(['JBT', JFC[1], JFC[2], JFC[3], JFC[4]])
    if len(OJFC) > 0: 
        # f.write("%6s, %7s, %.5f, %.3e, %.5f\n"%('JBT', JFC[1], JFC[2], JFC[3], JFC[4] ))
        mat_solids.append(['JBT', OJFC[1], OJFC[2], OJFC[3], OJFC[4]])
    # if len(BDC) > 0: f.write("%6s, %7s, %.5f, %.3e, %.5f\n"%("BDT", BDC[1], BDC[2], BDC[3], BDC[4] ))
    if len(SCT) > 0: 
        mat_solids.append(['SCT', SCT[1], SCT[2], SCT[3], SCT[4] ])
        # f.write("%6s, %7s, %.5f, %.3e, %.5f\n"%('SCT', SCT[1], SCT[2], SCT[3], SCT[4] ))
    if len(NCT) > 0: 
        mat_solids.append(['NCT', NCT[1], NCT[2], NCT[3], NCT[4]])
        # f.write("%6s, %7s, %.5f, %.3e, %.5f\n"%('NCT', NCT[1], NCT[2], NCT[3], NCT[4] ))

    # f.close()
    # print ("************************************************** ")
    return mat_solids, mat_cords, tireGroup, bt_gauge, bsd, rw, rd,size, btLift

def Area_steel_cord(cord, wrapping_dia=0.15e-3): 

    name = cord.upper().strip()
    if "W" in name: 
        wrp = 1 
        name = name.split("W")[0]
    else: 
        wrp = 0 
    # print (name)
    if name[-1:] == "+": 
        name = name[:-1]
    # print (name, len(name))
    for i in range(len(name)-1, 0, -1): 
        if ")" == name[i]: 
            name = name[:i+1]
            break 
    # print (name, end=" -> ")

    layer = 1;     ls = 0;     lr = 0;     lx = 0 
    fname =''
    for i in range(len(name)): 
        if name[i] == '/' : 
            ls += 1 
            layer += 1 
            fname += "+"
        elif name[i] == '+' : 
            lr += 1 
            layer += 1 
            fname += name[i]
        elif name[i] == 'X' : 
            lx += 1 
            fname += name[i]
        else: 
            fname += name[i]
    # print (fname)
    # print ("layer=%d, same_dir=%d, rev_dir=%d, cross=%d, wrap=%d"%(layer, ls, lr, lx, wrp))

    layers = fname.split("+")
    # print (layers)
    area = 0.0
    nWire = 0 
    for layer in layers: 
        if "X" in layer: 
            wires = layer.split("X")
            w1 = float(wires[0])
            if "(" in wires[1]: 
                wire = wires[1].split("(")
                w2 = float(wire[0])
                dia = float(wire[1].split(")")[0]) /1000.0 
            else: 
                w2 = float(wires[1])
                dia = 0  
            nWire += w1 * w2 
            if dia > 0: 
                # print ("   >> ", layer, " Area Cal : dia=%.3f cord N=%d"%(dia*1000, nWire))
                area += nWire * dia**2* PI/4.0
                nWire = 0 
        else: 
            if "(" in layer: 
                wire = layer.split("(")
                nWire += float(wire[0])
                dia = float(wire[1].split(")")[0]) /1000.0 
            else: 
                nWire += float(layer)
                dia = 0 
            if dia > 0: 
                # print ("   >> ", layer, " Area Cal : dia=%.3f cord N=%d"%(dia*1000, nWire))
                area += nWire * dia**2* PI/4.0
                nWire = 0 
    if wrp ==1: 
        area += wrapping_dia**2* PI/4.0 
    
    # print ("Area=%.3e"%(area)) 
    return area

def GetRimDia_Size(size=""): 
    if size =="": 
        return 0

    if "R" in size: 
        rd = size.split("R")[1]
        try:
            rd = float(rd.strip())
        except:
            rd = float(rd[:2])
        
    return rd 


def SmartMaterialInput(axi="", trd="", layout="", elset=[], node=[], element=[], \
    materialDir='', ISLM_cordDBFile='ISLM_CordDBName.dat', btAngles=[], overtype='',\
         PCIPress="", bdw=0): 

    equ_Density = 0 
    name_solids, name_cords = SolidComponents_checking(axi=axi, trd=trd, return_value=1)

    localCordDB = 'ISLM_CordDB.txt'
    fileListFile = 'ISLM_materialList.txt'
    ISLM_cordDBFile="ISLM_CordDBName.dat"
    host = '10.82.66.65'
    user = 'h20200155'
    pw = 'h20200155'
    if not os.path.isfile(fileListFile) or not os.path.isfile(ISLM_cordDBFile) : 
        try: 
            Update_ISLM_Material(wdir=materialDir, cordSaveFile=localCordDB, fileListFile=fileListFile, \
                 host=host, user=user, pw=pw, cordname=1, cordfile=ISLM_cordDBFile)
            print ("* ISLM Mateiral DB was updated.")
            
        except:
            ISLM_cordDB="/home/fiper/ISLM_MAT/CordDB_SLM_PCI_v2.txt"
            print ("* Cannot access ISLM Mateiral DB.")
            pass 
    if os.path.isfile(ISLM_cordDBFile): 
        with open(ISLM_cordDBFile) as DB:
            lines=DB.readlines()
        ISLM_cordDB=lines[0].strip()

    tireGroup="PCR"
    mat_solids, mat_cords, tireGroup, BT_cord_Ga, BSD, RW, RD, SIZE, beltLift = Equivalent_density_calculation(layout)
    if "LT" in tireGroup: tireGroup="LTR"
    if "TB" in tireGroup: tireGroup="TBR"

    rimDia = GetRimDia_Size(SIZE)
    Ccd_Dia = GetCarcassDrumDia(group=tireGroup, inch=rimDia, overtype=overtype) 

    npel = []
    for el in element: 
        npel.append(el[:3])
    npel = np.array(npel)
    npn = np.array(node)

    beltHalfDia=[]
    reBtHalfDia=[]
    cc1MaxR = 0.0
    for eset in elset: 
        if ("BT" in eset[0] or "SPC" in eset[0]) and not "BTT" in eset[0]: 
            N = len(eset)
            zMax = 0
            for k in range(1, N): 
                ix =np.where(npel[:,0]==eset[k])[0][0]
                nix = np.where(npn[:,0] == npel[ix][1])[0][0]
                if zMax < npn[nix][3]: 
                    zMax = npn[nix][3]
            beltHalfDia.append([eset[0], zMax/beltLift*1000])
        if "JEC" in eset[0] or "JFC" in eset[0] or "OJF" in eset[0]: 
            N = len(eset)
            zMax = 0
            for k in range(1, N): 
                ix =np.where(npel[:,0]==eset[k])[0][0]
                nix = np.where(npn[:,0] == npel[ix][1])[0][0]
                if zMax < npn[nix][3]: 
                    zMax = npn[nix][3]
            reBtHalfDia.append([eset[0], zMax/beltLift*1000])
        if "C01" in eset[0] or "CC1" in eset[0]: 
            N = len(eset)
            for k in range(1, N): 
                ix =np.where(npel[:,0]==eset[k])[0][0]
                nix = np.where(npn[:,0] == npel[ix][1])[0][0]
                if cc1MaxR < npn[nix][3]: 
                    cc1MaxR = npn[nix][3]

    ## check OJFC is or not 
    f1 = 0; f2 = 0; f3 = 0
    for re in reBtHalfDia: 
        if "OJFC1" in re[0]: f1 = re[1]
        if "OJFC2" in re[0]: f2 = re[1]
        if "OJFC3" in re[0]: f3 = re[1]
    if f1 > 0: 
        for i, re in enumerate(reBtHalfDia): 
            if "JFC1" == re[0] : reBtHalfDia[i][1] = f1 
    if f2 > 0: 
        for i, re in enumerate(reBtHalfDia): 
            if "JFC2" == re[0] : reBtHalfDia[i][1] = f2 
    if f3 > 0: 
        for i, re in enumerate(reBtHalfDia): 
            if "JFC3" == re[0] : reBtHalfDia[i][1] = f3 


            
    cc1MaxR *= 1000
    ixn = np.where(npn[:,2]>-0.001)[0]
    ixp = np.where(npn[:,2]< 0.001)[0]
    ixs = np.intersect1d(ixn, ixp)
    center_nodes = npn[ixs]
    center_minR = np.min(center_nodes[:,3]) *1000
    IL_Ga = (cc1MaxR-center_minR)


    f=open(axi[:-4]+"-material.dat", 'w')
    
    if len(mat_solids) == 0: 

        f.write("*********************************************************\n")
        f.write("*SOLID_SECTION, (SOL, MAT)\n")
        for mat in name_solids: 
            if "BD1" in mat : 
                f.write("%4s, ABW121A,   120,  1.0\n"%(mat))
            else: 
                f.write("%4s,        ,   120,  1.0\n"%(mat))
        
        f.write("*********************************************************\n")
        f.write("*BELT_THICKNESS_SUBTRACTION,\n")
        f.write(" BETWEEN_BELTS, 4.61E-04\n")
        
        bdwidth = bdw

        try:
            if tireGroup != 'TBR': 
                f.write("*IN_MOLDING_PCI_INFO, TYPE=0 ,LOWCURE=0, BSD=   , PCIRIMW=%.1f, BDWIDTH=%.3f, PCIPRS=%s\n"%(\
                    RW, bdwidth, PCIPress))
            else: 
                f.write("*IN_MOLDING_PCI_INFO, TYPE=1 ,LOWCURE=1, BSD=   , PCIRIMW=%.1f, BDWIDTH=%.3f, PCIPRS=0\n"%(\
                    RW, bdwidth))

            f.write("*********************************************************\n")
        except:
            pass

        f.write("*CORD_FILE=%s\n"%(ISLM_cordDB))
        f.write("*REBAR_SECTION\n")
        
        for mat in name_cords: 
            if "BT" in mat:
                if 'BT1' in mat: angle = btAngles[0]
                if 'BT2' in mat: angle = btAngles[1]
                if 'BT3' in mat: angle = btAngles[2]
                if 'BT4' in mat: angle = btAngles[3]
                f.write("%4s,    BT, ES...., 120.0, 1.0, 1, %.1f, Dia.OnDrum\n"%(mat, angle))
            elif "JEC" in mat or 'JFC' in mat or 'OJF' in mat:       f.write("%4s,    RB, ET...., 120.0, 1.0, 0, 0.0, Dia.OnDrum\n"%(mat))
            elif ("C0" in mat or "CC" in mat ) and tireGroup != 'TBR':  f.write("%4s,    CC, ET...., 120.0, 1.0, 0, 90.0, Dia.OnDrum\n"%(mat))
            elif ("C0" in mat or "CC" in mat ) and tireGroup == 'TBR':  f.write("%4s,    CC, ES...., 120.0, 1.0, 1, 90.0, Dia.OnDrum\n"%(mat))
            elif "BD" in mat  :                       f.write("%4s,    NA, ET...., 120.0, 1.0, 0, 45.0, 0.0\n"%(mat))
            elif "CH1" in mat  or "SCF" in mat:                      f.write("%4s,    NA, ES...., 120.0, 1.0, 1, 30.0, 0.0\n"%(mat))
            elif "CH2" in mat  or "NCF" in mat:                      f.write("%4s,    NA, ET...., 120.0, 1.0, 0, 30.0, 0.0\n"%(mat))
            elif "SPC" in mat  :                      f.write("%4s,    NA, ES...., 120.0, 1.0, 1, 0.0,  0.0\n"%(mat))
        
        # f.write("*** Belt cord max radius lifted\n")
        for bt in beltHalfDia: 
            f.write("*** Belt cord max radius lifted, %5s=%.4f\n"%(bt[0], bt[1]*beltLift))
        if len(reBtHalfDia) > 0: 
            # f.write("*** Reinforcement cord max radius lifted\n")
            for bt in reBtHalfDia: 
                f.write("*** Reinforcement cord max radius lifted, %5s=%.4f\n"%(bt[0], bt[1]*beltLift))
        f.write("*** Under carcass gauge =%.3f\n"%(IL_Ga))
        f.write("*** Carcass drum Dia.=%.3f\n"%(Ccd_Dia))
        f.write("*** Tire Center Min.Radius=%.3f\n"%(center_minR))
        f.write("*********************************************************\n")
        f.write("*INCLUDE, INP=%s\n"%(axi.split("/")[-1]))
        f.write("*INCLUDE, INP=%s\n"%(trd.split("/")[-1]))
        f.write("*********************************************************\n")


    else:
        f.write("*********************************************************\n")
        f.write("*SOLID_SECTION, (SOL, MAT)\n")
        name_compound=[]
        if equ_Density ==1: 
            for name in name_solids:
                for mat in mat_solids: 
                    if  mat[0].strip() in name : 
                        # mat_cords.append([name,1= code, 2=toping_density, 3=cord_density, 4=line_density, 5=wt * cf/(cf+rf), 6=Area, 7=topping compd, 8=ga])
                        if "CTR" in mat[0].strip() or "CTB" in mat[0].strip(): 
                            f.write("%4s,      %s,   120,   1.0, %10.2f, 0.95, %.3e, %.5f\n"%(name, mat[1][-3:], mat[2]*1000, mat[3], mat[4]))
                            name_compound.append(mat[1][-3:])

                        elif mat[0].strip() == 'BD1': 
                            f.write("%4s,  ABW121A,   120,   1.0, %10.2f,  1.0, %.3e, %.5f\n"%(name, mat[2]*1000, mat[3], mat[4]))
                        else: 
                            f.write("%4s,      %s,   120,   1.0, %10.2f,  1.0, %.3e, %.5f\n"%(name, mat[1][-3:], mat[2]*1000, mat[3], mat[4]))
                            name_compound.append(mat[1][-3:])
                        
                        break 
        else:
            for name in name_solids:
                for mat in mat_solids: 
                    if  mat[0].strip() in name : 
                        # mat_cords.append([name,1= code, 2=toping_density, 3=cord_density, 4=line_density, 5=wt * cf/(cf+rf), 6=Area, 7=topping compd, 8=ga])
                        if "CTR" in mat[0].strip() or "CTB" in mat[0].strip(): 
                            f.write("%4s,      %s,   120,   1.0\n"%(name, mat[1][-3:]))
                            name_compound.append(mat[1][-3:])

                        elif mat[0].strip() == 'BD1': 
                            f.write("%4s,  ABW121A,   120,   1.0\n"%(name))
                        else: 
                            f.write("%4s,      %s,   120,   1.0\n"%(name, mat[1][-3:]))
                            name_compound.append(mat[1][-3:])
                        
                        break 


        f.write("*********************************************************\n")
        f.write("*BELT_THICKNESS_SUBTRACTION,\n")
        if BT_cord_Ga !=0: 
            f.write(" BETWEEN_BELTS, %.2E\n"%(BT_cord_Ga))
        else: 
            f.write(" BETWEEN_BELTS, %.2E\n"%(4.61e-04))
        bdwidth = bdw
        
        if tireGroup != 'TBR': 
            f.write("*IN_MOLDING_PCI_INFO, TYPE=0 ,LOWCURE=0, BSD=%.1f, PCIRIMW=%.1f, BDWIDTH=%.3f, PCIPRS=2.0\n"%(\
                BSD, RW, bdwidth))
        else: 
            f.write("*IN_MOLDING_PCI_INFO, TYPE=1 ,LOWCURE=1, BSD=%.1f, PCIRIMW=%.1f, BDWIDTH=%.3f, PCIPRS=0\n"%(\
                BSD, RW, bdwidth))
        f.write("*********************************************************\n")

        f.write("*CORD_FILE=%s\n"%(ISLM_cordDB))
        f.write("*REBAR_SECTION\n")
        cordCord = []
        carcassGa = 1.0
        if equ_Density ==1: 
            for name in name_cords:
                for mat in mat_cords:
                    if name == mat[0].strip() or ( "OJF" in name  and "JFC" in mat[0]):  
                        ## mat_cords.append([name, code, toping_density, cord_density, line_density])
                        name_compound.append(mat[7][-3:])
                        if "BT" in mat[0]:
                            for dia in beltHalfDia: 
                                if dia[0] == mat[0].strip(): 
                                    bthalfDia = dia[1]
                                    break 
                            if 'BT1' in mat[0]: angle = btAngles[0]
                            if 'BT2' in mat[0]: angle = btAngles[1]
                            if 'BT3' in mat[0]: angle = btAngles[2]
                            if 'BT4' in mat[0]: angle = btAngles[3]
                            f.write("%4s,    BT, %s, 120.0, 1.0, 1, %5.1f, %10.4f, %10.5e, %10.2f, %10.3f, %10.3e\n"%(\
                                    mat[0].strip(), mat[1], angle, bthalfDia, mat[4], mat[2]*1000, mat[5], mat[6]))
                            cordCord.append(mat[1])
                        elif "JEC" in mat[0] or 'JFC' in mat[0] or 'OJF' in mat[0]:  
                            for dia in reBtHalfDia: 
                                if dia[0] == mat[0].strip()  or ( "OJF" in dia[0] and "JFC" in mat[0]): 
                                    bthalfDia = dia[1]
                                    break 
                            if "OJF" in name: 
                                f.write("%4s,    RB, %s, 120.0, 1.0, 0,   0.0, %10.4f, %10.5e, %10.2f, %10.3f, %10.3e\n"%(\
                                        dia[0], mat[1], bthalfDia, mat[4], mat[2]*1000, mat[5], mat[6]))
                            else:
                                f.write("%4s,    RB, %s, 120.0, 1.0, 0,   0.0, %10.4f, %10.5e, %10.2f, %10.3f, %10.3e\n"%(\
                                        mat[0], mat[1], bthalfDia, mat[4], mat[2]*1000, mat[5], mat[6]))
                            cordCord.append(mat[1])
                        elif "C0" in mat[0] :
                            nc = float(mat[0][-1])
                            ccDia = GetCarcassDia(group=tireGroup, inch=rimDia, layer=nc, overtype=overtype, ga=mat[8]*1000, innerGa=IL_Ga, centerMinR=center_minR)   ## TBR : Side over tread based carcass drum dia.
                            if "ET" in mat[1]: 
                                f.write("%4s,    CC, %s, 120.0, 1.0, 0,  90.0, %10.4f, %10.5e, %10.2f, %10.3f, %10.3e\n"%(\
                                                                        mat[0].strip(), mat[1], ccDia/2.0, mat[4], mat[2]*1000, mat[5], mat[6]))
                            else:
                                f.write("%4s,    CC, %s, 120.0, 1.0, 1,  90.0, %10.4f, %10.5e, %10.2f, %10.3f, %10.3e\n"%(\
                                                                        mat[0].strip(), mat[1], ccDia/2.0, mat[4], mat[2]*1000, mat[5], mat[6]))
                            cordCord.append(mat[1])                                            
                        elif "BDC" in mat[0]  :                       
                            f.write("%4s,    NA, %s, 120.0, 1.0, 0,  45.0,        0.0, %10.5e, %10.2f, %10.3f, %10.3e\n"%(\
                                                                        mat[0].strip(), mat[1], mat[4], mat[2]*1000, mat[5], mat[6]))
                            cordCord.append(mat[1])
                        elif "CH" in mat[0]  :
                            if "ES" in mat[1]:                       
                                f.write("%4s,    NA, %s, 120.0, 1.0, 1,  30.0,        0.0, %10.5e, %10.2f, %10.3f, %10.3e\n"%(\
                                                                        mat[0].strip(), mat[1], mat[4], mat[2]*1000, mat[5], mat[6]))
                            else:
                                f.write("%4s,    NA, %s, 120.0, 1.0, 0,  30.0,        0.0, %10.5e, %10.2f, %10.3f, %10.3e\n"%(\
                                                                        mat[0].strip(), mat[1], mat[4], mat[2]*1000, mat[5], mat[6]))
                            cordCord.append(mat[1])
                        elif "SPC" in mat[0]  :
                            for dia in beltHalfDia: 
                                if dia[0] == mat[0].strip(): 
                                    bthalfDia = dia[1]
                                    break                       
                            f.write("%4s,    BT, %s, 120.0, 1.0, 1,  0.0, %10.4f, %10.5e, %10.2f, %10.3f, %10.3e\n"%(\
                                    mat[0].strip(), mat[1], bthalfDia, mat[4], mat[2]*1000, mat[5], mat[6]))
                            cordCord.append(mat[1])

                        break 
        else:
            for name in name_cords:
                for mat in mat_cords:
                    if name == mat[0].strip() or ("OJF" in name and "JFC" in mat[0]):  
                        ## mat_cords.append([name, code, toping_density, cord_density, line_density])
                        name_compound.append(mat[7][-3:])
                        if "BT" in mat[0]:
                            for dia in beltHalfDia: 
                                if dia[0] == mat[0].strip(): 
                                    bthalfDia = dia[1]
                                    break 
                            if 'BT1' in mat[0]: angle = btAngles[0]
                            if 'BT2' in mat[0]: angle = btAngles[1]
                            if 'BT3' in mat[0]: angle = btAngles[2]
                            if 'BT4' in mat[0]: angle = btAngles[3]
                            f.write("%4s,    BT, %s, 120.0, 1.0, 1, %5.1f, %10.4f\n"%(mat[0].strip(), mat[1], angle, bthalfDia))
                            cordCord.append(mat[1])
                        elif "JEC" in mat[0] or 'JFC' in mat[0] or 'OJF' in mat[0] : 
                            for dia in reBtHalfDia: 
                                if dia[0] == mat[0].strip()  or ("OJF" in dia[0] and "JFC" in mat[0]): 
                                    bthalfDia = dia[1]
                                    break 
                            if "OJF" in name: 
                                f.write("%4s,    RB, %s, 120.0, 1.0, 0,   0.0, %10.4f\n"%(\
                                        dia[0], mat[1], bthalfDia))
                            else: 
                                f.write("%4s,    RB, %s, 120.0, 1.0, 0,   0.0, %10.4f\n"%(\
                                        mat[0], mat[1], bthalfDia))
                            cordCord.append(mat[1])
                        elif "C0" in mat[0] :
                            nc = float(mat[0][-1])
                            carcassGa = mat[8]*1000
                            ccDia = GetCarcassDia(group=tireGroup, inch=rimDia, layer=nc, overtype=overtype, ga=mat[8]*1000, innerGa=IL_Ga, centerMinR=center_minR)   ## TBR : Side over tread based carcass drum dia.
                            if "ET" in mat[1]: 
                                f.write("%4s,    CC, %s, 120.0, 1.0, 0,  90.0, %10.4f\n"%(mat[0].strip(), mat[1], ccDia/2.0))
                            else:
                                f.write("%4s,    CC, %s, 120.0, 1.0, 1,  90.0, %10.4f\n"%(mat[0].strip(), mat[1], ccDia/2.0))
                            cordCord.append(mat[1])                                            
                        elif "BDC" in mat[0]  :                       
                            f.write("%4s,    NA, %s, 120.0, 1.0, 0,  45.0,        0.0\n"%(mat[0].strip(), mat[1]))
                            cordCord.append(mat[1])
                        elif "CH" in mat[0]  :
                            if "ES" in mat[1]:                       
                                f.write("%4s,    NA, %s, 120.0, 1.0, 1,  30.0,        0.0\n"%(mat[0].strip(), mat[1]))
                            else:
                                f.write("%4s,    NA, %s, 120.0, 1.0, 0,  30.0,        0.0\n"%(mat[0].strip(), mat[1]))
                            cordCord.append(mat[1])
                        elif "SPC" in mat[0]  :
                            for dia in beltHalfDia: 
                                if dia[0] == mat[0].strip(): 
                                    bthalfDia = dia[1]
                                    break                       
                            f.write("%4s,    BT, %s, 120.0, 1.0, 1,  0.0, %10.4f\n"%(mat[0].strip(), mat[1], bthalfDia))
                            cordCord.append(mat[1])

                        break 

        if tireGroup == "TBR": f.write("*** Belt Lift Ratio=%.3f\n"%(beltLift))
        else: f.write("*** Belt Lift Ratio=%.3f\n"%(beltLift))
        for bt in beltHalfDia: 
            f.write("*** Belt cord max radius lifted, %5s=%.4f\n"%(bt[0], bt[1]*beltLift))
        if len(reBtHalfDia) > 0: 
            for bt in reBtHalfDia: 
                f.write("*** Reinforcement cord max radius lifted, %5s=%.4f\n"%(bt[0], bt[1]*beltLift))
        f.write("*** Under carcass gauge =%.3f\n"%(IL_Ga))
        f.write("*** Carcass drum Dia.=%.3f\n"%(Ccd_Dia))
        f.write("*** #1 Carcass gauge =%.3f\n"%(carcassGa))
        f.write("*** Tire Center Min.Radius=%.3f\n"%(center_minR))
        f.write("*********************************************************\n")

        name_compound = sorted(name_compound)
        i = 1
        while i < len(name_compound):
            if name_compound[i] == name_compound[i-1]: 
                del(name_compound[i])
                continue 
            i += 1 
        for name in name_compound: 
            f.write("*INCLUDE, INP=%s/%s.PYN\n"%(materialDir, name))
        f.write("*INCLUDE, INP=%s/ABW121A.COR\n"%(materialDir))
        

        f.write("*********************************************************\n")
        f.write("*INCLUDE, INP=%s\n"%(axi.split("/")[-1]))
        f.write("*INCLUDE, INP=%s\n"%(trd.split("/")[-1]))
        f.write("*********************************************************\n")
        f.write("*STEEL_BEAD_ELSET_FOR_SUB_CYCLING=BD1\n")
        f.write("*GROOVE_DEPTH_FOR_FPC  =0.001\n")
        f.write("*RIM_FRICTION          =1.000\n")
        f.write("*ROAD_FRICTION (UO, ZP, KP, ZS, KS, ALPHA, TAUC, BETA)\n")
        f.write("0.1, 0., 0., 0., 0., 0., 0., 0.\n")
        f.write("*********************************************************\n")
        

        if os.path.isfile(fileListFile) : 
            with open(fileListFile) as mf: 
                lines = mf.readlines()
            
            List=[]
            enter = 0 
            for line in lines:
                List.append(line.strip())
            for name in name_compound: 
                exist = 0 
                for cd in List: 
                    if cd == name.strip(): 
                        exist = 1
                        break 
                if exist ==0: 
                    f.write("*** %4s is not in the material DB\n"%(name))


        if os.path.isfile(localCordDB) : 
            
            try: 
                with open(localCordDB) as matf: 
                    lines = matf.readlines()
            except:
                fp=open(localCordDB, 'r', encoding='UTF8')
                lines = fp.readlines()
                fp.close()

            cordList=[]
            enter = 0 
            for i, line in enumerate(lines):
                if "*" in line: 
                    if "OLD_SPEC_CORD_NAME" in line: 
                        enter = 1
                    else: 
                        enter = 0 
                else:
                    if enter ==1: 
                        words = line.split(",")
                        cordList.append(words[0].strip())
            for name in cordCord: 
                exist = 0 
                for cd in cordList: 
                    if cd == name.strip(): 
                        exist = 1
                        break 
                if exist ==0: 
                    f.write("*** %8s is not in the cord DB\n"%(name))

    f.close()
def Update_ISLM_Material(wdir='', cordSaveFile='', fileListFile='', host='', user='', pw='', cordname=0, cordfile='', cordDBFile=''): 
    
    # if cord =="":       cord = "/home/fiper/ISLM_MAT/CordDB_SLM_PCI_v2.txt"
    if wdir =="":       wdir =  "/home/fiper/ISLM_MAT/"
    if cordSaveFile =="" :  cordSaveFile = 'ISLM_CordDB.txt'
    if fileListFile =="" :  fileListFile = 'ISLM_materialList.txt'
    
    if host =="" :host = '10.82.66.65'
    if user =="" :user = 'h20200155'
    if pw =="" :pw = 'h20200155'

    ftp = FTP.SSHClient()
    ftp.set_missing_host_key_policy(FTP.AutoAddPolicy())
    ftp.connect(host, username=user, password=pw)
    sftp = ftp.open_sftp()

    dirList =sftp.listdir(wdir)
    
    f = open(fileListFile, "w")
    for name in dirList: 
        if ".PYN" in name.upper() or ".COR" in name.upper(): 
            f.write("%s\n"%(name[:-4]))
        if "CordDB" in name and ".txt" in name and "SLM" in name: 
            cord = wdir+"/"+name 
    f.close()
    if cordDBFile !='': 
        cord = cordDBFile  ## if input by user 

    try: 
        sftp.get(cord, cordSaveFile)
    except:
        print ("## Error to read:",cord)

    sftp.close()
    ftp.close()
    
    fp = open(cordfile, 'w')
    fp.write("%s\n"%(cord))
    fp.close()

    # print ("Update material, cordfile", cordfile)

class MESH2D: 
    def __init__(self, filename):
        self.PI = 3.14159265358979323846
        self.OD=0.0   ## ** 
        self.GD=0.0   ## ** 
        self.TDW=0.0  ## ** 
        self.TW = 0.0
        self.shoulderDrop = 0.0
        self.RightProfile=[]  ## ** 
        self.LeftProfile=[]   ## ** 
        self.TargetPatternWidth = 0.0   ## ** 
        self.L_curves = []   ## ** 
        self.R_curves = []   ## ** 
        # self.TLW =[]  ## Tread Curve(line) widths 
        # self.UTG = 0.0
        self.T3DMMODE=0
        self.shocurve_limit = 13.01E-03 
        self.l_shocurve = 0.0
        self.r_shocurve = 0.0

        self.sideNodes=[]

        self.Tread = ELEMENT()
        self.tdnodes = []
        self.Deco_start = 0
        self.Deco_end = 0 
        self.sideBtmNode =[]

        self.TieMaster = []
        self.TieSlave =[]
        self.Press = []
        self.RimContact = []
        self.IsError = 0 
        self.TieError = []
        self.beadWidth = 0.0

        self.Edge_TireProfile=[] ## outer profile 
        self.shoulderType ='R' ## R:round, S:square

        print ("############################################")
        print ("## Reading Layout Mesh file ")
        print ("############################################")
        self.Node, self.Element, self.Elset, self.Surface, self.Tie, self.TxtElset, comments = self.readlayoutmesh(filename)
        if len(self.Element.Element) ==0: 
            with open(filename) as MS: 
                lines = MS.readlines()
            
            for line in lines: 
                if "*" in line and not "**" in line: 
                    print (line, end="")
                    break 
            print ("\n# No layout mesh found.\n")
            self.IsError =  100  

            return 
        
        isSTL =0 
        if len(self.LeftProfile) ==0 or len(self.RightProfile) == 0:
            self.T3DMMODE = 1 
        else:
            if self.LeftProfile[-1][0] < 0 or 'TB' in self.group: 
                self.shoulderType ='S'
                for lp, rp in zip(self.LeftProfile, self.RightProfile) : 
                    self.TW+= lp[1]
                    self.TW+= rp[1]
                    if lp[0] == 10.0: 
                        isSTL =  1

        if self.shoulderType =='R':     print ("* Shoulder profile type : %s"%("ROUND\n"))
        else:                           print ("* Shoulder profile type : %s"%("SQUARE\n"))

        for line in comments: 
            if '**    SIZE' in line: 
                word = list(line.split(":"))[1].strip()
                print ("SIZE: %s"%(word))
            if 'PATTERN' in line: 
                word = list(line.split(":"))[1].strip()
                print ("Pattern: %s"%(word))
        if self.GD>0: print ("Tread Design Width : %.2f\nGroove Depth: %.2f"%(self.TDW*1000, self.GD*1000))
        dropDiff = 0
        if isSTL == 1: 
            dropDiff = self.CheckTBR_STL_Tangential(self.shoulderDrop, self.RightProfile)
        if dropDiff != 0 : 
            if dropDiff > 0: r = -0.5 
            else: r = 0.5
            self.LeftProfile, self.RightProfile, r= self.AddAdditionalRadiusForShoDrop(self.RightProfile,\
                 dropDiff, r=r, halfOD=self.OD/2.0)
            print ("* A curve is added to Tread curves")
            for pf in self.LeftProfile: 
                print ("  R=%.1f, Length=%.2f"%(pf[0]*1000, pf[1]*1000))
            print("")
            
        ## Preprocessing CUTE INP  ###################################################################################
        ## 
        
        TreadElset = ['CTB', 'SUT', 'CTR', 'UTR', 'TRW']
        ChaferName = ['CH1', 'CH2', 'CH3', 'SCF', 'NCF']
        Element, Elset, LROffset = ChaferDivide(self.Element.Element, ChaferName, self.Elset.Elset, self.Node.Node)
        OffsetLeftRight= LROffset
        InsertBETWEENBELTS=1 
        if InsertBETWEENBELTS == 1:

            for i, est in enumerate(Elset): 
                if est[0] == 'BETWEEN_BELTS': 
                    del(Elset[i])
                    break 

            betweenBelts = ['BETWEEN_BELTS']
            BT1=[]; BT2 = []; BT3=[]; BT4=[]; SPC=[]
            for est in Elset: 
                if est[0] =='BT1': BT1=est 
                if est[0] =='BT2': BT2=est 
                if est[0] =='BT3': BT3=est 
                if est[0] =='BT4': BT4=est 
                if est[0] =='SPC': SPC=est 
            list_el = []
            for el in Element: 
                list_el.append([el[0], el[1], el[2], el[3], el[4], el[6]])
            list_el = np.array(list_el)

            if len(BT1): 
                between = FindSolidElementBetweenMembrane(BT1, BT2, list_el)
                betweenBelts = betweenBelts + between 
            
            if len(SPC) and len(BT3): 
                between = FindSolidElementBetweenMembrane(BT2, SPC, list_el)
                betweenBelts = betweenBelts + between 
                between = FindSolidElementBetweenMembrane(SPC, BT3, list_el)
                betweenBelts = betweenBelts + between 
            else: 
                if len(BT3) : 
                    between = FindSolidElementBetweenMembrane(BT2, BT3, list_el)
                    betweenBelts = betweenBelts + between 
                if len(BT4) : 
                    between = FindSolidElementBetweenMembrane(BT3, BT4, list_el)
                    betweenBelts = betweenBelts + between 

            if len(betweenBelts)>0:
                Elset.append(betweenBelts)

        GeneralElement = ELEMENT()
        sws =  ELEMENT()
        for e in Element:
            if e[5] != "SWS":        GeneralElement.Add(e)
            else:                    sws.Add(e)
        print ("* No of 'SWS' Element : %d"%(len(sws.Element)))
        
        if len(sws.Element)>0:
            i=0
            while i < len(Element):
                if Element[i][5] == 'SWS': 
                    del(Element[i])
                    i -=1
                i+= 1

            for i, es in enumerate(Elset):
                if es[0]  == 'SWS': 
                    ElsetSWS = es 
                    del(Elset[i])

        BDmin, BDMax, Center = BeadWidth(Element, self.Node.Node)
        self.beadWidth = (BDMax-Center)*2
        # beadcorefile = "bead.tmp"
        # bd=open(beadcorefile, "w")
        # bd.writelines("%6.3f" %((BDMax-Center)*2000))
        # print ("* Bead Core Width (HK-SMART) =%.3fmm"%((BDMax-Center)*2000))
        
        # bd.close()

        MasterEdge, SlaveEdge, OutEdges, CenterNodes, FreeEdges, AllEdges, self.TieError = TieSurface(Element, self.Node.Node)

        self.Edge_TireProfile = OutEdges
        
        if len( self.TieError) > 0: 
            print ("## Error to find Tie Surface") 
            self.IsError = 1 

        Nslave = []
        for i, me in enumerate(MasterEdge): 
            me[5] = i+1 
            # print (me)
            temp = []
            for se in SlaveEdge[i]: 
                se[5] = i+1 
                temp.append(se)
                # print (" >", se)
            Nslave.append(temp)

        PressureSurface, RimContactSurface, TreadToRoadSurface = Surfaces(OutEdges, self.Node.Node, OffsetLeftRight, TreadElset, Element)

        if len(sws.Element)>0:
            AllElement=ELEMENT()
            for e in Element.Element:
                AllElement.Add(e)
            for e in sws.Element:
                AllElement.Add(e)
            allElset=ELSET()
            for es in Elset.Elset:
                allElset.Elset.append(es)
            allElset.Elset.append(ElsetSWS)
            # Mesh2DScripts.Write2DFile(Mesh2DInp, Node.Node, AllElement.Element, allElset.Elset, TreadToRoadSurface, PressureSurface, RimContactSurface, MasterEdge, SlaveEdge, OffsetLeftRight.value, CenterNodes, Comments, fullpath=mesh2dpath)
        Mesh2DInp = filename[:-4] + "-tmp.tmp"
        Comments = []
        if len(MasterEdge) != len(Nslave): 
            print ("Tie Master")
            Printlist(MasterEdge)
            print ("Tie Slave")
            Printlist(SlaveEdge)

            print (len(MasterEdge))
            print (len(SlaveEdge)) 
            return
        # print ("duplication check")
        duplel = ElementDuplicationCheck(self.Element.Element)

        self.Element.Element,  errJacobian= checkJacobian2D(self.Element.Element, np.array(self.Node.Node))
        if errJacobian != []:
            print ("## Negative Element Area")
            print ("   Node order is changed in Elements below")
            for er in errJacobian: 
                print("%d, "%(er), end="")
            print("")

        if duplel == 1:
            self.IsError = 1
        # print ("* Writing mesh '*-tmp.tmp' ")
        Write2DFile(Mesh2DInp, self.Node.Node, Element, Elset, TreadToRoadSurface, PressureSurface, RimContactSurface, MasterEdge, Nslave, OffsetLeftRight, CenterNodes, Comments=comments)
        self.TieMaster = MasterEdge
        self.TieSlave  = Nslave 
        self.Press = PressureSurface
        self.RimContact = RimContactSurface
        # print ("* Pre-processed mesh '*-tmp.tmp' is created")
        
        ################################################################################################################
        self.Node, self.Element, self.Elset, self.Surface, self.Tie, self.TxtElset, comments = self.readlayoutmesh(Mesh2DInp)
        npnd = np.array(self.Node.Node)
        self.OD = np.max(npnd[:,3])*2.0
        print ("* Layout OD = %.1f (Radius =%.1f)"%(self.OD*1000, self.OD*500.0))
        
        # self.LeftProfile, self.RightProfile, _, _, _  = self.Temp_readprofile(Mesh2DInp)

        
        # if self.shoulderType =='S': 
        #     self.ElimateSquareTread()

        # print ("############################################")
    def __del__(self): 
        pass 
    def CheckTBR_STL_Tangential(self, shoDrop, profile): 
        if shoDrop ==0: 
            return 0 
        
        if profile[-1][0] < 0: 
            del(profile[-1])
        
        _, _, drop = TD_Arc_length_calculator(profile, totalwidth=1)
        if round(shoDrop, 4) == round(drop, 4): 
            return 0 
        
        print ("* Profile Shoulder Drop =%.2f\n  Tangential Sho.Drop=%.2f, Drop shift=%.2f"%(shoDrop*1000, drop*1000, (shoDrop-drop)*1000))
        return round(drop - shoDrop, 5)

    def AddAdditionalRadiusForShoDrop(self, profile, shiftDrop, r=-0.5, halfOD=0.0): 
        if profile[-1][0] < 0: 
            del(profile[-1])
        _, tx, drop = TD_Arc_length_calculator(profile, totalwidth=1)
        ty = halfOD - drop 
        # print ("Profile End x=%.2f, drop=%.2f"%(tx*1000, drop*1000))

        
        if profile[-1][0] >=10.0:
            strline = profile[-1] 
            del(profile[-1])
        _, sx, drop = TD_Arc_length_calculator(profile, totalwidth=1)
        sy = halfOD - drop 
        # print ("Profile line start x=%.2f, drop=%.2f"%(sx*1000, drop*1000))


        tAng = atan((ty-sy)/(tx-sx)) ## tangential line의 기울기 
        sAng = atan((ty+shiftDrop-sy)/(tx-sx)) ## straight line의 기울기 
        DiffAng = sAng - tAng 

        ## (sx,sy) 점을 중심으로 회전 이동위치 (sx,sy를 원점으로 가정)
        dx = cos(DiffAng) * (tx-sx) - sin(DiffAng) * (ty-sy)
        dy = sin(DiffAng) * (tx-sx) + cos(DiffAng) * (ty-sy)

        # print("drop from end = %.2f, from R=%.2f (=%.2f)"%(dy*1000, (halfOD-sy-dy)*1000, shiftDrop*1000))

        ## straight line 방정식 :  y - sy = dy/dx (x-sx) >> y = dy/dx * x - sx *dy/dx + sy >> y=ax+b 
        a = dy/dx 
        b = -sx * a + sy 
        
        # print(" shift x=%.3f, y=%.3f inclination=%.3f, angle=%.2f"%(dx*1000, dy*1000, a, degrees(atan(a))))
        

        ## 이 직선이 앞 곡선의 r 만큼 큰 원과 (m, n)에서 만남 
        ## 앞 곡선의 원의 중심 (p, q)
        pe = [0, 0, 0, halfOD]
        tmp=[]
        for pf in profile:
            tmp.append(pf)
            start = pe
            _, dst, drop = self.TD_Arc_length_calculator(tmp, h_dist=0, totalwidth=1)
            end = [0, 0, dst, halfOD - drop] 
            centers = Circle_Center_with_2_nodes_radius(pf[0], start, end)
            if abs(centers[0][3]) > abs(centers[1][3]):    center = centers[1]
            else:                                          center = centers[0] 
            pe = end 
        
        p = center[2]; q = center[3]


        if r> 0:  r = profile[-1][0] * 0.25
       

        ## r 만큼 평행이동한 직선 방정식 : y = ax + c 
        c = b  - r / cos(atan(a))  ## r < 0 이므로 -r 
        # print (" r=%.2f, b=%.3f, c=%.3f, c-b=%.4f"%(r*1000, b*1000, c*1000, (c-b)*1000))

        ## (p,q), (m,n) 거리 = pf[0] +- r 
        ## r < 0: (m-p)^2 + (n-q)^2 = (R+abs(r))^2 
        ## r > 0: (m-p)^2 + (n-q)^2 = (R-abs(r))^2 

        A = (a*a+1)
        B = a * c - a * q - p 
        if r < 0: 
            C = c*c - 2*c*q + q*q + p*p - (profile[-1][0]+abs(r))**2 
        else: 
            C = c*c - 2*c*q + q*q + p*p - (profile[-1][0]-abs(r))**2 

        
        if r < 0: 
            m = (-B + sqrt(B*B - A*C))/A 
            n = a * m + c 
            # print (" m=%.5f, n=%.5f, sx=%.5f, sy=%.5f"%(m, n, sx, sy))
            vP =[0, 0, p, q+1.0]
        else:
            m = (-B - sqrt(B*B - A*C))/A 
            n = a * m + c 
            # print (" m=%.5f, n=%.5f, sx=%.5f, sy=%.5f"%(m, n, sx, sy))
            vP =[0, 0, p, q+1.0]

        sA = Angle_3nodes(vP, center, [0, 0, m, n])
        eA = Angle_3nodes(vP, center, [0, 0, sx, sy])
        delLc = profile[-1][0] * abs(eA-sA) ## 앞 curve 삭제 길이 
        # print ("Curve Del=%.3f, Angle end =%.2f, start=%2f"%(delLc*1000, degrees(eA), degrees(sA)))

        ix = (m + a*n - a*b) / (a*a +1)
        iy = a * ix + b 

        delLl = sqrt((ix-sx)**2 + (iy-sy)**2) ## 직선의 삭제 길이 
        # print("intersec x=%f, %f"%(ix, iy))
        # print ("line Del=%.3f"%(delLl*1000))

        profile[-1][1] -= delLc 
        profile.append([r, delLc + delLl])
        strline[1] -= delLl 
        profile.append(strline)
        # print ("STR", strline)

        # for pf in profile:
        #     print (pf)
        return profile, profile, r 


    def EliminateTread(self, filename, ptnfile, LeftProfile, RightProfile, ptnOD, ptnTDW, ptnTW, ptnGD, t3dm=0, result=1, layoutProfile=[]): 
        
        print ("############################################")
        print ("## Removing crown for pattern ")
        print ("############################################")
        # self.Node.DeleteDuplicate()
        # self.Element.DeleteDuplicate() ## **   

        # LeftProfile, RightProfile, ptnOD, ptnTDW, ptnTW, ptnGD = ReadMoldProfileFromPatternMeshFile(ptnfile)
        ## 'Model Tire TDW and Deco. Width' need to define the removal width of the tread.  import the profile and dimension of the self pattern 
        if layoutProfile ==[]: 
            self.LeftProfile, self.RightProfile, self.TDW, self.TW, self.GD  = self.Temp_readprofile(filename)  ## read target layout tread profile
        
        if len(self.LeftProfile) ==0 or len(self.RightProfile) == 0 or t3dm == 1 : 
            self.LeftProfile = LeftProfile    ## leftprofile : profile from pattern mesh file 
            self.RightProfile = RightProfile  ## rightprofile : profile from pattern mesh file 
            self.T3DMMODE = 1 

            # print(">>>>>>>>>>>>>>>>>", LeftProfile)
        else: 
            if len(self.LeftProfile) == len(LeftProfile) and len(self.RightProfile) == len(RightProfile): 
                sameprofile = 1 
                for pf, tf, pf1, tf1 in zip(self.LeftProfile, LeftProfile, self.RightProfile, RightProfile):
                    if round(pf[0], 3) != round(tf[0], 3) or round(pf[1], 4) != round(tf[1], 4) or round(pf1[0], 3) != round(tf1[0], 3) or round(pf1[1], 4) != round(tf1[1], 4): 
                        sameprofile = 0 
                if sameprofile == 1: self.T3DMMODE =  1 

        if self.TDW ==0: self.TDW = ptnTDW 
        if self.TW == 0: self.TW = ptnTW 


        ###############################################################################
        ## make the deco-curves to 1 curve.. (sum the lengths)

        ## check sum_length == TDW (in case of no sho. curve)
        
    
        self.LeftProfile, shocurve,  htdw, r_shocurve,  l_shocurve = LayoutProfileDefineForExpansion(self.LeftProfile, self.TDW/2.0, ShoR=0.05, t3dm=t3dm)
        self.RightProfile, shocurve, htdw, r_shocurve,  l_shocurve = LayoutProfileDefineForExpansion(self.RightProfile, self.TDW/2.0, ShoR=0.05, t3dm=t3dm)
        if t3dm == 0: 
            self.TDW = htdw * 2.0
        

        print ("* Crown Profile Info(Neg/Pos side)")
        for pf1, pf2 in zip(self.LeftProfile, self.RightProfile): 
            print (" R=%.1f, L=%.1f / R=%.1f, L=%.1f"%(pf1[0]*1000, pf1[1]*1000, pf2[0]*1000, pf2[1]*1000))
        print ("**********************************\n")
        ##############################################################################

        LeftLastEL = 0
        RightLastEL = 0 
        LY = 0; RY =0
        if shocurve ==0:  ## in case that curves at shoulder are not tangential  
            LeftLastEL, LY, RightLastEL, RY, Deco_curves = self.Define_Deco_curve(self.Node, self.Element, Lprofile=self.LeftProfile, Rprofile=self.RightProfile, OD=self.OD, \
                TDW=self.TDW, ptnTW=ptnTW, prfTDW=ptnTDW)
            ## Deco_curves = [L_Curve, R_curve] = [ [[0.0, s2, s3], [0.0, e2, e3], [0.0, c2, c3]], [[0.0, s2, s3], [0.0, e2, e3], [0.0, c2, c3]] ]
            ##                Curve = [curve Start position], [Curve End position], [Curve Center Position]

        pe = [0, 0, 0, self.OD/2]
        profile=[]
        Lsho=[]
        negR = 0 
        for i, pf in enumerate(self.LeftProfile):
            profile.append(pf) 
            start = pe
            _, dst, drop = self.TD_Arc_length_calculator(profile, h_dist=0, totalwidth=1)
            end = [0, 0, -dst, self.OD/2 - drop] 
            centers = Circle_Center_with_2_nodes_radius(pf[0], start, end)
            if pf[0] < 0: negR = 1
            if negR == 0:
                if abs(centers[0][3]) > abs(centers[1][3]):    center = centers[1]
                else:                                          center = centers[0] 
            else: 
                if abs(centers[0][3]) < abs(centers[1][3]):    center = centers[1]
                else:                                          center = centers[0] 
            pe = end 
            if i == len(self.LeftProfile) -1 and shocurve ==0 : 
                Lsho = [start, end, center]
            else: 
                self.L_curves.append([start, end, center])

        pe = [0, 0, 0, self.OD/2]
        profile=[]
        Rsho=[]
        negR = 0 
        for i, pf in enumerate(self.RightProfile):
            
            profile.append(pf) 
            start = pe
            _, dst, drop = self.TD_Arc_length_calculator(profile, h_dist=0, totalwidth=1)
            end = [0, 0, dst, self.OD/2 - drop] 
            centers = Circle_Center_with_2_nodes_radius(pf[0], start, end)
            if pf[0] < 0: negR = 1
            if negR == 0:
                if abs(centers[0][3]) > abs(centers[1][3]):    center = centers[1]
                else:                                          center = centers[0] 
            else: 
                if abs(centers[0][3]) < abs(centers[1][3]):    center = centers[1]
                else:                                          center = centers[0] 

            pe = end 
            if i == len(self.RightProfile) -1 and shocurve ==0 : 
                Rsho = [start, end, center]
                self.Deco_start = start 
                self.Deco_end = end
            else: 
                self.R_curves.append([start, end, center])

        self.Shoulder_Neg_Angle = 0 
        self.Shoulder_Pos_Angle = 0 

        if shocurve ==0:
            self.L_curves.append(Deco_curves[0])
            self.R_curves.append(Deco_curves[1])

            self.Shoulder_Neg_Angle = Angle_3nodes(Deco_curves[0][2], Lsho[0], Lsho[2])
            self.Shoulder_Pos_Angle = Angle_3nodes(Deco_curves[1][2], Rsho[0], Rsho[2])
            print ("* Sho. Curve Angle Left = %.2f, Right=%.2f"%(degrees(self.Shoulder_Neg_Angle), degrees(self.Shoulder_Pos_Angle)))
        elif shocurve ==1 and r_shocurve < self.shocurve_limit: 
            TLprofile =[]; TRprofile=[]  ## temp left profile, temp right profile 
            TLprofile = self.LeftProfile
            TRprofile = self.RightProfile
            tmpLeftEL, tmpLY, tmpRightEL, tmpRY, tmpDeco_curves = self.Define_Deco_curve(self.Node, self.Element, TLprofile, TRprofile, self.OD, self.TDW, ptnTW, ptnTDW, summation=0)

            pe = [0, 0, 0, self.OD/2]
            tprofile=[]
            tLsho=[]
            # Printlist(TLprofile)
            negR = 0 
            for i, pf in enumerate(TLprofile):
                tprofile.append(pf) 
                start = pe
                _, dst, drop = self.TD_Arc_length_calculator(tprofile, h_dist=0, totalwidth=1)
                end = [0, 0, -dst, self.OD/2 - drop] 
                centers = Circle_Center_with_2_nodes_radius(pf[0], start, end)
                if pf[0] < 0: negR = 1
                if negR == 0: 
                    if abs(centers[0][3]) > abs(centers[1][3]):    center = centers[1]
                    else:                                          center = centers[0] 
                else: 
                    if abs(centers[0][3]) < abs(centers[1][3]):    center = centers[1]
                    else:                                          center = centers[0] 
                pe = end 
                if i == len(TLprofile) -1  : 
                    tLsho = [start, end, center]
            
            pe = [0, 0, 0, self.OD/2]
            tprofile=[]
            tRsho=[]
            negR = 0 
            for i, pf in enumerate(TRprofile):
                
                tprofile.append(pf) 
                start = pe
                _, dst, drop = self.TD_Arc_length_calculator(tprofile, h_dist=0, totalwidth=1)
                end = [0, 0, dst, self.OD/2 - drop] 
                centers = Circle_Center_with_2_nodes_radius(pf[0], start, end)
                if pf[0] < 0: negR = 1
                if negR == 0: 
                    if abs(centers[0][3]) > abs(centers[1][3]):    center = centers[1]
                    else:                                          center = centers[0] 
                else: 
                    if abs(centers[0][3]) < abs(centers[1][3]):    center = centers[1]
                    else:                                          center = centers[0] 
                pe = end 
                if i == len(TRprofile) -1 : 
                    tRsho = [start, end, center]
                    self.Deco_start = start 
                    self.Deco_end = end 
            
            self.Shoulder_Neg_Angle = Angle_3nodes(tmpDeco_curves[0][2], tLsho[0], tLsho[2]) + self.PI / 36.0
            self.Shoulder_Pos_Angle = Angle_3nodes(tmpDeco_curves[1][2], tRsho[0], tRsho[2]) + self.PI / 36.0

            # print ("* Tilting angle Left=%.2f, Right=%.2f"%(degrees(self.Shoulder_Neg_Angle), degrees(self.Shoulder_Pos_Angle)))
            # print ("  Curve radius=%.2f"%(self.r_shocurve*1000))
            # print ("############################################")

        print (" Model  OD=%7.2f, Target  OD=%7.2f"%(ptnOD*1000, self.OD*1000))
        print (" Model  GD=%7.2f, Target  GD=%7.2f"%(ptnGD*1000, self.GD*1000))
        print (" Model TDW=%7.2f, Target TDW=%7.2f"%(ptnTDW*1000, self.TDW*1000))
        print (" Model  TW=%7.2f, Target  TW=%7.2f"%(ptnTW*1000, self.TW*1000))
        print (" Model DHW=%7.2f, Target DHW=%7.2f"%((ptnTW-ptnTDW)*500, (self.TW-self.TDW)*500))

        if self.T3DMMODE == 0: 
            # t0 = time.time()
            self.Element, self.Elset, self.Tread = self.RemoveTread(self.Element, self.Node, self.Elset, self.LeftProfile, self.RightProfile, self.TDW,\
            ModelPatternTotalWidth=ptnTW, ModelPatternDesignWidth=ptnTDW, LastLeft=LeftLastEL, LastRight=RightLastEL, LY=LY, RY=RY, debug=0)
            # t1 = time.time()
            # print ("TIME TO REMOVE %.2f"%(t1-t0))
            
        else: 
            self.Element, self.Elset, self.Tread = self.RemoveCTRUTR(self.Element, self.Elset)
        
        self.body_nodes = self.Element.Nodes(node=self.Node) 

        tread_nodes = self.Tread.Nodes(node=self.Node) 
        tdnodes = []
        for nd in tread_nodes.Node:
            tdnodes.append(nd)

        self.tdnodes = np.array(tdnodes)     ## **  

        if shocurve !=0 and self.T3DMMODE == 0:
            self.R_curves[len(self.R_curves)-1][1][2] = self.right_end[0]
            self.R_curves[len(self.R_curves)-1][1][3] = self.right_end[1]
            self.L_curves[len(self.L_curves)-1][1][2] = self.left_end[0]
            self.L_curves[len(self.L_curves)-1][1][3] = self.left_end[1]
            # print ("* Profile Tread End Position ")
            # print ("    Right : %7.3f, %7.3f"%(self.right_end[0]*1000,self.right_end[1]*1000),self.R_curves[len(self.R_curves)-1])
            # print ("    Leff  : %7.3f, %7.3f"%(self.left_end[0]*1000, self.left_end[1]*1000), self.L_curves[len(self.L_curves)-1])

        self.RemoveTieOnTread()

        if result > 0 : 
            if '/' in filename:  ms = filename.split("/")[-1].split(".")[0]
            else:                ms = filename.split("\\")[-1].split(".")[0]
            Profile = NAME(ms)
            f = open("Body_Mesh_Tread_Removed_"+Profile.name+".inp", "w")
            f.write("*NODE, SYSTEM=R\n")
            for nd in self.Node.Node: 
                f.write("%6d, %10.6f, %10.6f, %10.6f\n"%(nd[0], nd[3], nd[2], nd[1]))
            f.write("*ELEMENT, TYPE=MGAX1\n")
            for el in self.Element.Element:
                if el[6] == 2: f.write("%6d, %6d, %6d\n"%(el[0], el[1], el[2]))
            f.write("*ELEMENT, TYPE=CGAX3H\n")
            for el in self.Element.Element:
                if el[6] == 3: f.write("%6d, %6d, %6d, %6d\n"%(el[0], el[1], el[2], el[3]))
            f.write("*ELEMENT, TYPE=CGAX4H\n")
            for el in self.Element.Element:
                if el[6] == 4: f.write("%6d, %6d, %6d, %6d, %6d\n"%(el[0], el[1], el[2], el[3], el[4]))
            for eset in self.Elset.Elset: 
                ending = 0 
                for i, e in enumerate(eset): 
                    if i ==0: f.write("*ELSET, ELSET=%s\n"%(e))
                    else: 
                        f.write("%6d,"%(e))
                        if i%10 ==0: 
                            f.write("\n")
                            ending = 1 
                        else: 
                            ending = 0 
                if ending ==0: 
                    f.write("\n")

            # print ("** Body_Mesh_Tread_Removed_%s.inp is created !!!"%(Profile.name))
            print ("\n* Tread Removed layout mesh is created.")
            # print ("############################################")

    def ElimateSquareTread(self, LeftProfile, RightProfile): 
        print ("############################################")
        print ("## Removing crown for pattern (Square)")
        print ("############################################")
        # self.Node.DeleteDuplicate()
        # self.Element.DeleteDuplicate() ## **   

        if self.T3DMMODE == 1: 
            self.Element, self.Elset, self.Tread = self.RemoveCTRUTR(self.Element, self.Elset)
            self.body_nodes = self.Element.Nodes(node=self.Node) 
            self.tdnodes = self.Tread.Nodes(node=self.Node)

            self.LeftProfile = LeftProfile    ## leftprofile : profile from pattern mesh file 
            self.RightProfile = RightProfile  ## rightprofile : profile from pattern mesh file 

        else: 

            npn = np.array(self.Node.Node)
            els =[]
            ndi = []
            for el in self.Element.Element: 
                if el[5] == "CTR" or el[5] == "CTB" or el[5] == "SUT" or el[5] == "UTR" or el[5] == "TRW": 
                    ix1 = np.where(npn[:, 0] ==el[1])[0][0]
                    ix2 = np.where(npn[:, 0] ==el[2])[0][0]
                    ix3 = np.where(npn[:, 0] ==el[3])[0][0]
                    if el[4]>0: 
                        ix4 = np.where(npn[:, 0] ==el[4])[0][0]
                        cx = (npn[ix1][2]+npn[ix2][2]+npn[ix3][2]+npn[ix4][2]) / 4.0
                        cy = (npn[ix1][3]+npn[ix2][3]+npn[ix3][3]+npn[ix4][3]) / 4.0
                        nx = min([npn[ix1][2], npn[ix2][2], npn[ix3][2], npn[ix4][2]])
                        my = max([npn[ix1][2], npn[ix2][2], npn[ix3][2], npn[ix4][2]])
                    else: 
                        cx = (npn[ix1][2]+npn[ix2][2]+npn[ix3][2]) / 3.0
                        cy = (npn[ix1][3]+npn[ix2][3]+npn[ix3][3]) / 3.0
                        nx = min([npn[ix1][2], npn[ix2][2], npn[ix3][2]])
                        my = max([npn[ix1][2], npn[ix2][2], npn[ix3][2]])

                    els.append([el[0], el[1], el[2], el[3], el[4], el[6], cx, cy, nx, my])
                    if el[6] ==3: 
                        ndi.append(el[1]); ndi.append(el[2]); ndi.append(el[3])
                    else: 
                        ndi.append(el[1]); ndi.append(el[2]); ndi.append(el[3]); ndi.append(el[4])
            els = np.array(els)
            ndi = np.array(ndi)
            ndi = np.unique(ndi)

            nds = []
            cn = []
            for n in ndi: 
                ix = np.where(npn[:,0] == n)[0][0]; nds.append(npn[ix])
                if abs(npn[ix][2]) < 0.1E-3: 
                    cn.append(npn[ix]) 
            nds = np.array(nds)

            ym = 10**7
            cni = -1 
            for n in cn: 
                if n[3] < ym: 
                    ym = n[3]
                    cni = n[0]
            start = []
            for e in els: 
                if e[1] == cni or e[2] == cni or e[3] == cni or e[4] == cni : 
                    start = e
                    break 

            ix = np.where(nds[:,0]==start[1])[0][0]; n1=nds[ix]
            ix = np.where(nds[:,0]==start[2])[0][0]; n2=nds[ix]
            ix = np.where(nds[:,0]==start[3])[0][0]; n3=nds[ix]
            ix = np.where(nds[:,0]==start[4])[0][0]; n4=nds[ix]

            ec =[(n1[3]+n2[3])/2, (n2[3]+n3[3])/2, (n3[3]+n4[3])/2, (n4[3]+n1[3])/2]
            ecmin = min(ec)
            for i, c in enumerate(ec): 
                if c == ecmin: 
                    btmface = i+1 
                    break 
            bf1 = btmface+1; bf2 = btmface+2
            if bf1 > 4: bf1 -= 4 
            if bf2 > 4: bf2 -= 4 
            negDirection =[start[bf1], start[bf2]]
            bf1 = btmface; bf2 = btmface-1
            if bf2 ==0 : bf2 = 4 
            posDirection = [start[bf1], start[bf2]]

            bottoms = [start]
            cnt = 0 
            while 1:
                ix1 = np.where(els[:,1:5] == negDirection[0])[0]
                ix2 = np.where(els[:,1:5] == negDirection[1])[0]
                ix = np.intersect1d(ix1, ix2)
                if len(ix) == 2: 
                    if bottoms[len(bottoms)-1][0] == els[ix[0]][0]: nxt = els[ix[1]]
                    else: nxt = els[ix[0]]
                    bottoms.append(nxt)
                    bn1 = negDirection[0]; bn2 = negDirection[1] 
                    negDirection = []
                    if nxt[1] != bn1 and nxt[1] != bn2: 
                        negDirection.append(nxt[1])
                    if nxt[2] != bn1 and nxt[2] != bn2: 
                        negDirection.append(nxt[2])
                    if nxt[3] != bn1 and nxt[3] != bn2: 
                        negDirection.append(nxt[3])
                    if nxt[4] != bn1 and nxt[4] != bn2: 
                        negDirection.append(nxt[4])
                elif len(ix) > 2: 
                    print ("## Too many element with node %d, %d"%(negDirection[0], negDirection[1]))
                    for x in ix: 
                        print ("  %d"%(els[x][0]), end="")
                    print("")
                    break 
                else:
                    break ## end searching  
                cnt += 1
                if cnt > 200: 
                    print ("## Too many iteration to search tread bottom.")
                    break 
            
            tmp = [start]
            cnt = 0 
            while 1:
                ix1 = np.where(els[:,1:5] == posDirection[0])[0]
                ix2 = np.where(els[:,1:5] == posDirection[1])[0]
                try: 
                    ix = np.intersect1d(ix1, ix2)
                except: 
                    print ("## btm f=%d node %d, %d"%(btmface, posDirection[0], posDirection[1]))
                    print ("center el", start)
                    for x in ix1: 
                        print (els[x]) 
                    print ("**************")
                    for x in ix2: 
                        print (els[x]) 
                    return 
                if len(ix) == 2: 
                    if tmp[len(tmp)-1][0] == els[ix[0]][0]: nxt = els[ix[1]]
                    else: nxt = els[ix[0]]
                    tmp.append(nxt)
                    bn1 = posDirection[0]; bn2 = posDirection[1] 
                    posDirection = []
                    if nxt[1] != bn1 and nxt[1] != bn2: 
                        posDirection.append(nxt[1])
                    if nxt[2] != bn1 and nxt[2] != bn2: 
                        posDirection.append(nxt[2])
                    if nxt[3] != bn1 and nxt[3] != bn2: 
                        posDirection.append(nxt[3])
                    if nxt[4] != bn1 and nxt[4] != bn2: 
                        posDirection.append(nxt[4])
                elif len(ix) > 2: 
                    print ("## Too many element with node %d, %d"%(posDirection[0], posDirection[1]))
                    for x in ix: 
                        print ("  %d"%(els[x][0]), end="")
                    print("")
                    break 
                else:
                    break ## end searching  
                cnt += 1
                if cnt > 200: 
                    print ("## Too many iteration to search tread bottom.")
                    break 
            del(tmp[0])

            bottoms += tmp 
            
            treads=[]
            for el in bottoms : #els.append([el[0], el[1], el[2], el[3], el[4], el[6], cx, cy, nx, ny])
                ix1 = np.where(els[:,6]>=el[8])[0]
                ix2 = np.where(els[:,6]<=el[9])[0]
                ux = np.where(els[:,7]>= el[7])[0]
                ix = np.intersect1d(ix1, ix2)
                ix = np.intersect1d(ix, ux)
                for x in ix: 
                    treads.append(els[x][0])
                    
            treads = np.array(treads)
            treads = np.unique(treads)

            axi=ELEMENT(); trd=ELEMENT()

            bnds = []
            for el in self.Element.Element: 
                ix = np.where(treads[:]==el[0])[0]
                if len(ix) :  
                    trd.Add(el)
                else:         
                    axi.Add(el)
                    bnds.append(el[1]); bnds.append(el[2])
                    if el[3] > 0: bnds.append(el[3])
                    if el[4] > 0: bnds.append(el[4])
            bnds = np.array(bnds) ## body nodes
            bnds = np.unique(bnds)


            NELSET=ELSET()
            for el in axi.Element: 
                NELSET.Add(el[0], el[5])
            
            for iset in self.Elset.Elset:
                if iset[0] != "CTB" and iset[0] != "CTR" and iset[0] != "SUT" and iset[0] != "UTR" and iset[0] != "TRW" :
                    f =0 
                    for ist in NELSET.Elset : 
                        if ist[0] == iset[0]: 
                            f = 1
                            break 
                    if f==0: 
                        NELSET.Elset.append(iset)

            # for eset in NELSET.Elset: 
            #     print (">> ", eset[0], eset[1])

            self.Element.Element = axi.Element 
            self.Tread.Element = trd.Element 
            self.Elset.Elset = NELSET.Elset  

            self.RemoveTieOnTread()

            i = 0 
            self.body_nodes = NODE()
            while i < len(self.Node.Node): 
                ix = np.where(bnds==self.Node.Node[i][0])[0]
                if len(ix): 
                    self.body_nodes.Node.append(self.Node.Node[i])
                i += 1 
            self.tdnodes = self.Tread.Nodes(node=self.Node)

        pe = [0, 0, 0, self.OD/2]
        profile=[]
        Lsho=[]
        # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        negR = 0 
        for i, pf in enumerate(self.LeftProfile):
            if i == len(self.LeftProfile)-1  and pf[0] < 0 : 
                break 
            else: 
                # print(pf)
                profile.append(pf) 
                start = pe
                _, dst, drop = self.TD_Arc_length_calculator(profile, h_dist=0, totalwidth=1)
                end = [0, 0, -dst, self.OD/2 - drop] 
                centers = Circle_Center_with_2_nodes_radius(pf[0], start, end)
                if pf[0] < 0: negR = 1
                if negR == 0: 
                    if abs(centers[0][3]) > abs(centers[1][3]):    center = centers[1]
                    else:                                          center = centers[0] 
                else: 
                    if abs(centers[0][3]) < abs(centers[1][3]):    center = centers[1]
                    else:                                          center = centers[0] 
                pe = end 
                self.L_curves.append([start, end, center])


        pe = [0, 0, 0, self.OD/2]
        profile=[]
        Rsho=[]
        negR = 0 
        for i, pf in enumerate(self.RightProfile):
            if i == len(self.LeftProfile)-1  and pf[0] < 0 : 
                break 
            else:
                profile.append(pf) 
                start = pe
                _, dst, drop = self.TD_Arc_length_calculator(profile, h_dist=0, totalwidth=1)
                end = [0, 0, dst, self.OD/2 - drop] 
                # print ("%d, r,%.6f, dist,%.6f, drop,%.6f, py, %.6f"%(i+1, pf[0], dst, drop, end[3]))
                centers = Circle_Center_with_2_nodes_radius(pf[0], start, end)
                if pf[0] < 0: negR = 1
                if negR == 0:  
                    if abs(centers[0][3]) > abs(centers[1][3]):    center = centers[1]
                    else:                                          center = centers[0] 
                else: 
                    if abs(centers[0][3]) < abs(centers[1][3]):    center = centers[1]
                    else:                                          center = centers[0] 
                pe = end 
                self.R_curves.append([start, end, center])
        # print (" circle point : start x, y, end x, y, center x, y, R=%.5f"%(self.OD/2))
        # for cv in self.R_curves: 
        #     print ("%.6f, %6f, %6f, %6f, %6f, %6f"%(cv[0][2], cv[0][3], cv[1][2], cv[1][3], cv[2][2], cv[2][3]))

    def RemoveTieOnTread(self): 
        ## Remove tie on the removed tread 
        # print ("DELETING TIE ON TREAD")
        i = 0 
        while i < len(self.TieMaster): 
            for el in self.Tread.Element: 
                if el[0] == self.TieMaster[i][4] : 
                    # print ("M: ", self.TieMaster[i])
                    # print ("S: ", self.TieSlave[i])
                    del(self.TieMaster[i]) 
                    del(self.TieSlave[i])
                    j = 0 
                    while j < len(self.Surface.Surface): 
                        if self.Surface.Surface[j][0] == self.Tie.Tie[i][2]: 
                            del(self.Surface.Surface[j]) 
                            break 
                        j += 1 
                    j = 0 
                    while j < len(self.Surface.Surface): 
                        if self.Surface.Surface[j][0] == self.Tie.Tie[i][1]: 
                            del(self.Surface.Surface[j]) 
                            break 
                        j += 1 

                    del(self.Tie.Tie[i])
                    i -= 1 
                    break 
            i += 1 

        i = 0 
        while i < len(self.TieSlave): 
            f = 0
            k = 0 
            while k < len(self.TieSlave[i]): 
                for el in self.Tread.Element: 
                    if el[0] == self.TieSlave[i][k][4]: 
                        # print ("*S: ", self.TieSlave[i][k], " in", self.TieSlave[i][0])
                        del(self.TieSlave[i][k])
                        f = 1 
                        k -= 1

                        j = 0
                        while j < len(self.Surface.Surface): 
                            if self.Surface.Surface[j][0] == self.Tie.Tie[i][1]: # check if the name of surface and tie are the same or not 
                                m = 1
                                while m < len(self.Surface.Surface[j]): 
                                    if self.Surface.Surface[j][m][0] == el[0]: 
                                        del(self.Surface.Surface[j][m])
                                        break 
                                    m += 1 
                            j += 1

                        break 
                k += 1

            ##  testing if nothing left in self.TieSlave[i]
            # if f ==1 : 
            #     k = 0 
            #     while k < len(self.TieSlave[i]):
            #         del(self.TieSlave[i][k]) 
            ################################################
                
            if len(self.TieSlave[i]) ==0: 
                del(self.TieSlave[i])
                del(self.TieMaster[i])
                j = 0 
                while j < len(self.Surface.Surface): 
                    if self.Surface.Surface[j][0] == self.Tie.Tie[i][2]: 
                        # print ("Tie[i][2]:", self.Surface.Surface[j])
                        del(self.Surface.Surface[j]) 
                        break 
                    j += 1 
                j = 0 
                while j < len(self.Surface.Surface): 
                    if self.Surface.Surface[j][0] == self.Tie.Tie[i][1]: 
                        # print ("Tie[i][1]:", self.Surface.Surface[j])
                        del(self.Surface.Surface[j]) 
                        break 
                    j += 1 

                del(self.Tie.Tie[i])

                i -= 1
            i += 1
        
    def readlayoutmesh(self, filename): 
        with open(filename) as INP:
            lines = INP.readlines()

        Node = NODE()
        Element = ELEMENT()
        Elset = ELSET()
        Surface = SURFACE()
        Tie = TIE()
        TxtElset =[]
        comments=[]

        x = 2; y=3
        scaling_factor = 0.001 

        cmd = ""
        name = ""
        profileDone = 0 
        if self.RightProfile != []: profileDone = 1
        for li, line in enumerate(lines) : 
            if "**" in line: 
                comments.append(line)
                if "SIZE    " in line : 
                    word = list(line.split(":"))[1].strip()
                    self.size = word
                elif "CLASS_CODE" in line:
                    word = list(line.split(":"))[1].strip()
                    self.group = word
                elif "PATTERN" in line: 
                    word = list(line.split(":"))[1].strip()
                    self.pattern = word
                elif "GROOVE DEPTH" in line: 
                    word = list(line.split(":"))[1].strip()
                    self.GD = float(word) /1000
                elif "TREAD DESIGN WIDTH" in line: 
                    word = list(line.split(":"))[1].strip()
                    self.TDW = round(float(word)/1000, 6)
                if "CAVITY_OD" in line: 
                    word = list(line.split(":"))[1].strip()
                    self.OD = round(float(word)/1000, 6)
                elif "SHOULDER" in line and "DROP" in line: 
                    word = list(line.split(":"))[1].strip()
                    self.shoulderDrop = round(float(word)/1000, 6)
                elif "PROFILE_LHS" in line: command="left"
                elif "PROFILE_RHS" in line: command="right"
                elif "TR :" in line or "** TR, TW" in line:  ## self.RightProfile=[]  ## **   self.LeftProfile=[]   ## ** 
                    if command == "left": 
                        line = list(line.split(":"))[1]
                        word = list(line.split(","))
                        R = round(float(word[0].strip())*scaling_factor, 5)
                        # if R == 10.0: R*= 1000
                        if profileDone ==0:  self.RightProfile.append([R, round(float(word[1].strip())*scaling_factor, 9)])
                    if command == "right": 
                        line = list(line.split(":"))[1]
                        word = list(line.split(","))
                        R = round(float(word[0].strip())*scaling_factor, 5)
                        # if R == 10.0: R*= 1000
                        if profileDone ==0: self.LeftProfile.append([R, round(float(word[1].strip())*scaling_factor, 9)])

                else: continue 
            elif "*NODE" in line.upper() and not "OUTPUT" in line.upper() and not "PRINT" in line.upper() and not "FILE" in line.upper(): cmd = "ND"
            elif "*ELEMENT" in line.upper() and "MGAX1" in line.upper(): cmd = "EL2"
            elif "*ELEMENT" in line.upper() and "CGAX3H" in line.upper(): cmd = "EL3"
            elif "*ELEMENT" in line.upper() and "CGAX4H" in line.upper(): cmd = "EL4"
            elif "*NSET" in line.upper(): cmd = "NS"
            elif "*ELSET" in line.upper(): 
                nextline = lines[li+1].split(",")
                try: 
                    nextnumber = int(nextline[0]) 
                    cmd = "ES"
                    word = list(line.split(","))
                    name = word[1].split("=")[1].strip()
                    Elset.AddName(name)
                except:
                    cmd = 'ELSE'

            elif "*SURFACE" in line.upper() and "ELEMENT" in line.upper() and "TYPE" in line.upper() : 
                nextline = lines[li+1].split(",")
                try: 
                    nextnumber = int(nextline[0]) 

                    cmd = "SF"
                    word = list(line.split(","))
                    name = word[2].split("=")[1].strip()
                    Surface.AddName(name)
                except: 
                    cmd = 'ELSE' 

            elif "*TIE" in line.upper(): 
                cmd ="TI"
                word = list(line.split(","))
                if len(word) == 3: name = word[2].split("=")[1].strip()
                elif len(word) ==2: name = word[1].split("=")[1].strip()

            elif "*" in line: cmd = "ELSE"
            else:
                word = list(line.split(","))
                for i, w in enumerate(word): 
                    word[i] = w.strip()
                if cmd == "ND":
                    if float(word[3]) ==0 and float(word[2]) ==0 and float(word[1]) ==0: 
                        print ("## ERROR: ", line[:-1])
                        continue 
                    Node.Add([int(word[0]), float(word[3]), float(word[2]), float(word[1])])
                if cmd == "EL2": 
                    if int(word[1]) == 0 or int(word[2]) == 0 : 
                        print ("## ERROR: ", line[:-1])
                        continue 
                    Element.Add([int(word[0]), int(word[1]), int(word[2]), 0, 0, "", 2, 0, 0, 0])
                if cmd == "EL3": 
                    if int(word[1]) == 0 or int(word[2]) == 0 or int(word[3]) == 0 : 
                        print ("## ERROR: ", line[:-1])
                        continue 
                    Element.Add([int(word[0]), int(word[1]), int(word[2]), int(word[3]), 0, "", 3, 0, 0, 0])
                if cmd == "EL4": 
                    if int(word[1]) == 0 or int(word[2]) == 0 or int(word[3]) == 0 or int(word[4]) == 0 : 
                        print ("## ERROR: ", line[:-1])
                        continue 
                    Element.Add([int(word[0]), int(word[1]), int(word[2]), int(word[3]), int(word[4]), "", 4, 0, 0, 0])
                if cmd == "ES": 
                    try: 
                        for w in word:
                            Elset.AddNumber(int(w), name)
                    except:
                        TxtElset.append([name, line.strip()])
                if cmd == "SF": 
                    Surface.AddSurface(name, int(word[0]), word[1])
                if cmd == "TI":
                    Tie.Add(name, word[0], word[1])

        for i in range(len(Elset.Elset)):
            fd = 0 
            for cm in TireRubberComponents: 
                if cm == Elset.Elset[i][0]: 
                    fd =1 
                    break 
            if fd == 0: 
                for cm in TireCordComponents: 
                    if cm == Elset.Elset[i][0]: 
                        fd =1 
                        break 
            if fd ==1:
                for j in range(1, len(Elset.Elset[i])):
                    for k in range(len(Element.Element)):
                        if Elset.Elset[i][j] == Element.Element[k][0]:
                            Element.Element[k][5] = Elset.Elset[i][0]
                            break

        if self.GD == 0: self.GD = 1.0E-03

        # t = time.time()
        nids = []
        for el in Element.Element: 
            nids.append(el[1]); nids.append(el[2])
            if el[3]>0: nids.append(el[3])
            if el[4]>0: nids.append(el[4])

        nids = np.array(nids)
        nids = np.unique(nids)
        nodes = np.array(Node.Node)
        tN = NODE()
        for nd in nids: 
            try:
                ix = np.where(nodes[:,0] == nd)[0][0]
            except:
                print(nd, " Node is not found!!! ")
                continue 
            tN.Add(Node.Node[ix]) 
        # t1 = time.time()
        # print ("sorting nodes %.2f"%(t1-t))

        return tN, Element, Elset, Surface, Tie, TxtElset, comments

        # return LeftProfile, RightProfile, tdw, tw, Diameter*scaling_factor, GD
    def Temp_readprofile(self, layoutmeshfile): 
        with open(layoutmeshfile) as INP:
            lines = INP.readlines()

        LeftProfile = []
        RightProfile = []
        scaling_factor = 0.001 
        Diameter = 0 
        command = ""
        GD = 0 
        tdw=0
        for line in lines : 
            if "**" in line: 
                if "PROFILE_SCALING" in line: 
                    word = list(line.split(":"))
                    scaling_factor = float(word[1].strip())
                    # print ("scaling factor=%f"%(scaling_factor))
                    continue 
                if "CAVITY_OD" in line: 
                    word = list(line.split(":"))
                    Diameter = float(word[1].strip()) 
                    continue 
                if "GROOVE DEPTH" in line: 
                    word = list(line.split(":"))
                    GD = float(word[1].strip()) /1000
                    continue 
                if "TREAD DESIGN WIDTH" in line: 
                    word = list(line.split(":"))
                    tdw = float(word[1].strip()) /1000
                    # print ("Profile TDW", tdw)
                    continue 

                if "PROFILE_LHS" in line: command="left"
                elif "PROFILE_RHS" in line: command="right"
                elif "TR :" in line or "** TR, TW" in line: 
                    if command == "left": 
                        line = list(line.split(":"))[1]
                        word = list(line.split(","))
                        R = round(float(word[0].strip())*scaling_factor, 5)
                        if R == 10.0: R*= 1000
                        LeftProfile.append([R, round(float(word[1].strip())*scaling_factor, 9)])
                    if command == "right": 
                        line = list(line.split(":"))[1]
                        word = list(line.split(","))
                        R = round(float(word[0].strip())*scaling_factor, 5)
                        if R == 10.0: R*= 1000
                        RightProfile.append([R, round(float(word[1].strip())*scaling_factor, 9)])
                else:
                    pass                    

        if tdw ==0: 
            twarc = 0 
            for pf in LeftProfile:
                if pf[0] > 50.0E-3: tdw += pf[1]
                else: 
                    tdw += pf[1]/2.0
                    twarc = 1
                    break 
            for pf in RightProfile:
                if pf[0] > 50.0E-3: tdw += pf[1]
                else: 
                    tdw += pf[1]/2.0
                    twarc = 1
                    break 
            if twarc == 0: 
                tdw = 0 
                for i, pf in enumerate(LeftProfile):
                    if i == len(LeftProfile)  : 
                        pass
                    tdw += pf[1]
                for pf in RightProfile:
                    if i == len(RightProfile) : 
                        pass     
                    tdw += pf[1]
                      
            
            tdw = round(tdw, 6)/1000

        tw=0
        LP = []
        psum = 0.0 
        enext = 0 
        for pf in LeftProfile:
            psum += pf[1]
            tw += pf[1]
            LP.append(pf) 
            # if enext == 1: break 
            if pf[0] < 50.E-03 or psum >= tdw/2.0: 
                enext =1 
            
        RP = []
        psum = 0.0 
        enext = 0 
        for pf in RightProfile:
            psum += pf[1]
            tw += pf[1]
            RP.append(pf)
            # if enext == 1: break 
            if pf[0] < 50.E-03 or psum >= tdw/2.0: 
                enext =1 

        if GD ==0: GD = 1.0E-03

        return LP, RP, tdw, tw,  GD
    def Define_PatternWidth(self, LeftProfile, RightProfile, TDW, ModelPatternTotalWidth, ModelPatternDesignWidth): 
        pattern_deco_halfwidth = (ModelPatternTotalWidth - ModelPatternDesignWidth)/2.0

        profile_width_L, maxLdist, _ = self.TD_Arc_length_calculator(LeftProfile, totalwidth=1)
        profile_width_R, maxRdist, _ = self.TD_Arc_length_calculator(RightProfile, totalwidth=1)

        
        profile_deco_halfwidth = ((profile_width_L+profile_width_R) - TDW  ) / 2.0 

        width_range = 0.6
        step = 0 

        prev = 0 
        if prev == 1: 

            if round(pattern_deco_halfwidth, 3) <= round(profile_deco_halfwidth, 3)  : 
                if pattern_deco_halfwidth > 20E-03 : 
                    target_halfwidth =  TDW/2 + profile_deco_halfwidth * 0.7
                    step = 2
                else:                                
                    target_halfwidth =  TDW/2 + pattern_deco_halfwidth 
                    step = 3
            elif profile_deco_halfwidth > 30E-03 and pattern_deco_halfwidth > 30E-03: 
                target_halfwidth =  TDW/2 +  profile_deco_halfwidth *0.8
                step = 4
            else:                      
                target_halfwidth =  TDW/2 + profile_deco_halfwidth *0.8
                step = 5
        else: 
            if pattern_deco_halfwidth <= profile_deco_halfwidth * 0.7 : 
                target_halfwidth =  TDW/2 + pattern_deco_halfwidth 
                step = 11 
            else: 
                target_halfwidth =  TDW/2 + profile_deco_halfwidth * 0.7 
                step = 12

            # print ("L = %.1f, R = %.1f"%(profile_width_L*1000, profile_width_R*1000))
            # print ("  70%% Profile =%.1f"%(profile_deco_halfwidth * 0.7*1000))


        print ("\n* Profile deco half width = %7.3f (def=%d)\n  (Half TW=%7.3f, Half Deco Width=%7.3f)"%(target_halfwidth*1000, step, TDW/2.0*1000, (target_halfwidth-TDW/2)*1000))
        print ("* Profile deco half width=%7.3fmm"%(profile_deco_halfwidth*1000))
        print ("* Pattern deco half width=%7.3fmm"%(pattern_deco_halfwidth*1000))

        return target_halfwidth
    def Define_Deco_curve(self, nd, el, Lprofile=[], Rprofile=[], OD=0.0, TDW=0.0, ptnTW=0.0, prfTDW=0.0, summation=1): 
        ## in case that curves at shoulder are not tangential 

        npn = np.array(nd.Node)
        R = OD/2.0

        # LayoutOuter = el.OuterEdge(nd)
        LayoutOuter = self.Edge_TireProfile
        # self.Edge_TireProfile = LayoutOuter
        # print (LayoutOuter)

        ond = []
        OuterEdge=EDGE()
        for ed in LayoutOuter: 
            if ed[2] == "CTR" or ed[2] == "CTB" or ed[2] == "UTR" or ed[2] == "SUT" or ed[2] == "TRW" or ed[2] == "BSW": 
                ix = np.where(npn[:,0] == float(ed[0]))[0][0]
                ond.append(npn[ix])
                ix = np.where(npn[:,0] == float(ed[1]))[0][0]
                ond.append(npn[ix])
                OuterEdge.Add(ed)

        ond = np.array(ond)

        deco = Lprofile[-1]
        td_profile = Lprofile[:-1]

        tdw, dist, drop = self.TD_Arc_length_calculator(td_profile, totalwidth=1)
        ## arc width, lateral, vertical position of arc of Tread Design Widths   

        target_half_width  = self.Define_PatternWidth(Lprofile, Rprofile, TDW, ptnTW, prfTDW)
        deco[1] = target_half_width - tdw
        if deco[1] < 0.001:  deco[1] = 0.001
        # print ("########  Left Total Half width without last curve=%7.2f, Distance from Center=%7.2f, Drop=%7.2f"%(tdw*1000, dist*1000, drop*1000), "\n######## Last_Profile: R=%6.2f, Length=%6.2f"%(deco[0]*1000, deco[1]*1000 ))

        mindist = 10.0E10 
        LeftY = 0.0
        LeftZ = 0.0 
        tn = []
        for n in ond: 
            if n[2] < -dist: 
                length = sqrt((-dist-n[2])**2 + (R - drop - n[3])**2)
                # print ("n2_y=%7.2f, n2_x=%7.2f, length=%7.2f, deco profile length=%7.2f, nx=%7.3f, ny=%7.3f"%(n[2]*1000, n[3]*1000, length*1000, deco[1]*1000, dist*1000, (R - drop)*1000))
                if abs(length - deco[1]*0.99) < mindist:
                    mindist = abs(length - deco[1]) 
                    tn = n 
                    LeftY = n[2]
                    LeftZ = n[3] 
        LeftEL = 0 
        for ed in OuterEdge.Edge: 
            if ed[0] == int(tn[0]): 
                # print (ed)
                LeftEL=ed[4]
                break 

        s2 = -dist; s3 = R - drop  
        e2 = LeftY; e3 = LeftZ  

        N1 = [0, 0.0, -dist, R - drop  ]
        N2 = [0, 0.0, LeftY, LeftZ]
        centers = Circle_Center_with_2_nodes_radius(deco[0], N1, N2, xy=23)

        if abs(centers[0][3]) > abs(centers[1][3]):    center = centers[1]
        else:                                          center = centers[0] 

        c2 = center[2]; c3 = center[3]
        L_curve = [[0, 0.0, s2, s3], [0, 0.0, e2, e3], [0, 0.0, c2, c3]]   ## s : start, e : end, c : center 

        if summation ==1: self.TargetPatternWidth += deco[0] * Angle_3nodes([0, 0.0, s2, s3],  [0, 0.0, c2, c3], [0, 0.0, e2, e3]) + tdw
        # print ("####### Half Profile Width for pattern = %.3f"%(self.TargetPatternWidth*1000))

        deco = Rprofile[-1]
        td_profile = Rprofile[:-1]

        print ("* Left Last Tread EL to delete =%4d, \n  Distance from Center=%7.3f, drop=%7.3f"%(LeftEL, dist*1000, drop*1000))

        tdw, dist, drop = self.TD_Arc_length_calculator(td_profile, totalwidth=1)
        deco[1] = target_half_width - tdw
        if deco[1] < 0.001:   deco[1] = 0.001
        # print ("######## Right Total Half width without last curve=%7.2f, Distance from Center=%7.2f, Drop=%7.2f"%(tdw*1000, dist*1000, drop*1000), "\n######## Last_Profile: R=%6.2f, Length=%6.2f"%(deco[0]*1000, deco[1]*1000 ))

        mindist = 10.0E10 
        RightY = 0.0
        RightZ = 0.0 
        tn = []
        for n in ond: 
            if n[2] > dist: 
                length = sqrt((dist-n[2])**2 + (R - drop - n[3])**2)
                # print ("n2_y=%7.2f, n2_x=%7.2f, length=%7.2f, deco profile length=%7.2f, nx=%7.3f, ny=%7.3f"%(n[2]*1000, n[3]*1000, length*1000, deco[1]*1000, dist*1000, (R - drop)*1000))
                if abs(length - deco[1]*0.99) < mindist:
                    mindist = abs(length - deco[1]) 
                    tn = n 
                    RightY = n[2]
                    RightZ = n[3]
        RightEL = 0 
        for ed in OuterEdge.Edge: 
            if ed[1] == int(tn[0]): 
                RightEL=ed[4]
                break 

        s2 = dist;  s3 = R - drop  
        e2 = RightY; e3 = RightZ  

        N1 = [0, 0.0, dist,  R - drop]
        N2 = [0, 0.0, RightY, RightZ]
        centers = Circle_Center_with_2_nodes_radius(deco[0], N1, N2, xy=23)
        if abs(centers[0][3]) > abs(centers[1][3]):    center = centers[1]
        else:                                          center = centers[0]  
        c2 = center[2]; c3 = center[3]
            
        R_curve = [[0, 0.0, s2, s3], [0, 0.0, e2, e3], [0, 0.0, c2, c3]]     ## s : start, e : end, c : center 
        if summation ==1: self.TargetPatternWidth += deco[0] * Angle_3nodes([0, 0.0, s2, s3],  [0, 0.0, c2, c3], [0, 0.0, e2, e3]) + tdw
        
        print ("* Right Last Tread EL to delete =%4d, \n  Distance from Center=%7.3f, drop=%7.3f"%(RightEL, dist*1000, drop*1000))
        print ("* Profile Width for pattern = %.3f"%(self.TargetPatternWidth*1000))
        return LeftEL, LeftY, RightEL, RightY, [L_curve, R_curve]
    def Searching_Upper_elements(self, el, solids, nodes, el2remove=[], btm_face=0, show=0, parallel=0 ): 
        ix1 = np.where(nodes[:,0] == el[1])[0][0]; n1 = nodes[ix1]
        ix2 = np.where(nodes[:,0] == el[2])[0][0]; n2 = nodes[ix2]
        ix3 = np.where(nodes[:,0] == el[3])[0][0]; n3 = nodes[ix3]
        if el[4] >0:  ix4 = np.where(nodes[:,0] == el[4])[0][0]; n4 = nodes[ix4]
        # nodes=[n1, n2, n3, n4]
        x =2; y=3 
        restrain = 0 
        # if el[0] == 522 : show = 1
        # else: show = 0 
        # if el[0] == 2788 or el[0] == 2855  or el[0] == 2871 : 
        #     print (">>>> %d"%(el[0]))
        #     show = 1
        if show==1: 
            print ("\n   START : ", el, " bottom face=",  btm_face)
            # print ("    %d, %7.3f, %7.3f, %7.3f"%(n1[0], n1[1]*1000,  n1[2]*1000,  n1[3]*1000 ))
            # print ("    %d, %7.3f, %7.3f, %7.3f"%(n2[0], n2[1]*1000,  n2[2]*1000,  n2[3]*1000 ))
            # print ("    %d, %7.3f, %7.3f, %7.3f"%(n3[0], n3[1]*1000,  n3[2]*1000,  n3[3]*1000 ))
            # print ("    %d, %7.3f, %7.3f, %7.3f"%(n4[0], n4[1]*1000,  n4[2]*1000,  n4[3]*1000 ))
        if  el[4] >0:
            if btm_face ==0: 
                if   n1[x] > n2[x] and n4[x] > n3[x] and n3[y] > n2[y] and n4[y] > n1[y]: f =1 
                elif n2[x] > n3[x] and n4[x] < n1[x] and n1[y] > n2[y] and n4[y] > n3[y]: f =2
                elif n2[x] > n1[x] and n3[x] > n4[x] and n1[y] > n4[y] and n2[y] > n3[y]: f =3 
                elif n4[x] > n1[x] and n3[x] > n2[x] and n3[y] > n4[y] and n2[y] > n1[y]: f =4 
                else:
                    if abs(n1[x] - n2[x]) < abs(n1[y] - n2[y]): 
                        if  n3[y] > n2[y] and n4[y] > n1[y]: f =1 
                    elif abs(n3[x] - n2[x]) < abs(n3[y] - n2[y]): 
                        if n2[y] > n1[y] and n3[y] > n4[y]: f =4
                    elif abs(n4[x] - n3[x]) < abs(n4[y] - n3[y]) : 
                        if n1[y] > n4[y] and n2[y] > n3[y]: f =3 
                    elif abs(n1[x] - n4[x]) < abs(n1[y] - n4[y]) : 
                        if n4[y] > n3[y] and n1[y] > n2[y]: f =4 
                    else: 
                        print ("!!!! ERROR No FOUND BOTTOM FACE. ")
                        print ("    ", el)
                        print ("    %d, %7.3f, %7.3f, %7.3f"%(n1[0], n1[1]*1000,  n1[2]*1000,  n1[3]*1000 ))
                        print ("    %d, %7.3f, %7.3f, %7.3f"%(n2[0], n2[1]*1000,  n2[2]*1000,  n2[3]*1000 ))
                        print ("    %d, %7.3f, %7.3f, %7.3f"%(n3[0], n3[1]*1000,  n3[2]*1000,  n3[3]*1000 ))
                        print ("    %d, %7.3f, %7.3f, %7.3f"%(n4[0], n4[1]*1000,  n4[2]*1000,  n4[3]*1000 ))
                        sys.exit()
                bf = f
            else: 
                bf = f = btm_face 
            # print (el)
            inext = Element2D_NextElement(el, solids, nodes, start=f, next=2)
            if show==1: print (" >> ", el, "bottom face=", bf, " -> ", inext, "start face=", f)
            if len(inext) == 0: 
                if show == 1: print (" ###########   no more element")
                return el2remove, restrain 
            elif el[0] == inext[0]: 
                if show == 1: print (" !!!!!!!!!!!   no more element")
                return el2remove, restrain
            else: 
                if len(el2remove) > 2: 
                    if inext[0] == el2remove[len(el2remove)-2] or inext[0] == el2remove[len(el2remove)-1]: 
                        if show == 1: print (" ************   no more element")
                        return  el2remove
                if inext[4] == 0: 
                    side1 = Element2D_NextElement(inext, solids, nodes, start=1, next=0)
                    side2 = Element2D_NextElement(inext, solids, nodes, start=1, next=1)
                    side3 = Element2D_NextElement(inext, solids, nodes, start=1, next=2)
                    if len(side1) ==0 or len(side2) ==0 or len(side3) ==0 :
                        el2remove.append(inext[0]) 
                        if show == 1: print (" &&&&&&&&&&&&&&&   end i next[0]=%d :: no more element"%(inext[0]))
                        return el2remove, restrain
                if inext[0] == el[0] : 
                    if show == 1: print (" ^^^^^^^^^^^^^   same element with initial element")
                    return el2remove, restrain

                if bf == 1: 
                    e1 = el[1]; e2=el[2]
                elif bf ==2: 
                    e1 = el[2]; e2=el[3]
                elif bf ==3: 
                    e1 = el[3]; e2=el[4]
                else: 
                    e1 = el[4]; e2=el[1]
                ix = np.where(nodes[:,0]==e1)[0][0]
                EN1 = nodes[ix]
                ix = np.where(nodes[:,0]==e2)[0][0]
                EN2 = nodes[ix]
                ran = np.array([abs(EN1[2]), abs(EN2[2])])
                rmin = np.min(ran); rmax = np.max(ran)

                if inext[4] > 0 and parallel == 0: 
                    diffn = np.setdiff1d(inext[1:5], el[1:5]) 
                    ix = np.where(nodes[:,0] == diffn[0])[0][0]; difn1=nodes[ix]
                    ix = np.where(nodes[:,0] == diffn[1])[0][0]; difn2=nodes[ix]
                    dist, InNode1=DistanceFromLineToNode2D(difn1, [EN1, EN2], xy=23)
                    dist, InNode2=DistanceFromLineToNode2D(difn2, [EN1, EN2], xy=23)

                    if (abs(InNode1[2]) <= rmin and abs(InNode2[2]) <=rmin and abs(difn1[2]) <= rmin and abs(difn2[2]) <=rmin ) or (abs(InNode1[2]) >= rmax and abs(InNode2[2]) >=rmax and abs(difn1[2]) >= rmax and abs(difn2[2]) >=rmax ) : 
                        restrain = 1
                        if show == 1: 
                            print (" ^^^^^^^^^^^^^   direction is turned ")
                            
                            print (EN1[0], ",", EN2[0], ":", difn1[0], "(%.3f),"%(abs(difn1[2])*1000), difn2[0],"(%.3f)"%(abs(difn2[2])*1000) )
                            print ("  start el=%d, rmin=%.3f, rmax=%.3f, up el=%d, intersection point n1x=%.3f, n2x=%.3f, out of the bottom line"%(el[0], rmin*1000, rmax*1000, inext[0], abs(InNode1[2])*1000, abs(InNode2[2])*1000))
                        return el2remove, restrain 

                ran = np.array([EN1[2], EN2[2]])
                rmin = np.min(ran); rmax = np.max(ran)

                el2remove.append(inext[0])

                rside = Element2D_NextElement(el, solids, nodes, start=f, next=3)
                lside = Element2D_NextElement(el, solids, nodes, start=f, next=1)

                nnext = inext[1:5]
                nrside = rside[1:5]
                nlside = lside[1:5]
                parallel = []
                n_common = np.intersect1d(nnext, nrside)
                if len(n_common) ==2 and n_common[0] !=0 and n_common[1] !=0: 
                    und =  0
                    fnd = 0
                    for nd in el[1:5]: 
                        if nd == n_common[0] : 
                            fnd = 1
                            break 
                    if fnd ==1: und = n_common[1]
                    else:       und = n_common[0]
                    ix = np.where(nodes[:,0]==und)[0][0]
                    UN = nodes[ix]
                    dist, InNode=DistanceFromLineToNode2D(UN, [EN1, EN2], xy=23)
                    if InNode[2] >= rmin and InNode[2] <=rmax: 
                        if show==1: print ("R SIDE Common")
                        parallel = rside 
                        ic = []
                        for k, ln in enumerate(nrside): 
                            if ln == n_common[0] or ln == n_common[1]: 
                                ic.append(k)
                        if ic[0] == 0 and ic[1] == 1:  bf = 4 
                        elif ic[0] ==0 and ic[1] == 3: bf = 3 
                        elif ic[0] == 1: bf = 1 
                        elif ic[0] == 2: bf = 2
                        # print (" # parallel start face @@@# %d f=%d"%(inext[0],  bf))
                    else: 
                        # print ("Right:  rmin=%.3f, rmax=%.3f, intersecting node x=%.3f"%(rmin*1000, rmax*1000, InNode[2]*1000))
                        # print (" # parallel start face #### %d f=%d"%(inext[0],  bf))
                        upnext = Element2D_NextElement(inext, solids, nodes, start=bf, next=2)
                        # print (" ::: ", inext, upnext)
                        if len(upnext) == 0 : 
                            restrain = 1 
                            return el2remove, restrain
                else:
                    n_common = np.intersect1d(nnext, nlside)
                    # print ("\n******************************")
                    # print (nnext, nlside, n_common)
                    if len(n_common) ==2 and n_common[0] !=0 and n_common[1] !=0 : 
                        und =  0
                        fnd = 0
                        for nd in el[1:5]: 
                            if nd == n_common[0] : 
                                fnd = 1
                                break 
                        if fnd ==1: und = n_common[1]
                        else:       und = n_common[0]
                        ix = np.where(nodes[:,0]==und)[0][0]
                        UN = nodes[ix]
                        dist, InNode=DistanceFromLineToNode2D(UN, [EN1, EN2], xy=23)
                        if InNode[2] >= rmin and InNode[2] <=rmax: 
                            if show==1: print ("L SIDE Common")
                            # print ("L SIDE Common")
                            parallel = lside 
                            ic = []
                            for k, ln in enumerate(nlside): 
                                if ln == n_common[0] or ln == n_common[1]: 
                                    ic.append(k)
                            if ic[0] == 0 and ic[1] == 1:  bf = 2 
                            elif ic[0] ==0 and ic[1] == 3: bf = 1 
                            elif ic[0] == 1: bf = 3 
                            elif ic[0] == 2: bf = 4 
                            # print ("L SIDE Common", bf)
                        else: 
                            # print ("Left:  rmin=%.3f, rmax=%.3f, intersecting node x=%.3f"%(rmin*1000, rmax*1000, InNode[2]*1000))
                            upnext = Element2D_NextElement(inext, solids, nodes, start=bf, next=2)
                            # print (upnext)
                            if len(upnext) == 0 : 
                                restrain = 1 
                                return el2remove, restrain


                if len(parallel) > 0:
                    if show==1: print ("parallel.. ", parallel[0], "btm face=", bf)
                    # print ("parallel.. ", parallel[0], "btm face=", bf)
                    el2remove.append(parallel[0])
                    parallel_solid, restrain = self.Searching_Upper_elements(parallel, solids, nodes, el2remove, btm_face=bf, show=0, parallel=1)
                    if show==1: print ("### ", inext, parallel, parallel_solid)

                ncurn = np.array(el[1:5])
                n_common = np.intersect1d(nnext, ncurn)
                ic = []
                for k, ln in enumerate(nnext): 
                    if ln == n_common[0] or ln == n_common[1]: 
                        ic.append(k)
                
                if nnext[3] == 0: 
                    if ic[0] == 0 and ic[1] == 1:  bf1 = 1 
                    elif ic[0] ==0 and ic[1] == 2: bf1 = 3 
                    elif ic[0] == 1: bf1 = 2 
                else: 
                    if ic[0] == 0 and ic[1] == 1:  bf1 = 1 
                    elif ic[0] ==0 and ic[1] == 3: bf1 = 4 
                    elif ic[0] == 1: bf1 = 2 
                    elif ic[0] == 2: bf1 = 3 
                nextelement, restrain =  self.Searching_Upper_elements(inext, solids, nodes, el2remove, btm_face=bf1, show=show) 
                if show==1:  
                    print ("COmmon", n_common)
                    print ("nnext",  nnext)
                    print ("ic",  ic)
                    print ("bf1", bf1)
                    print ("##  ", inext, nextelement)
                    print ("EL RMV", el2remove)
                
                return el2remove, restrain

        else: 
            xs = [n1[x], n2[x], n3[x]] 
            if n1[x] < 0 or n2[x] < 0 or n3[x] < 0 : 
                out = min(xs)
                if out == n1[x] : f = 3 
                elif out == n2[x] : f = 1 
                elif out == n3[x] : f = 2 
                else: 
                    print ("!!! ERROR No FOUND BOTTOM FACE. ")
                    sys.exit()
                nf = 1
                

            elif n1[x] > 0 or n2[x] > 0 or n3[x] > 0: 
                out = max(xs)
                if out == n1[x] : f = 1 
                elif out == n2[x] : f = 2 
                elif out == n3[x] : f = 3
                else: 
                    print ("!!! ERROR No FOUND BOTTOM FACE. ")
                    sys.exit()
                nf = 2
            
            inext = Element2D_NextElement(el, solids, nodes, start=f, next=nf)

            if len(inext) == 0 : 
                if show==1:print ("**>>>> ")
                return el2remove, restrain 
            else: 
                el2remove.append(inext[0])
                nextelement, _ =  self.Searching_Upper_elements(inext, solids, nodes, el2remove) 
                if show==1:print ("***&&&^^&* ")
                return el2remove, restrain
    def RemoveCTRUTR(self, el, elset): 
        EL = ELEMENT()
        ETL = ELEMENT()
        for e in el.Element:
            if e[5] != 'CTB' and e[5] != 'CTR' and e[5] != 'SUT' and e[5] != 'UTR' : 
                EL.Add(e)
            else: 
                ETL.Add(e)
        ESET = ELSET()
        for eset in elset.Elset: 
            if eset[0] != 'CTB' and eset[0] != 'CTR' and eset[0] != 'SUT' and eset[0] != 'UTR' : 
                ESET.Elset.append(eset)
        return EL, ESET, ETL 
    def RemoveTread(self, el, nd, elset, LeftProfile, RightProfile, TDW, ModelPatternTotalWidth=0, ModelPatternDesignWidth=0, LastLeft=0, LastRight=0, LY=0.0, RY=0.0, debug=0): 

        # target_halfwidth = self.Define_PatternWidth(LeftProfile, RightProfile, TDW, ModelPatternTotalWidth, ModelPatternDesignWidth)
        t0 = time.time()

        LayoutOuter = self.Edge_TireProfile

        npn = np.array(nd.Node)

        cedges = []
        zs = []
        for edge in LayoutOuter: 
            for n in nd.Node: 
                if n[0] == edge[0] and n[2] ==0 and (edge[2] == "CTR" or edge[2] == "CTB" or edge[2] == "SUT" or edge[2]  == "UTR" or edge[2]  == "BSW"):
                    cedges.append(edge)
                    zs.append(n[3]) 

        mz = max(zs)
        idx = 0 
        for i, z in enumerate(zs): 
            if z == mz: 
                idx = i
                break 
        Pos_edges=[]
        Pos_edges.append(cedges[idx])

        
        if LastRight ==0: 
            profile_width_L, maxLdist, _ = self.TD_Arc_length_calculator(LeftProfile, totalwidth=1)
            profile_width_R, maxRdist, _ = self.TD_Arc_length_calculator(RightProfile, totalwidth=1)
            # profile_deco_halfwidth = ((profile_width_L+profile_width_R) - TDW  ) / 2.0 
            target_halfwidth = self.Define_PatternWidth(LeftProfile, RightProfile, TDW, ModelPatternTotalWidth, ModelPatternDesignWidth)

            tedge = cedges[idx]

            length = 0 
            cnt = 0 
            targetdist = 0 
            targetlength = 0
            while length < target_halfwidth: 
                for n in nd.Node: 
                    if n[0] == tedge[1] : 
                        length = self.TD_Arc_length_calculator(LeftProfile, h_dist=n[2])
                        break 
                if length < target_halfwidth and abs(n[2]) < maxRdist : 
                    # print (tedge, round(length*1000, 2))
                    target_el=tedge[4]
                    indx = NextEdge(tedge, LayoutOuter)
                    tedge=LayoutOuter[indx]
                    targetdist = n[2]
                    targetZ = n[3] 
                    MaxRdist = n[2]
                    targetlength = length
                    # print ("el No=%4d(Node %4d(dist=%7.2f)), length=%7.3f < %7.3f"%(target_el, tedge[0], n[2]*1000, length*1000, target_halfwidth*1000))
                else: 
                    break 
                if cnt > 200: break 
                cnt += 1

            # print ("Length=%.1f, Target half width=%.2f"%(length*1000, target_halfwidth*1000))
            
            LastRight_EL=target_el 
            print ("* Tread last EL to remove :%4d\n  (Node %4d(dist=%7.2f, ht=%7.2f))\n  length=%7.2f (Target=%.3f)"%(target_el, tedge[0], targetdist*1000, targetZ*1000, targetlength*1000,target_halfwidth*1000 ))
            # print ("* Profile last Removing Right Element No=%4d\n  (Node %4d(dist=%7.2f, ht=%7.2f)), length=%7.2f"%(target_el, tedge[0], targetdist*1000, targetZ*1000, targetlength*1000))
            self.TargetPatternWidth += targetlength
            self.right_end = [targetdist, targetZ]
        else: 
            LastRight_EL= LastRight
            targetdist = RY
            MaxRdist = abs(RY)
            self.right_end = [targetdist, 0]
            print ("* Tread Last EL to remove : %4d, Dist=%7.2f"%(LastRight_EL, RY*1000))
            # print ("* Profile Last Removing Right Element No=%4d, Dist=%7.2f"%(LastRight_EL, RY*1000))

        t0= time.time()
        if LastLeft == 0: 
            tedge = cedges[idx]
            length = 0 
            cnt = 0 
            targetdist = 0 
            targetlength = 0

            while length < target_halfwidth: 
                for n in nd.Node: 
                    if n[0] == tedge[0] : 
                        length = self.TD_Arc_length_calculator(RightProfile, h_dist=n[2])
                        break 
                if length <= target_halfwidth and abs(n[2]) < maxLdist :  
                    target_el=tedge[4]
                    indx = PreviousEdge(tedge, LayoutOuter)
                    tedge=LayoutOuter[indx]
                    targetdist = n[2]
                    targetZ = n[3]
                    MaxLdist = abs(n[2])
                    targetlength = length
                    # if cnt >15: print ("el No=%4d(Node %4d(dist=%7.2f)), length=%7.3f < %7.3f"%(target_el, tedge[0], n[2]*1000, length*1000, target_halfwidth*1000))
                else: 
                    break 
                if cnt > 200: break 
                cnt += 1
            
            LastLeft_EL=target_el 
            self.TargetPatternWidth += targetlength
            self.left_end = [targetdist, targetZ]
            print ("* Tread last EL to remove: %4d\n  (Node %4d(dist=%7.2f, ht=%7.2f))\n  length=%7.2f (Target=%.3f)"%(target_el, tedge[1], targetdist*1000, targetZ*1000, targetlength*1000,target_halfwidth*1000))
            # print ("* Profile last Removing Left Element No=%4d(Node %4d(dist=%7.2f, ht=%7.2f)), length=%7.2f"%(target_el, tedge[1], targetdist*1000, targetZ*1000, targetlength*1000))
        else: 
            LastLeft_EL = LastLeft
            targetdist = LY 
            MaxLdist = abs(LY)
            self.left_end = [targetdist, 0]
            print ("* Tread Last EL to remove : %4d, Dist=%7.2f"%(LastLeft_EL, LY*1000))
            # print ("* Profile Last Removing Left Element No=%4d, Dist=%7.2f"%(LastLeft_EL, LY*1000))
        
        membrane = []
        solids = []
        for e in el.Element:
            if e[6] == 2:
                membrane.append([e[0], e[1], e[2], 2])
            else: 
                solids.append([e[0], e[1], e[2], e[3], e[4], e[6]])
        solids= np.array(solids)


        center = []
        for mem in membrane: 
            # N = nd.NodeByID(mem[1])
            ix = np.where(npn[:,0] == mem[1])[0][0]; N = nd.Node[ix]
            if N[2] ==0: 
                center.append([mem[0], mem[1], mem[2], N[3]])
                continue
            # N = nd.NodeByID(mem[2])
            ix = np.where(npn[:,0] == mem[2])[0][0]; N = nd.Node[ix]
            if N[2] ==0: 
                center.append([mem[0], mem[1], mem[2], N[3]])
                continue

        center = sorted(center, key=lambda x: x[3])
        topmembrane = center[len(center)-1]

        n1 = topmembrane[1]; n2 = topmembrane[2]
        solid_on_membrane = []
        pos = 0; neg = 0 
        for e in el.Element:
            cnt = 0
            f = 0
            if e[6] == 3: 
                if n1 == e[1] or n2 == e[1]: 
                    cnt += 1
                    f+=1
                if n1 == e[2] or n2 == e[2]: 
                    cnt += 1
                    f+=2
                if n1 == e[3] or n2 == e[3]: 
                    cnt += 1
                    f+=3
            elif e[6] == 4: 
                if n1 == e[1] or n2 == e[1]: 
                    cnt += 1
                    f+=0
                if n1 == e[2] or n2 == e[2]: 
                    cnt += 1
                    f+=2
                if n1 == e[3] or n2 == e[3]: 
                    cnt += 1
                    f+=3
                if n1 == e[4] or n2 == e[4]: 
                    cnt += 1
                    f+=4
            ht = []
            if cnt > 1: 
                # N = nd.NodeByID(e[1])
                ix = np.where(npn[:,0]==e[1])[0][0]; N=nd.Node[ix]
                ix = np.where
                ht.append(N[3])
                # N = nd.NodeByID(e[2])
                ix = np.where(npn[:,0]==e[2])[0][0]; N=nd.Node[ix]
                ht.append(N[3])
                # N = nd.NodeByID(e[3])
                ix = np.where(npn[:,0]==e[3])[0][0]; N=nd.Node[ix]
                ht.append(N[3])
                if e[6] == 4: 
                    # N = nd.NodeByID(e[4])
                    ix = np.where(npn[:,0]==e[4])[0][0]; N=nd.Node[ix]
                    ht.append(N[3])

            if cnt == 2 and max(ht) > topmembrane[3]: 
                solid_on_membrane = e 
                ix = np.where(npn[:,0]==e[1])[0][0]; n1=npn[ix]
                ix = np.where(npn[:,0]==e[2])[0][0]; n2=npn[ix]
                ix = np.where(npn[:,0]==e[3])[0][0]; n3=npn[ix]
                if e[6] ==3: 
                    b1 = (n1[3] + n2[3])/2.0
                    b2 = (n2[3] + n3[3])/2.0
                    b3 = (n3[3] + n1[3])/2.0
                    if b1 < b2 and b1 < b3: 
                        btm_face = 1 
                    elif b2 < b1 and b2 < b3: 
                        btm_face = 2 
                    else: 
                        btm_face = 3 
                else:
                    ix = np.where(npn[:,0]==e[4])[0][0]; n4=npn[ix]
                    b1 = (n1[3] + n2[3])/2.0
                    b2 = (n2[3] + n3[3])/2.0
                    b3 = (n3[3] + n4[3])/2.0
                    b4 = (n4[3] + n1[3])/2.0
                    if b1 < b2 and b1 < b3 and b1 < b4: 
                        btm_face = 1 
                    elif b2 < b1 and b2 < b3 and b2 < b4 : 
                        btm_face = 2 
                    elif b3 < b1 and b3 < b2 and b3 < b4: 
                        btm_face = 3 
                    else: 
                        btm_face = 4 


                pos = btm_face -1 
                neg = btm_face + 1
                if pos == 0 : pos = e[6]
                if neg > e[6] : neg = 1 

                if e[5] != 'CTB' and e[5] != 'CTR' and e[5] != 'SUT' and e[5] != 'UTR'  and e[5] != 'TRW' and e[5] != 'BSW': 
                    nf = btm_face + 2 
                    if nf > e[6]: nf -= e[6]
                    ns = [solid_on_membrane[0], solid_on_membrane[1], solid_on_membrane[2], solid_on_membrane[3], solid_on_membrane[4], solid_on_membrane[6]]
                    ns1, nf = self.SearchNextSolids(ns, face=nf, np_solid=solids, direction=1)
                    elno = int(ns1[0])
                    for en in el.Element:
                        if en[0] == elno:
                            solid_on_membrane = en 
                            break 
                            
                    if en[5] != 'CTB' and en[5] != 'CTR' and en[5] != 'SUT' and en[5] != 'UTR'  and en[5] != 'TRW' and en[5] != 'BSW': 
                        nf = btm_face 
                        ns1, nf = self.SearchNextSolids(ns, face=nf, np_solid=solids, direction=1)
                        elno = int(ns1[0])
                        for en in el.Element:
                            if en[0] == elno:
                                solid_on_membrane = en 
                                break 
                        pos = btm_face +1 
                        neg = btm_face - 1
                        if neg == 0 : neg = e[6]
                        if pos > e[6] : pos = 1 

                break 

        print ("  Center EL above membrane", solid_on_membrane[0], "Bottom F%d"%(btm_face))

        debug =1
         

        nextsolid = [solid_on_membrane[0], solid_on_membrane[1], solid_on_membrane[2], solid_on_membrane[3], solid_on_membrane[4], solid_on_membrane[6]]
        element_to_delete=[]
        Pos_elements=[]
        Pos_elements.append(nextsolid)
        
        ############################################################# 
        nep = np.array(nd.Node)
        ups =[]
        ups.append(nextsolid[0])
        ups, _ = self.Searching_Upper_elements(nextsolid, solids, nep, el2remove=ups)
        ending = 0
        for up in ups: 
            element_to_delete.append(up)

        next_face = pos
        cnt = 0 
        start_triangular = 0 
        deletes = []
        ending = 0
        meetlast = 0 
        skip = 1
        EL3Next = 0 

        ppp = 0 
        while next_face != 0: 
            ppp += 1 
            if ppp > 1000: 
                print ("ERROR!, No found element %d"%(LastRight_EL))
            if len(ups)> 0: 
                up = ups[-1]
                ix = np.where(solids[:,0]==up)[0][0]
                sol = solids[ix]
                nmy = 0
                for i in range(1, sol[5]+1): 
                    ix = np.where(npn[:,0] == sol[i])[0][0]
                    if nmy < npn[ix][2] : 
                        nmy = npn[ix][2]
                if nmy > self.right_end[0]+1.0e-03: 
                    break 
            ## WARNING!! if there is a tie surface on the element, errer may occur  ###########################
            ps = nextsolid
            preface = next_face 
            nextsolid, next_face = self.SearchNextSolids(nextsolid, face=next_face, np_solid=solids, direction=1)
            # print ("*ps", ps, "preface",  preface, "next face", next_face)

            if len(nextsolid) ==0: ## element has tie surface on the right (positive).. 
                # print (" MEET TIE>>", ps, preface)
                # sys.exit()
                if ps[5] == 4: 
                    if preface == 4: sharingnode = ps[1]
                    elif preface == 3: sharingnode = ps[4]
                    elif preface == 2: sharingnode = ps[3]
                    else: sharingnode = ps[2]
                
                else: 
                    if preface == 3: sharingnode = ps[1]
                    elif preface == 2: sharingnode = ps[3]
                    else: sharingnode = ps[2]
                # print ("next sharing node", sharingnode)

                idxs = np.where(solids[:, 1:5] == sharingnode)[0]

                i = 0  
                while i < len(idxs):  ## delete self element (pre-element)
                    if solids[idxs[i]][0] == ps[0]: 
                        refnodes = [solids[idxs[i]][1], solids[idxs[i]][2], solids[idxs[i]][3]]
                        if ps[4] > 0: refnodes.append(ps[4])
                        idxs = np.delete(idxs, i, 0)
                        break 
                    i += 1 
                
                i = 0
                while i < len(idxs):  ## delete 2-node sharing element (because we are trying to find the element of master tie)
                    cnt = 0 
                    for rn in refnodes: 
                        if solids[idxs[i]][1] == rn :  cnt+= 1
                        if solids[idxs[i]][2] == rn :  cnt+= 1
                        if solids[idxs[i]][3] == rn :  cnt+= 1
                        if solids[idxs[i]][4] > 0: 
                            if solids[idxs[i]][4] == rn :  cnt+= 1
                    if cnt == 2: 
                        idxs = np.delete(idxs, i, 0) 
                        break 
                    i += 1 
                
                nextnodes =[]
                for ix in idxs: 
                    
                    for i in range(1, 5): 
                        if sharingnode == solids[ix][i]: 
                            k = i+1
                            if k > solids[ix][5]: k == 1 
                            nextnodes.append([solids[ix], i, k])
                            break 
                
                z = 0.0
                f = 0
                for i, sol in enumerate(nextnodes): 
                    ix = np.where(npn[:,0]==sol[0][k])[0][0]
                    if z < npn[ix][3]: 
                        z = npn[ix][3]
                        nsol=sol 
                        f =1 
                if f ==1: 
                    if nsol[0][5] ==4: 
                        if nsol[1] == 1 and nsol[2] == 2: nf = 3 
                        elif nsol[1] == 2 and nsol[2] == 3: nf = 4 
                        elif nsol[1] == 3 and nsol[2] == 4: nf = 1 
                        else: nf = 2 

                        nextsolid = nsol[0]
                        next_face = nf 
                    else: 
                        if nsol[1] == 1 and nsol[2] == 2: nf = 2 
                        elif nsol[1] == 2 and nsol[2] == 3: nf = 3 
                        else: nf = 1 

                        ups = [nsol[0][0]]
                        bf = nf + 1 
                        if bf > nsol[0][5] : bf -= nsol[0][5]

                        ups, cont = self.Searching_Upper_elements(nsol[0], solids, nep, el2remove=ups, btm_face=bf, show=0)
                        t_ending =0 
                        for up in ups: 
                            deletes.append(up)
                            element_to_delete.append(up)
                            if LastRight_EL == up : 
                                t_ending = 1
                        if t_ending == 1: 
                            break 

                        nextsolid, nf0 = self.SearchNextSolids(nsol[0], face=nf, np_solid=solids, direction=1) 

                        next_face = nf0 + 1 
                        if next_face > nextsolid[5] : next_face -= nextsolid[5]

                    # print (nextsolid, next_face)
                    # ppp = 1 
                else: 
                    print ("There is a tie surface next to %d"%(ps[0]))
                    break  


            dup = 0 
            for up in ups: 
                if nextsolid[0] == up: 
                    dup = 1 
                    break 
            if dup == 1 and EL3Next == 0: 
                next_face += 1 
                if next_face > nextsolid[5] : next_face -= nextsolid[5] 
                continue 
            
            ups =[]
            ups.append(nextsolid[0])
            bf = next_face + 1
            if bf > nextsolid[5]: bf = 1 
            # if nextsolid[0] == 2604: sh = 1 
            # else: sh = 0 
            ups, cont = self.Searching_Upper_elements(nextsolid, solids, nep, el2remove=ups, btm_face=bf, show=0)
            for up in ups: 
                deletes.append(up)
                element_to_delete.append(up)
                if LastRight_EL == up : 
                    meetlast = 1 
                    if cont == 0 : 
                        ending = 1
                if skip == 0: 
                    if meetlast == 1:
                        ending =  1 
            # print ("1", nextsolid[0],  bf, ups, ending)
            if ending ==1:
                # print ("FOUND Last ################")
                ps = nextsolid
                preface = next_face 
                nextsolid, next_face = self.SearchNextSolids(nextsolid, face=next_face, np_solid=solids, direction=1) 
                if len(nextsolid) > 0 :
                    if start_triangular == 0: 
                        _, face = Contact_relation_2Elements(nextsolid, ps)
                        nf = face + 1 
                        if nf > nextsolid[5] : nf = 1 
                    else: 
                        nf = next_face  
                    checkups =[]
                    checkups.append(nextsolid[0])
                    bf = next_face + 1
                    if bf > nextsolid[5]: bf = 1 
                    checkups, cont = self.Searching_Upper_elements(nextsolid, solids, nep, el2remove=checkups, btm_face=bf, show=0)
                    adding = 0 
                    for up in checkups: 
                        if LastRight_EL == up: 
                            adding = 1 
                            break 
                    if adding == 1: 
                        for up in checkups: 
                            deletes.append(up)
                            element_to_delete.append(up)

                print ("  Profile Right Last Elements(%d)\n   to be deleted with"%(LastRight_EL), ups)
                break 
            if meetlast == 1: skip = 0 
            if nextsolid[5] == 4: EL3Next = 0  
            while nextsolid[5] ==3: 
                # print ("A: ns", nextsolid, "prev=", ps)
                _, face = Contact_relation_2Elements(nextsolid, ps)
                face += 1 
                if face == 4: face = 1 
                # print ("B ns", nextsolid, "face=", face)
                nxsolid, nxface = self.SearchNextSolids(nextsolid, face=face, np_solid=solids, direction=1)
                # print ("C ns:", nxsolid, "face=", nxface, " < Up element on 3-node Element")
                ups = [nextsolid[0]]
                bf = nxface + 2 
                if bf > nxsolid[5] : bf -= nxsolid[5]  
                ups.append(nxsolid[0])
                # print ("C1", nxsolid, bf)
                ups, cont = self.Searching_Upper_elements(nxsolid, solids, nep, el2remove=ups, btm_face=bf, show=0) ## nep : nodes
                for up in ups: 
                    deletes.append(up)
                    element_to_delete.append(up)
                    if LastRight_EL == up : 
                        ending = 1 
                # print ("UPS", ups)
                if ending == 1: 
                    break  ## if meeting target element in 

                nextsolid = nxsolid
                next_face = bf - 1
                if next_face == 0: next_face = nextsolid[5]
                EL3Next = 1 

            if ending ==1: 
                break 

            #############################################################            

        nextsolid = [solid_on_membrane[0], solid_on_membrane[1], solid_on_membrane[2], solid_on_membrane[3], solid_on_membrane[4], solid_on_membrane[6]]
        #############################################################
        # element_to_delete.append(nextsolid[0])

        ix = np.where(npn[:,0]==nextsolid[1])[0][0]; n1=npn[ix]
        ix = np.where(npn[:,0]==nextsolid[2])[0][0]; n2=npn[ix]
        ix = np.where(npn[:,0]==nextsolid[3])[0][0]; n3=npn[ix]
        ix = np.where(npn[:,0]==nextsolid[4])[0][0]; n4=npn[ix]
        b1 = (n1[3] + n2[3])/2.0
        b2 = (n2[3] + n3[3])/2.0
        b3 = (n3[3] + n4[3])/2.0
        b4 = (n4[3] + n1[3])/2.0
        if b1 < b2 and b1 < b3 and b1 < b4: 
            btm_face = 1 
        elif b2 < b1 and b2 < b3 and b2 < b4 : 
            btm_face = 2 
        elif b3 < b1 and b3 < b2 and b3 < b4: 
            btm_face = 3 
        else: 
            btm_face = 4 
        
        neg = btm_face + 1
        if neg > e[6] : neg = 1 


        ending = 0
        nf = neg 
        ns = nextsolid
        nextsolid, nf = self.SearchNextSolids(ns, face=nf, np_solid=solids, direction=1)
        ups=[nextsolid[0]]
        ups, _ = self.Searching_Upper_elements(nextsolid, solids, nep, el2remove=ups, show=0)
        
        for up in ups: 
            element_to_delete.append(up)

        Neg_elements=[]
        next_face = nf 
        cnt = 0 
        start_triangular = 0 
        deletes = []
        ending = 0
        meetlast = 0 
        skip = 1 
        EL3Next = 0  
        ppp = 0 
        while next_face != 0:
            ppp += 1 
            if ppp > 1000: 
                print ("ERROR!, No found element %d"%(LastLeft_EL))
            if len(ups)> 0: 
                up = ups[-1]
                ix = np.where(solids[:,0]==up)[0][0]
                sol = solids[ix]
                nmy = 0
                for i in range(1, sol[5]+1): 
                    ix = np.where(npn[:,0] == sol[i])[0][0]
                    if nmy > npn[ix][2] : 
                        nmy = npn[ix][2]
                if nmy < self.left_end[0]- 1.0e-03 : break 
            ## WARNING!! if there is a tie surface on the element, errer may occur  ###########################
            if ps[0] == nextsolid[0]:
                # print ("###########################")
                # print (nextsolid, next_face)
                nextsolid, next_face = self.SearchNextSolids(nextsolid, face=next_face, np_solid=solids, direction=-1) 
                # print (" >> ", nextsolid, next_face)
                # print ("###########################")
                
            ps = nextsolid       
            preface = next_face 
            
            nextsolid, next_face = self.SearchNextSolids(nextsolid, face=next_face, np_solid=solids, direction=-1)
            # print ("::  ", ps, preface, nextsolid, next_face)
            if len(nextsolid) ==0: ## element has TIE surface on the left (negative side).. 
                sharingnode = ps[preface] 
                # print ("next sharing node", sharingnode)

                idxs = np.where(solids[:, 1:5] == sharingnode)[0]
                i = 0  
                while i < len(idxs):  ## delete self element (pre-element)
                    if solids[idxs[i]][0] == ps[0]: 
                        refnodes = [solids[idxs[i]][1], solids[idxs[i]][2], solids[idxs[i]][3]]
                        if ps[4] > 0: refnodes.append(ps[4])
                        idxs = np.delete(idxs, i, 0)
                        break 
                    i += 1 
                
                i = 0
                while i < len(idxs):  ## delete 2-node sharing element (because we are trying to find the element of master tie)
                    cnt = 0 
                    for rn in refnodes: 
                        if solids[idxs[i]][1] == rn :  cnt+= 1
                        if solids[idxs[i]][2] == rn :  cnt+= 1
                        if solids[idxs[i]][3] == rn :  cnt+= 1
                        if solids[idxs[i]][4] > 0: 
                            if solids[idxs[i]][4] == rn :  cnt+= 1
                    if cnt == 2: 
                        idxs = np.delete(idxs, i, 0) 
                        break 
                    i += 1 
                
                nextnodes =[]
                for ix in idxs: 
                    for i in range(1, 5): 
                        if sharingnode == solids[ix][i]: 
                            k = i-1
                            if k == 0: k = solids[ix][5]
                            nextnodes.append([solids[ix], i, k])
                            break 
                
                z = 0.0
                f = 0 
                for i, sol in enumerate(nextnodes): 
                    ix = np.where(npn[:,0]==sol[0][k])[0][0]
                    if z < npn[ix][3]: 
                        z = npn[ix][3]
                        nsol=sol 
                        f =1 
                if f ==1: 
                    if nsol[0][5] ==4: 
                        nf = nsol[1]+2
                        if nf > 4: nf -= 4 
                        nextsolid = nsol[0]
                        next_face = nf 
                    else: 
                        if nsol[1] == 1 : nf = 2 
                        elif nsol[1] == 2 : nf = 3  
                        else: nf = 1 

                        ups = [nsol[0][0]]
                        bf = nf -1 
                        if bf ==0: bf == nsol[0][5]

                        ups, cont = self.Searching_Upper_elements(nsol[0], solids, nep, el2remove=ups, btm_face=bf, show=0)
                        t_ending =0 
                        for up in ups: 
                            deletes.append(up)
                            element_to_delete.append(up)
                            if LastRight_EL == up : 
                                t_ending = 1
                        if t_ending == 1: 
                            break 

                        nextsolid, nf0 = self.SearchNextSolids(nsol[0], face=nf, np_solid=solids, direction=1) 

                        next_face = nf0 -1 
                        if next_face == 0: next_face = nextsolid[5]
                else: 
                    print ("There is a tie surface next to %d"%(ps[0]))
                    break 
            # print ("                                   ", nextsolid)
            dup = 0 
            for up in ups: 
                if nextsolid[0] == up: 
                    dup = 1 
                    break 
            if dup == 1 and EL3Next == 0 : 
                next_face -= 1 
                if next_face ==0 : next_face = nextsolid[5] 
                
                continue 


            ups =[]
            ups.append(nextsolid[0])
            bf = next_face -1 
            if bf ==0: bf = nextsolid[5]
            # print (nextsolid, bf )
            ups, cont = self.Searching_Upper_elements(nextsolid, solids, nep, el2remove=ups, btm_face=bf, show=0)
            # print (nextsolid, bf, " UPS : ", ups)
            for up in ups: 
                deletes.append(up)
                element_to_delete.append(up)
                if LastLeft_EL == up : 
                    meetlast = 1 
                    if cont == 0 : 
                        ending = 1
                if skip == 0: 
                    if meetlast == 1:
                        ending =  1 
            if ending ==1: 
                ps = nextsolid       
                preface = next_face 
                nextsolid, next_face = self.SearchNextSolids(nextsolid, face=next_face, np_solid=solids, direction=-1)
                if len(nextsolid) > 0: 
                    if start_triangular == 0: 
                        _, face = Contact_relation_2Elements(nextsolid, ps)
                        nf = face - 1 
                        if nf ==0: nf = nextsolid[5]
                    else: 
                        nf = next_face 
                        next_face += 1
                        if next_face == nextsolid[5] : next_face = 1
                        nextsolid, next_face = self.SearchNextSolids(nextsolid, face=next_face, np_solid=solids, direction=1)

                    checkups =[]
                    checkups.append(nextsolid[0])
                    bf = next_face -1 
                    if bf ==0: bf = nextsolid[5]
                    # print (nextsolid, bf )
                    checkups, cont = self.Searching_Upper_elements(nextsolid, solids, nep, el2remove=checkups, btm_face=bf, show=0)
                    adding = 0 
                    for up in checkups: 
                        if LastLeft_EL == up : 
                            adding =1 
                            break 
                    sameEl = 0
                    for up in checkups: 
                        for u in ups: 
                            if u==up: 
                                sameEl+=1 
                                break
                    if sameEl > 1: 
                        adding = 0 
                    
                    if adding == 1: 
                        for up in checkups: 
                            deletes.append(up)
                            element_to_delete.append(up)

                # print (" Tread Last EL to remove %d is in "%(LastLeft_EL), ups)
                print ("*  Profile Left Last Elements(%d)\n   to be deleted with"%(LastLeft_EL), ups)
                break 
            if meetlast == 1: skip = 0 
            if nextsolid[5] == 4: EL3Next = 0
            while nextsolid[5] ==3:
                _, face = Contact_relation_2Elements(nextsolid, ps)
                face -= 1 
                if face ==0: face = 3 
                nxsolid, nxface = self.SearchNextSolids(nextsolid, face=face, np_solid=solids, direction=1)


                ups = [nextsolid[0]]
                bf = nxface + 2 
                ups, cont = self.Searching_Upper_elements(nxsolid, solids, nep, el2remove=ups, btm_face=bf, show=0) ## nep : nodes
                for up in ups: 
                    deletes.append(up)
                    element_to_delete.append(up)
                    if LastRight_EL == up : 
                        ending = 1

                if ending == 1: 
                    break  ## if meeting target element in 

                nextsolid = nxsolid 
                next_face = bf + 1 
                if next_face > nextsolid[5]: next_face -= nextsolid[5] 
                EL3Next = 1
            
            if ending == 1: 
                break 

        element_to_delete = np.array(element_to_delete)
        element_to_delete = np.unique(element_to_delete)
    
        NEL=ELEMENT()
        undelete = []
        cnt = 0 
        allel = []
        for e in el.Element: 
            allel.append(e[0])
            f = 0 
            for number in element_to_delete: 
                if e[0] == number: 
                    f = 1 
                    break
            ## only the elements whose names are CTB, SUT, BSW, TRW should be deleted. 
            if e[5] != "CTR" and e[5] != "CTB" and e[5] != "SUT" and e[5] != "UTR" and e[5] != "BSW" and e[5] != "TRW" : 
                f = 0
                undelete.append(e[0])
            if f ==0: 
                NEL.Add(e)
                continue
            cnt += 1 
        
        for en in undelete: 
            i = 0 
            while i < len(element_to_delete): 
                if en == element_to_delete[i] : 
                    element_to_delete= np.delete(element_to_delete, i)
                    break 
                i += 1

        ############################################################
        ## in case the element is divided into 2 elements 
        ## sometimes there are some elements to be deleted (isolated elements, no connection with other elelemnts )
        ## it is modified... 
        check_element_dividing =1 
        if check_element_dividing == 1: 

            OUT=NEL.OuterEdge(nd)
            pts=[]
            
            for i, ed in enumerate(OUT.Edge): 
                if i ==0: 
                    ix = np.where(nep[:,0]==ed[0])[0][0]; n1 = nep[ix]
                    pts.append([n1[2], n1[3]])
                
                ix = np.where(nep[:,0]==ed[1])[0][0]; n2 = nep[ix]
                pts.append([n2[2], n2[3]])
            k = 0
            while k < len(NEL.Element): 
                if NEL.Element[k][5] == "CTR" or NEL.Element[k][5] == "CTB" or NEL.Element[k][5] == "UTR" or NEL.Element[k][5] == "SUT" or NEL.Element[k][5] == "TRW" or NEL.Element[k][5] == "BSW": 
                    bnd = 0 
                    for ed in OUT.Edge: 
                        if ed[4] == NEL.Element[k][0]: 
                            bnd =1 
                            break 

                    if bnd == 0:     
                        ix = np.where(nep[:,0]==NEL.Element[k][1])[0][0]; n1 = nep[ix]
                        pt = [n1[2], n1[3]]
                        ix = np.where(nep[:,0]==NEL.Element[k][2])[0][0]; n2 = nep[ix]
                        pt1 = [n2[2], n2[3]]
                        ix = np.where(nep[:,0]==NEL.Element[k][3])[0][0]; n3 = nep[ix]
                        pt2 = [n3[2], n3[3]]
                        if not IsPointInPolygon(pt, pts) and not IsPointInPolygon(pt1, pts)  and not IsPointInPolygon(pt2, pts) :
                            del(NEL.Element[k])
                            k -= 1
                k += 1
        #########################################################
        
        ##############################################################
        ## Elset shoudl be re-orgamized. 
        ## the elimated element number should be deleted in the elset. 
        NELSET=ELSET()
        name = ''
        for k, eset in enumerate(elset.Elset):
            for i, es in enumerate(eset): 
                if i ==0: 
                    NELSET.AddName(es)
                    name=es 
                    continue 
                f = 0 
                for number in element_to_delete: 
                    if es == number: 
                        f = 1 
                        break 
                if f == 0: 
                    NELSET.AddNumber(es, name)
        i = 0 
        while i < len(NELSET.Elset): 
            if len(NELSET.Elset[i]) ==1: 
                del(NELSET.Elset[i])
                i -= 1
            i += 1

        
        resel = []
        for e in NEL.Element:
            resel.append(e[0])
        allel= np.array(allel)
        resel = np.array(resel)
        deleted=np.setdiff1d(allel, resel)

        Deleted=ELEMENT()
        for d in deleted: 
            for e in el.Element: 
                if d == e[0]: 
                    Deleted.Add(e)
                    break 
        ##############################################################
        return NEL, NELSET, Deleted
    def TD_Arc_length_calculator(self, profile, h_dist=0, totalwidth=0): 
        #  def TD_Arc_length_calculator(profile, h_dist=0, totalwidth=0, msh_return=0): 
        if totalwidth == 1: 
            length, dist, drop = TD_Arc_length_calculator(profile, h_dist=h_dist, totalwidth=totalwidth, msh_return=0)
            return length, dist, drop 
        else: 
            length, _ = TD_Arc_length_calculator(profile, h_dist=h_dist, totalwidth=totalwidth, msh_return=0)
            return length

    def SearchNextSolids(self, el, face=0, np_solid=[], direction=0):  ## side 0: left/rigth direction, side -1: neg direction +1 : pos direction 
        solids = np_solid
        n1 = el[face]
        face += 1
        if face > int(el[5]): face = 1 
        n2 = el[face]

        idxs1 = np.where(solids[:, 1:5] == n1)[0]
        idxs2 = np.where(solids[:, 1:5] == n2)[0]

        idxs = np.intersect1d(idxs1, idxs2) 
        if len(idxs)>1: 
            if solids[idxs[0]][0] == el[0]: next_solid = solids[idxs[1]]
            else: next_solid = solids[idxs[0]]
            f = 0 
            for i in range(1, int(next_solid[5]) + 1): 
                if i ==1 and (next_solid[i] == n1 or next_solid[i] == n2): f+= 0 
                elif (next_solid[i] == n1 or next_solid[i] == n2): f+= i  

            btm_face = 0 
            if next_solid[5] == 3 and f == 3: btm_face = 1
            if next_solid[5] == 3 and f == 5: btm_face = 2
            if next_solid[5] == 3 and f == 4: btm_face = 3
            if next_solid[5] == 4 and f == 2: btm_face = 1
            if next_solid[5] == 4 and f == 5: btm_face = 2
            if next_solid[5] == 4 and f == 7: btm_face = 3
            if next_solid[5] == 4 and f == 4: btm_face = 4
            if direction == 1: 
                next_face = btm_face - 2 
                if next_face <= 0 : next_face += next_solid[5]
            if direction == -1: 
                next_face = btm_face + 2 
                if next_face >  next_solid[5] : next_face -= next_solid[5]  

            return next_solid, int(next_face)
        else:  
            NOLIST=[]
            return NOLIST, 0

# Preprocessing - CUTE INP 
def existEL(SetName, Elsets):
    Exist =0
    for i in range(len(Elsets)):
        if SetName in Elsets[i][0]:
            Exist = 1
            break
    return Exist
def ConnectedEdge(edge, edges, exclude=[]): 
    con = []
    for e in edges: 
        if e[0] == edge[0] and e[1] == edge[1]: 
            continue 
        if e[1] == edge[0] or e[0] == edge[0]: 
            exc= 0 
            for ex in exclude: 
                if ex[0] == e[0] and ex[1] == e[1] : exc = 1
            if exc == 0:  con.append(e)
        if e[1] == edge[1] or e[0] == edge[1]: 
            exc= 0 
            for ex in exclude: 
                if ex[0] == e[0] and ex[1] == e[1] : exc = 1
            if exc == 0:  con.append(e)

    return con 
def ChaferDivide(Elements, ChaferName, Elset, Node):

    asymmetric =0
    I = len(Elements)
    J = len(Node)
    for i in range(I):
        if Elements[i][5]=="BT2":
            for j in range(J):
                if Node[j][0] == Elements[i][1]:
                    if Node[j][2] == 0:
                        relement=Elements[i][0]
                if Node[j][0] == Elements[i][2]:
                    if Node[j][2] == 0:
                        lelement=Elements[i][0]
    
    Offset = abs(relement - lelement )
    if Offset != 2000:
        for j in range(J):
            if Node[j][2] > 0.0 :
                Offset = Node[j][0]
                break
        # print ("Asymmetric Model %d"%(Offset))
        asymmetric =1

    
    for i in range(len(Elements)):
        for j in range(len(ChaferName)):
            if Elements[i][5] == ChaferName[j]:
                if Elements[i][8] > 0:
                    NewName = Elements[i][5] + '_R'
                else:
                    NewName = Elements[i][5] + '_L'
                Elements[i][5] = NewName
                    
    for i in range(len(Elements)):
        if Elements[i][5] == "BEAD_R" and Elements[i][8] < 0.0 :
            Elements[i][5] = 'BEAD_L'

    # for i in range(len(Elset)):
    #     for j in range(len(ChaferName)):
    #         if Elset[i][0] == ChaferName[j]:
    #             left=[]
    #             right=[]
    #             left.append(Elset[i][0] + '_L')
    #             right.append(Elset[i][0] + '_R')
    #             for k in range(1, len(Elset[i])):
    #                 for el in Elements:
    #                     if el[0] == Elset[i][k]: 
    #                         if el[8] > 0: 
    #                             right.append(Elset[i][k])
    #                         else: 
    #                             left.append(Elset[i][k])
    #                         break

    #             del(Elset[i])

    #             Elset.append(right)
    #             Elset.append(left)
    #             break
    if asymmetric ==1:
        Offset = 0
    return Elements, Elset, Offset
def FindSolidElementBetweenMembrane1(m1, m2, Elements):
    # Data types of m1, m2 are string
    between = []
    Elm1 = []
    Elm2 = []

    for i in range(len(Elements)):
        if Elements[i][5] == m1 or Elements[i][5] == m2:
            for j in range(len(Elements)):
                if j != i and Elements[j][6] == 3:
                    for k in range(1, 3):
                        if k == 1:
                            m = 2
                        else:
                            m = 1
                        for l in range(1, 4):
                            n = l + 1
                            if n > 3:
                                n = l - 3

                            if Elements[i][k] == Elements[j][l] and Elements[i][m] == Elements[j][n]:
                                if Elements[i][5] == m1:
                                    Elm1.append(Elements[j])
                                else:
                                    Elm2.append(Elements[j])
                                break

                elif j != i and Elements[j][6] == 4:
                    for k in range(1, 3):
                        if k == 1:
                            m = 2
                        else:
                            m = 1
                        for l in range(1, 5):
                            n = l + 1
                            if n > 4:
                                n = l - 4

                            if Elements[i][k] == Elements[j][l] and Elements[i][m] == Elements[j][n]:
                                if Elements[i][5] == m1:
                                    Elm1.append(Elements[j])
                                else:
                                    Elm2.append(Elements[j])
                                break

    for i in range(len(Elm1)):
        for j in range(len(Elm2)):
            if Elm1[i][0] == Elm2[j][0]:
                between.append(Elm2[j][0])
                break

    m1f=[]
    m2f=[]
    for i in range(len(Elm1)):
        match=0
        for j in range(len(between)):
            if Elm1[i][0] == between[j]:
                match = 1
                break
        if match == 0:
            m1f.append(Elm1[i])

    for i in range(len(Elm2)):
        match = 0
        for j in range(len(between)):
            if Elm2[i][0] == between[j]:
                match = 1
                break
        if match == 0:
            m2f.append(Elm2[i])
    ########################################################
    for i in range(len(m2f)):
        for j in range(len(m1f)):
            match = 0
            for m in range(1, 5):
                for n in range(1, 5):
                    if m2f[i][m] == m1f[j][n] and m1f[j][n] != '':
                        match += 1
            if match == 2:
                between.append(m2f[i][0])
                between.append(m1f[j][0])
                # print "Between Appended"
                break


    return between
def ElementCheck (Elements, Nodes):
    # rebar Connectivity
    # Element Shape 
    
    tmpEL = []
    for i in range(len(Elements)):
        tmpEL.append(Elements[i][0])
        tmpEL.append(Elements[i][1])
        tmpEL.append(Elements[i][2])
        if Elements[i][3] == '':
            tmpEL.append(0)
        else:
            tmpEL.append(Elements[i][3])
        if Elements[i][4] == '':
            tmpEL.append(0)
        else:
            tmpEL.append(Elements[i][4])
        tmpEL.append(Elements[i][6])

    tmpND = []
    tmpCoord = []
    for i in range(len(Nodes)):
        tmpND.append(Nodes[i][0])
        tmpCoord.append(Nodes[i][1])
        tmpCoord.append(Nodes[i][2])
        tmpCoord.append(Nodes[i][3])
    
    # tupleEL =tuple(tmpEL)
    # tupleND =tuple(tmpND)
    # tupleCo = tuple(tmpCoord)

    Results = 1 
    Message=[]

    return Results, Message
def BeadWidth(Element, Node):
    BDCore = []

    for i in range(len(Element)):
        if Element[i][5] == 'BEAD_L' or Element[i][5] == 'BD1':
            BDCore.append(Element[i])
    if len(BDCore) == 0:
        for i in range(len(Element)):
            if Element[i][5] == 'BEAD_R' or Element[i][5] == 'BD1':
                BDCore.append(Element[i])
    BDEdge = FindEdge(BDCore)
    BDFree = FindFreeEdge(BDEdge)

    nodes = []
    for i in range(len(BDFree)):
        if i == 0:
            nodes.append(BDFree[i][0])
            nodes.append(BDFree[i][1])
        else:
            N = len(nodes)
            match1 = 0
            match2 = 0
            for j in range(N):
                if BDFree[i][0] == nodes[j]:
                    match1 = 1
                if BDFree[i][1] == nodes[j]:
                    match2 = 1
            if match1 == 0:
                nodes.append(BDFree[i][0])
            if match2 == 0:
                nodes.append(BDFree[i][1])
    center = Area(nodes, Node)
    min = 100000.0
    max = -100000.0
    npn = np.array(Node)
    for nd in nodes: 
        ix = np.where(npn[:,0]==nd)[0][0]
        C = npn[ix]
        if abs(C[2]) > max:
            max = abs(C[2])
        if abs(C[2]) < min:
            min = abs(C[2])

    if abs(center[1]) > abs(max) or abs(center[1]) < abs(min):
        center[1] = (abs(max)+abs(min))/2.0

    return abs(min), abs(max), abs(center[1])
def TieSurface(Elements, Nodes):
    AllEdges=FindEdge(Elements)
    FreeEdges=FindFreeEdge(AllEdges)
    CenterNodes = FindCenterNodes(Nodes)
    OutEdges=FindOutEdges(FreeEdges, CenterNodes, Nodes, Elements)

    InnerFreeEdges = FindInnerFreeEdges(FreeEdges, OutEdges)
    ND =NODE()
    for n in Nodes:
        ND.Add(n)
    MasterEdges, SlaveEdges, Tie_error = DivideInnerFreeEdgesToMasterSlave(InnerFreeEdges, ND)
    return MasterEdges, SlaveEdges, OutEdges,CenterNodes, FreeEdges, AllEdges, Tie_error
def FindTieLoop(TieStartNode, nextEdge, FreeEdge):
    # len(nextEdge) == 2

    MAX = 50
    NextWay = 0
    iNext = []
    startNode = FreeEdge[nextEdge[0]][0]

    if FreeEdge[nextEdge[0]][5] < 1:
        testEdge = nextEdge[0]
        saveEdge = testEdge
        if FreeEdge[testEdge][1] == TieStartNode:
            NextWay = testEdge
            return NextWay
    elif FreeEdge[nextEdge[1]][5] < 1:
        testEdge = nextEdge[1]
        saveEdge = testEdge
        if FreeEdge[testEdge][1] == TieStartNode:
            NextWay = testEdge
            return NextWay
    else:
        print ('[INPUT]', FreeEdge[nextEdge[0]], ',', FreeEdge[nextEdge[1]], ' (1) TIE Conection InCompletion')
        # logline.append(['ERROR::PRE::[INPUT] {' + str(FreeEdge[nextEdge[0]]) + ', ' + str(FreeEdge[nextEdge[1]] + '} - (1) TIE Connection Incompletion\n')])
        return 0

    #    print ('TieStart', TieStartNode, 'Node start', startNode)
    #    print ('**', FreeEdge[testEdge]) # 1st Edge

    for i in range(MAX):
        iNext = []

        iNext = FindNextEdge(testEdge, FreeEdge)

        if len(iNext) == 1:
            if FreeEdge[iNext[0]][5] < 1:
                if FreeEdge[iNext[0]][1] == TieStartNode:
                    if saveEdge == nextEdge[0]:
                        NextWay = nextEdge[0]
                    else:
                        NextWay = nextEdge[1]
                    #                    print ('1.1',  FreeEdge[iNext[0]])
                    return NextWay
                elif FreeEdge[iNext[0]][1] == startNode:
                    if saveEdge == nextEdge[0]:
                        NextWay = nextEdge[1]
                    else:
                        NextWay = nextEdge[0]
                    #                    print ('1.2',  FreeEdge[iNext[0]])
                    return NextWay
                else:
                    #                    print ('1', FreeEdge[iNext[0]])
                    testEdge = iNext[0]
            else:
                print ('[INPUT]', FreeEdge[iNext[0]], ' (2) TIE Conection InCompletion')
                # logline.append(['ERROR::PRE::[INPUT] {' + str(FreeEdge[nextEdge[0]]) + '} - (2) TIE Connection Incompletion\n'])
                return 0
        ##################### ***************** #########################

        elif len(iNext) == 2:  # if another tie is connected
            if FreeEdge[iNext[0]][5] < 1:
                testEdge = iNext[0]
                #                print ('3.1', FreeEdge[iNext[0]])

                if FreeEdge[iNext[0]][1] == TieStartNode:
                    if saveEdge == nextEdge[0]:
                        NextWay = nextEdge[0]
                    else:
                        NextWay = nextEdge[1]
                    #                    print ('3.1.1',  FreeEdge[iNext[0]])
                    return NextWay
                elif FreeEdge[iNext[0]][1] == startNode:
                    if saveEdge == nextEdge[0]:
                        NextWay = nextEdge[1]
                    else:
                        NextWay = nextEdge[0]
                    #                    print ('3.1.2',  FreeEdge[iNext[0]])
                    return NextWay

            elif FreeEdge[iNext[1][5]] < 1:
                testEdge = iNext[1]
                #                print ('3.2', FreeEdge[iNext[1]])

                if FreeEdge[iNext[1]][1] == TieStartNode:
                    if saveEdge == nextEdge[0]:
                        NextWay = nextEdge[0]
                    else:
                        NextWay = nextEdge[1]
                    #                    print ('3.2.1',  FreeEdge[iNext[0]])
                    return NextWay
                elif FreeEdge[iNext[1]][1] == startNode:
                    if saveEdge == nextEdge[0]:
                        NextWay = nextEdge[1]
                    else:
                        NextWay = nextEdge[0]
                    #                    print ('3.2.2',  FreeEdge[iNext[1]])
                    return NextWay
    return NextWay
def FindTies(FreeEdge):
    global TIENUM
    TIENUM = 1
    i = 0;
    iTemp = 0;
    j = 0
    connectedEdge = []
    TieEdge = []
    while i < len(FreeEdge):

        if FreeEdge[i][5] < 1:
            TIENUM += 1
            nodeStart = FreeEdge[i][0]
            FreeEdge[i][5] = TIENUM
            TieEdge.append(FreeEdge[i])  # marked as TIE edge with No.
            iTemp = i
            while FreeEdge[iTemp][1] != nodeStart:
                j += 1;
                if j > 100:
                    break  # in case infinite loop
                connectedEdge = FindNextEdge(iTemp, FreeEdge)  # find next edge

                if len(connectedEdge) == 1:  # in case of being found just 1 edge
                    iTemp = connectedEdge[0]

                elif len(connectedEdge) == 2:  # when other tie is connected (2 ties are connected)
                    if FreeEdge[connectedEdge[0]][1] == nodeStart:
                        iTemp = connectedEdge[0]
                    elif FreeEdge[connectedEdge[1]][1] == nodeStart:
                        iTemp = connectedEdge[1]
                    else:
                        if FreeEdge[connectedEdge[0]][5] < 1 and FreeEdge[connectedEdge[1]][5] < 1:
                            iTemp = FindTieLoop(nodeStart, connectedEdge, FreeEdge)
                        elif FreeEdge[connectedEdge[0]][5] < 1:
                            iTemp = connectedEdge[0]
                        elif FreeEdge[connectedEdge[1]][5] < 1:
                            iTemp = connectedEdge[1]
                        else:
                            print ('[INPUT] {' + str(FreeEdge[connectedEdge[0]]) + ',' + str(FreeEdge[connectedEdge[1]]) + ' (0) TIE Conection InCompletion')
                            # logline.append(['ERROR::PRE::[INPUT] {' + str(FreeEdge[connectedEdge[0]]) + ', ' + str(FreeEdge[connectedEdge[1]]) + '} - (0) TIE Connection Incompletion\n'])
                            break
                else:
                    print ('[INPUT] 2 or more Ties are Connected.')
                    # logline.append(['ERROR::PRE::[INPUT] 2 or more Ties are Connected.\n'])
                    break

                # After finding next TIE Edge ################################
                FreeEdge[iTemp][5] = TIENUM
                TieEdge.append(FreeEdge[iTemp])
            #                print ('  -', FreeEdge[iTemp])

            # print 'TIENUM = ', TIENUM, 'edge Node=', FreeEdge.edge[connectedEdge[0]][0], \
            # FreeEdge.edge[connectedEdge[0]][1], 'ref node = ', FreeEdge.edge[i][0], FreeEdge.edge[i][1]

            del connectedEdge;
            connectedEdge = []

        i += 1

    #    print ('** TIE EDGE*************')
    #    for i in range(len(TieEdge)):
    #        print (TieEdge[i])
    return TieEdge
    #### Found all Tie surfaces

def FindMaster(edges, Nodes):
    iNum = 2
    Tedges = [];
    length = 0.0
    sLength = 0.0;
    ratio = 0.01
    # logline.append(['* Master Edges\n'])
    nodes = np.array(Nodes)
    while iNum <= TIENUM:
        k = 0;
        saveK = 0
        maxLength = 0.0
        sLength = 0
        while k < len(edges):
            if edges[k][5] == iNum:
                ix = np.where(nodes[:,0]==edges[k][0])[0][0]
                x1 = nodes[ix][2]; y1 = nodes[ix][3]
                ix = np.where(nodes[:,0]==edges[k][1])[0][0]
                x2 = nodes[ix][2]; y2 = nodes[ix][3]

                length = sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))
                sLength += length
                if length > maxLength:
                    maxLength = length
                    saveK = k
            k += 1

        sLength += -maxLength
        if sLength > maxLength * (1.0 + ratio) or sLength < maxLength * (1.0 - ratio):
            print ('TIE - Slave node is too far from master (%s)' % (edges[saveK]))
        Tedges.append(edges[saveK])
        iNum += 1
    return Tedges

def FindSlave(Elements, medge, edges):
    i = 0
    slaveedge = []
    # logline.append(['* Slave Edges\n'])
    while i < len(edges):
        j = 0;
        slave = 0
        while j < len(medge):
            if edges[i][3] == medge[j][3] and edges[i][4] == medge[j][4]:
                slave = 0
                break
            else:
                slave = 1
                j += 1
        if slave == 1:
            slaveedge.append(edges[i])
        i += 1

    for i in range(len(slaveedge)):
        for j in range(len(Elements)):
            if slaveedge[i][4] == Elements[j][0] and Elements[j][6] == 3:
                print ('TIE Slave (%4d) Edge is a part of Triangular Element' % (slaveedge[i][4]))
    return slaveedge

def Layout_outer_edge(Elements, Nodes): 
    AllEdges=FindEdge(Elements)
    FreeEdges=FindFreeEdge(AllEdges)
    CenterNodes = FindCenterNodes(Nodes)
    OutEdges=FindOutEdges(FreeEdges, CenterNodes, Nodes, Elements)
    return OutEdges 

def HowManyEdgeGroup(lstEdge): 
    nds = []
    for ed in lstEdge: 
        nds.append(ed[0])
        nds.append(ed[1])
    nds = np.array(nds)

    cnt = 0
    singles = []
    for nd in nds: 
        idx = np.where(nds==nd)[0]
        if len(idx) ==1: 
            cnt +=1 
            singles.append(int(nd))

    
    return cnt/2, singles 

def FindEdge(elements):
    # elements=[Element No, 1st Node, 2nd Node, 3rd Node, 4th Node, Mat_name, '']
    # edge element [node1, node2, ElsetName, FaceID, elementNo, Tie Definition No]
    i = 0
    edges = []
    while i < len(elements):
        if elements[i][6] == 4:
            edges.append([elements[i][1], elements[i][2], elements[i][5], 'S1', elements[i][0], -1])
            edges.append([elements[i][2], elements[i][3], elements[i][5], 'S2', elements[i][0], -1])
            edges.append([elements[i][3], elements[i][4], elements[i][5], 'S3', elements[i][0], -1])
            edges.append([elements[i][4], elements[i][1], elements[i][5], 'S4', elements[i][0], -1])
        elif elements[i][6] == 3:
            edges.append([elements[i][1], elements[i][2], elements[i][5], 'S1', elements[i][0], -1])
            edges.append([elements[i][2], elements[i][3], elements[i][5], 'S2', elements[i][0], -1])
            edges.append([elements[i][3], elements[i][1], elements[i][5], 'S3', elements[i][0], -1])
        i += 1
    return edges
def Surfaces(OutEdges, Node, OffsetLeftRight, TreadElset, AllElements):
    npn = np.array(Node)

    Press=[]; RimContact=[]; TreadToRoad=[]
    EOffset = NOffset = OffsetLeftRight
    Offset=[EOffset, NOffset]

    low = 100000000.0
    startNode = 0
    nextedge = []
    edgeNo = 0
    i = 0
    opposite = 0
    tmpY=0
    while i < len(Node):
        if Node[i][3] < low and Node[i][0] > Offset[0] and Node[i][2] > 0:
            low = Node[i][3]
            startNode = Node[i][0]
            tmpY = Node[i][2]
        i += 1
        if i > 100000:
            print ("[INPUT] Cannot Find the 1st Node for Pressure")
            return Press, RimContact, TreadToRoad

    for i in range(len(Node)):
        if low == Node[i][3] and tmpY == -Node[i][2]:
            opposite = Node[i][0]
            break

    i = 0
    while i < len(OutEdges):
        if OutEdges[i][0] == startNode:
            edgeNo = i
            break
        i += 1
        if i > 100000:
            print ("[INPUT] Cannot Find the 1st Edge for Pressure")
            return Press, RimContact, TreadToRoad

    
    # print ('**', OutEdges[i]); count=0
    method = 1
    if method ==1 : 
        for edge in OutEdges: 
            if "IL" in edge[2] or "L11" in edge[2] or "HUS" in edge[2] or "RIC" in edge[2]:  
                Press.append(edge)

        MAXY = 0
        MINY = 100000000.0
        YS=[]
        for i in range(len(AllElements)):
            if AllElements[i][5] == 'BEAD_R' or AllElements[i][5] == 'BEAD_L' or AllElements[i][5] == 'BD1':
                # print ("BD1 Elements", AllElements[i])
                for j in [1, 2, 3, 4]:
                    if AllElements[i][j] != '' and  AllElements[i][j] != 0:
                        ix = np.where(npn[:,0]==AllElements[i][j])[0][0]
                        YS.append(abs(npn[ix][2]))
        YS = np.array(YS)
        MINY = np.min(YS)

        i = 0
        while i < len(Press): 
            if Press[i][2] == "RIC" or Press[i][2] == "HUS": 
                ix = np.where(npn[:,0]==Press[i][0])[0][0]; n1=npn[ix]
                ix = np.where(npn[:,0]==Press[i][1])[0][0]; n2=npn[ix]

                if (abs(n1[2]) > MINY or abs(n2[2]) > MINY) : 
                    del(Press[i])
                    continue 
            i += 1



    elif method ==0 :  
        i = edgeNo
        Press.append(OutEdges[edgeNo])
        count = 0
        while OutEdges[i][1] != opposite:
            print(OutEdges[i])
            nextedge = FindNextEdge(i, OutEdges)
            i = nextedge[0]
            # print ('**', OutEdges[i])
            Press.append(OutEdges[i])
            if count > 2 and Press[len(Press)-2][4]  == OutEdges[i][4]:
                break
            if count > 1000:  # in case of infinite loop!!
                break
            count+=1
        #    print ('No of press', len(Press))
        # ADD Bead Base Edge as Pressure Surface
        #    print (AllElements[0])

        MAXY = 0
        MINY = 100000000.0
        YS=[]
        for i in range(len(AllElements)):
            if AllElements[i][5] == 'BEAD_R' or AllElements[i][5] == 'BEAD_L' or AllElements[i][5] == 'BD1':
                # print ("BD1 Elements", AllElements[i])
                for j in [1, 2, 3, 4]:
                    if AllElements[i][j] != '' and  AllElements[i][j] != 0:
                        ix = np.where(npn[:,0]==AllElements[i][j])[0][0]
                        YS.append(abs(npn[ix][2]))
        YS = np.array(YS)
        MAXY = np.max(YS)
        MINY = np.min(YS)
        AVGY = (MAXY + MINY) / 2.0
        # print ("find No", AVGY, MAXY, MINY)

        iNext = nextedge[0]
        nextedge = FindNextEdge(iNext, OutEdges)
        # ValueY = find_z(OutEdges[nextedge[0]][0], Node)
        ix = np.where(npn[:,0]==OutEdges[nextedge[0]][0])[0][0]
        ValueY = npn[ix][2]
        c=0
        # while abs(ValueY) < AVGY:
        while abs(ValueY) < MINY:
            # print ('C=', c, OutEdges[nextedge[0]])
            Press.append(OutEdges[nextedge[0]])
            iNext = nextedge[0]
            nextedge = FindNextEdge(iNext, OutEdges)
            ix = np.where(npn[:,0]==OutEdges[nextedge[0]][1])[0][0]
            ValueY = npn[ix][2]
            c += 1
            if c > 100000:
                print ('[INPUT] Cannot Find the next Pressure Edge (Right)')
                return Press, RimContact, TreadToRoad


        previousedge = FindPreviousEdge(edgeNo, OutEdges)
        # ValueY = find_z(OutEdges[previousedge[0]][1], Node)
        ix = np.where(npn[:,0]==OutEdges[previousedge[0]][1])[0][0]
        ValueY = npn[ix][2]
        # print ("AVG=%.2f, MIN=%.2f, Current Y=%.2f"%(AVGY*1000, MINY*1000, ValueY*1000))
        c=0
        # while abs(ValueY) < AVGY:
        while abs(ValueY) < MINY:
            # print (OutEdges[previousedge[0]])
            # print ("AVG=%.2f, MIN=%.2f, Current Y=%.2f"%(AVGY*1000, MINY*1000, ValueY*1000))
            Press.append(OutEdges[previousedge[0]])
            iNext = previousedge[0]
            previousedge = FindPreviousEdge(iNext, OutEdges)
            ix = np.where(npn[:,0]==OutEdges[previousedge[0]][0])[0][0]
            ValueY = npn[ix][2]
            c += 1
            if c > 100000:
                print ('[INPUT] Cannot Find the next Pressure Edge (Left)')
                return Press, RimContact, TreadToRoad

    #    print ('No of press', len(Press))

    if len(Press) < 1:
        print ('[INPUT] No Surface was created for Inner Pressure')
        return Press, RimContact, TreadToRoad
        # logline.append(['ERROR::PRE::[INPUT] No Surface was created for Inner Pressure\n'])
    else:
        print ('* All Edges for Pressure are searched.')
        # logline.append(['* All Surfaces for Pressure are searched. \n'])

    i = 0
    while i < len(OutEdges):
        if OutEdges[i][2] == 'HUS' or OutEdges[i][2] == 'RIC':
            ipress = 0
            if ipress == 0:
                RimContact.append(OutEdges[i])
                # print "Rim Contact", OutEdges[i]
        i += 1
        if i > 100000:
            print ('[INPUT] Cannot Find the Next Outer Edges ')
            return Press, RimContact, TreadToRoad

    #############################################
    ## ADD 5 edges of BSW
    #############################################
    NoOfAddingEdge = 5
    for i in range(len(RimContact)):
        for j in range(len(OutEdges)):
            if RimContact[i] == OutEdges[j]:
                break
        ne = FindNextEdge(j, OutEdges)
        m=ne[0]
        if OutEdges[m][2] == 'BSW':
            RimContact.append(OutEdges[m])
            for j in range(NoOfAddingEdge-1):
                ne= FindNextEdge(m, OutEdges)
                n=ne[0]
                if OutEdges[n][2] == 'BSW':
                    RimContact.append(OutEdges[n])
                m = n
        ne = FindPreviousEdge(j, OutEdges)
        m = ne[0]
        if OutEdges[m][2] == 'BSW':
            RimContact.append(OutEdges[m])
            for j in range(NoOfAddingEdge-1):
                ne= FindPreviousEdge(m, OutEdges)
                n = ne[0]
                if OutEdges[n][2] == 'BSW':
                    RimContact.append(OutEdges[n])
                m = n
    ###############################################

    if len(RimContact) < 1:
        print ('ERROR::PRE::[INPUT] No Surface was created for Rim Contact  ')
        return Press, RimContact, TreadToRoad
        # logline.append(['ERROR::PRE::[INPUT] No Surface was created for Rim Contact\n'])
    else:
        print ('* All Edges for Rim Contact are searched.')
        # logline.append(['* All Surfaces for Rim Contact are searched. \n'])
    
     ## npn .. node number... , AllElements
    ix = np.where(npn[:,2] <0.1E-03)[0]
    ix1 = np.where(npn[:,2] >-0.1E-03)[0]
    ix = np.intersect1d(ix, ix1)
    mincenter = np.min(npn[ix,3]) - 5.0E-03

    for edge in OutEdges: 
        if edge[2] == "BSW" or edge[2] == "CTR" or edge[2] == "CTB" or edge[2] == "SUT" or edge[2] == "UTR" or edge[2] == "TRW" or edge[2] == "BTT" :  
            ix = np.where(npn[:,0] == edge[0])[0][0]; n1 = npn[ix]
            ix = np.where(npn[:,0] == edge[1])[0][0]; n2 = npn[ix]
            if n1[3] >= mincenter or n2[3] >= mincenter: 
                 TreadToRoad.append(edge)

    if len(TreadToRoad) < 1:
        print ('[INPUT] No Surface was created for Road Contact')
        return Press, RimContact, TreadToRoad
        # logline.append(['ERROR::PRE::[INPUT] No Surface was created for Road Contact\n'])
    else:
        print ('* All Edges for Road Contact are searched.')
        # logline.append(['* All Surfaces for Road Contact are searched. \n'])

    return Press, RimContact, TreadToRoad

def FindFreeEdge(edges):
    freeEdge = []
    npedge = []
    for e in edges: 
        npedge.append([e[0], e[1]])
    npedge = np.array(npedge)

    free = []
    cnt = 0 
    for ed in npedge: 
        idx1 = np.where(npedge[:,:]==int(ed[0]))[0]
        idx2 = np.where(npedge[:,:]==int(ed[1]))[0]
        idx = np.intersect1d(idx1, idx2) 
            
        if len(idx) == 1: 
            free.append(edges[cnt])
        cnt += 1 
    # print ("NO of Free Edge=", len(free))
    return free
def FindCenterNodes(Nodes):
    centers=[]
    for i in range(len(Nodes)):
        if Nodes[i][2] == 0:
            centers.append(Nodes[i][0])
    return centers
def FindOutEdges(FreeEdge, CenterNodes, Nodes, Elements):
    # node of free edge is shared with another tie node
    # ShareNodePos -> 1 or 2
    # for fe in FreeEdge:
        # if fe[2] == "SUT":        print fe
    # for i in range(I):
    MAX = 10000
    ShareNodePos = []
    outEdge = []

    ## Find a 1st surround edge (IL at the center)
    low = 1000000.0
    i = 0
    savei = 0
    while i < len(CenterNodes):
        j = 0
        while j < len(Nodes):
            if CenterNodes[i] == Nodes[j][0]:
                if Nodes[j][3] < low:
                    low = Nodes[j][3]
                    savei = j
            j += 1
        i += 1

    i = 0
    while i < len(FreeEdge):
        if Nodes[savei][0] == FreeEdge[i][0]:
            break
        i += 1

    ## End of 1st Outer Edge finding (IL1)

    FreeEdge[i][5] = 1
    outEdge.append(FreeEdge[i])
    iFirstNode = FreeEdge[i][0]

    count = 0

    #    i=  # i is no matter how big, because i is redefined when next edge is found

    while i < len(FreeEdge):
        count += 1
        if count > MAX:
            print ('[INPUT] CANNOT FIND OUTER EDGES IN THE MODEL (too much iteration)')
            outEdge = []
            return outEdge
        j = 0
        while j < len(FreeEdge):
            if i != j:
                if FreeEdge[i][1] == FreeEdge[j][0]:
                    # print 'edge[i][1], [j][0] ', FreeEdge.edge[i], FreeEdge.edge[j], 'i=', i
                    ShareNodePos.append(j)
            j = j + 1
        #        print ('**', ShareNodePos)

        #        ShareNodePos=FindNextEdge()
        #        print (ShareNodePos, FreeEdge[ShareNodePos[0]][0])
        if len(ShareNodePos) != 0:
            if FreeEdge[ShareNodePos[0]][0] == iFirstNode:
                break
        else:
            print ('[INPUT] CANNOT FIND CONNECTED FREE EDGE. CHECK TIE CONDITION')
            outEdge=[]
            return outEdge
        # print 'sharenodePos count = ', len(ShareNodePos)
        if len(ShareNodePos) == 1:
            FreeEdge[ShareNodePos[0]][5] = 1
            outEdge.append(FreeEdge[ShareNodePos[0]])
            # print ("1,", FreeEdge[ShareNodePos[0]])
            i = ShareNodePos[0]

            del ShareNodePos
            ShareNodePos = []
        else:
            if FreeEdge[i][4] == FreeEdge[ShareNodePos[0]][4]:
                tmpPos = ShareNodePos[1]
                # print ("passed here")
            else:
                SHARE = ShareEdge(FreeEdge[i][4], FreeEdge[ShareNodePos[1]][4], Elements)
                if SHARE ==1:
                    tmpPos = ShareNodePos[0]
                else:
                    tmpPos = ShareNodePos[1]
                    nfe1 = 0; nfe2 = 0
                    for fe in FreeEdge:
                        if fe[4] == FreeEdge[tmpPos][4]:
                            # print (fe)
                            nfe1 += 1
                        if fe[4] == FreeEdge[ShareNodePos[0]][4]:
                            # print (fe)
                            nfe2 += 1
                    # print ("nfe=", nfe, FreeEdge[tmpPos])
                    if nfe1 < nfe2:
                        tmpPos = ShareNodePos[0]
                    elif nfe1 == nfe2:
                        tienode = FreeEdge[tmpPos][0]
                        nc = 0
                        for fe in FreeEdge:
                            if fe[4] == FreeEdge[tmpPos][4] and fe[1] == tienode: 
                                nc += 1
                                break
                        if nc == 0:   tmpPos = ShareNodePos[0]
                    

            FreeEdge[tmpPos][5] = 1
            outEdge.append(FreeEdge[tmpPos])
            # print ("2, ", FreeEdge[ShareNodePos[0]], FreeEdge[ShareNodePos[1]], "-", FreeEdge[tmpPos])
            i = tmpPos
            del ShareNodePos
            ShareNodePos = []
            

    return outEdge
def FindInnerFreeEdges(Oedge, medge): 
    residuals=[]
    for ed1 in Oedge: 
        mch = 0 
        for ed2 in medge: 
            if ed1[0] == ed2[0] and ed1[1] == ed2[1] : 
                mch = 1 
                break 
        if mch == 0: 
            residuals.append(ed1)
    return residuals 
def DivideInnerFreeEdgesToMasterSlave(edges, node_class): 
    npn = np.array(node_class.Node)
    masters=[]
    i = 0 
    while i < len(edges): 
        con1 = 0;         con2 = 0 
        c1e = [];         c2e = []
        ix = np.where(npn[:,0] == edges[i][0])[0][0]; N01 = npn[ix]
        ix = np.where(npn[:,0] == edges[i][1])[0][0]; N02 = npn[ix]
        ML = NodeDistance(N01, N02) 
        Ly=[N01[2], N02[2]]; Lz=[N01[3], N02[3]]
        MinY = min(Ly); MaxY = max(Ly)
        MinZ = min(Lz); MaxZ = max(Lz)
        tslave = []
        for j in range(len(edges)): 
            
            if i == j : continue 
            
            if edges[i][0] == edges[j][0] or edges[i][0] == edges[j][1] :
                ix = np.where(npn[:,0] == edges[j][0])[0][0]; N1 = npn[ix]
                ix = np.where(npn[:,0] == edges[j][1])[0][0]; N2 = npn[ix]
                SL = NodeDistance(N1, N2)  
                if ML < SL: 
                    continue 
                if edges[i][0] == edges[j][0]: 
                    if N2[2] >= MinY and N2[2] <= MaxY and N2[3] >= MinZ and N2[3] <= MaxZ: 
                        dist = DistanceFromLineToNode2D(N2, [N01, N02], onlydist=1)
                        if dist < .10E-03 : 
                            con1 = 1 
                            c1e = edges[j]
                            tslave.append(edges[j])
                else: 
                    if N1[2] >= MinY and N1[2] <= MaxY and N1[3] >= MinZ and N1[3] <= MaxZ: 
                        dist = DistanceFromLineToNode2D(N1, [N01, N02], onlydist=1)
                        if dist < .10E-03 : 
                            con1 = 1 
                            c1e = edges[j]
                            tslave.append(edges[j])

            if edges[i][1] == edges[j][0] or edges[i][1] == edges[j][1] : 
                ix = np.where(npn[:,0] == edges[j][0])[0][0]; N1 = npn[ix]
                ix = np.where(npn[:,0] == edges[j][1])[0][0]; N2 = npn[ix]
                SL = NodeDistance(N1, N2)  
                if ML < SL: 
                    continue 

                if edges[i][1] == edges[j][0]: 
                    if N2[2] >= MinY and N2[2] <= MaxY and N2[3] >= MinZ and N2[3] <= MaxZ: 
                        dist = DistanceFromLineToNode2D(N2, [N01, N02], onlydist=1)
                        if dist < .10E-03 : 
                            con2 = 1 
                            c2e = edges[j]
                            tslave.append(edges[j])
                else: 
                    if N1[2] >= MinY and N1[2] <= MaxY and N1[3] >= MinZ and N1[3] <= MaxZ: 
                        dist = DistanceFromLineToNode2D(N1, [N01, N02], onlydist=1)
                        if dist < .10E-03 : 
                            con2 = 1 
                            c2e = edges[j]
                            tslave.append(edges[j])

            if con1 == 1 and con2 ==1: 
                break 
        
        if con1 ==1 or con2 == 1: 
            masters.append([edges[i], tslave])
        i+=1 

    excluding = []
    isError = 0 
    TIE_ERROR = []
    for e in masters: 
        # print ("*****************")
        # print (e[0])
        # print ("-----------------")
        # print (e[1])
        excluding.append(e[0])
        excluding.append(e[1][0])
        if len(e[1]) <2: 
            print ("## Error to fine Tie Master surface (%d)"%(e[0][4]))
            TIE_ERROR.append(e[0][4])
            isError = 1
            continue 
            
        excluding.append(e[1][1])
    if isError == 1: 
        master_edge=[];  slave_edge=[]
        return master_edge, slave_edge, TIE_ERROR

    print ("* Tie No. in layout mesh =%d"%(len(masters)))
    master_edge = []
    slave_edge = []
    for i, ed in enumerate(masters): 
        master_edge.append(ed[0])
        s_temp=[]
        s_temp.append(ed[1][0])
        
        s_temp.append(ed[1][1])
        if ed[1][0][0] == ed[1][1][1] or ed[1][0][1] == ed[1][1][0] : 
            slave_edge.append(s_temp)
            # print ("* Slave Edges %2d, No=%d"%(i, len(s_temp)))
            continue 

        nexts = ConnectedEdge(ed[1][0], edges, exclude=excluding)
        s_temp.append(nexts[0])
        # print (ed[0], ":", nexts)
        if nexts[0][0] != ed[1][1][1] and nexts[0][1] != ed[1][1][0] : 
            excluding.append(nexts[0]) 
            nexts = ConnectedEdge(nexts[0], edges, exclude=excluding)
            s_temp.append(nexts[0])
            # print (ed[0], ":::", nexts)
        slave_edge.append(s_temp)
        # print ("**Slave Edges %2d, No=%d"%(i, len(s_temp)))

    return master_edge, slave_edge, TIE_ERROR
def FindNextEdge(refEdge, Edges):
    tmpi = refEdge;
    connected = []
    for m in range(len(Edges)):
        if tmpi != m:
            if Edges[tmpi][1] == Edges[m][0]:
                connected.append(m)
    return connected
def FindPreviousEdge(refEdge, Edges):
    tmpi = refEdge;
    connected = []
    for m in range(len(Edges)):
        if tmpi != m:
            if Edges[tmpi][0] == Edges[m][1]:
                connected.append(m)
    return connected
def Area(NodeList, Node, XY=23, **args):   ## Calculate Area of a polygon
    errorimage = 1
    for key, value in args.items():
        if key == 'xy' :   XY = int(value)
        if key == 'error': errorimage= int(value)
    
    if len(Node) > 0:
        node = np.array(Node) 
    
        ii = int(XY/10)
        jj = int(XY)%10
        
        n = len(NodeList)
        x = [];       y = []
        
        for nd in NodeList: 
            ix = np.where(node[:,0]==nd)[0][0]
            Ni = node[ix]
            x.append(Ni[ii])
            y.append(Ni[jj])
    
        x.append(x[0])
        y.append(y[0])
        
        A = [0.0, 0.0, 0.0]

        for i in range(n):
            s = x[i] * y[i + 1] - x[i + 1] * y[i]
            A[0] += s
            A[1] += (x[i] + x[i + 1]) * s
            A[2] += (y[i] + y[i + 1]) * s

        A[0] = A[0] / 2.0
        try:
            A[1] = A[1] / A[0] / 6
            A[2] = A[2] / A[0] / 6
        except:
            if errorimage > 0: 
                print ("!! Error to calculate Area ", A)
                pNode = NODE()
                for i in range(n):
                    ix = np.where(node[:,0]==nd)[0][0]
                    Ni = node[ix]
                    pNode.Add(Ni)
                pNode.Image("Error_Area_"+str(pNode.Node[0][0])+".png", size=1.5)
            return [0.0, 0.0, 0.0]

        if A[0] < 0:
            A[0] = -A[0]
            # print 'Negative Area Calculation! '
        return A
    else:
        print ("Length of Node is 0")
        return [0.0, 0.0, 0.0]
def Write2DFile(FileName, Node, AllElements, Elset, TreadToRoad, Press, RimContact, MasterEdges, SlaveEdges, Offset, CenterNodes, Comments):
    npel=[]
    npn =[]
    for el in AllElements:
        npel.append(el[0])
        npn.append(el[1]); npn.append(el[2]); npn.append(el[3])
        if el[4] > 0: npn.append(el[4])
    npel = np.array(npel)
    npn = np.array(npn)
    npn = np.unique(npn)

    i = 0
    while i < len(Node):
        ix = np.where(npn[:] == Node[i][0])[0]
        if len(ix) == 0: 
            del(Node[i])
            continue 
        i += 1

    for eset in Elset: 
        i = 1
        while  i < len(eset): 
            ix = np.where(npel[:]==eset[i])[0] 
            if len(ix) == 0: 
                del(eset[i])
                continue 
            i += 1


    f = open(FileName, 'w')

    fline = []
    for i in range(len(Comments)):
        fline.append([Comments[i]])
    fline.append(['*NODE, SYSTEM=R, NSET=ALLNODES\n'])

    i = 0
    while i < len(Node):
        fline.append(['%10d, %15.6E, %15.6E, %15.6E\n' % (Node[i][0], Node[i][3], Node[i][2], Node[i][1])])
        i += 1
    i = 0
    fline.append(['*ELEMENT, TYPE=MGAX1, ELSET=ALLELSET\n'])
    while i < len(AllElements):
        if AllElements[i][6] == 2:
            fline.append(['%10d, %10d, %10d\n' % (AllElements[i][0], AllElements[i][1], AllElements[i][2])])
        i += 1
    i = 0
    fline.append(['*ELEMENT, TYPE=CGAX3H, ELSET=ALLELSET\n'])
    while i < len(AllElements):
        if AllElements[i][6] == 3:
            fline.append(['%10d, %10d, %10d, %10d\n' % (AllElements[i][0], AllElements[i][1], AllElements[i][2], AllElements[i][3])])
        i += 1
    i = 0
    fline.append(['*ELEMENT, TYPE=CGAX4H, ELSET=ALLELSET\n'])
    while i < len(AllElements):
        if AllElements[i][6] == 4:
            fline.append(['%10d, %10d, %10d, %10d, %10d\n' % (AllElements[i][0], AllElements[i][1], AllElements[i][2], AllElements[i][3], AllElements[i][4])])
        i += 1
    isCH1=0
    isCH2=0
    isBDr=0
    isBDl=0
    for i in range(len(Elset)):
        fline.append(["*ELSET, ELSET=%s\n" %(Elset[i][0])])
        if 'CH1' in Elset[i][0]:
            isCH1=1
        if 'CH2' in Elset[i][0]:
            isCH2=1
        if 'BEAD_R' in Elset[i][0]:
            isBDr =1
        if 'BEAD_L' in Elset[i][0]:
            isBDl =1


        k = 0
        for j in range(1, len(Elset[i])):
            if ((k + 1) % 10 != 0):
                if (k +2) == len(Elset[i]):
                    fline.append(['%8d\n' % (Elset[i][j])])
                else:
                    fline.append(['%8d,' % (Elset[i][j])])
            else:
                fline.append(['%8d\n' % (Elset[i][j])])
            k += 1
    if isCH1 == 1:
        fline.append(['*ELSET,  ELSET=CH1\n'])
        fline.append([' CH1_R, CH1_L\n'])
    if isCH2 == 1:
        fline.append(['*ELSET,  ELSET=CH2\n'])
        fline.append([' CH2_R, CH2_L\n'])

    i = 0
    fline.append(['*SURFACE, TYPE=ELEMENT, NAME=CONT\n'])
    while i < len(TreadToRoad):
        fline.append(['%6d, %s\n' % (TreadToRoad[i][4], TreadToRoad[i][3])])
        i += 1

    i = 0
    fline.append(['*SURFACE, TYPE=ELEMENT, NAME=PRESS\n'])
    while i < len(Press):
        fline.append(['%6d, %s\n' % (Press[i][4], Press[i][3])])
        i += 1

    i = 0
    fline.append(['*SURFACE, TYPE=ELEMENT, NAME=RIC_R\n'])
    i=0
    while i < len(RimContact):
        for nd in Node:
            if RimContact[i][0] == nd[0]: 
                if nd[2]<0: 
                    fline.append(['%6d, %s\n' % (RimContact[i][4], RimContact[i][3])])
                    break
        i += 1

    i = 0
    fline.append(['*SURFACE, TYPE=ELEMENT, NAME=RIC_L\n'])
    while i < len(RimContact):
        for nd in Node:
            if RimContact[i][0] == nd[0]: 
                if nd[2]>0: 
                    fline.append(['%6d, %s\n' % (RimContact[i][4], RimContact[i][3])])
                    break
        i += 1


    cnt = 0 
    for mst in MasterEdges: 
        cnt += 1
        fline.append(['*SURFACE, TYPE=ELEMENT, NAME=Tie_m' + str(cnt) + '\n'])
        fline.append(['%6d, %s\n' % (mst[4], mst[3])])
        fline.append(['*SURFACE, TYPE=ELEMENT, NAME=Tie_s' + str(cnt) + '\n'])

        for slt in SlaveEdges[cnt-1]: 
            fline.append(['%6d, %s\n' % (slt[4], slt[3])])
        
        fline.append(['*TIE, NAME=TIE_' + str(cnt) + '\n'])
        fline.append(['Tie_s' + str(cnt) + ', ' + 'Tie_m' + str(cnt) + '\n'])
        
    ###########################################################

    if isBDr ==1 and isBDl ==1:
        fline.append(['*ELSET, ELSET=BD1\n BEAD_R, BEAD_L\n'])
    elif isBDr == 1 :
        fline.append(['*ELSET, ELSET=BD1\n BEAD_R\n'])
    elif isBDl ==1:
        fline.append(['*ELSET, ELSET=BD1\n BEAD_L\n'])

    Bdr = [0, 0]
    for i in range(len(AllElements)):
        if AllElements[i][5] == 'BEAD_L':
            Bdr[0] = AllElements[i][1]
        if AllElements[i][5] == 'BEAD_R':
            Bdr[1] = AllElements[i][1]

    if Bdr[0] != 0:
        fline.append(['\n*NSET, NSET=BD_L\n'])
        fline.append([str(Bdr[0])])
    if Bdr[1] != 0:
        fline.append(['\n*NSET, NSET=BD_R\n'])
        fline.append([str(Bdr[1])])


    if Bdr[0] != 0 and Bdr[1] != 0:
        fline.append(['\n*NSET, NSET=BDR\n BD_R, BD_L\n'])
    elif Bdr[1] != 0:
        fline.append(['\n*NSET, NSET=BDR\n BD_R\n'])
    elif Bdr[0] != 0 :
        fline.append(['\n*NSET, NSET=BDR\n BD_L\n'])
    else:
        pass

    fline.append(['*NSET, NSET=CENTER\n'])

    i = 0
    while i < len(CenterNodes):
        if ((i + 1) % 10 == 0):
            fline.append(['%8d\n' % (CenterNodes[i])])
        else:
            fline.append(['%8d,' % (CenterNodes[i])])
        i += 1

    f.writelines('%s' % str(item[0]) for item in fline)

    f.close()
##########################################################################################
# End of Profile CLASS    
##########################################################################################
class COPYLAYOUT: 
    def __init__(self, class_layout): 
        self.Node = NODE()
        for nd in class_layout.Node.Node:
            self.Node.Node.append(nd)
        self.Element = ELEMENT()
        for el in class_layout.Element.Element: 
            self.Element.Element.append(el)
        self.TieMaster = []
        for tie in class_layout.TieMaster : 
            self.TieMaster.append(tie)
        
        self.TieSlave = []
        for tie in class_layout.TieSlave : 
            self.TieSlave.append(tie)

        self.Press = class_layout.Press 
        self.RimContact = class_layout.RimContact 

    def __del__(self): 
        pass 
class COPYPTN: 
    def __init__(self, class_ptn): 
        self.npn = np.array(class_ptn.npn)
        self.nps = class_ptn.Solid
        self.freetop = class_ptn.freetop 
        self.freebottom = class_ptn.freebottom
        self.surf_pitch_up = class_ptn.surf_pitch_up
        self.surf_pitch_down = class_ptn.surf_pitch_down
        self.SF_fulldepthgrooveside = class_ptn.SF_fulldepthgrooveside
        self.SF_subgrooveside = class_ptn.SF_subgrooveside
        self.KerfsideSurface = class_ptn.KerfsideSurface
        self.surf_pattern_neg_side = class_ptn.surf_pattern_neg_side
        self.surf_pattern_pos_side = class_ptn.surf_pattern_pos_side
        self.Free_Surface_without_BTM = class_ptn.Free_Surface_without_BTM
        self.SF_fulldepthgroove = class_ptn.SF_fulldepthgroove
        self.SF_subgroove = class_ptn.SF_subgroove
        self.beforeside = class_ptn.beforeside
    def __del__(self): 
        pass 
class PATTERN:
    def __init__(self, filename,  test=0, start_number=10000000):
        self.PI = 3.14159265358979323846
        self.GlobalXY=21
        self.Node=[]   ## float : Id, x, y, z
        # self.npn=[]          ## ** 
        # self.Node_Origin = []
        self.Solid=[]  ## int : id, n1, ..., n8, 6 or 8, center (*10^6 -> make it into integer)
        self.Beam=[];         self.UpFront=[];         self.UpBack=[];         self.LowBack=[];         self.Center=[]

        self.GrooveCenter=[]
        
        self.Surface=[]
        self.leftprofile =[]
        self.rightprofile = []
        self.pitch1=[]
        self.pitchsequence =[] 
        
        self.NoPitch = 0
        self.ModelGD = 0.0
        self.PatternWidth =0.0
        self.TreadDesignWidth = 0.0
        self.HalfDia = 0.0
        self.diameter = 0.0 
        self.upFrontMaxY = 0.0

        self.Nstart = 10_000_000
        self.Estart = 10_000_000
        self.profilescaling = 0.001
        self.pitchscaling = 0.001

        self.surf_pattern_neg_side=[]
        self.surf_pattern_pos_side=[]
        self.SF_fulldepthgrooveside=[]

        self.Edge_bottomSurface = []

        self.IsError = 0 
        self.errorcode = 0 
        self.KerfsideSurface = []
        self.edge_top_surface = []

        self.shoulderType = 'R'

        ####################################################################################################
        print ("############################################")
        print ("## Reading Pattern Mesh file (*.ptn)")
        print ("############################################")
        print (filename)

        result_reading = self.ReadPtn(filename)
        if result_reading >= 100: 
            self.IsError = 1
            return 
        
        if result_reading ==0 : 
            print ("## Error to read pattern mesh file")
            self.IsError =  1 
            return 
        self.npn = np.array(self.Node)
        self.Node_Origin = np.array(self.npn) 
        self.nps = np.array(self.Solid)
        self.pitchlength = self.Pitchlength()
        self.errsolid = [] 
        self.HalfDia = round(self.HalfDia*self.profilescaling, 5)

        if len(self.UpFront) > 0: 
            ix = np.where(self.npn[:,0]== self.UpFront[0][1])[0][0]
            if self.npn[ix][3] != self.HalfDia: 
                print ("# Half diameter=%.2f, Guide Ht=%.2f"%(self.HalfDia*1000, self.npn[ix][3]*1000))
                print ("  Nodes are shifted (%.4f)"%((self.HalfDia - self.npn[ix][3])*1000))
                self.npn[:,3] += self.HalfDia - self.npn[ix][3]

                self.diameter = round(self.npn[ix][3] *2.0, 5)
                
            nds = []
            for nd in self.UpFront:
                nds.append(nd[1]); nds.append(nd[2])
            nds = np.array(nds)
            nds = np.unique(nds)
            upnodes=[]
            for nd in nds:
                ix = np.where(self.npn[:,0]==nd)[0][0]
                upnodes.append(self.npn[ix])
            upnodes = np.array(upnodes)
            self.upFrontMaxY = np.max(upnodes[:, 2])
        else:
            self.upFrontMaxY = self.npn[:,2]


        # t0=time.time()
        self.nps, self.Surface, printout, self.errsolid =  Generate_all_surfaces_on_solid(self.npn, self.nps, diameter=self.diameter)
        # t1 = time.time(); print (" Surface GEN %.3f"%(t1-t0))
        if len(self.errsolid)> 0 : 
            print (printout)
        else: 
            self.Solid = self.nps
            print (printout)
            
            self.Edge = AllEdgesInSurface(self.Surface, self.npn)

            ## surface = [El_id, Face_Id(1~6), type(3 or 4), layer, center X, y, z, n1, n2, n3, n4]
            ## all surfaces are created at 'RedefineSolid()'
            self.freesurface=[]
            self.freetop =[]
            self.freebottom=[]
            self.surf_pitch_down=[]
            self.surf_pitch_up=[]

            # t0=time.time()
            self.freetop, self.freebottom, self.uncheckedfree, self.Surface = self.Top_Bottom_FreeSurfacesFromAllSurfaces_01(self.Surface, self.npn, radius=self.diameter/2.0, margin=1.0E-03)
            # t1 = time.time(); print ("## Top/Btm/Free %.3f"%(t1-t0))
            if len(self.freetop) ==0: 
                print ("## Cannot find Top Surface ") 
                print ("## Check the tire Half diameter in *.ptn\n")
                print ("## Current half diameter=%.2fmm"%(np.max(self.npn[:,3])*1000))
                self.IsError = 1 
                return 
            nds = []
            for sf in self.freetop: 
                nds.append(sf[7]); nds.append(sf[8]); nds.append(sf[9])
                if sf[10] >= 10**7: nds.append(sf[10])
            nds = np.array(nds)
            nds = np.unique(nds)
            tnodes =[]
            for nd in nds: 
                ix = np.where(self.npn[:,0]==nd)[0][0]
                tnodes.append(self.npn[ix])
            tnodes = np.array(tnodes)
            topHalfWidth = np.max(tnodes[:,2]) 
            # print ("Shoulder Type")
            # print (topHalfWidth,",",  self.upFrontMaxY )
            if round(topHalfWidth, 5) < round(self.upFrontMaxY, 5) : 
                self.shoulderType ='S'
                self.TreadDesignWidth = round(topHalfWidth * 2.0, 4) 
            else: self.shoulderType ='R'

            # print("Up Beam Max Y=%.3f, Top Surface Max Y=%.3f"%(self.upFrontMaxY*1000, np.max(tnodes[:,2])*1000 ))
                    
            if self.shoulderType == "R":   print ("* Pattern Type : ROUND")
            else:  print ("* Pattern Type : SQUARE")
            # print (  "  Top surfaces    : %d EA"%(len(self.freetop)))
            # print (  "  Bottom surfaces : %d EA "%(len(self.freebottom)))
            # print (  "  Other Free surfaces : %d EA "%(len(self.uncheckedfree)))

            if len(self.freebottom) == 0: 
                self.IsError = 1 
                print ("# Error to find free surfaces of pattern")
                return 
            self.edge_top_surface = self.SurfaceBoundary(self.freetop)

            solnodes=[]
            for sol in self.nps: 
                solnodes.append(sol[1]); solnodes.append(sol[2]); solnodes.append(sol[3]); solnodes.append(sol[4])
                solnodes.append(sol[5]); solnodes.append(sol[6])
                if sol[7] > 0: 
                    solnodes.append(sol[7]); solnodes.append(sol[8])
            solnodes = np.array(solnodes)
            solnodes = np.unique(solnodes)
            solnd = []
            for sn in solnodes:
                ix = np.where(self.npn[:,0]==sn)[0][0]
                solnd.append(self.npn[ix])
            self.solidnodes = np.array(solnd)

            # t0 = time.time()

            method2pitch = 3
            if method2pitch ==2: 
                # print ("Pitch search method 2")
                self.totalsurfaces = np.array(self.uncheckedfree) 
                self.Free_Surface_without_BTM=np.array(self.uncheckedfree)
                self.surf_pitch_up, self.surf_pitch_down, self.surf_pattern_neg_side, self.surf_pattern_pos_side \
                    = self.pitch_updown_surface(self.uncheckedfree, self.freebottom, method=2, debug=0, npn=self.npn)
                ## divide all side surfaces into main groove side, sub groove side, kerf side 
                ## surface = [El_id, Face_Id(1~6), type(3 or 4), layer, center X, y, z, n1, n2, n3, n4]
                ## main groove side 

            elif method2pitch ==3: 
                # print ("Pitch search method 3")
                self.totalsurfaces = np.array(self.uncheckedfree) 
                self.Free_Surface_without_BTM=np.array(self.uncheckedfree)
                self.surf_pitch_up, self.surf_pitch_down, self.surf_pattern_neg_side, self.surf_pattern_pos_side, \
                    unpaired = self.pitch_updown_surface(self.uncheckedfree, self.freebottom, method=3, debug=0,\
                         npn=self.npn, halfOD=self.HalfDia, shoulder=self.shoulderType)

                for sf in unpaired: 
                    ix1 = np.where(self.uncheckedfree[:, 0]==sf[0])[0]
                    ix2 = np.where(self.uncheckedfree[:, 1]==sf[1])[0]
                    ix = np.intersect1d(ix1, ix2)
                    if len(ix) == 1: 
                        self.uncheckedfree = np.delete(self.uncheckedfree, ix[0], axis=0)
                        
                
            else: 
                self.surf_pitch_up, self.surf_pitch_down \
                    = self.pitch_updown_surface(self.uncheckedfree, self.freebottom, method=0, debug=0)

            # self.totalsurfaces = np.array(self.uncheckedfree) 
            # self.Free_Surface_without_BTM=np.array(self.uncheckedfree)


            
            uncheckedfree = self.uncheckedfree
            # print ("free surface", len(self.uncheckedfree))
            for sf in self.surf_pitch_up: 
                ix1 = np.where(self.uncheckedfree[:, 0]==sf[0])[0]
                ix2 = np.where(self.uncheckedfree[:, 1]==sf[1])[0]
                ix = np.intersect1d(ix1, ix2)
                if len(ix) == 1: 
                    self.uncheckedfree = np.delete(self.uncheckedfree, ix[0], axis=0)
                    

            for sf in self.surf_pitch_down: 
                ix1 = np.where(self.uncheckedfree[:, 0]==sf[0])[0]
                ix2 = np.where(self.uncheckedfree[:, 1]==sf[1])[0]
                ix = np.intersect1d(ix1, ix2)
                if len(ix) == 1: 
                    self.uncheckedfree = np.delete(self.uncheckedfree, ix[0], axis=0)
            
            # print ("DEL pitch surf", len(self.uncheckedfree), ", ", len(self.surf_pitch_up)+len(self.surf_pitch_down))
            for sf in self.surf_pattern_neg_side: 
                ix1 = np.where(self.uncheckedfree[:, 0]==sf[0])[0]
                ix2 = np.where(self.uncheckedfree[:, 1]==sf[1])[0]
                ix = np.intersect1d(ix1, ix2)
                if len(ix) == 1: 
                    self.uncheckedfree = np.delete(self.uncheckedfree, ix[0], axis=0)
            for sf in self.surf_pattern_pos_side: 
                ix1 = np.where(self.uncheckedfree[:, 0]==sf[0])[0]
                ix2 = np.where(self.uncheckedfree[:, 1]==sf[1])[0]
                ix = np.intersect1d(ix1, ix2)
                if len(ix) == 1: 
                    self.uncheckedfree = np.delete(self.uncheckedfree, ix[0], axis=0)

            self.SF_pitchside = np.concatenate((self.surf_pattern_neg_side,  self.surf_pattern_pos_side), axis=0)
            
            # print ("DEL side surf", len(self.uncheckedfree), ", ", len(self.surf_pattern_neg_side)+len(self.surf_pattern_pos_side))

            idxs = np.where(uncheckedfree[:, 1]==2)[0]  ## top surface 
            upsurf=uncheckedfree[idxs]

            SF_fulldepthgroove=[]
            SF_subgroove=[]
            btm= self.freebottom[:,0]
            for sf in upsurf: 
                ix = np.where(btm==sf[0])[0]
                if len(ix) >    0 :             SF_fulldepthgroove.append(sf)
                else:                           SF_subgroove.append(sf)
            self.SF_fulldepthgroove = np.array(SF_fulldepthgroove)
            
            
            ###############
            ## Error eccurs when the main groove bottom surface is also on the pattern side
            ## this removes the surfaces on the pattern side from main groove bottom 
            sideSolidIds = self.SF_pitchside[:,0]
            sideSolidIds = np.unique(sideSolidIds)

            i = 0 
            while i < len( self.SF_fulldepthgroove):
                idx = np.where(sideSolidIds[:]==self.SF_fulldepthgroove[i][0])[0]
                if len(idx): 
                    self.SF_fulldepthgroove = np.delete(self.SF_fulldepthgroove, i, axis=0 )
                    continue 
                i += 1
            #############################################################

            SmoothPattern = 0 
            if len(self.SF_fulldepthgroove) ==0: 
                btmn = []
                for sf in self.freebottom: 
                    btmn.append(sf[7])
                    btmn.append(sf[8])
                    btmn.append(sf[9])
                    if sf[10] > 0: btmn.append(sf[10])
                btmn = np.array(btmn) 
                btmn = np.unique(btmn)

                dun = np.array(self.solidnodes)
                for e in btmn: 
                    ix = np.where(dun[:,0]==e)[0][0]
                    dun = np.delete(dun, ix, axis=0)
                FDGrooveR = np.min(dun[:,3])
                SmoothPattern = 1 
            else:     
                FDGrooveR = np.min(self.SF_fulldepthgroove[:, 6])
                # FDGrooveR = np.min(FDGrooveR)
            MODEL_R =  self.diameter/2.0

            if self.ModelGD < 0.0011: 
                self.ModelGD = round(MODEL_R - FDGrooveR, 4)

            for sf in self.SF_fulldepthgroove: 
                ix1 = np.where(self.uncheckedfree[:, 0]==sf[0])[0]
                ix2 = np.where(self.uncheckedfree[:, 1]==sf[1])[0]
                ix = np.intersect1d(ix1, ix2)
                if len(ix) == 1: 
                    self.uncheckedfree = np.delete(self.uncheckedfree, ix[0], axis=0)
            # print ("DEL main groove", len(self.uncheckedfree), ", ", len(self.SF_fulldepthgroove))

            Vrt = [0, 0, 0, -1.0]
            self.SF_subgroove=[]
            for sf in SF_subgroove:
                ix = np.where(self.npn[:,0] == sf[7])[0][0]; n1 = self.npn[ix] 
                ix = np.where(self.npn[:,0] == sf[8])[0][0]; n2 = self.npn[ix] 
                ix = np.where(self.npn[:,0] == sf[9])[0][0]; n3 = self.npn[ix] 
                # NV = NormalVector_plane(n1, n2, n3)
                V_angle = Angle_Between_Vectors( NormalVector_plane(n1, n2, n3), Vrt)
                if sf[2] ==3 and V_angle < 0.35 : #and V_angle < 0.35:  ## 0.35 radian = 20.0 degrees
                    self.SF_subgroove.append(sf)
                    # print ("IN  : %d, angle=%.2f"%(sf[0]-10**7, degrees(V_angle)))
                elif sf[2] ==4 and V_angle < 0.523 : #and V_angle < 0.523:  ## 0.523 radian = 30.0 degrees
                    self.SF_subgroove.append(sf)
                    # print ("IN  : %d, angle=%.2f"%(sf[0]-10**7, degrees(V_angle)))
                else: 
                    pass
                    # print ("OUT : %d, angle=%.2f"%(sf[0]-10**7, degrees(V_angle)))
            
            self.SF_subgroove = np.array(self.SF_subgroove)

            for sf in self.SF_subgroove: 
                ix1 = np.where(self.uncheckedfree[:, 0]==sf[0])[0]
                ix2 = np.where(self.uncheckedfree[:, 1]==sf[1])[0]
                ix = np.intersect1d(ix1, ix2)
                if len(ix) == 1: 
                    self.uncheckedfree = np.delete(self.uncheckedfree, ix[0], axis=0)

            allix = np.arange(len(uncheckedfree))
            idxs = np.setdiff1d(allix, idxs)   
            side=self.uncheckedfree                   ## side surface 

            # print ("DEL sub groove", len(self.uncheckedfree), ", ", len(self.SF_subgroove))

            # t1 = time.time(); print (" GRVE %.3f"%(t1-t0))
            # t0=time.time()
            
            ###############################################################
            ## Searching Kerf Base Edge   : self.RemoveGrooveSideSurface(base surface, all side surface)
            ###############################################################
            
            self.beforeside = np.array(self.uncheckedfree)
            i = 0
            while i < len(self.uncheckedfree): 
                j = i+1
                while j < len(self.uncheckedfree): 
                    if self.uncheckedfree[i][0] == self.uncheckedfree[j][0] and self.uncheckedfree[i][1] == self.uncheckedfree[j][1]: 
                        self.uncheckedfree = np.delete(self.uncheckedfree, j, axis=0)
                        j -= 1 
                    j += 1
                i += 1

            # t1 = time.time(); print ("pitch sides surface time %.3f"%(t1-t0))
            # t0 = time.time()
            self.SF_subgrooveside = []
            self.KerfsideSurface = []

            self.SF_fulldepthgrooveside, self.SF_subgroove, self.uncheckedfree = self.Groove_side(self.uncheckedfree, self.SF_fulldepthgroove, self.SF_subgroove, self.freetop, self.npn, full_depth=1, shoulderType=self.shoulderType)
            if len(self.SF_subgroove) > 0: 
                self.SF_subgrooveside, self.KerfsideSurface = self.Groove_side(free=self.uncheckedfree, main_bottom=self.SF_subgroove, top_surf=self.freetop, npn=self.npn, full_depth=0, shoulderType=self.shoulderType)
            else: 
                self.KerfsideSurface = self.uncheckedfree

            if self.errorcode !=0: 
                detail = "ERROR! during Pitch side surface detecting."
                print (detail)
                
            if method2pitch ==1: 
                mxy = np.max(self.npn[:,2])
                mny = np.min(self.npn[:,2])
                margin = 3.0E-3 
                for sf in self.SF_pitchside: 
                    if sf[10] > 0: 
                        ix = np.where(self.npn[:,0] == sf[7])[0][0]; n1 = self.npn[ix]
                        ix = np.where(self.npn[:,0] == sf[8])[0][0]; n2 = self.npn[ix]
                        ix = np.where(self.npn[:,0] == sf[9])[0][0]; n3 = self.npn[ix]
                        ix = np.where(self.npn[:,0] == sf[10])[0][0]; n4 = self.npn[ix]
                        
                        if (abs(n1[2] - n2[2]) < 0.1E-03 and abs(n3[2] - n4[2]) < 0.1E-03 ) and abs(n4[3] - n1[3]) > abs(n4[2] - n1[2]) and (n4[2] > mxy - margin or n4[2] < mny + margin)  : 
                            if n1[2] > mxy - margin: self.surf_pattern_pos_side.append(sf) 
                            if n1[2] < mny + margin: self.surf_pattern_neg_side.append(sf) 

            # t1 = time.time(); print ("free surface time %.3f"%(t1-t0))

            # t1 = time.time(); print (" kerf %.3f"%(t1-t0))
            # t0=time.time()
            print ("* Surfaces : %d EA (Elements:%d EA)"%(len(self.Surface), len(self.Solid)))
            print ("  All Free : %d, Top : %d, Bottom : %d"%(len(self.freetop)+len(self.freebottom)+len(self.uncheckedfree), len(self.freetop), len(self.freebottom) ))
            
            print ("  Main Groove Bottom: %d, Sub Groove: %d \n  Other Sides=%d(grv %d, kerf %d)"%(\
                        len(self.SF_fulldepthgroove), len(self.SF_subgroove), len(self.surf_pattern_neg_side) + len(self.surf_pattern_pos_side), \
                            len(self.SF_subgrooveside), len(self.KerfsideSurface)))
            print ("\n*********************************************")
            print ("* Model Pattern")
            print ("* Diameter=%.2f(R=%.2f)"%(self.diameter*1000, MODEL_R*1000))
            print ("* Total Width=%.2f, Design Width=%.2f"%(self.PatternWidth*1000, self.TreadDesignWidth*1000))
            print ("* Groove depth=%.2fmm"%(self.ModelGD*1000))
            print ("* Pitch length=%.2fmm"%(self.pitchlength*1000))
            print ("*********************************************\n")

            NodesInFullDepthGrooves = self.NodesInSurface(self.SF_fulldepthgroove)
            self.Boundary_fulldepthgroove = self.SurfaceBoundary(self.SF_fulldepthgroove)  ## the nodes are counter-clockwise 
            tblocks = self.MakeEdgesToBlockGroup(self.Boundary_fulldepthgroove)       ## the nodes are still counter-clockwise direction 
            GroupsBoundary_fulldepthgroove=[]
            group_blockboundarypoints =[]
            blockboundarypoints =[]

            # print ("grouping block edges is done!")

            edge_blocks=[] ## base block edge 
            edge_semigroove=[]

            for i, block in enumerate(tblocks):
                polygon =[]
                for k in block: 
                    index = np.where(self.npn == k[0])
                    polygon.append([self.npn[index[0][0]][1], self.npn[index[0][0]][2] ])
                group_blockboundarypoints.append(polygon)

            not_block =[]      
            relation_blocks=[]
            for _ in group_blockboundarypoints: 
                relation_blocks.append([])
            
            for i, block in enumerate(group_blockboundarypoints): 
                point = [block[0][0], block[0][1]]
                isblock =1 
                for j, blk in enumerate(group_blockboundarypoints): 
                    if i == j: continue
                    else: 
                        result = IsPointInPolygon(point, blk)
                        if result == True :   ## i_th block is in the j_th block 
                            isblock = 0 
                            relation_blocks[j].append(i)
                            break 
                if isblock ==1: 
                    blockboundarypoints.append(block)
                    GroupsBoundary_fulldepthgroove.append(tblocks[i])  

                else: edge_semigroove.append(tblocks[i])
                not_block.append(isblock)
            del(group_blockboundarypoints)
            # print ("2!")
            # check if the group is main groove
            # there should be a node that is pitch length away from the bottom node 
            # sorting and find the node that is pitch length away from the 1st node 
            # Sorted[i] = [N1, N2, (0 = not main groove or 1 = main groove), EL ID, N1[1], N1[2], N1[3], N2[1], N2[2], N2[3], -1]

            image = 0 
            self.SortedGroove =[]
            is_main=[]
            addedgroove = 0 
            for i, grp in enumerate(tblocks): 
                Sorted, grooves =self.SortBoundaryEdgesStartingBottom(grp)
                if grooves == 1: 
                    if Sorted[0][2] == 1:  
                        is_main.append(addedgroove)   ### 'i' is substituted to 'addedgroove' 
                        # print ("is main added", i) 
                    self.SortedGroove.append(Sorted)
                    addedgroove += 1
                    # print ("sorted grooved added", i)
                elif grooves > 1: 
                    for j, std in enumerate(Sorted): 
                        self.SortedGroove.append(std)
                        is_main.append(addedgroove)
                        # print ("\n* j=", j, " adding=", addedgroove, "len sorted=", len(Sorted))
                        # print ("* is main added", addedgroove) 
                        # print ("* srt grv added i=", i, "j=", j, ", i+adding=", addedgroove)
                        if j!=0: relation_blocks.append([])
                        addedgroove += 1

            # print ("************************")
            # print ("is_main=%d, sorted grv=%d"%(len(is_main), len(self.SortedGroove)))
            # print (is_main)
            # print ("3!")

            image = 0 
            UntrimmedGroove = []
            for i, no in enumerate(is_main): 
                edges = self.SortedGroove[no]
                subedges = []
                for j in relation_blocks[no]:
                    subedges.append(self.SortedGroove[j])
                if len(subedges)>0: 
                    edges = self.MergeBoundariesForMainGrooveSearching(edges,subedges )
                UntrimmedGroove.append(edges)
            # print ("4!") 
            
            sortidx = []
            if len(UntrimmedGroove)> 1:
                sorting = [] 
                sortidx = []
                for i, edges in enumerate(UntrimmedGroove): 
                    if i ==0: 
                        sorting.append(edges[0][5])
                        sortidx.append(i)
                        continue 
                    inserted = 0
                    for j in range(i): 
                        if  sorting[j] > edges[0][5]: 
                            sorting.insert(j, edges[i][5])
                            sortidx.insert(j, i)
                            inserted =1 
                            break
                    if inserted == 0: 
                        sorting.append(edges[0][5])
                        sortidx.append(i)
            # print ("5!")
            self.MainGroove=[]
            try: 
                for g, i in enumerate(sortidx): 
                    # print ("Trimming lateral grv", g)
                    Trimmed, g_cent = self.TrimmingLateralGroove(UntrimmedGroove[i], self.SF_fulldepthgroove)
                    self.MainGroove.append(Trimmed)
                    self.GrooveCenter.append(g_cent)
                line = "* The No. of Main Grooves = %d EA \n  "%(len(self.MainGroove))
                if len(self.MainGroove)> 0: 
                    line += "("
                    for k, cn in enumerate(self.GrooveCenter): 
                        line += "%.1f%%"%(cn/self.TreadDesignWidth/2.0*100)
                        if k == len(self.GrooveCenter)-1: line += ")\n"
                        else: line +=", "
                print (line)
            except:
                print ("## Failed to find the main groove position\n")
                if SmoothPattern == 0: 
                    for i in sortidx: 
                        self.MainGroove.append(UntrimmedGroove[i])
            # print ("calculating main groove position is done!")

    def __del__(self): 
        pass 
    def ReadGeneralPattern(self, filename): 
        self.Estart = 10_000_000
        self.Nstart = 10_000_000
        self.pitchscaling = 1.0  
        self.ModelGD = 0.0 
        self.TreadDesignWidth = 0.0

        with open(filename) as PTN: 
            lines = PTN.readlines()
        cmd = ""
        depths=[]
        for line in lines:
            if "**" in line: 
                continue 
            if "*" in line: 
                if "PITCH_SCALING" in line.upper():
                    data = line.split(":")
                    self.pitchscaling = float(data[1].strip())
                elif "GROOVE_DEPTH" in line.upper():
                    data = line.split(":")
                    self.ModelGD = float(data[1].strip()) 
                elif "TREAD_DESIGN_WIDTH" in line.upper():
                    data = line.split(":")
                    self.TreadDesignWidth = float(data[1].strip())
                elif "*NODE" in line.upper() and not "FILE" in line.upper() and not "OUTPUT" in line.upper(): 
                    cmd = 'nd'
                elif "*ELEMENT" in line.upper() and "C3D8" in line.upper(): 
                    cmd = 'c8'
                elif "*ELEMENT" in line.upper() and "C3D6" in line.upper(): 
                    cmd = 'c6'
                else: 
                    cmd = ''
            else:
                if cmd == 'nd': 
                    data = line.split(",")
                    self.Node.append([float(int(data[0].strip()) + self.Nstart),  round(float(data[1].strip()) * self.pitchscaling, 7), \
                                  round(float(data[2].strip()) * self.pitchscaling, 7),  round(float(data[3].strip()) * self.pitchscaling, 7)])

                if cmd == 'c8': 
                    data = line.split(",")
                    # int(data[0].strip()) + self.Estart
                    self.Solid.append([int(data[0].strip()) + self.Estart, \
                        int(data[1].strip()) + self.Nstart, int(data[4].strip()) + self.Nstart, \
                        int(data[3].strip()) + self.Nstart, int(data[2].strip()) + self.Nstart, \
                        int(data[5].strip()) + self.Nstart, int(data[8].strip()) + self.Nstart, \
                        int(data[7].strip()) + self.Nstart, int(data[6].strip()) + self.Nstart, 8])
                if cmd == 'c6': 
                    data = line.split(",")
                    # int(data[0].strip()) + self.Estart
                    self.Solid.append([int(data[0].strip()) + self.Estart, \
                        int(data[1].strip()) + self.Nstart, int(data[3].strip()) + self.Nstart, \
                        int(data[2].strip()) + self.Nstart, int(data[4].strip()) + self.Nstart, \
                        int(data[6].strip()) + self.Nstart, int(data[5].strip()) + self.Nstart, \
                        0, 0, 6])

        if len(self.Node) > 10_0000: 
            print ("\n Too many nodes in the mesh (=%d)"%(len(self.Node)))
            return 0

        tnode = np.array(self.Node)

        self.diameter = np.max(tnode[:,3]) * 2.0

        ix = np.where(tnode[:,3] > self.diameter /2.0 - 0.0005)[0]
        wn = tnode[ix]
        ws = wn[:,2]
        wmin = np.min(ws); wmax=np.max(ws)
        self.PatternWidth = wmax - wmin 
        if self.ModelGD ==0: self.ModelGD = 1.0E-03 
        else: self.ModelGD = self.ModelGD * 0.001
        if self.TreadDesignWidth ==0: 
            self.TreadDesignWidth = round(self.PatternWidth - 20.0E-03, 9)
            print ("*Tread Design Width was set to 'Total width -10mm'") 
        else: 
            self.TreadDesignWidth = round(self.TreadDesignWidth/1000, 9)

        return 1 
                    
    def ReadPtn(self, filename, valuereturn=0):

        with open(filename) as PTN: 
            lines = PTN.readlines()
        cmd = ""
        depths=[]
        for line in lines:
            if "Regenerated Pattern mesh from P3DM" in line: 
                print ("* This mesh was generated by P3DM.")
                print ("  it is already bended to fit a layout \n")
                return 100

            if "**" in line: 
                continue
            elif "*" in line:
                if "*ELEMENT" in line.upper() and "CGAX4" in line.upper() : 
                    print ("* This mesh may be not a pattern mesh.")
                    print ("  This mesh can not be expanded.")
                    return 101 
                if "PROFILE_SCALING" in line.upper():
                    data = line.split(":")
                    self.profilescaling = float(data[1].strip())
                elif "GROOVE_DEPTH" in line.upper():
                    data = line.split(":")
                    self.ModelGD = float(data[1].strip()) 
                elif "HALF_DIAMETER" in line.upper():
                    data = line.split(":")
                    self.diameter = float(data[1].strip()) * 2.0 
                    self.HalfDia =  float(data[1].strip())
                elif "CENTER_ANGLE" in line:
                    data = line.split(":")
                    self.centerangle = float(data[1].strip()) 
                elif "PROFILE_LHS" in line.upper():
                    cmd = 'LHS'
                elif "PROFILE_RHS" in line.upper():
                    cmd = 'RHS'
                elif "PITCH_SCALING" in line.upper():
                    data = line.split(":")
                    self.pitchscaling = float(data[1].strip()) 
                elif "TREAD_DESIGN_WIDTH" in line.upper():
                    data = line.split(":")
                    self.TreadDesignWidth = float(data[1].strip())
                elif "GUIDELINE_TOLERANCE" in line.upper():
                    data = line.split(":")
                    self.guidelinetolerance = float(data[1].strip()) 
                elif "PITCH_DEFINITION_FIRST" in line:
                    cmd = 'P1'
                elif "PITCH_ARRAY_FIRST" in line.upper():
                    data = line.split(",")
                    for dt in data: 
                        if 'EIDSTART' in dt: 
                            self.Estart = int(dt.split("=")[1].strip())
                            self.Estart = 10_000_000
                        if 'NIDSTART' in dt: 
                            self.Nstart = int(dt.split("=")[1].strip())
                            self.Nstart = 10_000_000
                        if 'EIDOFFSET' in dt: 
                            self.Eoffset = int(dt.split("=")[1].strip())
                            self.Eoffset = 10000
                        if 'NIDOFFSET' in dt: 
                            self.Noffset = int(dt.split("=")[1].strip())
                            self.Noffset =10000
                        if 'ANGLE' in dt: self.Pangle = float(dt.split("=")[1].strip())
                        if 'DIRECTION' in dt: self.Direction = dt.split("=")[1].strip()
                    cmd = 'PS'
                elif "HEADING" in line.upper():
                    cmd = 'Heading'
                elif "*NODE" in line.upper() and not "FILE" in line.upper() and not 'OUTPUT' in line.upper() :
                    cmd = "ND"
                elif "ELEMENT" in line.upper() and "B31" in line.upper():
                    cmd = "BM"
                elif "ELEMENT" in line.upper() and "C3D8" in line.upper():
                    cmd = "SD8"
                elif "ELEMENT" in line.upper() and "C3D6" in line.upper():
                    cmd = "SD6"
                elif "*ELSET" in line.upper() and "CENTER" in line.upper():
                    if 'generate' in line.lower(): cmd = 'BCENG'
                    else:
                        cmd ="BCEN"
                elif "ELSET" in line.upper() and "UPFWD" in line.upper():
                    if 'generate' in line.lower(): cmd = 'BUFG'
                    else:   
                        cmd = "BUF"
                elif "ELSET" in line.upper() and "UPAFT" in line.upper():
                    if 'generate' in line.lower(): cmd = 'BUAG'
                    else:   
                        cmd = "BUA"
                elif "ELSET" in line.upper() and "LWAFT" in line.upper():
                    if 'generate' in line.lower(): cmd = 'BLAG'
                    else:
                        cmd = "BLA"
                elif "TREADPTN_NIDSTART_NIDOFFSET_EIDSTART_EIDOFFSET" in line.upper(): 
                    return 0 
                else:
                    cmd =""
            else:
                if cmd =="LHS": 
                    data = line.split(",")
                    PR = round(float(data[0].strip())*self.profilescaling, 6)
                    if PR == 0.0 : PR = 10.0
                    self.leftprofile.append([PR, float(data[1].strip())*self.profilescaling])
                if cmd =="RHS": 
                    data = line.split(",")
                    PR = round(float(data[0].strip())*self.profilescaling, 6)
                    if PR == 0.0 : PR = 10.0
                    self.rightprofile.append([PR, float(data[1].strip())*self.profilescaling])
                if cmd =="P1": 
                    data = line.split(",")
                    for dt in data:
                        self.pitch1.append(dt.strip())
                if cmd =="PS":
                    data = line.split(",")
                    if len(data) == 3: self.pitchsequence.append([int(data[0].strip()), data[1].strip(), int(data[2].strip()) ])
                if cmd =="ND":
                    data = line.split(",")
                    if float(data[3].strip()) > 0: 
                        self.Node.append([float(int(data[0].strip()) + self.Nstart),  round(float(data[1].strip()) * self.pitchscaling, 7), \
                                    round(float(data[2].strip()) * self.pitchscaling, 7),  round(float(data[3].strip()) * self.pitchscaling, 7)])
                    else: 
                        print ("* All the Z values of the nodes should be positive")
                        print ("  This mesh can not be expanded.")
                        return 101 

                    # if self.MaxY < float(data[2].strip()) * self.pitchscaling: self.MaxY = float(data[2].strip()) * self.pitchscaling
                    # if self.MinY > float(data[2].strip()) * self.pitchscaling: self.MinY = float(data[2].strip()) * self.pitchscaling
                if cmd == "BM": 
                    data = line.split(",")
                    if len(data) > 1: 
                        self.Beam.append([int(data[0].strip())+self.Estart, int(data[1].strip())+self.Nstart, int(data[2].strip())+self.Nstart])
                if cmd == "SD6": 
                    data = line.split(",")
                    # int(data[0].strip()) + self.Estart
                    self.Solid.append([int(data[0].strip()) + self.Estart, \
                        int(data[1].strip()) + self.Nstart, int(data[3].strip()) + self.Nstart, \
                        int(data[2].strip()) + self.Nstart, int(data[4].strip()) + self.Nstart, \
                        int(data[6].strip()) + self.Nstart, int(data[5].strip()) + self.Nstart, \
                        0, 0, 6])
                if cmd == "SD8": 
                    data = line.split(",")
                    self.Solid.append([int(data[0].strip()) + self.Estart, \
                        int(data[1].strip()) + self.Nstart, int(data[4].strip()) + self.Nstart, \
                        int(data[3].strip()) + self.Nstart, int(data[2].strip()) + self.Nstart, \
                        int(data[5].strip()) + self.Nstart, int(data[8].strip()) + self.Nstart, \
                        int(data[7].strip()) + self.Nstart, int(data[6].strip()) + self.Nstart, 8])                    
                if cmd == "BCEN":
                    data = line.split(",")
                    for dt in data:
                        if dt.strip() =="": continue 
                        if dt.strip() !="": bid =  int(dt.strip()) + self.Estart
                        for bm in self.Beam: 
                            if bm[0] == bid: 
                                tmp = [bm[0], bm[1], bm[2]]
                                for nd in self.Node:
                                    if bm[1] == nd[0]:
                                        tmp.append([nd[1], nd[2], nd[3]])
                                        break
                                for nd in self.Node:
                                    if bm[2] == nd[0]:
                                        tmp.append([nd[1], nd[2], nd[3]])
                                        break
                                
                                self.Center.append(tmp)
                if cmd == 'BCENG': 
                    data = line.split(",")
                    if len(data) < 3 : continue
                    data[0] = int(data[0].strip())
                    data[1] = int(data[1].strip())
                    data[2] = int(data[2].strip())
                    for dn in range(data[0], data[1]+1, data[2]): 
                        bid = dn + self.Estart 
                        for bm in self.Beam: 
                            if bm[0] == bid: 
                                tmp = [bm[0], bm[1], bm[2]]
                                for nd in self.Node:
                                    if bm[1] == nd[0]:
                                        tmp.append([nd[1], nd[2], nd[3]])
                                        break
                                for nd in self.Node:
                                    if bm[2] == nd[0]:
                                        tmp.append([nd[1], nd[2], nd[3]])
                                        break
                                
                                self.Center.append(tmp)

                if cmd == "BUF":
                    data = line.split(",")
                    for dt in data:
                        if dt.strip() =="": continue 
                        bid =  int(dt.strip()) + self.Estart
                        for bm in self.Beam: 
                            if bm[0] == bid: 
                                tmp = [bm[0], bm[1], bm[2]]
                                for nd in self.Node:
                                    if bm[1] == nd[0]:
                                        tmp.append([nd[1], nd[2], nd[3]])
                                        break
                                for nd in self.Node:
                                    if bm[2] == nd[0]:
                                        tmp.append([nd[1], nd[2], nd[3]])
                                        break
                                
                                self.UpFront.append(tmp)
                if cmd == 'BUFG': 
                    data = line.split(",")
                    if len(data) < 3 : continue
                    data[0] = int(data[0].strip())
                    data[1] = int(data[1].strip())
                    data[2] = int(data[2].strip())
                    for dn in range(data[0], data[1]+1, data[2]): 
                        bid = dn + self.Estart 
                        for bm in self.Beam: 
                            if bm[0] == bid: 
                                tmp = [bm[0], bm[1], bm[2]]
                                for nd in self.Node:
                                    if bm[1] == nd[0]:
                                        tmp.append([nd[1], nd[2], nd[3]])
                                        break
                                for nd in self.Node:
                                    if bm[2] == nd[0]:
                                        tmp.append([nd[1], nd[2], nd[3]])
                                        break
                                
                                self.UpFront.append(tmp)
                if cmd == "BUA":
                    data = line.split(",")
                    for dt in data:
                        if dt.strip() =="": continue 
                        bid =  int(dt.strip()) + self.Estart
                        for bm in self.Beam: 
                            if bm[0] == bid: 
                                tmp = [bm[0], bm[1], bm[2]]
                                for nd in self.Node:
                                    if bm[1] == nd[0]:
                                        tmp.append([nd[1], nd[2], nd[3]])
                                        break
                                for nd in self.Node:
                                    if bm[2] == nd[0]:
                                        tmp.append([nd[1], nd[2], nd[3]])
                                        break
                                
                                self.UpBack.append(tmp)
                if cmd == 'BUAG': 
                    data = line.split(",")
                    if len(data) < 3 : continue
                    data[0] = int(data[0].strip())
                    data[1] = int(data[1].strip())
                    data[2] = int(data[2].strip())
                    for dn in range(data[0], data[1]+1, data[2]): 
                        bid = dn + self.Estart 
                        for bm in self.Beam: 
                            if bm[0] == bid: 
                                tmp = [bm[0], bm[1], bm[2]]
                                for nd in self.Node:
                                    if bm[1] == nd[0]:
                                        tmp.append([nd[1], nd[2], nd[3]])
                                        break
                                for nd in self.Node:
                                    if bm[2] == nd[0]:
                                        tmp.append([nd[1], nd[2], nd[3]])
                                        break
                                
                                self.UpBack.append(tmp)
                if cmd == "BLA":
                    data = line.split(",")
                    
                    for dt in data:
                        if dt.strip() =="": continue 
                        bid =  int(dt.strip()) + self.Estart
                        for bm in self.Beam: 
                            if bm[0] == bid: 
                                tmp = [bm[0], bm[1], bm[2]]
                                for nd in self.Node:
                                    if bm[1] == nd[0]:
                                        tmp.append([nd[1], nd[2], nd[3]])
                                        break
                                for nd in self.Node:
                                    if bm[2] == nd[0]:
                                        tmp.append([nd[1], nd[2], nd[3]])
                                        break
                                
                                self.LowBack.append(tmp)
                if cmd == 'BLAG': 
                    data = line.split(",")
                    if len(data) < 3 : continue
                    data[0] = int(data[0].strip())
                    data[1] = int(data[1].strip())
                    data[2] = int(data[2].strip())
                    for dn in range(data[0], data[1]+1, data[2]): 
                        bid = dn + self.Estart 
                        for bm in self.Beam: 
                            if bm[0] == bid: 
                                tmp = [bm[0], bm[1], bm[2]]
                                for nd in self.Node:
                                    if bm[1] == nd[0]:
                                        tmp.append([nd[1], nd[2], nd[3]])
                                        break
                                for nd in self.Node:
                                    if bm[2] == nd[0]:
                                        tmp.append([nd[1], nd[2], nd[3]])
                                        break
                                
                                self.LowBack.append(tmp)
        
        if len(self.Node) > 10_0000: 
            print ("\n Too many nodes in the mesh (=%d >100,000)"%(len(self.Node)))
            return 0
        if len(self.Solid) == 0: 
            print ("\n No information of pattern mesh\n")
            return 0
        
        if self.TreadDesignWidth == 0: 

            tmp = 0
            sho = 0 
            for i, pf in enumerate(self.leftprofile): 
                if abs(pf[0]) > 0.05 and i < len(self.leftprofile)-1: 
                    self.TreadDesignWidth += pf[1]
                    sho = 1
                else: 
                    tmp = pf[1]
                    break 
            if sho == 1: self.TreadDesignWidth -= tmp/3.0 *2
            tmp = 0
            sho = 0 
            for i, pf in enumerate(self.rightprofile): 
                if abs(pf[0]) > 0.05 and i < len(self.rightprofile)-1: 
                    self.TreadDesignWidth += pf[1]
                    sho = 1
                else: 
                    tmp = pf[1]
                    break 
            if sho==1: self.TreadDesignWidth -= tmp/3.0 *2

            self.TreadDesignWidth = round(self.TreadDesignWidth, 9)
        else: 
            self.TreadDesignWidth = round(self.TreadDesignWidth/1000, 9)
            
        
        # self.PatternWidth 
        tnode = np.array(self.Node)
        zs = tnode[:,3]
        self.diameter = np.max(zs) * 2.0

        # self.diameter = round(self.diameter * self.pitchscaling, 6)
        # self.guidelinetolerance = round(self.guidelinetolerance * self.pitchscaling, 6)
        ix = np.where(tnode[:,3] > self.diameter /2.0 - 0.0005)[0]
        wn = tnode[ix]
        ws = wn[:,2]
        wmin = np.min(ws); wmax=np.max(ws)
        self.PatternWidth = wmax - wmin 
        if self.ModelGD ==0: self.ModelGD = 1.0E-03 
        else: self.ModelGD = self.ModelGD * 0.001

        if self.TreadDesignWidth == 0: 
            self.TreadDesignWidth = self.PatternWidth  - 10.0E-03 
            print ("*Design Width was set to 'Total width -10mm'")

        return 1 

    def Pitchlength(self): 
        pmin = 10000.0
        pmax = -10000.0
        x = int(self.GlobalXY/10)
        y = int(self.GlobalXY%10)
        for bm in self.Center: 
            if pmin > bm[3][y-1]: pmin = bm[3][y-1]
            if pmin > bm[4][y-1]: pmin = bm[4][y-1]
            if pmax < bm[3][y-1]: pmax = bm[3][y-1]
            if pmax < bm[4][y-1]: pmax = bm[4][y-1]
        return (pmax-pmin)
        # print ("Pitch length =%.3fmm"%(self.pitchlength*1000))
    def Expansion(self, layoutOD, layoutTDW, layoutTW, layoutGD, user_pitch_no=0, t3dm=0, shoulder="R"):
        print ("\n############################################")
        print ("## Scaling pattern ")
        print ("############################################")

        ## SCALING THE MESH with PL, TW, GD  ##########################################################################
        # TIME_START=time.time()
        self.TargetOD = layoutOD
        self.TargetTDW = layoutTDW
        self.TargetTW = layoutTW
        self.TargetGD = layoutGD 

        # print ("CHECKING NODE Number")
        # print (len(self.npn), ", initial", len(self.Node_Origin))
        if shoulder =="R":
            self.npn, NodeOrigin= self.PatternScaling(ModelGD=self.ModelGD, TargetGD=self.TargetGD, ModelPL=self.pitchlength, NoPitch=user_pitch_no, \
                ModelTDW=self.TreadDesignWidth, TargetTDW=self.TargetTDW, TargetTW=self.TargetTW, TargetOD=self.TargetOD, ModelOD=self.diameter, t3dm=t3dm, orgn=self.Node_Origin, surf_btm=self.freebottom)
        else:
            self.npn, NodeOrigin = self.PatternScalingSquare(ModelGD=self.ModelGD, TargetGD=self.TargetGD, ModelPL=self.pitchlength, NoPitch=user_pitch_no, \
                ModelTDW=self.TreadDesignWidth, TargetTDW=self.TargetTDW, TargetOD=self.TargetOD, ModelOD=self.diameter, t3dm=t3dm, orgn=self.Node_Origin, surf_btm=self.freebottom)
        # print (len(self.npn), ", initial", len(self.Node_Origin))

        node_simplescaled=[]
        for nd in self.npn:
            node_simplescaled.append([nd[0], nd[1], nd[2], nd[3]])
        node_simplescaled = np.array(node_simplescaled)

        # TIME_END=time.time()

        ####################################################################################################################
        ## groove nodes repositioning
        if t3dm ==0: 
            self.PTN_AllFreeSurface = np.vstack((self.freetop, self.freebottom,  self.totalsurfaces))

            for i, nd in enumerate(self.npn): 
                self.npn[i][1] = round(self.npn[i][1], 8)
                self.npn[i][2] = round(self.npn[i][2], 8)
                self.npn[i][3] = round(self.npn[i][3], 8)

            ######################################################################
            surfaces = np.array(self.totalsurfaces)    ## top and bottom surfaces are removed 
            Edges = AllEdgesInSurface(surfaces, self.npn)

            i = 0 # self.surf_pitch_up, self.surf_pitch_down
            while i < len(self.totalsurfaces): 
                for sf in self.surf_pitch_up: 
                    if sf[0] == self.totalsurfaces[i][0] and sf[1] == self.totalsurfaces[i][1]: 
                        self.totalsurfaces = np.delete( self.totalsurfaces, i, 0)
                        i -= 1
                        break 
                i += 1
            i = 0 # self.surf_pitch_up, self.surf_pitch_down
            while i < len(self.totalsurfaces): 
                for sf in self.surf_pitch_down: 
                    if sf[0] == self.totalsurfaces[i][0] and sf[1] ==  self.totalsurfaces[i][1]: 
                        self.totalsurfaces = np.delete( self.totalsurfaces, i, 0)
                        i -= 1
                        break 
                i += 1
                
            if len(self.SF_subgroove) > 0:         surf_allgroovebtm = np.vstack((self.SF_fulldepthgroove, self.SF_subgroove))
            else:                             surf_allgroovebtm = self.SF_fulldepthgroove

            if self.shoulderType =="S": 
                edge_top_surface = self.EliminateShoulderLugEdgeInTopEdges(self.edge_top_surface, self.npn)

                if len(self.MainGroove) > 0: 
                    kerfedges, grooveedges, pvnode, cnode, fnode=self.GrooveSideNodeRepositioningfromTop(TopEdges=edge_top_surface, orgn=NodeOrigin, alledges=Edges,\
                        surfaces=surfaces, maingroovebottomedge=self.SortedGroove, groovebottomsurf=surf_allgroovebtm, maingroovebottomsurf=self.SF_fulldepthgroove, \
                        surf_mainside=self.SF_fulldepthgrooveside, surf_subside=self.SF_subgrooveside, surf_kerfside=self.KerfsideSurface)
                else: 
                    grooveedges, kerfedges = self.Groove_kerf_edges_in_top_surface(top_edges=edge_top_surface, surf_main_side=self.SF_fulldepthgrooveside, surf_sub_side=self.SF_subgrooveside, surf_kerf_side=self.KerfsideSurface)
            else:
                if len(self.MainGroove) > 0: 
                    kerfedges, grooveedges, pvnode, cnode, fnode=self.GrooveSideNodeRepositioningfromTop(TopEdges=self.edge_top_surface, orgn=NodeOrigin, alledges=Edges,\
                        surfaces=surfaces, maingroovebottomedge=self.SortedGroove, groovebottomsurf=surf_allgroovebtm, maingroovebottomsurf=self.SF_fulldepthgroove, \
                        surf_mainside=self.SF_fulldepthgrooveside, surf_subside=self.SF_subgrooveside, surf_kerfside=self.KerfsideSurface)
                else: 
                    grooveedges, kerfedges = self.Groove_kerf_edges_in_top_surface(top_edges=self.edge_top_surface, surf_main_side=self.SF_fulldepthgrooveside, surf_sub_side=self.SF_subgrooveside, surf_kerf_side=self.KerfsideSurface)

            for psf in self.SF_pitchside:   ## delete pitch side surface to simplify the semi-groove bottom edge 
                i =0
                while i < len(surfaces): 
                    if psf[0] == surfaces[i][0] and psf[1] == surfaces[i][1]: 
                        surfaces = np.delete(surfaces, i, axis=0)
                        break 
                    i += 1

            i = 0
            while i <len(surfaces):    ## delete 2nd face surface of each element to simplify the semi-groove bottom edge 
                if surfaces[i][1] ==2: 
                    surfaces = np.delete(surfaces, i, axis=0)
                    i -= 1
                i+= 1

            Edge_subgroove = self.SurfaceBoundary(self.SF_subgroove)   ## sub groove edges 

            Edges = AllEdgesInSurface(surfaces, self.npn)              ## all edges on all surface whose top and pitch side surfaces are elimited 
            if len(self.MainGroove) > 0: 
                before, translated = self.GrooveSideNodeRepositioningOnSubgroove(Subgrooveedges=Edge_subgroove,  orgn_node=node_simplescaled, alledges=Edges, \
                    surfaces=surfaces, maingroovebottomedge=self.MainGroove, maingrooveside=self.SF_fulldepthgrooveside, modelnodes=NodeOrigin)
                ################################################################################
                ## Translation of the nodes on bottom surface 
                ################################################################################
                self.npn = self.ShiftNodesOnGrooveBottom(edge_groovebottom=self.Boundary_fulldepthgroove, orgnode=NodeOrigin, currentnode=self.npn)
                
            if len(kerfedges) > 0: 
                self.KeepKerfGaugeConstant(kerfedges=kerfedges, groovebottomsurf=surf_allgroovebtm, surfaces=surfaces, alledges=Edges, orgn_node=NodeOrigin, debug=0, surface_kerf=self.KerfsideSurface)
        
        
        self.PTN_AllFreeSurface = np.vstack((self.freetop, self.freebottom,  self.totalsurfaces))
        print ("** Pattern was scaled !! ")

        return self.NoPitch
    

    ## Method developed in September 2020 
    def Top_Bottom_FreeSurfacesFromAllSurfaces_01(self, allSurface, npn, radius=0.0, margin=1.0E-03): 

        # t0 = time.time()

        nodes =[]
        for i, sf in enumerate(allSurface):
            tnode = sf[7:]
            nodes.append(np.sort(tnode))
        nodes = np.array(nodes)
        filter_heightmargin =radius - margin ## 1mm from ht. 
        filter_heightmargin_top =radius - margin/2.0
        
        # print ("ht margin for top=%.3f"%(filter_heightmargin_top*1000))
        # print ("ht margin for btm=%.3f"%(filter_heightmargin*1000))
        # print ("Radius =%.3f"%(radius*1000))

        free = []
        bottom = []
        topfree = []
        for i, sf in enumerate(allSurface): 
            # ifree =1
            # print (" %d, %d, %d"%(sf[0]-10**7, sf[1], sf[3]))
            m = 0 
            if sf[3] != 99: 
                if sf[2] == 3:
                    ind1 = np.where(nodes[:, 3] == nodes[i][3])[0]  ## because nodes[i][0] == 0 
                    ind2 = np.where(nodes[:, 1] == nodes[i][1])[0]
                    ind3 = np.where(nodes[:, 2] == nodes[i][2])[0]
                    ind = np.intersect1d(ind1, ind2, assume_unique=True)
                    ind = np.intersect1d(ind,  ind3, assume_unique=True) 
                    m = 3                
                else: 
                    ind1 = np.where(nodes[:, 0] == nodes[i][0])[0]
                    ind2 = np.where(nodes[:, 1] == nodes[i][1])[0]
                    ind3 = np.where(nodes[:, 2] == nodes[i][2])[0]
                    ind4 = np.where(nodes[:, 3] == nodes[i][3])[0]
                    ind = np.intersect1d(ind1, ind2, assume_unique=True)
                    ind = np.intersect1d(ind,  ind3, assume_unique=True) 
                    ind = np.intersect1d(ind,  ind4, assume_unique=True) 

                if len(ind) ==2: 
                    # allSurface[i][3] = 99  ## 99: not free surface 
                    allSurface[ind[0]][3] = 99
                    allSurface[ind[1]][3] = 99
                #     ifree = 0
                # if ifree ==1:  ## among free surfaces 
                elif len(ind) ==1: 
                    ind= ind[0]
                    idx1 = np.where(npn[:,0]==nodes[ind][m])[0][0]
                    idx2 = np.where(npn[:,0]==nodes[ind][1])[0][0]
                    idx3 = np.where(npn[:,0]==nodes[ind][2])[0][0]
                    n1 = npn[idx1]; n2=npn[idx2]; n3 = npn[idx3]

                    if allSurface[i][1] == 1 and n1[3] < filter_heightmargin and n2[3] < filter_heightmargin and n3[3] < filter_heightmargin:  ## bottom surface : face = 1
                        allSurface[i][3] = 199  ## bottom surface 
                        bottom.append(sf)
                    elif allSurface[i][1] == 2 and n1[3] > filter_heightmargin_top and n2[3] > filter_heightmargin_top and n3[3] > filter_heightmargin_top:  ## top surface : face = 2
                        allSurface[i][3] = 101  ## top surface 
                        topfree.append(sf)
                    else: #if ht < filter_heightmargin :
                        allSurface[i][3] = 100  ## free surface 
                        free.append(sf)
        
        # print (" btm surf %d, top=%d, free=%d"%(len(bottom), len(topfree), len(free)))
        # t1 = time.time(); print ("** Top/BTM %.3f "%(t1-t0)); t0 = time.time()
        ## verifying the searching bottom surface #############

        bnd_btm = self.SurfaceBoundary(bottom)
        bnd = np.array(bnd_btm)
        self.Edge_bottomSurface = bnd_btm 

        # print (" the No. of bottom edge =%d"%(len(bnd_btm)))

        bd1 = bnd[0]
        bnd = np.delete(bnd, 0, axis=0)
        # print ("*DEL ", bd1)
        i = 0 
        groups=[]
        group=[bd1]
        added = 0 
        while i < len(bnd): 
            ix = np.where(bnd[:,0]==bd1[1])[0]
            if len(ix) > 0: 
                group.append(bnd[ix[0]])
                # print ("DEL ", bnd[ix[0]])
                bd1 = bnd[ix[0]]

                bnd = np.delete(bnd, ix[0], axis=0)
            else: 
                groups.append(group)
                group=[]
                if len(bnd)> 0: 
                    group=[bnd[0]]
                    bd1 = bnd[0]
                    # print ("*DEL ", bd1)
                    bnd = np.delete(bnd, 0, axis=0)
                    
        if len(group) > 0: 
            groups.append(group)
            group = []

        # t1 = time.time(); print ("** BTM %.3f"%(t1-t0)); t0 = time.time()
        if len(groups) > 1: 
            mg = len(groups[0])
            ibt=0 
            for i, gr in enumerate(groups): 
                if len(gr) > mg: 
                    mg = len(gr)
                    ibt = i 
            
            btm = groups[ibt] 
            btmg = []
            for bt in btm: 
                ix = np.where(npn[:,0] == bt[0])[0][0]; n1 = npn[ix]
                ix = np.where(npn[:,0] == bt[1])[0][0]; n2 = npn[ix]
                if n1[2] != n2[2]: 
                    if n1[2] > n2[2]: btmg.append([bt[0], bt[1], bt[2], bt[3], n2, n1])
                    else:             btmg.append([bt[0], bt[1], bt[2], bt[3], n1, n2]) 
            
            i = 0 
            while i < len(bottom): 
                cn = [0, bottom[i][4], bottom[i][5], bottom[i][6]]
                ix = np.where(npn[:,0] == bottom[i][7])[0][0]; n1 = npn[ix]
                ix = np.where(npn[:,0] == bottom[i][9])[0][0]; n3 = npn[ix]
                f = 0 
                for bt in btmg: 
                    d, P = DistanceFromLineToNode2D(cn, [bt[4], bt[5]], xy=23)
                    if d <= 0.2E-03 and bt[4][2] <= P[2] and P[2] <= bt[5][2] : 
                        f = 1
                        break 
                    if bt[4][2] <= n1[2] and n1[2] <= bt[5][2] and abs(bt[5][3]-bt[4][3]) > abs(bt[5][3]-n1[3]): 
                        f = 1
                        break 
                    if bt[4][2] <= n3[2] and n3[2] <= bt[5][2] and abs(bt[5][3]-bt[4][3]) > abs(bt[5][3]-n3[3]): 
                        f = 1
                        break 

                if f == 0: 
                    free.append(bottom[i])
                    # print ("del", bottom[i][0]-10**7, "f=", bottom[i][1], "dist=%.3f"%(d*1000))
                    del(bottom[i])
                    
                    i -= 1
                i += 1 

        # t1 = time.time(); print ("** FN %.3f"%(t1-t0)); t0 = time.time()
        # t2 = time.time()
        # print ("#####################################")
        # print (" TIME TO SEARCH FREE SURFACE =%.2f"%(t2-t1))
        # print ("#####################################")
        
        return np.array(topfree), np.array(bottom), np.array(free), allSurface 

    ##        Developed in April 2020 
    def Top_Bottom_FreeSurfacesFromAllSurfaces(self, allSurface, npn, radius=0.0, margin=1.0E-03): 
        nodes =[]
        for i, sf in enumerate(allSurface):
            tnode = sf[7:]
            nodes.append(np.sort(tnode))
        nodes = np.array(nodes)
        filter_heightmargin =radius - margin ## 1mm from ht. 
        filter_heightmargin_top =radius - margin/2.0
        free = []
        bottom = []
        topfree = []
        # t1 = time.time()
        for i, sf in enumerate(allSurface): 
            
            ifree =1
            m = 0 
            if sf[2] == 3:
                ind1 = np.where(nodes[:, 3] == nodes[i][3])[0]  ## because nodes[i][0] == 0 
                ind2 = np.where(nodes[:, 1] == nodes[i][1])[0]
                ind3 = np.where(nodes[:, 2] == nodes[i][2])[0]
                ind = np.intersect1d(ind1, ind2)
                ind = np.intersect1d(ind,  ind3) 
                m = 3                
            else: 
                ind1 = np.where(nodes[:, 0] == nodes[i][0])[0]
                ind2 = np.where(nodes[:, 1] == nodes[i][1])[0]
                ind3 = np.where(nodes[:, 2] == nodes[i][2])[0]
                ind4 = np.where(nodes[:, 3] == nodes[i][3])[0]
                ind = np.intersect1d(ind1, ind2)
                ind = np.intersect1d(ind,  ind3) 
                ind = np.intersect1d(ind,  ind4) 

            if len(ind) ==2: 
                allSurface[i][3] = 99  ## 99: not free surface 
                ifree = 0
            if ifree ==1:  ## among free surfaces 
                ind= ind[0]
                idx1 = np.where(npn[:,0]==nodes[ind][m])[0][0]
                idx2 = np.where(npn[:,0]==nodes[ind][1])[0][0]
                idx3 = np.where(npn[:,0]==nodes[ind][2])[0][0]
                n1 = npn[idx1]; n2=npn[idx2]; n3 = npn[idx3]

                if allSurface[i][1] == 1 and n1[3] < filter_heightmargin and n2[3] < filter_heightmargin and n3[3] < filter_heightmargin:  ## bottom surface : face = 1
                    allSurface[i][3] = 199  ## bottom surface 
                    bottom.append(sf)
                elif allSurface[i][1] == 2 and n1[3] > filter_heightmargin_top and n2[3] > filter_heightmargin_top and n3[3] > filter_heightmargin_top:  ## top surface : face = 2
                    allSurface[i][3] = 101  ## top surface 
                    topfree.append(sf)
                else: #if ht < filter_heightmargin :
                    allSurface[i][3] = 100  ## free surface 
                    free.append(sf)
            else: 
                continue
        # t2 = time.time()
        # print ("#####################################")
        # print (" TIME TO SEARCH FREE SURFACE =%.2f"%(t2-t1))
        # print ("#####################################")
        return np.array(topfree), np.array(bottom), np.array(free), allSurface 
    def pitch_updown_surface(self, free, bottom, method=3, debug=0, npn=[], halfOD = 0.0, shoulder="R"):
        ## surface = [El_id, Face_Id(1~6), type(3 or 4), layer, center X, y, z, n1, n2, n3, n4]
        free = np.array(free)

        pitchup=[]
        pitchdown=[]
        margin_pitchlength = 0.1E-03
        freesurf2del=[]
        
        # t0 = time.time()
        for cn in free: 
            ix1 = np.where(free[:,4] == cn[4])[0]
            ix2 = np.where(free[:,5] == cn[5])[0]
            ix3 = np.where(free[:,6] == cn[6])[0]
            ix = np.intersect1d(ix1, ix2)
            ix = np.intersect1d(ix,  ix3)
            if len(ix) ==2 : 
                for i in ix: 
                    if cn[7] != free[i][8] and cn[0] != free[i][0] and cn[9] == free[i][10] and cn[10] == free[i][9]: 
                        print ("#############################################")
                        print ("  ## EL(%5d, %5d) Bottom nodes are open."%(cn[0]-10**7, free[i][0]-10**7))
                        print ("  ## EL: %5d, F%d, %5d, %5d, %5d, %5d"%(cn[0]-10**7, cn[1], cn[7]-10**7, cn[8]-10**7, cn[9]-10**7, cn[10]-10**7))
                        print ("  ## EL: %5d, F%d, %5d, %5d, %5d, %5d"%(free[i][0]-10**7, free[i][1], free[i][7]-10**7, free[i][8]-10**7, free[i][9]-10**7, free[i][10]-10**7))
                        if cn[7] != free[i][8]: 
                            this = free[i][8]; to = cn[7]
                            up = cn[10]
                        else: 
                            this = free[i][7]; to = cn[8]
                            up  = cn[9]

                        ixd = np.where(free[:,7:9] == this)[0]
                        ixu = np.where(free[:,9:] == up)[0]
                        ix = np.intersect1d(ixd, ixu)
                        if len(ix) == 2: 
                            x1 = ix[0]; x2 = ix[1]
                            if free[x1][9] == free[x2][10] or free[x1][10] == free[x2][9]: 
                                freesurf2del.append(free[x1])
                                freesurf2del.append(free[x2])


                        ixd = np.where(free[:,7:9] == to)[0]
                        ixu = np.where(free[:,9:] == up)[0]
                        ix = np.intersect1d(ixd, ixu)
                        if len(ix) == 2: 
                            x1 = ix[0]; x2 = ix[1]
                            if free[x1][9] == free[x2][10] or free[x1][10] == free[x2][9]: 
                                freesurf2del.append(free[x1])
                                freesurf2del.append(free[x2])

                        for k in range(1, 5): 
                            ix = np.where(self.nps[:, k] == this)[0]
                            if len(ix) > 0: 
                                for x in ix: 
                                    self.nps[x][k] = to 
                                    print ("  >> ND %d on EL(%d) is replaced to %d"%(this-10**7, self.nps[x][0]-10**7, to-10**7))
            elif len(ix) > 2: 
                print ("#############################################")
                print ("## The surfaces of the elements are too close: ")
                cnt = 0 
                for i in ix: 
                    cnt += 1 
                    print ("  %5d,%5d : x=(%7.3f-%7.3f=%7.3f ), y=(%7.3f-%7.3f=%7.3f), z=(%7.3f-%7.3f=%7.3f)"%(cn[0]-10**7, free[i][0]-10**6, \
                        cn[4]*1000, free[i][4]*1000, (cn[4]-free[i][4])*1000, cn[5]*1000, free[i][5]*1000, (cn[5]-free[i][5])*1000, cn[6]*1000, free[i][6]*1000, (cn[6]-free[i][6])*1000 ))
                    if cnt > 10: 
                        print ("## Stopped to print.")
                        break 
            
            if method ==0: 
                if cn[2] ==4 and (cn[1] != 1 and cn[1] != 2): 
                    ix = np.where(self.solidnodes[:,0] == cn[7])[0][0]; n1 = self.solidnodes[ix]
                    ix00 = np.where(self.solidnodes[:,1] > n1[1] + self.pitchlength - margin_pitchlength)[0]
                    ix01 = np.where(self.solidnodes[:,1] < n1[1] + self.pitchlength + margin_pitchlength)[0]
                    ixx = np.intersect1d(ix00, ix01)
                    ix00 = np.where(self.solidnodes[:,2] > n1[2] - margin_pitchlength)[0]
                    ix01 = np.where(self.solidnodes[:,2] < n1[2] + margin_pitchlength)[0]
                    ixy = np.intersect1d(ix00, ix01)
                    ix00 = np.where(self.solidnodes[:,3] > n1[3] - margin_pitchlength)[0]
                    ix01 = np.where(self.solidnodes[:,3] < n1[3] + margin_pitchlength)[0]
                    ixz = np.intersect1d(ix00, ix01)
                    ix1 = np.intersect1d(ixx, ixy)
                    ix1 = np.intersect1d(ix1, ixz)

                    ix = np.where(self.solidnodes[:,0] == cn[8])[0][0]; n2 = self.npn[ix]
                    ix00 = np.where(self.solidnodes[:,1] > n2[1] + self.pitchlength - margin_pitchlength)[0]
                    ix01 = np.where(self.solidnodes[:,1] < n2[1] + self.pitchlength + margin_pitchlength)[0]
                    ixx = np.intersect1d(ix00, ix01)
                    ix00 = np.where(self.solidnodes[:,2] > n2[2] - margin_pitchlength)[0]
                    ix01 = np.where(self.solidnodes[:,2] < n2[2] + margin_pitchlength)[0]
                    ixy = np.intersect1d(ix00, ix01)
                    ix00 = np.where(self.solidnodes[:,3] > n2[3] - margin_pitchlength)[0]
                    ix01 = np.where(self.solidnodes[:,3] < n2[3] + margin_pitchlength)[0]
                    ixz = np.intersect1d(ix00, ix01)
                    ix2 = np.intersect1d(ixx, ixy)
                    ix2 = np.intersect1d(ix2, ixz)

                    ix = np.where(self.solidnodes[:,0] == cn[9])[0][0]; n3 = self.npn[ix]
                    ix00 = np.where(self.solidnodes[:,1] > n3[1] + self.pitchlength - margin_pitchlength)[0]
                    ix01 = np.where(self.solidnodes[:,1] < n3[1] + self.pitchlength + margin_pitchlength)[0]
                    ixx = np.intersect1d(ix00, ix01)
                    ix00 = np.where(self.solidnodes[:,2] > n3[2] - margin_pitchlength)[0]
                    ix01 = np.where(self.solidnodes[:,2] < n3[2] + margin_pitchlength)[0]
                    ixy = np.intersect1d(ix00, ix01)
                    ix00 = np.where(self.solidnodes[:,3] > n3[3] - margin_pitchlength)[0]
                    ix01 = np.where(self.solidnodes[:,3] < n3[3] + margin_pitchlength)[0]
                    ixz = np.intersect1d(ix00, ix01)
                    ix3 = np.intersect1d(ixx, ixy)
                    ix3 = np.intersect1d(ix3, ixz)

                    ix = np.where(self.solidnodes[:,0] == cn[10])[0][0]; n4 = self.npn[ix]
                    ix00 = np.where(self.solidnodes[:,1] > n4[1] + self.pitchlength - margin_pitchlength)[0]
                    ix01 = np.where(self.solidnodes[:,1] < n4[1] + self.pitchlength + margin_pitchlength)[0]
                    ixx = np.intersect1d(ix00, ix01)
                    ix00 = np.where(self.solidnodes[:,2] > n4[2] - margin_pitchlength)[0]
                    ix01 = np.where(self.solidnodes[:,2] < n4[2] + margin_pitchlength)[0]
                    ixy = np.intersect1d(ix00, ix01)
                    ix00 = np.where(self.solidnodes[:,3] > n4[3] - margin_pitchlength)[0]
                    ix01 = np.where(self.solidnodes[:,3] < n4[3] + margin_pitchlength)[0]
                    ixz = np.intersect1d(ix00, ix01)
                    ix4 = np.intersect1d(ixx, ixy)
                    ix4 = np.intersect1d(ix4, ixz)
                    
                    if len(ix1) ==1 and len(ix2) == 1 and len(ix3) ==1 and len(ix4) == 1: 
                        pn1 = n1; pn2=n2; pn3=n3; pn4=n4
                        n1 = self.solidnodes[ix1[0]]
                        n2 = self.solidnodes[ix2[0]]
                        n3 = self.solidnodes[ix3[0]]
                        n4 = self.solidnodes[ix4[0]]

                        iy1 = np.where(free[:,7:] == n1[0])[0]
                        iy2 = np.where(free[:,7:] == n2[0])[0]
                        iy3 = np.where(free[:,7:] == n3[0])[0]
                        iy4 = np.where(free[:,7:] == n4[0])[0]

                        

                        tiy = np.intersect1d(iy1, iy2)
                        tiy = np.intersect1d(tiy, iy3)
                        tiy = np.intersect1d(tiy, iy4)
                        if len(tiy) ==1: 
                            
                            pitchup.append(free[tiy[0]])
                            pitchdown.append(cn)
                        else: 
                            print ("Surfaces found %d"%(len(tiy)))
                            for idx in tiy: 
                                print ("### SURFACE : %4d, %4d, %4d, %4d, %4d"%(free[idx][0]-10**7, free[idx][7]-10**7, free[idx][8]-10**7, free[idx][9]-10**7, free[idx][10]-10**7))
                                dx  = np.where(self.solidnodes[:,0]==free[idx][7])[0][0]; n1 = self.solidnodes[dx]
                                dx  = np.where(self.solidnodes[:,0]==free[idx][8])[0][0]; n2 = self.solidnodes[dx]
                                dx  = np.where(self.solidnodes[:,0]==free[idx][9])[0][0]; n3 = self.solidnodes[dx]
                                dx  = np.where(self.solidnodes[:,0]==free[idx][10])[0][0]; n4 = self.solidnodes[dx]

                                print ("1: %d, %7.3f, %7.3f, %7.3f"%(pn1[0], pn1[1]*1000, pn1[2]*1000, pn1[3]*1000))
                                for idx in ix1: 
                                    n1 = self.solidnodes[idx]
                                    print ("   %d, %7.3f, %7.3f, %7.3f Pitch length=%7.3f, Distance=%7.3f, Diff=%7.3f\n"%(n1[0], n1[1]*1000, n1[2]*1000, n1[3]*1000, self.pitchlength*1000, (n1[1]-pn1[1])*1000, ((n1[1]-pn1[1]) - self.pitchlength)*1000))

                                print ("2: %d, %7.3f, %7.3f, %7.3f"%(pn2[0], pn2[1]*1000, pn2[2]*1000, pn2[3]*1000))
                                for idx in ix2: 
                                    n2 = self.solidnodes[idx]
                                    print ("   %d, %7.3f, %7.3f, %7.3f Pitch length=%7.3f, Distance=%7.3f, Diff=%7.3f\n"%(n2[0], n2[1]*1000, n2[2]*1000, n2[3]*1000, self.pitchlength*1000, (n2[1]-pn2[1])*1000, ((n2[1]-pn2[1]) - self.pitchlength)*1000))

                                print ("3: %d, %7.3f, %7.3f, %7.3f"%(pn3[0], pn3[1]*1000, pn3[2]*1000, pn3[3]*1000))
                                for idx in ix3: 
                                    n3 = self.solidnodes[idx]
                                    print ("   %d, %7.3f, %7.3f, %7.3f Pitch length=%7.3f, Distance=%7.3f, Diff=%7.3f\n"%(n3[0], n3[1]*1000, n3[2]*1000, n3[3]*1000, self.pitchlength*1000, (n3[1]-pn3[1])*1000, ((n3[1]-pn3[1]) - self.pitchlength)*1000))

                                print ("4: %d, %7.3f, %7.3f, %7.3f"%(pn4[0], pn4[1]*1000, pn4[2]*1000, pn4[3]*1000))
                                for idx in ix4: 
                                    n4 = self.solidnodes[idx]
                                    print ("   %d, %7.3f, %7.3f, %7.3f Pitch length=%7.3f, Distance=%7.3f, Diff=%7.3f\n"%(n4[0], n4[1]*1000, n4[2]*1000, n4[3]*1000, self.pitchlength*1000, (n4[1]-pn4[1])*1000, ((n4[1]-pn4[1]) - self.pitchlength)*1000))
                    else: 
                        if len(ix1) > 1 or len(ix2) > 1 or len(ix3) > 1 or len(ix4) > 1: 
                            print ("  nodes: %d, %d, %d, %d"%(len(ix1), len(ix2), len(ix3), len(ix4) ))
                            pn1 = n1; pn2=n2; pn3=n3; pn4=n4
                            if len(ix1) > 1: 
                                print ("*1* %d, %7.3f, %7.3f, %7.3f (target x=%7.3f)"%(pn1[0], pn1[1]*1000, pn1[2]*1000, pn1[3]*1000, (pn1[1]+self.pitchlength)*1000))
                                for idx in ix1: 
                                    n1 = self.solidnodes[idx]
                                    print ("   %d, %7.3f, %7.3f, %7.3f Pitch length=%7.3f, Distance=%7.3f, Diff=%7.3f"%(n1[0], n1[1]*1000, n1[2]*1000, n1[3]*1000, self.pitchlength*1000, (n1[1]-pn1[1])*1000, ((n1[1]-pn1[1]) - self.pitchlength)*1000))
                            if len(ix2) > 1: 
                                print ("*2* %d, %7.3f, %7.3f, %7.3f (target x=%7.3f)"%(pn2[0], pn2[1]*1000, pn2[2]*1000, pn2[3]*1000, (pn2[1]+self.pitchlength)*1000))
                                for idx in ix2: 
                                    n2 = self.solidnodes[idx]
                                    print ("   %d, %7.3f, %7.3f, %7.3f Pitch length=%7.3f, Distance=%7.3f, Diff=%7.3f"%(n2[0], n2[1]*1000, n2[2]*1000, n2[3]*1000, self.pitchlength*1000, (n2[1]-pn2[1])*1000, ((n2[1]-pn2[1]) - self.pitchlength)*1000))

                            if len(ix3) > 1: 
                                print ("*3* %d, %7.3f, %7.3f, %7.3f (target x=%7.3f)"%(pn3[0], pn3[1]*1000, pn3[2]*1000, pn3[3]*1000, (pn3[1]+self.pitchlength)*1000))
                                for idx in ix3: 
                                    n3 = self.solidnodes[idx]
                                    print ("   %d, %7.3f, %7.3f, %7.3f Pitch length=%7.3f, Distance=%7.3f, Diff=%7.3f"%(n3[0], n3[1]*1000, n3[2]*1000, n3[3]*1000, self.pitchlength*1000, (n3[1]-pn3[1])*1000, ((n3[1]-pn3[1]) - self.pitchlength)*1000))
                            if len(ix4) > 1: 
                                print ("*4* %d, %7.3f, %7.3f, %7.3f (target x=%7.3f)"%(pn4[0], pn4[1]*1000, pn4[2]*1000, pn4[3]*1000, (pn4[1]+self.pitchlength)*1000))
                                for idx in ix4: 
                                    n4 = self.solidnodes[idx]
                                    print ("   %d, %7.3f, %7.3f, %7.3f Pitch length=%7.3f, Distance=%7.3f, Diff=%7.3f"%(n4[0], n4[1]*1000, n4[2]*1000, n4[3]*1000, self.pitchlength*1000, (n4[1]-pn4[1])*1000, ((n4[1]-pn4[1]) - self.pitchlength)*1000))

            elif method ==1:  
            
                ix00 = np.where(free[:,4] > cn[4] + self.pitchlength - margin_pitchlength)[0]
                ix01 = np.where(free[:,4] < cn[4] + self.pitchlength + margin_pitchlength)[0]
                ix1 = np.intersect1d(ix00, ix01)
                if len(ix1) > 0: 

                    ix00 = np.where(free[:,5] > cn[5]-margin_pitchlength)[0]
                    ix01 = np.where(free[:,5] < cn[5]+margin_pitchlength)[0]
                    ix2 = np.intersect1d(ix00, ix01)

                    ix00 = np.where(free[:,6] > cn[6]-margin_pitchlength)[0]
                    ix01 = np.where(free[:,6] < cn[6]+margin_pitchlength)[0]
                    ix3 = np.intersect1d(ix00, ix01)

                    ix = np.intersect1d(ix1, ix2)
                    ix = np.intersect1d(ix,  ix3)
                    if len(ix) == 1 : 
                        pitchup.append(free[ix[0]])
                        pitchdown.append(cn)
                    elif len(ix) > 1: 
                        nds = []
                        idx = np.where(self.npn[:,0] == cn[7])[0][0]; nds.append(self.npn[idx])
                        idx = np.where(self.npn[:,0] == cn[8])[0][0]; nds.append(self.npn[idx])
                        idx = np.where(self.npn[:,0] == cn[9])[0][0]; nds.append(self.npn[idx])
                        if cn[10] > 0: idx = np.where(self.npn[:,0] == cn[10])[0][0]; nds.append(self.npn[idx])

                        for k, i in enumerate(ix): 
                            nns = []
                            idx = np.where(self.npn[:,0] == free[i][7])[0][0]; nns.append(self.npn[idx])
                            idx = np.where(self.npn[:,0] == free[i][8])[0][0]; nns.append(self.npn[idx])
                            idx = np.where(self.npn[:,0] == free[i][9])[0][0]; nns.append(self.npn[idx])
                            if cn[10] > 0: idx = np.where(self.npn[:,0] == free[i][10])[0][0]; nns.append(self.npn[idx])
                            f = 0
                            fdist = 0 
                            for d in nds: 
                                for n in nns: 
                                    dist = sqrt((d[1]-n[1])**2 + (d[2]-n[2])**2 + (d[3]-n[3])**2)
                                    if round(abs(dist-self.pitchlength)) < margin_pitchlength: 
                                        f += 1 
                                        fdist = dist
                                        break 
                            if len(nns) == f: 
                                pitchup.append(free[i])
                                pitchdown.append(cn)
                                print ("  ### %d, surface distance between (%4d, %4d) is %.3f (pitch length=%.3f, diff=%.3f)"%(k+1, cn[0]-10**7, free[i][0]-10**7, fdist*1000, self.pitchlength*1000, (fdist-self.pitchlength)*1000))
                                break 
            
        # t1 = time.time(); print("mesh check time %.3f"%(t1-t0))

        if method == 3: 
            edge_btm_boundary = self.SurfaceBoundary(bottom)
            btmg = []
            edge_side = []
            unpaired = []

            edge_btm = []
            # ta = time.time()
            for i, bt in enumerate(edge_btm_boundary): 
                ix = np.where(npn[:,0] == bt[0])[0][0]; n1 = npn[ix]
                ix = np.where(npn[:,0] == bt[1])[0][0]; n2 = npn[ix]
                edge_btm.append([bt[0], bt[1], bt[2], bt[3], n1[1], n1[2], n1[3], n2[1], n2[2], n2[3] ])

            edge_btm_boundary = np.array(edge_btm, dtype=np.float64)
            
            margin = 0.2E-03 
            # print (len(edge_btm_boundary), "\n", len(edge_btm_boundary[0]))
            ymx = np.max(edge_btm_boundary[:,5])
            ynx = np.min(edge_btm_boundary[:, 5])
            ylim = [ynx+margin, ymx-margin]

            # tb = time.time(); print("sub time %.3f"%(tb-ta))
            # ta = time.time()

            
            for bt in edge_btm_boundary: 
                # ix = np.where(npn[:,0] == bt[0])[0][0]; n1 = npn[ix]
                # ix = np.where(npn[:,0] == bt[1])[0][0]; n2 = npn[ix]
                n1 = [bt[0], bt[4], bt[5], bt[6]]
                n2 = [bt[1], bt[7], bt[8], bt[9]]

                if (n1[2] <= ylim[0] and n2[2] <=ylim[0]) or (n1[2] >= ylim[1] and n2[2] >=ylim[1]) : 
                    edge_side.append(bt)
                    continue 

                if n1[2] > n2[2]: btmg.append([bt[0], bt[1], bt[2], bt[3], n2, n1])
                else:             btmg.append([bt[0], bt[1], bt[2], bt[3], n1, n2]) 
            # tb = time.time(); print("1 sub time %.3f"%(tb-ta))
            # ta = time.time()

            pitch_up_down =[]
            # tsum = 0
            for sf in free: 
                
                # if sf[0]-10**7 == 3144 :
                #     print ("%d, %.3f, %.3f, %.3f"%(sf[0]-10**7, sf[4]*1000, sf[5]*1000, sf[6]*1000))

                for bt in btmg: 
                    # ttt = time.time()
                    d, P = DistanceFromLineToNode2D([0, sf[4], sf[5], sf[6]], [bt[4], bt[5]], xy=12)
                    # ttb = time.time()
                    # tsum += ttb - ttt 

                    # if sf[0]-10**7 == 3144 and  d <= 0.15E-03 : 
                    #     print (" > d=%.5f (%8.3f, %8.3f ~ %8.3f, %8.3f )"%(d*1000, bt[4][1]*1000, bt[4][2]*1000, bt[5][1]*1000, bt[5][2]*1000))
                    if bt[4][1] < bt[5][1]: 
                        lx = bt[4]
                        ux = bt[5]
                    else: 
                        lx = bt[5]
                        ux = bt[4] 
                    if d <= 0.15E-03 and bt[4][2] <= P[2] and P[2] <= bt[5][2] and (lx[1] <= P[1] and P[1] <= ux[1]) : 
                        # if sf[0]-10**7 == 3144 and  d <= 0.15E-03 : 
                        #     print (" >>> IN ")
                        pitch_up_down.append(sf)
                        break 
            # tb = time.time(); print("2 sub time %.3f"%(tb-ta))
            # print ("dist cal =%.3f"%(tsum))
            # ta = time.time()

            # pitch_margin = 0.1E-03
            margin = 0.2E-03 
            pitch_up_down = np.array(pitch_up_down)

            # print (" pitch all", len(pitch_up_down))
            for i, sf in enumerate(pitch_up_down): 
                ix1 = np.where(pitch_up_down[:,4] >= sf[4] + self.pitchlength - margin)[0]
                ix2 = np.where(pitch_up_down[:,4] <= sf[4] + self.pitchlength + margin)[0]
                ixx = np.intersect1d(ix1, ix2) 

                ix1 = np.where(pitch_up_down[:,5] >= sf[5]-margin)[0]
                ix2 = np.where(pitch_up_down[:,5] <= sf[5]+margin)[0]
                ixy = np.intersect1d(ix1, ix2) 

                ix1 = np.where(pitch_up_down[:,6] >= sf[6]-margin)[0]
                ix2 = np.where(pitch_up_down[:,6] <= sf[6]+margin)[0]
                ixz = np.intersect1d(ix1, ix2) 

                ix = np.intersect1d(ixx, ixy)
                ix = np.intersect1d(ix, ixz) 

                if len(ix) == 1: 
                    pitchdown.append(sf)
                    pitchup.append(pitch_up_down[ix[0]])
                else: 
                    unpaired.append(pitch_up_down[i])

            pitchup   = np.array(pitchup)
            pitchdown =  np.array(pitchdown)
            # tb = time.time(); print("3 sub time %.3f"%(tb-ta))
            # ta = time.time()
            # print (" unpaired surf", len(unpaired))
            # print (" paired surf", len(pitchup), len(pitchdown))
            i = 0 
            while i < len(unpaired): 
                # print (unpaired[i][0], ", ", unpaired[i][1])
                ix1 = np.where(pitchup[:,0] == unpaired[i][0])[0]
                ix2 = np.where(pitchup[:,1] == unpaired[i][1])[0]
                ix = np.intersect1d(ix1, ix2) 

                ix1 = np.where(pitchdown[:,0] == unpaired[i][0])[0]
                ix2 = np.where(pitchdown[:,1] == unpaired[i][1])[0]
                jx = np.intersect1d(ix1, ix2) 

                if len(ix) == 1 or len(jx) == 1: 
                    del(unpaired[i])
                    i -= 1 
                i += 1 

            # print (" unpaired surf", len(unpaired))
            # tb = time.time(); print("4 sub time %.3f"%(tb-ta))
            # ta = time.time()

            pitch_boundary = self.SurfaceBoundary(pitchup)
            sidebound  = np.max(npn[:,2]) * 0.8

            # print ("pitch up boundary")
            # print ("Half OD = ", halfOD)
            sidenodes =[]
            
            for edge in pitch_boundary: 
                ix = np.where(npn[:,0]==edge[0])[0][0]
                if abs(npn[ix][2]) > sidebound: 
                    ix1 = np.where(npn[:,0]==edge[1])[0][0]

                    if npn[ix][3] != halfOD or npn[ix1][3] != halfOD: 
                        # print ("%.3f(%.3f, %.3f), %.3f(%.3f, %.3f)"%(abs(npn[ix][2]-npn[ix1][2])*1000, npn[ix][2]*1000, npn[ix1][2]*1000, abs(npn[ix][3]-npn[ix1][3])*1000, npn[ix][3]*1000, npn[ix1][3]*1000)    )
                        if npn[ix][3] < npn[ix1][3]: sidenodes.append([npn[ix], npn[ix1]])
                        else: sidenodes.append([npn[ix1], npn[ix]])

            posnd=[]; negnd=[]
            for sn in sidenodes:
                ix1 = np.where(free[:,6]>=sn[0][3])[0]
                ix2 = np.where(free[:,6]<=sn[1][3])[0]
                ix = np.intersect1d(ix1, ix2)
                mxY = (sn[0][2]+sn[1][2])/2.0
                if mxY > 0: 
                    mxY += 0.05e-3
                    idx = -1
                    for x in ix: 
                        if free[x][5] > mxY: 
                            mxY = free[x][5]
                            idx = x 
                else: 
                    mxY -= 0.05e-3
                    idx = -1
                    for x in ix: 
                        if free[x][5] < mxY: 
                            mxY = free[x][5]
                            idx = x 
                if idx > 0: 
                    nz = sn[0][3]+1.0; mz = sn[1][3]-1.0
                    n01=[]; n02=[]

                    ix = np.where(npn[:,0] == free[x][7])[0][0]
                    if npn[ix][3] <= nz: 
                        nz = npn[ix][3];    n01 = npn[ix]
                    if npn[ix][3] >= mz: 
                        mz = npn[ix][3];    n02 = npn[ix]

                    ix = np.where(npn[:,0] == free[x][8])[0][0]
                    if npn[ix][3] <= nz: 
                        nz = npn[ix][3];    n01 = npn[ix]
                    if npn[ix][3] >= mz: 
                        mz = npn[ix][3];    n02 = npn[ix]
                    
                    ix = np.where(npn[:,0] == free[x][9])[0][0]
                    if npn[ix][3] <= nz: 
                        nz = npn[ix][3];    n01 = npn[ix]
                    if npn[ix][3] >= mz: 
                        mz = npn[ix][3];    n02 = npn[ix]
                    
                    if n01[0] != n02[0]: 
                        sn[0]=n01; sn[1] = n02 
                        # print ("SIDE NODE REPlaced", n01, n02 )

                if mxY > 0: 
                    posnd.append(sn[0])
                    posnd.append(sn[1])
                else:
                    negnd.append(sn[0])
                    negnd.append(sn[1])

            if shoulder =="S": 
                posnd = sorted(posnd, key=lambda x: x[3], reverse=True)
                negnd = sorted(negnd, key=lambda x: x[3], reverse=True)
                i = 1
                while i<len(posnd): 
                    if posnd[i-1][0] == posnd[i][0]: 
                        del(posnd[i])
                        continue 
                    j = i+1 
                    while j < len(posnd): 
                        if posnd[i][2] == posnd[j][2] and posnd[i][3] == posnd[j][3]: 
                            del(posnd[j])
                            continue
                        j += 1 
                    i += 1 
                i = 1
                while i<len(negnd): 
                    if negnd[i-1][0] == negnd[i][0]: 
                        del(negnd[i])
                        continue 
                    j = i+1 
                    while j < len(negnd): 
                        if negnd[i][2] == negnd[j][2] and negnd[i][3] == negnd[j][3]: 
                            del(negnd[j])
                            continue
                        j += 1 
                    i += 1 

                i = 1 
                while i < len(posnd): 
                    if abs(posnd[i][3] - posnd[i-1][3]) < 0.001: 
                        if abs(posnd[i][2]) > abs(posnd[i-1][2]) : del(posnd[i-1])
                        else: del(posnd[i])
                        continue 
                    i += 1
                i = 1 
                while i < len(negnd): 
                    if abs(negnd[i][3] - negnd[i-1][3]) < 0.001: 
                        if abs(negnd[i][2]) > abs(negnd[i-1][2]) : del(negnd[i-1])
                        else: del(negnd[i])
                        continue 
                    i += 1

                i = 2
                chamferNodes=[posnd[0], posnd[1]]
                # print("%d, %.5f, %.5f"%(posnd[0][0]-10**7, posnd[0][2], posnd[0][3]))
                # print("%d, %.5f, %.5f"%(posnd[1][0]-10**7, posnd[1][2], posnd[1][3]))
                chamfer = 0 
                lowR = 0 
                while i<len(posnd): 
                    # if i ==2: 
                    #     print ("N %6d, %10.2f, %10.2f"%(posnd[i-2][0]-10**7, posnd[i-2][2]*1000, posnd[i-2][3]*1000))
                    #     print ("N %6d, %10.2f, %10.2f"%(posnd[i-1][0]-10**7, posnd[i-1][2]*1000, posnd[i-1][3]*1000))
                    # print ("N %6d, %10.2f, %10.2f"%(posnd[i][0]-10**7, posnd[i][2]*1000, posnd[i][3]*1000), end=", ")
                    if posnd[i-1][2] > posnd[i][2]: 
                        # print ("END Y_i-1=%.3f, Y_i=%.3f"%(posnd[i-1][2]*1000, posnd[i][2]*1000))
                        break 
                    if posnd[i-2][3] == posnd[i-1][3] or  posnd[i-1][3] == posnd[i][3]: 
                        # print (" Horizental > Continuing, ", posnd[i-2][3]*1000 , posnd[i-1][3]*1000 , posnd[i][3]*1000 )
                        i += 1
                        continue 
                    radius, pCen = Circle3Nodes(posnd[i-2], posnd[i-1], posnd[i], xy=23, radius=1, center=1, error=0)
                    
                    # print ("radius=, %.5f"%(radius*1000))
                    
                    if radius < 0.05: 
                        lowR = 1
                        
                    if lowR ==1 and radius > 0.05: 
                        chamfer = 1
                        print ("## Chamfered pattern mesh")
                        print ("   Pattern TDW modified to TW (%.1f -> "%(self.TreadDesignWidth*1000), end="")
                        if pCen[0] == -1: 
                            # print ("\n%d, %.7f, %.7f"%(posnd[i-2][0], posnd[i-2][2], posnd[i-2][3]))
                            # print ("%d, %.7f, %.7f"%(posnd[i-1][0], posnd[i-1][2], posnd[i-1][3]))
                            # print ("%d, %.7f, %.7f"%(posnd[i][0], posnd[i][2], posnd[i][3]))
                            self.TreadDesignWidth = ( posnd[i][2] + (halfOD - posnd[3]) *(posnd[i][2]-posnd[i-1][2]) / (posnd[i][3]-posnd[i-1][3])  ) * 2.0
                        else: 
                            self.TreadDesignWidth = (pCen[2] - sqrt(radius*radius - (halfOD - pCen[3])**2)) * 2.0 
                        print (" %.1f)\n"%(self.TreadDesignWidth*1000))

                        break 
                    chamferNodes.append(posnd[i])
                    i += 1 
                    if i>1000:  break
                
                
                if chamfer ==1: 
                    chamferNodes = chamferNodes[:-2]

                    chamferNodes.append(negnd[0])
                    chamferNodes.append(negnd[1])
                    chamfer = 0 
                    lowR = 0 
                    i = 2
                    while i<len(negnd):
                        if negnd[i-1][2] < negnd[i][2]: 
                            break 
                        if negnd[i-2][3] == negnd[i-1][3] or  negnd[i-1][3] == negnd[i][3]: 
                            i += 1
                            continue  
                        radius, pCen = Circle3Nodes(negnd[i-2], negnd[i-1], negnd[i], xy=23, radius=1, center=1, error=0)
                        if radius < 0.05: 
                            lowR = 1
                        if lowR ==1 and radius > 0.05: 
                            chamfer = 1
                            break 
                        chamferNodes.append(negnd[i])
                        i+=1
                        if i>1000:  break

                    chamferNodes = chamferNodes[:-2]

                    ## deleting nodes on chamfer from side nodes group

                    i =0
                    while i < len(sidenodes): 
                        fd =0
                        for cn in chamferNodes:
                            if sidenodes[i][0][0] == cn[0] or sidenodes[i][1][0] == cn[0]: 
                                fd =1 
                                break 
                        if fd ==1: 
                            del(sidenodes[i])
                            continue 
                        i += 1 
                        if i>10000:  break

                    i =0
                    while i < len(sidenodes):
                        if abs(sidenodes[i][0][3] -sidenodes[i][1][3]) < 0.0001: 
                            del(sidenodes[i])
                            continue 
                        j = i+1  
                        while j<len(sidenodes): 
                            if sidenodes[i][0][0] == sidenodes[j][0][0] and sidenodes[i][1][0] == sidenodes[j][1][0]: 
                                del(sidenodes[j])
                                continue 
                            j += 1

                        i += 1
                    
            ## delete duplicates and nodes not on pitch up surface. 
            i = 0 
            while i < len(sidenodes): 
                j = i+1 
                while j < len(sidenodes): 
                    if sidenodes[i][0][2] == sidenodes[j][0][2] and sidenodes[i][0][3] == sidenodes[j][0][3]: 
                        if sidenodes[i][0][1] > sidenodes[j][0][1] : 
                            del(sidenodes[j])
                            continue 
                        else:
                            del(sidenodes[i])
                            i -= 1
                            break 
                    if sidenodes[i][1][2] == sidenodes[j][1][2] and sidenodes[i][1][3] == sidenodes[j][1][3]: 
                        if sidenodes[i][1][1] > sidenodes[j][1][1] : 
                            del(sidenodes[j])
                            continue 
                        else:
                            del(sidenodes[i])
                            i -= 1
                            break 

                    j += 1
                i += 1

            # for i, nds in enumerate(sidenodes): 
            #     if nds[0][2]*1000>0: print ("%d, %.3f, %.3f, %d, %.3f, %.3f"%(nds[0][0]-10**7, nds[0][2]*1000, nds[0][3]*1000, nds[1][0]-10**7, nds[1][2]*1000, nds[1][3]*1000))
            ##############################################################

            alledges = AllEdgesInSurface(free, self.solidnodes)
            neg=[]; pos=[]
            for edge in edge_side: ## edge_side >> bottom edge side 
                cedge = self.FindContactingEdge(edge, alledges, samedirection=1)
                if len(cedge) ==0: 
                    continue 
                nedge, nsf = self.FindAnotherEdgeInSurface(next=2, cedge=cedge, edges=alledges, surfaces=free, sfreturn=1, face_exclude=2)
                
                # if len(nsf) == 0: print (edge, cedge, nedge, nsf) 
                cnt = 0 
                while len(nsf) > 0: 

                    tn = [nsf[0], nsf[4], nsf[5], nsf[6]]
                    fd = 0 
                    for nds in sidenodes: 
                        dst, CN = DistanceFromLineToNode2D(tn, nds, xy=23)
                        if dst < 0.08e-3: 
                            # print ("Side NODE, %6d, %6d > Elid, %6d, d=,%.6f"%(nds[0][0]-10**7,nds[1][0]-10**7, tn[0]-10**7, dst*1000))
                            if nds[0][3] > nds[1][3]: 
                                if nds[0][3] > CN[3] and CN[3] > nds[1][3]: 
                                    fd =1 
                                    break 
                            else: 
                                if nds[1][3] > CN[3] and CN[3] > nds[0][3]: 
                                    fd =1 
                                    break 
                    if fd ==0: 
                        break 
                    
                    if nsf[5] > 0: 
                        pos.append(nsf)
                        # print (" %3d pos side "%(len(pos)), nsf[0]-10**7)
                    else: 
                        neg.append(nsf)
                        # print (" %3d Neg side "%(len(neg)), nsf[0]-10**7)
                    cedge = self.FindContactingEdge(nedge, alledges, samesolid=0)
                    if len(cedge) != 0 : 
                        nedge, nsf = self.FindAnotherEdgeInSurface(next=2, cedge=cedge, edges=alledges, surfaces=free, sfreturn=1, face_exclude=2)
                        if len(nsf) == 0: break 
                        if nsf[1] == 2: break 
                    else: 
                        break 
                    cnt += 1
                    if cnt > 50: 
                        print ("## Too many iterations for pattern side surfaces.")
                        return 
            # tb = time.time(); print("5 sub time %.3f"%(tb-ta))
            # ta = time.time()
            # t2 = time.time(); print("side surf time %.3f"%(t2-t1))
            return pitchup, pitchdown, np.array(neg), np.array(pos), unpaired


        if method ==2:  

            # btmedges = AllEdgesInSurface(bottom, self.solidnodes)
            alledges = AllEdgesInSurface(free, self.solidnodes)

            sides = []
            for edge in edge_btm_boundary: 
                cedge = self.FindContactingEdge(edge, alledges, samedirection=1)
                if len(cedge) ==0: 
                    continue 
                nedge, nsf = self.FindAnotherEdgeInSurface(next=2, cedge=cedge, edges=alledges, surfaces=free, sfreturn=1, face_exclude=2)
                
                if len(nsf) == 0: print (edge, cedge, nedge, nsf) 
                cnt = 0 
                while len(nsf) > 0: 
                    sides.append(nsf)
                    cedge = self.FindContactingEdge(nedge, alledges, samesolid=0)
                    if len(cedge) != 0 : 
                        nedge, nsf = self.FindAnotherEdgeInSurface(next=2, cedge=cedge, edges=alledges, surfaces=free, sfreturn=1, face_exclude=2)
                        if len(nsf) == 0: break 
                        if nsf[1] == 2: break 
                    else: 
                        break 
                    cnt += 1
                    if cnt > 50: 
                        print ("## Too many iterations for pattern side surfaces.")
                        sys.exit()
                        
            sides = np.array(sides) 
            mxy = np.max(self.solidnodes[:,2])
            mny = np.min(self.solidnodes[:,2])
            
            posside=[]; negside=[]
            pitches = []
            no_pitchsurf = 0 
            UpVector = [0, 0.0, 0.0, 1.0]

            margin_pitchlength = 0.1E-03 
            margin = 3.0E-3 
            pitchupdown_searching_method= 0
            if pitchupdown_searching_method != 1:
                margin_pitchlength = 0.1E-03 
                margin = 3.0E-3  
                sidedif = margin_pitchlength * 1.5 
                pitchside = margin_pitchlength * 2 
                for sf in sides: 
                    if sf[10] > 0: 
                        ix = np.where(self.solidnodes[:,0] == sf[7])[0][0];  n1 = [self.solidnodes[ix][0], round(self.solidnodes[ix][1], 5), round(self.solidnodes[ix][2], 5), self.solidnodes[ix][3]]
                        ix = np.where(self.solidnodes[:,0] == sf[8])[0][0];  n2 = [self.solidnodes[ix][0], round(self.solidnodes[ix][1], 5), round(self.solidnodes[ix][2], 5), self.solidnodes[ix][3]]
                        ix = np.where(self.solidnodes[:,0] == sf[9])[0][0];  n3 = [self.solidnodes[ix][0], round(self.solidnodes[ix][1], 5), round(self.solidnodes[ix][2], 5), self.solidnodes[ix][3]]
                        ix = np.where(self.solidnodes[:,0] == sf[10])[0][0]; n4 = [self.solidnodes[ix][0], round(self.solidnodes[ix][1], 5), round(self.solidnodes[ix][2], 5), self.solidnodes[ix][3]]
                        
                        # if sf[0]-10**7 > 1053 and sf[0]-10**7 > 1070 : 
                        #     print ("%d, MY=%.2f"%(sf[0]-10**7, mxy*1000))
                        #     print ("n1 %d, %.2f, %.2f, %.2f"%(n1[0]-10**7, n1[1]*1000, n1[2]*1000, n1[3]*1000))
                        #     print ("n2 %d, %.2f, %.2f, %.2f"%(n2[0]-10**7, n2[1]*1000, n2[2]*1000, n2[3]*1000))
                        #     print ("n3 %d, %.2f, %.2f, %.2f"%(n3[0]-10**7, n3[1]*1000, n3[2]*1000, n3[3]*1000))
                        #     print ("n4 %d, %.2f, %.2f, %.2f"%(n4[0]-10**7, n4[1]*1000, n4[2]*1000, n4[3]*1000))
                        if (abs(n1[2] - n2[2]) <sidedif and abs(n3[2] - n4[2]) < sidedif ) and abs(n4[3] - n1[3]) > abs(n4[2] - n1[2]) and (abs(n4[2]) > mxy - margin) : # or n4[2] < mny + margin)  : 
                            # if n1[2] > mxy - margin: posside.append(sf) 
                            # if n1[2] < mny + margin: negside.append(sf) 
                            if n1[2] < 0.0 : negside.append(sf)
                            else:            posside.append(sf)
                        else: 
                            # no_pitchsurf+= 1
                            id1 = np.where(sides[:,4] > sf[4] + self.pitchlength - margin_pitchlength)
                            id2 = np.where(sides[:,4] < sf[4] + self.pitchlength + margin_pitchlength)
                            idx = np.intersect1d(id1, id2)

                            id1 = np.where(sides[:,5] > sf[5]  -pitchside)
                            id2 = np.where(sides[:,5] < sf[5]  +pitchside)
                            idy = np.intersect1d(id1, id2)

                            id1 = np.where(sides[:,6] > sf[6]  - pitchside)
                            id2 = np.where(sides[:,6] < sf[6]  + pitchside)
                            idz = np.intersect1d(id1, id2)

                            idx = np.intersect1d(idx, idy)
                            idx = np.intersect1d(idx, idz)
                            if len(idx) ==1: 
                                    pitchdown.append(sf)
                                    pitchup.append(sides[idx[0]])
                                    # print (".. up %d"%(sides[idx[0]][0]))
                            else: 
                                pass
            else: 
                margin = 0.2E-03 
                margin_s = 3.0E-3  
                nsides = []
                outc = 0 
                digit = 6
                for sf in sides: 
                    if sf[10] > 0: 
                        ix = np.where(self.solidnodes[:,0] == sf[7])[0][0];  n1 = [self.solidnodes[ix][0], round(self.solidnodes[ix][1], digit), round(self.solidnodes[ix][2], digit), self.solidnodes[ix][3]]
                        ix = np.where(self.solidnodes[:,0] == sf[8])[0][0];  n2 = [self.solidnodes[ix][0], round(self.solidnodes[ix][1], digit), round(self.solidnodes[ix][2], digit), self.solidnodes[ix][3]]
                        ix = np.where(self.solidnodes[:,0] == sf[9])[0][0];  n3 = [self.solidnodes[ix][0], round(self.solidnodes[ix][1], digit), round(self.solidnodes[ix][2], digit), self.solidnodes[ix][3]]
                        ix = np.where(self.solidnodes[:,0] == sf[10])[0][0]; n4 = [self.solidnodes[ix][0], round(self.solidnodes[ix][1], digit), round(self.solidnodes[ix][2], digit), self.solidnodes[ix][3]]
                        nsides.append([ sf[0], sf[2], sf[2], sf[3], sf[4], sf[5], sf[6], n1[0], n1[1], n1[2], n1[3], n2[0], n2[1], n2[2], n2[3], n3[0], n3[1], n3[2], n3[3], n4[0], n4[1], n4[2], n4[3]])
                    # else: 
                    #     print (sf)
                nsides = np.array(nsides)
                for sf in nsides: 
                    n1 = [sf[7], sf[8], sf[9], sf[10]]
                    n2 = [sf[11], sf[12], sf[13], sf[14]]
                    n3 = [sf[15], sf[16], sf[17], sf[18]]
                    n4 = [sf[19], sf[20], sf[21], sf[22]]
                    
                    if (abs(n1[2] - n2[2]) < margin and abs(n3[2] - n4[2]) < margin ) and abs(n4[3] - n1[3]) > abs(n4[2] - n1[2]) and (n4[2] > mxy - margin_s or n4[2] < mny + margin_s)  : 
                        if n3[2] > mxy - margin_s: posside.append(sf) 
                        if n3[2] < mny + margin_s: negside.append(sf) 

                    else: 
                        f = 1 
                        if f == 1: 
                            id1 = np.where(nsides[:,16] > n3[1] + self.pitchlength - margin)
                            id2 = np.where(nsides[:,16] < n3[1] + self.pitchlength + margin)
                            ix01 = np.intersect1d(id1, id2)

                            id1 = np.where(nsides[:,17] > n3[2] - margin)
                            id2 = np.where(nsides[:,17] < n3[2] + margin)
                            ix02 = np.intersect1d(id1, id2)

                            id1 = np.where(nsides[:,18] > n3[3] - margin)
                            id2 = np.where(nsides[:,18] < n3[3] + margin)
                            ix03 = np.intersect1d(id1, id2)
                            ix1 = np.intersect1d(ix01, ix02)
                            ix1 = np.intersect1d(ix1, ix03)
                            # print ("\nix1", ix1)
                            
                            if len(ix1) == 0 : 
                                outc += 1 
                                continue 
                            if len(ix1) == 0 : print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

                            id1 = np.where(nsides[:,20] > n4[1] + self.pitchlength - margin)
                            id2 = np.where(nsides[:,20] < n4[1] + self.pitchlength + margin)
                            ix01 = np.intersect1d(id1, id2)

                            id1 = np.where(nsides[:,21] > n4[2] - margin)
                            id2 = np.where(nsides[:,21] < n4[2] + margin)
                            ix02 = np.intersect1d(id1, id2)

                            id1 = np.where(nsides[:,22] > n4[3] - margin)
                            id2 = np.where(nsides[:,22] < n4[3] + margin)
                            ix03 = np.intersect1d(id1, id2)
                            ix2 = np.intersect1d(ix01, ix02)
                            ix2 = np.intersect1d(ix2, ix03)
                            # print ("ix2", ix2)
                            if len(ix2) == 0: 
                                continue 
                            
                            id1 = np.where(nsides[:,8] > n1[1] + self.pitchlength - margin)
                            id2 = np.where(nsides[:,8] < n1[1] + self.pitchlength + margin)
                            ix01 = np.intersect1d(id1, id2)

                            id1 = np.where(nsides[:,9] > n1[2] - margin)
                            id2 = np.where(nsides[:,9] < n1[2] + margin)
                            ix02 = np.intersect1d(id1, id2)

                            id1 = np.where(nsides[:,10] > n1[3] - margin)
                            id2 = np.where(nsides[:,10] < n1[3] + margin)
                            ix03 = np.intersect1d(id1, id2)
                            ix3 = np.intersect1d(ix01, ix02)
                            ix3 = np.intersect1d(ix3, ix03)
                            # print ("ix2", ix3)
                            if len(ix3) > 0 : 
                                ixs1 = np.where(sides[:,7:]==n3[0])[0]
                                ixs2 = np.where(sides[:,7:]==n4[0])[0]
                                ixs3 = np.where(sides[:,7:]==n1[0])[0]
                                ix = np.intersect1d(ixs1, ixs2)
                                ix = np.intersect1d(ix, ixs3)
                                # print ("ix", ix)
                                if len(ix) == 1: 
                                    pitchdown.append([sf[0], sf[1], sf[2], sf[3], sf[4], sf[5], sf[6], sf[7], sf[11], sf[15], sf[19] ] )
                                    pitchup.append(sides[ix[0]])

            print ("* The number of surfaces : %d"%( len(sides)))
            print ("* Pitch Up=%d,Down=%d, sides=%d,%d(res=%d)"%(len(pitchup), len(pitchdown), len(posside), len(negside), len(sides) - len(pitchdown) - len(pitchup) - len(posside) - len(negside) ))
            # print ("* out=%d"%(outc))
        else:
            print ("* Pitch Up =%d, Down=%d "%(len(pitchup), len(pitchdown)))
        
        # sys.exit()
        if len(freesurf2del)>0: 
            N = len(free)
            for surf in freesurf2del: 
                ix1 = np.where(free[:,0] == surf[0])[0]
                ix2 = np.where(free[:,1] == surf[1])[0]

                ix = np.intersect1d(ix1, ix2) 
                if len(ix) == 1 : 
                    free = np.delete(free, ix[0], axis=0)

            print ("## Free surface is reduced(%d>%d(%d)).\n"%(N, len(free), len(free)-N))
            # print ("#########################################################")
        pitchup = np.array(pitchup)
        pitchdown = np.array(pitchdown)
        # bottom = np.array(bottom)
        
        if method ==2 :
            pos = np.array(posside)
            neg = np.array(negside) 
            return pitchup, pitchdown, neg, pos
        else: 
            # return bottom, free, pitchup, pitchdown
            return pitchup, pitchdown
    def SurfaceBoundary(self, surface):
        ## surface = [El_id, Face_Id(1~6), type(3 or 4), layer, center X, y, z, n1, n2, n3, n4]
        bndedge=[]
        alledge =[]
        for sf in surface:
            alledge.append([int(sf[7]), int(sf[8]), 0, sf[0]])
            alledge.append([int(sf[8]), int(sf[9]), 0, sf[0]])
            if sf[2] == 3: alledge.append([int(sf[9]), int(sf[7]), 0, sf[0]])
            else:
                alledge.append([int(sf[9]), int(sf[10]), 0, sf[0]])
                alledge.append([int(sf[10]), int(sf[7]), 0, sf[0]])

        npedge = np.array(alledge, dtype=np.int32)
        N = len(npedge)
        for i, eg in enumerate(npedge):
            if eg[2] == -1: continue
            bnd = 1

            ind1 = np.where(npedge[:, 1] == eg[0])
            if len(ind1[0]) > 0 : 
                N = len(ind1[0])
                for j in range(N):
                    if npedge[ind1[0][j]][0] == eg[1]: 
                        npedge[i][2] = -1
                        bnd = 0 
                        break 
            if bnd ==1:
                npedge[i][2] =1
                bndedge.append(npedge[i])
        
        return np.array(bndedge)
    def RemoveGrooveSideSurface(self, groove_base_surface, side_surface, call="", mbtm=[], sbtm=[]):
        error=0 
        Boundary = self.SurfaceBoundary(groove_base_surface)  ## search for the boundary edges 
        side = []
        removed = []

        side = np.array(side_surface)
        for bd in Boundary: 
            SF_adj=[0]
            nextedge = bd 
            cnt = 0 
            while len(SF_adj) > 0: 
                SF_adj_1 = np.where(side[:, 7:9] == nextedge[0])
                SF_adj_2 = np.where(side[:, 7:9] == nextedge[1])
                SF_adj = np.intersect1d(SF_adj_1[0], SF_adj_2[0])

                if len(SF_adj) > 1: 
                    if ("Pitch" in call or "Full Depth" in call ) and len(SF_adj) ==2 : 
                        break  ## It seems to be a kerf edge..
                        
                    error = 1 
                    print ("Error.  Too many surfaces that have a edge (%d, %d) on solid ( %d edges were found (tha should be 1)  "%(nextedge[0]-10**7, nextedge[1]-10**7, len(SF_adj)))
                    print (" FUNCTION : Remove Groove Side Surface Called by %s"%(call))
                    print ("BD EL %d, %d, %d"%(bd[3]-10**7, bd[0]-10**7, bd[1]-10**7))
                    print ("Nedge %d, %d, %d"%(nextedge[3]-10**7, nextedge[0]-10**7, nextedge[1]-10**7))
                    for ix in SF_adj:
                        print (" Solid %8d, Face=%d, N1=%d, N2=%d, N3=%d, N4=%d (X1=%7.3f, X2=%7.3f, X3=%7.3f)"%(side[ix][0]-10**7, side[ix][1], \
                                side[ix][7]-10**7, side[ix][8]-10**7, side[ix][9]-10**7, side[ix][10]-10**7, \
                                side[ix][4]*1000, side[ix][5]*1000, side[ix][6]*1000))
                        sx = np.where(self.nps[:,0]==side[ix][0])[0][0]
                    tp =[]
                    for d in SF_adj: 
                        tp.append(side[d])

                    solids=[]
                    SF_adj_1 = np.where(self.nps[:, 1:9] == nextedge[0])
                    SF_adj_2 = np.where(self.nps[:, 1:9] == nextedge[1])
                    SF_adj = np.intersect1d(SF_adj_1[0], SF_adj_2[0])
                    ids = []
                    for s in SF_adj_1[0]: 
                        ids.append(s)
                    for s in SF_adj_2[0]: 
                        ids.append(s)
                        
                    ids = np.array(ids)
                    ids = np.unique(ids)
                    
                    for s in ids: 
                        solids.append(self.nps[s])

                    try: 
                        ShowSolid(solids, self.npn)
                        sys.exit()
                    except: 
                        pass 
                    return side, np.array(removed), solids 
                    
                elif len(SF_adj) == 0: 
                    break 
                
                i = SF_adj[0]
                nextedge =[int(side[i][9]), int(side[i][10]), 0, int(side[i][0])]
                removed.append(side[i])
                side = np.delete(side, i, axis=0) 
                cnt += 1
                if cnt > 30: 
                    print ("!! ERROR, Too many attempts to groove side surfaces")
                    solids=[]
                    SF_adj_1 = np.where(self.nps[:, 1:9] == nextedge[0])
                    SF_adj_2 = np.where(self.nps[:, 1:9] == nextedge[1])
                    SF_adj = np.intersect1d(SF_adj_1[0], SF_adj_2[0])
                    ids = []
                    for s in SF_adj_1[0]: 
                        ids.append(s)
                    for s in SF_adj_2[0]: 
                        ids.append(s)
                        
                    ids = np.array(ids)
                    ids = np.unique(ids)
                    
                    for s in ids: 
                        solids.append(self.nps[s])

                    try: 
                        ShowSolid(solids, self.npn)
                        sys.exit()
                    except: 
                        pass 

                    return side, np.array(removed), solids 

        return side, np.array(removed), error  
    def Residual_GrooveSideSurfaces(self, top_surf, bottom, free, npn, presurf): 
        ## free : groove sides, kerf sides 
        ## fdepth : full depth groove 
        ## sdepth : sub groove 

        ## 1st : seargching the kerf sides 

        surf_residual = []
        kerf=[]
        check=[]
        margin = 0.5E-03

        if len(free) == 0: 
            return free, surf_residual, kerf

        R = np.max(npn[:,3])

        topedge = self.SurfaceBoundary(top_surf)
        alledges = AllEdgesInSurface(free, npn)
        
        # show = 0 
        isearch = 555
        ix = np.where(self.nps[:,0]== isearch + 10**7)[0][0]
        print("%d, %d, %d, %d, %d, %d, %d, %d, %d"%(self.nps[ix][0]-10**7, \
            self.nps[ix][1]-10**7, self.nps[ix][2]-10**7, self.nps[ix][3]-10**7, self.nps[ix][4]-10**7, \
            self.nps[ix][5]-10**7, self.nps[ix][6]-10**7, self.nps[ix][7]-10**7, self.nps[ix][8]-10**7 ))
        idx = np.where(free[:,0]== isearch + 10**7)[0]
        for ix in idx: 
            print (">%d(%d), %d, %d, %d, %d"%(free[ix][0]-10**7, free[ix][1], free[ix][7]-10**7, free[ix][8]-10**7, free[ix][9]-10**7, free[ix][10]-10**7))
        
        for ed in alledges: 
            if ed[3] -10**7 == isearch: 
                print ("* %d, %d, %d"%(ed[3]-10**7, ed[0]-10**7, ed[1]-10**7))
        
        for edge in topedge: 
            if edge[3] -10**7 == isearch: 
                print (edge)

            f = 0 
            for sf in presurf: 
                if sf[0] == edge[3]: 
                    ct = 0 
                    if sf[7] == edge[0] or sf[8] == edge[0] or sf[9] == edge[0] or sf[10] == edge[0] : 
                        ct += 1
                    if sf[7] == edge[1] or sf[8] == edge[1] or sf[9] == edge[1] or sf[10] == edge[1] : 
                        ct += 1
                    if ct == 2: 
                        # print ("%d, %d, %d, %d, %d"%(sf[0]-10**7, sf[7]-10**7, sf[8]-10**7, sf[9]-10**7, sf[10]-10**7))
                        f = 1
                        break 
            if f == 0: 
                cedge = edge 
                cnt = 0 
                temp = []
                while cnt < 20: 
                    cnt += 1 
                    # if cedge[3] - 10**7 == 874 :      show = 1
                    # else: show = 0  
                    tedge = self.FindContactingEdge(cedge, alledges, show=0)
                    print (" %d >> %d, %d, %d"%(cnt, cedge[3]-10**7, cedge[0]-10**7, cedge[1]-10**7))
                    if len(tedge) == 0: 
                        
                        ix =np.where(npn[:,0] == cedge[0])[0][0]
                        if R-npn[ix][3] <0.5E-03 : 
                            print (" kerf..", len(temp))
                            for tf in temp: 
                                kerf.append(tf)
                        else: 
                            print (" groove..", len(temp))
                            for tf in temp: 
                                surf_residual.append(tf)
                        break 
                    else: 
                        if tedge[3] - 10**7 == isearch : 
                            print ("* %d, %d, %d"%(tedge[3]-10**7, tedge[0]-10**7, tedge[1]-10**7))

                    ixs = np.where(free[:,0]==tedge[3])[0]
                    # print (len(free), ",", ixs)
                    if len(ixs) ==1: 
                        ix = ixs[0]
                        temp.append(free[ix])
                        print ("*>%d(%d), %d, %d, %d, %d\n"%(free[ix][0]-10**7, free[ix][1], free[ix][7]-10**7, free[ix][8]-10**7, free[ix][9]-10**7, free[ix][10]-10**7))
                        
                    elif len(ixs) > 1: 
                        for ix in ixs : 
                            # print (" ix =", ix)
                            ct = 0 
                            if free[ix][7] == tedge[0] or free[ix][8] == tedge[0] or free[ix][9] == tedge[0] or free[ix][10] == tedge[0] : 
                                ct += 1
                            if free[ix][7] == tedge[1] or free[ix][8] == tedge[1] or free[ix][9] == tedge[1] or free[ix][10] == tedge[1] : 
                                ct += 1
                            if ct == 2: 
                                temp.append(free[ix])
                                print (">>%d(%d), %d, %d, %d, %d\n"%(free[ix][0]-10**7, free[ix][1], free[ix][7]-10**7, free[ix][8]-10**7, free[ix][9]-10**7, free[ix][10]-10**7))
                                # print (" IX=", ix)
                                break
                        # print (" >> Ix = ", ix)
                    else: 
                        print ("no matching surfaces ")
                        break 
                     
                    # if tedge[3] - 10**7 == 874 or tedge[3] - 10**7 == 900:
                    #     print (">%d(%d), %d, %d, %d, %d\n"%(free[ix][0]-10**7, free[ix][1], free[ix][7]-10**7, free[ix][8]-10**7, free[ix][9]-10**7, free[ix][10]-10**7))
                    
                    if free[ix][10] > 0: 
                        inext = 2 
                        nedge, sf = self.FindAnotherEdgeInSurface(next=inext, cedge=tedge, edges=alledges, surfaces=free, sfreturn=1)
                    else: 
                        print (" 3 node surface"%(free[ix][0]-10**7))
                        inext = 1 
                        nedge, sf = self.FindAnotherEdgeInSurface(next=inext, cedge=tedge, edges=alledges, surfaces=free, sfreturn=1)
                        if len(nedge) == 0: 
                            inext == 2
                            nedge, sf = self.FindAnotherEdgeInSurface(next=inext, cedge=tedge, edges=alledges, surfaces=free, sfreturn=1)
                    
                    
                    
                    if len(nedge) ==0: 
                        print (" No more edge.. ")
                        break 

                    print ("next %d, %d, %d"%(nedge[3]-10**7, nedge[0]-10**7, nedge[1]-10**7))
                    ix1 = np.where(npn[:,0]== nedge[0])[0][0]
                    ix2 = np.where(npn[:,0]== nedge[1])[0][0]
                    n1 = npn[ix1]; n2 = npn[ix2]

                    if abs(n1[3] - n2[3]) > margin: 
                        ix1 = np.where(npn[:,0]== tedge[0])[0][0]
                        ix2 = np.where(npn[:,0]== tedge[1])[0][0]   
                        n3 = npn[ix1]; n4 = npn[ix2]
                        d1 = NodeDistance(n1, n4)
                        d2 = NodeDistance(n2, n3) 
                        if abs(d1-d2) > margin: 
                            for tf in temp: 
                                check.append(temp)
                            free = np.delete(free, ix, axis=0)
                            break 

                    cedge = nedge 
                    free = np.delete(free, ix, axis=0)
                    # if free[ix][0]-10**7 == 874 :      print ("# %d, %d, %d"%(cedge[3]-10*7, cedge[0]-10**7, cedge[1]-10**7))

        
        i = 0
        while i < len(kerf): 
            j = i+ 1
            while j < len(kerf): 
                if kerf[i][0] == kerf[j][0] and kerf[i][1] == kerf[j][1]: 
                    del(kerf[j])
                    break 
                j += 1 

            i+= 1

        return free, surf_residual, kerf 

    def EliminateShoulderLugEdgeInTopEdges(self, Topedges, npn):
        ## self.TreadDesignWidth

        ## self.freetop, self.freebottom, self.uncheckedfree, self.Surface

        print ("\n* Searching Shoulder Lug ", end=">>")

        BtmBoundary = self.Edge_bottomSurface 

        en = []
        for e in BtmBoundary: 
            en.append(e[0]); en.append(e[1])
        en = np.array(en)
        en = np.unique(en)

        nds = []
        for n in en:
            ix = np.where(npn[:,0]==n)[0][0]
            nds.append(npn[ix])
        nds = np.array(nds)

        minY = np.min(nds[:,2])+0.0001
        maxY = np.max(nds[:,2])-0.0001

        btmEdge=[]
        for e in BtmBoundary: 
            ix = np.where(npn[:,0]==e[0])[0][0]; n1 = npn[ix]
            ix = np.where(npn[:,0]==e[1])[0][0]; n2 = npn[ix]
            if n1[2] > maxY and n2[2] > maxY : 
                btmEdge.append(e)
            elif n1[2] < minY and n2[2] < minY : 
                btmEdge.append(e)
        
        TopNodesToBottom =[]

        dbg = 0 
        for ed in btmEdge:
            ix1 = np.where(self.Free_Surface_without_BTM[:,7:] == ed[0])[0]
            ix2 = np.where(self.Free_Surface_without_BTM[:,7:] == ed[1])[0]
            ix = np.intersect1d(ix1, ix2)
            # if ed[3] -10**7 == 633:     
            #     print("\nBottom Edge %d (%d, %d)"%(ed[3]-10**7, ed[0]-10**7, ed[1]-10**7), "Start surf %d (F%d)"%(self.Free_Surface_without_BTM[ix[0]][0]-10**7, self.Free_Surface_without_BTM[ix[0]][1]))
            #     dbg = 1
            # else: dbg = 0 

            excluding = [ ed[0], ed[1]]
            nextSurf = self.NextFreeSurface4Node(surf=self.Free_Surface_without_BTM[ix[0]], n1=ed[0], n2=ed[1], free=self.Free_Surface_without_BTM, exclude=excluding, debug=dbg)
            otherNodes = OtherNodes_InSurface(self.Free_Surface_without_BTM[ix[0]], [ed[0], ed[1]])   
            if nextSurf != []:
                # if ed[3] -10**7 == 633: print("* NEXT: %d, F%d, %d, %d, %d, %d"%(nextSurf[0]-10**7, nextSurf[1], nextSurf[7]-10**7, nextSurf[8]-10**7, nextSurf[9]-10**7, nextSurf[10]-10**7)) 

                cnt = 0 
                while nextSurf != []:
                    # if ed[3] -10**7 == 633: print("%d(%d, %d),"%(nextSurf[0]-10**7, otherNodes[0][0]-10**7, otherNodes[1][0]-10**7), end="->")
                    nextSurf = self.NextFreeSurface4Node(nextSurf, n1=otherNodes[0][0], n2=otherNodes[1][0], free=self.Free_Surface_without_BTM, exclude=excluding, debug=dbg)
                    
                    excluding.append(otherNodes[0][0]); excluding.append(otherNodes[1][0]) 
                    if nextSurf !=[]: 
                        # if ed[3] -10**7 == 633:     print("NEXT: %d, F%d, %d, %d, %d, %d"%(nextSurf[0]-10**7, nextSurf[1], nextSurf[7]-10**7, nextSurf[8]-10**7, nextSurf[9]-10**7, nextSurf[10]-10**7)) 
                        otherNodes = OtherNodes_InSurface(nextSurf, [otherNodes[0][0], otherNodes[1][0]])

                        ix = np.where(self.freetop[:,0] == nextSurf[0])[0]
                        if len(ix) > 0 : 
                            otherNodes = OtherNodes_InSurface(nextSurf, [otherNodes[0][0], otherNodes[1][0]])
                            TopNodesToBottom.append([otherNodes[0][0], otherNodes[1][0]])
                            # if ed[3] -10**7 == 633: print("TOP NODE ", TopNodesToBottom[-1])
                            break 
                    cnt += 1
                    if cnt > 20: 
                        break 

        # print ("\nDELETE TOPEDGE ")
        HalfTDW = self.TargetTDW / 2.0 - 0.001 
        
        i = 0
        delEdges=[]
        isLug = 0 
        edgeTopSurf = []
        while i < len(Topedges): 
            j = 0
            f = 0 
            while j < len(TopNodesToBottom): 
                if TopNodesToBottom[j][0] == Topedges[i][0] or TopNodesToBottom[j][1] == Topedges[i][1] : 
                    f = 1
                    break 
                if TopNodesToBottom[j][0] == Topedges[i][1] or TopNodesToBottom[j][1] == Topedges[i][0] : 
                    f = 1
                    break 
                j += 1

            idx = np.where(self.npn[:,0]==Topedges[i][0])[0][0]; n1 = self.npn[idx]
            idx = np.where(self.npn[:,0]==Topedges[i][1])[0][0]; n2 = self.npn[idx]
            if abs(n1[2]) > HalfTDW and abs(n2[2]) > HalfTDW: 
                edgeTopSurf.append(Topedges[i])
            
            if f ==1: 
                delEdges.append(Topedges[i])
            i += 1

        Dgroups = self.Grouping_ConnectedEdges(delEdges)
        Tgroups = self.Grouping_ConnectedEdges(edgeTopSurf)

        if len(Dgroups) != len(Tgroups): 
            isLug = 1 
            edgeShoulderLug = []
            for dgrp in Dgroups:
                cnt = 0  
                for tgrp in Tgroups: 
                    for tg in tgrp:
                        brk = 0 
                        for dg in dgrp:
                            if tg[3] == dg[3]: 
                                cnt += 1
                                brk = 1 
                                break 
                        if brk ==1 : 
                            break 
                if cnt > 1: 
                    edgeShoulderLug.append(dgrp)

                        
            if len(edgeShoulderLug) > 0: 
                for grp in edgeShoulderLug: 
                    for ed in grp: 
                        i = 0
                        while i < len(Topedges) : 
                            if Topedges[i][0] == ed[0] and Topedges[i][1] == ed[1]: 
                                Topedges = np.delete(Topedges, i, axis=0)
                                break 
                            i += 1

        print (" DONE!")
        if isLug ==1: print (" Disregarding the angle of Sho. Lug Side\n")
        
        return Topedges


    def NextFreeSurface4Node(self, surf=[], n1=0, n2=0, free=[], exclude=[], debug=0): 

        """
        if a surface is not input, return the surface including the nodes 
        """
        if surf!=[]: 
            
            otherNodes = OtherNodes_InSurface(surf, [n1, n2])
            otherNodes= [otherNodes[0][0], otherNodes[1][0]]
            if debug ==1: print("A surface is input > nodes including", otherNodes)
        else: 
            otherNodes = [n1, n2]
            if debug ==1: print("No surface is input > nodes including", otherNodes)

        adf1 = np.where(free[:,7:]==otherNodes[0])[0]
        adf2 = np.where(free[:,7:]==otherNodes[1])[0]

        adf = np.intersect1d(adf1, adf2) 

        new = []
        for af in adf:
            if free[af][3] > 99: 
                f = 0 
                for ex in exclude: 
                    if free[af][7] == ex or free[af][9] == ex or free[af][9] == ex or free[af][10] == ex:  
                        f =1
                        break 
                if f == 0:  new.append(af)
        
        if debug ==1: 
            print("Searched surfaces")
            for n in new: 
                print("%d, F%d"%(free[n][0]-10**7, free[n][1]))


        if len(new) == 0: 
            return []

        if len(new) == 1: 
            if free[new[0]][0] != surf[0] or free[new[0]][1] != surf[1]: 
                return free[new[0]]
            else: 
                return []


        elif len(new) ==2: 
            if free[new[0]][0] == surf[0] and free[new[0]][1] == surf[1]: 
                if debug ==1: print("Return surface %d, F%d\n"%(free[new[1]][0], free[new[1]][1]))
                return free[new[1]]
            else: 
                if debug ==1: print("Return surface %d, F%d\n"%(free[new[0]][0], free[new[0]][1]))
                return free[new[0]]

        else: 
            print ("Too many free surfaces next %d, F%d"%(surf[0]-10**7, surf[1]), end=" :")
            for el in new:
                print("%d(f%d),  "%(free[el][0]-10**7, free[el][1]), end="")
            print("")

            return []


    def Groove_side(self, free=[], main_bottom=[], sub_bottom=[], top_surf=[], npn=[], full_depth=1, shoulderType="R"): 

        if full_depth == 1: ## for detecting sub groove bottom 
            Vrt = [0, 0, 0, -1.0]
            angles = []
            for i, sf in enumerate(free): 
                ix = np.where(npn[:,0] == sf[7])[0][0]; n1 = npn[ix] 
                ix = np.where(npn[:,0] == sf[8])[0][0]; n2 = npn[ix] 
                ix = np.where(npn[:,0] == sf[9])[0][0]; n3 = npn[ix] 
                NV = NormalVector_plane(n1, n2, n3)
                V_angle = Angle_Between_Vectors(NV, Vrt)
                angles.append(V_angle)

        boundary = self.SurfaceBoundary(main_bottom)

        main = []
        subs = []
        for bd in boundary: 
            adj_sf = 1 
            cnt = 0 
            ups=[bd[0], bd[1]]
            while adj_sf: 
                cnt += 1
                if cnt > 15: break 

                adf1 = np.where(free[:,7:]==ups[0])[0]
                adf2 = np.where(free[:,7:]==ups[1])[0]
                adf = np.intersect1d(adf1, adf2) 
                # if len(adf) ==0 : ## connected to pitch surf / sub tread bottom (if cnt > 1: top surf)
                    # print(" NO SURF> %d"%(bd[3]-10**7))
                
                if cnt > 1 and len(adf) ==1: 
                    break 

                if len(adf) > 0 : 
                    if len(adf) > 2: 
                        print ("\n## Side Surface is dividing into More than 2!!")
                        print (" > Groove bottom may be open.")
                        for en in adf: 
                            print ("  %d"%(free[en][0]-10**7), end=",")
                        print ("")
                        break 
                    elif len(adf) ==2: ## self surface and up surface 
                        # if free[adf[0]][0] == 3233+10**7 or free[adf[1]][0] == 3233+10**7 : 
                        #     print ("%d:%f, %d: %f"%(free[adf[0]][0]-10**7, free[adf[0]][6]*1000, free[adf[1]][0]-10**7, free[adf[1]][6]*1000))
                        if free[adf[0]][6] > free[adf[1]][6] : 
                            adf = [adf[0]]
                        else: 
                            adf = [adf[1]]
                        # if free[adf[0]][0] == 3245+10**7 or free[adf[0]][0] == 3233+10**7 :
                        #     print (" >> %d:%f"%(free[adf[0]][0]-10**7, free[adf[0]][6]*1000))
                    # pre = free[adf[0]]
                    main.append(free[adf[0]])
                    if free[adf[0]][2] ==4: 
                        ## it must be connected to another groove side surface 
                        ## or it can be connected to sub_bottom surface or top surface 
                        
                        upnodes = OtherNodes_InSurface(free[adf[0]], [ups[0], ups[1]])
                        ups= [upnodes[0][0], upnodes[1][0]]
                        ## does it end (connected to top?)
                        ix1 = np.where(top_surf[:,7:]==ups[0])[0]
                        ix2 = np.where(top_surf[:,7:]==ups[1])[0]
                        ix = np.intersect1d(ix1, ix2)
                        if len(ix) == 1: 
                            break 

                        ## it connects to sub_groove bottom 
                        if full_depth == 1 and len(sub_bottom) > 0: 
                            ix1 = np.where(sub_bottom[:,7:]==ups[0])[0]
                            ix2 = np.where(sub_bottom[:,7:]==ups[1])[0]
                            ix = np.intersect1d(ix1, ix2)
                            if len(ix) == 1: 
                                if angles[adf[0]] < 1.0:  ## 1.0 radian = 57.3 degrees
                                    subs.append(free[adf[0]])
                                    sub_bottom = np.append(sub_bottom, [free[adf[0]]], axis=0)
                                    main.pop()
                                break 
                        ## next loop to search another side surface 
                    else: # 3 node surface 
                        ## hypothesis : it connected another 4 node side surface 
                        # print (" 3 node Surf added %d"%(free[adf[0]][0]-10**7))
                        upnodes = OtherNodes_InSurface(free[adf[0]], [ups[0], ups[1]])
                        ix1 = np.where(free[:,7:11]==ups[0])[0]
                        ix2 = np.where(free[:,7:11]==upnodes[0][0])[0]
                        ad0 = np.intersect1d(ix1, ix2)
                        # print (free[ad0[0]][0], ">  Common NODEs %d, %d"%(ups[0]-10**7, upnodes[0][0]-10**7))
                        # if len(ad0) ==2: 
                        #     print (free[ad0[1]][0], "> Common NODEs %d, %d"%(ups[0]-10**7, upnodes[0][0]-10**7))

                        if len(ad0) == 2: 
                            if free[adf[0]][0] == free[ad0[0]][0]: ## rule out the self-surface(the same no. of element)
                                ad0=[ad0[1]]
                            else: 
                                ad0=[ad0[0]]
                        # print (free[ad0[0]][0], " <<< designated ", free[adf[0]][0])


                        ix1 = np.where(free[:,7:11]==ups[1])[0]
                        ix2 = np.where(free[:,7:11]==upnodes[0][0])[0]
                        ad1 = np.intersect1d(ix1, ix2)
                        # print (free[ad1[0]][0], ">> Common NODEs %d, %d"%(ups[1]-10**7, upnodes[0][0]-10**7))
                        # if len(ad1) ==2: 
                        #     print (free[ad1[1]][0], ">> Common NODEs %d, %d"%(ups[1]-10**7, upnodes[0][0]-10**7))
                        
                        if len(ad1) == 2: 
                            ## rule out the self-surface(the same no. of element)
                            if free[adf[0]][0] == free[ad1[0]][0]: ad1=[ad1[1]]
                            else: ad1=[ad1[0]]
                        # print (free[ad1[0]][0], " <<< designated ")


                        if len(ad0) ==1 and len(ad1) ==1: 
                            if free[ad0[0]][6] > free[ad1[0]][6] : 
                                adf = ad0 
                                commons = [ups[0], upnodes[0][0]]
                            else: 
                                adf = ad1 
                                commons = [ups[1], upnodes[0][0]]
                        elif len(ad0) == 1 : 
                            adf = ad0
                            commons = [ups[0], upnodes[0][0]]
                        elif len(ad1) == 1 : 
                            adf = ad1 
                            commons = [ups[1], upnodes[0][0]]
                        else: 
                            # print ("no connection")
                            break ## no connection.. 
                        # print (" 3NODE ADD", free[adf[0]][0]-10**7)
                        main.append(free[adf[0]]) 
                        lefts = OtherNodes_InSurface(free[adf[0]], commons)
                        ups=[lefts[0][0], lefts[1][0]]
                        # pre = free[adf[0]]
                        ## go to next loop 
                else: 
                    ## no connection to side surface (pitch end)
                    break 

        ## missing surface.. 

        for sf in main: 
            ix1 = np.where(free[:, 0]==sf[0])[0]
            ix2 = np.where(free[:, 1]==sf[1])[0]
            ix = np.intersect1d(ix1, ix2)
            if len(ix) == 1: 
                free = np.delete(free, ix[0], axis=0)
        for sf in subs: 
            ix1 = np.where(free[:, 0]==sf[0])[0]
            ix2 = np.where(free[:, 1]==sf[1])[0]
            ix = np.intersect1d(ix1, ix2)
            if len(ix) == 1: 
                free = np.delete(free, ix[0], axis=0)

        ## searching surface from top 
        main = np.array(main)
        boundary = self.SurfaceBoundary(top_surf)
        adds = []
        for bd in boundary: 
            adj_sf = 1 
            cnt = 0 
            ups=[bd[0], bd[1]]
            pre = []
            while adj_sf: 
                cnt += 1
                if cnt > 15: break 

                adf1 = np.where(free[:,7:]==ups[0])[0]
                adf2 = np.where(free[:,7:]==ups[1])[0]
                adf = np.intersect1d(adf1, adf2)
                if len(adf) ==0 or len(adf) > 2: 
                    break 
                # print (" start > %d"%(len(adf)))

                if cnt > 1 and len(adf) ==1: 
                    break 
                if len(adf) == 2: 
                    if free[adf[0]][6] < free[adf[1]][6] : 
                        adf = [adf[0]]
                    else: 
                        adf = [adf[1]]
                
                if cnt == 1:  ## check it belongs to the main groove side at the 1st loop
                    ix1 = np.where(main[:,7:]==free[adf[0]][7])[0]
                    ix2 = np.where(main[:,7:]==ups[0])[0]
                    ixa = np.intersect1d(ix1, ix2)

                    ix1 = np.where(main[:,7:]==free[adf[0]][8])[0]
                    ix2 = np.where(main[:,7:]==ups[1])[0]
                    ixb = np.intersect1d(ix1, ix2)

                    if len(ixa) == 0 or len(ixb) == 0: 
                        ix1 = np.where(main[:,7:]==free[adf[0]][7])[0]
                        ix2 = np.where(main[:,7:]==ups[1])[0]
                        ixa = np.intersect1d(ix1, ix2)

                        ix1 = np.where(main[:,7:]==free[adf[0]][8])[0]
                        ix2 = np.where(main[:,7:]==ups[0])[0]
                        ixb = np.intersect1d(ix1, ix2)
                        if len(ixa) == 0 or len(ixb) == 0: 
                            break 
               
                main = np.append(main, [free[adf[0]]], axis=0) 
                adds.append(free[adf[0]])

                downnodes = OtherNodes_InSurface(free[adf[0]], [ups[0], ups[1]])
                ups= [downnodes[0][0], downnodes[1][0]]
                # print ("add ", bd, "> ", ups, "surf %d, %d"%(free[adf[0]][0]-10**7, free[adf[0]][1]))
                pre = free[adf[0]]
                ## next loop 
                
        for sf in adds: 
            ix1 = np.where(free[:, 0]==sf[0])[0]
            ix2 = np.where(free[:, 1]==sf[1])[0]
            ix = np.intersect1d(ix1, ix2)
            if len(ix) == 1: 
                free = np.delete(free, ix[0], axis=0)
                
        if full_depth == 1: 
            return main, sub_bottom, free 
        else: 
            return main, free  

    def NodesInSurface(self, surface): 
        nds = []
        for sf in surface:
            for i in range(7, 7+int(sf[2])): 
                nds.append(sf[i])
        nds = np.array(nds)
        nds = np.unique(nds)
        
        nodes = []
        for nd in nds:
            index = np.where(self.npn[:, 0] == nd)
            nodes.append([nd, self.npn[index[0][0]][1], self.npn[index[0][0]][2], self.npn[index[0][0]][3]])
        return np.array(nodes)
    def MakeEdgesToBlockGroup(self, edges): 
        tedge =[]
        for ed in edges: 
            tedge.append(ed)
        tedge = np.array(tedge)
        blocks =[]

        while len(tedge)>0:
            block =[]
            start = tedge[0]
            tedge = np.delete(tedge, (0), axis=0)
            block.append(start)
            next = NextEdge(block[len(block) -1], tedge)
            if next == -1: continue
            block.append(tedge[next])
            while tedge[next][1] != start[0]: 
                tedge = np.delete(tedge, (next), axis=0)
                next = NextEdge(block[len(block) -1], tedge)
                if next == -1:   break
                block.append(tedge[next])
            blocks.append(block)

        return blocks 
    def SortBoundaryEdgesStartingBottom(self, edges, reverse=0): 
        ### it starts at the bottom nodes. 
        ### edges should be closed. 
        xy = self.GlobalXY
        x = int(xy/10)
        y = int(xy%10)
        margin = 1.0E-04
        
        main = 0 
        bottom_edge = []
        for i, ied in enumerate(edges): 
            N1 = self.npn[np.where(self.npn[:,0] == ied[0])[0][0]]
            N2 = self.npn[np.where(self.npn[:,0] == ied[1])[0][0]]
            for j, jed in enumerate(edges): 
                if i == j : continue
                main1 = 0; main2 = 0
                N01 = self.npn[np.where(self.npn[:,0] == jed[0])[0][0]]
                N02 = self.npn[np.where(self.npn[:,0] == jed[1])[0][0]]
                if (abs(N1[y]+self.pitchlength - N02[y]) <margin and abs(N1[x] - N02[x]) <margin):     main1 = 1
                if (abs(N2[y]+self.pitchlength - N01[y]) <margin and abs(N2[x] - N01[x]) <margin):     main2 = 1
                if main1 * main2 == 1: 
                    main =1 
                    bottom_edge.append(ied)
                    break 

        grooves = 0 
        cnt = 0 
        Gedges=[] 
        while len(bottom_edge)>0: 
            tmp =[]
            iedge = bottom_edge[0]
            edge0=iedge
            tmp.append(iedge)
            del(bottom_edge[0]) 
            idx = NextEdge(iedge, bottom_edge)
            
            while idx >=0:
                iedge = bottom_edge[idx]
                del(bottom_edge[idx]) 
                tmp.append(iedge)
                idx = NextEdge(iedge, bottom_edge)
                cnt +=1

            idx = PreviousEdge(edge0, bottom_edge)
            while idx >=0: 
                iedge = bottom_edge[idx]
                tmp.append(iedge)
                del(bottom_edge[idx]) 
                idx = PreviousEdge(iedge, bottom_edge)
                cnt +=1
            Gedges.append(tmp)
            grooves +=1
            cnt +=1
            if cnt > 10000: 
                print ("Too many interations to discriminate the main grooves")
                print ("residual edegs %d"%(len(bottom_edge)))
                break 

        # print ("** Grooves in Boundary Edges = %d"%(grooves))
        # if grooves > 0: print ("* Main Groove Found")

        if grooves < 2: 

            startedge = 0 
            nedges = []
            min = 1000.0
            for i, ed in enumerate(edges): 
                N2 = self.npn[np.where(self.npn[:,0] == ed[0])[0][0]]
                N1 = self.npn[np.where(self.npn[:,0] == ed[1])[0][0]] 
                if main == 1: 
                    for sedge in edges: 
                        btm1 = 0 
                        N00 = self.npn[np.where(self.npn[:,0] == sedge[0])[0][0]]
                        if abs(N2[y]+self.pitchlength - N00[y]) <margin and abs(N2[x] - N00[x]) < margin : 
                            btm1 = 1
                        if btm1 == 1: 
                            btm2 = 0
                            for sedge in edges: 
                                N0 = self.npn[np.where(self.npn[:,0] == sedge[0])[0][0]] 
                                if abs(N1[y]+self.pitchlength - N0[y]) <margin and abs(N1[x] - N0[x]) < margin : 
                                    btm2 = 1
                                    break
                            if btm2 == 0: 
                                startedge = i
                                break 

                else: 
                    if N1[y] < min: 
                        min = N1[y]
                        startedge = i
                
                nedges.append([ed[0], ed[1], main, ed[3], N1[1], N1[2], N1[3], N2[1], N2[2], N2[3], -1])
            
            nedges[startedge][10]=0
            current = nedges[startedge]
            sortededge = []
            sortededge.append(current)
            i = 0
            if reverse == 0 and main ==1: 
                startnode = nedges[startedge][0]
                while current[1] != startnode: 
                    idx = NextEdge(current, edges)
                    current = nedges[idx] 
                    current[10]=i+1
                    sortededge.append(current)
                    # print (current[0], current[1])
                    i+=1
                    if i>100000: 
                        print ("Too many iteration to sort edges (over 100_000 times)")
                        break
            else:
                startnode = nedges[startedge][1]
                while current[0] != startnode: 
                    idx = PreviousEdge(current, edges)
                    current = nedges[idx] 
                    current[10]=i+1
                    sortededge.append(current)
                    i+=1
                    if i>100000: 
                        print ("Too many iteration to sort edges (over 100_000 times)")
                        break
            # self.ImageEdge(sortededge, file=Pattern.name+"-groove_edges01" , point=1, color='black')
            return np.array(sortededge), grooves 
        else: 
            XRanges=[]
            for ged in Gedges:
                Yl=10000.0
                Yr=-10000.0
                for ed in ged: 
                    N1 = NodeCoordinates(ed[0], self.npn)
                    N2 = NodeCoordinates(ed[1], self.npn)
                    if N1[x] > Yr: Yr=N1[x]
                    if N1[x] < Yl: Yl=N1[x]
                    if N2[x] > Yr: Yr=N2[x]
                    if N2[x] < Yl: Yl=N2[x]
                XRanges.append([Yl, Yr])

            ## sorting 
            Sorted =[]
            for i, xf in enumerate(XRanges): 
                Sorted.append(xf)
                if i == 0: continue
                else: 
                    I = len(Sorted)
                    for j, xs in enumerate(Sorted): 
                        if xs[0] > xf[0]: 
                            del(Sorted[I-1])
                            Sorted.insert(j, xf)
                            I = j
                            break 
            for i, xf in enumerate(Sorted): 
                XRanges[i] = xf
            del(Sorted)
            # print ("Sorted Main Groove Ranges", XRanges)

            Divided_Grooves = []
            for i in range(grooves): 
                divided = []
                if i ==0: 
                    xlimit = (XRanges[0][1] + XRanges[1][0])/2.0 
                    for ed in edges: 
                        N1 = NodeCoordinates(ed[0], self.npn) 
                        if N1[x] <= xlimit: 
                            divided.append(ed)
                elif i == grooves-1: 
                    xlimit = (XRanges[grooves-2][1] + XRanges[grooves-1][0])/2.0 
                    for ed in edges: 
                        N1 = NodeCoordinates(ed[0], self.npn)
                        if N1[x] >= xlimit: 
                            divided.append(ed)
                else: 
                    xlimit1 =  (XRanges[i-1][1] + XRanges[i][0])/2.0 
                    xlimit2 =  (XRanges[i][1] + XRanges[i+1][0])/2.0 
                    for ed in edges: 
                        N1 = NodeCoordinates(ed[0], self.npn)
                        if N1[x] >=xlimit1 and N1[x] <= xlimit2: 
                            divided.append(ed)

                main = 1

                startedge = 0 
                nedges = []
                min = 1000.0
                for i, ed in enumerate(divided): 
                    N2 = self.npn[np.where(self.npn[:,0] == ed[0])[0][0]]
                    N1 = self.npn[np.where(self.npn[:,0] == ed[1])[0][0]] 

                    for sedge in edges: 
                        btm1 = 0 
                        N00 = self.npn[np.where(self.npn[:,0] == sedge[0])[0][0]]
                        if abs(N2[y]+self.pitchlength - N00[y]) <margin and abs(N2[x] - N00[x]) < margin : 
                            btm1 = 1
                        if btm1 == 1: 
                            btm2 = 0
                            for sedge in edges: 
                                N0 = self.npn[np.where(self.npn[:,0] == sedge[0])[0][0]] 
                                if abs(N1[y]+self.pitchlength - N0[y]) <margin and abs(N1[x] - N0[x]) < margin : 
                                    btm2 = 1
                                    break
                            if btm2 == 0: 
                                startedge = i
                                break

                    nedges.append([ed[0], ed[1], main, ed[3], N1[1], N1[2], N1[3], N2[1], N2[2], N2[3], -1])
                
                nedges[startedge][10]=0
                current = nedges[startedge]
                sortededge = []
                sortededge.append(current)
                i = 0
                startnode = nedges[startedge][0]
                while current[1] != startnode: 
                    idx = NextEdge(current, nedges)
                    if idx ==-1: 
                        mdist = 1.0E15
                        for ced in nedges: 
                            already = 0 
                            for dge in sortededge: 
                                if dge[0] == ced[0] or dge[1] == ced[0]: 
                                    already =1 
                                    break 
                            if already ==1: 
                                continue 

                            dist = (ced[4]-current[7])*(ced[4]-current[7]) + (ced[5]-current[8])*(ced[5]-current[8]) + (ced[6]-current[9])*(ced[6]-current[9])  

                            # print (ced[0], ced[1], dist*1000, mdist*1000)
                            if dist < mdist: 
                                mdist = dist
                                tedge = [current[1], ced[0], main, current[3], current[7],current[8],current[9], ced[4], ced[5], ced[6], -1] 
                        
                        # print ("Main Groove Searching (dividing edges) : Edge (%d-%d) is connected width (%d-%d)"%(current[0], current[1], tedge[0], tedge[1]))
                        current = tedge 
                    else: 
                        current = nedges[idx] 
                    
                    current[10]=i+1
                    sortededge.append(current)
                    i+=1
                    if i>100000: 
                        print ("Too many iteration to sort edges (over 100_000 times)")
                        break

                Divided_Grooves.append(sortededge)
            return Divided_Grooves, grooves     
    def TrimmingLateralGroove(self, edges, groovebottom): 

        x=int(self.GlobalXY/10); y=int(self.GlobalXY%10)
        margin = 1.0E-04
        N = len(edges)

        accum=[]
        counts=[]
        edgesideL=[]
        edgestart=edges[0] 

        idx = np.where(self.npn[:, 0] == edges[0][0])[0][0]
        N1 = self.npn[idx]

        
        
        # print ("SIDE EDGE INPUT", edges[0][0], edges[0][1])
        inext= 0
        for i, edge in enumerate(edges): 
            idx = np.where(self.npn[:, 0] == edge[0])[0][0]
            N0 = self.npn[idx]
            # print (f"{edge[0]}, {edge[1]} : Del Y={abs(N0[y] -self.pitchlength -N1[y])*1000}, Del X={abs(N0[x] - N1[x])*1000}")
            if i!=0: 
                if abs(N0[y] -self.pitchlength -N1[y]) < margin and abs(N0[x] - N1[x]) < margin: 
                    inext = i
                    # print (f"End of left side edge : {i}th edge")
                    break 
            edgesideL.append(edge)
            accum.append(edge)

        for i, iedge in enumerate(edgesideL):
            cnt = 0
            for j, jedge in enumerate(edgesideL): 
                if i ==j: continue
                if iedge[3] == jedge[3]: cnt+=1

            counts.append(cnt)

        # print ("TOP EDGE INPUT")
        edgetop=[]
        for i in range(inext, N): 
            idx = np.where(self.npn[:, 0] == edges[i][1])[0][0]
            N1 = self.npn[idx]
            
            itop = 0 
            for edge in edges:
                idx = np.where(self.npn[:, 0] == edge[1])[0][0]
                N0 = self.npn[idx] 
                if abs(N0[y] + self.pitchlength - N1[y]) < margin and abs(N0[x] - N1[x]) < margin: 
                    itop = 1
                    break
            if itop ==1: 
                edges[i][10] = -100 
                # print (" TOP EDGE : ", edges[i][0], edges[i][1], edges[i][10])
                edgetop.append(edges[i])
                accum.append(edges[i])
                counts.append(0)
            else: 
                inext = i
                break 

        pcnt = inext 
        edgesideR=[]
        idx = np.where(self.npn[:, 0] == edges[inext][0])[0][0]
        N1 = self.npn[idx]
        for i in range(inext, N): 
            if i == inext : 
                edgesideR.append(edges[i])
                # print (" * Right side Edge : ", edges[i][0], edges[i][1], edges[i][10])
                continue 
            else: 
                idx = np.where(self.npn[:, 0] == edges[i][0])[0][0]
                N0 = self.npn[idx]
                itop = 0 
                if abs(N0[y] + self.pitchlength - N1[y]) < margin and abs(N0[x] - N1[x]) < margin: 
                    itop = 1
                    # print (f"itop={itop},  {edges[i][0]}, {edges[i][1]}")
                if itop !=1: 
                    # print (f" ** Right side Edge {edges[i][0]}, {edges[i][1]} : Del Y={abs(N0[y] +self.pitchlength -N1[y])*1000}, Del X={abs(N0[x] - N1[x])*1000}")
                    edgesideR.append(edges[i])
                else: 
                    inext = i
                    break 


        for i, iedge in enumerate(edgesideR):
            cnt = 0
            for j, jedge in enumerate(edgesideR): 
                if i ==j: continue
                if iedge[3] == jedge[3]: cnt+=1
            accum.append(edges[i+pcnt])
            counts.append(cnt)

        edgebtm=[]
        for i in range(inext, N): 
            if edges[i][0] != edgestart[0]: 
                edges[i][10] = -100 
                edgebtm.append(edges[i])
                accum.append(edges[i])
                counts.append(0)
                # print (" Bottom EDGE : ", edges[i][0], edges[i][1], edges[i][10])

        Trimmed=[]
        TN = len(edges)
        bottomedges = AllEdgesInSurface(groovebottom, self.npn)

        i = -1
        counting =0 
        Lateral_element_1 = 0 
        One_element_mode = 0
        while i < TN-1: 
            i += 1
            # if len(Trimmed) > TN :                 break 
            # if i %5 ==0:    print ("TN=%d, i=%d, len_trimmed=%d"%(TN, i, len(Trimmed)))
            if i ==0: 
                if edges[i][3] == edges[TN-1][3]: 
                    Trimmed.append(edges[i])
                else: 
                    # print ("i=%d, edge"%(i), edges[TN-1])
                    up = self.FindAnotherEdgeInSurface(next=2, cedge=edges[TN-1], edges=bottomedges, surfaces=groovebottom)
                    # print ("      up edge", up)
                    ctedge = self.FindContactingEdge(up, bottomedges)
                    # print ("       ct edge", up)

                    upnode =[]
                    upsurf = np.where(groovebottom[:, 0] == ctedge[3])[0][0]
                    upsurf = groovebottom[upsurf]
                    un = int(upsurf[2])
                    for j in range(7, 7+un): 
                        upnode.append(upsurf[j])
                    
                    cnode = []
                    cnsurf = np.where(groovebottom[:, 0] == edges[i][3])[0][0]
                    cnsurf = groovebottom[cnsurf]
                    cn = int(cnsurf[2])
                    for j in range(7, 7+cn): 
                        cnode.append(cnsurf[j])
                    cnt = 0
                    for c in cnode: 
                        for u in upnode: 
                            if c == u: cnt +=1
                    if cnt == 2: 
                        Trimmed.append(edges[i])
                        continue 
                    else: 
                        # print (" next edge start")
                        tedge = self.FindAnotherEdgeInSurface(next=1, cedge=edges[TN-1], edges=bottomedges, surfaces=groovebottom)
                        # print (" end next edge")
                        Trimmed.append(tedge)

                        lateralend =0
                        cnt =0
                        while lateralend ==0: 
                            cnt += 1
                            if cnt > 10: 
                                print ("Error to find next edge in the lateral groove at the beginning")
                                break 

                            for j, edge in enumerate(edges): 
                                if j ==0: continue
                                if edge[0] == tedge[1]: 
                                    i =j
                                    lateralend =1 
                                    break
                            if lateralend ==1: 
                                Trimmed.append(edges[i])
                                continue
                            else: 
                                ctedge = self.FindContactingEdge(tedge, bottomedges)
                                ref_edge = self.FindAnotherEdgeInSurface(next=-1, cedge=ctedge, edges=bottomedges, surfaces=groovebottom)
                                tedge, ref_edge = self.ExtendMainGrooveEdge_InlateralGroove(tedge, ref_edge, bottomedges, groovebottom)

                            

                        continue 

            elif edges[i-1][10] == -100 and edges[i][10] != -100: 

                if edges[i][3] == edges[i-1][3]: 
                    Trimmed.append(edges[i])
                    # print ("1. Trimmed", edges[i][3]-10**7)
                else: 
                    down = self.FindAnotherEdgeInSurface(next=2, cedge=edges[i-1], edges=bottomedges, surfaces=groovebottom)
                    ctedge = self.FindContactingEdge(down, bottomedges)

                    downnode =[]
                    downsurf = np.where(groovebottom[:, 0] == ctedge[3])[0][0]
                    downsurf = groovebottom[downsurf]
                    un = int(downsurf[2])
                    for j in range(7, 7+un): 
                        downnode.append(downsurf[j])
                    
                    cnode = []
                    cnsurf = np.where(groovebottom[:, 0] == edges[i][3])[0][0]
                    cnsurf = groovebottom[cnsurf]
                    cn = int(cnsurf[2])
                    for j in range(7, 7+cn): 
                        cnode.append(cnsurf[j])
                    cnt = 0
                    for c in cnode: 
                        for u in downnode: 
                            if c == u: cnt +=1
                    if cnt == 2: 
                        Trimmed.append(edges[i])
                        # print ("2. Trimmed", edges[i][3]-10**7)
                        continue 
                        ######################################################################################
                    else: 
                        # print (")))))))))", edges[i-1][3]-10**7, ", ", edges[i-1][0]-10**7, ", ", edges[i-1][1]-10**7)
                        # print (" ... ", Trimmed[len(Trimmed)-1][3]-10**7,  Trimmed[len(Trimmed)-1][0]-10**7,  Trimmed[len(Trimmed)-1][1]-10**7)
                        ## Initial formula ## 
                        ## but sometimes it outputs not-boundary-edge 
                        # tedge = self.FindAnotherEdgeInSurface(next=1, cedge=edges[i-1], edges=bottomedges, surfaces=groovebottom)
                        # Trimmed.append(tedge)
                        # print ("3. Trimmed", tedge[3]-10**7, ", ", tedge[0]-10**7, ", ",tedge[1]-10**7)

                        ## search next edge only among boundary edges 
                        for j, e in enumerate(edges): 
                            if e[0] == edges[i-1][1]: 
                                Trimmed.append(e) 
                                # print ("3. Trimmed", e[3]-10**7, ", ", e[0]-10**7, ", ",e[1]-10**7)
                                i = j 
                                tedge = e 
                                break 





                        lateralend =0
                        cnt =0
                        while lateralend ==0: 
                            cnt += 1
                            if cnt > 10: 
                                print ("Error to find next edge in the lateral groove at the beginning")
                                break 
                            for j, edge in enumerate(edges): 
                                if j ==0 : continue
                                if edge[0] == tedge[1]: 
                                    i =j
                                    lateralend =1 
                                    break
                            if lateralend ==1: 
                                Trimmed.append(edges[i])
                                # print ("** 4. Trimmed", edges[i][3]-10**7, ", ", edges[i][0]-10**7, ", ", edges[i][1]-10**7)
                                continue
                            else: 
                                ctedge = self.FindContactingEdge(tedge, bottomedges)
                                ref_edge = self.FindAnotherEdgeInSurface(next=-1, cedge=ctedge, edges=bottomedges, surfaces=groovebottom)
                                tedge, ref_edge = self.ExtendMainGrooveEdge_InlateralGroove(tedge, ref_edge, bottomedges, groovebottom)

                            

                        # continue 

            elif edges[i][10] == -100 :          
                Trimmed.append(edges[i])
                # print ("5. Trimmed", edges[i][3]-10**7)
                if len(Trimmed) > TN :                 break 
            elif edges[i-1][3] == edges[i][3]:         
                Trimmed.append(edges[i])
                # print ("6. Trimmed", edges[i][3]-10**7)
            else:
                pidx = np.where(groovebottom[:, 0] == edges[i-1][3])
                cidx = np.where(groovebottom[:, 0] == edges[i][3])

                if len(pidx[0]) !=1 or len(cidx[0]) !=1: 
                    print ("ERROR! Too many surfaces to find next groove edge (All should be 1 ) : %d / %d"%(len(pidx[0]), len(cidx[0])))
                    sys.exit()
                
                pnodes =[]; cnodes=[]
                pn = int(groovebottom[pidx[0][0]][2])
                cn = int(groovebottom[cidx[0][0]][2])
                for j in range(7, 7+pn): 
                    pnodes.append(groovebottom[pidx[0][0]][j])
                for j in range(7, 7+cn): 
                    cnodes.append(groovebottom[cidx[0][0]][j])
                
                howmany = 0
                for p in pnodes: 
                    for c in cnodes: 
                        if p == c: howmany+=1
                if howmany ==2 : 
                    cN = len(Trimmed)
                    if edges[i][0] != edges[cN-1][1]: 
                        k = i
                        
                        chnode = Trimmed[cN-1][1]
                        while edges[k][0] != chnode: 
                            k -= 1
                            Trimmed.append(edges[k])
                            # print ("7. Trimmed", edges[k][3]-10**7)
                            if k <1: 
                                print ("ERROR, NO EDGE between Edges")
                                break 
                                
                            
                    Trimmed.append(edges[i])
                    # print ("8. Trimmed", edges[i][3]-10**7)
                else:  ## howmany ==1 

                    counting +=1  
                    if counting > 50:  ## in case of infinite loop 
                        # self.ImageEdge(Trimmed, file=Pattern.name+"-ERROR Tri Rec Element", nid=1, dpi=400, tsize=3)
                        # sys.exit()
                        print (" Infinite loop to trim lateral grv from main")
                        break 

                    ## ######################################################################################
                    ##  triangular element between edges[i] and edges[i-1]
                    ##  
                    wdx = np.where(groovebottom[:, 7:] == edges[i-1][1]) 
                    wdx = wdx[0]
                    
                    pwdx = []
                    triangular = 0
                    for ix in wdx: 
                        if groovebottom[ix][0] != edges[i][3] and groovebottom[ix][0] != edges[i-1][3]: 
                            wdx = ix 
                            pwdx.append(ix)
                            if groovebottom[ix][2] == 3: triangular += 1
                    ###########################################################################
                    ## temporary for : meshfile = cwd + "\H436B\\H436B_225-45R18H.ptn"    ##  there is an error when trimming 1 groove 
                    ###########################################################################  
                    if len(pwdx) >1 and triangular >= 2: 
                        Trimmed.append(edges[i])
                        # print ("9. Trimmed", edges[i][3]-10**7)
                        continue 
                    ##################################################### end -  meshfile = cwd + "\H436B\\H436B_225-45R18H.ptn"  
                    wnodes =[]
                    try: 
                        wn = int(groovebottom[wdx][2])
                    except:
                        print (wdx)
                        print (f" edge i   : {edges[i][0]}, {edges[i][1]}")
                        print (f" edge i-1 : {edges[i-1][0]}, {edges[i-1][1]}")
                        for ix in wdx: 
                            print (f" : {groovebottom[ix][7]}, {groovebottom[ix][8]}, {groovebottom[ix][9]}, {groovebottom[ix][10]}")
                            self.ImageEdge(Trimmed, file=Pattern.name+"-ERROR Tri Rec Element", nid=1, dpi=400)
                            sys.exit()
                    if wn ==3 : 
                        for j in range(7, 7+wn): 
                            wnodes.append(groovebottom[wdx][j])
                        
                        howmany01 = 0; howmany02=0
                        for p in pnodes: 
                            for w in wnodes: 
                                if p == w: howmany01+=1
                        for c in cnodes: 
                            for w in wnodes: 
                                if c == w: howmany02+=1

                        if howmany01 ==2 and howmany02 == 2: 
                            Trimmed.append(edges[i])
                            # print ("10. Trimmed", edges[i][3]-10**7)
                            continue 
                    ## ######################################################################################
                    ##  Rectangular element between edges[i] and edges[i-1]
                    ##
                    elif wn ==4 : 
                        rdx = np.where(groovebottom[:,0] == edges[i-1][3])[0][0]   ## element 'a'
                        for j in range(7, 11 ): 
                            if edges[i-1][1] == groovebottom[rdx][j]: 
                                mch = j 
                        
                        if mch !=10: 
                            nd = groovebottom[rdx][mch+1]
                        else: 
                            nd = groovebottom[rdx][7]
                        
                        rdx = np.where(groovebottom[:, 7:]==nd)[0]

                        if len(rdx) == 3: 
                            if counts[i] ==0: 
                                Trimmed.append(edges[i])
                                # print ("11. Trimmed", edges[i][3]-10**7)
                                continue 
                            else: 
                                tedge, ref_edge = self.ExtendMainGrooveEdge_InlateralGroove(edges[i-1], edges[i], bottomedges, groovebottom)
                                Trimmed.append(tedge) 
                                # print ("12. Trimmed",tedge[3]-10**7)
                                for j, edge in enumerate(edges): 
                                    if edge[0] == ref_edge[0] and edge[1] == ref_edge[1]: 
                                        i =j
                                        break
                                Trimmed.append(edges[i+1])
                                # print ("13. Trimmed", edges[i+1][3]-10**7)
                                continue
                        else: 
                            ddx = np.where(groovebottom[:,0] == edges[i][3])[0][0]    ## element 'd' 
                            for j in range(7, 11): 
                                if edges[i][0] == groovebottom[ddx][j]: 
                                    mch = j 
                            
                            if mch !=7: 
                                nd = groovebottom[ddx][mch-1]
                            else: 
                                nd = groovebottom[ddx][10]
                            
                            ddx = np.where(groovebottom[:, 7:]==nd)[0]
                            if len(ddx) == 3: 
                                
                                for dx in ddx: 
                                    if groovebottom[dx][0] == edges[i][3]: d_el = dx 
                                    else: 
                                        cel = 1 
                                        for j in range(7, 11): 
                                            if groovebottom[dx][j] == edges[i][0]: 
                                                b_el = dx 
                                                cel  = 0 
                                        if cel ==1: 
                                            c_el = dx 
                                bnd=[]; cnd=[]; dnd=[]
                                for j in range(7, 11): 
                                    bnd.append(groovebottom[b_el][j])
                                    cnd.append(groovebottom[c_el][j])
                                    dnd.append(groovebottom[d_el][j])
                                bmc =0; cmc =0
                                for d in dnd: 
                                    for b in bnd: 
                                        if b==d: bmc +=1
                                    for c in cnd: 
                                        if c ==d: cmc +=1

                                if cmc ==2 and bmc ==2: 
                                    cN = len(Trimmed)
                                    if edges[i][0] != edges[cN-1][1]: 
                                        k = i
                                        
                                        chnode = Trimmed[cN-1][1]
                                        while edges[k][0] != chnode: 
                                            k -= 1
                                            Trimmed.append(edges[k])
                                            # print ("14. Trimmed", edges[k][3]-10**7)
                                            if k <1: 
                                                print ("ERROR, NO EDGE between Edges")
                                                sys.exit() 
                                    
                                    Trimmed.append(edges[i])
                                    # print ("15. Trimmed", edges[i][3]-10**7)
                                    continue 

                    ## ######################################################################################
                    ## in case there are more than 2 elements in lateral groove 
                    ## ######################################################################################
                    wedge = 0
                    if counts[i] == 0: 
                        for j in range(i, TN-1): 
                            pdx = np.where(groovebottom[:, 0] == edges[j][3])
                            cdx = np.where(groovebottom[:, 0] == edges[j+1][3])
                            pnds =[]; cnds=[]
                            ps = int(groovebottom[pdx[0][0]][2])
                            cs = int(groovebottom[cdx[0][0]][2])
                            for k in range(7, 7+ps): 
                                pnds.append(groovebottom[pdx[0][0]][k])
                            for k in range(7, 7+cs): 
                                cnds.append(groovebottom[cdx[0][0]][k])

                            howmany = 0
                            for p in pnds: 
                                for c in cnds: 
                                    if p == c: howmany+=1

                            ## if counts[j] > 1 comes early, it is edge in the lateral groove
                            ## if howmany ==1 or top or botm edge comes early, it is in the main groove 
                            if edges[i][3] == edges[i+1][3] : 
                                wedge = 0 
                                break 
                            if counts[j] > 0 : 
                                break 
                            if howmany == 1 or edges[j][10] == -100: 
                                wedge =1 
                                break

                    if wedge == 1: 
                        continue 
                    else: 
                        tedge, ref_edge = self.ExtendMainGrooveEdge_InlateralGroove(edges[i-1], edges[i], bottomedges, groovebottom)
                        Trimmed.append(tedge) 
                        # print ("16. Trimmed", tedge[3]-10**7)

                        exist = 0   ## check if the node is input already (if it's already input, it cannot be the next node (next edge))
                        counting =0 
                        while exist ==0: 
                            for edge in edges: 
                                if edge[0] == ref_edge[0] and edge[1] == ref_edge[1]: 
                                    exist =1
                                    break
                            if exist ==1: 
                                continue
                            else: 
                                tedge, ref_edge = self.ExtendMainGrooveEdge_InlateralGroove(tedge, ref_edge, bottomedges, groovebottom)
                                Trimmed.append([tedge])
                                # print ("17. Trimmed", tedge[3]-10**7)
                                if counts[i]>1:   print ("exist == 0 : ", tedge[0], tedge[1])
                            
                            counting +=1
                            if counting > 10: 
                                self.ImageEdge(Trimmed, file=Pattern.name+"-ERROR Loop extend main groove", edge1=[tedge], edge2=[ref_edge], nid=1)#, dpi=800, tsize=2)
                                sys.exit()

                        for j, edge in enumerate(edges): 
                            if edge[0] == ref_edge[0] and edge[1] == ref_edge[1]: 
                                i =j
                                break
                        Trimmed.append(edges[i+1])
                        # print ("18. Trimmed", edges[i+1][3]-10**7)
                        if edges[i][1] == edgestart[0]: break 

                if edges[i][1] == edges[0][0]: break
        
        # print ("OUT")

        i = 0
        while i < len(Trimmed): 
            # if i %100 ==0:    print ("T Edge=%d, i=%d"%(len(Trimmed), i))
            j = i+1
            for k in range(j, len(Trimmed)): 
                if Trimmed[i][0] == Trimmed[k][0] and Trimmed[i][1] == Trimmed[k][1]: 
                    Trimmed = np.delete(Trimmed, k, axis=0)
                    i -= 1
                    break 
            i += 1
        # print ("Trimmed")
        gmin = 1.0E10
        gmax = -1.0E10 

        for edge in Trimmed: 
            idx = np.where(self.npn[:, 0] == edge[0])[0][0]
            if self.npn[idx][2] < gmin: gmin = self.npn[idx][2]
            if self.npn[idx][2] > gmax: gmax = self.npn[idx][2]

        return Trimmed, round((gmax+gmin)/2.0, 8)
    def PatternScalingSquare(self, ModelGD=0.0, TargetGD=0.0, ModelPL=0.0, NoPitch=0,  ModelTDW=0, TargetTDW=0, \
         TargetOD=0.0, center=[], ModelOD=0.0, t3dm=0, orgn=[], surf_btm=[]):
        if NoPitch ==0: 
            # print ("No_Pitch=%d,  TargetTDW=%.3f, ModelTDW=%.3f, ModelPL=%.3f"%(NoPitch, TargetTDW*1000, ModelTDW*1000, ModelPL*1000))
            if TargetTDW ==0: TargetTDW = ModelTDW 

            RecommendedPL = TargetTDW / ModelTDW * ModelPL
            PN = TargetOD * self.PI / RecommendedPL
            NoPitch = round(PN, 0)
            try: 
                self.TargetPL = TargetOD * self.PI / NoPitch
            except: 
                print ("No_Pitch=%d, PN=%.3f, TargetTDW=%.3f, ModelTDW=%.3f, ModelPL=%.3f, Recommend PL=%.3f"%(NoPitch, PN, TargetTDW*1000, ModelTDW*1000, ModelPL*1000, RecommendedPL*1000))
                print (" ERROR No Pitch=%d"%(NoPitch))
                sys.exit()
            PitchLengthInfo = "* No. of Pitches= %.4f -> %d\n* Pitch Length=%.3f (Model=%.3f)"%(PN, NoPitch,  self.TargetPL*1000, ModelPL*1000)
            # PitchLengthInfo = "** Auto-Calculated the Number of Pitches= %.4f -> %d, Pitch Length=%.3f (Model=%.3f)"%(PN, NoPitch,  self.TargetPL*1000, ModelPL*1000)
        else: 
            self.TargetPL = TargetOD * self.PI / NoPitch
            PitchLengthInfo = "* No. of Pitches=%d\n* Pitch Length=%.3f (Model=%.3f)"%(NoPitch, self.TargetPL*1000, ModelPL*1000)
            # PitchLengthInfo = "** User Input the number of Pitches=%d, Pitch Length=%.3f  (Model=%.3f)"%(NoPitch, self.TargetPL*1000, ModelPL*1000)

        if TargetTDW == 0 : TargetTDW = ModelTDW
        self.NoPitch = NoPitch 

        if len(center) ==0:  center = [0, 0.0, 0.0, round(ModelOD /2.0, 9)]
        
        #####################################################################
        Ratio_PL =  self.TargetPL/ModelPL
        
        if TargetTDW > 0.0 :        Ratio_TW = TargetTDW / ModelTDW
        else:                       Ratio_TW = 1.0 

        if TargetGD > 1.0E-03 and ModelGD > 1.0E-03:       Ratio_GD = TargetGD / ModelGD 
        else:                                      Ratio_GD =  1.0

        if ModelOD == 0: 
            mz = -10.0
            for n in self.npn: 
                if n[3] > mz: mz = n[3]
            Shift_Z = round((TargetOD - mz*2) / 2.0, 9) 
        else: 
            Shift_Z = round((TargetOD - ModelOD) / 2.0, 9) 

        if t3dm == 1: 
            print ("* T3DM Mode ")
            Ratio_TW = 1.0
            Ratio_GD = 1.0 
            Shift_Z = 0.0
        else: 
            print ("* Expansion Mode ")
        # print (  "********************************************")

        print ("* OD: Model=%7.1f, Target=%5.1f, Shift=%6.1f"%(ModelOD*1000, TargetOD*1000, Shift_Z*1000))
        # if ModelGD > 1.0: print ("** Model GD=%7.2f, Target GD=%5.2f"%(ModelGD, TargetGD))
        print ("* GD: Model=%7.2f, Target=%5.2f"%(ModelGD*1000, TargetGD*1000))
        print (PitchLengthInfo)
        # print ("* PL: Model=%7.2f, Target=%7.2f"%(ModelPL*1000, self.TargetPL*1000))
        
        print ("\n* Scaling Ratio\n  PL=%6.3f, TW=%6.3f, GD=%6.2f"%(Ratio_PL, Ratio_TW, Ratio_GD))
        print ("\n* Profile TDW=%7.2f"%(TargetTDW*1000))
        print (  "* Pattern TDW=%7.2f"%(ModelTDW*1000))
        print (  "* Scaled  TDW=%7.2f"%((ModelTDW*Ratio_TW*1000)))
        
        NodeOrigin = [] 
        for i, nd in enumerate(self.npn): 
            NodeOrigin.append([nd[0], nd[1], nd[2], nd[3]])
        NodeOrigin = np.array(NodeOrigin)

        NewNode=[]       
        ModelHD =  ModelOD/2.0
        design_nodes=[]
        HalfWidth =  ModelTDW / 2.0
        if t3dm == 0 : 
            for i, nd in enumerate(self.npn): 
                # if nd[0] -10**7 == 749 or nd[0] -10**7 == 748 or nd[0] -10**7 == 858 or nd[0] -10**7 == 852: 
                #     print ("%5d, %.5f, %.5f, %.5f"%(nd[0]-10**7, nd[1], nd[2], nd[3]), end=", ")
                NZ =  ModelHD - (ModelHD - nd[3]) * Ratio_GD + Shift_Z
                NY = nd[2] * Ratio_TW 
                # if nd[0] -10**7 == 749 or nd[0] -10**7 == 748 or nd[0] -10**7 == 858 or nd[0] -10**7 == 852:  print ("y, %.5f, del Y, %.5f, ratio=%.3f"%(NY , NY-nd[2], NY/nd[2]))
                design_nodes.append(NY)
                NX = nd[1] * Ratio_PL 
                NewNode.append([nd[0], NX, NY, NZ])
                # if nd[0] -10**7 == 749 or nd[0] -10**7 == 748 or nd[0] -10**7 == 858 or nd[0] -10**7 == 852: 
                #     print ("%5d, %.5f, %.5f, %.5f"%(nd[0]-10**7, NX, NY, NZ))
        else: 
            for i, nd in enumerate(self.npn): 
                # if nd[0] == 10002896 or nd[0] == 10002934 or nd[0] == 10003048: print (nd[0]-10**7, round(nd[1]*1000, 5),  round(nd[2]*1000, 5),  round(nd[3]*1000, 5))
                NZ =  ModelHD - (ModelHD - nd[3]) * Ratio_GD + Shift_Z
                NX = (nd[1]) * Ratio_PL 
                NY = nd[2]
                NewNode.append([nd[0], NX, NY, NZ])

        NewNode = np.array(NewNode)

        ############################################################################
        ## block angle adjusting 
        ############################################################################
        # step 0 : generating beam element for replacing beam element to bottom edges 
      
        ## search the left bottom node (edge)
        digit=6
        edge_base_boundary =  self.SurfaceBoundary(surf_btm)

        sfn = []
        sfedge = []
        for dn in edge_base_boundary: 
            ix = np.where(orgn[:,0] == dn[0])[0][0]; n1 = orgn[ix]
            sfn.append(orgn[ix])
            ix = np.where(orgn[:,0] == dn[1])[0][0]; n2 = orgn[ix]
            sfn.append(orgn[ix])
            sfedge.append([dn[0], dn[1], dn[2], dn[3], n1[1], n1[2], n1[3], n2[1], n2[2], n2[3]]) 
        sfn = np.array(sfn)
        mw = round(np.max(sfn[:,2]), 5)
        nw = round(np.min(sfn[:,2]), 5)

        back = []
        for edge in sfedge: 
            if (round(edge[5], 5) == mw and round(edge[8], 5) == mw) or  (round(edge[5], 5) == nw and round(edge[8], 5) == nw) : 
                continue 
            if edge[5] > edge[8]: 
                back.append([edge[1], edge[0], edge[2], edge[3], edge[7], edge[8], edge[9], edge[4], edge[5], edge[6]])
            else: 
                back.append(edge)
        
        back = sorted(back, key=lambda val:val[5])  # sorted(newbm, key=lambda val:val[5])

        ptchbase = []
        for i, ed in enumerate(back): 
            if i %2 ==0: 
                ed1 = ed 
            else: 
                if ed1[4] > ed[4] : 
                    ptchbase.append([ed[3], ed[0], ed[1], [ed[4],ed[5], ed[6]], [ed[7],ed[8], ed[9]]])
                    break 
                else:
                    ptchbase.append([ed1[3], ed1[0], ed1[1], [ed1[4],ed1[5], ed1[6]], [ed1[7],ed1[8], ed1[9]]])
                    break 

        f = 1 
        cnt = 0 
        while f:
            f = 0 
            for j, bk in enumerate(back): 
                if ptchbase[len(ptchbase) -1][2] == bk[0] and  ptchbase[len(ptchbase) -1][1] != bk[1] : 
                    ptchbase.append([bk[3],  bk[0],  bk[1],  [bk[4],  bk[5],  bk[6] ], [ bk[7],  bk[8],   bk[9] ] ])
                    f = 1 
                    break 
                if ptchbase[len(ptchbase) -1][2] == bk[1] and  ptchbase[len(ptchbase) -1][1] != bk[0]: 
                    ptchbase.append([bk[3],  bk[1],  bk[0], [ bk[7],  bk[8],   bk[9] ],  [bk[4],  bk[5],  bk[6] ] ])
                    f = 1 
                    break
            if f == 1: 
                del(back[j])
            cnt += 1
            if cnt > 10000: 
                print ("ERROR to find base edges for block angle.")
                break
        
        i = 0 
        while i < len(ptchbase): 
            if i ==0 : 
                if ptchbase[i][3][1] == ptchbase[i][4][1] or  ptchbase[i][3][1] > ptchbase[i][4][1] : 
                    del(ptchbase[i])
                    i -= 1
            else: 
                if ptchbase[i][3][1] == ptchbase[i][4][1] or  ptchbase[i][3][1] > ptchbase[i][4][1] or ptchbase[0][1] == ptchbase[i][1]: 
                    del(ptchbase[i])
                    i -= 1
            i += 1 

        ## Step 2: checking connectivity of the beams 
        digit = 5
        for i, p in enumerate(ptchbase):  ## bm, ptchbase = [EL_No, Node No. 1, Node No. 2, [Coordinates x, y, z of node 1], [Coordinates x, y, z of node 2]]
            tmp = [p[0], p[1], p[2], p[3], p[4]]
            ptchbase[i]=tmp 
            if i ==0: continue 
            
            if ptchbase[i-1][2] != ptchbase[i][1]: 
                if round(ptchbase[i-1][4][1], 4) != round(ptchbase[i][3][1], 4): 
                    print ("There are void in beam elements", ptchbase[i-1][4][1]*1000, ptchbase[i][3][1]*1000, (ptchbase[i-1][4][1]-ptchbase[i][3][1])*1000)
                    print (ptchbase[i-1][3], ptchbase[i-1][4], "\n", ptchbase[i][3], ptchbase[i][4])
        
        #######################################################
        ## Scaled node position (NewNode : scaled node)
        ## find the 1st beam and sorting with the next beams 
        #######################################################
        sum = 0 
        sortedpos = []
        for bm in ptchbase: 
            idx1 = np.where(NewNode[:, 0] == bm[1])[0][0]
            N1 = NewNode[idx1]
            idx2 = np.where(NewNode[:, 0] == bm[2])[0][0]
            N2 = NewNode[idx2]
            w = N2[2] - N1[2]
            dh = -(N2[1] - N1[1]) + (bm[4][0] - bm[3][0])/(bm[4][1]-bm[3][1])  *w   ## the value of dh should be Subtracted. (-1 * value)

            bm.append([sum, w, dh])
            bm.append(N1)
            bm.append(N2)
            sortedpos.append(bm)
            
            sum += dh

        rnf = sortedpos[len(sortedpos)-1]
        rn0 = sortedpos[0]
        for i, nd in enumerate(NewNode): 
            shifted = 0 
            for rn in sortedpos:
                if nd[2] >= rn[6][2] and nd[2] <= rn[7][2]: 
                    NewNode[i][1] = (nd[1]+rn[5][0]) + (nd[2]-rn[6][2]) * rn[5][2] / rn[5][1]
                    shifted = 1 
                    break 
            if shifted == 0: 
                if nd[2] > 0 :
                    NewNode[i][1] = (nd[1]+rnf[5][0]) + (nd[2]-rnf[6][2]) * rnf[5][2] / rnf[5][1]
                else: 
                    NewNode[i][1] = (nd[1]+rn0[5][0]) + (nd[2]-rn0[6][2]) * rn0[5][2] / rn0[5][1]
        
        test = 0 
        if test ==1: 
            self.npn=NewNode
            self.ImageCompare(file=Pattern.name+"-Orign_scaled_comparison", dpi=300, edge1=Edge_Topboundary, edge2=Edge_Topboundary, node1=NodeOrigin, node2=self.npn, shift=[1, 1.5*self.TargetPL, 0.0, 0.0], nid=0)
            nd0=[]; nd1=[]
            nd2=[]; nd3=[]
            iedge=[]
            for bm in ptchbase:
                nd0.append([bm[1], bm[3][0], bm[3][1], bm[3][2]])
                nd1.append([bm[2], bm[4][0], bm[4][1], bm[4][2]])
                idx = np.where(self.npn[:,0]==bm[1])[0][0]
                nd2.append(self.npn[idx])
                idx = np.where(self.npn[:,0]==bm[2])[0][0]
                nd3.append(self.npn[idx])
                iedge.append([bm[1], bm[2], 0, bm[0]])
        
        return NewNode, NodeOrigin
        
        
    def PatternScaling(self, ModelGD=0.0, TargetGD=0.0, ModelPL=0.0, NoPitch=0,  ModelTDW=0, TargetTDW=0, TargetTW=0, TargetOD=0.0, center=[], ModelOD=0.0, t3dm=0, orgn=[], surf_btm=[]):
        if NoPitch ==0: 
            # print ("No_Pitch=%d,  TargetTDW=%.3f, ModelTDW=%.3f, ModelPL=%.3f"%(NoPitch, TargetTDW*1000, ModelTDW*1000, ModelPL*1000))
            if TargetTDW ==0: TargetTDW = ModelTDW 

            RecommendedPL = TargetTDW / ModelTDW * ModelPL
            PN = TargetOD * self.PI / RecommendedPL
            NoPitch = round(PN, 0)
            try: 
                self.TargetPL = TargetOD * self.PI / NoPitch
            except: 
                print ("No_Pitch=%d, PN=%.3f, TargetTDW=%.3f, ModelTDW=%.3f, ModelPL=%.3f, Recommend PL=%.3f"%(NoPitch, PN, TargetTDW*1000, ModelTDW*1000, ModelPL*1000, RecommendedPL*1000))
                print (" ERROR No Pitch=%d"%(NoPitch))
                sys.exit()
            PitchLengthInfo = "* No. of Pitches= %.4f -> %d\n* Pitch Length=%.3f (Model=%.3f)"%(PN, NoPitch,  self.TargetPL*1000, ModelPL*1000)
            # PitchLengthInfo = "** Auto-Calculated the Number of Pitches= %.4f -> %d, Pitch Length=%.3f (Model=%.3f)"%(PN, NoPitch,  self.TargetPL*1000, ModelPL*1000)
        else: 
            self.TargetPL = TargetOD * self.PI / NoPitch
            PitchLengthInfo = "* No. of Pitches=%d\n* Pitch Length=%.3f (Model=%.3f)"%(NoPitch, self.TargetPL*1000, ModelPL*1000)
            # PitchLengthInfo = "** User Input the number of Pitches=%d, Pitch Length=%.3f  (Model=%.3f)"%(NoPitch, self.TargetPL*1000, ModelPL*1000)
        
        TotalPitchWidth = self.PatternWidth # self.PatternWidth = self.PitchWidth(self.freetop)
        
        ########################################################
        # TargetPitchWidth = TotalPitchWidth + 0.02  ## --> for testing.   ## It needs to get Target Pitch Width 
        if TargetTW > 0: TargetPitchWidth = TargetTW 
        else:            TargetPitchWidth = TotalPitchWidth

        if TargetTDW == 0 : TargetTDW = ModelTDW 

        self.NoPitch = NoPitch 
        ########################################################

        if len(center) ==0:  center = [0, 0.0, 0.0, round(ModelOD /2.0, 9)]
        
        #####################################################################
        Ratio_PL =  self.TargetPL/ModelPL
        if TargetTDW > 0.0 :        Ratio_TW = TargetTDW / ModelTDW
        else:                       Ratio_TW = 1.0 
        if TargetGD > 1.0E-03 and ModelGD > 1.0E-03:       Ratio_GD = TargetGD / ModelGD 
        else:                                      Ratio_GD =  1.0

        if ModelOD == 0: 
            mz = -10.0
            for n in self.npn: 
                if n[3] > mz: mz = n[3]
            Shift_Z = round((TargetOD - mz*2) / 2.0, 9) 
        else: 
            Shift_Z = round((TargetOD - ModelOD) / 2.0, 9) 

        Deco_scaling_margin = 1.0E-03  ## half length margin = 1mm
        Ratio_DecoWidth = (TargetPitchWidth - TargetTDW - Deco_scaling_margin) / (TotalPitchWidth - ModelTDW) 

        # print (  "\n********************************************")
        if t3dm == 1: 
            print ("* T3DM Mode ")
            Ratio_TW = 1.0
            Ratio_GD = 1.0 
            Ratio_DecoWidth = 1.0 
            Shift_Z = 0.0
        else: 
            print ("* Expansion Mode ")
        # print (  "********************************************")

        print ("* OD: Model=%7.2f, Target=%5.2f, Shift=%6.2f"%(ModelOD*1000, TargetOD*1000, Shift_Z*1000))
        # if ModelGD > 1.0: print ("** Model GD=%7.2f, Target GD=%5.2f"%(ModelGD, TargetGD))
        print ("* GD: Model=%7.2f, Target=%5.2f"%(ModelGD*1000, TargetGD*1000))
        print (PitchLengthInfo)
        # print ("* PL: Model=%7.2f, Target=%7.2f"%(ModelPL*1000, self.TargetPL*1000))
        
        print ("\n* Scaling Ratio\n  PL=%6.3f, TW=%6.3f, GD=%6.2f, Deco=%6.2f"%(Ratio_PL, Ratio_TW, Ratio_GD, Ratio_DecoWidth))
        print ("\n* Profile TW=%7.2f, TDW=%7.2f"%(TargetPitchWidth*1000, TargetTDW*1000))
        print (  "* Pattern TW=%7.2f, TDW=%7.2f"%(TotalPitchWidth*1000, ModelTDW*1000))
        print (  "* Scaled  TW=%7.2f, TDW=%7.2f"%((ModelTDW*Ratio_TW +  (TotalPitchWidth - ModelTDW) * Ratio_DecoWidth)*1000, ModelTDW*Ratio_TW*1000))
        print (  "* Deco Width ")
        print (  "  Pattern=%7.2f, Profile=%7.2f"%((TotalPitchWidth - ModelTDW)*500,(TargetPitchWidth - TargetTDW)*500))
        print (  "   Scaled=%7.2f"%((TotalPitchWidth - ModelTDW)*Ratio_DecoWidth*500))
        # print ("* Deco Width %7.2f -> %7.2f, Target=%7.2f"%((TotalPitchWidth - ModelTDW)*500, (TotalPitchWidth - ModelTDW)*Ratio_DecoWidth*500,  (TargetPitchWidth - TargetTDW)*500))
        
        
        NodeOrigin = [] 
        for i, nd in enumerate(self.npn): 
            NodeOrigin.append([nd[0], nd[1], nd[2], nd[3]])
        NodeOrigin = np.array(NodeOrigin)
        
        method =0   ## method 0 is the best option so far .
        if method ==1:   
            Edge_Topboundary = self.SurfaceBoundary(self.freetop)
            base = self.SearchingLowBottomFromBottomBoundaryEdge(Edge_Topboundary, NodeOrigin= self.npn, return_edge=0)  #  Edge_boundary, NodeOrigin=[], return_edge=1)
        NewNode=[]       
        ModelHD =  ModelOD/2.0
        Scaled_HalfTW = ModelTDW * Ratio_TW / 2.0 
        design_nodes=[]
        Pos_deco_nodes=[]
        HalfWidth =  ModelTDW / 2.0
        if t3dm == 0 : 
            for i, nd in enumerate(self.npn): 
                # if nd[0] == 10002896 or nd[0] == 10002934 or nd[0] == 10003048: print (nd[0]-10**7, round(nd[1]*1000, 5),  round(nd[2]*1000, 5),  round(nd[3]*1000, 5))
                NZ =  ModelHD - (ModelHD - nd[3]) * Ratio_GD + Shift_Z
                DelY = abs(nd[2]) - HalfWidth
                if DelY > 0: 
                    NY = Scaled_HalfTW + DelY * Ratio_DecoWidth
                    if nd[2] < 0: NY = -NY 
                    else: Pos_deco_nodes.append(NY)
                else: 
                    NY = (nd[2] ) * Ratio_TW 
                    design_nodes.append(NY)
                

                if method ==1: 
                    NX= self.PL_Scaling(ModelPL, self.TargetPL, nd, base, NodeOrigin, Ratio_TW, beam=1, t3dm=0)
                else: 
                    NX = (nd[1]) * Ratio_PL 
                NewNode.append([nd[0], NX, NY, NZ])
        else: 

            for i, nd in enumerate(self.npn): 
                # if nd[0] == 10002896 or nd[0] == 10002934 or nd[0] == 10003048: print (nd[0]-10**7, round(nd[1]*1000, 5),  round(nd[2]*1000, 5),  round(nd[3]*1000, 5))
                NZ = nd[3] 
                NX = (nd[1]) * Ratio_PL 
                NY = nd[2]
                NewNode.append([nd[0], NX, NY, NZ])

        NewNode = np.array(NewNode)
        if t3dm == 0 : 
            def_TDW=max(design_nodes)-min(design_nodes)
            def_deco = (max(Pos_deco_nodes)-min(Pos_deco_nodes))
            TotalW =NewNode[:,2]
            TotalWidth = np.max(TotalW) - np.min(TotalW)
            print ("\n# Deformed Width=%7.3f\n  >> TDW=%7.3f, Deco=%7.3f"%(TotalWidth*1000, def_TDW*1000, def_deco*1000))
            # print ("* Deformed TDW =%7.3f, Deco Width=%7.2f\n* Total Pattern Width=%7.3f"%(def_TDW*1000, def_deco*1000, TotalWidth*1000)) 
            print ("********************************************\n")

        ############################################################################
        ## block angle adjusting 
        ############################################################################
        # step 0 : generating beam element for replacing beam element to bottom edges 
        method = 1 
        if method == 1 and t3dm ==0 : 
            ## search the left bottom node (edge)
            digit=6
            edge_base_boundary =  self.SurfaceBoundary(surf_btm)

            sfn = []
            sfedge = []
            for dn in edge_base_boundary: 
                ix = np.where(orgn[:,0] == dn[0])[0][0]; n1 = orgn[ix]
                sfn.append(orgn[ix])
                ix = np.where(orgn[:,0] == dn[1])[0][0]; n2 = orgn[ix]
                sfn.append(orgn[ix])
                sfedge.append([dn[0], dn[1], dn[2], dn[3], n1[1], n1[2], n1[3], n2[1], n2[2], n2[3]]) 
            sfn = np.array(sfn)
            mw = round(np.max(sfn[:,2]), 5)
            nw = round(np.min(sfn[:,2]), 5)
            # print ("Min Y=%.5f, Max Y=%.5f"%(nw*1000, mw*1000))

            back = []
            for edge in sfedge: 
                if (round(edge[5], 5) == mw and round(edge[8], 5) == mw) or  (round(edge[5], 5) == nw and round(edge[8], 5) == nw) : 
                    continue 
                if edge[5] > edge[8]: 
                    back.append([edge[1], edge[0], edge[2], edge[3], edge[7], edge[8], edge[9], edge[4], edge[5], edge[6]])
                else: 
                    back.append(edge)
            
            back = sorted(back, key=lambda val:val[5])  # sorted(newbm, key=lambda val:val[5])

            ptchbase = []
            for i, ed in enumerate(back): 
                if i %2 ==0: 
                    ed1 = ed 
                else: 
                    if ed1[4] > ed[4] : 
                        ptchbase.append([ed[3], ed[0], ed[1], [ed[4],ed[5], ed[6]], [ed[7],ed[8], ed[9]]])
                        break 
                    else:
                        ptchbase.append([ed1[3], ed1[0], ed1[1], [ed1[4],ed1[5], ed1[6]], [ed1[7],ed1[8], ed1[9]]])
                        break 
            # del(back[0])
            # del(back[0])
            ## found the left bottom 

            # print (ptchbase[0])

            f = 1 
            cnt = 0 
            while f:
                f = 0 
                for j, bk in enumerate(back): 
                    if ptchbase[len(ptchbase) -1][2] == bk[0] and  ptchbase[len(ptchbase) -1][1] != bk[1] : 
                        ptchbase.append([bk[3],  bk[0],  bk[1],  [bk[4],  bk[5],  bk[6] ], [ bk[7],  bk[8],   bk[9] ] ])
                        # print ("BK", ptchbase[len(ptchbase) -1])
                        f = 1 
                        break 
                    if ptchbase[len(ptchbase) -1][2] == bk[1] and  ptchbase[len(ptchbase) -1][1] != bk[0]: 
                        ptchbase.append([bk[3],  bk[1],  bk[0], [ bk[7],  bk[8],   bk[9] ],  [bk[4],  bk[5],  bk[6] ] ])
                        # print ("*BK", ptchbase[len(ptchbase) -1])
                        f = 1 
                        break
                if f == 1: 
                    del(back[j])
                cnt += 1
                if cnt > 10000: 
                    print ("ERROR to find base edges for block angle.")
                    break
            
            i = 0 
            while i < len(ptchbase): 
                if i ==0 : 
                    if ptchbase[i][3][1] == ptchbase[i][4][1] or  ptchbase[i][3][1] > ptchbase[i][4][1] : 
                        del(ptchbase[i])
                        i -= 1
                else: 
                    if ptchbase[i][3][1] == ptchbase[i][4][1] or  ptchbase[i][3][1] > ptchbase[i][4][1] or ptchbase[0][1] == ptchbase[i][1]: 
                        del(ptchbase[i])
                        i -= 1
                i += 1 

        elif method == 0  and t3dm ==0: 
            ptchbase=[]
            for bm in self.UpBack:     ## bm, ptchbase = [EL_No, Node No. 1, Node No. 2, [Coordinates x, y, z of node 1], [Coordinates x, y, z of node 2]]
                if round(bm[3][1], 5) != round(bm[4][1], 5):   ## self.LowBack is used for TBR Pattern expansion. 
                    ptchbase.append(bm)
                # ix = np.where(self.npn[:,0] == bm[1])[0]
                # print ("beam node %d > %d"%(bm[1]-10**7, len(ix)))

            for i, p in enumerate(ptchbase):
                if p[3][1] > p[4][1]: 
                    tmp = [p[0], p[2], p[1], p[4], p[3], p[4][1]]
                    ptchbase[i] = tmp 
                else: 
                    tmp = [p[0], p[1], p[2], p[3], p[4], p[3][1]]
                    ptchbase[i] = tmp 
                # print ("%5d, %5d, %5d, %7.3f, %7.3f"%(ptchbase[i][0]-10**7, ptchbase[i][1]-10**7, ptchbase[i][2]-10**7, ptchbase[i][3][1]*1000, ptchbase[i][4][1]*1000))

            ptchbase=sorted(ptchbase, key=lambda val:val[5])
        
        else: 
            return NewNode, NodeOrigin
        # for i, p in enumerate(ptchbase): 
        #     if i ==0: print (" %6d(%10.4f) ~ %6d(%10.4f) "%(p[1]-10**7, p[3][1]*1000, p[2]-10**7, p[4][1]*1000))
        #     else:     print (" %6d(%10.4f) ~ %6d(%10.4f) diff=%6.4f "%(p[1]-10**7, p[3][1]*1000, p[2]-10**7, p[4][1]*1000, (ptchbase[i-1][4][1]-p[3][1])*1000))

        ## Step 2: checking connectivity of the beams 
        digit = 5
        for i, p in enumerate(ptchbase):  ## bm, ptchbase = [EL_No, Node No. 1, Node No. 2, [Coordinates x, y, z of node 1], [Coordinates x, y, z of node 2]]
            tmp = [p[0], p[1], p[2], p[3], p[4]]
            ptchbase[i]=tmp 
            # print ("%5d, %5d, %5d, %7.3f, %7.3f"%(ptchbase[i][0]-10**7, ptchbase[i][1]-10**7, ptchbase[i][2]-10**7, ptchbase[i][3][1]*1000, ptchbase[i][4][1]*1000), ptchbase[i][3], ptchbase[i][4])
            if i ==0: continue 
            
            if ptchbase[i-1][2] != ptchbase[i][1]: 
                if round(ptchbase[i-1][4][1], digit) != round(ptchbase[i][3][1], digit): 
                    print ("There are void in beam elements", ptchbase[i-1][4][1]*1000, ptchbase[i][3][1]*1000, (ptchbase[i-1][4][1]-ptchbase[i][3][1])*1000)
                    print (ptchbase[i-1][3], ptchbase[i-1][4], "\n", ptchbase[i][3], ptchbase[i][4])
                    # sys.exit()
        # print ("ENDDDD")
        # sys.exit()
        
        #######################################################
        ## Scaled node position (NewNode : scaled node)
        ## find the 1st beam and sorting with the next beams 
        #######################################################
        sum = 0 
        sortedpos = []
        for bm in ptchbase: 
            idx1 = np.where(NewNode[:, 0] == bm[1])[0][0]
            N1 = NewNode[idx1]
            idx2 = np.where(NewNode[:, 0] == bm[2])[0][0]
            N2 = NewNode[idx2]
            w = N2[2] - N1[2]


            #  method 1 : not good algorithm.. 
            # idx1 = np.where(self.npn[:, 0] == bm[1])[0][0]
            # N01 = self.npn[idx1]
            # idx2 = np.where(self.npn[:, 0] == bm[2])[0][0]
            # N02 = self.npn[idx2]
            # h0 = N02[3] - N01[3] 
            # w0 = N02[2] - N01[2]
            # if w0 < 0: print ("####################### opposite position of beam nodes... ")
            # dh =  -h0 / w *(1-w/w0)

            # method : better algorithm. 
            dh = -(N2[1] - N1[1]) + (bm[4][0] - bm[3][0])/(bm[4][1]-bm[3][1])  *w   ## the value of dh should be Subtracted. (-1 * value)

            bm.append([sum, w, dh])
            bm.append(N1)
            bm.append(N2)
            sortedpos.append(bm)
            
            # print ("shift = %7.3f, w=%7.3f(Model W=%7.3f, ratio=%5.2f), dh=%7.3f(ht ratio=%5.2f), current Beam Angle=%6.2f, Del angle=%6.2f, Model Angle=%6.2f, N1[2]=%7.3f, N2[2]=%7.3f"%(sum*1000, w*1000, (bm[4][1]-bm[3][1])*1000, w/ (bm[4][1]-bm[3][1]), dh*1000, (N2[1] - N1[1])/(bm[4][0] - bm[3][0]) , degrees(atan((N2[1] - N1[1])/w)), degrees(atan(dh/w)), degrees(atan((bm[4][0] - bm[3][0])/(bm[4][1]-bm[3][1]))), N1[2]*1000, N2[2]*1000))
            # print (" Node id Model = %6d, %6d, Current = %6d, %6d"%(bm[1]-10**7, bm[2]-10**7, N1[0]-10**7, N2[0]-10**7)) # Verified.. the same node ids 
            sum += dh

        #####################################################################################################
        ## for checking the values in sorted positions
        ## beam element iD, node 1 id, node 2 id, [Original coordinates node 1], [Original coordinates node 2], 
        ##          [element shift position along x-axis, width value of the inclination, height value of the inclination], 
        ##          [node 1 id, current x, y, z], [node 2 id, current x, y, z]
        # N = len(sortedpos)
        # for i in range(N): 
        #     print ("############################################")
        #     for m, tm in enumerate(sortedpos[i]): 
        #         if m ==0: print ("Beam Element ID=", tm-10**7)
        #         if m ==1: print ("Beam Node 1 ID=", tm-10**7)
        #         if m ==2: print ("Beam Node 2 ID=", tm-10**7)
        #         if m == 3: print ("Node 1 Model Coordinates : %7.3f, %7.3f, %7.3f"%(tm[0]*1000, tm[1]*1000, tm[2]*1000))
        #         if m == 4: print ("Node 2 Model Coordinates : %7.3f, %7.3f, %7.3f"%(tm[0]*1000, tm[1]*1000, tm[2]*1000))
        #         if m == 5: print ("Element X shift =%7.3f, and Inclination y=%7.3f, X=%7.3f"%(tm[0]*1000, tm[1]*1000, tm[2]*1000))
        #         if m ==6 : print ("Current Node 1 : %6d, %7.3f, %7.3f, %7.3f"%(tm[0]-10**7, tm[1]*1000, tm[2]*1000, tm[3]*1000))
        #         if m ==7 : print ("Current Node 2 : %6d, %7.3f, %7.3f, %7.3f"%(tm[0]-10**7, tm[1]*1000, tm[2]*1000, tm[3]*1000))
        #     print ("verification with original inclination Del x=%7.3f, y=%7.3f"%((sortedpos[i][4][0]-sortedpos[i][3][0])*1000, (sortedpos[i][4][1]-sortedpos[i][3][1])*1000))
        #     print ("                   Current inclination Del x=%7.3f, y=%7.3f"%((sortedpos[i][7][1]-sortedpos[i][6][1])*1000, (sortedpos[i][7][2]-sortedpos[i][6][2])*1000))
        #####################################################################################################
        
        
        # rn[5][0] : element shift 
        # rn[5][1] : width of Model inclination; rn[5][2] : del height of Model inclination (dh = h1 - w1/w0 * h0)  
        # rn[6] : Beam Node 1, rn[7] : beam node 2
        rnf = sortedpos[len(sortedpos)-1]
        rn0 = sortedpos[0]
        for i, nd in enumerate(NewNode): 
            # if nd[0] == 10002896 or nd[0] == 10002934 or nd[0] == 10003048: print (nd[0]-10**7, round(nd[1]*1000, 5),  round(nd[2]*1000, 5),  round(nd[3]*1000, 5))
            shifted = 0 
            for rn in sortedpos:
                if nd[2] >= rn[6][2] and nd[2] <= rn[7][2]: 
                    NewNode[i][1] = (nd[1]+rn[5][0]) + (nd[2]-rn[6][2]) * rn[5][2] / rn[5][1]
                    shifted = 1 
                    break 
            if shifted == 0: 
                if nd[2] > 0 :
                    # rn = sortedpos[len(sortedpos)-1]
                    NewNode[i][1] = (nd[1]+rnf[5][0]) + (nd[2]-rnf[6][2]) * rnf[5][2] / rnf[5][1]
                else: 
                    # rn = sortedpos[0]
                    NewNode[i][1] = (nd[1]+rn0[5][0]) + (nd[2]-rn0[6][2]) * rn0[5][2] / rn0[5][1]
        

        # NodeOrigin = np.array(NodeOrigin)
        test = 0 
        if test ==1: 
            self.npn=NewNode
            # self.Image(file=Pattern.name+"-PitchAngle_Scaled.png", edge0=Edge_Topboundary)
            self.ImageCompare(file=Pattern.name+"-Orign_scaled_comparison", dpi=300, edge1=Edge_Topboundary, edge2=Edge_Topboundary, node1=NodeOrigin, node2=self.npn, shift=[1, 1.5*self.TargetPL, 0.0, 0.0], nid=0)
            nd0=[]; nd1=[]
            nd2=[]; nd3=[]
            iedge=[]
            for bm in ptchbase:
                nd0.append([bm[1], bm[3][0], bm[3][1], bm[3][2]])
                nd1.append([bm[2], bm[4][0], bm[4][1], bm[4][2]])
                idx = np.where(self.npn[:,0]==bm[1])[0][0]
                nd2.append(self.npn[idx])
                idx = np.where(self.npn[:,0]==bm[2])[0][0]
                nd3.append(self.npn[idx])
                iedge.append([bm[1], bm[2], 0, bm[0]])
            # self.Image(file=Pattern.name+"-beam", dpi=300, node0=nd0, node1=nd1, node2=nd2, node3=nd3, edge0=iedge)
            # sys.exit()
        # self.ImageCompare(file=Pattern.name+"-Orign_scaled_comparison", dpi=300, edge1=Edge_Topboundary, edge2=Edge_Topboundary, node1=NodeOrigin, node2=self.npn, shift=[0, self.TargetPL, 0.0, 0.0])
        
        return NewNode, NodeOrigin
    def PitchWidth(self, Top_surface): 
        
        Wmax = 0.0
        Wmin = 0.0
        for sf in Top_surface: 
            idx = np.where(self.npn[:, 0] == sf[7])[0][0]
            if self.npn[idx][2] > Wmax: Wmax = self.npn[idx][2]
            if self.npn[idx][2] < Wmin: Wmin = self.npn[idx][2]

            idx = np.where(self.npn[:, 0] == sf[8])[0][0]
            if self.npn[idx][2] > Wmax: Wmax = self.npn[idx][2]
            if self.npn[idx][2] < Wmin: Wmin = self.npn[idx][2]

            idx = np.where(self.npn[:, 0] == sf[9])[0][0]
            if self.npn[idx][2] > Wmax: Wmax = self.npn[idx][2]
            if self.npn[idx][2] < Wmin: Wmin = self.npn[idx][2]

            if int(sf[10]) > 0: 
                idx = np.where(self.npn[:, 0] == sf[10])[0][0]
                if self.npn[idx][2] > Wmax: Wmax = self.npn[idx][2]
                if self.npn[idx][2] < Wmin: Wmin = self.npn[idx][2]

        return (Wmax-Wmin)
    def SearchingLowBottomFromBottomBoundaryEdge(self, Edge_boundary, NodeOrigin=[], return_edge=0): 
        if len(NodeOrigin) > 0: NodeOrigin=np.array(NodeOrigin)
        else: NodeOrigin = self.npn 

        bm_updown=[]
        for ed in Edge_boundary: 
            a = np.where(NodeOrigin[:,0]==ed[0])[0][0]
            b = np.where(NodeOrigin[:,0]==ed[1])[0][0]
            N1 = NodeOrigin[a]
            N2 = NodeOrigin[b]
            if N1[2] != N2[2]: 
                tmp=[ed[3], N1[0], N2[0], [N1[1], N1[2], N1[3]], [N2[1], N2[2], N2[3]]]
                bm_updown.append(tmp)

        ptchbase=[]
        neg=[]
        tedge=[]
        digit=7
        for bm in bm_updown:
            fd = 0
            for bt in bm_updown:
                if (bm[3][2] == bt[4][2] and bm[4][2] == bt[3][2]) or (bm[3][2] == bt[3][2] and bm[4][2] == bt[4][2]): 
                    if bm[3][1] < bt[4][1]: 
                        fd = 0
                        break
                    else: 
                        fd = 1 
                        break  
            if fd ==0: 
                ptchbase.append(bm)
                tedge.append([bm[1], bm[2], 1, bm[0]])

        if return_edge ==1: 
            return tedge 
        else: 
            for i, p in enumerate(ptchbase):
                if p[3][1] > p[4][1]: 
                    tmp = [p[0], p[2], p[1], p[4], p[3], p[4][1]]
                    ptchbase[i] = tmp 
                else: 
                    tmp = [p[0], p[1], p[2], p[3], p[4], p[3][1]]
                    ptchbase[i] = tmp 
            ptchbase=sorted(ptchbase, key=lambda val:val[5])
            return ptchbase
    
    def Groove_kerf_edges_in_top_surface(self, top_edges=[], surf_main_side=[], surf_sub_side=[], surf_kerf_side=[]) : # , orgn=[], npn=[], surf_main_btm=[], surf_sub_btm=[]): 
        top_edges_2_groove =[]
        top_edges_2_kerf = []
        i = 0 
        if len(surf_kerf_side) > 0: 
            while i < len(top_edges): 
                ix1 = np.where(surf_kerf_side[:,7:] == top_edges[i][0])[0]
                ix2 = np.where(surf_kerf_side[:,7:] == top_edges[i][1])[0]
                ix = np.intersect1d(ix1, ix2)
                if len(ix) == 1: 
                    top_edges_2_kerf.append(top_edges[i])
                    top_edges = np.delete(top_edges, i, axis=0)
                    i -= 1 
                i += 1 

        if len(surf_sub_side) > 0: 
            i = 0 
            while i < len(top_edges): 
                ix1 = np.where(surf_sub_side[:,7:] == top_edges[i][0])[0]
                ix2 = np.where(surf_sub_side[:,7:] == top_edges[i][1])[0]
                ix = np.intersect1d(ix1, ix2)
                if len(ix) == 1: 
                    top_edges_2_groove.append(top_edges[i])
                    top_edges = np.delete(top_edges, i, axis=0)
                    i -= 1 
                i += 1 
        
        if len(surf_main_side) > 0: 

            i = 0 
            while i < len(top_edges): 
                ix1 = np.where(surf_main_side[:,7:] == top_edges[i][0])[0]
                ix2 = np.where(surf_main_side[:,7:] == top_edges[i][1])[0]
                ix = np.intersect1d(ix1, ix2)
                if len(ix) == 1: 
                    top_edges_2_groove.append(top_edges[i])
                    top_edges = np.delete(top_edges, i, axis=0)
                    i -= 1 
                i += 1 

        # print ("* Groove side angle is ajusted.\n")
        return np.array(top_edges_2_groove), np.array(top_edges_2_kerf)#, pvnode, cnode, fnode

    
    def GrooveSideNodeRepositioningfromTop(self, TopEdges=[],  orgn=[], alledges=[], surfaces=[], fname="", maingroovebottomedge=[],\
         groovebottomsurf=[], maingroovebottomsurf=[], \
        surf_mainside=[], surf_subside=[], surf_kerfside=[]):## orgn : Nodes with original(model)  coordinates, nodes : coordinates after moved 
        ## groove base boundary edges
        grooveedges, kerfedges = self.Groove_kerf_edges_in_top_surface(top_edges=TopEdges, surf_main_side=surf_mainside, surf_sub_side=surf_subside, surf_kerf_side=surf_kerfside)

        # ## option : only edges to main groove 
        allbottomedges=[]

        for gedegs in maingroovebottomedge: 
            for ed in gedegs: 
                allbottomedges.append(ed)
        
        allbottomedges = np.array(allbottomedges)

        pvnode, cnode, fnode= self.GrooveSideTranslationByDistance(grooveedges, alledges, surfaces, orgn, allbottomedges, chamfer_gauge=0)
        print ("* Groove side angle is ajusted.\n")
        # print ("* Nodes on Groove Side from Top have been translated (by distance)")
        return np.array(kerfedges), np.array(grooveedges), pvnode, cnode, fnode
    def Distinguish_kerf_groove(self, iedges=[], surf_bottom=[], alledges=[], allsurfaces=[], orgn=[]):

        ## iedges :top edges 


        edges=[]
        for edge in iedges: 
            nx1 = np.where(orgn[:, 0]==edge[0])[0][0]
            nx2 = np.where(orgn[:, 0]==edge[1])[0][0]
            edges.append([edge[0], edge[1], 0, edge[3], orgn[nx1][1], orgn[nx1][2], orgn[nx1][3], orgn[nx2][1], orgn[nx2][2], orgn[nx2][3] ])
        iedges=np.array(edges)

        temp=[]
        for edge in alledges: 
            nx1 = np.where(orgn[:, 0]==edge[0])[0][0]
            nx2 = np.where(orgn[:, 0]==edge[1])[0][0]
            temp.append([edge[0], edge[1], 0, edge[3], orgn[nx1][1], orgn[nx1][2], orgn[nx1][3], orgn[nx2][1], orgn[nx2][2], orgn[nx2][3] ])
        alledges=np.array(temp)


        surf_kerf=[]
        edge_kerf=[]
        surf_groove=[]
        edge_groove=[]
        debug = 0
        for i, edge in enumerate(iedges): 
            surfs =[]
            edges=[]
            cedge = edge 
            counting = 0
            while counting < 20: 
                counting += 1
                tedge = self.FindContactingEdge(cedge, alledges)
                if len(tedge)> 0: 
                    edges.append(tedge)
                    nedge, sf = self.FindAnotherEdgeInSurface(next=2, cedge=tedge, edges=alledges, surfaces=allsurfaces, sfreturn=1)

                    ix = np.where(self.SF_pitchside[:,0]==sf[0])[0]
                    ix1 = np.where(self.SF_pitchside[:,1]==sf[1])[0]
                    ix = np.intersect1d(ix, ix1)
                    if len(ix) == 1: 
                        break 

                else: 
                    ## no more next edge.. 
                    id1 = np.where(surf_bottom[:,7:] == cedge[0])[0]
                    id2 = np.where(surf_bottom[:,7:] == cedge[1])[0]
                    ids = np.intersect1d(id1, id2) 
                    if len(ids) > 0: 
                        surf_groove.append(surfs)
                        edge_groove.append(edge)
                        if debug ==1: print ("    ************* i=%3d, counting=%2d  met the groove bottom"%(i, counting))
                        break
                    else: 
                        surf_kerf.append(surfs)
                        edge_kerf.append(edge)
                        if debug ==1: print ("    >>>>>>>>>>>> ", len(surfs), ", the numger of kerf edge =", len(surf_kerf), ",", id1, id2)
                        break 

                id1 = np.where(surf_bottom[:,0] == sf[0])[0]
                if debug ==2: print ("  i=%3d, counting=%2d, sf id=%6d face=%d"%(i, counting, sf[0]-10**7, sf[1]), id1)

                if len(id1) > 0: 
                    surf_groove.append(surfs)
                    edge_groove.append(edge)
                    if debug ==1: print ("    >*********** i=%3d, counting=%2d  met the groove bottom"%(i, counting))
                    break 
                else: 
                    surfs.append(sf)
                    cedge = nedge

        # print ("All kerf edges : ", len(surf_kerf), "edges=", len(kerfedges))

        return edge_groove, surf_groove, edge_kerf, surf_kerf

    def Grooveside_2NodeTranslation(self, ind, NodeTranslated, cnd, nodecnt2): 
        case21=0;         case22=0;         case23=0
        case24=0; case241=0; case242=0; case243=0 

        anglestd = 10.0 



        nodecnt2.append(self.npn[ind][0])

        # print (len(NodeTranslated), cnd)

        aLen = round(sqrt(NodeTranslated[cnd[2]-cnd[1  ]][5]**2 + NodeTranslated[cnd[2]-cnd[1]  ][6]**2), 9)
        bLen = round(sqrt(NodeTranslated[cnd[2]-cnd[1]+1][5]**2 + NodeTranslated[cnd[2]-cnd[1]+1][6]**2), 9)

        if aLen ==0 and bLen ==0:   
            DelX=0.0
            DelY=0.0
            DelZ=0.0
            self.TranslatedNode.append([self.npn[ind][0], DelX, DelY, DelZ])
            case21+=1
        
        elif aLen ==0: 
            x1 = NodeTranslated[cnd[2]-cnd[1]+1][5]
            y1 = NodeTranslated[cnd[2]-cnd[1]+1][6]
            x2 = self.npn[ind][1] - NodeTranslated[cnd[2]-cnd[1]][8][1] 
            y2 = self.npn[ind][2] - NodeTranslated[cnd[2]-cnd[1]][8][2] 

            if round(x1*x2 + y2, 6) == 0: 
                DelX = x1
                DelY = y1
            else: 
                DelX = (x1**2 + y1**2) * x2 / (x1*x2 + y2)
                DelY = (x1**2 + y1**2) * y2 / (x1*x2 + y2)
            DelZ = 0.0

            self.TranslatedNode.append([self.npn[ind][0], DelX, DelY, DelZ])
            self.npn[ind][1] += DelX
            self.npn[ind][2] += DelY
            case22+=1

        elif bLen ==0: 
            x1 = NodeTranslated[cnd[2]-cnd[1]][5]
            y1 = NodeTranslated[cnd[2]-cnd[1]][6]
            x2 = self.npn[ind][1] - NodeTranslated[cnd[2]-cnd[1]+1][8][1] 
            y2 = self.npn[ind][2] - NodeTranslated[cnd[2]-cnd[1]+1][8][2] 

            if round(x1*x2 + y2, 6) == 0: 
                DelX = x1
                DelY = y1
            else: 
                DelX = (x1**2 + y1**2) * x2 / (x1*x2 + y2)
                DelY = (x1**2 + y1**2) * y2 / (x1*x2 + y2)

            DelZ = 0.0

            self.TranslatedNode.append([self.npn[ind][0], DelX, DelY, DelZ])
            self.npn[ind][1] += DelX
            self.npn[ind][2] += DelY
            case23+=1
        else: 
            if round(NodeTranslated[cnd[2]-cnd[1]  ][5], 4) == round(NodeTranslated[cnd[2]-cnd[1]+1][5], 4) and round(NodeTranslated[cnd[2]-cnd[1]  ][6], 4) == round(NodeTranslated[cnd[2]-cnd[1]+1][6], 4): 
                self.npn[ind][1] = NodeTranslated[cnd[2]-cnd[1]][1]
                self.npn[ind][2] = NodeTranslated[cnd[2]-cnd[1]][2]
                
                DelX = NodeTranslated[cnd[2]-cnd[1]][5]
                DelY = NodeTranslated[cnd[2]-cnd[1]][6]
                DelZ = 0.0
                self.TranslatedNode.append([self.npn[ind][0], DelX, DelY, DelZ])

                case24+=1

            else: 

                vb0 = [0, NodeTranslated[cnd[2]-cnd[1]  ][5], NodeTranslated[cnd[2]-cnd[1]  ][6], 0.0]
                vb1 = [0, NodeTranslated[cnd[2]-cnd[1]+1][5], NodeTranslated[cnd[2]-cnd[1]+1][6], 0.0]
                angleBtw = round(Angle_Between_Vectors(vb0, vb1), 8)
                vk = (vb0[0]*vb1[1]-vb0[1]*vb1[0]) 
                if vk < 0: 
                    angleBtw = -angleBtw

                if abs(degrees(angleBtw)) <anglestd or abs(degrees(angleBtw)) > 180-anglestd:   ## nodes on line (angle under 10 degrees) 
                    self.npn[ind][1] = (NodeTranslated[cnd[2]-cnd[1]][1] + NodeTranslated[cnd[2]-cnd[1]+1][1] ) / 2.0
                    self.npn[ind][2] = (NodeTranslated[cnd[2]-cnd[1]][2] + NodeTranslated[cnd[2]-cnd[1]+1][2] ) / 2.0
                    self.TranslatedNode.append([self.npn[ind][0], NodeTranslated[cnd[2]-cnd[1]][5],NodeTranslated[cnd[2]-cnd[1]][6],NodeTranslated[cnd[2]-cnd[1]][7]])
                    case241+=1

                elif (NodeTranslated[cnd[2]-cnd[1]  ][9] == 1 and NodeTranslated[cnd[2]-cnd[1]+1][9] == 0) or (NodeTranslated[cnd[2]-cnd[1]  ][9] == 0 and NodeTranslated[cnd[2]-cnd[1]+1][9] ==1) :  ## main and sub groove meeting .. follow the main groove edge 
                    if NodeTranslated[cnd[2]-cnd[1]  ][9] == 1: 
                        DelX = NodeTranslated[cnd[2]-cnd[1]  ][5]
                        DelY = NodeTranslated[cnd[2]-cnd[1]  ][6]
                    else: 
                        DelX = NodeTranslated[cnd[2]-cnd[1]+1][5]
                        DelY = NodeTranslated[cnd[2]-cnd[1]+1][6]
                    DelZ = 0
                    self.TranslatedNode.append([self.npn[ind][0], DelX, DelY, DelZ])
                    self.npn[ind][1] += DelX
                    self.npn[ind][2] += DelY
                    case242+=1
                else:
                    x1 = NodeTranslated[cnd[2]-cnd[1]][5];   y1=NodeTranslated[cnd[2]-cnd[1]  ][6]
                    x2 = NodeTranslated[cnd[2]-cnd[1]+1][5]; y2=NodeTranslated[cnd[2]-cnd[1]+1][6]

                    DelX = (y2*(x1**2 + y1**2) - y1*(x2**2 +  y2**2))/(x1*y2 - x2*y1)
                    DelY = (-x2*(x1**2 + y1**2) +x1*(x2**2 +  y2**2))/(x1*y2 - x2*y1)

                    DelZ = 0
                    self.TranslatedNode.append([self.npn[ind][0], DelX, DelY, DelZ])
                    self.npn[ind][1] += DelX
                    self.npn[ind][2] += DelY
                    # self.npn[ind][3] += DelZ
                    case243+=1


        return case21, case22, case23, case24, case241, case242, case243, nodecnt2

    def GrooveSideTranslationByDistance(self, grooveedges, alledges, surfaces, orgn, maingroovebottomedge, chamfer_gauge=0): 
        T_Start = time.time()

        edges=[]
        edges0 = []
        for edge in grooveedges: 
            nx1 = np.where(self.npn[:, 0]==edge[0])[0][0]
            nx2 = np.where(self.npn[:, 0]==edge[1])[0][0]
            edges.append([edge[0], edge[1], 0, edge[3], self.npn[nx1][1], self.npn[nx1][2], self.npn[nx1][3], self.npn[nx2][1], self.npn[nx2][2], self.npn[nx2][3] ])
            edges0.append([edge[0], edge[1], 0, edge[3], orgn[nx1][1], orgn[nx1][2], orgn[nx1][3], orgn[nx2][1], orgn[nx2][2], orgn[nx2][3] ])
        edges=np.array(edges)
        edges0=np.array(edges0)

        temp=[]
        temp0=[]
        for edge in alledges: 
            nx1 = np.where(self.npn[:, 0]==edge[0])[0][0]
            nx2 = np.where(self.npn[:, 0]==edge[1])[0][0]
            temp.append([edge[0], edge[1], 0, edge[3], self.npn[nx1][1], self.npn[nx1][2], self.npn[nx1][3], self.npn[nx2][1], self.npn[nx2][2], self.npn[nx2][3] ])
            temp0.append([edge[0], edge[1], 0, edge[3], orgn[nx1][1], orgn[nx1][2], orgn[nx1][3], orgn[nx2][1], orgn[nx2][2], orgn[nx2][3] ])
        alledges=np.array(temp)
        alledges0 = np.array(temp0)

        scalednode = np.array(self.npn)

        NodeTranslated = []
        BottomEdgeNodes=[]
        # rz = self.TargetGD / self.ModelGD
        rx = self.TargetTW / self.TreadDesignWidth
        ry = self.TargetPL / self.pitchlength

        # self.Image(edge0=edges, file=Pattern.name+"-BLOCK_EDGE________", eeid=1)
        # sys.exit()
        ShowN1= 2262; ShowN2= 0
        groove_angle_margin = 25.0 
        e_digit=5
        surf_ht_margin = 1.0E-04
        n3d=0; n4d=0
        case1=0; case2=0
        NOID = 6315 # 5357, 5519, 5518 4958 # 4959 
        # SFID1= 0
        # SFID2= 0

        chfnode = []
        # print ("\n\n")
        debugmode =0

        for i, edge in enumerate(edges):
            if debugmode ==1: 
                print ("\n\n") 
                # if i == 5: sys.exit()
            cedge = edge
            cedge0 = edges0[i]
            # va = [edge[7] - edge[4], edge[8] - edge[5], edge[9] - edge[6] ]
            counting = 0
            firstsurface = 1 
            chamfer = 0 
            Pangle = 1000.0

            bigangle =0
            ending = 0 
            addnodecounting = 0 
            ###################################################################################
            # if edge[3]-10000000 == 899 or edge[3]-10000000 == 857: 
            # if edge[0]-10**7 == NOID or edge[1]-10**7 == NOID or edge[0]-10**7 == 6428 or edge[1]-10**7 == 6428: 
            #     debugmode =1
            # else: 
            #     debugmode =0
            ###################################################################################
            
            while counting <20: 
                counting +=1
                tedge = self.FindContactingEdge(cedge, alledges)
                tedge0 = self.FindContactingEdge(cedge0, alledges0)
                
                try: 
                    nedge, sf = self.FindAnotherEdgeInSurface(next=2, cedge=tedge, edges=alledges, surfaces=surfaces, sfreturn=1)
                    nedge0 = self.FindAnotherEdgeInSurface(next=2, cedge=tedge0, edges=alledges0, surfaces=surfaces)
                except:
                    if debugmode ==1 : print ("   %d   no further surface"%(counting))
                    break

                isbtm = np.where(maingroovebottomedge[:,3]==sf[0])[0]
                if len(isbtm) > 0: 
                    break 

                if  counting ==2 and chamfer == 1 and firstsurface == 0 :
                    indx = np.where(scalednode[:,0]==tedge[0])[0][0]   ## saving top edge 
                    N10 = [scalednode[indx][0], scalednode[indx][1], scalednode[indx][2], scalednode[indx][3] ]
                    N1  = [scalednode[indx][0], scalednode[indx][1], scalednode[indx][2], scalednode[indx][3] ]
                    indx = np.where(scalednode[:,0]==tedge[1])[0][0]  ## saving top edge 
                    N20 = [scalednode[indx][0], scalednode[indx][1], scalednode[indx][2], scalednode[indx][3] ]
                    N2  = [scalednode[indx][0], scalednode[indx][1], scalednode[indx][2], scalednode[indx][3] ]

                    N01 = [tedge0[0], tedge0[4], tedge0[5], tedge0[6]]   ## Model top edge 
                    N02 = [tedge0[1], tedge0[7], tedge0[8], tedge0[9]]   ## Model top edge
                    if debugmode ==1: print (" ** 2nd Surf after Chamfer (EL ID =%d)- counting=%2d (N1=%d, N2=%d)"%(sf[0]-10000000, counting, N10[0]-1000_0000, N20[0]-1000_0000))      

                elif counting ==1 and firstsurface == 1 : 
                    firstsurface =0
                    chamfer = 0

                    indx = np.where(scalednode[:,0]==tedge[0])[0][0] 
                    N10 = [scalednode[indx][0], scalednode[indx][1], scalednode[indx][2], scalednode[indx][3] ] ## extra saving for loop 
                    N1  = [scalednode[indx][0], scalednode[indx][1], scalednode[indx][2], scalednode[indx][3] ]
                    indx = np.where(scalednode[:,0]==tedge[1])[0][0] 
                    N20 = [scalednode[indx][0], scalednode[indx][1], scalednode[indx][2], scalednode[indx][3] ] ## extra saving for loop 
                    N2  = [scalednode[indx][0], scalednode[indx][1], scalednode[indx][2], scalednode[indx][3] ]
                    
                    N01 = [tedge0[0], tedge0[4], tedge0[5], tedge0[6]]   ## Model 1st surface top edge 
                    N02 = [tedge0[1], tedge0[7], tedge0[8], tedge0[9]]   ## Model 1st surface top edge 
                    N03 = [nedge0[0], nedge0[4], nedge0[5], nedge0[6]]   ## Model 1st surface bottom edge 
                    N04 = [nedge0[1], nedge0[7], nedge0[8], nedge0[9]]   ## Model 1st surface bottom edge 

                    if debugmode ==1: 
                        print ("*******************************************************************************")
                        print ("* Edge %3d (on element= %d) Node (%d, %d), counting=%2d "%(i, sf[0]-10000000, N10[0]-1000_0000, N20[0]-1000_0000, counting))

                    ######################################################################################
                    ## check if the block edge is chamfered or not 
                    ## angle calculation of the first surface from top 

                    Nf1 = [tedge0[0], tedge0[4], tedge0[5], tedge0[6]]   ## Model Node 1
                    Nf2 = [tedge0[1], tedge0[7], tedge0[8], tedge0[9]]   ## Model Node 2
                    Nf3 = [nedge0[0], nedge0[4], nedge0[5], nedge0[6]]   ## Model Node 3
                    Nf4 = [nedge0[1], nedge0[7], nedge0[8], nedge0[9]]   ## Model Node 4

                    # def DistanceFromLineToNode2D(N0, nodes=[], xy=12):
                    df3, _ = DistanceFromLineToNode2D(Nf3,[Nf1, Nf2], xy=12)
                    df4, _ = DistanceFromLineToNode2D(Nf4,[Nf1, Nf2], xy=12)  
                    htf3 = round(Nf2[3]-Nf3[3], e_digit)
                    htf4 = round(Nf1[3]-Nf4[3], e_digit)

                    df3 = round(df3, e_digit); df4 = round(df4, e_digit)

                    ######################################################################
                    # if Nf3[0]-10**7 ==NOID  or Nf4[0]-10**7 == NOID: 
                    #     debugmode =1
                    # else: 
                    #     debugmode =0
                    ######################################################################

                    ## if the angle ==0, then skip this edge (going to next edge)
                    if round(df3, e_digit) ==0 and round(df4, e_digit) ==0: 
                        if debugmode ==1: 
                            print (" ** first surface is vertical(break), Distance from node to line : 3=%7.3f, 4=%7.3f"%(df3*1000, df4*1000))
                        break 
                        ## vertical --> going to next surface ..

                    ## if height is negative, this means the side surface goes up.. (it does not need to translate)
                    ## if height is too low, the surface is almost flat. 
                    #########################################################
                    # in case that the 1st surface ht. is too small (under 0.1mm)
                    # we can ignore it. 
                    ignore =1 
                    if ignore == 0: 
                        if htf3 <= surf_ht_margin or htf4 <= surf_ht_margin:  #3 surf_height margin = 0.1mm (current)
                            if debugmode ==1: print ("low margin ht ht 3=%7.3f, 4=%7.3f"%(htf3*1000, htf4*1000))
                            break   ## ht. is too low, regard the height 
                    ########################################################3
                    ## 1st groove side angle  (first side, e_digit=5)
                    fs4 = round(df4 / htf4, e_digit); fs3 = round(df3 / htf3, e_digit)    ## fs3 == tangent angle of the surface (length / height) 

                    if debugmode ==1:  
                        print (" ** 1st Surface (id=%6d) NID3=%6d, dist 3=%.3f, angle 3=%.3f"%(sf[0]-1000_0000, Nf3[0]-10000000, df3*1000, degrees(atan(fs3)) )) 
                        print ("                           NID4=%6d, dist 4=%.3f, angle 4=%.3f"%(Nf4[0]-10000000, df4*1000, degrees(atan(fs4)) ))

                    #######################################################################################################################
                    ## search the next edge and surface to distinguish if the 1st surface is a chamfer or not (by comparing their angles)
                    #######################################################################################################################
                    tmp_cedge0 = nedge0 
                    tmp_tedge0 = self.FindContactingEdge(tmp_cedge0, alledges0)
                    try: 
                        tnedge0, sf2 = self.FindAnotherEdgeInSurface(next=2, cedge=tmp_tedge0, edges=alledges0, surfaces=surfaces, sfreturn=1)
                        ending =0 
                    except:
                        ending = 1  ## no surface connected from the 1st surface, processing.. eventually it's going to be stopped.  

                    if abs(degrees(atan(fs3)) - degrees(atan(fs4))) > 1.0 and ending == 0 :  ## survived . this surface has next surface.. 
                        chamfer = 1 
                        if debugmode ==1: 
                            print ("   >> This 1st surface is a chamfer(slant), Node 2-3 angle=%6.1f, Node 1-4 angle=%6.1f"%(degrees(atan(fs3)), degrees(atan(fs4))))

                    if ending ==0: 
                        if debugmode ==1: 
                            print (" *******************************************************")
                            print (" ** second Edge checking")
                            print (" *******************************************************")


                        Ns1 = Nf4; Ns2 = Nf3
                        Ns3 = [tnedge0[0], tnedge0[4], tnedge0[5], tnedge0[6]]
                        Ns4 = [tnedge0[1], tnedge0[7], tnedge0[8], tnedge0[9]] 

                        ds3, _ = DistanceFromLineToNode2D(Ns3,[Ns1, Ns2], xy=12)
                        ds4, _ = DistanceFromLineToNode2D(Ns4,[Ns1, Ns2], xy=12)  
                        ds3 = round(ds3, e_digit); ds4 = round(ds4, e_digit)
                        hts3 = round(Ns2[3]-Ns3[3], e_digit)
                        hts4 = round(Ns1[3]-Ns4[3], e_digit)

                        if hts4 == 0 or hts3 ==0: 
                            if debugmode ==1: print (" >> Second surface is vertical --> skip, ht 3=%7.3f, 4=%7.3f"%(hts3*1000, hts4*1000))
                            break 

                        ss4 = round(ds4 / hts4, e_digit); ss3 = round(ds3 / hts3, e_digit)    ## second surface 3 => ss3 
                        if  abs(degrees(atan(fs4)) - degrees(atan(ss4))) > 1.0 and (htf3 <= 2.0E-03 and htf4 <= 2.0E-03): ## chamfer case  
                            ## the angles of the 1st and 2nd surfaces are differnet more than 1 degree 
                            ## (the ht. of the chamfer surface(ht f3 and f4 : f== first) should not be greater than 2.0mm)
                            if debugmode ==1:  
                                print (" This 1st surface is a chamfer, 1st Surf angle=%6.1f, 2nd Surf angle=%6.1f"%(degrees(atan(fs3)), degrees(atan(ss3))))
                            chamfer = 1  

                        if abs(degrees(atan(ss4)) - degrees(atan(ss3))) > 1.0: 
                            ## the angles of the 1st and 2nd surfaces are differnet more than 1 degree 
                            
                            if debugmode ==1:  print ("chamfer = %d, Angle SS3=%f, ss4=%f"%(chamfer, degrees(atan(ss3)), degrees(atan(ss4))), end=", ")
                            chamfer =0
                            if debugmode ==1:  print (" chamfer = %d"%(chamfer))
                            if degrees(atan(fs4)) > degrees(atan(ss4))+5 and degrees(atan(fs3)) > degrees(atan(ss3))+5: 
                                chamfer = 1

                        if debugmode ==1: 
                            print (" 2nd Surface (id=%6d) NID3=%6d, dist 3=%.3f, angle 3=%.3f"%(sf2[0]-1000_0000, Ns3[0]-10000000, ds3*1000, degrees(atan(ss3)) )) 
                            print ("                         NID4=%6d, dist 4=%.3f, angle 4=%.3f"%(Ns4[0]-10000000, ds4*1000, degrees(atan(ss4)) ))

                        ## for the 2nd surface.....
                        ## if the angle ==0  ==> if 1st angle is not 0,             then the 1st surface is a chamfer 
                        ## if the distance of the 2 nodes to the edge is different, then the 1st surface is a chamfer
                        ## if the angle is different from the 1st angle,            then the 1st surface is a chamfer
                        
                        ## if the angle ~ 90 ==> the 2nd surface is a bottom surface of the groove. ==> not a chamfer ==> processing 
                        ##              is the same with the 1st angle, not a chamfer ==> processing 

                        
                        if degrees(atan(ss4)) > 70.0: 
                            ending =1 
                    if debugmode ==1: 
                        if chamfer ==1: 
                            print (" EL ID %d is chamfered, ending=%d"%(sf[0]-1000_0000, ending))
                        else: 
                            print (" EL ID %d is not chamfered"%(sf[0]-1000_0000))
                    if chamfer ==1 and ending ==0:    ## change the chamfer option not to operate  .. ## in case of chamfered.  (this is still the 1st surface)
                        if debugmode ==1: 
                            print ("        1st surf Only Scaled N3=%6d, Dist=%.3f, ht=%.3f, angle=%.2f"%(Nf3[0]-10000000, df3*1000, htf3*1000, degrees(atan(df3/htf3))))
                            print ("        1st surf Only Scaled N4=%6d, Dist=%.3f, ht=%.3f, angle=%.2f"%(Nf4[0]-10000000, df4*1000, htf4*1000, degrees(atan(df4/htf4))))

                        indx = np.where(scalednode[:,0]==tedge[0])[0][0] 
                        n1 = scalednode[indx]
                        indx = np.where(scalednode[:,0]==tedge[1])[0][0] 
                        n2 = scalednode[indx]
                        indx = np.where(scalednode[:,0]==nedge[0])[0][0] 
                        n3 = scalednode[indx]
                        indx = np.where(scalednode[:,0]==nedge[1])[0][0] 
                        n4 = scalednode[indx]

                        model1stsurfht3 = htf3; model1stsurfht4 = htf4 
                        exp1stsurfht3 = n2[3] - n3[3]; exp1stsurfht4 = n1[3] - n4[3] 

                        if self.TargetGD > 1.0E-03: ## if layout mesh has the groove depth value 
                            del3z = model1stsurfht3 * (1 - self.TargetGD / self.ModelGD )   ## if self.Target is incorrect.. 
                            del4z = model1stsurfht4 * (1 - self.TargetGD / self.ModelGD )
                        else: 
                            del3z = 0.0
                            del4z = 0.0 

                        if chamfer_gauge == 0: 
                            del3z = 0.0
                            del4z = 0.0 
                        ## chamfer height adjustment #####################################
                        # if round(del3z, e_digit-1) ==0: 
                        #     if debugmode ==1: print("DEL 3Z.............")
                        #     del3x = 0; del3y = 0
                        #     done = 0
                        #     for cn in chfnode: 
                        #         if cn == n3[0]: 
                        #             done = 1
                        #     if done ==0: 
                        #         chfnode.append(n3[0])
                        #         NodeTranslated.append([n3[0], n3[1], n3[2], n3[3], 0.0, del3x, del3y, del3z, n4, 0])
                        #         addnodecounting += 1 
                        #     delx3=del3x; dely3=del3y; delz3= del3z    
                        # else:  
                        ######################################################################################
                        if  1:     
                            ## traslation is proportion to the 2nd surface of the expanded mesh 
                            if debugmode ==1: print("DEL 3Z.....>>>>>>>>>>>>........")
                            ce = nedge
                            te = self.FindContactingEdge(ce, alledges)
                            te = self.FindAnotherEdgeInSurface(next=2, cedge=te, edges=alledges, surfaces=surfaces)
                            ns1 = n4; ns2 = n3 
                            indx = np.where(scalednode[:,0]==te[0])[0][0] 
                            ns3 = scalednode[indx]
                            indx = np.where(scalednode[:,0]==te[1])[0][0] 
                            ns4 = scalednode[indx]
                            if round(ns2[3]-ns3[3], 5) < 0 or round(ns1[3]-ns4[3], 5) < 0:  
                                break 

                            ds, _ = DistanceFromLineToNode2D(ns3,[ns1, ns2], xy=12)
                            slope = ds/(ns2[3]-ns3[3])
                            if debugmode ==1: print("   DS3 = %.4f"%(ds*1000))

                            if slope> 2: 
                                print ("################################################################################")
                                print ("\tns1 %6d: %.3f, %.3f, %.3f"%(ns1[0]-1000_0000, ns1[1]*1000, ns1[2]*1000, ns1[3]*1000))
                                print ("\tns2 %6d: %.3f, %.3f, %.3f"%(ns2[0]-1000_0000, ns2[1]*1000, ns2[2]*1000, ns2[3]*1000))
                                print ("\tns3 %6d: %.3f, %.3f, %.3f"%(ns3[0]-1000_0000, ns3[1]*1000, ns3[2]*1000, ns3[3]*1000))
                                print ("\tns4 %6d: %.3f, %.3f, %.3f"%(ns4[0]-1000_0000, ns4[1]*1000, ns4[2]*1000, ns4[3]*1000))
                                print ("\tDIst from n3 to node = %.3f (ht=%.3f)"%(ds*1000,(ns2[3]-ns3[3])*1000))

                                indx = np.where(self.npn[:,0]==ns3[0])[0][0]
                                if debugmode ==1:  
                                    print ("\t ==> ns3 %6d: %.3f, %.3f, %.3f"%(self.npn[indx][0]-1000_0000, self.npn[indx][1]*1000, self.npn[indx][2]*1000, self.npn[indx][3]*1000))

                            if round(ds, e_digit) < 0.1E-03:       
                                del3x =0; del3y = 0
                                done=0
                                for cn in chfnode: 
                                    if cn == n3[0]: 
                                        done = 1
                                if done ==0: 
                                    chfnode.append(n3[0])
                                    NodeTranslated.append([n3[0], n3[1], n3[2], n3[3], 0.0, del3x, del3y, del3z, n4, 0])
                                    addnodecounting += 1
                                delx3=del3x; dely3=del3y; delz3= del3z
                            else: 
                                # vx = (ns3[1] - ns2[1]); vy = (ns3[2] - ns2[2])
                                # del3x = -vx * slope  * del3z;   del3y = -vy * slope * del3z
                                # delx3=del3x; dely3=del3y; delz3= del3z

                                vx = (N03[1] - N02[1]); vy = (N03[2] - N02[2]); vz = (N03[3] - N02[3])
                                TargetDx_fromN2 = vx * self.TargetTW / self.TreadDesignWidth
                                TargetDy_fromN2 = vy * self.TargetPL / self.pitchlength
                                # print ("Model PL=%7.3f, Target PL=%7.3f, ratio=%.2f"%(self.pitchlength, self.TargetPL, self.TargetPL / self.pitchlength))
                                # TargetDz_fromN2 = vz * sqrt(self.TargetTW**2 + self.TargetPL**2) / sqrt(self.TreadDesignWidth**2+self.pitchlength**2)

                                
                                done=0
                                for cn in chfnode: 
                                    if cn == n3[0]: 
                                        done = 1
                                if done ==0: 
                                    chfnode.append(n3[0])
                                    ind =  np.where(self.npn[:,0] == n2[0])[0][0]
                                    indx = np.where(self.npn[:,0] == n3[0])[0][0]
                                    Targetx = self.npn[ind][1] + TargetDx_fromN2
                                    Targety = self.npn[ind][2] + TargetDy_fromN2
                                    # Targetz = self.npn[ind][3] + TargetDz_fromN2

                                    del3x = Targetx - self.npn[indx][1]
                                    del3y = Targety - self.npn[indx][2]
                                    # del3z = Targetz - self.npn[indx][3]

                                    self.npn[indx][1] = Targetx
                                    self.npn[indx][2] = Targety
                                    # self.npn[indx][3] = Targetz

                                    # if debugmode ==1:    print ("       - New Translation %6d (%6d)"%(self.npn[indx][0]-10**7, n3[0]-10**7))
                                    
                                    del3x = 0; del3y=0; del3z = 0 
                                    NodeTranslated.append([n3[0], self.npn[indx][1], self.npn[indx][2], self.npn[indx][3], degrees(atan(slope)), del3x, del3y, del3z, n4, 0])
                                    addnodecounting += 1
                                    jndx = np.where(edges[:,0]==n3[0])[0]
                                    for dx in jndx: 
                                        edges[4] = self.npn[indx][1]
                                        edges[5] = self.npn[indx][2]
                                        edges[6] = self.npn[indx][3]
                                    jndx = np.where(edges[:,1]==n3[0])[0]
                                    for dx in jndx: 
                                        edges[7] = self.npn[indx][1]
                                        edges[8] = self.npn[indx][2]
                                        edges[9] = self.npn[indx][3]

                                    jndx = np.where(alledges[:,0]==n3[0])[0]
                                    for dx in jndx: 
                                        alledges[dx][4] = self.npn[indx][1]
                                        alledges[dx][5] = self.npn[indx][2]
                                        alledges[dx][6] = self.npn[indx][3]
                                    jndx = np.where(alledges[:,1]==n3[0])[0]
                                    for dx in jndx: 
                                        alledges[dx][7] = self.npn[indx][1]
                                        alledges[dx][8] = self.npn[indx][2]
                                        alledges[dx][9] = self.npn[indx][3]


                                    if debugmode ==1:     
                                        print ("        2nd surf Only Scaled N3=%6d, Dist=%.3f, ht=%.3f, angle=%.2f, Diaplacement N3 %6d, vx=%.3f, vy=%.3f del x3=%.3f, y3=%.3f, z4=0.0"%(ns3[0]-10000000, ds*1000, (ns2[3]-ns3[3])*1000, degrees(atan(slope)),\
                                        n3[0]-10**7, vx*1000, vy*1000, del3x*1000, del3y*1000))
                                else: 
                                    if debugmode ==1: print (" N3 Nodes is translated already")

                        if round(del4z, e_digit-1) ==0: 
                            if debugmode ==1: print("DEL 4Z.............")
                            del4x = 0; del4y = 0
                            done=0
                            for cn in chfnode: 
                                if cn == n4[0]: 
                                    done = 1
                            if done ==0: 
                                chfnode.append(n4[0])
                                NodeTranslated.append([n4[0], n4[1], n4[2], n4[3], 0.0, del4x, del4y, del4z, n3, 0])
                                addnodecounting += 1
                            
                            delx4=del4x; dely4=del4y; delz4= del4z
                        else: 
                            ## traslation is proportion to the 2nd surface of the expanded mesh 
                            if debugmode ==1: print("DEL 4Z.....>>>>>>>>>>>>........")
                            ce = nedge
                            te = self.FindContactingEdge(ce, alledges)
                            te = self.FindAnotherEdgeInSurface(next=2, cedge=te, edges=alledges, surfaces=surfaces)
                            ns1 = n4; ns2 = n3 
                            indx = np.where(scalednode[:,0]==te[0])[0][0] 
                            ns3 = scalednode[indx]
                            indx = np.where(scalednode[:,0]==te[1])[0][0] 
                            ns4 = scalednode[indx]
                            if round(ns2[3]-ns3[3], 5) < 0 or round(ns1[3]-ns4[3], 5) < 0:  
                                break 

                            ds, _ = DistanceFromLineToNode2D(ns4,[ns1, ns2], xy=12)
                            slope = ds/(ns1[3]-ns4[3])
                            if debugmode ==1: print("   DS4 = %.4f"%(ds*1000))
                            
                            if ds> 0.1: 
                                print ("################################################################################")
                                print ("\tns1 %6d: %.3f, %.3f, %.3f"%(ns1[0]-1000_0000, ns1[1]*1000, ns1[2]*1000, ns1[3]*1000))
                                print ("\tns2 %6d: %.3f, %.3f, %.3f"%(ns2[0]-1000_0000, ns2[1]*1000, ns2[2]*1000, ns2[3]*1000))
                                print ("\tns3 %6d: %.3f, %.3f, %.3f"%(ns3[0]-1000_0000, ns3[1]*1000, ns3[2]*1000, ns3[3]*1000))
                                print ("\tns4 %6d: %.3f, %.3f, %.3f"%(ns4[0]-1000_0000, ns4[1]*1000, ns4[2]*1000, ns4[3]*1000))
                                print ("\tDIst from n4 to node = %.3f (ht=%.3f)"%(ds*1000,(ns1[3]-ns4[3])*1000))

                                indx = np.where(self.npn[:,0]==ns4[0])[0][0]
                                print ("\t ==> ns4 %6d: %.3f, %.3f, %.3f"%(self.npn[indx][0]-1000_0000, self.npn[indx][1]*1000, self.npn[indx][2]*1000, self.npn[indx][3]*1000))

                            if round(ds, e_digit) < 0.1E-03:  
                                del4x =0; del4y = 0
                                for cn in chfnode: 
                                    if cn == n3[0]: 
                                        done = 1
                                if done ==0: 
                                    chfnode.append(n4[0])
                                    NodeTranslated.append([n4[0], n4[1], n4[2], n4[3], 0.0, del4x, del4y, del4z, n3, 0])
                                    addnodecounting += 1
                                delx4=del4x; dely4=del4y; delz4= del4z
                            else: 
                                # vx = (ns4[1] - ns2[1]); vy = (ns4[2] - ns1[2])
                                # del4x = -vx * slope * del4z;   del4y = -vy * slope  * del4z
                                # delx4=del4x; dely4=del4y; delz4= del4z
                                vx = (N04[1] - N01[1]); vy = (N04[2] - N01[2]); vz = (N04[3] - N01[3])
                                TargetDx_fromN1 = vx * self.TargetTW / self.TreadDesignWidth
                                TargetDy_fromN1 = vy * self.TargetPL / self.pitchlength
                                # TargetDz_fromN1 = vz * sqrt(self.TargetTW**2 + self.TargetPL**2) / sqrt(self.TreadDesignWidth**2+self.pitchlength**2)

                                
                                done=0
                                for cn in chfnode: 
                                    if cn == n4[0]: 
                                        done = 1
                                if done ==0: 
                                    chfnode.append(n4[0])
                                    ind =  np.where(self.npn[:,0] == n1[0])[0][0]
                                    indx = np.where(self.npn[:,0] == n4[0])[0][0]
                                    Targetx = self.npn[ind][1] + TargetDx_fromN1
                                    Targety = self.npn[ind][2] + TargetDy_fromN1
                                    # Targetz = self.npn[ind][3] + TargetDz_fromN1

                                    del4x = Targetx - self.npn[indx][1]
                                    del4y = Targety - self.npn[indx][2]
                                    # del4z = 0

                                    self.npn[indx][1] = Targetx
                                    self.npn[indx][2] = Targety
                                    # self.npn[indx][3] = Targetz
                                    
                                    del4x = 0; del4y=0; del4z = 0 
                                    NodeTranslated.append([n4[0], self.npn[indx][1], self.npn[indx][2], self.npn[indx][3], degrees(atan(slope)), del4x, del4y, del4z, n3, 0])
                                    addnodecounting += 1

                                    jndx = np.where(edges[:,0]==n4[0])[0]
                                    for dx in jndx: 
                                        edges[dx][4] = self.npn[indx][1]
                                        edges[dx][5] = self.npn[indx][2]
                                        edges[dx][6] = self.npn[indx][3]
                                    jndx = np.where(edges[:,1]==n4[0])[0]
                                    for dx in jndx: 
                                        edges[dx][7] = self.npn[indx][1]
                                        edges[dx][8] = self.npn[indx][2]
                                        edges[dx][9] = self.npn[indx][3]

                                    jndx = np.where(alledges[:,0]==n4[0])[0]
                                    for dx in jndx: 
                                        alledges[dx][4] = self.npn[indx][1]
                                        alledges[dx][5] = self.npn[indx][2]
                                        alledges[dx][6] = self.npn[indx][3]
                                    jndx = np.where(alledges[:,1]==n4[0])[0]
                                    for dx in jndx: 
                                        alledges[dx][7] = self.npn[indx][1]
                                        alledges[dx][8] = self.npn[indx][2]
                                        alledges[dx][9] = self.npn[indx][3]

                                    if debugmode ==1: 
                                        print ("        2nd surf Only Scaled N4=%6d, Dist=%.3f, ht=%.3f, angle=%.2f, Displacement N4 %6d, vx=%.3f, vy=%.3f del x4=%.3f, y4=%.3f, z4=0.0"%(ns4[0]-10000000, ds*1000, (ns1[3]-ns4[3])*1000, degrees(atan(slope)), \
                                            n4[0]-10**7, vx*1000, vy*1000, del4x*1000, del4y*1000))
                                else: 
                                    if debugmode ==1: print (" N4 Nodes is translated already")
                        if debugmode ==1:
                            print ("** Final Node displacement")
                            # print ("         *>> DID3=%d, Del 3x=%.3f, 3y=%.3f, 3z=%.3f"%(n3[0]-1000_0000, del3x*1000, del3y*1000, del3z*1000))
                            print ("         *>> NID4=%d, Del 4x=%.3f, 4y=%.3f, 4z=%.3f"%(n4[0]-1000_0000, del4x*1000, del4y*1000, del4z*1000))
                        case1 +=1
                        ## 2nd surface is going to be the base surface for transition (like the top surface)
                        cedge = nedge
                        cedge0 = nedge0

                        nn3 = 0; nn4=0
                        for nd in NodeTranslated: 
                            if nd[0] == n3[0]: nn3+=1
                            if nd[0] == n4[0]: nn4+=1
                        if nn3>2 or nn4>2: 
                            print ("\n ### N3=%d, count=%d, N4=%d, count=%d"%(n3[0]-10000000, nn3, n4[0]-10000000, nn4))
                            # sys.exit()
                        continue 
                    else:
                        chamfer = 0
                        if debugmode ==1: 
                            print ("*********** Not chamfered (EL ID=%d)"%(sf[0]-1000_0000 ))

                else: 
                    N1 = N4
                    N2 = N3 

                indx = np.where(scalednode[:,0]==nedge[0])[0][0] 
                N3 = [scalednode[indx][0], scalednode[indx][1], scalednode[indx][2], scalednode[indx][3] ]
                indx = np.where(scalednode[:,0]==nedge[1])[0][0] 
                N4 = [scalednode[indx][0], scalednode[indx][1], scalednode[indx][2], scalednode[indx][3] ]

                N03 = [nedge0[0], nedge0[4], nedge0[5], nedge0[6]]        
                N04 = [nedge0[1], nedge0[7], nedge0[8], nedge0[9]]

                ######################################################################
                # if edge[0]-10**7 == NOID or edge[1]-10**7 == NOID or edge[0]-10**7 == 6428 or edge[1]-10**7 == 6428: 
                #     debugmode =1
                # else: 
                #     debugmode =0
                ######################################################################

                if round(N20[1] - N10[1], 7) == 0: 
                    d3 = abs(N3[1] - N10[1]);              d4 = abs(N4[1] - N10[1]);              d03 = abs(N03[1] - N01[1]);                 d04 = abs(N04[1] - N01[1])
                elif round(N20[2]-N10[2], 7) == 0 : 
                    d3 = abs(N3[2] - N10[2]);              d4 = abs(N4[2] - N10[2]);              d03 = abs(N03[2] - N01[2]);                 d04 = abs(N04[2] - N01[2])
                else: 
                    a = (N20[2] - N10[2]) / (N20[1] - N10[1]) 
                    A = -a 
                    C = a * N10[1] - N10[2] 

                    a0 = (N02[2] - N01[2]) / (N02[1] - N01[1]) 
                    A0 = -a0 
                    C0 = a0 * N01[1] - N01[2] 

                    ## distance 
                    d3 = abs(A*N3[1]+N3[2]+C) / sqrt(A*A + 1)
                    d4 = abs(A*N4[1]+N4[2]+C) / sqrt(A*A + 1)
                    d03 = abs(A0*N03[1]+N03[2]+C0) / sqrt(A0*A0 + 1)
                    d04 = abs(A0*N04[1]+N04[2]+C0) / sqrt(A0*A0 + 1)
                
                #######################################
                h3 = round(N20[3] - N3[3],6)
                h4 = round(N10[3] - N4[3],6)

                h03 =round(N02[3] - N03[3],6)
                h04 =round(N01[3] - N04[3],6)

                if N2[3] - N3[3] < surf_ht_margin or N1[3] - N4[3] < surf_ht_margin: 
                    # if debugmode ==1: 
                    #     print ("  >>  Reached bottom (%d) : N10=%d, N20=%d, N1=%d, N2=%d, N3=%d, N4=%d, h03=%.3f, h04=%.3f"%(counting, N10[0]-1000_0000, N20[0]-1000_0000, N1[0]-1000_0000, N2[0]-1000_0000, N3[0]-1000_0000,N4[0]-1000_0000, h03*1000, h04*1000))
                    BottomEdgeNodes.append([tedge[3], tedge[0], tedge[1], [N1[0], N1[1], N1[2], N1[3]], [N2[0], N2[1], N2[2], N2[3]]])
                    # print (maingroovebottomedge[0])
                    indxs1 = np.where(maingroovebottomedge[:,0] == tedge[0])[0]
                    indxs2 = np.where(maingroovebottomedge[:,1] == tedge[1])[0]
                    indxs = np.intersect1d(indxs1, indxs2)
                    if len(indxs) ==1: 
                        NN = len(NodeTranslated)-1
                        for nnct in range(addnodecounting): 
                            NodeTranslated[NN-nnct][9] = 1 
                    
                    break 

                ## initial Angle 
                AO3 = degrees(atan((d03)/(h03)))
                AO4 = degrees(atan((d04)/(h04)))
                
                if AO3 >groove_angle_margin or AO4 > groove_angle_margin :  ## if groove angle is too big
                    BottomEdgeNodes.append([tedge[3], tedge[0], tedge[1], [N1[0], N1[1], N1[2], N1[3]], [N2[0], N2[1], N2[2], N2[3]]])
                    indxs1 = np.where(maingroovebottomedge[:,0] == tedge[0])[0]
                    indxs2 = np.where(maingroovebottomedge[:,1] == tedge[1])[0]
                    indxs = np.intersect1d(indxs1, indxs2)
                    if len(indxs) ==1: 
                        NN = len(NodeTranslated)-1
                        for nnct in range(addnodecounting): 
                            NodeTranslated[NN-nnct][9] = 1 
                    
                    if debugmode ==1: 
                        print ("  >>>  Reached bottom (%d, element=%d) : N10=%d, N20=%d, N1=%d, N2=%d, N3=%d, N4=%d angle 3=%.1f, 4=%.1f"%(counting, sf[0]-10000000, N10[0]-1000_0000, N20[0]-1000_0000, N1[0]-1000_0000, N2[0]-1000_0000, N3[0]-1000_0000,N4[0]-1000_0000, AO3, AO4))
                    
                    break 
                
                #######################################
                if debugmode ==1:
                
                    if sf[0]-1000_0000== ShowN1 or sf[0]-1000_0000== ShowN2: 
                        print ("**************************************************************")
                        print ("Surface %d"%(sf[0]-1000_0000))
                        print ("N01: model X=%7.3f, y=%7.3f, z=%7.3f"%(N01[1]*1000, N01[2]*1000, N02[3]*1000))
                        print ("N02: model X=%7.3f, y=%7.3f, z=%7.3f\n"%(N02[1]*1000, N02[2]*1000, N02[3]*1000))
                        print ("N03: model X=%7.3f, y=%7.3f, z=%7.3f, ht=%7.3f"%(N03[1]*1000, N03[2]*1000, N03[3]*1000, h03*1000))
                        print ("N04: model X=%7.3f, y=%7.3f, z=%7.3f, ht=%7.3f\n"%(N04[1]*1000, N04[2]*1000, N04[3]*1000, h04*1000))
                        print ("**************************************************************")
                        print ("N1: defm X=%7.3f, y=%7.3f, z=%7.3f"%(N1[1]*1000, N1[2]*1000, N1[3]*1000))
                        print ("N2: defm X=%7.3f, y=%7.3f, z=%7.3f\n"%(N2[1]*1000, N2[2]*1000, N2[3]*1000))
                        print ("N3: defm X=%7.3f, y=%7.3f, z=%7.3f, ht=%7.3f"%(N3[1]*1000, N3[2]*1000, N3[3]*1000, h3*1000))
                        print ("N4: defm X=%7.3f, y=%7.3f, z=%7.3f, ht=%7.3f\n"%(N4[1]*1000, N4[2]*1000, N4[3]*1000, h4*1000))

                # self.TargetGD <= self.ModelGD: 
                horver = 0 
                v3x = 0; v3y=0; v4x=0; v4y=0
                ratio3=0; ratio4=0
                TargetDist3 = h3 * d03 / h03
                TargetDist4 = h4 * d04 / h04
                # DelDist3 = abs(TargetDist3 - d3 )
                # DelDist4 =abs(TargetDist4 - d4 )

                DelDist3 = d3 - TargetDist3 
                DelDist4 = d4 - TargetDist4 

                # print ("**   N3 Target Dist=%7.3f, current Dist=%7.3f (Del=%7.3f)(Model GD=%.1f, Target GD=%.1f)"%(TargetDist3*1000, d3*1000, (TargetDist3-d3)*1000, self.ModelGD, self.TargetGD), end=", ")

                if round(N02[1] - N01[1], 4) == 0: 
                    if N03[1] > N02[1]: DelDist3 = -DelDist3
                    if N04[1] > N01[1]: DelDist4 = -DelDist4
                    # if self.ModelGD > self.TargetGD: 
                    #     DelDist3 = -DelDist3
                    #     DelDist4 = -DelDist4

                    New3x = N3[1] + DelDist3 
                    New3y = N3[2] 
                    New4x = N4[1] + DelDist4 
                    New4y = N4[2]  
                    Delx3 = DelDist3 
                    Dely3 = 0
                    Delx4 = DelDist4 
                    Dely4 = 0

                    # print (" Vertical N1[1] = %.3f, N2[1]= %.3f"%(N10[1], N20[1]))
                    horver =1
                    if debugmode ==1: 
                        print ("## case I")
                        print ('      Node 3(%6d) : Del distance =%.3f'%(N3[0]-10**7, DelDist3*1000))
                        print ('      Node 4(%6d) : Del distance =%.3f'%(N4[0]-10**7, DelDist4*1000))
                        
                
                elif round(N02[2]-N01[2], 4) == 0 : 
                    if N03[2] > N02[2]: DelDist3 = -DelDist3
                    if N04[2] > N01[2]: DelDist4 = -DelDist4
                    # if self.ModelGD > self.TargetGD: 
                    #     DelDist3 = -DelDist3
                    #     DelDist4 = -DelDist4

                    New3x = N3[1] 
                    New3y = N3[2]  + DelDist3
                    New4x = N4[1] 
                    New4y = N4[2]  + DelDist4

                    Delx3 = 0 
                    Dely3 = DelDist3
                    Delx4 = 0 
                    Dely4 = DelDist4
                    horver =1
                    if debugmode ==1: 
                        print ("## case II-1")
                        print ('      Node 3(%6d) : Del distance =%.3f'%(N3[0]-10**7, DelDist3*1000))
                        print ('      Node 4(%6d) : Del distance =%.3f'%(N4[0]-10**7, DelDist4*1000))
                        
                else: 
                    ## intersection point cx, cy 
                    cx3 = (a * (a*N10[1] - N10[2]) +     (N3[1] + a * N3[2]) )/ (1 + a*a)
                    cy3 = (-   (a*N10[1] - N10[2]) + a * (N3[1] + a * N3[2]) )/ (1 + a*a)
                    cx4 = (a * (a*N10[1] - N10[2]) +     (N4[1] + a * N4[2]) )/ (1 + a*a)
                    cy4 = (-   (a*N10[1] - N10[2]) + a * (N4[1] + a * N4[2]) )/ (1 + a*a)

                    v3x = abs(N3[1] - cx3 )
                    v3y = abs(N3[2] - cy3 )
                    v4x = abs(N4[1] - cx4 )
                    v4y = abs(N4[2] - cy4 )

                    if d3 == 0: 
                        Delx3= 0; Dely3=0
                    else: 
                        Delx3 = v3x * (1-TargetDist3/d3)
                        Dely3 = v3y * (1-TargetDist3/d3)
                    if d4 ==0: 
                        Delx4 = 0; Dely4 = 0
                    else: 
                        Delx4 = v4x * (1-TargetDist4/d4)
                        Dely4 = v4y * (1-TargetDist4/d4)

                    if N3[1] > cx3: Delx3=-Delx3
                    if N3[2] > cy3: Dely3=-Dely3
                    if N4[1] > cx4: Delx4=-Delx4
                    if N4[2] > cy4: Dely4=-Dely4

                    New3x = N3[1] + Delx3 
                    New3y = N3[2] + Dely3 
                    New4x = N4[1] + Delx4 
                    New4y = N4[2] + Dely4

                    # debugmode =1 
                    if debugmode ==1: 
                        print ("## case II-2")
                        print ('      Node 3(%6d) : Del distance =%.3f'%(N3[0]-10**7, (TargetDist3-d3)*1000))
                        print ('      Node 4(%6d) : Del distance =%.3f'%(N4[0]-10**7, (TargetDist4-d4)*1000))
                        
                        print ("      Del3x=%7.3f, 3y=%7.3f, Del4x=%7.3f, 4y=%7.3f"%(Delx3*1000, Dely3*1000, Delx4*1000, Dely4*1000))
                        print ("     * Scaled Position ")
                        print ("      N1 x=%7.3f, y=%7.3f, z=%7.3f"%(N1[1]*1000, N1[2]*1000, N1[3]*1000))
                        print ("      N2 x=%7.3f, y=%7.3f, z=%7.3f"%(N2[1]*1000, N2[2]*1000, N2[3]*1000))
                        print ("      N3 x=%7.3f, y=%7.3f, z=%7.3f"%(N3[1]*1000, N3[2]*1000, N3[3]*1000))
                        print ("      N4 x=%7.3f, y=%7.3f, z=%7.3f"%(N4[1]*1000, N4[2]*1000, N4[3]*1000))
                        print ("  New N3 x=%7.3f, y=%7.3f, z=%7.3f"%(New3x*1000, New3y*1000, N3[3]*1000))
                        print ("  New N4 x=%7.3f, y=%7.3f, z=%7.3f"%(New4x*1000, New4y*1000, N4[3]*1000))
                        print ('      v3x=%7.3f, v3y=%7.3f, v4x=%7.3f, v4y=%7.3f'%(v3x*1000, v3y*1000, v4x*1000, v4y*1000))
                        print ("      Target Dist 3=%7.3f, 4=%7.3f, Model Dist 3=%7.3f, 4=%7.3f"%(TargetDist3*1000, TargetDist4*1000, d3*1000, d4*1000))
                        print ("                                          Del dist 3=%7.3f, 4=%7.3f"%((TargetDist3-d3)*1000, (TargetDist4-d4)*1000))
                    # debugmode = 0

                        if N3[0]-1000_0000== NOID or N4[0]-1000_0000== NOID:
                            if N3[0]-1000_0000== NOID:    print (" Node %d, N3"%(NOID))
                            else: print  (" Node %d, N4"%(NOID))
                            if N3[0]-1000_0000== NOID: 
                                print ('* Target Distance 3=%7.3f, Current Distance 3=%7.3f'%(TargetDist3*1000,  d3*1000))   
                                print ("* Intersection Point 3x=%7.3f, 3y=%7.3f"%(cx3*1000, cy3*1000))
                                print ("  Del                3x=%7.3f, 3y=%7.3f"%(Delx3*1000, Dely3*1000))
                                print ("  Initial Position  x=%7.3f, y=%7.3f "%(N3[1]*1000, N3[2]*1000))
                                print ("  Transit Position  x=%7.3f, y=%7.3f "%(New3x*1000, New3y*1000))
                                print ("  Top Surface edge line inclination on 2D = %.2f"%(a))
                                print ("  vector 3 x=%7.3f, y=%7.3f, vector ratio=%7.3f"%(v3x*1000, v3y*1000, TargetDist3/d3))
                                print ("  Target Surface Ht= %7.3f, Distance from point 3=%7.3f, Inclination=%6.2f"%(h3*1000, d3*1000, degrees(atan(d3/h3))))
                                print ("   Model Surface Ht= %7.3f, Distance from point 3=%7.3f, Inclination=%6.2f"%(h03*1000, d03*1000, degrees(atan(d03/h03))))
                                print ("\n N10=%6d: X=%7.3f, y=%7.3f, z=%7.3f"%(N10[0]-1000_0000, N10[1]*1000, N10[2]*1000, N20[3]*1000))
                                print (" N20=%6d: X=%7.3f, y=%7.3f, z=%7.3f\n"%(N20[0]-1000_0000, N20[1]*1000, N20[2]*1000, N20[3]*1000))
                                print (" N3=%6d: X=%7.3f, y=%7.3f, z=%7.3f"%(N3[0]-1000_0000, N3[1]*1000, N3[2]*1000, N3[3]*1000))
                                print (" N4=%6d: X=%7.3f, y=%7.3f, z=%7.3f\n"%(N4[0]-1000_0000, N4[1]*1000, N4[2]*1000, N4[3]*1000))
                                print (" N1=%6d: X=%7.3f, y=%7.3f, z=%7.3f"%(N1[0]-1000_0000, N1[1]*1000, N1[2]*1000, N2[3]*1000))
                                print (" N2=%6d: X=%7.3f, y=%7.3f, z=%7.3f"%(N2[0]-1000_0000, N2[1]*1000, N2[2]*1000, N2[3]*1000))
                                
                            else: 
                                print ('* Target Distance 4=%7.3f, Current Distance 4=%7.3f'%(TargetDist4*1000,  d4*1000))  
                                print ("* Intersection Point 4x=%7.3f, 4y=%7.3f"%(cx4*1000, cy4*1000))
                                print ("  Del                4x=%7.3f, 4y=%7.3f"%(Delx4*1000, Dely4*1000))
                                print ("  Initial Position   x=%7.3f, y=%7.3f "%(N4[1]*1000, N4[2]*1000))
                                print ("  Transit Position   x=%7.3f, y=%7.3f "%(New4x*1000, New4y*1000))
                                print ("  Top edge line inclination on 2D = %.2f"%(a))
                                print ("  vector 4 x=%7.3f, y=%7.3f, vector ratio=%7.3f"%(v4x*1000, v4y*1000, TargetDist4/d4))
                                print ("  Target Surface Ht= %7.3f, Distance from point 4=%7.3f, Inclination=%6.2f"%(h4*1000, d4*1000, degrees(atan(d4/h4))))
                                print ("   Model Surface Ht= %7.3f, Distance from point 4=%7.3f, Inclination=%6.2f"%(h04*1000, d04*1000,degrees(atan(d04/h04))))
                                print ("\n N10=%6d: X=%7.3f, y=%7.3f, z=%7.3f"%(N10[0]-1000_0000, N10[1]*1000, N10[2]*1000, N20[3]*1000))
                                print (" N20=%6d: X=%7.3f, y=%7.3f, z=%7.3f\n"%(N20[0]-1000_0000, N20[1]*1000, N20[2]*1000, N20[3]*1000))
                                print (" N3=%6d: X=%7.3f, y=%7.3f, z=%7.3f"%(N3[0]-1000_0000, N3[1]*1000, N3[2]*1000, N3[3]*1000))
                                print (" N4=%6d: X=%7.3f, y=%7.3f, z=%7.3f\n"%(N4[0]-1000_0000, N4[1]*1000, N4[2]*1000, N4[3]*1000))
                                print (" N1=%6d: X=%7.3f, y=%7.3f, z=%7.3f"%(N1[0]-1000_0000, N1[1]*1000, N1[2]*1000, N2[3]*1000))
                                print (" N2=%6d: X=%7.3f, y=%7.3f, z=%7.3f"%(N2[0]-1000_0000, N2[1]*1000, N2[2]*1000, N2[3]*1000))
                
                NodeTranslated.append([N3[0], New3x, New3y, N3[3], AO3, Delx3, Dely3, 0.0, N4, 0]) 
                addnodecounting += 1
                NodeTranslated.append([N4[0], New4x, New4y, N4[3], AO4, Delx4, Dely4, 0.0, N3, 0])
                addnodecounting += 1
                if debugmode ==1: 
                    print ("      Del 3x=%.3f, 3y=%.3f, 3z=0.0, 4x=%.3f, 4y=%.3f, 4z=0.0"%(Delx3*1000, Dely3*1000, Delx4*1000, Dely4*1000))
                    print ('      Model vector 3x=%.3f, 3y=%.3f, N03[1]=%.3f (N02[1]=%.3f, N03[2]=%.3f, N02[2]=%.3f)'%(v3x*1000, v3y*1000, N03[1]*1000, N02[1]*1000, N03[2]*1000, N02[2]*1000)) 
                    print ('      Model vector 4x=%.3f, 4y=%.3f, N04[1]=%.3f (N01[1]=%.3f, N04[2]=%.3f, N01[2]=%.3f)'%(v4x*1000, v4y*1000, N04[1]*1000, N01[1]*1000, N04[2]*1000, N01[2]*1000)) 
                    print ("      Model Node 3 : height =%7.3f, Distance =%7.3f, Angle=%5.1f"%(h03*1000, d03*1000, AO3))
                    print ("      Model Node 4 : height =%7.3f, Distance =%7.3f, Angle=%5.1f"%(h04*1000, d04*1000, AO4))
                
                case2+=1 

                ## check the number of nodes in the list 
                # nn3 = 0; nn4=0
                # for nd in NodeTranslated: 
                #     if nd[0] == N3[0]: nn3+=1
                #     if nd[0] == N4[0]: nn4+=1
                # if nn3>2 or nn4>2: 
                #     print ("\n\n\n ### N3=%d, count=%d, N4=%d, count=%d"%(N3[0]-10000000, nn3, N4[0]-10000000, nn4))
                ##############################################################################################################
                # print ("Displacement N3, x=%7.3f, y=%7.3f (length=%7.3f)"%(Delx3*1000, Dely3*1000, sqrt(Delx3**2+Dely3**2)*1000))
                    
                cedge = nedge
                cedge0= nedge0
        print ("* Node translation Type. \n  Total edges=%d (Chamfer=%d, normal=%d)"%(len(edges), case1, case2))
        case1=0; case21=0; case22=0; case23=0; case24=0; case241=0; case242=0; case243=0 
        
        # debugmode = 0 

        # if edge[0]-10**7 == NOID or edge[1]-10**7 == NOID or edge[0]-10**7 == 6428 or edge[1]-10**7 == 6428: 
        #     debugmode =1
        # else: 
        #     debugmode =0
        # sys.exit()
        if len(NodeTranslated) == 0 : 
            print ("## No groove side node to move")
            return [], [], []
        # [print (ND) for ND in NodeTranslated]
        NodeTranslated = sorted(NodeTranslated, key=lambda node: node[0])
        # NodeTranslated = np.array(NodeTranslated)
        NoNodes=[]
        for ND in NodeTranslated: 
            NoNodes.append(ND[0])
        # NoNodes=NodeTranslated[:,0]
        NoNodes=np.unique(NoNodes)
        # print (NoNodes[:10])
        # print ("## %d(%d) groove side nodes are moved"%(len(NoNodes), len(NodeTranslated)))

        nodecounting = []
        prev=NodeTranslated[0][0]
        NN = len(NodeTranslated)
        cnt = 0
        for i, nd in enumerate(NodeTranslated): 
            if nd[0] == prev:     
                cnt += 1
                # print (" %d, "%(int(nd[0]-1000_0000)), end="")
            else: 
                nodecounting.append([prev, cnt, i])
                # print (" ==> N=%d\n %d,"%(cnt, int(nd[0]-1000_0000)), end="")
                cnt = 1
                prev=nd[0]

            
            if i == NN -1 and nd[0] == prev: 
                nodecounting.append([prev, cnt, i+1])
                # print (cnt)
                # if cnt >2:print ("counting =%d"%(cnt))
        
        ## node adjustment because of the sharing node on more than 1 surface 
        # debugmode =0
        if debugmode ==1: 
            NOID=3505
            swn1 = NOID
            idx = np.where(self.npn[:,0] == swn1+1000_0000)[0][0]
            print ("## Node %d, fin X=%7.3f, y=%7.3f, ht=%7.3f"%(swn1, self.npn[idx][1]*1000, self.npn[idx][2]*1000, self.npn[idx][3]*1000))
            NOID=2706
            swn2 =  NOID
            idx = np.where(self.npn[:,0] == swn2+1000_0000)[0][0]
            print ("## Node %d, fin X=%7.3f, y=%7.3f, ht=%7.3f"%(swn2, self.npn[idx][1]*1000, self.npn[idx][2]*1000, self.npn[idx][3]*1000))
        # debugmode = 0 

        pv_node=[]
        cnode=[]
        fnode=[]
        anglestd = 10.0
        # n4032v=[]
        self.TranslatedNode =[]
        lim = 0.1E-03 
        nodeprint = 0 

        nodecnt1 = []
        nodecnt2 =[]
        tmpcount = 0
        

        for cnd in nodecounting:
    
            ind = np.where(self.npn[:, 0] == cnd[0])[0][0] 
            
            if  cnd[1] == 1:
                if debugmode ==1: 
                    if swn1+1000_0000 == self.npn[ind][0] or swn2 +1000_0000== self.npn[ind][0]: 
                        print ("* 1 Node Transition : %d, %.3f, %.3f, %.3f"%(self.npn[ind][0]-1000_0000,self.npn[ind][1]*1000,self.npn[ind][2]*1000,self.npn[ind][3]*1000))
                        print ("  Node translated %d, %.3f, %.3f, %.3f"%(NodeTranslated[cnd[2]-cnd[1]][0]-10000000, NodeTranslated[cnd[2]-cnd[1]][1]*1000, NodeTranslated[cnd[2]-cnd[1]][2]*1000, NodeTranslated[cnd[2]-cnd[1]][3]*1000))

                self.TranslatedNode.append([self.npn[ind][0], NodeTranslated[cnd[2]-cnd[1]][5], NodeTranslated[cnd[2]-cnd[1]][6], NodeTranslated[cnd[2]-cnd[1]][7]])
                # self.npn[ind][1] += NodeTranslated[cnd[2]-cnd[1]][5]
                # self.npn[ind][2] += NodeTranslated[cnd[2]-cnd[1]][6]

                self.npn[ind][1] = NodeTranslated[cnd[2]-cnd[1]][1]
                self.npn[ind][2] = NodeTranslated[cnd[2]-cnd[1]][2]
                # self.npn[ind][3] = NodeTranslated[cnd[2]-cnd[1]][3]

                case1 += 1

                # if  self.npn[ind][0]-10000000 == 4881: 
                #     print (">> NODE %d : %.3f, %.3f"%(self.npn[ind][0]-10000000, self.npn[ind][1]*1000, self.npn[ind][2]*1000))

                pv_node.append([NodeTranslated[cnd[2]-cnd[1]][0], NodeTranslated[cnd[2]-cnd[1]][1], NodeTranslated[cnd[2]-cnd[1]][2], NodeTranslated[cnd[2]-cnd[1]][3]])
                nodecnt1.append(self.npn[ind][0])
                # print ("%d"%(NodeTranslated[cnd[2]-cnd[1]][0]))

                # if  self.npn[ind][0]-10**7 == 6313 or  self.npn[ind][0]-10**7 == 6317 or  self.npn[ind][0]-10**7 == 6427 or  self.npn[ind][0]-10**7 == 6449:  
                #     print (" 1 DEL  %d, %.3f, %.3f, %.3f"%(self.npn[ind][0]-10**7,(NodeTranslated[cnd[2]-cnd[1]][5])*1000, (NodeTranslated[cnd[2]-cnd[1]][6])*1000, (NodeTranslated[cnd[2]-cnd[1]][7])*1000))     
            elif cnd[1] == 2: 
                # indexes = [self.npn[ind][0], 2, 2]
                c21, c22, c23, c40,  c41, c42, c43, nodecnt2 = self.Grooveside_2NodeTranslation(ind, NodeTranslated, cnd, nodecnt2)
                case21 += c21
                case22 += c22
                case23 += c23
                case24 += c40
                case241 += c41 
                case242 += c42 
                case243 += c43 
            else: 
                # print ("many nodes need to check ...  (%d): "%(cnd[1]), end="")
                # check if their displacements are the same or not 
                cnt = 0 
                dff = 0 
                for i in range(cnd[2]-cnd[1], cnd[2]):
                    cnt += 1 
                    if cnt == 1: 
                        vx=NodeTranslated[i][5]; vy=NodeTranslated[i][6]; vz=NodeTranslated[i][7]
                        continue 
                    if abs(vx-NodeTranslated[i][5]) > 0.01E-03 or abs(vy-NodeTranslated[i][6]) > 0.01E-03 or abs(vz-NodeTranslated[i][7]) > 0.01E-03 : 
                        dff = 1 
                    vx=NodeTranslated[i][5]; vy=NodeTranslated[i][6]; vz=NodeTranslated[i][7]

                if dff == 0: 
                    self.TranslatedNode.append([self.npn[ind][0], NodeTranslated[cnd[2]-cnd[1]][5], NodeTranslated[cnd[2]-cnd[1]][6], NodeTranslated[cnd[2]-cnd[1]][7]])
                    self.npn[ind][1] = NodeTranslated[cnd[2]-cnd[1]][1]
                    self.npn[ind][2] = NodeTranslated[cnd[2]-cnd[1]][2]
                    case1 += 1

                    pv_node.append([NodeTranslated[cnd[2]-cnd[1]][0], NodeTranslated[cnd[2]-cnd[1]][1], NodeTranslated[cnd[2]-cnd[1]][2], NodeTranslated[cnd[2]-cnd[1]][3]])
                    nodecnt1.append(self.npn[ind][0])
                    continue 

                trans = []
                k=0 
                for i in range(cnd[2]-cnd[1], cnd[2]):
                    k += 1 
                    if k ==1: 
                        trans.append(NodeTranslated[i])
                    else: 
                        exist = 0 
                        for tns in trans: 
                            if abs(tns[5] - NodeTranslated[i][5]) <0.01E-03  and  abs(tns[6] - NodeTranslated[i][6]) <0.01E-03: 
                            # if round(tns[5], 5) == round(NodeTranslated[i][5],5) and round(tns[6],5) == round(NodeTranslated[i][6],5) : 
                                exist =1
                                break 
                        if exist == 0: 
                            trans.append(NodeTranslated[i])
                if len(trans) == 1: 
                    self.npn[ind][1] += trans[0][5]
                    self.npn[ind][2] += trans[0][6]
                    self.TranslatedNode.append([self.npn[ind][0], self.npn[ind][1] - trans[0][5], self.npn[ind][2] - trans[0][6], 0.0])
                    continue 
                elif len(trans) ==2: 
                    indexes = [self.npn[ind][0], 2, 2]
                    c21, c22, c23, c40, c41, c42, c43, nodecnt2 = self.Grooveside_2NodeTranslation(ind, trans,indexes, nodecnt2)
                    case21 += c21
                    case22 += c22
                    case23 += c23
                    case24 += c40
                    case241 += c41 
                    case242 += c42 
                    case243 += c43 
                    continue 


                print ("many nodes need to check ...  : \n", cnd)

                rightangle = 0 
                rightX=10000.0; rightY=10000.0
                pref = 0 
                nodeid=0
                for i in range(cnd[2]-cnd[1], cnd[2]):
                    # print (NodeTranslated[i][0]-1000_0000, end=", ")
                    # print (" N %d(%d), DelX=%.3f, DelY=%.3f, DelZ=%.3f"%(NodeTranslated[i][0]-10**7, cnd[2]-cnd[1], NodeTranslated[i][5]*1000, NodeTranslated[i][6]*1000, NodeTranslated[i][7]*1000))
                    print (" N %d(%d), DelX=%.3f, DelY=%.3f"%(NodeTranslated[i][0]-10**7, i, NodeTranslated[i][5]*1000, NodeTranslated[i][6]*1000))
                    nodeid = NodeTranslated[i][0]
                    if round(NodeTranslated[i][4], 3) == 0.0: 
                        rightangle=1
                        print (" >> right angle")
                        # break
                print(" Node in Elements ")
                idxs = np.where(self.nps[:,1:9]==nodeid)[0]
                for ix in idxs: 
                    print("%5d,"%(self.nps[ix][0]-10**7), end="")
                print ("")
                
                xs=0.0; ys=0.0
                counting = 0 
                for i in range(cnd[2]-cnd[1], cnd[2]):
                    # print (NodeTranslated[i][0]-1000_0000, end=", ")
                    xs += NodeTranslated[i][1]
                    ys += NodeTranslated[i][2]
                    counting += 1 
                    if rightangle ==1 and NodeTranslated[i][4]<anglestd: 
                        rightX=NodeTranslated[i][1]
                        rightY=NodeTranslated[i][2]

                    if cnd[1] <=2: cnode.append([cnd[0], NodeTranslated[i][1], NodeTranslated[i][2], NodeTranslated[i][3] ])
                # print ("")
                x_avg = xs/float(cnd[1])
                y_avg = ys/float(cnd[1])

                if rightX !=10000 : 
                    x_avg = rightX
                    y_avg = rightY

                self.TranslatedNode.append([self.npn[ind][0], x_avg - self.npn[ind][1], y_avg - self.npn[ind][2], 0.0])
                self.npn[ind][1] = x_avg
                self.npn[ind][2] = y_avg 
                
            
            if cnd[1] <=2: fnode.append(self.npn[ind])

        # print ("Cases of node translation ")
        print (" 1 Node Type  = %d"%(case1))
        print (' 2 Node Type I= %d, II=%d, III=%d\n the same position=%d\n Different position case 1=%d, 2=%d, 3=%d'%(case21, case22, case23, case24, case241, case242, case243))

        if debugmode ==1: 
            idx = np.where(self.npn[:,0] == swn1+1000_0000)[0][0]
            print ("**Node %d, fin X=%7.3f, y=%7.3f, ht=%7.3f"%(swn1, self.npn[idx][1]*1000, self.npn[idx][2]*1000, self.npn[idx][3]*1000))

            idx = np.where(self.npn[:,0] == swn2+1000_0000)[0][0]
            print ("**Node %d, fin X=%7.3f, y=%7.3f, ht=%7.3f"%(swn2, self.npn[idx][1]*1000, self.npn[idx][2]*1000, self.npn[idx][3]*1000))


        self.TranslatedNode = np.array(self.TranslatedNode)


        TIME_FINE=time.time()
        print ("* Nodes on Groove side were moved !!")
        # print ("* All Nodes on Groove side Groove Side Surface were moved !!", round(TIME_FINE - T_Start, 2))

        
        if debugmode ==1: 
            idx = np.where(self.npn[:,0] == swn1+1000_0000)[0][0]
            print ("Node %d, fin X=%7.3f, y=%7.3f, ht=%7.3f"%(swn1, self.npn[idx][1]*1000, self.npn[idx][2]*1000, self.npn[idx][3]*1000))
            idx = np.where(self.npn[:,0] == swn2+1000_0000)[0][0]
            print ("Node %d, fin X=%7.3f, y=%7.3f, ht=%7.3f"%(swn2, self.npn[idx][1]*1000, self.npn[idx][2]*1000, self.npn[idx][3]*1000))

            for nd in self.TranslatedNode: 
                if nd[0]-10**7 == 6313 or  nd[0]-10**7 == 6317 or  nd[0]-10**7 == 6427 or  nd[0]-10**7 == 6449: 
                    print (" Transition %d, %.3f, %.3f, %.3f"%(nd[0]-10**7, nd[1]*1000, nd[2]*1000, nd[3]*1000))

        # sys.exit()
        return pv_node, cnode, fnode
    
    def FindContactingEdge(self, cedge, edges, samesolid=0, samedirection=0, show=0): 
        
        if samedirection ==0: 
            dx1 = np.where(edges[:,0] == cedge[1])
            dx2 = np.where(edges[:,1] == cedge[0])
            dx = np.intersect1d(dx1, dx2)
        else: 
            dx1 = np.where(edges[:,0] == cedge[0])
            dx2 = np.where(edges[:,1] == cedge[1])
            dx = np.intersect1d(dx1, dx2)
        if show ==1: 
            print ("LEN", len(dx))
            for d in dx: 
                print ("> %d, %d, %d"%(edges[d][3]-10**7, edges[d][0]-10**7, edges[d][1]-10**7))
        if len(dx) == 1:
            return edges[dx[0]]
        elif len(dx) == 2: 
            if samesolid == 0: 
                if  edges[dx[0]][3] == cedge[3]: return edges[dx[1]]
                else: return edges[dx[0]]
            else: 
                if  edges[dx[0]][3] == cedge[3]: return edges[dx[0]]
                else: return edges[dx[1]]
        else: #  len(dx) ==0: 
            result = []
            return result 
    def FindAnotherEdgeInSurface(self, next=1, cedge=[], edges=[], surfaces=[], sfreturn=0, face_exclude=0): 
        # print (surfaces)
        edx =  np.where(surfaces[:, 0] == cedge[3])[0]
        n1dx = np.where(surfaces[:, 7:] == cedge[0])[0]
        n2dx = np.where(surfaces[:, 7:] == cedge[1])[0]

        sfdx = np.intersect1d(edx, n1dx)
        sfdx = np.intersect1d(sfdx, n2dx)

        if len(sfdx) ==0: 
            if sfreturn ==1: return [], []
            else: return []

        if len(sfdx) ==2: 
            cn = int(surfaces[sfdx[0]][2])
            imatch = 0
            for i in range(7, 7+cn): 
                if surfaces[sfdx[0]][i] == cedge[0]: 
                    imatch = i 
                    break 
            if cn == 4 and imatch == 10:        inext = 7 
            elif cn ==3 and imatch == 9:        inext = 7
            else:                               inext = imatch + 1

            if surfaces[sfdx[0]][inext] == cedge[1]:         
                idx = sfdx[0]
                cnd = [imatch, inext]
            else:                                            
                idx = sfdx[1]
                cn = int(surfaces[idx][2])
                imatch = 0
                for i in range(7, 7+cn): 
                    if surfaces[idx][i] == cedge[0]: 
                        imatch = i 
                        break 
                if cn == 4 and imatch == 10:        inext = 7 
                elif cn ==3 and imatch == 9:        inext = 7
                else:                               inext = imatch + 1
                cnd = [imatch, inext]

        elif len(sfdx) ==1 : 
            idx =sfdx[0]
            cn = int(surfaces[idx][2])
            imatch = 0
            for i in range(7, 7+cn): 
                if surfaces[idx][i] == cedge[0]: 
                    imatch = i 
                    break 
            if cn == 4 and imatch == 10:        inext = 7 
            elif cn ==3 and imatch == 9:        inext = 7
            else:                               inext = imatch + 1
            cnd = [imatch, inext]

        else: 
            print ("### ERROR to find surface surfance found =%d "%(len(sfdx)))

            for i in range(len(sfdx)): 
                print ("SF%d: %d(face=%d): %d, %d, %d, %d"%(i+1, surfaces[sfdx[0]][0]-10000000, surfaces[sfdx[0]][1], surfaces[sfdx[0]][7]-10000000, surfaces[sfdx[0]][8]-10000000, surfaces[sfdx[0]][9]-10000000, surfaces[sfdx[0]][10]-10000000))
            try: 
                idx = np.where(self.Solid[:,0]==cedge[3])[0][0]
                print ("SOLID = %d, %d, %d, %d, %d, %d, %d, %d, %d"%(self.Solid[idx][0]-10000000, self.Solid[idx][1]-10000000, self.Solid[idx][2]-10000000, self.Solid[idx][3]-10000000, self.Solid[idx][4]-10000000, self.Solid[idx][5]-10000000, self.Solid[idx][6]-10000000, self.Solid[idx][7]-10000000, self.Solid[idx][8]-10000000))
            except: 
                pass 
            sys.exit()


        if  cn == 4: 
            if next == -1: next = 3 
            elif next == -2: next =2
            elif next == -3: next = 1

        else: 
            if next == -1: next = 2
            elif next == -2: next = 1

        nnd =[]
        face = 0
        if cn ==4:
            nnd.append([7, 8, 1])
            nnd.append([8, 9, 2])
            nnd.append([9, 10, 3])
            nnd.append([10, 7, 4])
            
            if cnd[0]==7 and cnd[1] == 8:                 face =1 
            if cnd[0]==8 and cnd[1] == 9:                 face =2 
            if cnd[0]==9 and cnd[1] == 10:                face =3 
            if cnd[0]==10 and cnd[1] == 7:                face =4 
            
            
        else: 
            nnd.append([7, 8, 1])
            nnd.append([8, 9, 2])
            nnd.append([9, 7, 3])
            
            if cnd[0]==7 and cnd[1] == 8:                 face =1 
            if cnd[0]==8 and cnd[1] == 9:                 face =2
            if cnd[0]==9 and cnd[1] == 7:                 face =3 
            

        nextface = int(face + next)  
        if nextface > cn: nextface -= cn 

        nx1=0
        nx2 = 0
        for nd in nnd: 
            if nd[2] == nextface: 
                nx1 = surfaces[idx][nd[0]]
                nx2 = surfaces[idx][nd[1]]
                break
                
        mat1 = np.where(edges[:,0]==nx1)[0]
        mat2 = np.where(edges[:,1]==nx2)[0]

        # mat = np.intersect1d(mat1, mat2) 
        mat = []
        for m1 in mat1: 
            for m2 in mat2: 
                if m1 == m2: 
                    mat.append(m1)
                    break 

        if len(mat) ==1 : 
            if sfreturn ==1: 
                return edges[mat[0]], surfaces[idx]
            else: 
                return edges[mat[0]]
        else: 
            # print ("How many indices=%d"%(len(mat)))
            for t in mat: 
                # print ("Solid id of edge=%d, N1=%d, N2=%d"%(edges[t][3]-1000_0000, edges[t][0]-1000_0000, edges[t][1]-1000_0000))
                if edges[t][3] == cedge[3]: 
                    if sfreturn == 1:   
                        if face_exclude == 0: 
                            return edges[t], surfaces[idx]
                        else: 
                            if int(surfaces[idx][1]) != face_exclude: 
                                return edges[t], surfaces[idx]
                            else: 
                                continue
                    else: 
                        return edges[t]
            # print ("self.FindAnotherEdgeInSurface -> nothing to return")
            if sfreturn ==1: return [], []
            else: return []
            # sys.exit()
    def GrooveSideNodeRepositioningOnSubgroove(self, Subgrooveedges=[], orgn_node=[], alledges=[], surfaces=[], fname="",\
         maingroovebottomedge=[], maingrooveside=[], modelnodes=[]): ## orgn : Nodes with original(model)  coordinates, nodes : coordinates after moved 
        
        ## Initialization  #############################################################
        orgn = orgn_node
        edges=[]
        for edge in Subgrooveedges: 
            nx1 = np.where(orgn[:, 0]==edge[0])[0][0]
            nx2 = np.where(orgn[:, 0]==edge[1])[0][0]
            edges.append([edge[0], edge[1], 0, edge[3], orgn[nx1][1], orgn[nx1][2], orgn[nx1][3], orgn[nx2][1], orgn[nx2][2], orgn[nx2][3] ])
        edges=np.array(edges)

        temp=[]
        for edge in alledges: 
            nx1 = np.where(orgn[:, 0]==edge[0])[0][0]
            nx2 = np.where(orgn[:, 0]==edge[1])[0][0]
            temp.append([edge[0], edge[1], 0, edge[3], orgn[nx1][1], orgn[nx1][2], orgn[nx1][3], orgn[nx2][1], orgn[nx2][2], orgn[nx2][3] ])
        alledges=np.array(temp)
        ################################################################################

        TIME_START=time.time()
        cnode = []
        for nd in self.npn: 
            cnode.append([nd[0], nd[1], nd[2], nd[3]])
        cnode=np.array(cnode)
        pb1=[0, 0, 0]
        pb2=[0, 0.001, 0]
        pb3=[0, .001, 0.001]
        pb4=[0, 0, 0.001]
        plane_base =[pb1, pb2, pb3, pb4]

        grooveedges=[]
        kerfedges=[]
        orgplane=[]
        sidesurface=[]
        for i, edge in enumerate(edges):   ## sub groove edges ()
            # if edge[3] == 2262+10**7 : print (edge)
            # if edge[0] == 3505+10**7 or edge[1] == 3505+10**7 or edge[0] == 2706+10**7 or edge[1] == 2706+10**7 : print (edge)
            planes=[]
            noid=[]
            cedge = edge
            counting = 0
            rightangle=0
            while counting < 20:
                counting +=1  
                tedge = self.FindContactingEdge(cedge, alledges)
                try: 
                    nedge = self.FindAnotherEdgeInSurface(next=2, cedge=tedge, edges=alledges, surfaces=surfaces)
                except: 
                    if counting ==1: break 
                    else: 
                        grooveedges.append(edge)
                        break 
                    
                N10 = [tedge[0], tedge[4], tedge[5], tedge[6]]
                N20 = [tedge[1], tedge[7], tedge[8], tedge[9]]
                N30 = [nedge[0], nedge[4], nedge[5], nedge[6]]
                N40 = [nedge[1], nedge[7], nedge[8], nedge[9]]
                B01 = [N10[1], N10[2], N10[3]]            
                B02 = [N20[1], N20[2], N20[3]]            
                B03 = [N30[1], N30[2], N30[3]]            
                B04 = [N40[1], N40[2], N40[3]]
                b = [B02, B01, B04, B03]


                angle = abs(self.PI-self.SurfaceAngle_AxisZ(b))   ## initial Angle 
                angle = degrees(angle)
                temp = self.SurfaceAngle_AxisZ(b)
                tep = degrees(temp)

                if counting ==1 and N10[3] < N40[3]: 
                    break ### going-up-surface : continue to next edge

                if angle>135:  # kerfedges - line should be upward
                    if counting > 1: kerfedges.append(edge)
                    break

                if  round(abs(90 - angle), 2) < 30.0 :    
                    ## reached the bottom surface
                    grooveedges.append(edge)
                    planes.append(b)
                    # print (" groove base angle = 90")
                    break 
                
                else:   
                    PAO=angle
                    planes.append(b)
                cedge = nedge

        TIME_END=time.time()
        print ('* SEMI-GROOVE EDGE SEARCHED !!\n Total Edges=%d(Groove=%d, Kerf=%d)'%(len(edges),  len(grooveedges), len(kerfedges) ))

        ## DONE Searching Top Edges reaching to Grooves 
        ## warning!! The kerf on boader line is disregarded... (cannot know the connectivity with the nodes on the pitch up or down)
        ######################################################################################################################
        
        ## algorithm 1 : Groove Side Surface rotation 
        debugmode = 0 
        edge_groups = self.Grouping_ConnectedEdges(grooveedges, checknodes=self.TranslatedNode)
        print ("* Edge Group of Sub grooves(%d)"%(len(edge_groups)))

        # edge=[edge[0], edge[1], 0, edge[3], orgn[nx1][1], orgn[nx1][2], orgn[nx1][3], orgn[nx2][1], orgn[nx2][2], orgn[nx2][3] 

        va = [1.0E-01, 0, 0]

        displaced = []
        trans0 = []; trans = []; trans1=[]
        for group in edge_groups:
            # print (" > Elements in group=%d"%(len(group)))
            
            N = len(group)
            # if N>1: 
                
            indx=[]
            for i, edge in enumerate(group): 
                # if edge[3]-10**7 == 4772 :     
                #     print ("**** THERE IS 4772 ELEMENT")
                #     print ("  n1=%6d, n2=%6d"%(edge[0]-10**7, edge[1]-10**7))
                #     print ("  How many edges in the group = %d"%(len(group)))
                if i ==0: 
                    nd0 = np.where(self.npn[:,0] == edge[0])[0][0]
                    indx.append(nd0)
                    trans0.append([orgn[nd0][0], orgn[nd0][1], orgn[nd0][2], orgn[nd0][3]])
                    # if orgn[nd0][0] == 3505+10**7: print ("* 3505")
                ndn = np.where(self.npn[:,0] == edge[1])[0][0]
                indx.append(ndn)
                trans0.append([orgn[ndn][0], orgn[ndn][1], orgn[ndn][2], orgn[ndn][3]])
                # if orgn[ndn][0] == 3505+10**7: print ("** 3505")
                ## if the edges are closed, the 1st and the last node is the same. 

            ## Translation of the nodes on the top edge of sub groove bottom 

            
            if indx[0] == indx[N]: continue 
            ## if the edges are closed, the 1st and the last node is the same. 
            ## in this case, we don't need to re-position the nodes 
            # print("3")
            trans=self.MoveNodesBetween2Nodes(N00=orgn[indx[0]], NN0=orgn[indx[N]], N01=self.npn[indx[0]], NN1=self.npn[indx[N]], orgn=orgn, indexes=indx)

            iN = len(indx)
            if N > 1: 
                
                for i in range(1, iN-1): 
                    self.npn[indx[i]][1] = trans[i-1][1]
                    self.npn[indx[i]][2] = trans[i-1][2]
            elif N == 1 and len(trans) ==1 : 
                    # print ("  trans*** ")
                    ix = np.where(self.npn[:,0] == trans[0][0])[0][0]
                    self.npn[ix][1] = trans[0][1]
                    self.npn[ix][2] = trans[0][2]
                    trans1.append(self.npn[ix])

            ## the nodes on the beneath surfaces 
            edge_group=[]
            for i, edge in enumerate(group): 
                cedge = edge 
                face = 0
                temp = []
                # print ("##############################################################")
                while face != 1: 
                    tedge = self.FindContactingEdge(cedge, self.Edge, samesolid=1)
                    if len(tedge) == 0: 
                        break 
                    try: 
                        tem = tedge[0][0]
                        for ed in tedge: 
                            if cedge[3] == ed[3]: 
                                tedge = ed
                                break 
                    except: 
                        pass 
                    

                    nedge, sf = self.FindAnotherEdgeInSurface(next=2, cedge=tedge, edges=self.Edge, surfaces=self.Surface, sfreturn=1, face_exclude=2)
                    if debugmode ==1: 
                        print  ("TOP edge EL ID=%6d, N1=%6d, N2=%6d"%(cedge[3]-10000000, cedge[0]-10000000, cedge[1]-10000000))
                        print  ("  N edge EL ID=%6d, N1=%6d, N2=%6d"%(tedge[3]-10000000, tedge[0]-10000000, tedge[1]-10000000))

                    if len(sf) == 0: 
                        break 

                    if debugmode ==1: 
                        print  ("    Next EL ID=%6d, N1=%6d, N2=%6d"%(nedge[3]-10000000, nedge[0]-10000000, nedge[1]-10000000))
                        print  ("    SF   EL ID=%6d, Face=%d, N1=%6d, N2=%6d, N3=%6d, N4=%6d"%(sf[0]-10000000, sf[1], sf[7]-10000000, sf[8]-10000000, sf[9]-10000000, sf[10]-10000000))
                    temp.append(nedge)
                    sf = self.FindContactingSurfacebyElementID(sf[0], face=1)
                    if len(sf) == 0: 
                        break 

                    dx1 = np.where(orgn[:,0] == nedge[0])[0][0]
                    dx2 = np.where(orgn[:,0] == nedge[1])[0][0]
                    nedge = np.array([nedge[0], nedge[1], 0, sf[0], orgn[dx1][1], orgn[dx1][2], orgn[dx1][3], orgn[dx2][1], orgn[dx2][2], orgn[dx2][3]])
                    if debugmode ==1: 
                        print  ("  ->Next EL ID=%6d, N1=%6d, N2=%6d"%(nedge[3]-10000000, nedge[0]-10000000, nedge[1]-10000000))
                        print  ("  ->SF   EL ID=%6d, Face=%d, N1=%6d, N2=%6d, N3=%6d, N4=%6d"%(sf[0]-10000000, sf[1], sf[7]-10000000, sf[8]-10000000, sf[9]-10000000, sf[10]-10000000))
                        print ("***********************************************************")
                    face = int(sf[1])
                    cedge = nedge

                edge_group.append(temp) 

            # print (" >>>>>>> Edge grouped. %d(=j), %d(=k)"%(len(edge_group), len(edge_group[0])))

            jN = len(edge_group)
            kN = len(edge_group[0])
            jGroup=[]
            for k in range(kN): 
                sub=[]
                for j in range(jN): 
                    # if len(edge_group[j]) > k: 
                    try:
                        sub.append(edge_group[j][k])
                    except:
                        break
                #     print ("j=%d/%d , k=%d/%d"%(j, jN, k, kN))
                # print ("***********************************")
                jGroup.append(sub)
                # k += 1 

            for sub in jGroup: 
                N = len(sub)
                indx=[]
                for j, edge in enumerate(sub): 
                    if j ==0: 
                        nd0 = np.where(self.npn[:,0] == edge[0])[0][0]
                        indx.append(nd0)
                        trans0.append([orgn[nd0][0], orgn[nd0][1], orgn[nd0][2], orgn[nd0][3]])
                        # if orgn[nd0][0] == 3505+10**7: print ("*** 3505")
                    ndn = np.where(self.npn[:,0] == edge[1])[0][0]
                    indx.append(ndn)
                    trans0.append([orgn[ndn][0], orgn[ndn][1], orgn[ndn][2], orgn[ndn][3]])
                    # if orgn[ndn][0] == 3505+10**7: print ("**** 3505")
                # print ("2")
                if orgn[indx[0]][0]== orgn[indx[N]][0]: 
                    continue 
                trans=self.MoveNodesBetween2Nodes(N00=orgn[indx[0]], NN0=orgn[indx[N]], N01=self.npn[indx[0]], NN1=self.npn[indx[N]], orgn=orgn, indexes=indx)
                try: 
                    pN=len(trans)
                    if N > 1: 
                        for k in range(1, pN+1): 
                            self.npn[indx[k]][1] = trans[k-1][1]
                            self.npn[indx[k]][2] = trans[k-1][2]
                            trans1.append(self.npn[indx[k]])
                    elif N == 1 and len(trans) ==1 :    ## 1 node
                        # print ("  trans")
                        ix = np.where(self.npn[:,0] == trans[0][0])[0][0]
                        self.npn[ix][1] = trans[0][1]
                        self.npn[ix][2] = trans[0][2]
                        trans1.append(self.npn[ix])
                except:
                    return 
        
        #######################################################################################
        ## if nodes are on main groove bottom(allbottomedges) but one of them does not translated, they should be moved. 
        ##  in case that there is a sub groove one of the pitch up/down  
        ## 피치 끝에 sub groove가 있어서 Main groove side 각을 조정할 때 절점의 위치 조정 시 누락된 부분이 생김 
        ######################################################################################
        debugmode = 0
        if self.TargetGD > 1.01E-03: 
            gdratio = self.TargetGD / self.ModelGD 
        else: 
            gdratio = 1.0
        distmargin = 5.0E-03

        allbottomedges=[]
        btm_top_nodes=[]
        for gedegs in maingroovebottomedge: 
            # print ("******************************************************")
            temp=0
            newgrv = 1; upedge=0; downedge=0
            upstart = 0; upend=0; downstart=0; downend=0 
            for ed in gedegs: 
                allbottomedges.append(ed)
                # print (ed[0]-10**7,",", ed[1]-10**7,",", ed[2], ",", ed[3]-10**7, ",", ed[10])
                if ed[10] ==0: 
                    upstart=ed[0]
                if ed[10] == -100 and newgrv==1 and upend ==0: 
                    upend = ed[0]
                    newgrv ==0
                    upedge =1
                if upedge ==1 and ed[10] > 0 and downstart ==0: 
                    downstart = ed[0]
                if upedge ==1 and ed[10] == -100 and downstart > 0 and downend==0: 
                    downend = ed[0]
                    # break 
            # print ("pitch botm/top nodes, upstart=%d, upend=%d, downstart=%d, downend=%d"%(upstart-10**7, upend-10**7, downstart-10**7, downend-10**7))
            btm_top_nodes.append([upstart, upend])
            btm_top_nodes.append([downend, downstart])

        if debugmode ==1: print ("Main groove Bottom [Upper and lower] Nodes\n    ", btm_top_nodes)

        if len(self.TranslatedNode) ==0: 
            return np.array(trans0), np.array(trans1)

        tnodes = self.TranslatedNode[:,0]
        Tnodes=[]
        for nd in tnodes:
            idx = np.where(self.npn[:,0]==nd)[0][0]
            Tnodes.append(self.npn[idx])
        Tnodes = np.array(Tnodes)  ## Tnodes : all the nodes to move 

        # edge_group=[]
        for i, nd in enumerate(btm_top_nodes):   ## all the nodes on the main groove at pitch upper  / down : len(btm_top_nodes) = (No. of main groove) X 2 
            idx1 = np.where(Tnodes[:,0] == nd[0])[0]
            idx2 = np.where(Tnodes[:,0] == nd[1])[0]

            if len(idx1) ==1 and len(idx2) ==1:    ## if both nodes on the main grooves were moved, we don't need to care any more. 
                if debugmode ==1: print ("Distance = %7.5f (pitch length=%7.5f)"%(NodeDistance(Tnodes[idx1[0]], Tnodes[idx2[0]])*1000, self.TargetPL*1000))
                continue
            
            if len(idx1) + len(idx2) ==1:    ## if one node of the edge was moved (another was not moved)  : pitch up or down nodes 
                                             ## there is a sub groove on pitch up or down (only on side)
                if debugmode ==1: print (idx1, idx2)
                up = 0 
                if len(idx1) ==1: 
                    idx1 = idx1[0]
                    basenode = Tnodes[idx1]
                    idx2 = np.where(self.npn[:,0] == nd[0])[0][0]
                    secndnode = self.npn[idx2]
                    up =1
                else: 
                    idx2 = idx2[0]
                    basenode = Tnodes[idx2]
                    idx1 = np.where(self.npn[:,0] == nd[0])[0][0]
                    secndnode = self.npn[idx1]
                    up = -1 
                DIST = NodeDistance(basenode,secndnode)
                if debugmode ==1: 
                    print ("******************************************************************************")
                    print ("* Search Node : %d"%(secndnode[0]))
                    if up == 1: 
                        print (" - already moved node : %d,  still not moved node : %d"%(Tnodes[idx1][0]-10**7, nd[1]-10**7))
                    else: 
                        print (" _ already moved node : %d,  still not moved node : %d"%(Tnodes[idx2][0]-10**7, nd[0]-10**7))

                    print ("  The distance on the 1st / 2nd node on edge (== pitch length) = %.3f"%(DIST*1000))
                    print ("******************************************************************************")

                idxsbtm = [idx1, idx2]
                if len(idxsbtm) == 2  : 
                    for id in idxsbtm: 
                        if NodeDistance([0, self.npn[id][1], self.npn[id][2], 0.0], [0, basenode[1] + self.TargetPL * up, basenode[2], 0.0]) < distmargin:  ## currennt distmargin = 5mm 
                            if debugmode ==1: 
                                print (" NDOE %6d moved : x=%7.3f, y=%7.3f"%(self.npn[id][0]-10**7, self.npn[id][1]*1000, self.npn[id][2]*1000), end=" -->")
                            self.npn[id][1] = basenode[1] + self.TargetPL * up
                            self.npn[id][2] = basenode[2]
                            if debugmode ==1: 
                                print (" x=%7.3f, y=%7.3f"%(self.npn[id][1]*1000, self.npn[id][2]*1000))

                    ## making edge group
                    sgroup = []
                    if i%2 == 0:   ## [ up start, end ]
                        # if debugmode ==1: print ("left groove side")
                        gedge = maingroovebottomedge[int(i/2)]
                        
                        if up == 1: 
                            
                            fnd = 0 
                            for j, ed in enumerate(gedge): 
                                idxs = np.where(Tnodes[:,0] == ed[1])[0] 
                                if fnd==1: 
                                    sgroup.append(ed)

                                if len(idxs) == 0 and fnd==0: 
                                    sgroup.append(gedge[j-1])
                                    sgroup.append(gedge[j])
                                    fnd =1 
                                if ed[1] ==nd[0]: 
                                    ## No gathering edges .. 
                                    sgroup=[]
                                    break 
                                if ed[1] == nd[1]: 
                                    break 
                        else: 
                            # print (" up = -1")
                            for j, ed in enumerate(gedge): 
                                sgroup.append(ed)
                                # print ("Edge nodes to add into sgroup [%d, %d] in %d  "%(ed[0]-10**7, ed[1]-10**7, ed[3]-10**7))
                                idxs = np.where(Tnodes[:,0]==ed[0])[0]
                                if len(idxs) > 0: 
                                    break 

                    else:     # [down start, end]
                        # if debugmode ==1: print ("right groove side")
                        # print ("right groove side")
                        gedge = maingroovebottomedge[int(i/2)]

                        if up ==-1: 
                            fnd = 0 
                            down = 0
                            for j, ed in enumerate(gedge): 
                                if ed[10] == -100: 
                                    down =1 
                                if down ==1 and ed[10] != -100: 
                                    idxs = np.where(Tnodes[:,0] == ed[1])[0] 
                                    if fnd==1: 
                                        sgroup.append(ed)

                                    if len(idxs) == 0 and fnd==0: 
                                        sgroup.append(gedge[j-1])
                                        sgroup.append(gedge[j])
                                        fnd =1 
                                    if ed[1] ==nd[1]: 
                                        ## No gathering edges .. 
                                        sgroup=[]
                                        break 
                                    if ed[1] == nd[0]: 
                                        break 

                        else:
                            down = 0 
                            for j, ed in enumerate(gedge): 
                                # print ( " %2d:: N1=%6d, N2=%6d, edge[10]=%d"%(j, ed[0]-10**7, ed[1]-10**7, ed[10]))
                                if ed[10] == -100: 
                                    down = 1
                                if down ==1 and ed[10] != -100: 
                                    sgroup.append(ed)
                                    idxs = np.where(Tnodes[:,0]==ed[0])[0]
                                    # print (' .. ', j, ',', len(idxs), ed[0]-10**7, ',', ed[1]-10**7)
                                    if len(idxs) > 0: 
                                        break 

                    
                    # edge_group.append(sgroup) 
                    ## nodes translation at the groove bottom edge
                                            # N = len(sgroup)
                    # print ("************************************")
                    # Printlist(sgroup)
                    # print ("************************************")
                    debugmode = 0
                    if len(sgroup) > 0: 
                        if sgroup[0][3] !=  sgroup[len(sgroup)-1][3]: 
                            indx = []
                            if debugmode ==1: print ("################################################")
                            for j, edge in enumerate(sgroup): 
                                if debugmode ==1: print (" %2d : %6d, %6d (%6d)"%(j, edge[0]-10**7, edge[1]-10**7, edge[3]-10**7))
                                if j == 0: 
                                    nd0= np.where(self.npn[:,0] == edge[0])[0][0]
                                    indx.append(nd0)
                                    trans0.append([orgn[nd0][0], orgn[nd0][1], orgn[nd0][2], orgn[nd0][3]])
                                    # if orgn[nd0][0] == 3505+10**7: print ("*# 3505")
                                ndn = np.where(self.npn[:,0] == edge[1])[0][0]
                                indx.append(ndn)
                                trans0.append([orgn[ndn][0], orgn[ndn][1], orgn[ndn][2], orgn[ndn][3]])
                                # if orgn[ndn][0] == 3505+10**7: print ("*## 3505")
                            if debugmode ==1: print ("No of edges in the group=%d"%(len(sgroup)))
                            # print ("1")
                            trans=self.MoveNodesBetween2Nodes(N00=orgn[indx[0]], NN0=orgn[indx[N]], N01=self.npn[indx[0]], NN1=self.npn[indx[N]], orgn=orgn, indexes=indx, debug=debugmode)
                            pN=len(trans)
                            if N > 1: 
                                for k in range(1, pN+1): 
                                    self.npn = self.MoveNodesAtSomePositionXY(SearchPosition=[self.npn[indx[k]][1], self.npn[indx[k]][2]], ReplacePosition=[trans[k-1][1], trans[k-1][2]], nodes=self.npn, debug=debugmode)
                            elif N == 1 and len(trans) ==1 :    ## 1 node
                                ix = np.where(self.npn[:,0] == trans[0][0])[0][0]
                                self.npn = self.MoveNodesAtSomePositionXY(SearchPosition=[self.npn[ix][1], self.npn[ix][2]],ReplacePosition=[trans[0][1], trans[0][2]], nodes=self.npn, debug=debugmode)

                            for j, edge in enumerate(sgroup): 
                                
                                idx1 = np.where(maingrooveside[:,7:]==edge[0])[0]
                                idx2 = np.where(maingrooveside[:,7:]==edge[1])[0]
                                idx = np.intersect1d(idx1, idx2)
                                
                                if len(idx) > 0: 
                                    if debugmode ==1: PN = len(idx)
                                    idx = idx[0]

                                    if debugmode ==1: 
                                        print (PN, " >>> ",edge[0]-10**7, ',', edge[0]-10**7, ",", edge[1]-10**7, ", ", maingrooveside[idx][1], ',', maingrooveside[idx][7] - 10**7, ',', maingrooveside[idx][8] - 10**7, ',', maingrooveside[idx][9] - 10**7, ',', maingrooveside[idx][10] - 10**7 )
                                
                                else: 
                                    # Image (file="ERROR Groove bottom node movement", edge0=sgroup, edge1=sgroup, surf=maingrooveside, sfn=self.npn, edn=self.npn, xy=12, dpi=500)
                                    # print ("### ERROR!! There are some errors to find main groove side surface")
                                    
                                    ############################################################################
                                    ## this may be caused because there are sub groove on the pitch up / down . 
                                    ## example APR-140647_H436_P225-55R.ptn .. 
                                    continue   ## therefore we should not exit but continue 
                                    # sys.exit()

                                ## orgn : simple scaled nodes position, modelnodes : Model pattern nodes position
                                idn1 = np.where(orgn[:,0] == maingrooveside[idx][7])[0][0]
                                idn2 = np.where(orgn[:,0] == maingrooveside[idx][8])[0][0]
                                n11 = orgn[idn1];          n12 = orgn[idn2]
                                idn1 = np.where(modelnodes[:,0] == maingrooveside[idx][7])[0][0]
                                idn2 = np.where(modelnodes[:,0] == maingrooveside[idx][8])[0][0]
                                n01 = modelnodes[idn1];    n02 = modelnodes[idn2]

                                idn31 = np.where(orgn[:,0] == maingrooveside[idx][9])[0]
                                idn41 = np.where(orgn[:,0] == maingrooveside[idx][10])[0]
                                
                                idn30 = np.where(modelnodes[:,0] == maingrooveside[idx][9])[0]
                                
                                idn40 = np.where(modelnodes[:,0] == maingrooveside[idx][10])[0]

                                idx2= np.where(self.npn[:,0] == maingrooveside[idx][8])[0][0]
                                basenode3 = self.npn[idx2]
                                idx1= np.where(self.npn[:,0] == maingrooveside[idx][7])[0][0]
                                basenode4 = self.npn[idx1]
                                cnt = 0 
                                while len(idn31) > 0 : 
                                    n13 = orgn[idn31[0]];          n14 = orgn[idn41[0]]
                                    n03 = modelnodes[idn30[0]];    n04 = modelnodes[idn40[0]]

                                    dist03, in3 = DistanceFromLineToNode2D(n03, [n01, n02])
                                    dist04, in4 = DistanceFromLineToNode2D(n04, [n01, n02])

                                    h03 = n03[3] - n02[3];            h04 = n04[3] - n01[3] 
                                    h13 = n13[3] - n12[3];            h14 = n14[3] - n11[3] 

                                    inc3 = dist03 / h03;              inc4 = dist04 / h04
                                    Tdist3 = inc3 * h13;              Tdist4 = inc4 * h14

                                    v3x = (n03[1] - n02[1]);          v3y = (n03[2] - n02[2])
                                    v4x = (n04[1] - n01[1]);          v4y = (n04[2] - n01[2])

                                    if round(dist03, 6) ==0:        Del3x = 0; Del3y = 0
                                    else:                           Del3x = v3x * Tdist3 / dist03; Del3y = v3y * Tdist3/dist03 
                                    if round(dist04, 6) ==0:        Del4x = 0; Del4y = 0
                                    else:                           Del4x = v4x * Tdist4 / dist04; Del4y = v4y * Tdist4/dist04 
                                    
                                    idx3= np.where(self.npn[:,0] == maingrooveside[idx][9])[0][0]
                                    if debugmode ==1: 
                                        ini3x = self.npn[idx3][1]
                                        ini3y = self.npn[idx3][2]
                                    self.npn[idx3][1] = basenode3[1] + Del3x
                                    self.npn[idx3][2] = basenode3[2] + Del3y
                                    
                                    idx4= np.where(self.npn[:,0] == maingrooveside[idx][10])[0][0]
                                    if debugmode ==1: 
                                        ini4x = self.npn[idx4][1]
                                        ini4y = self.npn[idx4][2]
                                    self.npn[idx4][1] = basenode4[1] + Del4x
                                    self.npn[idx4][2] =basenode4[2] + Del4y

                                    idx1 = np.where(maingrooveside[:,7:9]== n14[0])[0]
                                    idx2 = np.where(maingrooveside[:,7:9]== n13[0])[0]
                                    idx = np.intersect1d(idx1, idx2)
                                    if len(idx) > 0: 
                                        idx = idx[0]

                                        idn31 = np.where(orgn[:,0] == maingrooveside[idx][9])[0]
                                        idn41 = np.where(orgn[:,0] == maingrooveside[idx][10])[0]
                                        
                                        idn30 = np.where(modelnodes[:,0] == maingrooveside[idx][9])[0]
                                        idn40 = np.where(modelnodes[:,0] == maingrooveside[idx][10])[0]
                                    else:
                                        idn31 = []
                                    if debugmode ==1: 
                                        print (cnt, "********************************************************************************")
                                        print ("    v3x=%7.3f, v3y=%7.3f, v4x=%7.3f, v4y=%7.3f"%(v3x*1000, v3y*1000, v4x*1000, v4y*1000))
                                        print ("    Tdist3=%7.3f, dist03=%7.3f, Tdist4=%7.3f, dist04=%7.3f"%(Tdist3*1000, dist03*1000, Tdist4*1000, dist04*1000))
                                        print ("    Del 3x=%7.3f, 3y=%7.3f, Del 4x=%7.3f, 4y=%7.3f"%(Del3x*1000, Del3y*1000, Del4x*1000, Del4y*1000))
                                        print ("    Initial Pos 3: x=%7.3f, y=%7.3f -> x=%7.3f, y=%7.3f"%(ini3x*1000,ini3y*1000, self.npn[idx3][1]*1000,self.npn[idx3][2]*1000))
                                        print ("    Initial Pos 4: x=%7.3f, y=%7.3f -> x=%7.3f, y=%7.3f"%(ini4x*1000,ini4y*1000, self.npn[idx4][1]*1000,self.npn[idx4][2]*1000))

                                    cnt +=1
                                    if cnt > 20: 
                                        print ("!!! ERROR , Too much iteration for translating the nodes at the groove top / bottom edge with sub groove")
                                        sys.exit()

        return np.array(trans0), np.array(trans1)
    def SurfaceAngle_AxisZ(self, MA, screen=0): 
        PI = self.PI
        planes=[]
        if screen==1: 
            
            print (" P1 : %.3f, %.3f, %.3f"%(MA[0][0]*1000, MA[0][1]*1000, MA[0][2]*1000))
            print (" P2 : %.3f, %.3f, %.3f"%(MA[1][0]*1000, MA[1][1]*1000, MA[1][2]*1000))
            print (" P3 : %.3f, %.3f, %.3f"%(MA[2][0]*1000, MA[2][1]*1000, MA[2][2]*1000))
            print (" P4 : %.3f, %.3f, %.3f"%(MA[3][0]*1000, MA[3][1]*1000, MA[3][2]*1000))
            

        i=0; j=1; k=2; l=3

        Points = np.array([
            [MA[i][0], MA[j][0], MA[k][0], MA[l][0]], 
            [MA[i][1], MA[j][1], MA[k][1], MA[l][1]],
            [MA[i][2], MA[j][2], MA[k][2], MA[l][2]],
            [     1,      1,      1,      1]
        ])
        D = np.array([
            [1, 0, 0, -MA[i][0]], 
            [0, 1, 0, -MA[i][1]],
            [0, 0, 1, -MA[i][2]],
            [0, 0, 0, 1]
        ])

        MA = np.matmul(D, Points)
        if screen==1:
            print ("Translate to Origin")
            print (" P1 : %.3f, %.3f, %.3f"%(MA[0][i]*1000, MA[1][i]*1000, MA[2][i]*1000))
            print (" P2 : %.3f, %.3f, %.3f"%(MA[0][j]*1000, MA[1][j]*1000, MA[2][j]*1000))
            print (" P3 : %.3f, %.3f, %.3f"%(MA[0][k]*1000, MA[1][k]*1000, MA[2][k]*1000))
            print (" P4 : %.3f, %.3f, %.3f"%(MA[0][l]*1000, MA[1][l]*1000, MA[2][l]*1000))
        plane=[
            [MA[0][i],MA[1][i],MA[2][i]],
            [MA[0][j],MA[1][j],MA[2][j]],
            [MA[0][k],MA[1][k],MA[2][k]],
            [MA[0][l],MA[1][l],MA[2][l]]
        ]
        planes.append(plane)

        a = abs(round(MA[0][j] - MA[0][i], 8))
        b = abs(round(MA[1][j] - MA[1][i], 8))
        c = abs(round(MA[2][j] - MA[2][i], 8))

        A = MA 

        na = len(A)
        a = [A[0][1] - A[0][0], A[1][1] - A[1][0], A[2][1] - A[2][0]]
        b = [A[0][na-1] - A[0][0], A[1][na-1] - A[1][0], A[2][na-1] - A[2][0]]

        va = [a[1]*b[2] - a[2]*b[1], a[2]*b[0] - a[0]*b[2], a[0]*b[1] - a[1]*b[0]]
        if screen==1: 
            print ('Vector P2-P1 : %.3f, %.3f, %.3f'%(a[0]*1000, a[1]*1000, a[2]*1000))
            print ('Vector P4-p1 : %.3f, %.3f, %.3f'%(b[0]*1000, b[1]*1000, b[2]*1000))

        
        vb = [0.0, 0.0, 0.001]
        la = sqrt(va[0]*va[0] + va[1]*va[1] + va[2]*va[2])
        lb = 0.001
        pcos = round((va[0]*vb[0]+va[1]*vb[1]+va[2]*vb[2]) / la/lb , 6)
        if round(la, 8) == 0: 
            
            print ("  Normal Vector : %.3f, %.3f, %.3f"%(va[0]*1000, va[1]*1000, va[2]*1000))
            print (" Plane N1 : %6.3f,%6.3f,%6.3f"%(A[0][0]*1000, A[1][0]*1000, A[2][0]*1000))
            print ("       N2 : %6.3f,%6.3f,%6.3f"%(A[0][1]*1000, A[1][1]*1000, A[2][1]*1000))
            print ("       N3 : %6.3f,%6.3f,%6.3f"%(A[0][2]*1000, A[1][2]*1000, A[2][2]*1000))
            print ("       N4 : %6.3f,%6.3f,%6.3f"%(A[0][3]*1000, A[1][3]*1000, A[2][3]*1000))

            print (" #########################################")
            print (" P1 : %.3f, %.3f, %.3f"%(Points[0][0]*1000, Points[1][0]*1000, Points[2][0]*1000))
            print (" P2 : %.3f, %.3f, %.3f"%(Points[0][1]*1000, Points[1][1]*1000, Points[2][1]*1000))
            print (" P3 : %.3f, %.3f, %.3f"%(Points[0][2]*1000, Points[1][2]*1000, Points[2][3]*1000))
            print (" P4 : %.3f, %.3f, %.3f"%(Points[0][3]*1000, Points[1][2]*1000, Points[2][3]*1000))
            

            ShowPlanes(planes)
            sys.exit()


        angle = acos(pcos)
        if screen==1: 
            print (' Between Angle=%.1f'%(degrees(angle)))
            print ("  Normal Vector : %.3f, %.3f, %.3f"%(va[0]*1000, va[1]*1000, va[2]*1000))
            print ("  Normal X-Y Plane: %.3f, %.3f, %.3f"%(vb[0]*1000, vb[1]*1000, vb[2]*1000))
            ShowPlanes(planes)

        return angle + PI/2.0
    def Grouping_ConnectedEdges(self, edges, checknodes=[], debug=0): 
        chkpt = 0
        if len(checknodes)>0: 
            tn = checknodes[:,0]
            chkpt = 1

        idxs=[]

        i=0 
        while i < len(edges): 
            j=i+1
            first=1
            for k in range(len(edges)): 
                if edges[i][0] == edges[k][1] : 
                    first = 0
                    break 
            if first ==1: 
                group=[]

                nxt = i
                group.append(nxt)
                while nxt >=0:  
                    
                    nxt = NextEdge(edges[nxt], edges)
                    if nxt >=0: 
                        if chkpt ==1: 
                            ns = np.where(tn==edges[nxt][1])[0]
                            if len(ns)>0: 
                                group.append(nxt) 
                                idxs.append(group)
                                group=[]
                            else:
                                group.append(nxt) 
                        else: 
                            group.append(nxt) 

                if len(group)> 0: idxs.append(group)
                # print (group)
            i += 1

        groups =[]
        allidx = []
        cnt=0
        for grp in idxs:
            edge=[]
            for gp in grp: 
                edge.append(edges[gp])
                allidx.append(gp)
                cnt += 1 
            groups.append(edge)
        
        if debug ==1: print (" all edges to group=%d, idx=%d"%(len(edges), cnt))
        #######################################################
        ## for closed edges 
        #######################################################

        # print (" groups 1", len(groups))
        # debug = 1
        if len(edges) > len(allidx): 
            idxarray = np.arange(len(edges))
            difarray = np.setdiff1d(idxarray, allidx)
            residuals = []
            for i in difarray: 
                residuals.append(edges[i])  ## collecting the edges that consist the closed loop 

            total = len(residuals)
            i = 0 
            cont = 0 
            while i < len(residuals):   ## 
                n1= residuals[i][0]
                n2= residuals[i][1]

                nxt = NextEdge(residuals[i], residuals)
                n3 = residuals[nxt][0]
                n4 = residuals[nxt][1]

                idx = np.where(self.npn[:,0]==n1)[0][0]
                N1 = self.npn[idx]
                idx = np.where(self.npn[:,0]==n2)[0][0]
                N2 = self.npn[idx]
                idx = np.where(self.npn[:,0]==n3)[0][0]
                N3 = self.npn[idx]
                idx = np.where(self.npn[:,0]==n4)[0][0]
                N4 = self.npn[idx]

                L14 = NodeDistance(N1, N4) 
                L12 = NodeDistance(N1, N2) 
                if debug ==1: print (" Dist L14=%7.2f, L12=%7.2f, (N1=%4d, N2=%4d, N3=%4d, N4=%4d)"%(L14*1000, L12*1000, N1[0]-10**7,  N2[0]-10**7,  N3[0]-10**7, N4[0]-10**7))
                i += 1

                if L14 < L12: 
                    grp=[]
                    tedge = residuals[nxt]
                    grp.append(tedge)
                    del(residuals[nxt])
                    cont += 1

                    if debug ==1: 
                        print ("#######################################")
                        print (" el %4d, %4d, %4d"%(tedge[3]-10**7, tedge[0]-10**7, tedge[1]-10**7))

                    nxt = NextEdge(tedge, residuals)
                    cnt = 0 
                    while residuals[nxt][1] != tedge[0] :#and nxt >=0: 
                        nxtedge = residuals[nxt]
                        if debug ==1: print (" el %4d, %4d, %4d"%(nxtedge[3]-10**7, nxtedge[0]-10**7, nxtedge[1]-10**7))
                        grp.append(nxtedge)
                        cont += 1
                        del( residuals[nxt])
                        nxt = NextEdge(nxtedge, residuals)

                        if nxt == -1: break 
                        cnt += 1
                        if cnt > 100:  break 

                    grp.append(residuals[nxt])
                    if debug ==1: print (" el %4d, %4d, %4d"%(residuals[nxt][3]-10**7, residuals[nxt][0]-10**7, residuals[nxt][1]-10**7))
                    del( residuals[nxt])
                    cont += 1
                    groups.append(grp)
                    if debug ==1: self.Image(file="_grouped_"+str(len(groups)), edge0=grp, eeid=1, enid=1, dpi=500)

                    i = 0
                    continue 
                if cont == total: 
                    break 
                
        return groups
    def MoveNodesBetween2Nodes(self, N00=[], NN0=[], N01=[], NN1=[], nodes=[], indexes=[], orgn=[], debug=0): 
        ## N00 : start node with just scaled coordinates
        ## NN0 : end node with just scaled coordinates 
        ## N01 : start node with just current coordinates
        ## NN1 : end node with just current coordinates 
        ## nodes : nodes to move they are between start and  end node. // index can be a substitute
        ##            nodes[0] == indexes[0]= N10, nodes[-1] = indexes[-1] = NN1 
        ## orgn : nodes with just scaled coordinates 

        NodeTranslated = []

        if len(self.TranslatedNode) ==0: 
            return NodeTranslated

        iN = len(indexes)
        if iN >=3: 
            if iN > 0: 
                indx=[]
                for i in range(1, iN-1): 
                    indx.append(indexes[i])
            else: 
                indx=[]
                for nd in nodes: 
                    ndx = np.where(orgn[:,0]==nd[0])[0][0]
                    indx.append(ndx)
            N00 = orgn[indexes[0]]
            NN0 = orgn[indexes[-1]]
            N01 = self.npn[indexes[0]]
            NN1 = self.npn[indexes[-1]]
            L0=NodeDistance(N00, NN0)
            L1=NodeDistance(N01, NN1)
            try: 
                ratio = L1 / L0
            except:
                print ("* ERROR!! The 2 nodes are the same (in def MoveNodesBetween2Nodes)")
                print ("%6d, %7.3f, %7.3f, %7.3f"%(N00[0]-10**7, N00[1]*1000, N00[2]*1000, N00[3]*1000))
                print ("%6d, %7.3f, %7.3f, %7.3f"%(NN0[0]-10**7, NN0[1]*1000, NN0[2]*1000, NN0[3]*1000))
                for idx in indexes: 
                    print (" Node ID=%d"%(orgn[idx][0]-10**7))
                

            for i, ix in enumerate(indx): 
                nix = N01[1] + (orgn[ix][1]- N00[1]) * ratio 
                niy = N01[2] + (orgn[ix][2]- N00[2]) * ratio 

                NodeTranslated.append([orgn[ix][0], nix, niy, orgn[ix][3]])
                narry = np.array([self.npn[ix][0],   nix - self.npn[ix][1],   niy - self.npn[ix][2],   0])
                self.TranslatedNode = np.vstack((self.TranslatedNode, narry))

        elif iN ==2: 
            
            translated = self.TranslatedNode[:,0]

            idx1 = np.where(translated == orgn[indexes[0]][0])[0]
            idx2 = np.where(translated == orgn[indexes[-1]][0])[0]
            if len(idx1) >0 and len(idx2) ==0: 
                N00 = orgn[indexes[0]]
                NN0 = orgn[indexes[-1]]
                N01 = self.npn[indexes[0]]
                NN1 = self.npn[indexes[-1]]
            elif len(idx1) == 0 and len(idx2) > 0: 
                N00 = orgn[indexes[-1]]
                NN0 = orgn[indexes[0]]
                N01 = self.npn[indexes[-1]]
                NN1 = self.npn[indexes[0]]
            else: 
                return []

            dx = NN0[1] - N00[1]
            dy = NN0[2] - N00[2]
            nix = N01[1] + dx 
            niy = N01[2] + dy 

            NodeTranslated.append([NN1[0], nix, niy, NN1[3]])
            narry = np.array([NN1[0],   nix - NN1[1],   niy - NN1[2],   0])
            self.TranslatedNode = np.vstack((self.TranslatedNode, narry))


        return NodeTranslated


        inc0 = 1
        if round (va0[0], 5) !=0:   ##  X coordinates are not constant
            a0 = va0[1] / va0[0]
        else: 
            inc0 = 0               ############################################################# inclination is correct???? 
        inc1 = 1
        if round (va1[0], 5) !=0:   ## X coordinates are not constant
            a1 = va1[1] / va1[0]
        else: 
            inc1 = 0              ############################################################# inclination is correct???? 

        C1 = a1*N01[1] - N01[2] 
        
        iN = len(indexes)
        if iN > 0: 
            indx=[]
            for i in range(1, iN-1): 
                indx.append(indexes[i])
        else: 
            indx=[]
            for nd in nodes: 
                ndx = np.where(orgn[:,0]==nd[0])[0][0]
                indx.append(ndx)

        iN = len(indx)
        for i in range(iN): 
            N0i = orgn[indx[i]]
            if inc0 == 1: 
                h0i = abs(-a0 * N00[1] + N00[2]+ a0 * N00[1]-N00[2]) / sqrt(1+ a0*a0)
            else: 
                h0i = abs(N0i[2] - N00[2])

            L0i = NodeDistance(N00, N0i)

            m1 = N01[1] + L0i / L0 * (NN1[1] - N01[1])
            n1 = N01[2] + L0i / L0 * (NN1[2] - N01[2])

            if round(h0i, 5) == 0: 
                x1i = m1 
                y1i = n1 
            else: 

                if inc1 == 1: 
                    M = C1 + m1 / a1 + n1 

                    x1i = a1 /( a1 + 1) *( L1/L0 * h0i * sqrt(1+a1*a1) - M)
                    y1i = m1 / a1 + n1 - x1i / a1 

                    va0i = [N0i[1]-N00[1], N0i[2]-N00[2], N0i[3]-N00[3]]
                    va1i = [x1i-N01[1],   y1i-N01[2], N0i[3]-N00[3]]
                    v_cross0 = VectorCross(va0, va0i)
                    v_cross1 = VectorCross(va1, va1i)

                    if v_cross0[2] * v_cross1[2] < 0:  
                        x1i = a1 /( a1 + 1) *( -L1/L0 * h0i * sqrt(1+a1*a1) - M)  
                        y1i = m1 / a1 + n1 - x1i / a1 
                    # print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

                else: 
                    x1i = m1
                    y1i = n1 + L1 / L0 * h0i 

                    va0i = [N0i[1]-N00[1], N0i[2]-N00[2], N0i[3]-N00[3]]
                    va1i = [x1i-N01[1],   y1i-N01[2], N0i[3]-N00[3]]
                    v_cross0 = VectorCross(va0, va0i)
                    v_cross1 = VectorCross(va1, va1i)

                    if v_cross0[2] * v_cross1[2] < 0:  
                        y1i = n1 - L1 / L0 * h0i 
                    # print ("|||||||||||||||||||||||||||||||||||||||")

            NodeTranslated.append([self.npn[indx[i]][0], x1i, y1i, self.npn[indx[i]][3]])

        return np.array(NodeTranslated)
    def FindContactingSurfacebyElementID(self, solidno, face, surfaces=[]): 
        if len(surfaces) == 0: surfaces = self.Surface 

        ind = np.where(surfaces[:,0] == solidno)[0] 
        indx = 0
        for i in ind: 
            if int(surfaces[i][1]) == int(face): 
                indx = i 
                break 
        surface = surfaces[indx] 
        if int(surface[2]) == 3: ## 3 node surface 
            nd1 = np.where(surfaces[:,7:] == surface[7])[0]
            nd2 = np.where(surfaces[:,7:] == surface[8])[0]
            nd3 = np.where(surfaces[:,7:] == surface[9])[0]

            temp = np.intersect1d(nd1, nd2)
            temp = np.intersect1d(temp, nd3)
            if len(temp) ==2: 
                if surface[0] == surfaces[temp[0]][0]:      return surfaces[temp[1]]
                else:                                   return surfaces[temp[0]]
            else: 
                nolist =[]
                return nolist

        else:  ## 4 node surface
            nd1 = np.where(surfaces[:,7:] == surface[7])[0]
            nd2 = np.where(surfaces[:,7:] == surface[8])[0]
            nd3 = np.where(surfaces[:,7:] == surface[9])[0]
            nd4 = np.where(surfaces[:,7:] == surface[10])[0]

            temp = np.intersect1d(nd1, nd2)
            temp = np.intersect1d(temp, nd3)
            temp = np.intersect1d(temp, nd4)
            if len(temp) ==2: 
                if surface[0] == surfaces[temp[0]][0]:      return surfaces[temp[1]]
                else:                                   return surfaces[temp[0]]
            else: 
                nolist =[]
                return nolist
    def MoveNodesAtSomePositionXY(self, SearchPosition=[], ReplacePosition=[], nodes=[], distmargin=0.1E-03, debug=0): 
        if len(nodes) ==0: nodes = self.npn 

        idxsbtm=[]
        margin = 0.001E-03
        cnt = 0 
        while len(idxsbtm) < 2: 
            idxs10 = np.where(nodes[:, 1] > SearchPosition[0]-margin)[0]
            idxs11 = np.where(nodes[:, 1] < SearchPosition[0]+margin)[0]
            idxs20 = np.where(nodes[:, 2] > SearchPosition[1]-margin)[0]
            idxs21 = np.where(nodes[:, 2] < SearchPosition[1]+margin)[0]
            idxs1 = np.intersect1d(idxs10, idxs11)
            idxs2 = np.intersect1d(idxs20, idxs11)
            idxsbtm = np.intersect1d(idxs1, idxs2)
            
            margin += margin
            cnt += 1
            if cnt > 20: 
                print ("!!! ERROR. Cannot find the Pitch matching nodes") 
                break 
        if debug==1: print (" ** SEARCHING POSITION x=%7.3f, y=%7.3f"%(SearchPosition[0]*1000, SearchPosition[1]*1000))
        for id in idxsbtm: 
            if NodeDistance([0, SearchPosition[0], SearchPosition[1], 0.0], [0, nodes[id][1], nodes[id][2], 0.0]) < distmargin: 
                if debug==1: print ("  >> NODE %6d moved.  %7.3f, %7.3f --> %7.3f, %7.3f"%(nodes[id][0]-10**7, nodes[id][1]*1000, nodes[id][2]*1000, ReplacePosition[0]*1000,  ReplacePosition[1]*1000))
                nodes[id][1] = ReplacePosition[0]
                nodes[id][2] = ReplacePosition[1]
            
        return nodes 
    def ShiftNodesOnGrooveBottom(self, edge_groovebottom=[], orgnode=[], currentnode=[]): 
        
        margin = 0.1E-3
        allnodeids = []
        for edge in edge_groovebottom: 
            allnodeids.append(edge[0])
            allnodeids.append(edge[1])
        allnodeids=np.array(allnodeids)
        allnodeids=np.unique(allnodeids)

        for ids in allnodeids: 
            idx = np.where(orgnode[:,0] == ids)[0][0]
            N = orgnode[idx]
            idx = np.where(currentnode[:,0] == ids)[0][0]
            CN = currentnode[idx]

            ids1 = np.where(orgnode[:,1] > N[1]-margin)[0]
            ids2 = np.where(orgnode[:,1] < N[1]+margin)[0]            
            idxs = np.intersect1d(ids1, ids2)

            ids1 = np.where(orgnode[:,2] > N[2]-margin)[0]
            ids2 = np.where(orgnode[:,2] < N[2]+margin)[0]            
            idys = np.intersect1d(ids1, ids2)

            ids = np.intersect1d(idxs, idys)

            if len(ids) ==0: 
                for xs in idxs: 
                    print ("%4d, x=%7.2f"%(orgnode[xs][0]-10**7, orgnode[xs][1]*1000))
                for xs in idys: 
                    print ("%4d, y=%7.2f"%(orgnode[xs][0]-10**7, orgnode[xs][2]*1000))
                sys.exit()
            
            for id in ids: 
                ids = np.where(currentnode[:,0] == orgnode[id][0])[0][0]
                currentnode[ids][1] = CN[1]
                currentnode[ids][2] = CN[2]

        return currentnode
    
    def Keeping_gauge(self, n1, n2, orgn=[], curn=[]): 
        if n1[0] == n2[0]: 
            print ('Error. Kerf Gauge - the 2 nodes are the same %d'%(n1[0]-10**7))
            return n1, n2 
        ixs =  np.where(orgn[:,0] == n1[0])[0][0]; on1 = orgn[ixs]
        ixs =  np.where(orgn[:,0] == n2[0])[0][0]; on2 = orgn[ixs]

        ixs1 =  np.where(curn[:,0] == n1[0])[0][0]; tn1 = curn[ixs1]
        ixs2 =  np.where(curn[:,0] == n2[0])[0][0]; tn2 = curn[ixs2]
        o_d = Distance_2nodes(on1, on2, xy=12)
        t_d = Distance_2nodes(tn1, tn2, xy=12)
        if round(o_d, 6) == round(t_d, 6): 
            return n1, n2 
        
        cx = (tn1[1]+tn2[1])/2.0 
        cy = (tn1[2]+tn2[2])/2.0 

        ratio = t_d / o_d 
        v1x = tn1[1] - cx; v1y = tn1[2] - cy 
        v2x = tn2[1] - cx; v2y = tn2[2] - cy 

        tn1[1]  = cx + v1x * ratio; tn1[2] = cy + v1y * ratio 
        tn2[1]  = cx + v2x * ratio; tn2[2] = cy + v2y * ratio 
        return tn1, tn2 

    def Grouping_kerf_surfaces(self, topedges=[], side_surfaces=[], orgn=[], limitDepth=50): 
        MR = np.max(orgn[:,3]) ## model Tire Radius 
        sides = side_surfaces
        groups = []
        for edge in topedges: 
            group = []
            ix1 = np.where(sides[:, 7:11] == edge[0])[0]
            ix2 = np.where(sides[:, 7:11] == edge[1])[0]
            ix = np.intersect1d(ix1, ix2)
            e1 = edge[0]
            e2 = edge[1]
            # if len(ix) != 1: print (" Searched surf %d"%(len(ix)))
            cnt = 0 
            while len(ix) > 0: 
                cnt += 1 
                if cnt > limitDepth:   ## the limit of kerf depth.. (the number of surfaces in kerf) 
                    print (" Grouping error on edge %d"%(edge[3]))
                    break 

                group.append(sides[ix[0]])
                others = OtherNodes_InSurface(sides[ix[0]], [e1, e2])
                ixs = np.where(orgn[:,0] == others[0][0])[0][0]; cn = orgn[ixs]
                if abs(cn[3] - MR) < 0.1E-03 : break ## top 


                if sides[ix[0]][2] == 3: 
                    ix1 = np.where(sides[:,7:11]==e1)[0]
                    ix2 = np.where(sides[:,7:11]==others[0][0])[0]
                    ad0 = np.intersect1d(ix1, ix2)

                    if len(ad0) == 2: 
                        # print (" %d - adjacent surface %d, %d"%(sides[ix[0]][0]-10**7, sides[ad0[0]][0]-10**7, sides[ad0[1]][0]-10**7)) 
                        if sides[ix[0]][0] == sides[ad0[0]][0]: 
                            ad0=[ad0[1]]
                        else: 
                            ad0=[ad0[0]]

                        ixs = np.where(orgn[:,0] == e1)[0][0]; n1 = orgn[ixs]
                        ixs = np.where(orgn[:,0] == e2)[0][0]; n2 = orgn[ixs]
                        
                        d, P = DistanceFromLineToNode2D([0, sides[ad0[0]][4], sides[ad0[0]][5], sides[ad0[0]][6]], [n1, n2],xy=12)
                        if n1[1] > n2[1]: 
                            exmin = n2[1]; exmax = n1[1]
                        else: 
                            exmin = n1[1]; exmax = n2[1]
                        if n1[2] > n2[2]: 
                            eymin = n2[2]; eymax = n1[2]
                        else: 
                            eymin = n1[2]; eymax = n2[2]

                        if exmin <= P[1] and P[1] <= exmax and eymin <= P[2] and P[2] <= eymax : 
                            pass 
                        else: 
                            tmp = e1 
                            e1 = e2 
                            e2 = tmp 
                            ix1 = np.where(sides[:,7:11]==e1)[0]
                            ad0 = np.intersect1d(ix1, ix2)

                            if sides[ix[0]][0] == sides[ad0[0]][0]: 
                                ad0=[ad0[1]]
                            else: 
                                ad0=[ad0[0]]

                    # print ("selected %d"%(sides[ad0[0]][0]-10**7))

                    ## case 1: keep going up  >> meet 4-node surface
                    ## case 2: keep going down  >> meet 4-node surface 
                    ## case 3 : reversed       >> meet another 3-node surface 
                    ## case 4 : curved kerf  >> 
                    ########################################################
                    # case 1 : going down 
                    ## case i_1 : meet 4 node surface 
                    ## case 1_2 : no more elements (stops) 
                    ##          |_|_|_|
                    ##          |_\*/_|    << starred tri-anular 
                    if sides[ad0[0]][2] == 3:  ## connected to another 3 node surface 
                        group.append(sides[ad0[0]])
                        ct1 = OtherNodes_InSurface(sides[ad0[0]], [e1, others[0][0]])

                        ixs =  np.where(orgn[:,0] == ct1[0][0])[0][0]; tn = orgn[ixs]
                        if abs(tn[3] - MR) < 0.1E-03 : ## top 
                            break 
                        ix = ad0 
                        e2 = ct1[0][0]
                        # e2 = e1 

                        ix1 = np.where(sides[:, 7:11] == e1)[0]
                        ix2 = np.where(sides[:, 7:11] == e2)[0]
                        ixt = np.intersect1d(ix1, ix2)
                        if len(ixt) == 2: 
                            # print (" %d >>adjacent surface %d, %d"%(sides[ad0[0]][0]-10**7, sides[ixt[0]][0]-10**7, sides[ixt[1]][0]-10**7)) 
                            if sides[ixt[0]][0] == sides[ix[0]][0] : 
                                ix = [ixt[1]]
                            else: 
                                ix = [ixt[0]]
                            # print ("selected %d"%(sides[ix[0]][0]-10**7))
                        elif len(ixt) == 1: 
                            if sides[ixt[0]][0] == sides[ix[0]][0]:
                                break 
                        continue 

                    ix1 = np.where(sides[:,7:11]==e2)[0]
                    ix2 = np.where(sides[:,7:11]==others[0][0])[0]
                    ad1 = np.intersect1d(ix1, ix2)

                    if len(ad1) == 2: 
                        if sides[ix[0]][0] == sides[ad1[0]][0]: 
                            ad1=[ad1[1]]
                        else: 
                            ad1=[ad1[0]]
                    
                    ixs = np.where(orgn[:,0] == e1)[0][0]; n1 = orgn[ixs]
                    ixs = np.where(orgn[:,0] == e2)[0][0]; n2 = orgn[ixs]
                    ixs = np.where(orgn[:,0] == others[0][0])[0][0]; n3 = orgn[ixs] 

                    if len(ad1) > 0: 
                        if sides[ad1[0]][2] == 3: 
                            group.append(sides[ad1[0]])
                            ct1 = OtherNodes_InSurface(sides[ad1[0]], [e2, others[0][0]])
                            ixs =  np.where(orgn[:,0] == ct1[0][0])[0][0]; tn = orgn[ixs]
                            if abs(tn[3] - MR) < 0.1E-03 : ## top 
                                break 
                            ix = ad1 
                            e1 = ct1[0][0]
                            continue 

                    vert = [0, 0, 0, 1]
                    if len(ad0) ==1 and len(ad1) ==1: 
                        ct1 = OtherNodes_InSurface(sides[ad0[0]], [e1, others[0][0]])
                        ixs =  np.where(orgn[:,0] == ct1[0][0])[0][0]; ct1n1 = orgn[ixs]
                        ixs =  np.where(orgn[:,0] == ct1[1][0])[0][0]; ct1n2 = orgn[ixs]

                        vec1 = [0, ct1n2[1]-ct1n1[1], ct1n2[2]-ct1n1[2], ct1n2[3]-ct1n1[3]]
                        Ang_v1 = Angle_Between_Vectors(vert, vec1) 
                        down1 = 1 
                        if 0.75 > Ang_v1 and Ang_v1 > 2.5: # 0.75 ~ 45 degree, 2.5 ~ 145deg 
                            down1 = 0

                        ct2 = OtherNodes_InSurface(sides[ad1[0]], [e1, others[1][0]])
                        ixs =  np.where(orgn[:,0] == ct2[0][0])[0][0]; ct2n1 = orgn[ixs]
                        ixs =  np.where(orgn[:,0] == ct2[1][0])[0][0]; ct2n2 = orgn[ixs]

                        vec2 = [0, ct2n2[1]-ct2n1[1], ct2n2[2]-ct2n1[2], ct1n2[3]-ct2n1[3]]
                        Ang_v2 = Angle_Between_Vectors(vert, vec2) 
                        down2 = 1 
                        if 0.75 > Ang_v2 and Ang_v2 > 2.5: # 0.75 ~ 45 degree, 2.5 ~ 145deg 
                            down2 = 0

                        if down1 == 0 and down2 == 0 : 
                            break 
                        elif down1 == 1 and down2 == 0:
                            group.append(sides[ad0[0]]) 
                            ix = ad0
                            e1 = ct1n1[0]
                            e2 = ct1n2[0]

                        elif down1 == 0 and down2 == 1: 
                            group.append(sides[ad1[0]])
                            ix = ad1 
                            e1 = ct2n1[0]
                            e2 = ct2n2[0]
                        else: 
                            print ("# Check the direction of the next kerf surf %d"%(sides[ix[0]][0]-10**7))
                            break 
                    elif len(ad0) == 1: 
                        group.append(sides[ad0[0]]) 
                        ix = ad0
                        e1 = ct1[0][0]
                        e2 = ct1[1][0]
                    elif len(ad1) == 1: 
                        group.append(sides[ad1[0]])
                        ix = ad1 
                        e1 = ct2[0][0]
                        e2 = ct2[0][0]
                    else: 
                        break 

                else: 
                    e1 = others[0][0]
                    e2 = others[1][0]
                    ix1 = np.where(sides[:, 7:11] == e1)[0]
                    ix2 = np.where(sides[:, 7:11] == e2)[0]
                    ixt = np.intersect1d(ix1, ix2)
                    if len(ixt) == 2: 
                        if sides[ixt[0]][0] == sides[ix[0]][0] : 
                            ix = [ixt[1]]
                        else: 
                            ix = [ixt[0]]
                    elif len(ixt) == 1: 
                        if sides[ixt[0]][0] == sides[ix[0]][0]:
                            break 
                    # print (edge[3]-10**7, " NEXT > ", sides[ix[0]][0]-10**7)
                    # print ("  TOP %d, %d, other %d, %d"%(edge[0], edge[1], e1, e2))

            sf0=group[0]
            sf1 = group[len(group)-1] 

            ix = np.where(orgn[:,0]==sf0[7])[0][0]; n0=orgn[ix]
            ix = np.where(orgn[:,0]==sf1[7])[0][0]; n1=orgn[ix]
            length = sqrt((n0[1]-n1[1])**2 + (n0[2]-n1[2])**2)
            if length < 10E-03 and len(group) > 0: 
                groups.append(group)

        return groups

    def KeepKerfGaugeConstant(self, kerfedges=[], groovebottomsurf=[], surfaces=[], alledges=[], orgn_node=[], debug=0, surface_kerf=[]):
        
        ## some of kerf edges are actually groove edges 
        # self.Image(sf=groovebottomsurf,  file=Pattern.name+"-OnlyKerf.png", xy=self.GlobalXY, dpi=300, edge1=kerfedges)
        # print ("* Edges on kerfs =%d"%(len(kerfedges)), end=".\n  Filtering")

        # _,_, _, surf_kerf = self.Distinguish_kerf_groove( iedges=kerfedges, surf_bottom=groovebottomsurf, alledges=alledges, allsurfaces=surfaces, orgn=orgn_node)

        # print (" >> kerf=%d, grooves=%d"%(len(edge_kerf), len(gedge)))

        ## Grouping the surfaces of the kerf to find the matched nodes couple 

        surf_kerf = self.Grouping_kerf_surfaces(topedges=kerfedges, side_surfaces=surface_kerf, orgn=orgn_node)


        ###################################################################
        ## Start to group the connected edges
        ###################################################################
        distmargin=1.5E-03
        topedgegroup = self.Grouping_ConnectedEdges(kerfedges)
        print ("* Edges on kerfs =%d"%(len(kerfedges)), "Connected Edges=%d"%(len(topedgegroup)))

        # self.Grouping_edges_by_kerf(topedgegroup, surf_kerf)
        
        advgroup=[]
        all_edge = []
        for edges in topedgegroup: 
            advgroup.append(edges)
            # print (" EDGE GROUP ####### ")
            for edge in edges: 
                # print ("  > %d"%(edge[3]))
                all_edge.append(edge)
        
        debug =0
        group_kerfs=[]
        for i, edges in enumerate(advgroup):
            topedgegroup, opposite = self.DivideEdgegroupByDistance(i, advgroup, orgn_node, distmargin, debug=debug)
            # if len(topedgegroup) != 1 : print (" kerf %2d(edges=%2d) is divided into %d kerfs"%(i+1, len(advgroup[i]), len(topedgegroup)))
            opp =[]
            for j, egroup in enumerate(topedgegroup): 
                # print (egroup)
                group_kerfs.append([egroup, opposite[j]])
                for ed in opposite[j]: 
                    opp.append(ed)
            # if len(topedgegroup) > 0 :
            #     print ("%d Grp This is divided into "%(i+1), len(topedgegroup), "groups. 1st group of this have %d edges"%(len(topedgegroup[0])))
            # if  len(topedgegroup) == 0 : 
            #     print ("%d Grp This is divided into "%(i+1), len(topedgegroup), "groups. 1st group of this have 0 edges")

        print ("* Regrouped kerfs=%d (Initial %d)"%(len(group_kerfs), len(advgroup)))

        ## deleting duplicates 

        i=0
        while i < len(group_kerfs): 
            iN = len(group_kerfs[i][1])
            j = 0
            if debug ==1: 
                print("######################################################")
                print ("** node   1=%4d, 2=%4d,   i=%d"%(group_kerfs[i][1][0][0]-10**7, group_kerfs[i][1][0][1]-10**7, i))
            while j <len(group_kerfs): 
                jN = len(group_kerfs[j][0])

                
                if debug ==1: print ("  %2d      3=%4d, 4=%4d"%(j, group_kerfs[j][0][jN-1][0]-10**7, group_kerfs[j][0][jN-1][1]-10**7))
                if (group_kerfs[i][1][0][0] == group_kerfs[j][0][jN-1][1] and group_kerfs[i][1][0][1] == group_kerfs[j][0][jN-1][0] ) or \
                   (group_kerfs[i][1][0][0] == group_kerfs[j][0][jN-1][0] and group_kerfs[i][1][0][1] == group_kerfs[j][0][jN-1][1] ) : 
                    del(group_kerfs[j])
                    if debug ==1: print (" *  del j=%d"%(j))
                    break 
                if debug ==1: print ("          3=%4d, 4=%4d"%(group_kerfs[j][0][0][0]-10**7, group_kerfs[j][0][0][1]-10**7))
                if (group_kerfs[i][1][0][0] == group_kerfs[j][0][0][1] and group_kerfs[i][1][0][1] == group_kerfs[j][0][0][0] ) or \
                   (group_kerfs[i][1][0][0] == group_kerfs[j][0][0][0] and group_kerfs[i][1][0][1] == group_kerfs[j][0][0][1] ) : 
                    del(group_kerfs[j])
                    if debug ==1: print (" ** del j=%d"%(j))
                    break
                j += 1 
            i += 1

        print ("* The No. of kerfs to gauge adjust=%d"%(len(group_kerfs)))
        if debug ==2: 
            for i, group in enumerate(group_kerfs): 
                # if i > 65: 
                    self.Image(file=Pattern.name+"-Final_EDGE_GROUPING-"+str(i+1), edge0=group[0], edge1=group[1], eeid=1, textsize=5, enid=1, elw0=1.0, elw1=0.1)

        ## Surface grouping corresponding to kerf edges 
        debug = 0
        surf_kerfgroup=[]
        for i, group in enumerate(group_kerfs): 
            if debug ==1: print ("\n## %2d_th kerf (edges=%d) "%(i, len(group[0])))
            # print ("## %2d_th kerf (edges=%d) "%(i, len(group[0])))
            surfgroup=[]
            for edge in group[0]: 
                for surf in surf_kerf: 
                    if (edge[0] == surf[0][10] and edge[1] == surf[0][9]) or (edge[0] == surf[0][9] and edge[1] == surf[0][10]) : 
                        if debug ==1: 
                            print ("  EDGE %4d, %4d on %d (depth*2=%d) "%(edge[0]-10**7, edge[1]-10**7, edge[3]-10**7, len(surf)))
                            for sf in surf:
                                print (" %d, "%(sf[0]-10**7), end="")
                        surfgroup.append(surf)
                        break            
                
            surf_kerfgroup.append(surfgroup)

        # print ("KERF GROUPS ", len(surf_kerfgroup))
        debug = 1
        NodeRelocated= self.KerfNodesRelocation(surf_kerfgroup, orgn_node, debug=debug)

        # print ("no of relocation=%d"%(len(NodeRelocated)))
    def Grouping_edges_by_kerf(self, edge_group, surf_group): 
        edge_edge_index=[]
        gauge_group=[]
        for i, edges in enumerate(edge_group): 
            for edge in edges: 
                en1 = edge[0]; en2 = edge[1]
                for j, surfs in enumerate(surf_group):
                    if (surfs[0][9] == en1 and surfs[0][10] == en2 ) or (surfs[0][9] == en2 and surfs[0][10] == en1 ): 
                        SN = len(surfs)
                        if j == SN-1: 
                            opn1 = surfs[SN-1][9]
                            opn2 = surfs[SN-1][10]
                        else: 
                            opn1 = surfs[0][9]
                            opn2 = surfs[0][10]
                        print (" KERF EDGE (%d) %d, %d  // %d, %d"%(SN, en1-10**7, en2-10**7, opn1-10**7, opn2-10**7))
                        break 
            for k, sdgs in enumerate(edge_group): 
                if i == k: continue 
                for sdg in sdgs: 
                    if (sdg[0] == opn1 and sdg[1] == opn2) or (sdg[0] == opn2 and sdg[1] == opn1) : 
                        edge_edge_index.append([i, k])
                        print ("   >> FOUND %d, %d "%(sdg[0]-10**7, sdg[1]-10**7))
                        break 
        print ("GAUGE GROUPING #############")
        for idx in edge_edge_index: 
            print (edge_group[idx[0]][0][3]-10**3, " ::", edge_group[idx[1]][0][3]-10**3)

        # sys.exit()

    def DivideEdgegroupByDistance(self, index, groups, nodes, distmargin, debug=0): 
        # if index == 0:      debug =1 
        iN = len(groups[index])
        criticangle =10 
        divides = []
        opposite=[]
        if iN == 0:  ## in case that there is no edges . 
            divides.append(groups[index])
            return divides, opposite

        edges = groups[index]

        if len(edges) > 1: 
        
            t_div = []
            t_op = []
            vshape = 0 
            full = 0 
            for im in range(iN-1):
                if vshape == 0 : 
                    t_div.append(edges[im])
                    n1 = edges[im][0] 
                    n2 = edges[im][1]
                    idx = np.where(nodes[:,0]==n1)[0][0]
                    N1 = nodes[idx]
                    idx = np.where(nodes[:,0]==n2)[0][0]
                    N2 = nodes[idx]

                    n3 = edges[im+1][0]
                    n4 = edges[im+1][1]
                    idx = np.where(nodes[:,0]==n3)[0][0]
                    N3 = nodes[idx]
                    idx = np.where(nodes[:,0]==n4)[0][0]
                    N4 = nodes[idx]
                    # if edges[0][3] -10**7 == 1115 or edges[0][3] -10**7 == 1440: 
                    if debug ==1: 
                        print (" EDGE %d(%d): %d, %d - %d, %d dist=%7.2f"%(im, edges[im][3]-10**7, edges[im][0]-10**7, edges[im][1]-10**7, edges[im+1][0]-10**7, edges[im+1][1]-10**7, NodeDistance(N1, N4)*1000))

                    if N2[0] == N3[0]  and NodeDistance(N1, N4) < NodeDistance(N3, N4)  and NodeDistance(N1, N4) < distmargin: 
                        vshape =1
                        tN = len(t_div) 
                else: 
                    t_op.append(edges[im]) 
                    if debug ==1: print ("    Opposite in %d"%(edges[im][3]-10**7))
                    if len(t_op) == tN: 
                        full =1 
                        break 

            if vshape ==1: 
                if full ==0:    t_op.append(edges[iN-1])
                divides.append(t_div)
                opposite.append(t_op)

                kN = len(divides[0])
                jN = len(opposite[0])

                if debug ==1: print (" iN=%d, kN=%d, jN=%d"%(iN, kN, jN))

                if kN + jN < iN and kN == jN: 
                    # debug =1 
                    tedges=[]
                    [tedges.append(edge) for edge in edges ]
                    i = 0
                    for _ in range(kN+jN): 
                        if debug ==1: print ("del %d"%(tedges[0][3]-10**7))
                        del(tedges[0])
                    iN = len(tedges)
                    t_div = []
                    t_op = []
                    vshape = 0 
                    full = 0 
                    for im in range(iN-1):
                        if vshape == 0 : 
                            t_div.append(tedges[im])
                            n1 = tedges[im][0] 
                            n2 = tedges[im][1]
                            idx = np.where(nodes[:,0]==n1)[0][0]
                            N1 = nodes[idx]
                            idx = np.where(nodes[:,0]==n2)[0][0]
                            N2 = nodes[idx]

                            n3 = tedges[im+1][0]
                            n4 = tedges[im+1][1]
                            idx = np.where(nodes[:,0]==n3)[0][0]
                            N3 = nodes[idx]
                            idx = np.where(nodes[:,0]==n4)[0][0]
                            N4 = nodes[idx]
                            if debug ==1: 
                                print (" EDGE %d(%d): %d, %d - %d, %d dist=%7.2f"%(im, tedges[im][3]-10**7, tedges[im][0]-10**7, tedges[im][1]-10**7, tedges[im+1][0]-10**7, edges[im+1][1]-10**7, NodeDistance(N1, N4)*1000))

                            if N2[0] == N3[0]  and NodeDistance(N1, N4) < NodeDistance(N3, N4)  and NodeDistance(N1, N4) < distmargin: 
                                vshape =1
                                tN = len(t_div) 
                        else: 
                            t_op.append(tedges[im]) 
                            if debug ==1: print ("    Opposite in %d"%(edges[im][3]-10**7))
                            if len(t_op) == tN: 
                                full =1 
                                break 
                    dn = len(t_div)
                    on = len(t_op)
                    if debug ==1: print (" DN ON", dn, ',', on)
                    if on > 0: 
                        if dn > on: 
                            for _ in range(dn-on):
                                if debug ==1: print ("   ....... del %d"%(t_div[0][3]-10**7)) 
                                del(t_div[0])
                        elif dn < on: 
                            for _ in range(on-dn): 
                                temp= len(t_op)
                                del(t_op[temp-1])

                        divides.append(t_div)
                        opposite.append(t_op)
                        # debug = 0
                        return divides, opposite

                elif kN == jN : 
                    n1 = divides[0][0][0]
                    n4 = opposite[0][jN-1][1] 
                    idx = np.where(nodes[:,0] == n1)[0][0]
                    N1 = nodes[idx]
                    idx = np.where(nodes[:,0] == n4)[0][0]
                    N4 = nodes[idx]

                    if NodeDistance(N1, N4) > distmargin: 
                        divides=[]
                        opposite=[]

                    return divides, opposite
                else: 

                    cnt = iN - jN 
                    temp=[]
                    for i in range(cnt): 
                        temp.append(divides[0][0])
                        del(divides[0][0])
                    edges = np.array(temp)
                    iN = len(edges)

        #########################################################################
        ## if not v_shaped kerf ... >> divides block (kerf does not return to its initial position)
        ## There is a parallel edge to the edge 
        #########################################################################

        iN = len(groups[index])
        edges = groups[index]
        
        divides = []
        opposite=[]

        m = 0 
        n1 = edges[m][0] 
        n2 = edges[m][1]
        idx = np.where(nodes[:,0]==n1)[0][0]
        N1 = nodes[idx]
        idx = np.where(nodes[:,0]==n2)[0][0]
        N2 = nodes[idx]
        d12 = sqrt((N1[1]-N2[1])**2 + (N1[2]-N2[2])**2)

        rad_criticangle = 0.175  ## 10 degree angle 


        
        j = 0
        end = 0 
        loopcount = 0 
        debug =0
        while j < len(groups):  ## search the matching edge for each edge in groups[index][m] = edges[m] 
            if j == index:  
                j+=1
                continue
            temp = []
            opp = []
            kN = len(groups[j])
            k = 0 
            f = 0 
            if debug ==1: print ("**************** Forward ******************************")
            while k < kN: 
                rk = kN -1 -k 
                n3 = groups[j][rk][0]
                n4 = groups[j][rk][1]
                idx = np.where(nodes[:,0]==n3)[0][0]
                N3 = nodes[idx]
                idx = np.where(nodes[:,0]==n4)[0][0]
                N4 = nodes[idx]

                va = [0, N1[1]-N2[1], N1[2]-N2[2], 0.0]
                vb = [0, N3[1]-N4[1], N3[2]-N4[2], 0.0]
                ang = Angle_Between_Vectors (va, vb)
                if ang > rad_criticangle and ang < 2.967 :  ##  condition 1 : the 2 edges should be parallel 
                    if debug ==1: print ("   * m=%2d, j=%2d(index=%d), k=%2d: edge id=%6d (n1=%6d, n2=%6d), op edge=%d (n3=%6d, n4=%6d), angle=%7.2f"%(m, j, index, k, edges[m][3]-10**7, n1-10**7, n2-10**7, groups[j][rk][3]-10**7, n3-10**7, n4-10**7, degrees(ang)))
                    k += 1
                    continue

                dist1 = DistanceFromLineToNode2D(N3, [N1, N2], onlydist=1)
                dist2 = DistanceFromLineToNode2D(N4, [N1, N2], onlydist=1)
                if abs(dist1 - dist2)>distmargin / 2:                                 ## the difference of the distances from edge should be less than 0.75mm (distmargin/2)
                    if debug ==1: print ("   * m=%2d, j=%2d(index=%d), k=%2d: edge id=%6d (n1=%6d, n2=%6d), op edge=%d (n3=%6d, n4=%6d), dist1=%7.2f, dist2=%7.2f"%(m, j, index, k, edges[m][3]-10**7, n1-10**7, n2-10**7, groups[j][rk][3]-10**7, n3-10**7, n4-10**7, dist1*1000, dist2*1000))
                    k += 1
                    continue

                if dist1 > dist2: dist=dist1
                else: dist = dist2                ## reference distance from line > greater value

                D13 = NodeDistance(N1, N3)
                D12 = NodeDistance(N1, N2)
                D24 = NodeDistance(N2, N4)
                D34 = NodeDistance(N3, N4)
                D23 = NodeDistance(N2, N3)
                D14 = NodeDistance(N1, N4)

                # if debug ==1: 
                #     print ("   * m=%2d, j=%2d(index=%d), k=%2d: edge id=%6d (n1=%6d, n2=%6d), op edge=%d (n3=%6d, n4=%6d), dist=%7.2f, D23=%7.2f, D14=%7.2f"%(m, j, index, k, edges[m][3]-10**7, n1-10**7, n2-10**7, \
                #         groups[j][rk][3]-10**7, n3-10**7, n4-10**7, dist*1000, D23*1000, D14*1000))
                
                if dist <= distmargin and   (D23 < D12 and D14 < D12 ) : # and (D23 + D14) < D12 : 
                    if (D12 > distmargin * 2 and (D23 + D14) < D12) or (D12 <=  distmargin * 2 ): 
                        if debug ==1: 
                            print ("   > edge is added to 'temp' (dist margin=%7.2f, Lenght N1~N2 = %7.2f, N3~N4 = %7.2f, Dist N2~3=%7.2f, N1~4=%7.2f)"%(distmargin*1000, D12*1000, D34*1000, D23*1000, D14*1000), end="\n\n")
                        temp.append(edges[m])
                        opp.append(groups[j][rk])
                        k += 1     ## k += 1 
                        m += 1     ## if found the matched edge, go to next edge (m += 1 )

                        if m == iN:     ## if reached the edge, then break. 
                            if debug ==1:     print(" *> Group with %d edges is added. Edge in the opposite =%d\n"%(len(temp), groups[j][k-1][3]-10**7))
                            divides.append(temp)
                            opposite.append(opp)
                            end = 1
                            break 

                        ## Going to the next edge. 
                        n1 = edges[m][0] 
                        n2 = edges[m][1]
                        idx = np.where(nodes[:,0]==n1)[0][0]
                        N1 = nodes[idx]
                        idx = np.where(nodes[:,0]==n2)[0][0]
                        N2 = nodes[idx]
                        f = 1 
                        if k == kN: 
                            break 
                    else: 
                        k += 1 
                        continue 
                
                elif f == 1 and dist > distmargin: 
                    divides.append(temp)
                    opposite.append(opp)

                    if debug ==1:         print(" > Group with %d edges is added. Edge in the opposite =%d\n"%(len(temp), groups[j][k][3]-10**7))
                    
                    temp = []
                    opp = []
                    break 
                else: 
                    k += 1
                    continue 
            
            if end ==1: 
                break 
            if f == 0: ## if no matching edge, try reverse direction edge... 
                if debug ==1: print ("**************** REVERSE ******************************")
                k = 0 
                while k <kN: 
                    n3 = groups[j][k][1]
                    n4 = groups[j][k][0]
                    idx = np.where(nodes[:,0]==n3)[0][0]
                    N3 = nodes[idx]
                    idx = np.where(nodes[:,0]==n4)[0][0]
                    N4 = nodes[idx]
                    va = [0, N1[1]-N2[1], N1[2]-N2[2], 0.0]
                    vb = [0, N3[1]-N4[1], N3[2]-N4[2], 0.0]
                    ang = Angle_Between_Vectors (va, vb)
                    if ang > rad_criticangle and ang < 2.967 :
                        if debug ==1: print ("   * m=%2d, j=%2d(index=%d), k=%2d: edge id=%6d (n1=%6d, n2=%6d), op edge=%d (n3=%6d, n4=%6d), Anlge=%7.2f"%(m, j, index, k, edges[m][3]-10**7, n1-10**7, n2-10**7, groups[j][k][3]-10**7, n3-10**7, n4-10**7,  degrees(ang)))
                        k += 1
                        continue
                    dist1 = DistanceFromLineToNode2D(N4, [N1, N2], onlydist=1)
                    dist2 = DistanceFromLineToNode2D(N3, [N1, N2], onlydist=1)
                    if abs(dist1 - dist2)>distmargin/2: 
                        if debug ==1: print ("   * m=%2d, j=%2d(index=%d), k=%2d: edge id=%6d (n1=%6d, n2=%6d), op edge=%d (n3=%6d, n4=%6d), dist1=%7.2f, dist2=%7.2f"%(m, j, index, k, edges[m][3]-10**7, n1-10**7, n2-10**7, groups[j][k][3]-10**7, n3-10**7, n4-10**7, dist1*1000, dist2*1000))
                        k += 1
                        continue
                    if dist1 > dist2: dist=dist1
                    else: dist = dist2
                    D13 = NodeDistance(N1, N3)
                    D12 = NodeDistance(N1, N2)
                    D24 = NodeDistance(N2, N4)
                    D34 = NodeDistance(N3, N4)
                    D23 = NodeDistance(N2, N3)

                    if debug ==1: print ("   * m=%2d, j=%2d(index=%d), k=%2d: edge id=%6d (n1=%6d, n2=%6d), op edge=%d (n3=%6d, n4=%6d), dist=%7.2f, D13=%7.2f, D24=%7.2f"%(m, j, index, k, edges[m][3]-10**7, n1-10**7, n2-10**7,\
                        groups[j][k][3]-10**7, n3-10**7, n4-10**7, dist*1000, D13*1000, D24*1000))
                    
                    if dist <= distmargin and   (D23 < D12 and D14 < D12 ) : 
                        if (D12 > distmargin * 2 and (D23 + D14) < D12) or (D12 <=  distmargin * 2 ): 
                            if debug ==1: 
                                print ("  >> edge is added to 'temp' (dist margin=%7.2f, Lenght N1~N2 = %7.2f, N3~N4 = %7.2f, Dist N1~3=%7.2f, N2~4=%7.2f)"%(distmargin*1000, D12*1000, D34*1000, D13*1000, D24*1000), end="\n\n")
                            temp.append(edges[m])
                            opp.append(groups[j][k])
                            k += 1
                            m += 1
                            if m == iN : 
                                if debug ==1: 
                                    print(" >> Group with %d edges is added. Edge in the opposite =%d\n"%(len(temp), groups[j][k-1][3]-10**7))
                                divides.append(temp)
                                opposite.append(opp)
                                end = 1
                                break 

                            n1 = edges[m][0] 
                            n2 = edges[m][1]
                            idx = np.where(nodes[:,0]==n1)[0][0]
                            N1 = nodes[idx]
                            idx = np.where(nodes[:,0]==n2)[0][0]
                            N2 = nodes[idx]
                            f = 1 
                        else: 
                            k += 1
                            continue 

                        
                        if k == kN: 
                            if debug ==1: 
                                print(" >>> Group with %d edges is added. Edge in the opposite =%d\n"%(len(temp), groups[j][k-1][3]-10**7))
                            divides.append(temp)
                            opposite.append(opp)
                            j = 0 
                            break
                        
                    elif f == 1 and dist > distmargin: 
                        divides.append(temp)
                        opposite.append(opp)
                        if debug ==1: 
                            print(" >>>> Group with %d edges is added. Edge in the opposite =%d\n"%(len(temp), groups[j][k][3]-10**7))
                        temp = []
                        opp = []
                        break 
                    else: 
                        k += 1
                        continue 
            if end ==1: 
                break 
            if f ==0: 
                j += 1
            else:
                # print ("** FOUND in direction ")
                if len(temp)>0: 
                    divides.append(temp)
                    opposite.append(opp)
                    if debug ==1: 
                        print(" >> Group with %d edges is added. "%(len(temp)))
                    n1 = edges[m][0] 
                    n2 = edges[m][1]
                    idx = np.where(nodes[:,0]==n1)[0][0]
                    N1 = nodes[idx]
                    idx = np.where(nodes[:,0]==n2)[0][0]
                    N2 = nodes[idx]
                j = 0

            if j == len(groups) and m < iN-1: 
                if len(temp)> 0 : 
                    divides.append(temp)
                    opposite.append(opp)
                
                m += 1
                n1 = edges[m][0] 
                n2 = edges[m][1]
                idx = np.where(nodes[:,0]==n1)[0][0]
                N1 = nodes[idx]
                idx = np.where(nodes[:,0]==n2)[0][0]
                N2 = nodes[idx]
                j = 0 

                loopcount += 1 
                if loopcount > 30: 
                    print (" No found matched kerf on EL %d"%(edges[m][3]))
                    break 
                    # sys.exit()
        debug = 0 
        i = 0
        while i < len(divides): 
            iN = len(divides[i])

            wide = 0 
            for j in range(iN): 
                n1 = divides[i][j][0]
                n2 = divides[i][j][1]
                n3 = opposite[i][j][0]
                n4 = opposite[i][j][1]

                idx = np.where(nodes[:,0]==n1)[0][0]
                N1 = nodes[idx]
                idx = np.where(nodes[:,0]==n2)[0][0]
                N2 = nodes[idx]

                idx = np.where(nodes[:,0]==n3)[0][0]
                N3 = nodes[idx]
                idx = np.where(nodes[:,0]==n4)[0][0]
                N4 = nodes[idx]

                dist1 = DistanceFromLineToNode2D(N3, [N1, N2], onlydist=1)
                dist2 = DistanceFromLineToNode2D(N4, [N1, N2], onlydist=1)

                # print (" review distance (kerf gauge) = %7.2f, %7.2f"%(dist1*1000, dist2*1000))

                if dist1 > distmargin or dist2 > distmargin: 
                    wide =1 
                    break 

            if wide ==1: 
                del(divides[i])
                del(opposite[i])
                i -= 1
            i += 1

        if debug ==1: 
            print ("   initial groups = %d"%(len(groups)))
            print (">>>>>>>>>>>>>>>>>>>>>> Returning edge groups > %d"%(len(divides)))
        return divides, opposite
    def KerfNodesRelocation(self, kerf_surf, origin, debug=0):  ## origin = model node set
        ### kerf_surf : surface group of kerfs that comprise the kerf wall 

        relocated = []

        # Wratio = self.TargetTDW / self.TreadDesignWidth * self.TargetGD / self.ModelGD
        # Lratio = self.TargetPL / self.pitchlength  * self.TargetGD / self.ModelGD

        # print(" Kerf Ga : Width Ratio=%.2f, Length Ratio=%.2f"%(Wratio, Lratio))

        for kerf_group in kerf_surf: 
            for i, surfs in enumerate(kerf_group): 
                protrusion = 0 
                ## find bottom nodes in the kerf sides 
                ## this is the base line for the node position. 
                ndo = []
                ndn = []
                tri = 0 
                for j, surf in enumerate(surfs):
                    if surf[10] < 10**7: 
                        tri = 1 
                        break 
                    n1 = origin[np.where(origin[:,0]==surf[7])[0][0]]
                    n2 = origin[np.where(origin[:,0]==surf[8])[0][0]]
                    n3 = origin[np.where(origin[:,0]==surf[9])[0][0]]
                    n4 = origin[np.where(origin[:,0]==surf[10])[0][0]]
                    ndo.append([(n1[3]+n2[3])/2.0, n1, n2, n3, n4])
                    n1 = self.npn[np.where(self.npn[:,0]==surf[7])[0][0]]
                    n2 = self.npn[np.where(self.npn[:,0]==surf[8])[0][0]]
                    n3 = self.npn[np.where(self.npn[:,0]==surf[9])[0][0]]
                    n4 = self.npn[np.where(self.npn[:,0]==surf[10])[0][0]]
                    ndn.append([(n1[3]+n2[3])/2.0, n1, n2, n3, n4])
                
                Nsurf = int(len(surfs) / 2) 

                if tri == 1: 
                    continue 


                mz = 10**7 
                for nd in ndo:
                    if nd[0] < mz : 
                        mz = nd[0]
            
                for od, nd in zip(ndo, ndn):
                    if od[0] == mz: 
                        refo = [od[1], od[2]] ## kerf bottom nodes .. 
                        refn = [nd[1], nd[2]]

                cnt = 0   
                reDo = 0   
                for od, nd in zip(ndo, ndn):
                    cnt += 1 
                    d03, inPoint03 = DistanceFromLineToNode2D(od[3], refo, xy=12)
                    d04, inPoint04 = DistanceFromLineToNode2D(od[4], refo, xy=12)

                    d13, inPoint13 = DistanceFromLineToNode2D(nd[3], refn, xy=12)
                    d14, inPoint14 = DistanceFromLineToNode2D(nd[4], refn, xy=12)

                    V1 = [0, refo[1][1]-refo[0][1], refo[1][2]-refo[0][2], 0.0]
                    V2 = [0, od[4][1]-od[3][1],  od[4][2]-od[3][2], 0.0]

                    ang = Angle_Between_Vectors(V1, V2)

                    if ang > 0: 
                        LefN03 = refo[0]; LefN04 = refo[1]
                        LefN13 = refn[0]; LefN14 = refn[1]
                    else: 
                        LefN03 = refo[1]; LefN04 = refo[0]
                        LefN13 = refn[1]; LefN14 = refn[0]
                    
                    V03 = [(od[3][1]-inPoint03[1]) , (od[3][2]-inPoint03[2]) ]

                    ix3 = np.where(self.npn[:,0]==nd[3][0])[0][0]
                    ix4 = np.where(self.npn[:,0]==nd[4][0])[0][0]
                    
                    ix = ix3 
                    self.npn[ix3][1] = inPoint13[1] + V03[0]  
                    self.npn[ix3][2] = inPoint13[2] + V03[1]

                    if cnt == 1: 
                        topN13 = self.npn[ix3]

                    else:
                        if od[3][1] - LefN03[1] !=0 or od[3][2] - LefN03[2] !=0 : 
                            ang03 = Angle_3nodes (od[4], od[3], LefN03, xy=12) - 1.5707963
                            ang13 = Angle_3nodes (self.npn[ix4], self.npn[ix3], LefN13,  xy=12)  - 1.5707963

                            # if od[3][0] -10**7 == 1988 or od[3][0] -10**7 == 1989 or od[4][0] -10**7 == 1988 or od[4][0] -10**7 == 1989: 
                            #     print ("NODE %d, %d"%(od[3][0] -10**7, od[4][0] -10**7))
                            #     print ("%.3f, %.3f, , %.3f, %.3f, 3"%(od[3][1]*1000, od[3][2]*1000, self.npn[ix3][1]*1000, self.npn[ix3][2]*1000))  
                            #     print ("%.3f, %.3f, , %.3f, %.3f, 4\n"%(od[4][1]*1000, od[4][2]*1000, self.npn[ix4][1]*1000, self.npn[ix4][2]*1000))  
                                
                            #     print ("%.3f, %.3f, , %.3f, %.3f, ref3"%(LefN03[1]*1000, LefN03[2]*1000, LefN13[1]*1000, LefN13[2]*1000))  
                            #     print ("%.3f, %.3f, , %.3f, %.3f, ref4\n"%(LefN04[1]*1000, LefN04[2]*1000, LefN14[1]*1000, LefN14[2]*1000))
                            #     print ("%.3f, %.3f, , %.3f, %.3f, vec3, norm"%( V03[0]*1000, V03[1]*1000, inPoint13[1]*1000, inPoint13[2]*1000))   
                            #     print ("Angle 03=, %.3f, %.3f\n"%(degrees(ang03), degrees(ang13)))
                            
                            # if od[3][0] -10**7 == 1682 or od[3][0] -10**7 == 1697 or od[4][0] -10**7 == 1682 or od[4][0] -10**7 == 1697: 
                            #     print ("NODE %d, %d"%(od[3][0] -10**7, od[4][0] -10**7))
                            #     print ("%.3f, %.3f, , %.3f, %.3f, 3"%(od[3][1]*1000, od[3][2]*1000, self.npn[ix3][1]*1000, self.npn[ix3][2]*1000))  
                            #     print ("%.3f, %.3f, , %.3f, %.3f, 4\n"%(od[4][1]*1000, od[4][2]*1000, self.npn[ix4][1]*1000, self.npn[ix4][2]*1000))  
                                
                            #     print ("%.3f, %.3f, , %.3f, %.3f, ref3"%(LefN03[1]*1000, LefN03[2]*1000, LefN13[1]*1000, LefN13[2]*1000))  
                            #     print ("%.3f, %.3f, , %.3f, %.3f, ref4\n"%(LefN04[1]*1000, LefN04[2]*1000, LefN14[1]*1000, LefN14[2]*1000))
                            #     print ("%.3f, %.3f, , %.3f, %.3f, vec3, norm"%( V03[0]*1000, V03[1]*1000, inPoint13[1]*1000, inPoint13[2]*1000))   
                            #     print ("Angle 03=, %.3f, %.3f\n"%(degrees(ang03), degrees(ang13)))

                            if ang03 * ang13 < 0.0  : 
                                ix = np.where(self.npn[:,0]==nd[3][0])[0][0]

                                d13 = sqrt (  (topN13[1] - self.npn[ix3][1])**2 + (topN13[2] - self.npn[ix3][2])**2 )
                                if d13 > 0.0001: 
                                        
                                    V13 = [(self.npn[ix3][1] - topN13[1])/d13, (self.npn[ix3][2] - topN13[2])/d13]  ## vector from top to bottom 
                                    
                                    slope13 = sqrt (  (topN13[1] - LefN13[1])**2 + (topN13[2] - LefN13[2])**2 ) / (topN13[3] - LefN13[3])  

                                    self.npn[ix3][1] =  topN13[1] + V13[0]  * slope13 * (topN13[3] - self.npn[ix3][3])  
                                    self.npn[ix3][2] =  topN13[2] + V13[1]  * slope13 * (topN13[3] - self.npn[ix3][3]) 

                                    reDo += 1 

                            if reDo ==1 and Nsurf > cnt -1: 
                                    for k in range(cnt-2, 1, -1): 
                                        idx = np.where(self.npn[:,0]==ndn[k][2][0])[0][0]; ni = self.npn[idx]
                                        idx = np.where(self.npn[:,0]==ndn[k][3][0])[0][0]; nj = self.npn[idx]
                                        

                                        slope1 = sqrt((nj[1]-ni[1])**2 + (nj[2]-ni[2])**2)
                                        di0 =  sqrt((ndo[k][3][1]-ndo[k][2][1])**2 + (ndo[k][3][2]-ndo[k][2][2])**2) 
                                        if di0 > 0.0001: 
                                            slope0 = di0 / (ndo[k][3][3]-ndo[k][2][3])

                                            vec = [(ndo[k][3][1]-ndo[k][2][1]) / di0  , (ndo[k][3][2]-ndo[k][2][2]) / di0]
                                            self.npn[idx][1] = ni[1] + vec[0] * (nj[3]-ni[3])  * slope0
                                            self.npn[idx][2] = ni[2] + vec[1] * (nj[3]-ni[3])  * slope0
                                    reDo += 1 

                    relocated.append(self.npn[ix3][0])

                    V04 = [(od[4][1]-inPoint04[1])  , (od[4][2]-inPoint04[2]) ]

                    ix = ix4 
                    self.npn[ix4][1] = inPoint14[1] + V04[0]  
                    self.npn[ix4][2] = inPoint14[2] + V04[1]

                    if cnt == 1:  
                        topN14 = self.npn[ix4]
                        
                    else:
                        if od[4][1] - LefN04[1] !=0 or od[4][2] - LefN04[2] !=0 : 
                            ang04 = Angle_3nodes (od[3], od[4], LefN04, xy=12) - 1.5707963
                            ang14 = Angle_3nodes (self.npn[ix3], self.npn[ix4], LefN14,  xy=12)  - 1.5707963

                            # if od[3][0] -10**7 == 1988 or od[3][0] -10**7 == 1989 or od[4][0] -10**7 == 1988 or od[4][0] -10**7 == 1989: 
                            #     print ("** NODE %d, %d"%(od[3][0] -10**7, od[4][0] -10**7))
                            #     print ("%.3f, %.3f, , %.3f, %.3f, 3"%(od[3][1]*1000, od[3][2]*1000, self.npn[ix3][1]*1000, self.npn[ix3][2]*1000))  
                            #     print ("%.3f, %.3f, , %.3f, %.3f, 4\n"%(od[4][1]*1000, od[4][2]*1000, self.npn[ix4][1]*1000, self.npn[ix4][2]*1000))  
                                
                            #     print ("%.3f, %.3f, , %.3f, %.3f, ref3"%(LefN03[1]*1000, LefN03[2]*1000, LefN13[1]*1000, LefN13[2]*1000))  
                            #     print ("%.3f, %.3f, , %.3f, %.3f, ref4\n"%(LefN04[1]*1000, LefN04[2]*1000, LefN14[1]*1000, LefN14[2]*1000))
                            #     print ("%.3f, %.3f, , %.3f, %.3f, vec4, norm"%( V04[0]*1000, V04[1]*1000, inPoint14[1]*1000, inPoint14[2]*1000))   
                            #     print ("Angle 03=, %.3f, %.3f\n"%(degrees(ang04), degrees(ang14)))
                            
                            # if od[3][0] -10**7 == 1682 or od[3][0] -10**7 == 1697 or od[4][0] -10**7 == 1682 or od[4][0] -10**7 == 1697: 
                            #     print ("NODE %d, %d"%(od[3][0] -10**7, od[4][0] -10**7))
                            #     print ("%.3f, %.3f, , %.3f, %.3f, 3"%(od[3][1]*1000, od[3][2]*1000, self.npn[ix3][1]*1000, self.npn[ix3][2]*1000))  
                            #     print ("%.3f, %.3f, , %.3f, %.3f, 4\n"%(od[4][1]*1000, od[4][2]*1000, self.npn[ix4][1]*1000, self.npn[ix4][2]*1000))  
                                
                            #     print ("%.3f, %.3f, , %.3f, %.3f, ref3"%(LefN03[1]*1000, LefN03[2]*1000, LefN13[1]*1000, LefN13[2]*1000))  
                            #     print ("%.3f, %.3f, , %.3f, %.3f, ref4\n"%(LefN04[1]*1000, LefN04[2]*1000, LefN14[1]*1000, LefN14[2]*1000))
                            #     print ("%.3f, %.3f, , %.3f, %.3f, vec4, norm"%( V04[0]*1000, V04[1]*1000, inPoint14[1]*1000, inPoint14[2]*1000))   
                            #     print ("Angle 03=, %.3f, %.3f\n"%(degrees(ang04), degrees(ang14)))
                            
                            if ang04 * ang14 < 0.0   :
                                ix = np.where(self.npn[:,0]==nd[4][0])[0][0]

                                d14 = sqrt (  (topN14[1] - self.npn[ix4][1])**2 + (topN14[2] - self.npn[ix4][2])**2 )
                                if d14 > 0.0001: 
                                        
                                    V14 = [(self.npn[ix4][1] - topN14[1])/d14, (self.npn[ix4][2] - topN14[2])/d14]  ## vector from top to bottom 
                                    
                                    slope14 = sqrt (  (topN14[1] - LefN14[1])**2 + (topN14[2] - LefN14[2])**2 ) / (topN14[3] - LefN14[3])  

                                    self.npn[ix4][1] =  topN14[1] + V14[0]  * slope14 * (topN14[3] - self.npn[ix4][3])  
                                    self.npn[ix4][2] =  topN14[2] + V14[1]  * slope14 * (topN14[3] - self.npn[ix4][3]) 

                                    reDo += 1 

                            if reDo ==1 and Nsurf > cnt -1: 
                                    for k in range(cnt-2, -1, -1): 
                                        idx = np.where(self.npn[:,0]==ndn[k][1][0])[0][0]; ni = self.npn[idx]
                                        idx = np.where(self.npn[:,0]==ndn[k][4][0])[0][0]; nj = self.npn[idx]
                                        

                                        slope1 = sqrt((nj[1]-ni[1])**2 + (nj[2]-ni[2])**2)

                                        di0 =  sqrt((ndo[k][4][1]-ndo[k][1][1])**2 + (ndo[k][4][2]-ndo[k][1][2])**2) 
                                        if di0 > 0.0001: 
                                            slope0 = di0 / (ndo[k][4][3]-ndo[k][1][3])

                                            vec = [(ndo[k][4][1]-ndo[k][1][1]) / di0  , (ndo[k][4][2]-ndo[k][1][2]) / di0]
                                            self.npn[idx][1] = ni[1] + vec[0] * (nj[3]-ni[3]) * slope0
                                            self.npn[idx][2] = ni[2] + vec[1] * (nj[3]-ni[3]) * slope0

                                    reDo += 1 

                    relocated.append(self.npn[ix][0])

        return relocated
         
    def ExtendMainGrooveEdge_InlateralGroove(self, cedge, redge, bottomedges, groovebottom): 
        """
        Searching th edge to connect the main groove in the lateral groove 
        cedge : the edge which is added just before 
        redge : reference edge (= boundary edge in the lateral groove) for searching the connecting edge 
               - next reference edge is going to be returned also. 
        tedge : connecting edge 
                  ______         <- redge which is return  
                 |      |
                 |      |        <- tedge (right vertical edge)
                 |______|        <- tedge which is input 

        bottomedges : all edges in the main groove surfaces 
        groovebottom : all surfaces of full depth groove 
        """
        ## cedge : last edge, redge : reference edge for searching the next edge 
        ## bottomedges : all edges from the main groove bottem surface 

        ## check the ref. surface (redge) and current surface(cedge) is adjacent or not 
        ## if they are adjacent ref. surface should be changed to next surface 

        rdx = np.where(groovebottom[:, 0] == redge[3])[0][0]
        cdx = np.where(groovebottom[:, 0] == cedge[3])[0][0]
        rnd =[]; cnd =[]
        rn = int(groovebottom[rdx][2]); cn = int(groovebottom[cdx][2])
        cnt = 0
        for i in range(7, 7+rn): 
            for j in range(7, 7+cn): 
                if groovebottom[rdx][i] == groovebottom[cdx][j]: 
                    cnt += 1
        if cnt == 2: 
            idx1 = np.where(bottomedges[:,0] == redge[1])[0]
            idx2 = np.where(bottomedges[:,1] == redge[0])[0]

            idx = np.intersect1d(idx1, idx2).reshape(-1)

            if len(idx) != 1: 
                print ("ERROR, TOO many / few edge(s) in the ref. surface (searching the next edge in the lateral groove)")
                sys.exit()

            redge = bottomedges[int(idx[0])]

        idx = np.where(groovebottom[:, 0] == redge[3])[0][0]
        rsf = groovebottom[idx]   ## reference surface (in the lateral groove)
        

        cm_node_rsf=[]
        rnode =[]
       
        for j, rcm in enumerate(rsf): 
            if j>=7 and (rcm == redge[0] or rcm == redge[1]): 
                cm_node_rsf.append(j)
            if j>=7 and rcm != 0: 
                rnode.append(rcm)

        rnp =[]
        tpn =[]
        if rsf[2] == 4: 
            if cm_node_rsf[0] == 7 and cm_node_rsf[1] == 8: 
                rpn = [9, 10]
                tpn = [10, 7]
            elif cm_node_rsf[0] == 7 and cm_node_rsf[1] == 10: 
                rpn = [8, 9]
                tpn = [9, 10]
            elif cm_node_rsf[0] == 9 and cm_node_rsf[1] == 10: 
                rpn = [7, 8]
                tpn = [8, 9]
            elif cm_node_rsf[0] == 8 and cm_node_rsf[1] == 9: 
                rpn = [10, 7]
                tpn = [7, 8]
            else: 
                print ("ERROR", cm_node_rsf)
        else: 
            if cm_node_rsf[0] == 7 and cm_node_rsf[1] == 8: 
                rpn = [8, 9]
                tpn = [9, 7]
            elif cm_node_rsf[0] == 7 and cm_node_rsf[1] == 9: 
                rpn = [7, 8]
                tpn = [8, 9]
            elif cm_node_rsf[0] == 8 and cm_node_rsf[1] == 9: 
                rpn = [9, 7]
                tpn = [7, 8]

        idx = np.where(self.npn[:, 0] == rsf[rpn[0]])[0][0]
        N1 = self.npn[idx]
        idx = np.where(self.npn[:, 0] == rsf[rpn[1]])[0][0]
        N2 = self.npn[idx]

        nextref= [rsf[rpn[0]], rsf[rpn[1]], 1, rsf[0], N1[1], N1[2], N1[3], N2[1], N2[2], N2[3]]


        idx = np.where(groovebottom[:, 7:] == cedge[1])
        idx = idx[0]
        if len(idx) < 3: 
            print (f"ERROR! Too few surfaces to fine next groove edge (The number should be equal or greater than 3) : {idx}")
            # self.ImageEdge(bottomedges, file=Pattern.name+"-ERROR to trim lateral groove", dpi=1000, edge1=[cedge], edge2=[redge], eid=1, tsize=3)#, nid=1, eid=1, tsize=3)
            sys.exit()

        teln=[]
        for j in idx: 
            if groovebottom[j][0] != cedge[3] and groovebottom[j][0] != redge[3]: 
                jn = int(groovebottom[j][2])
                gonext = 0
                tnode = []
                for k in range(7, 7+jn):
                    if cedge[1] == redge[1]: 
                        if groovebottom[j][k] == cedge[0] or groovebottom[j][k] == redge[0]: 
                            gonext =1 
                    else: 
                        if groovebottom[j][k] == cedge[0] or groovebottom[j][k] == redge[1]: 
                            gonext =1 
                    tnode.append(groovebottom[j][k])
                
                if gonext ==1: continue 
                cnt = 0
                for t in tnode: 
                    for r in rnode: 
                        if r == t: cnt += 1
                if cnt == 2: 
                    teln.append(j)
                    break 
        if len(teln) == 0: 
            print ("ERROR, Cannot find the next Surface which has next edge")
            print ("Current edge", cedge[0]-1000_0000, cedge[1]-1000_0000, "in Surf", cedge[3]-1000_0000)
            print ("Current Ref ", redge[0]-1000_0000, redge[1]-1000_0000, "in Surf", redge[3]-1000_0000)
            for j in idx: 
                if groovebottom[j][0] != cedge[3] and groovebottom[j][0] != redge[3]: 
                    jn = int(groovebottom[j][2])
                    tnode=[]
                    for k in range(7, 7+jn):
                        tnode.append(groovebottom[j][k]-1000_0000)
                    print (" Surface Candidate : ", tnode)
            # self.ImageEdge(bottomedges, file=Pattern.name+"-ERROR NEXT EDGE IN Lateral Groove", edge1=[cedge], edge2=[redge], dpi=1000, nid=1, tsize=0.5)#, eid=1)
            sys.exit()
        
        tsurf = -1
        for i in teln: 
            tsf = groovebottom[i]

            tnode =[]
            cn = int(tsf[2])
            for j in range(7, 7+cn): 
                tnode.append(tsf[j])
            cnt = 0
            com_node=[]
            for t in tnode: 
                for r in rnode: 
                    if r==t: 
                        cnt += 1
                        com_node.append(t)
                        break
            if cnt ==2 : 
                tsurf = i
                break

        if tsurf == -1:  
            print ("Surf. ")
            print ("Node in ref.Surf(", rsf[0]-1000_0000, "): ",  rsf[7]-1000_0000, rsf[8]-1000_0000, rsf[9]-1000_0000, rsf[10]-1000_0000)
            print ("Node in Cur.Surf(", tsf[0]-1000_0000, "): ", tsf[7]-1000_0000, tsf[8]-1000_0000, tsf[9]-1000_0000, tsf[10]-1000_0000)
            print ("Current edge", cedge[0]-1000_0000, cedge[1]-1000_0000, "in Surf", cedge[3]-1000_0000)
            print ("Current Ref ", redge[0]-1000_0000, redge[1]-1000_0000, "in Surf", redge[3]-1000_0000)
            print ("Next Ref    ", nextref[0]-1000_0000, nextref[1]-1000_0000, "in Surf", nextref[3]-1000_0000 )
            # self.ImageEdge(bottomedges, file=Pattern.name+"-ERROR NEXT EDGE IN Lateral Groove", edge1=[cedge], edge2=[redge], edge3=[nextref], dpi=1000, nid=1, tsize=0.5, eid=1)
            sys.exit()

        tpn =[]
        tn = int(groovebottom[tsurf][2])
        for i in range(7, 7+tn): 
            if groovebottom[tsurf][i] == com_node[0] or groovebottom[tsurf][i] == com_node[1] : 
                tpn.append(i)
        
        if tn == 4: 
            if tpn[0] == 7 and tpn[1] == 10: 
                tpn = [10, 7]
        else: 
            if tpn[0] == 7 and tpn[1] == 9: 
                tpn = [9, 7]
        
        idx = np.where(self.npn[:, 0] == tsf[tpn[0]])[0][0]
        N1 = self.npn[idx]
        idx = np.where(self.npn[:, 0] == tsf[tpn[1]])[0][0]
        N2 = self.npn[idx]

        nextedge = [groovebottom[tsurf][tpn[0]], groovebottom[tsurf][tpn[1]], 1, groovebottom[tsurf][0], N1[1], N1[2], N1[3], N2[1], N2[2], N2[3], 0]
        
        return nextedge, nextref
    def MergeBoundariesForMainGrooveSearching(self, medge, edges): 
        ## edges should be sorted 
        ## the first node in the 1st edge is the lowest node in the main groove(mEdge) 
        ## medge : main groove edge, edges : sub groove edges, it can be multiple

        ## calculate the center of each sub groove 
        x = int(self.GlobalXY/10); y = int(self.GlobalXY%10)

        CX=[]
        for edge in edges:
            sx = 0
            counting = 0 
            for mem in edge:
                sx += mem[x+3]
                counting +=1
            CX.append(sx/float(counting))

        MX = medge[0][x+3]
        MX1 = medge[0][x+6]
        
        Left =[]
        Right = []
        Rmin = CX[0]
        Lmax = CX[0]
        for i, cx in enumerate(CX): 
            if MX-cx > 0: 
                Left.append(i)
                if Lmax < cx: Lmax = cx
            elif MX1-cx < 0: 
                Right.append(i)
                if Rmin > cx: Rmin = cx 
            else: print ("ERROR!! Sub Groove is too close to Main groove")

        if len(Left)>0: 
            iedges =[]
            counting = 0
            for edge in medge:
                if edge[x+3] > Lmax and edge[x+6] > Lmax: 
                    iedges.append(edge)
                    counting += 1
            medge = iedges
        
            for i in Left: 
                iedges=[]
                for edge in edges[i]: 
                    if edge[x+3] > Lmax and edge[x+6] > Lmax: 
                        iedges.append(edge)
                iedges = np.array(iedges)
                if len(iedges)>0:    medge = np.concatenate((medge, iedges), axis=0)


        if len(Right) > 0:         
            iedges =[]
            for edge in medge:
                if edge[x+3] < Rmin and edge[x+6] < Rmin: 
                    iedges.append(edge)
            medge = np.array(iedges)

            for i in Right: 
                iedges=[]
                for edge in edges[i]: 
                    if edge[x+3] < Rmin and edge[x+6] < Rmin: 
                        iedges.append(edge)
                iedges = np.array(iedges)
                if len(iedges)> 0:  medge = np.concatenate((medge, iedges), axis=0)


        iedges=[]

        current = medge[0]
        startnode = medge[0][0]
        iedges.append(current)
        i=0
        while current[1] != startnode:

            idx = NextEdge(current, medge)
            if idx >=0: 
                current = medge[idx]
                current[10] = i+1 
            else:
                mdist = 1.0E15
                for edge in medge: 
                    already = 0
                    for ied in iedges: 
                        if edge[0] == ied[0] or edge[1] == ied[0]: 
                            already =1
                            break
                    if already ==1: continue 

                    dist = (edge[4] - current[7])*(edge[4] - current[7]) + (edge[5] - current[8])*(edge[5] - current[8]) + (edge[6] - current[9])*(edge[6] - current[9])

                    if dist < mdist: 
                        mdist = dist 
                        tedge = [current[1], edge[0], 1, current[3], current[7], current[8], current[9], edge[4], edge[5], edge[6], i+1]
                        # print ("dist %.3f (%d, %d : %d, %d)"%(dist*1000, int(current[0]-10000000), int(current[1]-10000000), int(edge[0]-10000000), int(edge[1]-10000000)))

                print ("* Main Groove Searching (merging edges) \n Edge (%d-%d) is connected width (%d-%d)"%(current[0], current[1], tedge[0], tedge[1]))
                current = tedge 

            iedges.append(current)
            
            i+=1
            if i > 100_000: 
                print ("Too many iteration for searching edges when merging edges")
                break 

        medge = np.array(iedges)
        return medge 


##########################################################################################
# End of PATTERN CLASS    
##########################################################################################
def SearchConnectedElement(element, ELEMENT): 
    elem = ELEMENT
    ns = []
    ns.append(element[1])
    ns.append(element[2])
    if element[6] == 3:   ns.append(element[3])
    elif element[6] == 4: 
        ns.append(element[3])
        ns.append(element[4])

    el = []
    for e in elem.Element: 
        cnt = 0 
        for i in range(1, e[6]+1):
            for n in ns: 
                if e[i] == n: cnt += 1
            if cnt == 2 and e[0] != element[0]: 
                el.append(e)
    i = 0
    while i < len(el): 
        j = i+1
        while j < len(el): 
            if el[i][0] == el[j][0]: 
                del(el[j])
                j -= 1
            j += 1
        i += 1 

    return el
def Circle_Center_with_2_nodes_radius(r, n1, n2, xy=23): 
    x = int(xy/10)
    y = int(xy%10)

    s1=n1[x]; s2=n1[y]
    e1=n2[x]; e2=n2[y]

    if round(e1, 10) == round(s1, 10) and round(e2, 10) == round(s2, 10): 
        c1=[0, n1[1], n1[2], n1[3]]
        c2=[0, n2[1], n2[2], n2[3]]
        centers=[c1, c2]
        if r ==0 : 
            print ("## warning!! To find the center of a circle. The 2 points are the same position.")
            return centers 
        else: 
            print ("## Error!! To find the center of a circle. The 2 points are the same position.")
            print ("   start %7.3f, %7.3f, %7.3f"%(n1[1]*1000, n1[2]*1000, n1[3]*1000))
            print ("    End  %7.3f, %7.3f, %7.3f"%(n2[1]*1000, n2[2]*1000, n2[3]*1000))
            print ("  Radius=%7.3f"%(r))
            return centers
    
    if e2 == s2 : 
        c1=[0, 0.0, 0.0, 0.0]
        c2=[0, 0.0, 0.0, 0.0]
        c2[x] = c1[x] = (e1+e2)/2.0 
        d = abs(s1 - e1)/2.0 
        angle = asin(d/r)
        c1[y] = e2 + r * cos(angle) 
        c2[y] = e2 - r * cos(angle) 
        centers=[c1, c2]
        return centers


    #########################################################################################
    ## normal line to the line (n1~n2) : y - m2 = A (x - m1), where mid point (m1, m2)
    ##     where mid point m(m1, m2),              A = - (n2x - n1x) / (n2y - n1y)
    m1 = (e1+s1)/2.0; m2 = (e2+s2)/2.0
    A = - (e1-s1) / (e2-s2)
    B = -m1 * A + m2 
    # print ("y = %7.3f * (x-%7.3f) + %7.3f = %7.3f*x + %7.3f"%(A, m1, m2, A, B))
    # print ("mid point =(%.3f, %.3f)"%(m1, m2))
    #########################################################################################

    #########################################################################################
    ## triangle [center, n1, m] 
    ## distance h = [n1, m], angle = (n1,center,m)
    ## distance m to center = r * cos(angle) 
    h= sqrt((m1-s1)**2 + (m2-s2)**2)
    try: 
        angle = asin(h/r)
    except: 
        print ("## Distance from N1 to N2 = %.8E, radius=%.8E"%(h*2, r))
        print ("## Error!! To find the center of a circle. Radius is too small.")
        sys.exit()
    dist_c_m = r * cos(angle)
    # print ("distance m~n1=%.3f, angle=%.1f, distance center~m=%.3f"%(h, degrees(angle), dist_c_m))
    #########################################################################################

    #########################################################################################
    ## we can make a circle whose center is m and radius is r*cos(a) : (x-m1)**2 + (y-m2)**2 = (distance m ~ center)**2
    ## this circle meets the normal line (y = Ax + B ) : (1+A**2) * x**2 + 2*( A*B - A*m2 - m1 )*x + m1**2 + (B-m2)**2 - h**2 = 0 
    ##  O = 1 + A**2, S = ( A*B - A*m2 - m1 ), T =  m1**2 + (B-m2)**2 - dist_c_m**2
    ## x = (-S + sqrt(S - O*T)) / O or (-S - sqrt(S - O*T)) / O 

    O = 1 + A**2
    S = A * B - A * m2 - m1 
    T = m1**2 + (B - m2)**2 - dist_c_m**2 

    centers=[]
    center1=[0, 0.0, 0.0, 0.0]
    center2=[0, 0.0, 0.0, 0.0]

    c1 = (-S + sqrt(S**2 - O*T)) / O   ## x 
    c2 = A * c1 + B             ## y 
    # print ("O=%.3f, S=%.3f, T=%.3f, A=%.3f"%(O, S, T, A))
    # print ("-S/O = %.3f, sqrt(S^2 - O*T)/O = %.3f"%(-S/O, sqrt(S**2 - O*T)/O))
    

    center1[x] = c1 
    center1[y] = c2 
    centers.append(center1)

    c1 = (-S - sqrt(S**2 - O*T)) / O   ## x 
    c2 = A * c1 + B            ## y 
    center2[x] = c1 
    center2[y] = c2 
    
    centers.append(center2)

    return centers 

def Jacobian_check(nodes, solids): 
    ## cannot check horizental/vertical plane 
    print ("\n******************************************")
    cnt = 0; jnt = 0; negleng=0; countshow = 2
    Jmin = 0.005
    hmg = 0.45E-03 
    show = 0
    errel=[]
    Jacs = []
    Length8=[]
    Length6=[]
    for sd in solids: 
        if sd[8] > 0: 
            ix = np.where(nodes[:,0]==sd[1])[0][0]; n1 = [nodes[ix][0], nodes[ix][1]*1000, nodes[ix][2]*1000, nodes[ix][3]*1000]
            ix = np.where(nodes[:,0]==sd[2])[0][0]; n2 = [nodes[ix][0], nodes[ix][1]*1000, nodes[ix][2]*1000, nodes[ix][3]*1000]
            ix = np.where(nodes[:,0]==sd[3])[0][0]; n3 = [nodes[ix][0], nodes[ix][1]*1000, nodes[ix][2]*1000, nodes[ix][3]*1000]
            ix = np.where(nodes[:,0]==sd[4])[0][0]; n4 = [nodes[ix][0], nodes[ix][1]*1000, nodes[ix][2]*1000, nodes[ix][3]*1000]
            ix = np.where(nodes[:,0]==sd[5])[0][0]; n5 = [nodes[ix][0], nodes[ix][1]*1000, nodes[ix][2]*1000, nodes[ix][3]*1000]
            ix = np.where(nodes[:,0]==sd[6])[0][0]; n6 = [nodes[ix][0], nodes[ix][1]*1000, nodes[ix][2]*1000, nodes[ix][3]*1000]
            ix = np.where(nodes[:,0]==sd[7])[0][0]; n7 = [nodes[ix][0], nodes[ix][1]*1000, nodes[ix][2]*1000, nodes[ix][3]*1000]
            ix = np.where(nodes[:,0]==sd[8])[0][0]; n8 = [nodes[ix][0], nodes[ix][1]*1000, nodes[ix][2]*1000, nodes[ix][3]*1000]

            l1 = sqrt( (n1[1]-n2[1])**2 +   (n1[2]-n2[2])**2 + (n1[3]-n2[3])**2 )
            l2 = sqrt( (n2[1]-n3[1])**2 +   (n2[2]-n3[2])**2 + (n2[3]-n3[3])**2 )
            l3 = sqrt( (n3[1]-n4[1])**2 +   (n3[2]-n4[2])**2 + (n3[3]-n4[3])**2 )
            l4 = sqrt( (n4[1]-n1[1])**2 +   (n4[2]-n1[2])**2 + (n4[3]-n1[3])**2 )
            l5 = sqrt( (n5[1]-n6[1])**2 +   (n5[2]-n6[2])**2 + (n5[3]-n6[3])**2 )
            l6 = sqrt( (n6[1]-n7[1])**2 +   (n6[2]-n7[2])**2 + (n6[3]-n7[3])**2 )
            l7 = sqrt( (n7[1]-n8[1])**2 +   (n7[2]-n8[2])**2 + (n7[3]-n8[3])**2 )
            l8 = sqrt( (n8[1]-n5[1])**2 +   (n8[2]-n5[2])**2 + (n8[3]-n5[3])**2 )

            h1 = sqrt( (n1[1]-n5[1])**2 +   (n1[2]-n5[2])**2 + (n1[3]-n5[3])**2 )
            h2 = sqrt( (n2[1]-n6[1])**2 +   (n2[2]-n6[2])**2 + (n2[3]-n6[3])**2 )
            h3 = sqrt( (n3[1]-n7[1])**2 +   (n3[2]-n7[2])**2 + (n3[3]-n7[3])**2 )
            h4 = sqrt( (n4[1]-n8[1])**2 +   (n4[2]-n8[2])**2 + (n4[3]-n8[3])**2 )
            Length8.append([l1, l2, l3, l4, l5, l6, l7, l8, h1, h2, h3,h4])
            d1, det = Point_Plane_Distance(n5, [n4, n1, n2])
            if det < 10**-13: print ("d1", det, sd)
            d2, det = Point_Plane_Distance(n6, [n1, n2, n4])
            if det < 10**-10: print ("d2", det, sd)
            d3, det = Point_Plane_Distance(n7, [n2, n3, n4])
            if det < 10**-10: print ("d3", det, sd)
            d4, det = Point_Plane_Distance(n8, [n3, n4, n1])
            if det < 10**-10: print ("d4", det, sd)

            if (d1 > 0 and d2 > 0 and d3 > 0 and d4 > 0)  or (d1 < 0 and d2 < 0 and d3 < 0 and d4 < 0) : 
                pass 
            else: 
                # cnt += 1 
                # print ("neg %d, 1=%.2f, %.2f, %.2f, %.2f"%(sd[0]-10**7, d1*1000, d2*1000, d3*1000, d4*1000))
                # errel.append(sd) 
                jnt += 1 
                negleng += 1 
                continue 

            if l1 < hmg  or l2 < hmg  or l3 < hmg  or l4 < hmg or h1 < hmg  or h2 < hmg  or h3 < hmg  or h4 < hmg or l5 < hmg  or l6 < hmg  or l7 < hmg  or l8 < hmg: 
                # print (" The bottom edge lengthes of the solid %4d are %7.3f, %7.3f, %7.3f, %7.3f"%(sd[0]-10**7, l1*1000, l2*1000, l3*1000, l4*1000))
                # print ("              The heights of the solid %4d are %7.3f, %7.3f, %7.3f, %7.3f"%(sd[0]-10**7, h1*1000, h2*1000, h3*1000, h4*1000))
                cnt += 1 
                # errel.append(sd)
                if show ==1 and cnt < countshow: ShowSolid(sd, nodes)

            J = Jacobian_Hexahedron(n4, n3, n2, n1, n8, n7, n6, n5, s=-1, t=1, u=-1)
            Jacs.append(J)
            if J < Jmin : 
                # print ("#1 Jacobian of Solid %5d is negative (%.3f)"%(sd[0]-10**7, J))
                
                jnt += 1
                # print ("%6d,%6d,%6d,%6d,%6d,%6d,%6d,%6d,%6d"%(sd[0]-10**7, sd[1]-10**7, sd[2]-10**7, sd[3]-10**7, sd[4]-10**7, sd[5]-10**7, sd[6]-10**7, sd[7]-10**7, sd[8]-10**7))
                if show ==1 and jnt <countshow: ShowSolid(sd, nodes)
                errel.append(sd)
                continue 
            J = Jacobian_Hexahedron(n4, n3, n2, n1, n8, n7, n6, n5, s=-1, t=-1, u=-1)
            Jacs.append(J)
            if J <Jmin: 
                # print ("#2 Jacobian of Solid %5d is negative (%.3f)"%(sd[0]-10**7, J))
                jnt += 1
                if show ==1 and jnt <countshow: ShowSolid(sd, nodes)
                errel.append(sd)
                continue 
            J = Jacobian_Hexahedron(n4, n3, n2, n1, n8, n7, n6, n5, s=1, t=-1, u=-1)
            Jacs.append(J)
            if J < Jmin: 
                # print ("#3 Jacobian of Solid %5d is negative (%.3f)"%(sd[0]-10**7, J))
                jnt += 1
                if show ==1 and jnt <countshow: ShowSolid(sd, nodes)
                errel.append(sd)
                continue 
            J = Jacobian_Hexahedron(n4, n3, n2, n1, n8, n7, n6, n5, s=1, t=1, u=-1)
            Jacs.append(J)
            if J < Jmin: 
                # print ("#4 Jacobian of Solid %5d is negative (%.3f)"%(sd[0]-10**7, J))
                jnt += 1
                if show ==1 and jnt <countshow: ShowSolid(sd, nodes)
                errel.append(sd)
                continue

            J = Jacobian_Hexahedron(n4, n3, n2, n1, n8, n7, n6, n5, s=1, t=-1, u=1)
            Jacs.append(J)
            if J < Jmin: 
                # print ("#4 Jacobian of Solid %5d is negative (%.3f)"%(sd[0]-10**7, J))
                jnt += 1
                if show ==1 and jnt <countshow: ShowSolid(sd, nodes)
                errel.append(sd)
                continue
            J = Jacobian_Hexahedron(n4, n3, n2, n1, n8, n7, n6, n5, s=1, t=1, u=1)
            Jacs.append(J)
            if J < Jmin: 
                # print ("#4 Jacobian of Solid %5d is negative (%.3f)"%(sd[0]-10**7, J))
                jnt += 1
                if show ==1 and jnt <countshow: ShowSolid(sd, nodes)
                errel.append(sd)
                continue
            J = Jacobian_Hexahedron(n4, n3, n2, n1, n8, n7, n6, n5, s=-1, t=1, u=1)
            Jacs.append(J)
            if J < Jmin: 
                # print ("#4 Jacobian of Solid %5d is negative (%.3f)"%(sd[0]-10**7, J))
                jnt += 1
                if show ==1 and jnt <countshow: ShowSolid(sd, nodes)
                errel.append(sd)
                continue
            J = Jacobian_Hexahedron(n4, n3, n2, n1, n8, n7, n6, n5, s=-1, t=-1, u=1)
            Jacs.append(J)
            if J < Jmin: 
                # print ("#4 Jacobian of Solid %5d is negative (%.3f)"%(sd[0]-10**7, J))
                jnt += 1
                if show ==1 and jnt <countshow: ShowSolid(sd, nodes)
                errel.append(sd)
                continue
        else: 
            # print ("%6d, %6d, %6d, %6d, %6d, %6d, %6d, %6d, %6d"%(sd[0]-10**7,sd[1]-10**7,sd[2]-10**7,sd[3]-10**7,sd[4]-10**7,sd[5]-10**7,sd[6]-10**7,sd[7],sd[8]))
            ix = np.where(nodes[:,0]==sd[1])[0][0]; n1 = [nodes[ix][0], nodes[ix][1]*1000, nodes[ix][2]*1000, nodes[ix][3]*1000]
            ix = np.where(nodes[:,0]==sd[2])[0][0]; n2 = [nodes[ix][0], nodes[ix][1]*1000, nodes[ix][2]*1000, nodes[ix][3]*1000]
            ix = np.where(nodes[:,0]==sd[3])[0][0]; n3 = [nodes[ix][0], nodes[ix][1]*1000, nodes[ix][2]*1000, nodes[ix][3]*1000]
            ix = np.where(nodes[:,0]==sd[4])[0][0]; n4 = [nodes[ix][0], nodes[ix][1]*1000, nodes[ix][2]*1000, nodes[ix][3]*1000]
            ix = np.where(nodes[:,0]==sd[5])[0][0]; n5 = [nodes[ix][0], nodes[ix][1]*1000, nodes[ix][2]*1000, nodes[ix][3]*1000]
            ix = np.where(nodes[:,0]==sd[6])[0][0]; n6 = [nodes[ix][0], nodes[ix][1]*1000, nodes[ix][2]*1000, nodes[ix][3]*1000]

            l1 = sqrt( (n1[1]-n2[1])**2 +   (n1[2]-n2[2])**2 + (n1[3]-n2[3])**2 )
            l2 = sqrt( (n2[1]-n3[1])**2 +   (n2[2]-n3[2])**2 + (n2[3]-n3[3])**2 )
            l3 = sqrt( (n1[1]-n3[1])**2 +   (n1[2]-n3[2])**2 + (n1[3]-n3[3])**2 )
            l4 = sqrt( (n4[1]-n5[1])**2 +   (n4[2]-n5[2])**2 + (n4[3]-n5[3])**2 )
            l5 = sqrt( (n5[1]-n6[1])**2 +   (n5[2]-n6[2])**2 + (n5[3]-n6[3])**2 )
            l6 = sqrt( (n6[1]-n4[1])**2 +   (n6[2]-n4[2])**2 + (n6[3]-n4[3])**2 )

            h1 = sqrt( (n1[1]-n4[1])**2 +   (n1[2]-n4[2])**2 + (n1[3]-n4[3])**2 )
            h2 = sqrt( (n2[1]-n5[1])**2 +   (n2[2]-n5[2])**2 + (n2[3]-n5[3])**2 )
            h3 = sqrt( (n3[1]-n6[1])**2 +   (n3[2]-n6[2])**2 + (n3[3]-n6[3])**2 )
            Length6.append([l1, l2, l3, l4, l5, l6, h1, h2, h3])
            d1, det = Point_Plane_Distance(n4, [n3, n1, n2])
            d2, det = Point_Plane_Distance(n5, [n1, n2, n3])
            d3, det = Point_Plane_Distance(n6, [n2, n3, n1])

            if (d1 > 0 and d2 > 0 and d3 > 0)  or (d1 < 0 and d2 < 0 and d3 < 0) : 
                pass 
            else: 
                # print ("neg length", sd)
                # errel.append(sd) 
                jnt += 1 
                negleng += 1 
                continue 

            if l1 < hmg  or l2 < hmg  or l3 < hmg or h1 < hmg  or h2 < hmg  or h3 < hmg or l4 < hmg  or l5 < hmg  or l6 < hmg: 
                print (" The edge lengthes of the tri-angule (solid %4d) are %7.3f, %7.3f, %7.3f"%(sd[0]-10**7, l1*1000, l2*1000, l3*1000))
                print ("       The heights of the tri-angule (solid %4d) are %7.3f, %7.3f, %7.3f"%(sd[0]-10**7, h1*1000, h2*1000, h3*1000))
                cnt += 1
                errel.append(sd)

    text =  "** Negative Jacobian(< %.3f): %d / %d \n"%(Jmin, len(errel), len(solids))
    text += "** Small length Element(< %.2fmm) : %d"%(hmg*1000, cnt)
    print (text)

    Jacs = np.array(Jacs)
    min_jac = np.min(Jacs)
    
    Len = np.array(Length8).reshape(-1)
    if len(Length6) > 0: 
        Len6 = np.array(Length6).reshape(-1)
        Len = np.concatenate((Len, Len6), axis=None)

    MinLen = np.min(Len) 
    print ("  Minimum J=%.2E, L=%.2fmm"%(min_jac, MinLen))
    print ("******************************************\n")
    return errel, text, negleng, cnt  
def Jacobian_Hexahedron(n1, n2, n3, n4, n5, n6, n7, n8, s=1, t=1, u=-1) : 

    N1s = -(1+t)*(1-u)/8;    N2s = -(1-t)*(1-u)/8;   N3s = (1-t)*(1-u)/8;     N4s = (1+t)*(1-u)/8
    N5s = -(1+t)*(1+u)/8;    N6s = -(1-t)*(1+u)/8;   N7s = (1-t)*(1+u)/8;     N8s = (1+t)*(1+u)/8

    Ns = [N1s, N2s, N3s, N4s, N5s, N6s, N7s, N8s]
    X = [n1[1], n2[1], n3[1], n4[1], n5[1], n6[1], n7[1], n8[1]]

    N1t =  (1-s)*(1-u)/8;    N2t = -(1-s)*(1-u)/8;    N3t = -(1+s)*(1-u)/8; N4t = (1+s)*(1-u)/8 
    N5t =  (1-s)*(1+u)/8;    N6t = -(1-s)*(1+u)/8;    N7t = -(1+s)*(1+u)/8; N8t = (1+s)*(1+u)/8 
    Nt = [N1t, N2t, N3t, N4t, N5t, N6t, N7t, N8t]
    Y = [n1[2], n2[2], n3[2], n4[2], n5[2], n6[2], n7[2], n8[2]]

    N1u = (1-s)*(1+t)/8;   N2u = (1-s)*(1-t)/8;    N3u = (1+s)*(1-t)/8; N4u = (1+s)*(1+t)/8
    N5u = -N1u;            N6u = -N2u;             N7u = -N3u;          N8u = -N4u 
    Nu = [N1u, N2u, N3u, N4u, N5u, N6u, N7u, N8u] 
    Z = [n1[3], n2[3], n3[3], n4[3], n5[3], n6[3], n7[3], n8[3]]

    Xs = 0
    for ns, x in zip(Ns, X): 
        Xs += ns*x 
    Ys = 0
    for ns, y in zip(Ns, Y): 
        Ys += ns*y
    Zs = 0
    for ns, z in zip(Ns, Z): 
        Zs += ns*z

    Xt = 0
    for nt, x in zip(Nt, X): 
        Xt += nt*x 
    Yt = 0
    for nt, y in zip(Nt, Y): 
        Yt += nt*y
    Zt = 0
    for nt, z in zip(Nt, Z): 
        Zt += nt*z

    Xu = 0
    for nu, x in zip(Nu, X): 
        Xu += nu*x 
    Yu = 0
    for nu, y in zip(Nu, Y): 
        Yu += nu*y
    Zu = 0
    for nu, z in zip(Nu, Z): 
        Zu += nu*z

    J = np.array([[Xs, Ys, Zs], [Xt, Yt, Zt], [Xu, Yu, Zu]])

    Det = np.linalg.det(J)

    return Det 
def Generate_all_surfaces_on_solid(npn, nps, diameter=0, text=""):  ##  --> GenerateAllSurfaces(self) 
    ## before call this function, 'makenumpyarray()' should be called.

    Solid = []
    Surface=[]
    if diameter == 0: 
        zs = npn[:,3]
        diameter = np.max(zs) * 2 
    R = round(diameter / 2.0, 7)
    R1000 = R*1000
    changed = 0
    img = 0 
    topmargin = R - 0.5E-03
    topmax = 0
    btmmax = 0 
    truncation = 5
    layer = -1
    for solid in nps:

        # if solid[0]-10**7 == 928: 
        #     print ("%d, %d, %d, %d, %d, %d, %d, %d, %d"%(solid[0]-10**7, solid[1]-10**7, solid[2]-10**7, solid[3]-10**7, solid[4]-10**7, solid[5]-10**7, solid[6]-10**7,solid[7]-10**7, solid[8]-10**7))

        if solid[9] == 6: N=7     ## solid[9] == 6
        else: N=9                 ## solid[9] == 8
        nodes_coord = []
        sx = 0.0;   sy = 0.0;      sz = 0.0
        topnode = []
        for i in range(1, N):
            index = np.where(npn[:, 0] == solid[i])
            tx = npn[index[0][0]][1]; ty=npn[index[0][0]][2]; tz =npn[index[0][0]][3]
            sx += tx;                  sy += ty;                 sz += tz 

            # if round(tz, 7) == round(diameter/2.0, 7) : topnode.append(npn[index[0][0]][0])
            if abs(round(tz -R, truncation)) < 0.5E-3 : topnode.append(npn[index[0][0]][0])
            nodes_coord.append([tx,ty,tz])

        SolidCenter = [round(sx/solid[9], truncation), round(sy/solid[9], truncation), round(sz/solid[9], truncation)] 

        centers = []
        centers_surface=[]

        top = 0 
        gap = R*2 
        
        
        
        if N == 9: 
            i = 0; j=1; m=2; n=3
            ssx = round((nodes_coord[i][0] + nodes_coord[j][0] + nodes_coord[m][0] + nodes_coord[n][0])  / 4.0, truncation)
            ssy = round((nodes_coord[i][1] + nodes_coord[j][1] + nodes_coord[m][1] + nodes_coord[n][1])  / 4.0, truncation)
            ssz = round((nodes_coord[i][2] + nodes_coord[j][2] + nodes_coord[m][2] + nodes_coord[n][2])  / 4.0, truncation)
            centers.append([ssx, ssy, ssz, 1])
            if ssz >= topmargin and R-ssz < gap : 
                top =1 
                gap = R-ssz 

            i = 4; j=5; m=6; n=7
            ssx = round((nodes_coord[i][0] + nodes_coord[j][0] + nodes_coord[m][0] + nodes_coord[n][0])  / 4.0, truncation)
            ssy = round((nodes_coord[i][1] + nodes_coord[j][1] + nodes_coord[m][1] + nodes_coord[n][1])  / 4.0, truncation)
            ssz = round((nodes_coord[i][2] + nodes_coord[j][2] + nodes_coord[m][2] + nodes_coord[n][2])  / 4.0, truncation) 
            centers.append([ssx, ssy, ssz, 2])
            if ssz >= topmargin and R-ssz < gap : 
                top =2 
                gap = R-ssz 

            i = 0; j=1; m=5; n=4
            ssx = round((nodes_coord[i][0] + nodes_coord[j][0] + nodes_coord[m][0] + nodes_coord[n][0])  / 4.0, truncation)
            ssy = round((nodes_coord[i][1] + nodes_coord[j][1] + nodes_coord[m][1] + nodes_coord[n][1])  / 4.0, truncation)
            ssz = round((nodes_coord[i][2] + nodes_coord[j][2] + nodes_coord[m][2] + nodes_coord[n][2])  / 4.0, truncation) 
            centers.append([ssx, ssy, ssz, 3])
            if ssz >= topmargin and R-ssz < gap : 
                top =3 
                gap = R-ssz 

            i = 1; j=2; m=6; n=5
            ssx = round((nodes_coord[i][0] + nodes_coord[j][0] + nodes_coord[m][0] + nodes_coord[n][0])  / 4.0, truncation)
            ssy = round((nodes_coord[i][1] + nodes_coord[j][1] + nodes_coord[m][1] + nodes_coord[n][1])  / 4.0, truncation)
            ssz = round((nodes_coord[i][2] + nodes_coord[j][2] + nodes_coord[m][2] + nodes_coord[n][2])  / 4.0, truncation) 
            centers.append([ssx, ssy, ssz, 4])
            if ssz >= topmargin and R-ssz < gap : 
                top =4 
                gap = R-ssz 

            i = 2; j=3; m=7; n=6
            ssx = round((nodes_coord[i][0] + nodes_coord[j][0] + nodes_coord[m][0] + nodes_coord[n][0])  / 4.0, truncation)
            ssy = round((nodes_coord[i][1] + nodes_coord[j][1] + nodes_coord[m][1] + nodes_coord[n][1])  / 4.0, truncation)
            ssz = round((nodes_coord[i][2] + nodes_coord[j][2] + nodes_coord[m][2] + nodes_coord[n][2])  / 4.0, truncation) 
            centers.append([ssx, ssy, ssz, 5])
            if ssz >=topmargin and R-ssz < gap : 
                top =5 
                gap = R-ssz 

            i = 3; j=0; m=4; n=7
            ssx = round((nodes_coord[i][0] + nodes_coord[j][0] + nodes_coord[m][0] + nodes_coord[n][0])  / 4.0, truncation)
            ssy = round((nodes_coord[i][1] + nodes_coord[j][1] + nodes_coord[m][1] + nodes_coord[n][1])  / 4.0, truncation)
            ssz = round((nodes_coord[i][2] + nodes_coord[j][2] + nodes_coord[m][2] + nodes_coord[n][2])  / 4.0, truncation) 
            centers.append([ssx, ssy, ssz, 6])
            if ssz >=topmargin and R-ssz < gap : 
                top =6 
                gap = R-ssz 
        else:
            i = 0; j=1; m=2
            ssx = round((nodes_coord[i][0] + nodes_coord[j][0] + nodes_coord[m][0] )  / 3.0, truncation)
            ssy = round((nodes_coord[i][1] + nodes_coord[j][1] + nodes_coord[m][1] )  / 3.0, truncation)
            ssz = round((nodes_coord[i][2] + nodes_coord[j][2] + nodes_coord[m][2] )  / 3.0, truncation) 
            centers.append([ssx, ssy, ssz, 1])
            if ssz >= topmargin and R-ssz < gap : 
                top =1 
                gap = R-ssz 

            i = 3; j=4; m=5
            ssx = round((nodes_coord[i][0] + nodes_coord[j][0] + nodes_coord[m][0] )  / 3.0, truncation)
            ssy = round((nodes_coord[i][1] + nodes_coord[j][1] + nodes_coord[m][1] )  / 3.0, truncation)
            ssz = round((nodes_coord[i][2] + nodes_coord[j][2] + nodes_coord[m][2] )  / 3.0, truncation) 
            centers.append([ssx, ssy, ssz, 2])
            if ssz >= topmargin and R-ssz < gap : 
                top =2
                gap = R-ssz 

            i = 0; j=1; m=4; n=3
            ssx = round((nodes_coord[i][0] + nodes_coord[j][0] + nodes_coord[m][0] + nodes_coord[n][0])  / 4.0, truncation)
            ssy = round((nodes_coord[i][1] + nodes_coord[j][1] + nodes_coord[m][1] + nodes_coord[n][1])  / 4.0, truncation)
            ssz = round((nodes_coord[i][2] + nodes_coord[j][2] + nodes_coord[m][2] + nodes_coord[n][2])  / 4.0, truncation) 
            centers.append([ssx, ssy, ssz, 3])
            if ssz >=topmargin and R-ssz < gap : 
                top =3 
                gap = R-ssz 

            i = 1; j=2; m=5; n=4
            ssx = round((nodes_coord[i][0] + nodes_coord[j][0] + nodes_coord[m][0] + nodes_coord[n][0])  / 4.0, truncation)
            ssy = round((nodes_coord[i][1] + nodes_coord[j][1] + nodes_coord[m][1] + nodes_coord[n][1])  / 4.0, truncation)
            ssz = round((nodes_coord[i][2] + nodes_coord[j][2] + nodes_coord[m][2] + nodes_coord[n][2])  / 4.0, truncation) 
            centers.append([ssx, ssy, ssz, 4])
            if ssz >=topmargin and R-ssz < gap : 
                top =4 
                gap = R-ssz  

            i = 2; j=0; m=3; n=5
            ssx = round((nodes_coord[i][0] + nodes_coord[j][0] + nodes_coord[m][0] + nodes_coord[n][0])  / 4.0, truncation)
            ssy = round((nodes_coord[i][1] + nodes_coord[j][1] + nodes_coord[m][1] + nodes_coord[n][1])  / 4.0, truncation)
            ssz = round((nodes_coord[i][2] + nodes_coord[j][2] + nodes_coord[m][2] + nodes_coord[n][2])  / 4.0, truncation) 
            centers.append([ssx, ssy, ssz, 5])
            if ssz >= topmargin and R-ssz < gap : 
                top =5 
                gap = R-ssz 
        # if top > 0: 
        #     print (" %d (N=%d) TOP Face=%d "%(solid[0]-10**7, N-1, top))
        #     if len(centers) ==6: 
        #         print ("%5.2f,%5.2f,%5.2f,%5.2f,%5.2f,%5.2f"%(R1000-centers[0][2]*1000,R1000-centers[1][2]*1000,R1000-centers[2][2]*1000,R1000-centers[3][2]*1000,R1000-centers[4][2]*1000,R1000-centers[5][2]*1000))
        #     else: 
        #         print ("%5.2f,%5.2f,%5.2f,%5.2f,%5.2f"%(R1000-centers[0][2]*1000,R1000-centers[1][2]*1000,R1000-centers[2][2]*1000,R1000-centers[3][2]*1000,R1000-centers[4][2]*1000))

        if top == 0 or N != 9: 
            cnt = 0
            mz = 100000.0
            my1  =centers[0][1]
            my2 = centers[0][1]
            for cz in centers: 
                if cz[1] > my2: my2 = cz[1]
                if cz[1] < my1: my1 = cz[1]
            # print ("*********")
            for i, cz in enumerate(centers): 
                # if solid[0]-10**7 == 260: 
                #     print ("%d, %f"%(i, cz[2]*1000))
                if cz[2] < mz: 
                    # if solid[0]-10**7 == 260:   print (" >> max...")
                    mz = cz[2]
                    if cz[1] > my1 and cz[1] < my2: cnt = i
        else : 
            if N==9 and top == 2 : cnt = 0 
            elif N==9 and top == 1 : cnt = 1

            elif N==9 and top == 3 : cnt = 4
            elif N==9 and top == 4 : cnt = 5
            elif N==9 and top == 5 : cnt = 2
            elif N==9 : cnt = 3

        if N ==9: 
            # print ("## ROTATION C3D8 %d"%(cnt), solid[0]-10000000, " \n ", solid[1]-10000000, solid[2]-10000000, solid[3]-10000000, solid[4]-10000000, solid[5]-10000000, solid[6]-10000000, solid[7]-10000000, solid[8]-10000000)
            if cnt == 0:   orders = [[0, 1, 4, 3, 2, 5, 8, 7, 6, 9] , [0, 1, 5, 4, 3, 2] ]  # [0, 1, 2, 3, 4, 5]  ## orders = [[el[0], N1[i]],   centers of faces ()]
            elif cnt == 1: orders = [[0, 6, 7, 8, 5, 2, 3, 4, 1, 9] , [1, 0, 3, 4, 5, 2] ]  # [[0,   6, 5, 8, 7,   2, 1, 4, 3, 9] , [1, 0,   2, 5, 4, 3] ]

            elif cnt == 2: orders = [[0, 1, 2, 6, 5, 4, 3, 7, 8, 9] , [2, 4, 0, 3, 1, 5] ]  # [[0,   1, 5, 6, 2,   4, 8, 7, 3, 9] , [2, 4,   5, 1, 3, 0] ]
            elif cnt == 3: orders = [[0, 2, 3, 7, 6, 1, 4, 8, 5, 9] , [3, 5, 0, 4, 1, 2] ]  # [[0,   2, 6, 7, 3,   1, 5, 8, 4, 9] , [3, 5,   2, 1, 4, 0] ]
            elif cnt == 4: orders = [[0, 4, 8, 7, 3, 1, 5, 6, 2, 9]  , [4, 2, 5, 1, 3, 0] ] # [[0,   4, 3, 7, 8,   1, 2, 6, 5, 9]  , [4, 2,   0, 3, 1, 5] ]
            elif cnt == 5: orders = [[0, 1, 5, 8, 4, 2, 6, 7, 3, 9] , [5, 3, 2, 1, 4, 0] ]  # [[0,   1, 4, 8, 5,   2, 3, 7, 6, 9] , [5, 3,   0, 4, 1, 2] ]
            else:  
                orders = [[0, 1, 4, 3, 2, 5, 8, 7, 6, 9] , [0, 1, 5, 4, 3, 2] ]
                print ("## ERROR no combination C3D8 ", solid[0]-10000000, " \n ", solid[1]-10000000, solid[2]-10000000, solid[3]-10000000, solid[4]-10000000, solid[5]-10000000, solid[6]-10000000, solid[7]-10000000, solid[8]-10000000)
                # errsolid = [solid]
                # text = "!! Error in solid construction %d"%(solid[0]-10**7)
        else: 
            if cnt == 0: orders =   [[0, 1, 3, 2, 4, 6, 5, 7, 8, 9] , [0, 1, 4, 3, 2] ]    # [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9] , [0, 1, 2, 3, 4] ]
            elif cnt == 1: orders = [[0, 4, 5, 6, 1, 2, 3, 7, 8, 9] , [1, 0, 2, 3, 4] ]    # [[0, 4, 6, 5, 1, 3, 2, 7, 8, 9] , [1, 0, 4, 3, 2] ]

            else: 
                orders =   [[0, 1, 3, 2, 4, 6, 5, 7, 8, 9] , [0, 1, 4, 3, 2] ] 
                print ("## Warning no combination C3D6 ", solid[0]-10000000, " \n ", solid[1]-10000000, solid[2]-10000000, solid[3]-10000000, solid[4]-10000000, solid[5]-10000000, solid[6]-10000000)
                errsolid =[solid]
                text = "!! Warning in solid construction %d"%(solid[0]-10**7)
                # return nps, Surface, text, errsolid 
                # sys.exit()

        # print ("...... ", cnt)
        tmp = []
        for i in orders[0]: 
            tmp.append(solid[i])

        tmp.append(SolidCenter[0])
        tmp.append(SolidCenter[1])
        tmp.append(SolidCenter[2])

        # print (tmp)
        # print (len(nodes_coord))
        
        for i in orders[0]: 
            if i ==9: break 
            else: 
                if N == 7 and i > 6: 
                        tmp.append(0.0);                tmp.append(0.0);                tmp.append(0.0)
                else: 
                    tmp.append(nodes_coord[i-1][0])
                    tmp.append(nodes_coord[i-1][1])
                    tmp.append(nodes_coord[i-1][2])

        # if solid[0]-10**7 == 260: 
        #     print (" cnt =", cnt )
        #     print ("%d, %d, %d, %d, %d, %d, %d, %d, %d"%(tmp[0]-10**7, tmp[1]-10**7, tmp[2]-10**7, tmp[3]-10**7, tmp[4]-10**7, tmp[5]-10**7, tmp[6]-10**7,tmp[7]-10**7, tmp[8]-10**7))
        # print (solid[0])
        
        margin = 0.15E-03
        pl =0 
        
        if N == 9: 
            # layer = -1
            Surface.append([tmp[0], 1, 4, layer, centers[orders[1][0]][0], centers[orders[1][0]][1], centers[orders[1][0]][2], tmp[1],tmp[2],tmp[3],tmp[4]])
            Surface.append([tmp[0],2, 4, layer, centers[orders[1][1]][0], centers[orders[1][1]][1], centers[orders[1][1]][2], tmp[5],tmp[6],tmp[7],tmp[8]])
            
            # layer = -1
            Surface.append([tmp[0],3, 4, layer, centers[orders[1][2]][0], centers[orders[1][2]][1], centers[orders[1][2]][2], tmp[1],tmp[2],tmp[6],tmp[5]])
            Surface.append([tmp[0],4, 4, layer, centers[orders[1][3]][0], centers[orders[1][3]][1], centers[orders[1][3]][2], tmp[2],tmp[3],tmp[7],tmp[6]])
            Surface.append([tmp[0],5, 4, layer, centers[orders[1][4]][0], centers[orders[1][4]][1], centers[orders[1][4]][2], tmp[3],tmp[4],tmp[8],tmp[7]])
            Surface.append([tmp[0],6, 4, layer, centers[orders[1][5]][0], centers[orders[1][5]][1], centers[orders[1][5]][2], tmp[4],tmp[1],tmp[5],tmp[8]])
        else: 
            # layer = -1
            Surface.append([tmp[0],1, 3, layer, centers[orders[1][0]][0], centers[orders[1][0]][1], centers[orders[1][0]][2], tmp[1],tmp[2],tmp[3], 0])
            Surface.append([tmp[0],2, 3, layer, centers[orders[1][1]][0], centers[orders[1][1]][1], centers[orders[1][1]][2], tmp[4],tmp[5],tmp[6],0 ])
            
            # layer = -1
            Surface.append([tmp[0],3, 4, layer, centers[orders[1][2]][0], centers[orders[1][2]][1], centers[orders[1][2]][2], tmp[1],tmp[2],tmp[5],tmp[4]])
            Surface.append([tmp[0],4, 4, layer, centers[orders[1][3]][0], centers[orders[1][3]][1], centers[orders[1][3]][2], tmp[2],tmp[3],tmp[6],tmp[5]])
            Surface.append([tmp[0],5, 4, layer, centers[orders[1][4]][0], centers[orders[1][4]][1], centers[orders[1][4]][2], tmp[3],tmp[1],tmp[4],tmp[6]])

        Solid.append(tmp)
        if cnt >0: 
            changed+=1

    del(centers)
    del(orders)
    nps = np.array(Solid, dtype=np.float64)
    Surface = np.array(Surface)
    text += "\n* The node order of PTN was checked(%dEA)\n"%(changed)
    errsolid = []
    return nps, Surface, text, errsolid
def Point_Plane_Distance(n, nodes): 
    n1 = nodes[0]; n2 = nodes[1]; n3 = nodes[2] 
    det = 1.0 

    vectors = [
        [n1[1], n1[2], n1[3]], 
        [n2[1], n2[2], n2[3]], 
        [n3[1], n3[2], n3[3]]
    ]

    vec = np.array(vectors)
    try: 
        rev = np.linalg.inv(vec) 
    except:
        vectors = [
            [n1[1], n1[2], n1[3]], 
            [n2[1], n2[2]+0.00001, n2[3]], 
            [n3[1], n3[2], n3[3]+0.00001]
        ]  ## change the node position when the plane is vertical or horizental. 

        vec = np.array(vectors)
        rev = np.linalg.inv(vec) 

    A = (rev[0][0] + rev[0][1] + rev[0][2]) 
    B = (rev[1][0] + rev[1][1] + rev[1][2]) 
    C = (rev[2][0] + rev[2][1] + rev[2][2]) 


    D = (A*n[1] + B*n[2] + C*n[3] -1) / sqrt(A*A + B*B + C*C)

    # if det < 10-10: print ("Distance =%e"%(D*1000))
        
    return D, det 


def NodeDistanceChecking(nodes, nps, margin=0.1E-03): 

    solidnode = nps[:,1:9]
    sn = np.unique(solidnode)
    if sn[0] == 0: 
        sn = np.delete(sn, 0)
    newnode=[]
    for n in sn: 
        id0 = np.where(nodes[:,0]==n)[0][0]
        newnode.append(nodes[id0])
    nodes = np.array(newnode)

    count =0 
    smalldist = []
    dists = []
    for n in sn:
        id0 = np.where(nodes[:,0]==n)[0][0]
        nd = nodes[id0]
        id1 = np.where(nodes[:,1] > nd[1] - margin)[0]
        id2 = np.where(nodes[:,1] < nd[1] + margin)[0]
        idx = np.intersect1d(id1, id2) 

        id1 = np.where(nodes[:,2] > nd[2] - margin)[0]
        id2 = np.where(nodes[:,2] < nd[2] + margin)[0]
        idy = np.intersect1d(id1, id2) 

        id1 = np.where(nodes[:,3] > nd[3] - margin)[0]
        id2 = np.where(nodes[:,3] < nd[3] + margin)[0]
        idz = np.intersect1d(id1, id2) 

        idy = np.where(nodes[:,2]==nd[2])[0]
        idz = np.where(nodes[:,3]==nd[3])[0]
        idn = np.intersect1d(idx, idy)
        idn = np.intersect1d(idn, idz)

        if len(idn) > 1: 
            clnd = [nd]
            tcounting = 0 
            for i in idn: 
                dn = nodes[i]
                if dn[0] != n: 
                    length = sqrt ((nd[1]-dn[1])**2 + (nd[2]-dn[2])**2 + (nd[3]-dn[3])**2) 
                    dists.append(length)
                    if length < margin: 
                        clnd.append([nodes[i], length])
                        tcounting += 1 
            if tcounting > 0: 
                count += 1 
                smalldist.append(clnd)
    if len(dists)>0: 
        dists = np.array(dists)
        md = np.min(dists)
        print ("* Mininum distance of pattern nodes %.2f"%(md*1000))
    return count, smalldist 

def SearchingNode(nid, npn, index=1): 
    ix = np.where(npn[:,0]==nid)[0]
    if len(ix) ==0: 
        print ("ERROR, NO NODE in Nodes %d"%(nid))
        return 0 
    else: 
        if index ==0: return npn[ix[0]]
        else:       return ix

def AllEdgesInSurface(surface, npn): 
    alledge =[]
    for sf in surface:
        idx = np.where(npn[:,0] == sf[7])
        N1 = npn[idx[0][0]] 
        idx = np.where(npn[:,0] == sf[8])
        N2 = npn[idx[0][0]] 
        idx = np.where(npn[:,0] == sf[9])
        N3 = npn[idx[0][0]] 
        alledge.append([int(sf[7]), int(sf[8]), int(sf[1]*10+1), sf[0], N1[1], N1[2], N1[3], N2[1], N2[2], N2[3], 0])
        alledge.append([int(sf[8]), int(sf[9]), int(sf[1]*10+2), sf[0], N2[1], N2[2], N2[3], N3[1], N3[2], N3[3], 0])
        if sf[2] == 3: alledge.append([int(sf[9]), int(sf[7]), int(sf[1]*10+3), sf[0], N3[1], N3[2], N3[3], N1[1], N1[2], N1[3], 0])
        else:
            idx = np.where(npn[:,0] == sf[10])
            N4 = npn[idx[0][0]] 
            alledge.append([int(sf[9]), int(sf[10]), int(sf[1]*10+3), sf[0], N3[1], N3[2], N3[3], N4[1], N4[2], N4[3], 0])
            alledge.append([int(sf[10]), int(sf[7]), int(sf[1]*10+4), sf[0], N4[1], N4[2], N4[3], N1[1], N1[2], N1[3], 0])

    return np.array(alledge)
def IsPointInPolygon(Point, PolygonPoints): 
    """
    Point = [a, b]
    PolygonPoints = [[x1, y1], [x2, y2], ... ]
    return True / False 
    

    check if the point is on the edge of the polygon
         xi <= a <= xj & y = (yj-yi)/(xj-xi) * (x-xi) + yi |x=a = b
      if function of the edge is y=b or x=a,
    """
    #####################################################################
    OutofPolygon = False
    OnLine = 0
    InPolygon = True
    counting = 0

    Point[0] = float(Point[0])
    Point[1] = float(Point[1])
    for i in range(len(PolygonPoints)):
        for j in range(len(PolygonPoints[i])):
            PolygonPoints[i][j] = float(PolygonPoints[i][j])

    for i in range(len(PolygonPoints)):
        if i != len(PolygonPoints) - 1:
            m = i
            n = i + 1
        else:
            m = i
            n = 0
        if PolygonPoints[m][0] == Point[0] and PolygonPoints[m][1] == Point[1]:
            return OnLine
        elif PolygonPoints[m][0] == PolygonPoints[n][0]:
            if PolygonPoints[m][0] == Point[0]:
                if PolygonPoints[m][1] > PolygonPoints[n][1] and Point[1] < PolygonPoints[m][1] and Point[1] > PolygonPoints[n][1]:
                    return OnLine
                elif PolygonPoints[m][1] < PolygonPoints[n][1] and Point[1] > PolygonPoints[m][1] and Point[1] < PolygonPoints[n][1]:
                    return OnLine
                else:
                    return OutofPolygon
        elif PolygonPoints[m][1] == PolygonPoints[n][1]:
            if PolygonPoints[m][1] == Point[1]:
                if PolygonPoints[m][0] > PolygonPoints[n][0] and Point[0] < PolygonPoints[m][0] and Point[0] > PolygonPoints[n][0]:
                    return OnLine
                elif PolygonPoints[m][0] < PolygonPoints[n][0] and Point[0] > PolygonPoints[m][0] and Point[0] < PolygonPoints[n][0]:
                    return OnLine
                else:
                    return OutofPolygon
            else:
                if PolygonPoints[m][0] > PolygonPoints[n][0] and Point[0] < PolygonPoints[m][0] and Point[0] > PolygonPoints[n][0] and Point[1] < PolygonPoints[m][1]:
                    # print 'c1'
                    counting += 1
                elif PolygonPoints[m][0] < PolygonPoints[n][0] and Point[0] < PolygonPoints[n][0] and Point[0] > PolygonPoints[m][0] and Point[1] < PolygonPoints[n][1]:
                    # print 'c2'
                    counting += 1
        else:
            y0 = (PolygonPoints[n][1] - PolygonPoints[m][1]) / (PolygonPoints[n][0] - PolygonPoints[m][0]) * (Point[0] - PolygonPoints[m][0]) + PolygonPoints[m][1]
            if y0 >= Point[1]:
                if PolygonPoints[m][0] > PolygonPoints[n][0]:
                    if Point[0] < PolygonPoints[m][0] and Point[0] > PolygonPoints[n][0]:
                        # print y0, Point[1]
                        if y0 == Point[1]:
                            return OnLine
                        counting += 1
                        if PolygonPoints[m][1] == y0:
                            counting -= 1
                if PolygonPoints[m][0] < PolygonPoints[n][0]:
                    if Point[0] > PolygonPoints[m][0] and Point[0] < PolygonPoints[n][0]:
                        # print y0, Point[1]
                        if y0 == Point[1]:
                            return OnLine
                        counting += 1
                        if PolygonPoints[m][1] == y0:
                            counting -= 1
    if counting % 2 == 0:
        return OutofPolygon   ## == False
    else:
        return InPolygon      ## == True
def NodeCoordinates(N, nodes): 
    index = np.where(nodes[:, 0] == N)
    return [N, nodes[index[0][0]][1], nodes[index[0][0]][2], nodes[index[0][0]][3]]
def DistanceFromLine3D(n0, nodes=[]):
    ## this function is not verified yet.... 

    U = [0, nodes[1][1]-nodes[0][1], nodes[1][2]-nodes[0][2], nodes[1][3]-nodes[0][3]]
    H = [0, n0[1]-nodes[0][1], n0[2]-nodes[0][2], n0-nodes[0][3]]

    UL = sqrt(U[1]**2+U[2]**2+U[3]**2)
    HL = sqrt(H[1]**2+H[2]**2+H[3]**2)

    crossProduct = sqrt( (U[2]*H[3] - U[3]*H[2])**2 + (H[3]*U[1]-H[1]*U[3])**2 + (H[1]*U[2]-U[1]*H[2])**2 ) 

    d =  crossProduct / UL 
    return d 

def DistanceFromLineToNode2D(N0, nodes=[], xy=12, onlydist=0):
    x = int(xy/10)
    y = int(xy%10)

    N1=nodes[0]
    N2=nodes[1]
    # shw = 0 
    # if round(N0[x], 4) > 140.0e-3: shw =1 
    N=[-1, 0, 0, 0]
    if round(N2[x]-N1[x], 8) and round(N2[y]-N1[y], 8): 
        A =  (N2[y]-N1[y])/(N2[x]-N1[x]) 
        cx = A / (A*A+1) *(N0[x]/A + N0[y] + A*N1[x] - N1[y])
        cy = A * (cx - N1[x]) + N1[y] 
        N[x] = cx
        N[y] = cy
        distance = sqrt((cx-N0[x])**2 + (cy-N0[y])**2)

        # if shw ==1:  print ("A=%.3f"%(A))
        # if shw == 1: print ("x2-x1=%.3f, y2-y1=%.3f"%((N2[x]-N1[x])*1000, (N2[y]-N1[y]) *1000 ))
        # if shw ==1:  print ("d=%.3f (%.3f, %.3f)"%(distance*1000, cx*1000, cy*1000))


        # a = (N2[y]-N1[y])/(N2[x]-N1[x])
        # A = -a
        # C = a * N1[x] - N1[y]

        # ## intersection position : N 
        # cx = (-a * (-a*N1[x] + N1[y]) +     (N0[x] + a * N0[y]) )/ (1 + a*a)
        # cy = (     (-a*N1[x] + N1[y]) + a * (N0[x] + a * N0[y]) )/ (1 + a*a)
        # N=[-1, 0, 0, 0]
        # N[x] = cx
        # N[y] = cy
        # distance = abs(A*N0[x]+N0[y]+C) / sqrt(A*A+1)
    elif round(N2[x]-N1[x], 8) and round(N2[y]-N1[y], 8) == 0: 
        distance = abs(N0[y] - N1[y])
        N[x] = N0[x]
        N[y] = N1[y]

    else: 
        distance = abs(N0[x] - N1[x])
        
        N[x] = N1[x]
        N[y] = N0[y]
    if onlydist ==1: 
        return distance
    else: 
        return distance, N 

def NormalPositionFromLineInPlane(position_ratio=10E10, n=[], ref_line=[],  xy=23): 
    x = int(xy/10); y = int(xy%10)
    line = ref_line 
    n1 = line[0]; n2=line[1]
    if (n2[x] != n1[x] and n2[y] != n1[y]) or  n2[x] == n1[x]: 
        if  n2[x] != n1[x] : 
            a = (n2[y]-n1[y])/(n2[x]-n1[x]) 
            na = - 1/a 
        else: 
            na = 0.0 
        dist, N = DistanceFromLineToNode2D(n, line, xy=xy)

        if position_ratio == 10E10:   # should be len(n) > 0 
            nDist=  Distance_2nodes(N, line[0])
            tDist = Distance_2nodes(line[1], line[0])
            position_ratio = nDist / tDist 
            if (line[0][x] - n[x]) *  (line[1][x] - n[x]) >= 0 and (line[0][x] - n[x]) <  (line[1][x] - n[x]): 
                position_ratio = -position_ratio

        cx = N[x]
        cy = N[y]

        M = -na * cx + cy 

        A = na*na +  1
        B = -cx + na * M - cy * na 
        C = cx*cx + M*M - 2*cy*M + cy*cy - dist*dist 
        tx1 = (-B + sqrt(B*B - A * C)) / A 
        tx2 = (-B - sqrt(B*B - A * C)) / A 

        if len(n) > 0: 
            if n[x] > N[x] : 
                tx = tx1 
            else: 
                tx = tx2 

            ty = na * tx + M 

            inter_point = [n[0], n[1], n[2], n[3]]
            inter_point[x] = tx 
            inter_point[y] = ty 

            return inter_point 
        else: 
            ty1 = na * tx1 + M 
            ty2 = na * tx2 + M 

            point1 = [0, 0.0, 0.0, 0.0]
            point2 = [0, 0.0, 0.0, 0.0]
            point1[x] = tx1 
            point1[y] = ty1
            point2[x] = tx2 
            point2[y] = ty2
            if (x == 1 and y == 2) or (x == 2 and y == 1) : z = 3 
            if (x == 2 and y == 3) or (x == 3 and y == 2) : z = 1 
            if (x == 3 and y == 1) or (x == 1 and y == 3) : z = 2
            point1[z]  = n[z]
            point2[z]  = n[z]

            return [point1, point2] 

    elif n2[y] == n1[y]: 

        if position_ratio == 10E10:   # should be len(n) > 0 
            cent = line[0]
            cent[x] = n[x] 

        dist = n[y] - cent[y]
        
        if len(n) > 0 : 
            point = cent 
            point[y] += dist 
        else: 
            point1 = cent 
            point2 = cent 

            point1[y] += dist 
            point2[y] -= dist 

            return [point1, point2]

def NodeDistance(N1, N2, xy=0): 
    if xy > 10: 
        x = int(xy/10); y=int(xy%10)
        return sqrt((N2[x] - N1[x])**2 + (N2[y] - N1[y])**2)
    else: 
        return sqrt((N2[1]-N1[1])*(N2[1]-N1[1]) + (N2[2]-N1[2])*(N2[2]-N1[2]) + (N2[3]-N1[3])*(N2[3]-N1[3]))
def Angle_Between_Vectors(va, vb):
    la = sqrt(va[1]*va[1] + va[2]*va[2] + va[3]*va[3])
    lb = sqrt(vb[1]*vb[1] + vb[2]*vb[2] + vb[3]*vb[3])
    cos = round((va[1]*vb[1]+va[2]*vb[2]+va[3]*vb[3]) / la/lb , 8)
    return round(acos(cos), 10)
def Angle_3nodes(n1=[], n2=[], n3=[], xy=0): ## n2 : mid node 
    
    v1 = [n1[1]-n2[1], n1[2]-n2[2], n1[3]-n2[3] ]
    v2 = [n3[1]-n2[1], n3[2]-n2[2], n3[3]-n2[3] ]
    
    if xy ==0: 
        cos = round((v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2]) /  sqrt(v1[0]**2 + v1[1]**2 + v1[2]**2) / sqrt(v2[0]**2 + v2[1]**2 + v2[2]**2), 9)
        angle = acos(cos)
    else: 
        x = int(xy/10)-1;     y = int(xy%10)-1
        L1 = sqrt(v1[x]**2 + v1[y]**2 ) 
        L2 = sqrt(v2[x]**2 + v2[y]**2)
        if L1 > 0 and L2 > 0: 
            cos = round((v1[x]*v2[x] + v1[y]*v2[y] ) /  L1 / L2, 9)
            angle = acos(cos)
        else: 
            print ("Error calculate angle")
            print (n1)
            print (n2)
            print (n3)

    return angle 
def Distance_2nodes(n1, n2, d2=0, xy=23): 
    if d2 == 0: 
        length = sqrt((n2[1]-n1[1])**2 + (n2[2]-n1[2])**2 + (n2[3]-n1[3])**2 )
    else: 
        x = int (xy/10)
        y = int (xy%10) 

        length = sqrt((n2[x]-n1[x])**2 + (n2[y]-n1[y])**2)

    return length 
def Change3DFace(Id):
    face=''
    if Id =='S1':
        face='S3'
    elif Id=='S2':
        face='S4'
    elif Id=='S3':
        face='S5'
    elif Id=='S4':
        face='S6'
    return face
def shallow_solid_node_search(solids, node, nodes): 
    ix8 = np.where(solids[:,9] == 8.0)[0]
    ix6 = np.where(solids[:,9] == 6.0)[0]
    # print ("** searching node : %d"%(node[0]-10**7))
    
    moving_nodes=[] 
    if len(ix8)>0: 
        SSolids = solids[ix8]
        ixs = np.where(SSolids[:,1:5] ==node[0])[0]
        if len(ixs)> 0: 
            solid = SSolids[ixs]
            # print ("   8 node solids, total=%d, searched=%d"%(len(SSolids), len(solid)), ixs)
            
            s = solid[0]
            # print ("   %6d, %6d, %6d, %6d, %6d, %6d, %6d, %6d, %6d"%(s[0]-10**7, s[1]-10**7, s[2]-10**7, s[3]-10**7, s[4]-10**7, s[5]-10**7, s[6]-10**7, s[7]-10**7, s[8]-10**7))
            num_col = 0 
            for i in range(1, 5): 
                if s[i] == node[0]: num_col = s[i + 4]

            while len(s) > 0: 
                column, s = UpSolid(s, SSolids)
                if len(column) > 0: 
                    for i in range(1, 5): 
                        if s[i] == num_col: 
                            moving_nodes.append(num_col)
                            num_col = s[i + 4]
                    # print ("   %6d, %6d, %6d, %6d, %6d, %6d, %6d, %6d, %6d"%(s[0]-10**7, s[1]-10**7, s[2]-10**7, s[3]-10**7, s[4]-10**7, s[5]-10**7, s[6]-10**7, s[7]-10**7, s[8]-10**7))
    
    elif len(ix6) > 0 : 
        SSolids = solids[ix6]
        ix = np.where(SSolids[:,1:4] == node[0])[0]
        if len(ix)> 0: 
            solid = SSolids[ix]
            # print ("   6 node solids, total=%d, searched=%d"%(len(SSolids), len(solid)))
            s = solid[0]    
            # print ("   %6d, %6d, %6d, %6d, %6d, %6d, %6d"%(s[0]-10**7, s[1]-10**7, s[2]-10**7, s[3]-10**7, s[4]-10**7, s[5]-10**7, s[6]-10**7))
            num_col = 0 
            for i in range(1, 4): 
                if s[i] == node[0]: num_col = s[i + 3]
            while len(s) > 0: 
                column, s = UpSolid(s, SSolids)
                if len(column) > 0: 
                    for i in range(1, 4): 
                        if s[i] == num_col: 
                            moving_nodes.append(num_col)
                            num_col = s[i + 3]
                    # print ("   %6d, %6d, %6d, %6d, %6d, %6d, %6d"%(s[0]-10**7, s[1]-10**7, s[2]-10**7, s[3]-10**7, s[4]-10**7, s[5]-10**7, s[6]-10**7))
    return moving_nodes
def UpSolid(solid, solids) : 
    nds = []
    if solid[9] == 6:
        ix1 = np.where(solids[:, 1:4]==solid[4])[0]
        ix2 = np.where(solids[:, 1:4]==solid[5])[0]
        ix3 = np.where(solids[:, 1:4]==solid[6])[0]

        ix = np.intersect1d(ix1, ix2)
        ix = np.intersect1d(ix, ix3)
        if len(ix) ==1: 
            if solid[4] == solids[ix[0]][1] or solid[4] == solids[ix[0]][2] or solid[4] == solids[ix[0]][3] : 
                nds.append([solids[ix[0]][1], solids[ix[0]][2], solids[ix[0]][3]])
                return nds, solids[ix[0]]
            else: 
                nds = []
                return nds, nds 
        elif len(ix) == 0: 
            nds = []
            return nds, nds  
        else: 
            print ("ERROR, Too many solids on the element!! (%dEA found)"%(len(ix)))
            print (" Elements found")
            txt =" "
            for x in ix: 
                txt += str(solids[x][0]) + ", "
            print (txt )
            sys.exit()
    
    else: 
        ix1 = np.where(solids[:, 1:5]==solid[5])[0]
        ix2 = np.where(solids[:, 1:5]==solid[6])[0]
        ix3 = np.where(solids[:, 1:5]==solid[7])[0]
        ix4 = np.where(solids[:, 1:5]==solid[8])[0]

        ix = np.intersect1d(ix1, ix2)
        ix = np.intersect1d(ix, ix3)
        ix = np.intersect1d(ix, ix4)
        if len(ix) ==1: 
            if solid[5] == solids[ix[0]][1] or solid[5] == solids[ix[0]][2] or solid[5] == solids[ix[0]][3] or solid[5] == solids[ix[0]][4]: 
                nds.append([solids[ix[0]][1], solids[ix[0]][2], solids[ix[0]][3], solids[ix[0]][4]])
                return nds, solids[ix[0]]
            else: 
                nds = []
                return nds, nds 
        elif len(ix) == 0: 
            nds = []
            return nds, nds 
        else: 
            print ("ERROR, Too many solids on the element!! (%dEA found)"%(len(ix)))
            print (" Elements found")
            txt =" "
            for x in ix: 
                txt += str(solids[x][0]) + ", "
            print (txt )
            sys.exit()
def Element2D_relatonship(el1, el2): 
    EN1=[]; EN2=[]
    for i, e1 in enumerate(el1): 
        if i == 0: continue 
        if e1 == 0 or i > 4: break
        for j, e2 in enumerate(el2): 
            if j ==0: continue 
            if e2 == 0  or j > 4: break 

            if e1 == e2: 
                EN1.append(i)
                EN2.append(j) 
    if len(EN1) == 0: 
        ## no contacting between 2 elements
        return "0", 0, 0
    elif len(EN1) == 1: 
        ## 1 node connecton
        return "N", EN1[0], EN2[0]
    elif len(EN1) == 2: 
        ## edge connection
        EN1 = sorted(EN1); EN2 = sorted(EN2)
        if el1[4] > 0: 
            if EN1[0] == 1 and EN1[1] == 2: f1 = 1 
            if EN1[0] == 2 and EN1[1] == 3: f1 = 2 
            if EN1[0] == 3 and EN1[1] == 4: f1 = 3 
            if EN1[0] == 1 and EN1[1] == 4: f1 = 4
        else: 
            if EN1[0] == 1 and EN1[1] == 2: f1 = 1 
            if EN1[0] == 2 and EN1[1] == 3: f1 = 2 
            if EN1[0] == 1 and EN1[1] == 3: f1 = 3 

        if el2[4] > 0: 
            if EN2[0] == 1 and EN2[1] == 2: f2 = 1 
            if EN2[0] == 2 and EN2[1] == 3: f2 = 2 
            if EN2[0] == 3 and EN2[1] == 4: f2 = 3 
            if EN2[0] == 1 and EN2[1] == 4: f2 = 4
        else: 
            if EN2[0] == 1 and EN2[1] == 2: f2 = 1 
            if EN2[0] == 2 and EN2[1] == 3: f2 = 2 
            if EN2[0] == 1 and EN2[1] == 3: f2 = 3 
            
        return "E", f1, f2 
    else: 
        print ("## Error!!!, more than 2 nodes are shared in 2-D elements")
        print ("## ", el1)
        print ("## ", el2)
        print ("## Shared Nodes : ", EN1, EN2)
        return "X", 0, 0
def Scaled_node_GaugeCheck(origin, scaled, mgd, tgd): 

    MR = np.max(origin[:,3])
    SR = np.max(scaled[:,3])
    if mgd > 50.0E-3: 
        mgd = mgd/1000
    ratio = round(tgd / mgd, 5)
    cnt = 0 
    for i, nd in enumerate(scaled): 
        ix = np.where(origin[:,0] == nd[0])[0][0]
        sc = origin[ix]
        mg = MR - sc[3]
        sg = SR - nd[3]
        if mg > 1.5E-03: 
            if round(sg / mg, 5) != ratio : 
                scaled[i][3] = SR - ratio * mg 
                cnt += 1 
    text = "## Virtical position of %d nodes were repositioned. ################### "%(cnt); print (text)
    text = "## Model Groove Depth = %.2f, Scaled Groove Depth = %.2f (ratio=%.2f)"%(mgd*1000, tgd*1000, ratio); print (text)
    
    return scaled 
def Pattern_Node_DistanceCheck(npn, solid, mg=0.1E-03): 
    # text = "#############################################################";  print (text)
    # text = "## START TO CHECK NODE DISTANCE OF PATTERN"; print (text)
    # text = "#############################################################";  print (text)

    ids = []
    for sd in solid: 
        for i in range(1,9): 
            if sd[i] > 0: 
                ids.append(sd[i])
    ids = np.array(ids)
    ids = np.unique(ids)
    nodes=[]
    for d in ids: 
        ix = np.where(npn[:,0]==d)[0][0]
        nodes.append(npn[ix])
    nodes = np.array(nodes)

    for nd in nodes:
        ix1 = np.where(nodes[:,1] > nd[1]-mg)[0]
        ix2 = np.where(nodes[:,1] < nd[1]+mg)[0]
        ix = np.intersect1d(ix1, ix2)

        iy1 = np.where(nodes[:,2] > nd[2]-mg)[0]
        iy2 = np.where(nodes[:,2] < nd[2]+mg)[0]
        iy = np.intersect1d(iy1, iy2)

        iz1 = np.where(nodes[:,3] > nd[3]-mg)[0]
        iz2 = np.where(nodes[:,3] < nd[3]+mg)[0]
        iz = np.intersect1d(iz1, iz2)

        idx = np.intersect1d(ix, iy)
        idx = np.intersect1d(idx, iz)

        if len(idx) > 1: 
            for ix in idx: 
                if nodes[ix][0] != nd[0]: 
                    length = sqrt((nd[1]-nodes[ix][1])**2 + (nd[1]-nodes[ix][1])**2 + (nd[1]-nodes[ix][1])**2 )

                    if length <= 0.1E-3 : 
                        text = "## The nodes are too close. Distance=%.3fmm"%(length*1000); print(text)
                        text = "## %d:%d,   x=%.3f:%.3f,   y=%.3f:%.3f,   z=%.3f:%.3f"%(nd[0]-10**7, nodes[ix][0]-10**7, nd[1]*1000, nodes[ix][1]*1000, nd[2]*1000, nodes[ix][2]*1000, nd[3]*1000, nodes[ix][3]*1000); print(text)
def RotateNode(n=[], angle=0.0, center=[0, 0.0, 0.0, 0.0], xy=23): 
    x = int(xy/10); y=int(xy%10)
    v = [0, n[1]-center[1], n[2] - center[2], n[3]-center[3]]
    rx = cos(angle) * v[x] - sin(angle)*v[y]
    ry = sin(angle) * v[x] + cos(angle)*v[y]
    result = [n[0], n[1], n[2], n[3]]
    result[x] = rx + center[x]
    result[y] = ry + center[y]
    return result 
def NormalVector(n1, n2):
    x1 = n1[1]; y1 = n1[2]; z1 = n1[3]
    x2 = n2[1]; y2 = n2[2]; z2 = n2[3]

    vx = y1*z2 - z1*y2 
    vy = z1*x2 - x1*z2 
    vz = x1*y2 - y1*x2 
    norm = [0, vx, vy, vz]
    return norm 
def NormalVector_plane(n1, n2, n3): 
    a = [0, n1[1]-n2[1], n1[2]-n2[2], n1[3]-n2[3]]
    b = [0, n3[1]-n2[1], n3[2]-n2[2], n3[3]-n2[3]]

    II = a[2]*b[3] - a[3]*b[2]
    JJ = a[3]*b[1] - a[1]*b[3]
    KK = a[1]*b[2] - a[2]*b[1]

    return [0, II, JJ, KK]

def TiltShoulderNodes(angle=0.0, nodes=[], less=10000.0, more=10000.0, buffer=0, shoulder_radius=0): 
    R = np.max(nodes[:,3]) 
    Hpw = np.max(nodes[:,2])
    width = 5.0E-03 
    if buffer ==0: 
        if less < 1000 and more > 1000: 
            for i, nd in enumerate(nodes): 
                if nd[2] < -Hpw + width: 
                    rt = 0.1 * (1 - (nd[2] + Hpw)/width)
                    cn = [nd[0], nd[1], nd[2], R]
                    rd = RotateNode(nd, angle*(1.0 - rt), cn, xy=23)
                    nodes[i][2] = rd[2]
                    nodes[i][3] =  R - (R-nd[3]) * 0.9 
                    # print ("half pw=%.2f, angle=%.2f, ratio=%.3f,  x + hpw =%.1f"%(Hpw*1000, degrees( angle**(1.0 - rt)), rt, (nd[2]+Hpw)*1000))
                elif nd[2] < less - buffer and nd[3] < R: 
                    cn = [nd[0], nd[1], nd[2], R]
                    rd = RotateNode(nd, angle, cn, xy=23)
                    nodes[i][2] = rd[2]
                    nodes[i][3] = R - (R-nd[3]) * 0.9 
        elif more < 1000 and less > 1000: 

            for i, nd in enumerate(nodes): 
                if nd[2] > Hpw - width: 
                    rt = 0.1 * (1 - (Hpw - nd[2])/width)
                    cn = [nd[0], nd[1], nd[2], R]
                    rd = RotateNode(nd, angle*(1.0 - rt), cn, xy=23)
                    nodes[i][2] = rd[2]
                    nodes[i][3] =  R - (R-nd[3]) * 0.9 
                elif nd[2] > more and nd[3] < R: 
                    cn = [nd[0], nd[1], nd[2], R]
                    rd = RotateNode(nd, angle, cn, xy=23)
                    nodes[i][2] = rd[2]
                    nodes[i][3] =  R - (R-nd[3]) * 0.9 
    elif buffer > 1.0: 
        rw = buffer * 2.0
        print ("***************************************")
        print ("* Tilting angle after P point=%.2f"%(degrees(angle)))
        print ("***************************************")
        case = 1 
        if less < 1000 and more > 1000: 
            MinMargin = (less + buffer)
            for i, nd in enumerate(nodes): 
                # if case == 0: 
                    if nd[2] < MinMargin :
                        if shoulder_radius > 6.0E-03 : 
                            rangle, rate = angle_converting_for_pattern_shoulder_tilting(x=nd[2], minval=MinMargin, lrange=rw, ref_angle=angle, shoR=shoulder_radius, R=R, posY=nd[3])
                        elif shoulder_radius > 0: 
                            if nd[2] > less - buffer and nd[2] > less + buffer: 
                                rangle = (1 - (nd[2] - less - buffer )/rw ) * angle  ## anyway this formula works well. at radius 5 mm
                                rate = rangle / angle 
                            else: 
                                rangle = angle 
                                rate = 1.0
                        else: 
                            rangle = angle 
                            rate = 1.0

                        cn = [nd[0], nd[1], nd[2], R]
                        rn = RotateNode(nd, rangle, cn, xy=23)
                        nodes[i][2] = rn[2]
                        # text = "%.3f, %.3f, %.3f, %.3f, %.3f, %.3f\n"%(nd[2]*1000, degrees(rangle), shoulder_radius*1000, MinMargin*1000, rw*1000, rate)
                        # f.writelines(text)
                        # print (text)

                    continue 

        elif more < 1000 and less > 1000: 
            MinMargin = more - buffer 
            for i, nd in enumerate(nodes): 
                # if case == 0: 
                    if nd[2] > MinMargin : 
                        rangle, rate = angle_converting_for_pattern_shoulder_tilting(x=nd[2], minval=MinMargin, lrange=rw, ref_angle=angle, shoR=shoulder_radius, R=R, posY=nd[3])

                        cn = [nd[0], nd[1], nd[2], R]
                        rn = RotateNode(nd, rangle, cn, xy=23)
                        nodes[i][2] = rn[2]

                    continue 
    else: 
        start = abs(less)
        if more < 10000: start = abs(more)

        start -= buffer 
        lw = buffer * 2 

        s_gage = 0.9 * shoulder_radius 
        angle = abs(angle)

        print ("***************************************")
        print ("* Tilting angle after P point=%.2f"%(degrees(angle)))
        print ("***************************************")
        for i, nd in enumerate(nodes): 
            ylen = abs(nd[2])
            if ylen > start: 
                mlen = (ylen - start) / lw 
                
                if mlen < 1.0: 
                    mgage = (R - nd[3]) / s_gage  
                    if mgage > 1.0 : mgage = 1.0 
                else: 
                    mgage = 1.0

                if mlen > 1.0: mlen = 1.0 

                cn = [nd[0], nd[1], ylen, R]
                cnd = [nd[0], nd[1], ylen, nd[3]]
                rd = RotateNode(cnd,  angle * mlen * mgage / 2.0 , cn, xy=23)
                if mlen*mgage < 1.0: 
                    print ("%8.2f > %8.3f A=%.1f (lg=%.2f, gg=%.2f)"%(nd[2]*1000, rd[2]*1000, degrees(angle)*mlen*mgage, mlen, mgage))
                if nd[2] < 0.0 : nodes[i][2] = -rd[2] 
                else:            nodes[i][2] = rd[2] 
                # nodes[i][3] = R - (R-nd[3]) * (1-0.1 * mlen)
                nodes[i][3] = rd[3]

    return nodes 

def angle_converting_for_pattern_shoulder_tilting(x=0, minval=0, lrange=0, ref_angle=0, shoR=0, R=0, posY=0): 
    angle = 0.0  
    mul = 0.5
    x = abs(x); minval = abs(minval); lrange = abs(lrange)
    if x > minval: 
        length = x - minval
        rate = length / lrange 
    if rate > 1.0:    
        
        if shoR < 6.0E-03 : angle = ref_angle * 1.1
        else:               angle = ref_angle * 1.1
        
    else: 
        angle = ref_angle * (rate + (R-posY)/shoR*0.8 )  *mul   
    return angle, (rate + (R-posY)/shoR) 

def RepositionNodesAfterShoulder_old(shopoint=[], endpoint=[], ptn_tw=0.0, current_ptn_nodes=[], org_ptn_node=[]): 
    x = 2; y=3 
    nodes = current_ptn_nodes
    orgn = org_ptn_node 
    half_ptn_tw = ptn_tw / 2.0 
    ## positive
    pVector = [endpoint[x]-shopoint[y], endpoint[y]- shopoint[y]]
    ## negative 
    nVector = [-pVector[0], pVector[1]]  ## mirror vector 

    halfw = np.max(orgn[:,2])
    ptnR = np.max(orgn[:,3])
    L_model = halfw - half_ptn_tw / 2.0 
    L_profile = sqrt(pVector[0]**2 + pVector[1]**2)
    L_ratio = L_profile / L_model 
    
    ref_line = [shopoint, endpoint]

    for nd in orgn: 
        if abs(nd[2]) > half_ptn_tw and nd[3] < ptnR - 2.0E-03: 
            if nd[2] > 0.0:  vector = pVector 
            else:             vector = nVector 
            ix = np.where(nodes[:, 0] == nd[0])[0]
            if len(ix) > 0: 
                ix = ix[0]
            else: 
                continue 
            n = nodes[ix]

            dist, InterN = DistanceFromLineToNode2D(n, ref_line, xy=23)
            position_ratio = (halfw - abs(nd[2]))/L_model
            N = NormalPositionFromLineInPlane(position_ratio=position_ratio, ref_line=ref_line, n=n)

            nodes[ix][x] = N[x]
            # nodes[ix][y] = N[y]


    return nodes 

def Get_layout_treadbottom(flatten, allnodes): 
    nodes = []
    for nd in flatten: 
        ix = np.where(allnodes[:,0]==nd[0])[0][0]
        nodes.append(allnodes[ix])
    return np.array(nodes)

def ShiftShoulderNodesSquarePattern(npn, orn, profiles, curves, sideNodes, surf_posSide, surf_negSide, ptn_TDW, profile_TDW, ptn_sideBtmNode):

    ## delete side profiles 
    # for pf, cv in zip(profiles, curves):
    #     print (pf, cv)
    if profiles[-1][0] < 0: 
        del(profiles[-1])
        if len(curves) > len(profiles): 
            del(curves[-1])

    profiles[-1][1] -= 0.5
    profiles[-1][2] -= 0.5
    lastWidth = profiles[-1][1] 
    lastCurve = curves[-1] 


    lastAngle = 0.0
    vn = [sideNodes[0][0], sideNodes[0][1], sideNodes[0][2], sideNodes[0][3]-1.0]
    lastAngle = Angle_3nodes(vn, sideNodes[0], sideNodes[2], xy=23)
    if vn[2] > sideNodes[2][2]: lastAngle = -lastAngle
    ## ptn_sideBtmNode : side bottom node after bended, not attatched to profile 
    sideBendedAngle = Angle_3nodes(vn, sideNodes[0], ptn_sideBtmNode, xy=23)
    if vn[2] > ptn_sideBtmNode[2]: sideBendedAngle = -sideBendedAngle

    # print (" Profile Shoulder Angle =%.2f (bended =%.2f)"%(degrees(lastAngle), degrees(sideBendedAngle)))
    maxDelAngle = sideBendedAngle - lastAngle
    maxDelY = ptn_sideBtmNode[2] - sideNodes[2][2]
    maxDelZ = ptn_sideBtmNode[3] - sideNodes[2][3]

    # print ("max del y,", maxDelY*1000, "max del z, ", maxDelZ*1000)
    # print ("profile_TDW", profile_TDW*1000, "pattern tdw", ptn_TDW*1000)

    width = profile_TDW * 0.12 
    startAngle = 0
    if lastWidth > width: 
        n= [lastCurve[0][0], lastCurve[0][1], lastCurve[0][2], lastCurve[0][3]-1]
        aAngle = Angle_3nodes(n, lastCurve[0], lastCurve[2], xy=23)
        if n[2] > lastCurve[2][3]: aAngle *= -1 

        n= [lastCurve[1][0], lastCurve[1][1], lastCurve[1][2], lastCurve[1][3]-1]
        bAngle = Angle_3nodes(n, lastCurve[1], lastCurve[2], xy=23)
        if n[2] > lastCurve[2][3]: aAngle *= -1

        startAngle = aAngle*(1-width/lastWidth) + bAngle *(width/lastWidth)
    
    else: 
        n= [lastCurve[0][0], lastCurve[0][1], lastCurve[0][2], lastCurve[0][3]-1]
        startAngle = Angle_3nodes(n, lastCurve[0], lastCurve[2], xy=23)
        if n[2] > lastCurve[2][3]: startAngle *= -1 

    
    scaleRatio = profile_TDW / ptn_TDW 
    modelWidth = width / scaleRatio
    modelStart = ptn_TDW/2.0 - modelWidth
    modelEnd = np.max(orn[:,2])
    modelLength = modelEnd - modelStart 
    modelR = np.max(orn[:,3])
    ix = np.where(orn[:,0] == ptn_sideBtmNode[0])[0][0]
    modelEndGauge = modelR - orn[ix][3]

    # print ("model start=",modelStart , ", end,", modelEnd)
    # print("model end ga=", modelEndGauge)
    # print ("model length,", modelLength)

    idx1 = np.where(orn[:,2] > modelStart)[0]
    idx2 = np.where(orn[:,2] < -modelStart)[0]
    idx = np.concatenate((idx1, idx2), axis=0)
    nodes = orn[idx]
    # print ("NO : ", len(idx1), len(idx2), len(nodes))
    
    nds =[]
    for sf in surf_posSide:
        nds.append(sf[7]); nds.append(sf[8]); nds.append(sf[9]) 
        if sf[10] > 0: nds.append(sf[10])
    for sf in surf_negSide:
        nds.append(sf[7]); nds.append(sf[8]); nds.append(sf[9]) 
        if sf[10] > 0: nds.append(sf[10])
    nds=np.array(nds); nds=np.unique(nds)
    for n in nds:
        ix = np.where(nodes[:,0]==n)[0]
        if len(ix)>0:
            nodes = np.delete(nodes, ix[0], axis=0)
    ## nodes : list of the nodes to reposition.

    # print (" the no of nodes to reposition %d"%(len(nodes)))
    # print (" Distance from TW =%.2f"%( modelWidth*1000))

    ## maxDelZ 
    cnt = 0 
    for nd in nodes:
        wd = abs(nd[2]) - modelStart 
        if nd[2] <0: wd = -wd 

        ix = np.where(orn[:,0]==nd[0])[0][0]; n=orn[ix]
        ix = np.where(npn[:,0]==nd[0])[0][0]
        # print ("Initial %d, %.5f, %.5f, "%(npn[ix][0], npn[ix][2], npn[ix][3] ), end="")
        npn[ix][2] -= maxDelY * (modelR - n[3]) / modelEndGauge * wd / modelLength 
        npn[ix][3] -= (modelR - n[3]) / modelEndGauge * maxDelZ * abs(wd)/modelLength 
        cnt += 1

        # print (" >>  %d, %.5f, %.5f "%(npn[ix][0], npn[ix][2], npn[ix][3] ))

        # ix0 = np.where(orn[:,0]==nd[0])[0][0]
        # if orn[ix0][0]  != npn[ix][0] : print (" node is different %d, %d"%(orn[ix0][0]-10**7,  npn[ix][0]-10**7))

    return npn 
    
def RepositionNodesAfterShoulder(pf_endings, ptn_gaged, surf_pos_side, surf_neg_side, ptn_npn, layout_TDW, profile, curves, Lcurves, ht_ratio=1.0, ptn_TDW=0.0,\
         btm_surf=[], ptn_R=0, ptn_orgn=[], bodynodes=[], bodybottom=[] ): 
    ## profile : right profile (positive profile)
    ## curves : curves of right profile 
    ## Lcurves : curves of left profile 
    # ptn_gaged : actually gaged pattern mesh 
    ## ShoR = 50mm 

    repo = 1
    start_angle = 0  
    start = 0
    PN = len(profile)

    ShoR = 0.05 
    for i, pf in enumerate(profile): 
        if i == PN-2: ## always the number of Deco. cuvres is 1.
            if pf[0] < ShoR: 
                repo = 1
                icurve = i 
                refn = [0, curves[icurve][0][1], curves[icurve][0][2], curves[icurve][0][3] - 1.0 ]
                start_angle = Angle_3nodes(refn, curves[icurve][0], curves[icurve][2], xy=23) #-radians(5)
                len_shocurve = pf[1]
                buffer = layout_TDW / 2.0 - start 
                break 
        if i == PN-1:  
            repo = 0
            buffer = 0.0 
            len_shocurve = 0.0 
            icurve = i 
            refn = [0, curves[icurve-1][1][1], curves[icurve-1][1][2], curves[icurve-1][1][3] - 1.0 ]
            start_angle = Angle_3nodes(refn, curves[icurve-1][1], curves[icurve-1][2], xy=23) #-radians(5)

            break 


        start += pf[1]

                


    deco_n = [] 
    max_y =  np.max(ptn_gaged[:,2]) 
    # decolength_without_last = 0 

    # print (repo, icurve, PN)

    curveradius = 0 
    curvelength = 0 
    if repo == 1 and PN - 2 > icurve : 
        tmpprofile = []
        for i in range(PN): 
            if i < icurve+1: 
                tmpprofile.append(profile[i])
            elif i == icurve + 1: 
                curveradius = profile[i][0]
                curvelength += profile[i][1]
            else: 
                curvelength += profile[i][1]
        tmpprofile.append([curveradius, curvelength])
        profile = tmpprofile 
        PN = icurve + 2 

    if repo ==0 and PN - 1 > icurve: 
        tmpprofile = []
        for i in range(PN): 
            if i < icurve: 
                tmpprofile.append(profile[i])
            elif i == icurve : 
                curveradius = profile[i][0]
                curvelength += profile[i][1]
            else: 
                curvelength += profile[i][1]
        tmpprofile.append([curveradius, curvelength])

        profile = tmpprofile 
        PN = icurve + 1

    # for pf in profile: 
    #     print (" %.2f, %.2f"%(pf[0]*1000, pf[1]*1000))            



    if icurve == PN -2 and repo ==1  : 
        profile_last_r = profile[PN-1][0]
        curve_last = curves[PN-1]
        Lcurves_last = Lcurves[PN-1]
        deco_n.append([profile[PN-1], curves[PN-1]]) 

        ptn_edges = pf_endings[2] 
        idx = np.where(ptn_npn[:,0] == pf_endings[0][0])[0][0]
        n1 = ptn_npn[idx]
        L_end_angle =pf_endings[2] 

        delA_L = Angle_3nodes(Lcurves_last[0], Lcurves_last[2], n1, xy=23)
        Llength_last = delA_L * profile_last_r

        idx = np.where(ptn_npn[:,0] == pf_endings[1][0])[0][0]
        n1 = ptn_npn[idx]
        R_end_angle = pf_endings[3]  

        delA_R = Angle_3nodes(curve_last[0], curve_last[2], n1, xy=23)
        Rlength_last = delA_R * profile_last_r
        # print ("right n1 x=%.2f, y=%.2f"%(n1[2]*1000, n1[3]*1000))

    elif icurve == PN-1 and repo ==0: 
        profile_last_r = profile[PN-1][0]
        curve_last = curves[PN-1]
        Lcurves_last = Lcurves[PN-1]
        deco_n.append([profile[PN-1], curves[PN-1]]) 

        ptn_edges = pf_endings[2] 
        idx = np.where(ptn_npn[:,0] == pf_endings[0][0])[0][0]
        n1 = ptn_npn[idx]
        L_end_angle =pf_endings[2] 

        delA_L = Angle_3nodes(Lcurves_last[0], Lcurves_last[2], n1, xy=23)
        Llength_last = delA_L * profile_last_r

        idx = np.where(ptn_npn[:,0] == pf_endings[1][0])[0][0]
        n1 = ptn_npn[idx]
        R_end_angle = pf_endings[3]  

        delA_R = Angle_3nodes(curve_last[0], curve_last[2], n1, xy=23)
        Rlength_last = delA_R * profile_last_r
    else: 
        profile_last_r = profile[PN-1][0]
        curve_last = curves[PN-1]
        Lcurves_last = Lcurves[PN-1]
        deco_n.append([profile[PN-1], curves[PN-1]]) 

        ptn_edges = pf_endings[2] 
        idx = np.where(ptn_npn[:,0] == pf_endings[0][0])[0][0]
        n1 = ptn_npn[idx]
        L_end_angle =pf_endings[2] 

        delA_L = Angle_3nodes(Lcurves_last[0], Lcurves_last[2], n1, xy=23)
        Llength_last = delA_L * profile_last_r

        idx = np.where(ptn_npn[:,0] == pf_endings[1][0])[0][0]
        n1 = ptn_npn[idx]
        R_end_angle = pf_endings[3]  

        delA_R = Angle_3nodes(curve_last[0], curve_last[2], n1, xy=23)
        Rlength_last = delA_R * profile_last_r


    expansed_lastCurve_length =  np.max(ptn_gaged[:,2]) - (start + len_shocurve)
    last_l_ratio = Llength_last / expansed_lastCurve_length
    last_r_ratio = Rlength_last / expansed_lastCurve_length

    if ht_ratio ==1.0: 
        print ("* Ratio of the last curve length modifying")
        print ("   Left=%.2f, Scaled= %.2f >> %.2f"%(last_l_ratio, expansed_lastCurve_length*1000, Llength_last*1000 ))
        print ("  Right=%.2f, Scaled= %.2f >> %.2f"%(last_r_ratio, expansed_lastCurve_length*1000, Rlength_last*1000 ))
        print ("  Sho. Angle Start=%.1f, End=%.1f/%.1f"%(degrees(start_angle), degrees(L_end_angle), degrees(R_end_angle)))
    else: 
        print ("* Shoulder Element thickness re-adjusting")

    ###################################################################
    ## collecting the nodes to re-position
    ###################################################################

    psidenodes = surf_pos_side[:, 7:]
    nsidenodes = surf_neg_side[:, 7:]
    sidenodes = np.concatenate((psidenodes, nsidenodes), axis=None)
    snodes = np.unique(sidenodes) 

    addbuf = 0.0E-03
    if len_shocurve == 0: 
        addsho = start - addbuf
    else: 
        addsho = start 

    if len(ptn_orgn) ==0: 
        # print ("start = %.2f buffer=%.2f (layout half TDW=%.2f)"%(( layout_TDW/2.0 - buffer)*1000, buffer*1000, layout_TDW*500))

        temp1 = np.where(ptn_gaged[:,2] >= addsho)[0] 
        temp2 = np.where(ptn_gaged[:,2] <= -addsho)[0] 

        temp = np.concatenate((temp1, temp2), axis=None)
        tn = ptn_gaged[temp, 0]
    else: 
        # ptn_TDW, layout_TDW
        WidthR = ptn_TDW / layout_TDW 
        # print ("TDW: Layout= %.2f, Model= %.2f"%(layout_TDW*1000, ptn_TDW*1000))
        # print (" buffer =%.2f >> %.2f"%(buffer*1000, buffer*WidthR*1000))

        temp1 = np.where(ptn_orgn[:,2] >= addsho * WidthR)[0] 
        temp2 = np.where(ptn_orgn[:,2] <= -addsho * WidthR)[0] 

        # print ("start.. orgn", start * WidthR*1000)

        temp = np.concatenate((temp1, temp2), axis=None)
        tn = ptn_orgn[temp, 0]
    
    tn = np.setdiff1d(tn, snodes)


    if ht_ratio != 1.0: 
        btmnode = btm_surf[:,7:].reshape(-1)
        btmnode = np.unique(btmnode)
        tn = np.setdiff1d(tn, btmnode)

    tnodes = []
    for n in tn: 
        ix = np.where(ptn_npn[:,0] == n)[0]
        if len(ix) > 0: ix = ix[0]
        else:  continue 
        tnodes.append(ptn_npn[ix])
    tnodes = np.array(tnodes)   ## node which need to reposition 

    # start = layout_TDW / 2.0 - buffer 
    # print (".. start = %.1f, %.1f"%((layout_TDW / 2.0 - buffer )*1000, start*1000))
    width = max_y - start 
    # R = np.max(ptn_gaged[:,3]) 
    R = curves[0][0][3]
    # print ("start=%.1f, width=%.1f, R=%.5f"%(start*1000, width*1000, R*1000))

    ## section with nodes on the bottom of pattern 
    # ptn_orgn, btm_surf 

    allbtms = btm_surf[:,7:].reshape(-1)
    allbtms = np.unique(allbtms)
    btnodes = []
    
    # print (ptn_orgn)
    # print (allbtms)
    for no in allbtms: 
        
        
        ix = np.where(ptn_orgn[:,0] == no)[0]
        if len(ix)>0: 
            btnodes.append(ptn_orgn[ix[0]])
        # else: 
        #     print ("no found node", no) 

    btnodes = sorted(btnodes, key=lambda X:X[2]) 
    btnodes = np.array(btnodes)
    ptn_section  = []
    for i, nd in enumerate(btnodes): 
        if i ==0: 
            end = [nd[2], nd[3]]
            continue 
        if nd[2] -end[0] > 2.0E-03: 
            front = end 
            end   = [nd[2], nd[3]]
            ptn_section.append([front, end]) 



    rotated=[]
    tops = [];     other=[];     des_x = [];    des_y=[]   ; show = 0 
    lines = []
    # show = 0 
    for nid in tnodes: 

        ix = np.where(ptn_gaged[:,0] == nid[0])[0]
        if len(ix) > 0 : ix = ix[0]
        else:           continue 
        n = ptn_gaged[ix]
        # if show ==1: print ("N x=%.2f"%(n[2]*1000))

        # if nid[0] -10**7 == 198: 
        #     print ("checking node", nid)
        #     print ("%d, %.1f, %.1f, %.1f"%(n[0]-10**7, n[1]*1000, n[2]*1000, n[3]*1000))

        if n[2] < 0.0 : 
            ny = -n[2]
            end_angle = L_end_angle 
        else: 
            ny = n[2]
            end_angle = R_end_angle 
        s = (ny - start) / width
        angle = s * end_angle + (1-s) * start_angle 

        if ny < start and len_shocurve == 0  : 
            L = profile[PN-2][1] - (start - ny)
            curve = curves[PN-2]
            SR =  profile[PN-2][0]
            angle = start_angle

        elif start <= ny and start +len_shocurve > ny : 
            L = ny - start
            curve = curves[PN-2]
            SR = profile[PN-2][0]
            # if nid[0] -10**7 == 198: 
            #     print("1 y=%.2f, SR=%.1f"%(ny*1000, SR*1000))
            #     print ("dist = %.2f"%((ny -  start)*1000))
            #     print ("L=%.1f, CV_y=%.1f, CV_z= %.1f, sr=%.1f"%(L*1000, curve[0][2]*1000, curve[0][3]*1000, SR*1000))
        else: 
            if nid[2] > 0: 
                L = (ny -  (start  + len_shocurve)) * last_r_ratio
            else: 
                L = (ny -  (start  + len_shocurve)) * last_l_ratio
            curve = curves[PN-1]
            SR = profile[PN-1][0]
            # print("2 y=%.2f, SR=%.1f"%(ny*1000, SR*1000))

        toppos = positionOnCurve_byLength(L, curve[0], curve[1], curve[2], r=SR, xy=23)
        if n[2] > 0:    tops.append(toppos)
        else:           tops.append([toppos[0], toppos[1], -toppos[2], toppos[3]])
        # if nid[0] -10**7 == 198: 
        #     print ("dist = %.2f ratio=%.1f"%((ny -  (start  + len_shocurve))*1000, last_r_ratio ))
        #     print ("%.1f, %.1f, %.1f, sr=%.1f"%(L*1000, curve[0][2]*1000, curve[0][3]*1000, SR*1000))
        # if nid[0] -10**7 == 198: 
        #     print (" L = %.1f"%(L*1000))
        pattern_gage_ratio = Gauge_Ratio_to_Bottom_of_Pattern_node(n, ptn_section, ptn_R, ptn_orgn)
        layout_gage, other_pos = Layout_Tread_Gauge_at_pattern_node (toppos, bodybottom, angle)
        if n[2] > 0: other.append(other_pos)
        else:        other.append([-other_pos[0], other_pos[1]])

        # print ("n3 x=%.1f, y=%.1f, Top x=%.1f, y=%.1f"%(n[2]*1000, n[3]*1000, toppos[2]*1000, toppos[3]*1000))
        # if pattern_gage_ratio > 1.0: 
        #     print (" x=%.1f y=%.1f A =%.1f, R=%.2f, Ga=%.1f > %.1f"%(n[2]*1000, n[3]*1000, degrees(angle), pattern_gage_ratio, layout_gage*1000, layout_gage * pattern_gage_ratio*1000))
        if pattern_gage_ratio >=0 and layout_gage > 0: 
            ht = layout_gage * pattern_gage_ratio 
        else: 
            # print ("No value n=%d ratio=%.1f, ga=%.2f"%(n[0]-10**7, pattern_gage_ratio, layout_gage*1000))
            ht = R - n[3]

    

        initpos = [0, toppos[1], toppos[2], toppos[3] - ht]

        if ht ==R: 
            rd = toppos
        else: 
            rd = RotateNode(initpos, -angle, toppos, xy=23)
        ix = np.where(ptn_npn[:,0]==n[0])[0][0]
        # print (" (%.2f, %.2f) => (%.2f, %.2f)"%( ptn_npn[ix][2]*1000,  ptn_npn[ix][3]*1000, rd[2]*1000, rd[3]*1000))
        # print (" (%.2f, %.2f) => (%.2f, %.2f)"%( initpos[2]*1000,  initpos[3]*1000, rd[2]*1000, rd[3]*1000))
        if n[2] < 0: ptn_npn[ix][2] = - rd[2] 
        else:        ptn_npn[ix][2] =  rd[2]  
        ptn_npn[ix][3] = rd[3]
        des_x.append(ptn_npn[ix][2])
        des_y.append(ptn_npn[ix][3])

        # if ht < 0.1E-03: 
        #     lines.append([[n[2], ptn_npn[ix][2]], [n[3], ptn_npn[ix][3]]])

        # if show == 1:  print ("sho node x=%.2f, y=%.2f => x=%.2f, y=%.2f (a=%.1f)"%(n[2]*1000, n[3]*1000, ptn_npn[ix][2]*1000, ptn_npn[ix][3]*1000, degrees(angle)))

    
    return ptn_npn#, lines

def Gauge_Ratio_to_Bottom_of_Pattern_node(N, Ptn_btm_sorted_nodes, pattern_max_R, ptn_orgn): 
    sections = Ptn_btm_sorted_nodes
    R = pattern_max_R
    ix = np.where(ptn_orgn[:,0] == N[0])[0][0]
    n = ptn_orgn[ix]

    if n[3] == R : return 0 

    # print ("N x=%8.2f, y=%8.2f Dist=%.2f"%(N[2]*1000, N[3]*1000, (R-N[3])*1000))


    TG = -1  
    
    for sec in sections: 
        if sec[0][0] <= n[2] and n[2] <= sec[1][0] : 
            TG = (sec[1][1] - sec[0][1]) / (sec[1][0] - sec[0][0]) * ( n[2] - sec[0][0] ) + sec[0][1] 
            break 
    if TG>0: 
        return (R-n[3]) / (R-TG)
    if n[2] < 0: 
        TG = (sections[0][1][1] - sections[0][0][1]) / (sections[0][1][0] - sections[0][0][0]) * ( n[2] - sections[0][0][0] ) + sections[0][0][1] 
    else: 
        N = len(sections)-1 
        TG = (sections[N][1][1] - sections[N][0][1]) / (sections[N][1][0] - sections[N][0][0]) * ( n[2] - sections[N][0][0] ) + sections[N][0][1] 
    
    if TG>0: 
        return (R-n[3]) / (R-TG)
    # print ("TG=%.1f, R=%.1f, n[3]=%.1f"%(TG*1000, R*1000, n[3]*1000))
    return -1

def Layout_Tread_Gauge_at_pattern_node(node_on_profile, nodes_layout_td_bottom, tilting_angle): 
    N = node_on_profile 
    PI = 3.14159265358979323846
    # slope = tan(PI/2 - angle)
    ## y1 = slope * (x1 - N[2]) + N[3]  
    ## y2 = (n2[3]-n1[3]) / (n2[2] - n1[3]) (x2 - n1[2] ) + n1[3]  

    m1 = tan(PI/2 - tilting_angle); n1 = -m1 * N[2] + N[3] 


    for i, nd in enumerate(nodes_layout_td_bottom): 
        if i ==0: continue  

        m2 = (nd[3] - nodes_layout_td_bottom[i-1][3]) / (nd[2] - nodes_layout_td_bottom[i-1][2]) 
        n2 = -m2 * nodes_layout_td_bottom[i-1][2] + nodes_layout_td_bottom[i-1][3]

        Px = (m1*N[2] - m2 * nodes_layout_td_bottom[i-1][2] - N[3] + nodes_layout_td_bottom[i-1][3]) / (m1 - m2)
        Py = m1 * (Px - N[2]) + N[3]

        if nd[3] > nodes_layout_td_bottom[i-1][3]: 
            up = nd[3]; down = nodes_layout_td_bottom[i-1][3]
        else: 
            down = nd[3]; up = nodes_layout_td_bottom[i-1][3]

        if nodes_layout_td_bottom[i-1][2] <= Px and Px <= nd[2] and down <=Py and Py <= up : ## edges_layout_removed_tread should be only bottom.. 
            Length = sqrt ((N[2] - Px)**2 + (N[3]-Py)**2) 
            return Length, [Px, Py]

    return 0, [N[2], N[3]]


def positionOnCurve_byLength(length, curve_start, curve_end, curve_center, r=0, xy=23): 
    x = int(xy/10); y=int(xy%10)

    cs = curve_start
    ce = curve_end 
    cc = curve_center 
    
    refn = [0, cc[1], cc[2], cc[3]]
    refn[y] += 1.0  
    start_angle = Angle_3nodes(refn, cc, cs) 
    if r == 0 : 
        r = NodeDistance(cc, cs, xy=23) 

    angle = length / r  + start_angle 

    rx = r * sin(angle) + cc[x] 
    ry = r * cos(angle) + cc[y]

    position = [0, 0.0, 0.0, 0.0]
    position[x] = rx 
    position[y] = ry 
    return position 


def Pattern_Gauge_ratio_adjustment(section, nodes_solids, pattern_solid, pattern_nodes, pattern_org_nodes, modelgauges, GaugeConstantRange, fix=0, start=0, xy=23, mg=0.5E-03, TargetR=0, ModelR=0): 
    x = int(xy/10); y=int(xy%10)
    R = TargetR
    PR = ModelR

    pnodes = []
    m = len(section) -1 
    fix_ratio = 0
    if start > 0: GaugeConstantRange = start 
    border_width = 10.0E-03 # np.max(pattern_nodes[:,2]) - GaugeConstantRange

    # print ("GAUGE AJD START=%.3fmm"%(GaugeConstantRange*1000))

    #  modelgauges = [start_node[x], end_node[x], start_node[y], end_node[y]] 
    for n in nodes_solids:    ## nodes except bottom surface 
        if n > 0: 
            ix = np.where(pattern_nodes[:,0] == n)[0][0]
            pn = pattern_nodes[ix]
            ## section : profile top surface (tread bottom surface) - edges.. 
            if pn[x] <=section[0][0][0]:    ## k = 0 : in case that the nodes are over the total pattern width  to the negative 
                ty = ((section[0][1][1]-section[0][0][1])/(section[0][1][0]-section[0][0][0])) * (pn[x]-section[0][0][0]) + section[0][0][1]
                CG = R - ty ## Target Tire Tread Gauge 
                ix = np.where(pattern_org_nodes[:,0] == pn[0])[0][0]; ON = pattern_org_nodes[ix]
                PL = PR - ON[3] 
                PG = PR - modelgauges[0][2]
                pn[y]=R - PL * CG / PG 
                pnodes.append(pn)
                continue 

            elif pn[x] >= section[m][1][0]:  ## m = len(section) - 1 :  in case that the nodes are over the total pattern width  to the positive 
                ty = ((section[m][1][1]-section[m][0][1])/(section[m][1][0]-section[m][0][0])) * (pn[x]-section[m][0][0]) + section[m][0][1]
                CG = R-ty ## Target Tire Tread Gauge 
                CL = R - pn[y]   # distance from Tire OD to the current node 
                ix = np.where(pattern_org_nodes[:,0] == pn[0])[0][0]; ON = pattern_org_nodes[ix]
                PL = PR - ON[3] 
                PG = PR - modelgauges[m][3]
                pn[y]=R - PL * CG / PG 
                pnodes.append(pn)
                continue 

            elif abs(pn[x]) >= GaugeConstantRange - border_width and abs(pn[x]) <= GaugeConstantRange: 
                for sec in section: 
                    if pn[x] > sec[0][0] and pn[x] <= sec[1][0]: ##  the lateral position  of node(pn)
                        ty = ((sec[1][1]-sec[0][1])/(sec[1][0]-sec[0][0])) * (pn[x]-sec[0][0]) + sec[0][1]  ## ty = gauge at pn[x] 
                        CG = R - ty ## Tire Tread Gauge at pn[x]
                        CL = R - pn[y]   # distance from Tire OD to the current node 
                        scaled_gage_ratio = CL / CG 

                        ix = np.where(pattern_org_nodes[:,0] == pn[0])[0][0]
                        ON = pattern_org_nodes[ix]
                        PL = PR - ON[3]  ## Distance from top to the node in Model Pattern 

                        PG = 0 
                        
                        for g in modelgauges: 
                            if ON[x] >= g[0] and ON[x]<=g[1]: 
                                py = (g[3]-g[2]) / (g[1]-g[0]) * (ON[x] - g[0]) + g[2]
                                PG = PR - py # Model Pattern tire tread gauge 
                                break 

                        if PG == 0: 
                            if ON[x] < modelgauges[0][0] : 
                                py = modelgauges[0][2]
                            else: 
                                N  = len(modelgauges)
                                py = modelgauges[N-1][3]
                            PG = PR - py 

                        model_gage_ratio = PL / PG 
                        # if  abs(pn[x]) < GaugeConstantRange :
                        s = 1 -  (GaugeConstantRange - abs(pn[x])) / border_width 
                        target_gage_ratio = model_gage_ratio * s + (1-s)*scaled_gage_ratio 
                        modified_gauge =  CG * target_gage_ratio 
                        pn[y]=R - modified_gauge

                        # print ("Node %d: X=%.3f (y=%.3f > %.3f)\n c : %.3f/%.3f=%.2f, M: %.3f/%.3f=%.2f"%(pn[0]-10**7, pn[x]*1000, (R-CL)*1000, pn[y]*1000, CL*1000, CG*1000, CL/CG, PL*1000, PG*1000, PL/PG))

                        pnodes.append(pn)
                        break 
            elif abs(pn[x]) > GaugeConstantRange: 
                ## normal case  : for the most cases 
                for sec in section: 
                    if pn[x] > sec[0][0] and pn[x] <= sec[1][0]: 
                        ty = ((sec[1][1]-sec[0][1])/(sec[1][0]-sec[0][0])) * (pn[x]-sec[0][0]) + sec[0][1]

                        CG = R - ty ## Target Tire Tread Gauge 
                        CL = R - pn[y]   # distance from Tire OD to the current node 
                        
                        ix = np.where(pattern_org_nodes[:,0] == pn[0])[0][0]
                        ON = pattern_org_nodes[ix]
                        PL = PR - ON[3]  ## Distance from top to the node in Model Pattern 
                        PG = 0 
                        for g in modelgauges: 
                            if ON[x] >= g[0] and ON[x]<=g[1]: 
                                py = (g[3]-g[2]) / (g[1]-g[0]) * (ON[x] - g[0]) + g[2]
                                PG = PR - py # Model Pattern tire tread gauge 
                                break 
                        if round(PG, 3) <= 0 : 
                            if ON[x] < 0 : PG = PR - modelgauges[0][3]
                            else:          PG = PR - modelgauges[len(modelgauges)-1][3]
                            # print (" No model gauge, position x =%.3f, replace PG = %.3f"%(pn[x]*1000, PG*1000) )
                        # modified_gauge =  CG *  PL / PG 
                        pn[y]=R -  CG *  PL / PG
                        pnodes.append(pn)
                        
                        break
            else: 
                pnodes.append(pn)
                
    # print ("#################### fix=%d, start=%.2f"%(fix_ratio, start*1000))
    return pnodes, fix_ratio, start
def Adjust_PatternBottomSideNodes(layout_nodes, element_body, element_tread, pattern_nodes, surf_pattern_neg, surf_pattern_pos, pattern_origin_node, pattern_bottom_surf, TDW=0.0, t3dm=0): 
    
    edge_body = element_body.OuterEdge(layout_nodes)
    edge_tread = element_tread.OuterEdge(layout_nodes)

    npn = np.array(layout_nodes)

    # Image(file="0-body_outer_edge", edge=edge_body.Edge,  edn=layout_nodes.Node, eeid=1, enid=1, dpi=800)
    # Image(file="0-body_outer_edge1",  edge1=edge_tread.Edge, edn=layout_nodes.Node, eeid=1, enid=1, dpi=800)
    # Printlist(edge_body.Edge, all=1)
    # print ("***********************")
    # Printlist(edge_tread.Edge, all=1)

    interface = EDGE()
    for e1 in edge_tread.Edge:
        for e2 in edge_body.Edge: 
            if e1[0] == e2[1] or e1[1] == e2[0]:   # it's possible to find the edges with 2:1 element tie connection ... 
                interface.Add(e1) 
                break 
    nGroup, singles =HowManyEdgeGroup(interface.Edge)
    # print ("edge groups=%d"%(nGroup))
    # print ("nodes", singles)
    if nGroup > 1: 
        ## edge =>  n2 - n1 
        # print ("connecting edgess")
        ymax = 0
        ymin = 0 
        nmax = 0
        nmin = 0 
        for i, ed in enumerate(interface.Edge): 
            # n = layout_nodes.NodeByID(ed[0]) 
            ix = np.where(npn[:,0]==ed[0])[0][0]; n = layout_nodes.Node[ix]
            # print(i, ed[0], n)
            if i == 0: 
                nmax = n[0] 
                nmin = n[0]
                ymax = n[2]
                ymin = n[2]
            else: 
                if ymax < n[2] : 
                    ymax = n[2]
                    nmax = n[0]
                if ymin > n[2]: 
                    ymin = n[2]
                    nmin = n[0]
        # print (" >>", nmin, nmax)
        # print (" <<", ymin, ymax) 


        for ed in interface.Edge: 
            if ed[0] == nmax: 
                sedge=ed 
                break 

        # print ("pos", sedge)

        f = 1 
        while f : 
            ix = NextEdge(sedge, edge_tread.Edge)
            sedge = edge_tread.Edge[ix]
            interface.Add(sedge) 
            # print (sedge)
            for ed in  interface.Edge: 
                if ed[0] == sedge[0] and ed[1] == sedge[1]: 
                    f = 0
                    break 

        for ed in interface.Edge: 
            if ed[1] == nmin: 
                sedge=ed 
                break 
        # print ("neg", sedge)

        f = 1 
        while f: 
            ix = PreviousEdge(sedge, edge_tread.Edge)
            sedge = edge_tread.Edge[ix]
            interface.Add(sedge) 
            # print (sedge)
            for ed in  interface.Edge: 
                if ed[0] == sedge[0] and ed[1] == sedge[1]: 
                    f = 0 
                    break 

    nGroup, singles =HowManyEdgeGroup(interface.Edge)
    # print ("edge groups=%d"%(nGroup))  
    interface.Sort()
    N = len(interface.Edge)
    del(interface.Edge[N-1])
    del(interface.Edge[0])


    
    ## only for round type shoulder. 
    ## need to divide the edges into sides and bottom 
    ############################################################################################
    layoutnode = np.array(layout_nodes.Node)

    rightside=EDGE()
    re = 0 
    for i, e in enumerate(interface.Edge): 
        if i ==0: 
            rightside.Add(e)
        else: 
            idx = np.where(layoutnode[:,0]==interface.Edge[i-1][0])[0][0]
            n1 = layoutnode[idx]
            idx = np.where(layoutnode[:,0]==e[0])[0][0]
            n2 = layoutnode[idx]
            idx = np.where(layoutnode[:,0]==e[1])[0][0]
            n3 = layoutnode[idx]

            angle = Angle_3nodes(n1, n2, n3, xy=23)

            if degrees(angle) < 150.0: 
                re = i
                break 
            else:
                rightside.Add(e)

    i = 0 
    while i < re: 
        del(interface.Edge[0])
        i += 1 

    
    interface.Sort(reverse=True)
    leftside=EDGE()
    le = 0 
    for i, e in enumerate(interface.Edge): 
        if i ==0: 
            leftside.Add(e)
        else: 
            idx = np.where(layoutnode[:,0]==interface.Edge[i-1][1])[0][0]
            n1 = layoutnode[idx]
            idx = np.where(layoutnode[:,0]==e[1])[0][0]
            n2 = layoutnode[idx]
            idx = np.where(layoutnode[:,0]==e[0])[0][0]
            n3 = layoutnode[idx]

            angle = Angle_3nodes(n1, n2, n3, xy=23)

            if degrees(angle) < 150.0: 
                le=i 
                break 
            else:
                leftside.Add(e)

    i = 0 
    while i < le: 
        del(interface.Edge[0])
        i += 1 

    pf_righttop = rightside.Edge[0][0]; pf_rightbtm = rightside.Edge[len(rightside.Edge)-1][1]  
    
    ix = np.where(layoutnode[:,0] == pf_righttop)[0][0]
    pf_topnode = layoutnode[ix]
    ix = np.where(layoutnode[:,0] == pf_rightbtm)[0][0]
    pf_btmnode = layoutnode[ix]

    refn = [0, pf_topnode[1], pf_topnode[2], pf_topnode[3] - 1.0]
    R_end_angle = Angle_3nodes(refn, pf_topnode, pf_btmnode) 

    ## end of the searching edegs in the interface between tread and bottom
    ############################################################################
    # surf_pattern_neg, surf_pattern_pos

    ## surf_patternside : [node_id, face_id, No_nodes, 1.0(free_sf), center coord_1, center coord_2, center coord_3, n1, n2, n3, n4]
    
    nds = []
    for sf in surf_pattern_neg:
        nds.append(sf[7])
        nds.append(sf[8])
        nds.append(sf[9])
        nds.append(sf[10])
    for sf in surf_pattern_pos:
        nds.append(sf[7])
        nds.append(sf[8])
        nds.append(sf[9])
        nds.append(sf[10])
    nds = np.array(nds)
    nds = np.unique(nds)

    ## search for all pattern side nodes : nodes 

    nodes = []
    o_nodes = []
    nothing =[]
    for n in nds: 
        ix = np.where(pattern_nodes[:,0] == n)[0][0]
        nodes.append(pattern_nodes[ix])
        # print (n," : ", ix, " - ", pattern_nodes[ix], end= " *** ")
        ix = np.where(pattern_origin_node[:,0] == n)[0][0]
        o_nodes.append(pattern_origin_node[ix])
        # print (ix, " - ", pattern_origin_node[ix])
    nodes = np.array(nodes)
    o_nodes = np.array(o_nodes)


    idxs = np.where(nodes[:, 2]> 0.0)[0]
    pt_r_nodes = nodes[idxs]
    idxs = np.where(o_nodes[:, 2]>0.0)[0]
    pt_r_Onodes = o_nodes[idxs]


    mg = 0.5E-3 
    mht = np.max(pt_r_nodes[:,3])
    t_idxs = np.where(pt_r_nodes[:,3] == mht)[0]
    pt_topnode = pt_r_nodes[t_idxs[0]] 

    nht = np.min(pt_r_nodes[:,3])
    b_idxs = np.where(pt_r_nodes[:,3] == nht)[0]
    pt_btmnode = pt_r_nodes[b_idxs[0]]

    pf_dist = Distance_2nodes(pf_topnode, pf_btmnode, d2=1, xy=23)
    pt_dist = Distance_2nodes(pt_topnode, pt_btmnode, d2=1, xy=23)

    t_dx=pt_btmnode[2] - pt_topnode[2]; t_dy=abs(pt_topnode[3] - pt_btmnode[3])
    p_dx=pf_btmnode[2] - pf_topnode[2]; p_dy=abs(pf_topnode[3] - pf_btmnode[3])

    t_angle = atan((t_dx)/(t_dy))
    p_angle = atan((p_dx)/(p_dy))
    angle =  p_angle - t_angle  

    ratio = pf_dist / pt_dist
    topwd = pt_topnode[2];        topht = pt_topnode[3]
    for i, nd in enumerate(pt_r_nodes): 
        pt_r_nodes[i][2] = topwd - (topwd - nd[2])*ratio 
        pt_r_nodes[i][3] = topht - (topht - nd[3])*ratio 

        length = sqrt((topwd - nd[2])**2 + (topht - nd[3])**2)
        if length < .1E-03: 
            pt_r_nodes[i][2] = topwd; pt_r_nodes[i][3] = topht

    


    ## node distance ratio from top done.
    pt_right_edge=[pt_topnode[0], pt_btmnode[0]]

    #############################################################################################
    ### # verification 
    # t_idxs1 = np.where(pt_r_Onodes[:,3] > mht-mg)[0]
    # pt_topnode_1 = pt_r_nodes[t_idxs1[0]] 
    # nht = np.min(pt_r_Onodes[:,3])
    # b_idxs1 = np.where(pt_r_Onodes[:,3] < nht+mg)[0]
    # pt_btmnode_1 = pt_r_nodes[b_idxs1[0]]
    # pt_dist_1 = Distance_2nodes(pt_topnode_1, pt_btmnode_1, d2=1, xy=23)
    # print ("Pattern SIDE TOP: %4d, %7.3f, %7.3f, %7.3f"%(pt_topnode[0]-10**7, pt_topnode[1]*10**3, pt_topnode[2]*10**3, pt_topnode[3]*10**3))
    # print ("Pattern SIDE BTM: %4d, %7.3f, %7.3f, %7.3f"%(pt_btmnode[0]-10**7, pt_btmnode[1]*10**3, pt_btmnode[2]*10**3, pt_btmnode[3]*10**3))
    # print ("PROFILE SIDE TOP: %4d, %7.3f, %7.3f, %7.3f"%(pf_topnode[0], pf_topnode[1]*10**3, pf_topnode[2]*10**3, pf_topnode[3]*10**3))
    # print ("PROFILE SIDE BTM: %4d, %7.3f, %7.3f, %7.3f"%(pf_btmnode[0], pf_btmnode[1]*10**3, pf_btmnode[2]*10**3, pf_btmnode[3]*10**3))
    # print ("LENGTH RATIO=%.3f, Pattern=%.3f, Profile=%.3f, Length of pattern side=%.3f"%(ratio, pt_dist*1000, pf_dist*1000, pt_dist_1*1000))
    # print ("ANGLE BETWEEN=%.2f"%(degrees(angle)))

    # for iptn in pt_r_nodes: 
    #     dist_1 = Distance_2nodes(pt_topnode_1, iptn, d2=1, xy=23)
    #     print (" > Length from Side Top=%.3f (<=%.3f) diff=%.3f"%(dist_1*1000,pf_dist*1000, (dist_1-pf_dist)*1000))
    # print ("PRF top %12.6f, %12.6f"%(pf_topnode[2]*1000, pf_topnode[3]*1000))
    # print ("PTN top %12.6f, %12.6f"%(pt_topnode[2]*1000, pt_topnode[3]*1000))
    #############################################################################################

    shift2 = pf_topnode[2]-pt_topnode[2]
    shift3 = pf_topnode[3]-pt_topnode[3]
    
    tp2 = pt_topnode[2]; tp3 = pt_topnode[3]
    tf2 = pf_topnode[2]; tf3 = pf_topnode[3]
    
    # w = open("0_sidenodepositioning.txt", 'w')
    pnds=[]
    for i, nd in enumerate(pt_r_nodes): 
        
        line = "%8d, %.6f, %.6f, %.6f, ,"%(nd[0], nd[1], nd[2], nd[3])

        # _, insec = DistanceFromLineToNode2D(nd, [pf_topnode, pf_btmnode], xy=23)
        ix = np.where(pattern_nodes[:,0] == nd[0])[0][0]
        # pattern_nodes[ix][2] = insec[2]
        # pattern_nodes[ix][3] = insec[3]
        # if nd[0]-10**7 == 3622 or nd[0]-10**7 == 3634:  
        #     print (" node %d: %.3f,  %.3f"%(nd[0]-10**7, nd[2]*1000, nd[3]*1000))
        #     print ("            %.3f,  %.3f"%(pattern_nodes[ix][2]*1000, pattern_nodes[ix][3]*1000))

        n2 = nd[2] - topwd; n3 = nd[3] - topht 
        # ix = np.where(pattern_nodes[:,0] == nd[0])[0][0]
        # print (" node %d: %.3f,  %.3f"%(nd[0]-10**7, nd[2]*1000, nd[3]*1000))
        pattern_nodes[ix][2] = topwd + cos(angle) * n2 - sin(angle) * n3 +shift2
        pattern_nodes[ix][3] = topht + sin(angle) * n2 + cos(angle) * n3 +shift3
        # print ("            %.3f,  %.3f"%(pattern_nodes[ix][2]*1000, pattern_nodes[ix][3]*1000))

        ## Re-Attaching the nodes on the side surface .. 
        _, intersectN = DistanceFromLineToNode2D(pattern_nodes[ix], [pf_topnode, pf_btmnode], xy=23)
        pattern_nodes[ix][2] = intersectN[2]
        pattern_nodes[ix][3] = intersectN[3]

        # print (nd[0], ",", pattern_nodes[ix][0])

        # line += "%6f, %6f, %6f\n"%(pattern_nodes[ix][1], pattern_nodes[ix][2], pattern_nodes[ix][3])

        # if nd[0]-10**7 == 3628 or nd[0]-10**7 == 3634:  
        #     print (" node %d: %.3f,  %.3f  distance from top x=%.3f, y=%.3f "%(nd[0]-10**7, nd[2]*1000, nd[3]*1000, n2*1000, n3*1000))
        #     print ("            %.3f,  %.3f  displacement x=%.3f, y=%.3f"%(pattern_nodes[ix][2]*1000, pattern_nodes[ix][3]*1000, (pattern_nodes[ix][2]-nd[2])*1000, (pattern_nodes[ix][3]-nd[3])*1000))
        pnds.append(nd[0])

        # w.write(line)
    # w.close()

    ix21 = np.where(pattern_nodes [:, 2] > tp2 - 0.05E-3)[0]
    ix22 = np.where(pattern_nodes [:, 2] < tp2 + 0.05E-3)[0]
    ix2 = np.intersect1d(ix21, ix22)

    ix31 = np.where(pattern_nodes [:, 3] > tp3 - 0.05E-3)[0]
    ix32 = np.where(pattern_nodes [:, 3] < tp3 + 0.05E-3)[0]
    ix3 = np.intersect1d(ix31, ix32)
    ix = np.intersect1d(ix2, ix3)

    for x in ix: 
        pattern_nodes[x][2] =  tf2
        pattern_nodes[x][3] =  tf3

    

    # print ("####### no of side nodes %d"%(len(pt_r_nodes)))

    ## Nodes on the right side surface is attached to the profile right  Pattern boundary. 


    ########################################################################################
    leftside.Sort(reverse=True)
    # leftside.Print(all=1)
    pf_lefttop = leftside.Edge[0][1]; pf_leftbtm = leftside.Edge[len(leftside.Edge)-1][0]  

    ix = np.where(layoutnode[:,0] == pf_lefttop)[0][0]
    pf_topnode = layoutnode[ix]
    ix = np.where(layoutnode[:,0] == pf_leftbtm)[0][0]
    pf_btmnode = layoutnode[ix]

    refn = [0, pf_topnode[1], pf_topnode[2], pf_topnode[3] - 1.0]
    L_end_angle = Angle_3nodes(refn, pf_topnode, pf_btmnode) 

    
    idxs = np.where(nodes[:, 2]< 0.0)[0]
    pt_l_nodes = nodes[idxs]
    pt_l_Onodes = o_nodes[idxs]

    # Print_list(pt_l_nodes)  ## for checking node data 

    mht = np.max(pt_l_nodes[:,3])
    t_idxs = np.where(pt_l_nodes[:,3] == mht)[0]
    pt_topnode = pt_l_nodes[t_idxs[0]] 

    nht = np.min(pt_l_nodes[:,3])
    b_idxs = np.where(pt_l_nodes[:,3] == nht)[0]
    pt_btmnode = pt_l_nodes[b_idxs[0]]

    pf_dist = Distance_2nodes(pf_topnode, pf_btmnode, d2=1, xy=23)
    pt_dist = Distance_2nodes(pt_topnode, pt_btmnode, d2=1, xy=23)

    t_dx=pt_btmnode[2] - pt_topnode[2]; t_dy=abs(pt_topnode[3] - pt_btmnode[3])
    p_dx=pf_btmnode[2] - pf_topnode[2]; p_dy=abs(pf_topnode[3] - pf_btmnode[3])
    t_angle = atan((t_dx)/(t_dy))
    p_angle = atan((p_dx)/(p_dy))
    angle =  p_angle - t_angle  


    ratio = pf_dist / pt_dist
    topwd = pt_topnode[2];        topht = pt_topnode[3]
    for i, nd in enumerate(pt_l_nodes): 
        pt_l_nodes[i][2] = topwd - (topwd - nd[2])*ratio 
        pt_l_nodes[i][3] = topht - (topht - nd[3])*ratio 

        length = sqrt((topwd - nd[2])**2 + (topht - nd[3])**2)
        if length < .1E-03: 
            pt_l_nodes[i][2] = topwd; pt_l_nodes[i][3] = topht
        
    shift2 = pf_topnode[2]-pt_topnode[2]
    shift3 = pf_topnode[3]-pt_topnode[3]
    
    tp2 = pt_topnode[2]; tp3 = pt_topnode[3]
    tf2 = pf_topnode[2]; tf3 = pf_topnode[3]
    for i, nd in enumerate(pt_l_nodes): 
        n2 = nd[2] - topwd; n3 = nd[3] - topht 
        pt_l_nodes[i][2] = topwd + cos(angle) * n2 - sin(angle) * n3 +shift2
        pt_l_nodes[i][3] = topht + sin(angle) * n2 + cos(angle) * n3 +shift3

        ## Re-Attaching the nodes on the side surface .. 
        _, intersectN = DistanceFromLineToNode2D(pt_l_nodes[i], [pf_topnode, pf_btmnode], xy=23)
        pt_l_nodes[i][2] = intersectN[2]
        pt_l_nodes[i][3] = intersectN[3]

    ### leftside nodes 
    for nd in pt_l_nodes: 
        ix = np.where(pattern_nodes [:,0] == nd[0])[0][0]
        pattern_nodes[ix][2] = nd[2]
        pattern_nodes[ix][3] = nd[3]

    ix21 = np.where(pattern_nodes [:, 2] > tp2 - 0.05E-3)[0]
    ix22 = np.where(pattern_nodes [:, 2] < tp2 + 0.05E-3)[0]
    ix2 = np.intersect1d(ix21, ix22)

    ix31 = np.where(pattern_nodes [:, 3] > tp3 - 0.05E-3)[0]
    ix32 = np.where(pattern_nodes [:, 3] < tp3 + 0.05E-3)[0]
    ix3 = np.intersect1d(ix31, ix32)
    ix = np.intersect1d(ix2, ix3)

    for x in ix: 
    #     # print ("  ** ", int(pattern_nodes[x][0]), round(pattern_nodes[x][1]*1000, 3), round(pattern_nodes[x][2]*1000, 3), round(pattern_nodes[x][3]*1000, 3))
        pattern_nodes[x][2] =  tf2
        pattern_nodes[x][3] =  tf3
    
    pt_left_edge=[pt_topnode[0], pt_btmnode[0], pattern_nodes]
    
    #################################################################
    ## bottom nodes adjustment.. 
    #################################################################
    if t3dm ==1: 
        return pattern_nodes, edge_body,  pnds, [pt_left_edge, pt_right_edge, L_end_angle, R_end_angle]
    return pattern_nodes, edge_body,  pnds, [pt_left_edge, pt_right_edge, L_end_angle, R_end_angle]
def AttatchSquarePatternSideNodes(layout_sidenodes, npn, orgn, surf_posSide, surf_negSide, t3dm=0):
    if layout_sidenodes[0][2] <0 : layout_sidenodes[0][2] *= -1
    if layout_sidenodes[1][2] <0 : layout_sidenodes[1][2] *= -1
    if layout_sidenodes[2][2] <0 : layout_sidenodes[2][2] *= -1
    sideR, sideCen = Circle3Nodes(layout_sidenodes[0], layout_sidenodes[1], layout_sidenodes[2], xy=23, radius=1, center=1)

    # print (" 3 nodes on profile side")
    # print (layout_sidenodes[0][2], ",", layout_sidenodes[0][3])
    # print (layout_sidenodes[1][2], ",", layout_sidenodes[1][3])
    # print (layout_sidenodes[2][2], ",", layout_sidenodes[2][3])
    
    sideNodes=[]
    for sf, sf1 in zip(surf_posSide, surf_negSide): 
        sideNodes.append(sf[7]);    sideNodes.append(sf[8]);    sideNodes.append(sf[9]);    sideNodes.append(sf[10])
        sideNodes.append(sf1[7]);   sideNodes.append(sf1[8]);   sideNodes.append(sf1[9]);   sideNodes.append(sf1[10])
    
    sNodes = np.array(sideNodes)
    sNodes = np.unique(sNodes)
    
    R = np.max(orgn[:,3])
    cn = []; on = []
    for sn in sNodes: 
        ix = np.where(orgn[:,0]==sn)[0][0]
        on.append(orgn[ix])
        cn.append(npn[ix])
        # print ("%d, %.5f, %.5f, %.5f"%(npn[ix][0], npn[ix][1], npn[ix][2], npn[ix][3]))
        # print ("%d, %.5f, %.5f, %.5f"%(orgn[ix][0], orgn[ix][1], orgn[ix][2], orgn[ix][3]))
    
    on = np.array(on)
    sMin = np.min(on[:,3])
    HT = R - sMin 

    ix = np.where(on[:,3]< sMin+0.0001)[0]
    # print (len(ix))
    mw = 0.0
    for x in ix: 
        # print (mw, ",", on[x][0], ",", on[x][2])
        if mw <on[x][2]: 
            mw = on[x][2]
            nodeSideBtm = on[x][0]

    # nodeSideBtm = on[ix[0]][0]

    ix = np.where(npn[:,0]==nodeSideBtm)[0][0]
    nodeSideBtm = [npn[ix][0], npn[ix][1], npn[ix][2], npn[ix][3]]

    
    sMin = layout_sidenodes[2][3]
    ht0 =  layout_sidenodes[0][3] ## shoulder point 
    ht = ht0 - sMin 

    for o in on: 
        ratio = (R-o[3]) / HT 
        dy = ht0 - ht * ratio 
        dx =  sideCen[2] - sqrt(sideR**2 -(dy - sideCen[3])**2)
        ix = np.where(npn[:,0]==o[0])[0][0]
        
        if o[2] >= 0:   npn[ix][2] = dx 
        else: npn[ix][2] = -dx 
        # print (" side Ny=%.2f > %.2f"%(o[2]*1000, npn[ix][2]*1000))
        npn[ix][3] = dy 

    # print ("Tire Half Dia= %.2f"%(R*1000))
    # print ("Side Center, %.2f, %.2f"%(sideCen[2]*1000, sideCen[3]*1000))

    # for p in layout_sidenodes: 
    #     print ("point, %.2f, %.2f"%(p[2]*1000, p[3]*1000))

    return npn, nodeSideBtm


def Unbending_layoutTread(nodes, Tread, LProfile, RProfile, Lcurves, Rcurves, OD, ptn_node=[], GD=0.0) : 

    nodes = np.array(nodes)
    node=NODE()
    for nd in nodes:
        node.Add(nd)
    
    edge_tread = Tread.OuterEdge(node)
    ## searching left bottom or right bottom node for tread bottom edge 
    ## 1) collecting all nodes on tread boundary edge
    edgenodes=[]
    for ed in edge_tread.Edge:
        edgenodes.append(ed[0])
        edgenodes.append(ed[1])
    bnodes = np.array(edgenodes)
    bnodes = np.unique(bnodes)

    ## 2) searching negative/positive bottom end node among them 
    ##     In Round type shoulder profile, right/left bottom node is the lowest point in the z-direction. because its shape is bended. 
    ##    >> leftbtm, rightbtm 
    ## in case that they have square shoulder?  ##############################
    ##    in case of square shoulder profile 
    ##    the leftbtm, rightbtm should be on the far left /right of the tread 

    ##########################################################################

    nds3n=[]; nds3p=[]
    nneg=[]; npos=[]
    for n in bnodes: 
        ix = np.where(nodes[:,0] == n)[0][0]
        if nodes[ix][2] >=0: 
            nds3p.append(nodes[ix][3])
            npos.append(nodes[ix])
            # print ("pos", nodes[ix])
            # print ("pos, %.3f, %.3f"%(nodes[ix][2], nodes[ix][3]))
        else: 
            nds3n.append(nodes[ix][3])
            nneg.append(nodes[ix])
    npos=np.array(npos); nneg=np.array(nneg)

    zmin = min(nds3p)
    ix = np.where(npos[:,3] == zmin)[0][0]
    rightbtm = npos[ix]

    zmin = min(nds3n)
    ix = np.where(nneg[:,3] == zmin)[0][0]
    leftbtm = nneg[ix]


    i = 0 
    while i < len(edge_tread.Edge): 
        if edge_tread.Edge[i][1] == rightbtm[0]: 
            del(edge_tread.Edge[i])
            break 
        i += 1

    edge_tread.Sort()

    btm_edge=EDGE()
    nds=[]
    for ed in edge_tread.Edge:
        btm_edge.Add(ed)
        nds.append(ed[0]); nds.append(ed[1])
        if ed[1] == leftbtm[0]: break 
    
    nds=np.array(nds)
    nds=np.unique(nds)

    tnodes=[]
    for n in nds:
        ix = np.where(nodes[:,0] == n)[0][0]
        tnodes.append(nodes[ix])

    tnds=np.array(tnodes) ## bottom nodes.. 
    # all Bottom nodes are collected. 
    ###################################################

    Rangles=[]
    for crv in Rcurves:
        # print ("* ", crv[0], end=" : ")
        vert = [0, 0, crv[2][2], crv[2][3]+1.0]
        angle_start = Angle_3nodes(vert, crv[2], crv[0], xy=23)
        angle_end = Angle_3nodes(vert, crv[2], crv[1], xy=23)
        Rangles.append([angle_start, angle_end])
        # print ("*Angles start=%.3f, end=%.3f"%(degrees(angle_start), degrees(angle_end)))

    Langles=[]
    for crv in Lcurves:
        # print (crv[0], crv[1], crv[2], end=" : ")
        vert = [0, 0, crv[2][2], crv[2][3]+1.0]
        angle_start = Angle_3nodes(vert, crv[2], crv[0], xy=23)
        angle_end = Angle_3nodes(vert, crv[2], crv[1], xy=23)
        Langles.append([angle_start, angle_end])
        # print ("Angles start=%.3f, end=%.3f"%(degrees(angle_start), degrees(angle_end)))

    flatten=NODE()
    orgn=NODE()
    btmnodes = [] 
    R = OD/2.0 
    for n in tnds:
        orgn.Add(n)
        if abs(n[2])<0.01E-03 : # and n[2] >=0.0: 
            flatten.Add([n[0], n[1], 0.0, n[3]])
        else: 
            if n[2]>0: 
                lsum = 0.0
                cnt = 0 
                for pf, crv, cangle in zip(RProfile, Rcurves, Rangles):
                    vert = [0, 0, crv[2][2], crv[2][3]+1.0]
                    angle = Angle_3nodes(vert, crv[2], n, xy=23)
                    cnt += 1
                    if cnt < len(RProfile): 
                        if angle > cangle[0] and angle <= cangle[1]: 
                            del_length = pf[0] * (angle - cangle[0])
                            length = lsum + del_length ## distance from center 
                            height = R -  pf[0] + sqrt((crv[2][2]-n[2])**2 + (crv[2][3]-n[3])**2) 
                            flatten.Add([n[0], n[1],  length, height])
                            break 
                    else: 
                        del_length = pf[0] * (angle - cangle[0])
                        length = lsum + del_length ## distance from center 
                        height =  R -  pf[0] + sqrt((crv[2][2]-n[2])**2 + (crv[2][3]-n[3])**2) 
                        flatten.Add([n[0], n[1],length, height])
                        break 

                    lsum += pf[1] 
            else: 
                lsum = 0.0
                cnt = 0 
                n[2] *= -1
                for pf, crv, cangle in zip(LProfile, Lcurves, Langles):
                    # print ("\n*** ", -crv[1][2])
                    sx = -crv[0][2]
                    ex = -crv[1][2]
                    cx = -crv[2][2]
                    
                    vert = [0, 0, cx, crv[2][3]+1.0]
                    cent = [crv[2][0],crv[2][1], cx, crv[2][3]]
                    angle = Angle_3nodes(vert, cent, n, xy=23)
                    
                    cnt += 1
                    if cnt < len(LProfile): 
                        if angle > cangle[0] and angle <= cangle[1]: 
                            # print ("  current angle=%7.3f (Curve Start=%7.3f, end=%7.3f), profile R=%7.3f, curve start Y=%7.3f, end=%7.3f, nx=%7.3f"%(degrees(angle), degrees(cangle[0]), degrees(cangle[1]),  pf[0]*1000, sx*1000, ex*1000, n[2]*1000))
                            del_length = pf[0] * (angle - cangle[0])
                            length = lsum + del_length ## distance from center 
                            height = R -  pf[0] + sqrt((cx-n[2])**2 + (crv[2][3]-n[3])**2) 
                            flatten.Add([n[0], n[1],  -length, height])
                            break 
                    else: 
                        # print ("* current angle=%7.3f (Curve Start=%7.3f, end=%7.3f), profile R=%7.3f, curve start Y=%7.3f, end=%7.3f, nx=%7.3f"%(degrees(angle), degrees(cangle[0]), degrees(cangle[1]),  pf[0]*1000, sx*1000, ex*1000, n[2]*1000))
                        del_length = pf[0] * (angle - cangle[0])
                        length = lsum + del_length ## distance from center 
                        height =  R -  pf[0] + sqrt((cx-n[2])**2 + (crv[2][3]-n[3])**2) 
                        flatten.Add([n[0], n[1], -length, height])
                        break 
                    lsum += pf[1] 


    flatterned_sorted = flatten.Sort(item=2)

    ## calculating groove depth if groove depth <=1.0
    ## other nodes 
    if GD <= 1.001E-03: 
        upsides = np.setdiff1d(bnodes, tnds[:,0])

        coordy = tnds[:,2] 
        my = np.max(coordy)
        ups = []
        for nd in upsides:
            idx = np.where(nodes[:,0]==nd)[0][0]
            if abs(nodes[idx][2]) < my*0.8: 
                ups.append(nodes[idx])
        ups = np.array(ups)
        up_flatten = NODE()
        for n in ups:
            if abs(n[2])<0.01E-03 : # and n[2] >=0.0: 
                up_flatten.Add([n[0], n[1], 0.0, n[3]])
            else: 
                if n[2]>0: 
                    lsum = 0.0
                    cnt = 0 
                    for pf, crv, cangle in zip(RProfile, Rcurves, Rangles):
                        vert = [0, 0, crv[2][2], crv[2][3]+1.0]
                        angle = Angle_3nodes(vert, crv[2], n, xy=23)
                        cnt += 1
                        if cnt < len(RProfile): 
                            if angle > cangle[0] and angle <= cangle[1]: 
                                del_length = pf[0] * (angle - cangle[0])
                                length = lsum + del_length ## distance from center 
                                height = R -  pf[0] + sqrt((crv[2][2]-n[2])**2 + (crv[2][3]-n[3])**2) 
                                up_flatten.Add([n[0], n[1],  length, height])
                                break 
                        else: 
                            del_length = pf[0] * (angle - cangle[0])
                            length = lsum + del_length ## distance from center 
                            height =  R -  pf[0] + sqrt((crv[2][2]-n[2])**2 + (crv[2][3]-n[3])**2) 
                            up_flatten.Add([n[0], n[1],length, height])
                            break 

                        lsum += pf[1] 
                else: 
                    lsum = 0.0
                    cnt = 0 
                    n[2] *= -1
                    for pf, crv, cangle in zip(LProfile, Lcurves, Langles):
                        # print ("\n*** ", -crv[1][2])
                        sx = -crv[0][2]
                        ex = -crv[1][2]
                        cx = -crv[2][2]
                        
                        vert = [0, 0, cx, crv[2][3]+1.0]
                        cent = [crv[2][0],crv[2][1], cx, crv[2][3]]
                        angle = Angle_3nodes(vert, cent, n, xy=23)
                        
                        cnt += 1
                        if cnt < len(LProfile): 
                            if angle > cangle[0] and angle <= cangle[1]: 
                                # print ("  current angle=%7.3f (Curve Start=%7.3f, end=%7.3f), profile R=%7.3f, curve start Y=%7.3f, end=%7.3f, nx=%7.3f"%(degrees(angle), degrees(cangle[0]), degrees(cangle[1]),  pf[0]*1000, sx*1000, ex*1000, n[2]*1000))
                                del_length = pf[0] * (angle - cangle[0])
                                length = lsum + del_length ## distance from center 
                                height = R -  pf[0] + sqrt((cx-n[2])**2 + (crv[2][3]-n[3])**2) 
                                up_flatten.Add([n[0], n[1],  -length, height])
                                break 
                        else: 
                            # print ("* current angle=%7.3f (Curve Start=%7.3f, end=%7.3f), profile R=%7.3f, curve start Y=%7.3f, end=%7.3f, nx=%7.3f"%(degrees(angle), degrees(cangle[0]), degrees(cangle[1]),  pf[0]*1000, sx*1000, ex*1000, n[2]*1000))
                            del_length = pf[0] * (angle - cangle[0])
                            length = lsum + del_length ## distance from center 
                            height =  R -  pf[0] + sqrt((cx-n[2])**2 + (crv[2][3]-n[3])**2) 
                            up_flatten.Add([n[0], n[1], -length, height])
                            break 
                        lsum += pf[1] 

            
        up_flatten = np.array(up_flatten.Node)
        GD = round(R - np.min(up_flatten[:, 3]), 4)
    return np.array(flatterned_sorted), GD
def Unbending_squareLayoutTread(nodes, Tread, LProfile, RProfile, OD, curves, shoDrop=0.0): 
    # print("UNBENDING Layout tread")

    edge_tread = Tread.OuterEdge(nodes)
    edgenodes=[]
    for ed in edge_tread.Edge:
        edgenodes.append(ed[0])
        edgenodes.append(ed[1])
    bnodes = np.array(edgenodes)
    bnodes = np.unique(bnodes)
    nodes = np.array(nodes.Node)
    tnodes=[]
    for n in bnodes:
        ix = np.where(nodes[:,0] == n)[0][0]
        tnodes.append(nodes[ix])


    same = 1 
    profiles = []
    if len(LProfile[0]) == 2:      
        addsum = 1
        lsum = 0; rsum=0
    else:
        addsum = 0 

    for lp, rp in zip(LProfile, RProfile): 
        if addsum == 1: 
            lsum += lp[1]; rsum += rp[1]
            lp.append(lsum); rp.append(rsum)
        if round(lp[0], 3) != round(rp[0], 3) : 
            same = 0
        if round(lp[1], 4) != round(rp[1], 4) : 
            same = 0
        profiles.append(rp)
        # print("Right Profile", rp)

    if same ==0: 
        print ("### Asymmetric profile does not support yet.") 
        return nodes, curves

    R = OD/2.0
    pe = [0, 0, 0, R]
    profile=[]
    
    
    angles=[]
    for crv in curves:
        
        vert = [0, 0, crv[2][2], crv[2][3]+1.0]
        angle_start = Angle_3nodes(vert, crv[2], crv[0], xy=23)
        angle_end = Angle_3nodes(vert, crv[2], crv[1], xy=23)
        angles.append([angle_start, angle_end])
        # print ('start, %.5f, %.5f, end,%.5f, %.5f, center, %.5f, %.5f, angle start,%.3f end, %.3f'%(\
        #     crv[0][2], crv[0][3],crv[1][2], crv[1][3],crv[2][2], crv[2][3], degrees(angle_start), degrees(angle_end)))

    negR = 0 
    i = 0
    while i < len(profiles): 
        if i == len(profiles) -1: 
            break 
        if profiles[i][0]<0: 
            negR = 1
            break 
        i += 1
    flatten=NODE()
    orgn=NODE()
    btmnodes = [] 
    lastangle = angles[len(angles)-1][1]
    lastR = profiles[len(profiles)-1][0]
    lastCnt = curves[len(curves)-1][2]
    sideNodes=[curves[len(curves)-1][1]]

    for n in  tnodes:
        orgn.Add(n)
        if abs(n[2])<0.01E-03: 
            flatten.Add([n[0], n[1], 0.0, n[3]])
        elif n[2]>0:
            lsum = 0.0
            fd = 0 
            negR = 0 
            for pf, crv, cangle in zip(profiles, curves, angles): 
                vert = [0, 0, crv[2][2], crv[2][3]+10.0]
                angle = Angle_3nodes(vert, crv[2], n, xy=23)
                if pf[0] < 0 : negR = 1
                if angle > cangle[0] and angle <= cangle[1]: 
                    del_length = pf[0] * (angle - cangle[0])
                    length = lsum + del_length ## distance from center 
                    if negR ==0 : 
                        height = R -  pf[0] + sqrt((crv[2][2]-n[2])**2 + (crv[2][3]-n[3])**2) 
                    else: 
                        height = R + abs(pf[0]) - sqrt((crv[2][2]-n[2])**2 + (crv[2][3]-n[3])**2) 
                    
                    height = round(height, 4)
                    flatten.Add([n[0], n[1],  length, height])
                    # print ([n[0], n[1],  length, height])
                    # print ("R=%.1f, ht=%.5f"%(pf[0], height*1000))
                    fd = 1
                    break 
                else: 
                    lsum = pf[2]
            if fd ==0: 
                # print ("***************************")
                # print (vert)
                # print ("R=%.1f, angle=%.3f"%(pf[0]*1000, degrees(angle)))
                del_length = lastR * (angle - lastangle)

                length = lsum + del_length ## distance from center 
                # print ("y=%.3f, l=%.3f (sum=%.3f, del=%.3f)"%(n[2]*1000, length*1000, lsum*1000, del_length*1000))
                # print (" DelA=%.5f, angle=%.5f, lastA=%.2f"%(degrees(angle -lastangle), degrees(angle), degrees(lastangle)))
                if negR ==0: 
                    dist = lastR - sqrt((lastCnt[2]-n[2])**2 + (lastCnt[3]-n[3])**2) 
                else: 
                    dist = -abs(lastR) + sqrt((lastCnt[2]-n[2])**2 + (lastCnt[3]-n[3])**2) 
                height =  round(R - dist, 4)
                # print (" Del L=%.3f, R=%.2f dist=%.3f ht=%.4f"%(del_length, lastR*1000, dist*1000, height*1000))
                # print ("center, %.3f, %.3f"%(lastCnt[2]*1000, lastCnt[3]*1000))
                flatten.Add([n[0], n[1], length, height])
        else:
            lsum = 0.0
            fd = 0 
            posn = [n[0], n[1], -n[2], n[3]]
            negR = 0 
            for pf, crv, cangle in zip(profiles, curves, angles): 
                vert = [0, 0, crv[2][2], crv[2][3]+10.0]
                angle = Angle_3nodes(vert, crv[2], posn, xy=23)
                if pf[0] < 0 : negR = 1
                if angle > cangle[0] and angle <= cangle[1]: 
                    del_length = pf[0] * (angle - cangle[0])
                    length = lsum + del_length ## distance from center 
                    if negR ==0: 
                        height = R -  pf[0] + sqrt((crv[2][2]-posn[2])**2 + (crv[2][3]-posn[3])**2) 
                    else: 
                        height = R +  abs(pf[0]) - sqrt((crv[2][2]-posn[2])**2 + (crv[2][3]-posn[3])**2) 
                    height = round(height, 4)
                    flatten.Add([n[0], n[1],  -length, height])
                    # print ([n[0], n[1],  length, height])
                    # print ("R=%.1f, ht=%.5f"%(pf[0], height*1000))
                    fd = 1
                    break 
                else: 
                    lsum = pf[2]
            if fd ==0: 
                # print ("***************************")
                # print (vert)
                # print ("R=%.1f, angle=%.3f"%(pf[0]*1000, degrees(angle)))
                del_length = lastR * (angle - lastangle)

                length = lsum + del_length ## distance from center 
                # print ("y=%.3f, l=%.3f (sum=%.3f, del=%.3f)"%(n[2]*1000, length*1000, lsum*1000, del_length*1000))
                # print (" DelA=%.5f, angle=%.5f, lastA=%.2f"%(degrees(angle -lastangle), degrees(angle), degrees(lastangle)))
                if negR ==0: 
                    dist = lastR - sqrt((lastCnt[2]-posn[2])**2 + (lastCnt[3]-posn[3])**2) 
                else: 
                    dist =  -abs(lastR) + sqrt((lastCnt[2]-posn[2])**2 + (lastCnt[3]-posn[3])**2) 
                height =  round(R - dist, 4)
                # print (" Del L=%.3f, R=%.2f dist=%.3f ht=%.4f"%(del_length, lastR*1000, dist*1000, height*1000))
                # print ("center, %.3f, %.3f"%(lastCnt[2]*1000, lastCnt[3]*1000))
                flatten.Add([n[0], n[1], -length, height])

    # for on, fn in zip(orgn.Node, flatten.Node): 
    #     print ("%d, %.6f, %.6f, , %d, %.6f, %.6f"%(on[0], on[2], on[3], fn[0], fn[2], fn[3]))

    # print (len(orgn.Node), len(flatten.Node))

    # flatterned_sorted = flatten.Sort(item=2)
    npn = np.array(flatten.Node)

    ## search bottom nodes 
    # btm_edges = EDGE()
    btm_edges = []
    e1=[]; e2=[]; edges=[]
    # print ("## TREAD EDGE TOP")
    for ed in edge_tread.Edge:
        ix1 = np.where(npn[:,0] == ed[0])[0][0]
        ix2 = np.where(npn[:,0] == ed[1])[0][0]

        # print (" %.5f, %.5f,\n %.5f, %5.5f,"%(npn[ix1][2], npn[ix1][3], npn[ix2][2], npn[ix2][3]))
        if npn[ix1][3] < R or npn[ix2][3] < R: 
            # print ("%d (%.2f), %d (%.2f)"%(ed[0], npn[ix1][3]*1000, ed[1], npn[ix2][3]*1000))
            # print("%d,"%(ed[4]), end=" ")
            btm_edges.append(ed)
            e1.append(ed[0])
            e2.append(ed[1])
            edges.append([ed[0], ed[1]])

    e1 = np.array(e1); e2 = np.array(e2); edges = np.array(edges)
    en = np.setdiff1d(e1, e2)
    # print ("the No. of Tread Edge separated %d\n\n"%(len(en)))
    if len(en)>1: 
        connected = []
        for e in en: 
            tmp = []
            idx = np.where(edges[:,0]==e)[0]
            cnt = 0 
            while len(idx): 
                tmp.append(btm_edges[idx[0]])
                idx =np.where(edges[:,0] == edges[idx[0]][1])[0]
                cnt += 1
                if cnt > 10000: break 
            if len(tmp) > 0: connected.append(tmp)
        mx = 0 
        for con in connected:   ## 가장 많은 개수를 가진 Edge 선택 
            # print ("the no. of edge", len(con))
            if len(con)> mx: 
                btm_edges = con 
                mx = len(con) 
                # print ("EDGE selected..")
    # print ("BTM Edges\n\n")
    # for ed in btm_edges:
    #     print("%d,"%(ed[4]), end="")

    # print ("end...")
    i = 0
    N = len(btm_edges)-5
    cnt = 0 
    while 1:
        cnt += 1
        if i >= N or cnt > 100000: break 
        ix = np.where(npn[:,0]==btm_edges[0][0])[0][0]; n0=npn[ix]
        ix = np.where(npn[:,0]==btm_edges[0][1])[0][0]; n1=npn[ix]
        ix = np.where(npn[:,0]==btm_edges[1][1])[0][0]; n2=npn[ix]
        if abs(n0[2] - n1[2]) > abs(n0[3] - n1[3]) : 
            del(btm_edges[0])
            continue 
        angle = Angle_3nodes(n0, n1, n2, xy=23)
        treadSide2Nodes = [n0[0], n1[0]]
        # print (n0[0], n1[0])
        del(btm_edges[0])
        if angle < 2.3: ## 130 degrees
            break 
    cnt = 0 
    while 1: 
        cnt += 1
        N = len(btm_edges)-1
        if N < 5 or cnt > 100000: break 
        ix = np.where(npn[:,0]==btm_edges[N][1])[0][0]; n0=npn[ix]
        ix = np.where(npn[:,0]==btm_edges[N][0])[0][0]; n1=npn[ix]
        ix = np.where(npn[:,0]==btm_edges[N-1][0])[0][0]; n2=npn[ix]
        if abs(n0[2] - n1[2]) > abs(n0[3] - n1[3]) : 
            del(btm_edges[N])
            continue 
        angle = Angle_3nodes(n0, n1, n2, xy=23)
        del(btm_edges[N])
        if angle < 2.3: ## 130 degrees
            break 

    # print ("BTM Edges")
    # for ed in btm_edges:
    #     print("%d,"%(ed[4]), end="")

    btm_nodes=NODE()
    for i, ed in enumerate(btm_edges): 
        if i == 0: 
            ix = np.where(npn[:,0]==ed[0])[0][0]
            btm_nodes.Add(npn[ix])
        ix = np.where(npn[:,0]==ed[1])[0][0]
        btm_nodes.Add(npn[ix])
    # for n in btm_nodes.Node:
    #     print("%d,"%(n[0]))
    btm_nodes = btm_nodes.Sort(item=2)

    ix = np.where(nodes[:,0]== treadSide2Nodes[0])[0][0]
    sideNodes.append(nodes[ix])
    ix = np.where(nodes[:,0]== treadSide2Nodes[1])[0][0]
    sideNodes.append(nodes[ix])

    return  np.array(btm_nodes), sideNodes

def Pattern_Gauge_Adjustment_ToBody(bottom_nodes_sorted, pattern_nodes, pattern_btm_surf, pattern_solid, OD, GaugeConstantRange, pattern_org_nodes, surf_ptnside_pos, surf_ptnside_neg, xy=23, mg=0.5E-03): 
    #        _Tread_bottom_sorted, pattern.npn, pattern.freebottom, pattern.nps, layout.OD, gauge_constant_range, pattern.Node_Origin, pattern.surf_pattern_pos_side, pattern.surf_pattern_neg_side)
    # bottom_nodes_sorted : flattened profile tread bottom nodes. 
    # pattern_nodes : current configuration. , pattern_org_nodes : initial configuration 

    x = int(xy/10); y=int(xy%10)

    sod =[]
    for sd in pattern_solid: 
        sod.append([sd[0], sd[1], sd[2], sd[3], sd[4], sd[5], sd[6], sd[7], sd[8], int(sd[9])])
    pattern_solid = np.array(sod)

    R = OD / 2.0 
    section=[]
    for i, nd in enumerate(bottom_nodes_sorted):   ## body bottom nodes sorted... 
        if i ==0: continue 
        start = [bottom_nodes_sorted[i-1][x], bottom_nodes_sorted[i-1][y]]
        end = [nd[x], nd[y]]
        section.append([start, end])

    ## shifting bottom nodes 
    nodes_btm = pattern_btm_surf[:, 7:]
    nodes_btm = nodes_btm.reshape(-1)
    nodes_btm = np.unique(nodes_btm)
    btmnodes = []
    for n in nodes_btm: 
        if n > 0: ## for all nodes (node number is greater than 0)
            ix = np.where(pattern_nodes[:,0] == n)[0][0]
            btmnodes.append(pattern_nodes[ix])

    btmnodes = np.array(btmnodes)

    k = 0 
    m = len(section) -1 
    for i, n in enumerate(btmnodes): ## bottom nodes of the pattern mesh move to the profile top surface 

        # if n[0]-10**7 == 2353 or n[0]-10**7 == 1940 or n[0]-10**7 == 1941 or n[0]-10**7 == 2352  or n[0]-10**7 == 2346: fd=1 
        # else: fd =0 
        if n[x] <=section[k][0][0]: 
            ty = ((section[k][1][1]-section[k][0][1])/(section[k][1][0]-section[k][0][0])) * (n[x]-section[k][0][0]) + section[k][0][1]
            btmnodes[i][y] = ty 
            ix = np.where(pattern_nodes[:,0] == n[0])[0][0]
            pattern_nodes[ix][y] = ty
            continue 
        if n[x] > section[m][1][0]: 
            ty = ((section[m][1][1]-section[m][0][1])/(section[m][1][0]-section[m][0][0])) * (n[x]-section[m][0][0]) + section[m][0][1]
            btmnodes[i][y] = ty 
            ix = np.where(pattern_nodes[:,0] == n[0])[0][0]
            pattern_nodes[ix][y] = ty
            continue 
        for sec in section: 
            if n[x] > sec[0][0]  and n[x] <= sec[1][0] : 
                ty = ((sec[1][1]-sec[0][1])/(sec[1][0]-sec[0][0])) * (n[x]-sec[0][0]) + sec[0][1]
                # if fd ==1: print ("s %d: %.3f, (%.3f -> %.3f)"%(n[0]-10**7, btmnodes[i][x] *1000, btmnodes[i][y] *1000, ty*1000))
                btmnodes[i][y] = ty 
                ix = np.where(pattern_nodes[:,0] == n[0])[0][0]
                pattern_nodes[ix][y] = ty
                break 

    ####################################
    ## solid node connectivity check 
    ###################################

    mg = 0.2E-03 
    for i, sd in enumerate(pattern_solid): 
        ix1 = np.where(pattern_nodes[:,0]==sd[1])[0][0]; n1=pattern_nodes[ix1]
        ix2 = np.where(pattern_nodes[:,0]==sd[2])[0][0]; n2=pattern_nodes[ix2]
        ix3 = np.where(pattern_nodes[:,0]==sd[3])[0][0]; n3=pattern_nodes[ix3]
        ix4 = np.where(pattern_nodes[:,0]==sd[4])[0][0]; n4=pattern_nodes[ix4]
        ix5 = np.where(pattern_nodes[:,0]==sd[5])[0][0]; n5=pattern_nodes[ix5]
        ix6 = np.where(pattern_nodes[:,0]==sd[6])[0][0]; n6=pattern_nodes[ix6]
        if n5[3] > R - mg or n6[3] > R - mg : 
            continue 
        if sd[8] > 0: 
            ix7 = np.where(pattern_nodes[:,0]==sd[7])[0][0]; n7=pattern_nodes[ix7]
            ix8 = np.where(pattern_nodes[:,0]==sd[8])[0][0]; n8=pattern_nodes[ix8]
            if n1[3] >= n5[3]-mg : 
                pattern_nodes[ix5][3] = n1[3] + mg 
                if GaugeConstantRange > abs(n1[2]): GaugeConstantRange = abs(n1[2])
            if n2[3] >= n6[3]-mg : 
                pattern_nodes[ix6][3] = n2[3] + mg 
                if GaugeConstantRange > abs(n2[2]): GaugeConstantRange = abs(n2[2])
            if n3[3] >= n7[3]-mg : 
                pattern_nodes[ix7][3] = n3[3] + mg 
                if GaugeConstantRange > abs(n3[2]): GaugeConstantRange = abs(n3[2])
            if n4[3] >= n8[3]-mg : 
                pattern_nodes[ix8][3] = n4[3] + mg 
                if GaugeConstantRange > abs(n4[2]): GaugeConstantRange = abs(n4[2])
        else: 
            if n1[3] >= n4[3]-mg : 
                pattern_nodes[ix4][3] = n1[3] + mg 
                if GaugeConstantRange > abs(n1[2]): GaugeConstantRange = abs(n1[2])
            if n2[3] >= n5[3]-mg : 
                pattern_nodes[ix5][3] = n2[3] + mg 
                if GaugeConstantRange > abs(n2[2]): GaugeConstantRange = abs(n2[2])
            if n3[3] >= n6[3]-mg : 
                pattern_nodes[ix6][3] = n3[3] + mg 
                if GaugeConstantRange > abs(n3[2]): GaugeConstantRange = abs(n3[2])

    ###################################
    

    ## org pattern pre-precessing 
    PR   = np.max(pattern_org_nodes[:, y])
    pmin = np.min(pattern_org_nodes[:, x])
    pmax = np.max(pattern_org_nodes[:, x])
    btn_ids = btmnodes[:,0]
    org_btnodes = []
    for ids in btn_ids: 
        ix = np.where(pattern_org_nodes[:,0] == ids)[0][0]
        org_btnodes.append([pattern_org_nodes[ix][0], pattern_org_nodes[ix][1], round(pattern_org_nodes[ix][2], 4), pattern_org_nodes[ix][3]])
    org_btnodes = np.array(org_btnodes)
    org_x2 = org_btnodes[:,2]
    org_x2 = np.unique(org_x2)
    org_uni = []
    modelgauges=[]
    for m, x2 in enumerate(org_x2): 
        ix = np.where(org_btnodes[:,2]== x2)[0][0]   ## x coordinate: x1, y coordinate: x2, z coordinate : x3 
        if m == 0: 
            start_node  = org_btnodes[ix]
            continue 
        modelgauges.append([start_node[x], org_btnodes[ix][x], start_node[y], org_btnodes[ix][y]])
        start_node = org_btnodes[ix]

    modelgauges = np.array(modelgauges)

    # border_width = pmax - GaugeConstantRange
    ########################################################################################

    
    nodes_solids = pattern_solid[:, 1: 9]
    nodes_solids = nodes_solids.reshape(-1)
    nodes_solids = np.unique(nodes_solids)
    nodes_solids = np.setdiff1d(nodes_solids, nodes_btm)   ## nodes except bottom surface 
    print ("* GD adjusted after %.2fmm from center"%(GaugeConstantRange*1000))
    pnodes, fix, start = Pattern_Gauge_ratio_adjustment(section, nodes_solids, pattern_solid, pattern_nodes, pattern_org_nodes, modelgauges, GaugeConstantRange, fix=0,   start=GaugeConstantRange, xy=xy,  mg=mg, TargetR=R, ModelR=PR)
    # if fix == 1: 
    #     print ("** Groove Depth ratio adjusted after half width %.2fmm from center"%(start*1000))
    #     pnodes, _,   _ = Pattern_Gauge_ratio_adjustment(section, nodes_solids, pattern_solid, pattern_nodes, pattern_org_nodes, modelgauges, GaugeConstantRange, fix=fix, start=start, xy=xy, mg=mg, TargetR=R, ModelR=PR)

    for n in btmnodes:   ## add bottom nodes 
        pnodes.append(n)   
    pnodes = np.array(pnodes)                                     
    ### All Tread Solids > define CTB 

    Elset = ["CTB", pattern_solid[:,0]]
    elsets=[]  # Elset_SUT = ["SUT", []]
    elsets.append(Elset)
    
    sidenode_checking = 1 
    ############################################################################
    ## pattern side node gauge check (the same ratio to the model)
    ###############################################################################
    if sidenode_checking == 1: 
        try: 
            nodes_side=surf_ptnside_pos[:,7:]
        except:
            nodes_side=[]
            for sf in surf_ptnside_pos: 
                try: 
                    # print (sf[7:])
                    nodes_side.append(sf[7])
                    nodes_side.append(sf[8])
                    nodes_side.append(sf[9])
                    nodes_side.append(sf[10])
                except:
                    print (" #### >> ", sf)
                    sys.exit()
                
            nodes_side = np.array(nodes_side)


        nodes_side = np.unique(nodes_side)
        on =[]; nn = []
        for nd in nodes_side: 
            ix = np.where(pattern_org_nodes[:,0]==nd)[0][0]
            on.append(pattern_org_nodes[ix])
            ix = np.where(pnodes[:,0]==nd)[0][0]
            nn.append(pnodes[ix])
        on = np.array(on)
        nn = np.array(nn)
        t=np.max(on[:,3])
        b=np.min(on[:,3])
        H = t - b 

        tc = np.max(nn[:,3])
        bc = np.min(nn[:,3])
        lc = tc - bc 

        # print ("       R=%.3f, min ht of side=%.3f, dif=%.3f"%(R*1000, bc*1000, lc*1000) )
        # print (" Model R=%.3f, min ht of side=%.3f, dif=%.3f"%(t*1000,  b*1000, H*1000) )

        for nd in nodes_side: 
            ix = np.where(on[:,0]==nd)[0][0]
            h = t - on[ix][3] 

            ix = np.where(pnodes[:,0]==nd)[0][0]
            pnodes[ix][3] = tc - lc / H * h 

        ########################################################################
        try: 
            nodes_side=surf_ptnside_neg[:,7:]
        except:
            nodes_side=[]
            for sf in surf_ptnside_neg: 
                try: 
                    nodes_side.append(sf[7])
                    nodes_side.append(sf[8])
                    nodes_side.append(sf[9])
                    nodes_side.append(sf[10])
                except:
                    print (" #### >> ", sf)
                    sys.exit()
                
            nodes_side = np.array(nodes_side)


        nodes_side = np.unique(nodes_side)
        on =[]; nn = []
        for nd in nodes_side: 
            ix = np.where(pattern_org_nodes[:,0]==nd)[0][0]
            on.append(pattern_org_nodes[ix])
            ix = np.where(pnodes[:,0]==nd)[0][0]
            nn.append(pnodes[ix])
        on = np.array(on)
        nn = np.array(nn)
        t=np.max(on[:,3])
        b=np.min(on[:,3])
        H = t - b 

        tc = np.max(nn[:,3])
        bc = np.min(nn[:,3])
        lc = tc - bc 
        # print ("       R=%.3f, min ht of side=%.3f, dif=%.3f"%(R*1000, bc*1000, lc*1000) )
        # print (" Model R=%.3f, min ht of side=%.3f, dif=%.3f"%(t*1000,  b*1000, H*1000) )

        for nd in nodes_side: 
            ix = np.where(on[:,0]==nd)[0][0]
            h = t - on[ix][3] 

            ix = np.where(pnodes[:,0]==nd)[0][0]
            pnodes[ix][3] = tc - lc / H * h 

    return pnodes,  elsets

def NodesOnSolids(npn, pattern_solid): 
    nodes_solids = pattern_solid[:, 1: 9]
    nodes_solids = nodes_solids.reshape(-1)
    nodes_solids = np.unique(nodes_solids)
    nodes = []
    for ni in nodes_solids:
        ix = np.where(npn[:,0]==ni)[0]
        if len(ix) ==1:      nodes.append(npn[ix[0]])

    return np.array(nodes)

def BendingSquarePattern(OD=0.0, profiles=[], curves=[], nodes=[], xy=23): 
    x = int(xy/10); y = int(xy%10)
    prf = []
    print ("\n## Bending Pattern - Positive side profile")
    lsum = 0 
    if profiles[-1][0] < 0: del(profiles[-1])
    for pf in profiles:
        if len(pf)  ==2: 
            lsum += pf[1]
            pf.append(lsum)
        if pf[0] < 10.0:  print (" R=%7.1f, Length=%6.2f(~%.2f)"%(pf[0]*1000, pf[1]*1000, pf[2]*1000))
        else:             
            print ("       LINE, Length=%6.2f(~%.2f)"%(pf[1]*1000, pf[2]*1000))

    

    N = len(profiles)
    profiles[-1][1] += 0.5 
    profiles[-1][2] += 0.5 

    bended = []
    mg = 0.1e-3 
    for i, nd in enumerate(nodes): 
        px = 0.0
        py = 0.0 
        deformed = [nd[0], nd[1], nd[2], nd[3]]
        if abs(nd[2]) < mg : 
            px = nd[x]; py=nd[y]
        else: 
            npf = 0; f=0 
            negR = 0 
            for i, pf in enumerate(profiles): 
                if pf[0]<0: 
                    negR = 1 
                if i == 0: 
                    if abs(nd[x]) <= pf[2]: 
                        npf = i
                        f = 1 
                        break 
                else: 
                    if profiles[i-1][2] < abs(nd[x])  and abs(nd[x]) <= pf[2] : 
                        npf = i 
                        f = 1 
                        break 
            
            curve=curves[npf]
            if f ==0: 
                npf = len(profiles)  -1 
                curve = curves[-1]

            if npf ==0:    s_length = 0 
            else:          s_length = profiles[npf-1][2]

            sx = round(curves[npf][0][x], 9); sy = round(curves[npf][0][y], 9)
            ex = round(curves[npf][1][x], 9); ey = round(curves[npf][1][y], 9)
            cx = round(curves[npf][2][x], 9); cy = round(curves[npf][2][y], 9)
            r = profiles[npf][0]
            del_l = abs(nd[x]) - s_length 
            # if del_l > profiles[npf][1]: 
            #     print ("%d, x=%.1f, Curve L=%.3f, Del=%.3f"%(npf, nd[x]*1000, profiles[npf][1]*1000, del_l*1000))
            h = OD/2.0 - nd[y] 

            if negR == 0: 

                A = abs(asin((sx-cx)/r)) + del_l / r # A0 = atan((sx-cx)/(sy-cy)) angle of the curve start,  del_A  = del_l / r 
                
                if curve[1][x] < 0: A *= -1 
                
                px = round(cx + (r-h) * sin(A), 9)
                py = round(cy + (r-h) * cos(A), 9)
            else: 
                if r < 0: r = -r 
                A = asin((cy - sy)/r) + del_l / r 
                px = cx - (r+h) * cos(A)
                py = cy - (r+h) * sin(A)


        # if py > OD/2 or r < 0 : 
            # print (" curve R=,%.6f, flat X=,%.6f, Ht=,%.6f, bended x=,%.6f, y=,%.6f, angle=,%.3f, sx=,%.6f, sy=,%6f, cx=,%.6f, cy=,%.6f"%(r, nd[x], h, px, py, degrees(A), sx,sy, cx, cy))
            # print ("del L, %.6f, Del Angle, %.3f, start Angle=%.3f"%(del_l, degrees(del_l / r ), degrees(asin((cy - sy)/r)) ))


        if nd[2]>0: deformed[x] = px 
        else: deformed[x] = -px 
        deformed[y] = py 
        bended.append(deformed)

    return np.array(bended)

def BendingPattern(OD=0.0, Rprofiles=[], Rcurves=[], Lprofiles=[], Lcurves=[], nodes=[], xy=23):  ## target profile information (OD, Profile, scaled nodes) Left : negative, Right : Positivie 
    x = int(xy/10); y = int(xy%10)
    lsum = 0 
    for i, pf in enumerate(Rprofiles): 
        lsum += pf[1]
        Rprofiles[i].append(lsum)
    L_sho=[]
    lsum = 0 
    for i, pf in enumerate(Lprofiles): 
        lsum += pf[1]
        Lprofiles[i].append(lsum)
    print ("\n## Bending Pattern - Positive side profile")
    # print (" * Crown Profile (Positive)")
    for i, pf in enumerate(Rprofiles): 
        print (" %d, R=%7.1f, Length=%6.2f(~%.2f)"%(i+1, pf[0]*1000, pf[1]*1000, pf[2]*1000))

    bended = []
    mg = 0.1E-03

    Rsho_nodes=[]
    Lsho_nodes=[]

    # allx=[]; ally=[]
    # ox = []; oy =[] 
    # lns = []; defm=[]
    for i, nd in enumerate(nodes): 
        px = 0.0
        py = 0.0 
        deformed = [nd[0], nd[1], nd[2], nd[3]]

        if nd[x] >= mg: 
            # print (" Right SIDE", Rcurves[3])
            profiles = Rprofiles
            curves = Rcurves
        elif nd[x] <= -mg: 
            # print (" LEFT SIDE")
            profiles = Lprofiles
            curves = Lcurves 
        else: 
            px = nd[x]
            py = nd[y]

        if abs(nd[x]) > mg: 

            npf = 0; f=0 
            for i, pf in enumerate(profiles): 
                if i == 0: 
                    if abs(nd[x]) <= pf[2]: 
                        npf = i
                        f = 1 
                        break 
                else: 
                    if profiles[i-1][2] < abs(nd[x])  and abs(nd[x]) <= pf[2] : 
                        npf = i 
                        f = 1 
                        break 
            curve=curves[npf]
            if f ==0: 
                N = len(profiles) 
                curve = curves[N-1]
                npf = N -1 

            if npf ==0:    s_length = 0 
            else:          s_length = profiles[npf-1][2]

            sx = round(curves[npf][0][x], 9); sy = round(curves[npf][0][y], 9)
            ex = round(curves[npf][1][x], 9); ey = round(curves[npf][1][y], 9)
            cx = round(curves[npf][2][x], 9); cy = round(curves[npf][2][y], 9)
            r = profiles[npf][0]
            del_l = abs(nd[x]) - s_length 
            # if del_l > profiles[npf][1]: 
            #     print ("%d, x=%.1f, Curve L=%.3f, Del=%.3f"%(npf, nd[x]*1000, profiles[npf][1]*1000, del_l*1000))
            h = OD/2.0 - nd[y] 

            # if h< 0.5E-03: 
            #     ox.append(nd[x]); oy.append(nd[y])

            if abs((sx-cx)/r) > 1.0: 
                print ("R Curves")
                Print_list(Rcurves)
                print ("L Curves")
                Print_list(Lcurves)
                print ("-----------------------------------------------------------------------")
                print ("nodeposition Y=%.3f, del_l=%.3f, r=%.3f"%(nd[x]*1000, del_l*1000, r*1000))
                print ("Start x=%.3f, y=%.3f, Center x=%.3f, y=%.3f, End x=%.3f, y=%.3f"%(sx*1000, sy*1000, cx*1000, cy*1000, ex*1000, cy*1000))
                print ("sx - cx = %.6e, (sx-cx)/r=%.3f"%((sx-cx), (sx-cx)/r))
                print ("Profiles...")
                Print_list(profiles)
                print ("Curves...")
                Print_list(curves)
            
            A = abs(asin((sx-cx)/r)) + del_l / r # A0 = atan((sx-cx)/(sy-cy)) angle of the curve start,  del_A  = del_l / r 
               
            if curve[1][x] < 0: A *= -1 
            
            lx = round(cx + r * sin(A), 9)
            ly = round(cy + r * cos(A), 9)

            M = (ly - cy) / (lx - cx)
            if lx >= 0: px = lx - h / sqrt(1+M*M)
            else:       px = lx + h / sqrt(1+M*M)
            py = M * px - M * lx +  ly 
        
        deformed[x] = px 
        deformed[y] = py 
        # if h< 0.5E-03: 
        #     allx.append(px); ally.append(py)
        #     lns.append([[nd[x], px], [nd[y], py]])
        #     defm.append(deformed)
        bended.append(deformed)
        # if  py > nd[y]: #px < 0.01E-3: 
        #     print ("\n Start=(%.2f, %.2f), End=(%.2f, %.2f), Center=(%.2f, %.2f)"%(sx*1000, sy*1000, ex*1000, ey*1000, cx*1000, cy*1000))
        #     print (" Radius=%.2f, del_Dist=%.2f, height=%.2f"%(r*1000, del_l*1000, h*1000))
        #     print (" M=%.2f, px=%.2f, py=%.2f, Initial Node position x=%.2f, y=%.2f"%(M, px*1000, py*1000, nd[x]*1000, nd[y]*1000))
        #     print (" lx=%.3f, ly=%.3f"%(lx*1000, ly*1000))
        #     print (" Initial Angle=%.2f, del angle=%.2f"%(degrees(atan((sx-cx)/(sy-cy))), degrees(del_l/r)))
        #     print (" Profile OD=%.2f (R=%.2f)"%(OD*1000, OD*500))
    bended = np.array(bended)


    # plt.scatter(ox, oy, c='gray', s=0.5)
    # plt.scatter(allx, ally, c='red', s=2.0)
    # for ln in lns: 
    #     plt.plot(ln[0], ln[1], color="red", linewidth=0.1)

    # for x, y in zip(ox, oy): 
    #     allx.append(x)
    #     ally.append(y)

    # alx = np.array(allx)
    # aly = np.array(ally)
    # plt.xlim(np.min(alx), np.max(alx))
    # plt.ylim(np.min(aly), np.max(aly))
    # plt.axis('equal')

    # plt.savefig("shouldernodes.png", dpi=500)


    return bended#, defm, lns
def ShoulderTreadGa(OD, profiles, curves, layout_btm_nodes, TDW, shoR=0, xy=23):
    x = int(xy/10); y = int(xy%10)

    mga= 0 

    R_sho=[]
    R = OD/2.0 
    lsum = 0 
    tmp = 0 
    for i, pf in enumerate(profiles): 
        lsum += pf[1]
        profiles[i].append(lsum)
        if round(pf[0], 4) == round(shoR, 4) and shoR > 0.0 : tmp=i 
    if tmp > 0:    ## Rcurves = [Curve start point(node), curve end point(node), curve center point]
        R_sho= [profiles[tmp-1][2], profiles[tmp][2], curves[tmp][0], curves[tmp][1], curves[tmp][2]]
    
        btm =  layout_btm_nodes 
        
        gauges = []
        for bn in btm:  ## shoulder max gauge at the positive side,   R_sho= [Rprofiles[i-1][2], Rprofiles[i][2], Rcurves[i][0], Rcurves[i][1], Rcurves[i][2] ]
            if R_sho[0]>=bn[x] and R_sho[1]<=bn[x] : 
                gauges.append([R-bn[y]]) 
        if len(gauges) == 0: 
            dist = 10E10
            for bn in btm:
                if abs(R_sho[0] - bn[x]) < dist and bn[x] < R_sho[0]: 
                    dist = abs(R_sho[0] - bn[x])
                    mga = R - bn[y]
        else:
            ga = np.array(gauges)
            mga = np.max(ga)

    return mga 

def AttatchBottomNodesToBody(bodynodes=[], bodyelements=[], ptnnodes=[], ptnbottom=[], start=0, shoulder='R',\
    ): 
    btnodes = ptnbottom[:,7:]
    btnodes = np.unique(btnodes)
    btm = []
    for nd in btnodes: 
        if nd>0: 
            ix = np.where(ptnnodes[:,0]==nd)[0][0]
            if abs(ptnnodes[ix][2]) >= start :
                btm.append(ptnnodes[ix])
    btm = np.array(btm)

    edges = bodyelements.OuterEdge(bodynodes)


    outer = EDGE()
    for edge in edges.Edge: 
        # print ("%d, %d - %d"%(edge[0], edge[1], edge[4]))
        if edge[2] != "IL1" and edge[2] != "RIC" and edge[2] != "HUS" and edge[2] != "L11" : 
            outer.Add(edge)
    outer.Sort()
    npn = np.array(bodynodes.Node)

    icenter = 0 
    for i, edge in enumerate(outer.Edge): 
        ix = np.where(npn[:,0]==edge[0])[0][0]
        if abs(npn[ix][2]) < 0.1E-03: 
            icenter = i 
            break 

    margin = 2.094395 ## = radians(120)
    N = len(outer.Edge)
    Base = EDGE()
    base = []
    for i in range(icenter, N): 
        ix = np.where(npn[:,0]==outer.Edge[i-1][0])[0][0];       n1 = npn[ix]
        ix = np.where(npn[:,0]==outer.Edge[i-1][1])[0][0];       n2 = npn[ix]
        ix = np.where(npn[:,0]==outer.Edge[i][1])[0][0];         n3 = npn[ix]
        an = Angle_3nodes(n1, n2, n3) 
        if shoulder =='R':
            if an < margin and n2[3] < n3[3]: 
                # print ("#End of TD left (%d,%d,%d)=%.2f degree"%(n1[0], n2[0], n3[0], degrees(an)))
                break 
        else:
            if an < margin*1.1 : 
                # print ("#End of TD left (%d,%d,%d)=%.2f degree"%(n1[0], n2[0], n3[0], degrees(an)))
                break 
        Base.Add(outer.Edge[i])
        base.append([n2, n3])
        # print (" - %d, %d (%.3f~%.3f) "%(n2[0], n3[0], n2[2]*1000, n3[2]*1000))


    for i in range(icenter-1, -1, -1): 
        ix = np.where(npn[:,0]==outer.Edge[i+1][1])[0][0];       n1 = npn[ix]
        ix = np.where(npn[:,0]==outer.Edge[i+1][0])[0][0];       n2 = npn[ix]
        ix = np.where(npn[:,0]==outer.Edge[i][0])[0][0];         n3 = npn[ix]
        an = Angle_3nodes(n1, n2, n3) 
        if shoulder =='R':
            if an < margin and n2[3] < n3[3]: 
                # print ("#End of TD right (%d,%d,%d)=%.2f degree"%(n1[0], n2[0], n3[0], degrees(an)))
                break 
        else:
            if an < margin*1.1 : 
                # print ("#End of TD left (%d,%d,%d)=%.2f degree"%(n1[0], n2[0], n3[0], degrees(an)))
                break 
        Base.Add(outer.Edge[i])
        base.append([n2, n3])
        # print (" - %d, %d (%.3f~%.3f) "%(n2[0], n3[0], n2[2]*1000, n3[2]*1000))

    # sh = 0 
    for nd in btm: 
        # if nd[0] == 4282+10**7 or nd[0] == 4355 + 10**7 : sh = 1
        # else: sh = 0 
        fd = 0 
        for bs in base: 
            dist, cn = DistanceFromLineToNode2D(nd, nodes=bs, xy=23)
            if cn[2]*nd[2] < 0: continue
            # if dist < 0.05e-3 : 
            #     fd = 1
            #     break  
            if bs[0][3] > bs[1][3]: 
                up=bs[0][3]; down=bs[1][3]
            else: 
                up=bs[1][3]; down=bs[0][3]

            if bs[0][2] > bs[1][2]: 
                lt=bs[1][2]; rt = bs[0][2]
            else: 
                lt=bs[0][2]; rt = bs[1][2]

            # if sh == 1: print (" %d (%.2f,%.2f)> (%.2f,%.2f)- (%.2f,%.2f)/(%.2f,%.2f)"%(nd[0]-10**7, nd[2]*1000, nd[3]*1000, cn[2]*1000, cn[3]*1000, bs[0][2]*1000, bs[1][2]*1000, down*1000, up*1000))
            if cn[2] >= lt and cn[2] <= rt and down<=cn[3] and cn[3] <=up: 
                # if sh == 1: print (" **************** MATCH")               
                fd = 1 
                ix = np.where(ptnnodes[:, 0] == nd[0])[0][0]
                ptnnodes[ix][2] = cn[2]
                ptnnodes[ix][3] = cn[3]
                break
        if fd == 0: 
            # print (">> %d, %.3f, %.3f"%(nd[0]-10**7, nd[2]*1000, nd[3]*1000))
            mdist = 10e10
            md = base[0][0]
            for i, bs in enumerate(base): 
                # print ("** %d, %.3f, %.3f "%(bs[1][0], bs[1][2]*1000, bs[1][3]*1000))
                if i ==0 : 
                    mdist  = sqrt((bs[0][2]-nd[2])**2 + (bs[0][3]-nd[3])**2)
                    md = bs[0]

                dist = sqrt((bs[1][2]-nd[2])**2 + (bs[1][3]-nd[3])**2)
                if dist < mdist: 
                    mdist = dist 
                    md = bs[1]
                    # if dist < 0.01: print ("     %d, %.3f, %.3f, d=%.3f"%(bs[1][0], bs[1][2]*1000, bs[1][3]*1000, dist*1000))
            ix = np.where(ptnnodes[:, 0] == nd[0])[0][0]
            ptnnodes[ix][2] = md[2]
            ptnnodes[ix][3] = md[3]
            
    return ptnnodes
def BendintPatternInCircumferentialDirection(nodes, OD): 
    R = OD/2.0 

    bended = []
    for i, nd in enumerate(nodes):
        r = nd[3]
        theta = nd[1] /R
        bended.append([nd[0], r  * sin(theta), nd[2], r  * cos(theta),  r,  theta])
    return np.array(bended)
def GenerateFullPatternMesh(nodes, solids, pn, OD, surf_pitch_up, surf_pitch_down, surf_free=[], \
    surf_btm=[], surf_side=[], elset=[], offset=10000, pl=0, ptn_org=[], ptn_pl=0, pd=[], rev=False): # pn: the number of pitches, 
    ## the nodes should have its radius for the processing speed.
    # pn : pitch number, OD : Tire OD (target) 
    # surf_side = [neg_pitch_side, pos_pitch_side]
    PI = 3.14159265358979323846

    if len(elset) == 0: 
        Elset = ["CTB", solids[:,0]]
        elsets=[]  # Elset_SUT = ["SUT", []]
        elsets.append(Elset)

    if len(surf_pitch_up) != len(surf_pitch_down): 
        print ("## The numbers of pitch up and down surfaces are different.")
        # sys.exit()


    ups=[]; downs=[]
    if rev == False: 
        for i, sf in enumerate(surf_pitch_up): 
            ups.append(sf[7]); ups.append(sf[8]); ups.append(sf[9])
            downs.append(surf_pitch_down[i][7]); downs.append(surf_pitch_down[i][8]); downs.append(surf_pitch_down[i][9])
            if sf[10] > 0: 
                ups.append(sf[10])
                downs.append(surf_pitch_down[i][10])
    else: 
        for i, sf in enumerate(surf_pitch_down): 
            ups.append(sf[7]); ups.append(sf[8]); ups.append(sf[9])
            downs.append(surf_pitch_up[i][7]); downs.append(surf_pitch_up[i][8]); downs.append(surf_pitch_up[i][9])
            if sf[10] > 0: 
                ups.append(sf[10])
                downs.append(surf_pitch_up[i][10])
    ups = np.array(ups);  downs=np.array(downs)
    ups = np.unique(ups); downs = np.unique(downs)

    # print ("* Nodes Up/Down Surface [%d,%d] (=%d)"%(len(ups), len(downs), len(surf_pitch_up)*4))
    
    couple=[]
    mg = 0.15E-03 
    origin=ptn_org
    for up in ups: 
        ix = np.where(origin[:,0]==up)[0][0]; un=origin[ix]
        for dw in downs: 
            ix = np.where(origin[:,0]==dw)[0][0]; dn=origin[ix]
            if abs(un[2] - dn[2]) < mg and abs(un[3] - dn[3]) < mg and abs(un[1] - dn[1] - ptn_pl)  < mg: 
                couple.append([un[0], dn[0]])
                # print ("CPLE: %d, %d"%(un[0]-10**7, dn[0]-10**7))
                break

    print ("* Unique Nodes Up/Down Surface[%d,%d] \n -> Found matches=%d"%(len(ups), len(downs), len(couple)))

    ups = []
    mched_nodes=[]
    for i, cp in enumerate(couple): 
        ix = np.where(nodes[:,0] == cp[0])[0]
        # if len(ix) ==0: 
        #     line = "not found to del %8d, %.6f, %.6f, %.6f >> r = %.6f"%(tnodes[ix][0],tnodes[ix][1], tnodes[ix][2],tnodes[ix][3],  r)
        #     print (line)
        for j, x in enumerate(ix): 
            ups.append(nodes[x][0])
            N = len(nodes)
            mched_nodes.append(nodes[x])
            nodes = np.delete(nodes, x, axis=0)
            # print (" %4d, %6d (%d/%d).. %6d > %6d (%d)"%(i, nodes[x][0], j+1, len(ix), N, len(nodes), N - len(nodes)))
    ups = np.array(ups)
    deleted_nodes = np.array(couple)
    # print ("DELETING PITCH SURFACE")
    # if rev == True: print ("#### Pattern Reversed ... " )
    # else: print ("## Pattern is not reversed...")
    # print (deleted_nodes)
    mched_nodes = np.array(mched_nodes)

    delta = 2*PI / float(pn) 
    if pl >0: ## check the delta angle 
        Total_Length = pl * pn 
        Circumferential_length = PI * OD 
        
        print ("* The No. of pitches=%d\n* Unit PL=%.3fmm(angle = %.3fdeg)"%(pn, pl*1000, degrees(delta)))
        print ("* All Pitch Length = %.3fmm\n* Tire Circumferential Length = %.3fmm"%(Total_Length*1000, Circumferential_length*1000))

    fullnodes=[]
    fullsolids=[]

    ##  r,  theta
    fnode = fullnodes.append 
    for i in range(int(pn)): 
        for nd in nodes: 
            temp = [nd[0] + offset * i, nd[4]*sin(nd[5]+delta*float(i)), nd[2], nd[4]*cos(nd[5]+delta*float(i))]
            # fullnodes.append(temp)
            fnode(temp)

    fnodes = np.array(fullnodes)
    fsolid = fullsolids.append 
    for sd in solids:
        
        ix1 = np.where(ups==sd[1])[0]
        ix2 = np.where(ups==sd[2])[0]
        ix3 = np.where(ups==sd[3])[0]
        ix4 = np.where(ups==sd[4])[0]
        ix5 = np.where(ups==sd[5])[0]
        ix6 = np.where(ups==sd[6])[0]
        ix7 = np.where(ups==sd[7])[0]
        ix8 = np.where(ups==sd[8])[0]

        for i in range(int(pn)): 
            if i < int(pn)-1: 
                if len(ix1) > 0 :   n1 = couple[ix1[0]][1] + offset * (i+1)
                else:               n1 = sd[1] + offset * i
                if len(ix2) > 0 :   n2 = couple[ix2[0]][1] + offset * (i+1)
                else:               n2 = sd[2] + offset * i
                if len(ix3) > 0 :   n3 = couple[ix3[0]][1] + offset * (i+1)
                else:               n3 = sd[3] + offset * i
                if len(ix4) > 0 :   n4 = couple[ix4[0]][1] + offset * (i+1)
                else:               n4 = sd[4] + offset * i
                if len(ix5) > 0 :   n5 = couple[ix5[0]][1] + offset * (i+1)
                else:               n5 = sd[5] + offset * i
                if len(ix6) > 0 :   n6 = couple[ix6[0]][1] + offset * (i+1)
                else:               n6 = sd[6] + offset * i
                if len(ix7) > 0 :   n7 = couple[ix7[0]][1] + offset * (i+1)
                else:               n7 = sd[7] + offset * i
                if len(ix8) > 0 :   n8 = couple[ix8[0]][1] + offset * (i+1)
                else:               n8 = sd[8] + offset * i

            else: 
                if len(ix1) > 0 :   n1 = couple[ix1[0]][1] 
                else:               n1 = sd[1] + offset *i
                if len(ix2) > 0 :   n2 = couple[ix2[0]][1] 
                else:               n2 = sd[2] + offset *i
                if len(ix3) > 0 :   n3 = couple[ix3[0]][1] 
                else:               n3 = sd[3] + offset *i
                if len(ix4) > 0 :   n4 = couple[ix4[0]][1] 
                else:               n4 = sd[4] + offset *i
                if len(ix5) > 0 :   n5 = couple[ix5[0]][1] 
                else:               n5 = sd[5] + offset *i
                if len(ix6) > 0 :   n6 = couple[ix6[0]][1] 
                else:               n6 = sd[6] + offset *i
                if len(ix7) > 0 :   n7 = couple[ix7[0]][1] 
                else:               n7 = sd[7] + offset *i
                if len(ix8) > 0 :   n8 = couple[ix8[0]][1] 
                else:               n8 = sd[8] + offset *i

            # fullsolids.append([sd[0] + offset * i, n1, n2, n3, n4, n5, n6, n7, n8, sd[9]])
            fsolid([sd[0] + offset * i, n1, n2, n3, n4, n5, n6, n7, n8, sd[9]])
            
    
    fsolids = np.array(fullsolids)

    surf_XTRD1001=[]
    surf_YTIE1001=[]
    #  surf_pitch_up, surf_pitch_down, surf_free=[], surf_btm=[], surf_side=[],

    for sf in surf_pitch_up: 
        ix1 = np.where(surf_free[:,0] == sf[0])[0]
        ix2 = np.where(surf_free[:,1] == sf[1])[0]
        idx = np.intersect1d(ix1, ix2) 
        if len(idx) == 1: 
            surf_free = np.delete(surf_free, idx[0], 0)
    for sf in surf_pitch_down: 
        ix1 = np.where(surf_free[:,0] == sf[0])[0]
        ix2 = np.where(surf_free[:,1] == sf[1])[0]
        idx = np.intersect1d(ix1, ix2) 
        if len(idx) == 1: 
            surf_free = np.delete(surf_free, idx[0], 0)

    surf_to_body=[]
    for sf in surf_side[0]:  ## surf_side = [[surfaces in the neg. side], [surfaces in the pos. side]]
        #print("SIDE %d, Face=%d"%(sf[0]-10**7, sf[1]))
        ix1 = np.where(surf_free[:,0] == sf[0])[0]
        ix2 = np.where(surf_free[:,1] == sf[1])[0]
        idx = np.intersect1d(ix1, ix2) 
        if len(idx) == 1: 
            surf_to_body.append(sf)
    for sf in surf_side[1]:  ## surf_side = [[surfaces in the neg. side], [surfaces in the pos. side]]
        ix1 = np.where(surf_free[:,0] == sf[0])[0]
        ix2 = np.where(surf_free[:,1] == sf[1])[0]
        idx = np.intersect1d(ix1, ix2) 
        if len(idx) == 1: 
            surf_to_body.append(sf)
    for sf in surf_btm: 
        ix1 = np.where(surf_free[:,0] == sf[0])[0]
        ix2 = np.where(surf_free[:,1] == sf[1])[0]
        idx = np.intersect1d(ix1, ix2) 
        if len(idx) == 1: 
            surf_to_body.append(sf)

    for i in range(int(pn)): 
        for sf in surf_free: 
            surf_XTRD1001.append([sf[0]+offset*i, "S"+str(int(sf[1]))])
    for i in range(int(pn)): 
        for sf in surf_to_body: 
            surf_YTIE1001.append([sf[0]+offset*i, "S"+str(int(sf[1]))])
    
    elset3d=[]
    esed = elset3d.append 
    for sets in elset: 
        nos = []
        for i in range(int(pn)): 
            for no in sets[1]: 
                nos.append(no + offset * i)
                # if no == 1 + 10**7: print ("!!!!!!! #1: %s"%(no + offset * i))
        # elset3d.append([sets[0], nos])
        esed([sets[0], nos])


    return fnodes, fsolids, elset3d, surf_XTRD1001, surf_YTIE1001, deleted_nodes, mched_nodes
def GenerateFullBodyMesh(nodes, elements, elsets, surfaces=[], sectors=240, offset=10000, body_outer=[]): 
    PI = 3.14159265358979323846
    nodes3d = []
    delta = 2*PI / float(sectors) 

    el2n=[]; el3n=[]; el4n=[]
    for i in range(sectors): 
        f=float(i)
        for nd in nodes.Node:
            nodes3d.append([nd[0]+offset*i, nd[3]*sin(delta * f), nd[2], nd[3]*cos(delta*f)])

        for el in elements.Element: 
            en = el[0] + offset*i
            if i < sectors -1: 
                n1 = el[1] + offset*i
                n2 = el[2] + offset*i
                n3 = el[3] + offset*i
                n4 = el[4] + offset*i
                n5 = el[1] + offset*(i+1)
                n6 = el[2] + offset*(i+1)
                n7 = el[3] + offset*(i+1)
                n8 = el[4] + offset*(i+1)
            else: 
                n1 = el[1] + offset*i
                n2 = el[2] + offset*i
                n3 = el[3] + offset*i
                n4 = el[4] + offset*i
                n5 = el[1] 
                n6 = el[2] 
                n7 = el[3] 
                n8 = el[4] 
            if el[6] == 2: el2n.append([en, n1, n2, n6, n5])
            elif el[6] == 3: el3n.append([en, n5, n6, n7, n1, n2, n3])
            elif el[6] == 4: el4n.append([en, n5, n6, n7, n8, n1, n2, n3, n4])
    elset3d=[]
    for elset in elsets.Elset: 
        sets=[elset[0]]
        tmp = []
        for i in range(sectors): 
            for j, el in enumerate(elset): 
                if j==0: continue 
                tmp.append(el + offset*i)
        sets.append(tmp)
        elset3d.append(sets)
    
    surface3d = []
    for surf in surfaces.Surface: 
        surface = [surf[0]]
        tmp = []
        for i in range(sectors): 
            for j, sf in enumerate(surf): 
                if j==0: continue 
                tmp.append([sf[0]+offset*i, Change3DFace(sf[1])])
        surface.append(tmp)
        surface3d.append(surface)

    
    bodysurf=[]
    for i in range(sectors): 
        for edge in body_outer.Edge: 
            bodysurf.append([edge[4]+offset*i, Change3DFace(edge[3])])
    

    return nodes3d, el2n, el3n, el4n, elset3d, surface3d, bodysurf
def Write_SMART_PatternMesh(file="pattern.trd", nodes=[], elements=[], elsets=[], XTRD=[], YTIE=[],\
     ties=[], start=10000000, offset=10000, namechange=[0,0], abaqus=0, revPtn=False): 
    f = open(file, 'w')
    if abaqus ==0: 
        # print (" Pattern Offset=", offset)
        f.write("*TREADPTN_NIDSTART_NIDOFFSET_EIDSTART_EIDOFFSET= %d, %d, %d, %d\n"%(start, offset, start, offset))
    f.write("*NODE\n")
    for n in nodes: 
        f.write("%10d, %15.8E, %15.8E, %15.8E\n"%(n[0], n[1], n[2], n[3]))

    ix6 = np.where(elements[:,9]==6)[0]
    if len(ix6) > 0 : 
        f.write( "*ELEMENT, TYPE=C3D6\n")
        solid6 = elements[ix6]
        for s in solid6: 
            f.write("%10d, %10d, %10d, %10d, %10d, %10d, %10d\n"%(s[0], s[1], s[2], s[3], s[4], s[5], s[6]))

    ix8 = np.where(elements[:,9]==8)[0]
    if len(ix8) > 0 : 
        f.write("*ELEMENT, TYPE=C3D8R\n")
        solid8 = elements[ix8]
        for s in solid8: 
            f.write("%10d, %10d, %10d, %10d, %10d, %10d, %10d, %10d, %10d\n"%(s[0], s[1], s[2], s[3], s[4], s[5], s[6], s[7], s[8]))

    for elset in elsets: 
        if (elset[0] == 'CTR' or elset[0] =='CTB') and namechange[0] == 1: 
            f.write("*ELSET, ELSET=%s1\n"%(elset[0]))
        elif elset[0] == 'CTR' or elset[0] =='CTB': 
            f.write("*ELSET, ELSET=%s\n"%(elset[0]))

        if (elset[0] == 'UTR' or elset[0] =='SUT') and namechange[1] == 1: 
            f.write("*ELSET, ELSET=%s1\n"%(elset[0]))
        elif elset[0] == 'UTR' or elset[0] =='SUT': 
            f.write("*ELSET, ELSET=%s\n"%(elset[0]))

        for i, en in enumerate(elset[1]): 
            if i%15 == 14: 
                f.write("%10d\n"%(en))
            else: 
                f.write("%10d,"%(en))
            
        if i %15 !=14: 
            f.write("\n")
    if revPtn == False: 
        f.write("*SURFACE, TYPE=ELEMENT, NAME=XTRD1001\n")
        for sf in XTRD:
            f.write(" %10d, %s\n"%(sf[0], sf[1]))

        f.write("*SURFACE, TYPE=ELEMENT, NAME=YTIE1001\n")
        for sf in YTIE:
            f.write(" %10d, %s\n"%(sf[0], sf[1]))
    else:
        f.write("*SURFACE, TYPE=ELEMENT, NAME=XTRD1001\n")
        for sf in XTRD:
            if sf[1] =="S3": f.write(" %10d, %s\n"%(sf[0], "S5"))
            elif sf[1] =="S5": f.write(" %10d, %s\n"%(sf[0], "S3"))
            else: f.write(" %10d, %s\n"%(sf[0], sf[1]))

        f.write("*SURFACE, TYPE=ELEMENT, NAME=YTIE1001\n")
        for sf in YTIE:
            if sf[1] =="S3": f.write(" %10d, %s\n"%(sf[0], "S5"))
            elif sf[1] =="S5": f.write(" %10d, %s\n"%(sf[0], "S3"))
            else: f.write(" %10d, %s\n"%(sf[0], sf[1]))
    
    
    line = "*TIE, NAME=TBD2TRD, ADJUST=YES, POSITION TOLERANCE= 0.0001\n"
    line += " YTIE1001, TIREBODY\n"
    f.write(line)
    f.close()
    print ("\n## Full Pattern Mesh was created")
def Write_SMART_TireBodyMesh(file="tirebody.axi", nodes=[], el4=[], el6=[], el8=[], elsets=[], surfaces=[], surf_body=[],  ties=[], txtelset=[], start=1, offset=10000, abaqus=0, bodyonly=0): 
    f = open(file, 'w')
    if abaqus == 0: 
        f.write("*TIREBODY_NIDSTART_NIDOFFSET_EIDSTART_EIDOFFSET= %d, %d, %d, %d\n"%(start, offset, start, offset))
    f.write("*NODE\n")
    for n in nodes: 
        f.write("%9d, %16.6E, %16.6E, %16.6E\n"%(n[0], n[1], n[2], n[3]))

    if len(el4) > 0 : 
        f.write("*ELEMENT, TYPE=M3D4R\n")
        N = len(el4)
        i = 0 
        while i < N: 
            f.write("%10d, %10d, %10d, %10d, %10d\n"%(el4[i][0], el4[i][1], el4[i][2], el4[i][3], el4[i][4]))
            i += 1
    if len(el6) > 0 : 
        f.write("*ELEMENT, TYPE=C3D6\n")
        for s in el6: 
            f.write("%10d, %10d, %10d, %10d, %10d, %10d, %10d\n"%(s[0], s[1], s[2], s[3], s[4], s[5], s[6]))

    if len(el8) > 0 : 
        f.write("*ELEMENT, TYPE=C3D8R\n")
        for s in el8: 
            f.write("%10d, %10d, %10d, %10d, %10d, %10d, %10d, %10d, %10d\n"%(s[0], s[1], s[2], s[3], s[4], s[5], s[6], s[7], s[8]))
    bd1set = []; isbd1=0 
    for elset in elsets: 
        f.write("*ELSET, ELSET=%s\n"%(elset[0]))
        if elset[0] == "BD1": isbd1 = 1 
        for i, en in enumerate(elset[1]): 
            if elset[0] == "BEAD_R" or elset[0] == "BEAD_L" : bd1set.append(en)

            if i%15 == 14: 
                f.write("%10d\n"%(en))
            else: 
                f.write("%10d,"%(en))
        if i %15 !=14: 
            f.write("\n")
    if isbd1 == 0: 
        f.write("*ELSET, ELSET=BD1\n")
        for i, en in enumerate(bd1set): 
            if i%15 == 14: 
                f.write("%10d\n"%(en))
            else: 
                f.write("%10d,"%(en))
        if i %15 !=14: 
            f.write("\n")

    if bodyonly ==0:
        for surface in surfaces:
            if surface[0] == "CONT": continue 
            f.write("*SURFACE, TYPE=ELEMENT, NAME=%s\n"%(surface[0]))
            for sf in surface[1]:
                f.write(" %10d, %s\n"%(sf[0], sf[1]))
    else: 
        for surface in surfaces:
            f.write(line= "*SURFACE, TYPE=ELEMENT, NAME=%s\n"%(surface[0]))
            for sf in surface[1]:
                f.write(" %10d, %s\n"%(sf[0], sf[1]))
    f.write("*SURFACE, TYPE=ELEMENT, NAME=TIREBODY\n")
    for surf in surf_body: 
        f.write(" %10d, %s\n"%(surf[0], surf[1]))
    
    for tie in ties.Tie: # tie = [name, slave_surface, master_surface]
        f.write("*TIE, NAME=%s\n"%(tie[0]))
        f.write(" %s, %s\n"%(tie[1], tie[2]))
        
    f.close()
    print ("## Full 3D Body Mesh was created")
def PatternElsetDefinition(ptn_solid, ptn_node, layout_tread, layout_node, subtread=False, xy=23, btm=1, surf_btm=[]):
    x = int(xy/10); y=int(xy%10)

    STR = ELEMENT()
    iCTR = 0 
    for td in layout_tread.Element: 
        if td[5] == "SUT" or td[5] =="UTR": 
            STR.Add(td) 
        if td[5] == "CTR": 
            iCTR = 1 

    if subtread == False  : 
        if iCTR ==0: 
            Elset = ["CTB", ptn_solid[:,0]]
        else: 
            Elset = ["CTR", ptn_solid[:,0]]
        elsets=[]  # Elset_SUT = ["SUT", []]
        elsets.append(Elset)
        return elsets


    if btm ==1: 
        btmsolid = surf_btm[:, 0]
        allsolid = ptn_solid[:, 0]

        if iCTR ==0: 
            sut = ["SUT", btmsolid]
            ctb = ["CTB", np.setdiff1d(allsolid,  btmsolid)]
        else: 
            sut = ["UTR", btmsolid]
            ctb = ["CTR", np.setdiff1d(allsolid,  btmsolid)]
        elsets=[ctb, sut]  # Elset_SUT = ["SUT", []]
        return elsets 
    else: 
        lnode = STR.Nodes(node=layout_node) 
        str_outer = STR.OuterEdge(lnode)
        ln = np.array(layout_node.Node) 

        poly = []
        ix = np.where(ln[:, 0] == str_outer.Edge[0][0])[0][0]
        poly.append([ln[ix][x], ln[ix][y]])
        for edge in str_outer.Edge: 
            ix = np.where(ln[:, 0] == edge[1])[0][0]
            poly.append([ln[ix][x], ln[ix][y]])
        
        sutn=[]
        ctbn=[]
        for sol in ptn_solid: 
            cx = 0.0;  cy =0.0
            ix = np.where(ptn_node[:,0]==sol[1])[0][0]
            cx += ptn_node[ix][x]; cy += ptn_node[ix][y]
            ix = np.where(ptn_node[:,0]==sol[2])[0][0]
            cx += ptn_node[ix][x]; cy += ptn_node[ix][y]
            ix = np.where(ptn_node[:,0]==sol[3])[0][0]
            cx += ptn_node[ix][x]; cy += ptn_node[ix][y]
            ix = np.where(ptn_node[:,0]==sol[4])[0][0]
            cx += ptn_node[ix][x]; cy += ptn_node[ix][y]
            ix = np.where(ptn_node[:,0]==sol[5])[0][0]
            cx += ptn_node[ix][x]; cy += ptn_node[ix][y]
            ix = np.where(ptn_node[:,0]==sol[6])[0][0]
            cx += ptn_node[ix][x]; cy += ptn_node[ix][y]
            if sol[7] > 0: 
                ix = np.where(ptn_node[:,0]==sol[7])[0][0]
                cx += ptn_node[ix][x]; cy += ptn_node[ix][y]
                ix = np.where(ptn_node[:,0]==sol[8])[0][0]
                cx += ptn_node[ix][x]; cy += ptn_node[ix][y]

                cx = cx / 8.0 
                cy = cy / 8.0 
            else: 
                cx = cx / 6.0 
                cy = cy / 6.0 

            if IsPointInPolygon([cx, cy], poly) : 
                sutn.append(sol[0])
            else: 
                ctbn.append(sol[0])
        if iCTR ==0: 
            sut=["SUT", sutn]
            ctb=["CTB", ctbn] 
        else: 
            sut=["UTR", sutn]
            ctb=["CTR", ctbn] 
        ptn_elset = [sut, ctb]

        return ptn_elset 
def Creating_pattern_pitch(expanded_pattern, pattern, LProfile, RProfile, Lcurves, Rcurves, OD, GD, ptn_id=10**7, TDW=0.0, fname="",\
 PN=0, pitch_up=[], pitch_down=[], pitch_side_pos=[], pitch_side_neg=[], bottom_surf=[], top_free=[], revPtn=False): 

    npn = expanded_pattern.npn 
    nps = expanded_pattern.nps 
    free = expanded_pattern.Free_Surface_without_BTM
    
    Rangles=[]
    for crv in Rcurves:
        # print ("* ", crv[0], end=" : ")
        vert = [0, 0, crv[2][2], crv[2][3]+1.0]
        angle_start = Angle_3nodes(vert, crv[2], crv[0], xy=23)
        angle_end = Angle_3nodes(vert, crv[2], crv[1], xy=23)
        Rangles.append([angle_start, angle_end])
        # print ("*Angles start=%.3f, end=%.3f"%(degrees(angle_start), degrees(angle_end)))

    Langles=[]
    for crv in Lcurves:
        # print (crv[0], crv[1], crv[2], end=" : ")
        vert = [0, 0, crv[2][2], crv[2][3]+1.0]
        angle_start = Angle_3nodes(vert, crv[2], crv[0], xy=23)
        angle_end = Angle_3nodes(vert, crv[2], crv[1], xy=23)
        Langles.append([angle_start, angle_end])
        # print ("Angles start=%.3f, end=%.3f"%(degrees(angle_start), degrees(angle_end)))

    flatten = NODE()
    R = OD/2.0
    for n in npn: 
        if abs(n[2]) <= 0.01E03 : 
            flatten.Add([n[0], n[1], n[2], n[3]])
        else: 
            if n[2] > 0 : 
                lsum = 0.0
                cnt = 0 
                for pf, crv, cangle in zip(RProfile, Rcurves, Rangles):
                    vert = [0, 0, crv[2][2], crv[2][3]+1.0]
                    angle = Angle_3nodes(vert, crv[2], n, xy=23)
                    cnt += 1
                    if cnt < len(RProfile): 
                        if angle > cangle[0] and angle <= cangle[1]: 
                            del_length = pf[0] * (angle - cangle[0])
                            length = lsum + del_length ## distance from center 
                            height = R -  pf[0] + sqrt((crv[2][2]-n[2])**2 + (crv[2][3]-n[3])**2) 
                            flatten.Add([n[0], n[1],  length, height])
                            break 
                    else: 
                        del_length = pf[0] * (angle - cangle[0])
                        length = lsum + del_length ## distance from center 
                        height =  R -  pf[0] + sqrt((crv[2][2]-n[2])**2 + (crv[2][3]-n[3])**2) 
                        flatten.Add([n[0], n[1],length, height])
                        break 

                    lsum += pf[1] 
            else: 
                lsum = 0.0
                cnt = 0 
                n[2] *= -1
                for pf, crv, cangle in zip(LProfile, Lcurves, Langles):
                    # print ("\n*** ", -crv[1][2])
                    sx = -crv[0][2]
                    ex = -crv[1][2]
                    cx = -crv[2][2]
                    
                    vert = [0, 0, cx, crv[2][3]+1.0]
                    cent = [crv[2][0],crv[2][1], cx, crv[2][3]]
                    angle = Angle_3nodes(vert, cent, n, xy=23)
                    
                    cnt += 1
                    if cnt < len(LProfile): 
                        if angle > cangle[0] and angle <= cangle[1]: 
                            # print ("  current angle=%7.3f (Curve Start=%7.3f, end=%7.3f), profile R=%7.3f, curve start Y=%7.3f, end=%7.3f, nx=%7.3f"%(degrees(angle), degrees(cangle[0]), degrees(cangle[1]),  pf[0]*1000, sx*1000, ex*1000, n[2]*1000))
                            del_length = pf[0] * (angle - cangle[0])
                            length = lsum + del_length ## distance from center 
                            height = R -  pf[0] + sqrt((cx-n[2])**2 + (crv[2][3]-n[3])**2) 
                            flatten.Add([n[0], n[1],  -length, height])
                            break 
                    else: 
                        # print ("* current angle=%7.3f (Curve Start=%7.3f, end=%7.3f), profile R=%7.3f, curve start Y=%7.3f, end=%7.3f, nx=%7.3f"%(degrees(angle), degrees(cangle[0]), degrees(cangle[1]),  pf[0]*1000, sx*1000, ex*1000, n[2]*1000))
                        del_length = pf[0] * (angle - cangle[0])
                        length = lsum + del_length ## distance from center 
                        height =  R -  pf[0] + sqrt((cx-n[2])**2 + (crv[2][3]-n[3])**2) 
                        flatten.Add([n[0], n[1], -length, height])
                        break 
                    lsum += pf[1] 

    flatterned_sorted = flatten.Sort(item=0)

    f = open(fname, 'w')
    f.writelines("*PROFILE_SCALING : 0.001000\n")
    f.writelines("*HALF_DIAMETER : %.5f\n"%(R*1000))
    f.writelines("*CENTER_ANGLE  : 0.000000\n")
    f.writelines("*GROOVE_DEPTH  : %.3f\n"%(GD*1000))
    f.writelines("*TREAD_DESIGN_WIDTH : %.3f\n"%(TDW*1000))
    f.writelines("*PROFILE_LHS\n")
    for pf in LProfile: 
        f.writelines("%.5f, %.5f\n"%(pf[0]*1000, pf[1]*1000))    
    f.writelines("*PROFILE_RHS\n")
    for pf in RProfile: 
        f.writelines("%.5f, %.5f\n"%(pf[0]*1000, pf[1]*1000))    
    f.writelines("*PITCH_SCALING : 0.001000\n")
    f.writelines("*GUIDELINE_TOLERANCE : 0.500000\n")
    f.writelines("*PITCH_DEFINITION_FIRST\n")
    f.writelines("P1, 0, 0.000000, 0, P1_SOLID, P1_CENTER, P1_UPAFT, P1_LWAFT, P1_UPFWD\n")
    f.writelines("*PITCH_ARRAY_FIRST, EIDSTART=10000000, NIDSTART=10000000, EIDOFFSET=10000, NIDOFFSET=10000, ANGLE=180.0000, DIRECTION=CW\n")
    f.writelines("	1,	P1, %d\n"%(PN))  ## the No. of pitch
    f.writelines("*HEADING\n")
    f.writelines("**% ======================================================\n")
    f.writelines("**% Regenerated Pattern mesh from P3DM\n")
    f.writelines("**% ======================================================\n")
    f.writelines("*NODE\n")
    for n in flatten.Node: 
        f.writelines("%10d, %.7E, %.7E, %.7E\n"%(n[0]-ptn_id, n[1]*1000, n[2]*1000, n[3]*1000))
        # f.writelines("%10d, %.7E, %.7E, %.7E\n"%(n[0]-ptn_id, n[1], n[2], n[3]))
        # f.writelines("%10d, %.7E, %.7E, %.7E\n"%(n[0]-ptn_id, n[1]*1000, n[2]*1000, n[3]*1000))
    ## beam node need to be added. 

    idx = np.where(nps[:,7] == 0)[0]
    s6 = 0 
    if len(idx)> 0 : 
        s6 =1 
        f.writelines("*ELEMENT, TYPE=C3D6, ELSET=SOLID0\n")
        sol = nps[idx]
        for el in sol: 
            f.writelines("%6d, %6d, %6d, %6d, %6d, %6d, %6d\n"%(el[0]-ptn_id, el[1]-ptn_id, el[2]-ptn_id, el[3]-ptn_id, el[4]-ptn_id, el[5]-ptn_id, el[6]-ptn_id))
    idx = np.where(nps[:,7] > 0)[0]
    f.writelines("*ELEMENT, TYPE=C3D8, ELSET=SOLID1\n")
    sol = nps[idx]
    for el in sol: 
        f.writelines("%6d, %6d, %6d, %6d, %6d, %6d, %6d, %6d, %6d\n"%(el[0]-ptn_id, el[1]-ptn_id, el[2]-ptn_id, el[3]-ptn_id, el[4]-ptn_id, el[5]-ptn_id, el[6]-ptn_id, el[7]-ptn_id, el[8]-ptn_id))
    f.writelines("*ELSET,ELSET=ALLELEMENTS\n")
    if s6 ==1 :  f.writelines("SOLID0,\n")
    f.writelines("SOLID1,\n")

    if len(pitch_up)> 0 : 
        f.writelines("*SURFACE, TYPE=ELEMENT, NAME=PITCH_UP\n")
        for sf in pitch_up: 
            if revPtn == False:  f.writelines("%6d, S%d\n"%(sf[0]-ptn_id, sf[1]))
            else: 
                if sf[1] ==3: f.writelines("%6d, S%d\n"%(sf[0]-ptn_id, 5))
                elif sf[1] == 5: f.writelines("%6d, S%d\n"%(sf[0]-ptn_id, 3))
                else: f.writelines("%6d, S%d\n"%(sf[0]-ptn_id, sf[1]))
            ix1 = np.where(free[:,0] == sf[0])[0]
            ix2 = np.where(free[:,1] == sf[1])[0]
            idx = np.intersect1d(ix1, ix2) 
            if len(idx) == 1: 
                free = np.delete(free, idx[0], 0)

        

    if len(pitch_down)> 0 : 
        f.writelines("*SURFACE, TYPE=ELEMENT, NAME=PITCH_down\n")
        for sf in pitch_down: 
            if revPtn == False:  f.writelines("%6d, S%d\n"%(sf[0]-ptn_id, sf[1]))
            else: 
                if sf[1] ==3: f.writelines("%6d, S%d\n"%(sf[0]-ptn_id, 5))
                elif sf[1] == 5: f.writelines("%6d, S%d\n"%(sf[0]-ptn_id, 3))
                else: f.writelines("%6d, S%d\n"%(sf[0]-ptn_id, sf[1]))
            ix1 = np.where(free[:,0] == sf[0])[0]
            ix2 = np.where(free[:,1] == sf[1])[0]
            idx = np.intersect1d(ix1, ix2) 
            if len(idx) == 1: 
                free = np.delete(free, idx[0], 0)

    if len(pitch_side_pos)> 0 : 
        f.writelines("*SURFACE, TYPE=ELEMENT, NAME=PITCH_SIDE_POS\n")
        for sf in pitch_side_pos: 
            if revPtn == False:  f.writelines("%6d, S%d\n"%(sf[0]-ptn_id, sf[1]))
            else: 
                if sf[1] ==3: f.writelines("%6d, S%d\n"%(sf[0]-ptn_id, 5))
                elif sf[1] == 5: f.writelines("%6d, S%d\n"%(sf[0]-ptn_id, 3))
                else: f.writelines("%6d, S%d\n"%(sf[0]-ptn_id, sf[1]))
            ix1 = np.where(free[:,0] == sf[0])[0]
            ix2 = np.where(free[:,1] == sf[1])[0]
            idx = np.intersect1d(ix1, ix2) 
            if len(idx) == 1: 
                free = np.delete(free, idx[0], 0)

    if len(pitch_side_neg)> 0 : 
        f.writelines("*SURFACE, TYPE=ELEMENT, NAME=PITCH_SIDE_NEG\n")
        for sf in pitch_side_neg: 
            if revPtn == False:  f.writelines("%6d, S%d\n"%(sf[0]-ptn_id, sf[1]))
            else: 
                if sf[1] ==3: f.writelines("%6d, S%d\n"%(sf[0]-ptn_id, 5))
                elif sf[1] == 5: f.writelines("%6d, S%d\n"%(sf[0]-ptn_id, 3))
                else: f.writelines("%6d, S%d\n"%(sf[0]-ptn_id, sf[1]))
            ix1 = np.where(free[:,0] == sf[0])[0]
            ix2 = np.where(free[:,1] == sf[1])[0]
            idx = np.intersect1d(ix1, ix2) 
            if len(idx) == 1: 
                free = np.delete(free, idx[0], 0)
    if len(bottom_surf)> 0 : 
        f.writelines("*SURFACE, TYPE=ELEMENT, NAME=PITCH_BOTTOM\n")
        for sf in bottom_surf: 
            if revPtn == False:  f.writelines("%6d, S%d\n"%(sf[0]-ptn_id, sf[1]))
            else: 
                if sf[1] ==3: f.writelines("%6d, S%d\n"%(sf[0]-ptn_id, 5))
                elif sf[1] == 5: f.writelines("%6d, S%d\n"%(sf[0]-ptn_id, 3))
                else: f.writelines("%6d, S%d\n"%(sf[0]-ptn_id, sf[1]))
            ix1 = np.where(free[:,0] == sf[0])[0]
            ix2 = np.where(free[:,1] == sf[1])[0]
            idx = np.intersect1d(ix1, ix2) 
            if len(idx) == 1: 
                free = np.delete(free, idx[0], 0)

    if len(free)> 0 :
        f.writelines("*SURFACE, TYPE=ELEMENT, NAME=SELF_CONTACT\n")
        for sf in free: 
            if revPtn == False:  f.writelines("%6d, S%d\n"%(sf[0]-ptn_id, sf[1]))
            else: 
                if sf[1] ==3: f.writelines("%6d, S%d\n"%(sf[0]-ptn_id, 5))
                elif sf[1] == 5: f.writelines("%6d, S%d\n"%(sf[0]-ptn_id, 3))
                else: f.writelines("%6d, S%d\n"%(sf[0]-ptn_id, sf[1]))
    
    tns =[]
    tes = []
    if len(top_free)>0: 
        f.writelines("*SURFACE, TYPE=ELEMENT, NAME=TOP_SURFACE\n")
        for sf in top_free: 
            tns.append(sf[7]-ptn_id); tns.append(sf[8]-ptn_id); tns.append(sf[9]-ptn_id) 
            if sf[10]>=10**7: tns.append(sf[10]-ptn_id) 
            tes.append(sf[0]-ptn_id)
            if revPtn == False:  f.writelines("%6d, S%d\n"%(sf[0]-ptn_id, sf[1]))
            else: 
                if sf[1] ==3: f.writelines("%6d, S%d\n"%(sf[0]-ptn_id, 5))
                elif sf[1] == 5: f.writelines("%6d, S%d\n"%(sf[0]-ptn_id, 3))
                else: f.writelines("%6d, S%d\n"%(sf[0]-ptn_id, sf[1]))

    tns = np.array(tns)
    tns = np.unique(tns)
    f.writelines("*NSET, NSET=TOP_SURFACE\n")
    N = len(tns)-1
    for i, n in enumerate(tns): 
        if (i+1) %15 == 0: f.writelines(" %8d\n"%(n))
        else: 
            if i<N: f.writelines(" %8d, "%(n))
            else: f.writelines(" %8d\n"%(n))

    f.writelines("*ELSET, ELSET=TOP_SURFACE\n")
    N = len(tes)-1
    for i, n in enumerate(tes): 
        if (i+1) %15 == 0: f.writelines(" %8d\n"%(n))
        else: 
            if i<N: f.writelines(" %8d, "%(n))
            else: f.writelines(" %8d\n"%(n))
    
    f.close()

    return top_free, free

def Creating_tread_removed_layout(fname="", nodes=[], elements=[], elsets=[], surfaces=[], ties=[], treads=[], all_nodes=[]): 

    edge_body = elements.OuterEdge(all_nodes)
    edge_tread = treads.OuterEdge(all_nodes)
    npn = np.array(all_nodes.Node)

    interface = EDGE()
    for e1 in edge_body.Edge:
        for e2 in edge_tread.Edge: 
            if e1[0] == e2[1] or e1[1] == e2[0]:   # it's possible to find the edges with 2:1 element tie connection ... 
                interface.Add(e1) 
                break 
    nGroup, singles =HowManyEdgeGroup(interface.Edge)
    # print ("edge groups=%d"%(nGroup))
    # print ("nodes", singles)
    if nGroup > 1: 
        ## edge =>  n2 - n1 
        # print ("connecting edgess")
        ymax = 0
        ymin = 0 
        nmax = 0
        nmin = 0 
        for i, ed in enumerate(interface.Edge): 
            # n = all_nodes.NodeByID(ed[0]) 
            ix = np.where(npn[:,0] == ed[0])[0][0]; n = all_nodes[ix]
            # print(i, ed[0], n)
            if i == 0: 
                nmax = n[0] 
                nmin = n[0]
                ymax = n[2]
                ymin = n[2]
            else: 
                if ymax < n[2] : 
                    ymax = n[2]
                    nmax = n[0]
                if ymin > n[2]: 
                    ymin = n[2]
                    nmin = n[0]
        # print (" >>", nmin, nmax)
        # print (" <<", ymin, ymax) 


        for ed in interface.Edge: 
            if ed[0] == nmax: 
                sedge=ed 
                break 

        # print ("pos", sedge)

        f = 1 
        while f : 
            ix = NextEdge(sedge, edge_tread.Edge)
            sedge = edge_tread.Edge[ix]
            interface.Add(sedge) 
            # print (sedge)
            for ed in  interface.Edge: 
                if ed[0] == sedge[0] and ed[1] == sedge[1]: 
                    f = 0
                    break 

        for ed in interface.Edge: 
            if ed[1] == nmin: 
                sedge=ed 
                break 
        # print ("neg", sedge)

        f = 1 
        while f: 
            ix = PreviousEdge(sedge, edge_tread.Edge)
            sedge = edge_tread.Edge[ix]
            interface.Add(sedge) 
            # print (sedge)
            for ed in  interface.Edge: 
                if ed[0] == sedge[0] and ed[1] == sedge[1]: 
                    f = 0 
                    break 

    nGroup, singles =HowManyEdgeGroup(interface.Edge)
    # print ("edge groups=%d"%(nGroup))  
    interface.Sort()
    N = len(interface.Edge)
    if N > 1: 
        del(interface.Edge[N-1])
        del(interface.Edge[0])
    


    f = open(fname, "w")
    f.write("** TREAD REMOVED LAYOUT MESH BY P3DM\n")

    f.write("*NODE, SYSTEM=R\n")
    for nd in nodes.Node: 
        f.write("%6d, %10.6f, %10.6f, %10.6f\n"%(nd[0], nd[3], nd[2], nd[1]))
    f.write("*ELEMENT, TYPE=MGAX1\n")
    for el in elements.Element:
        if el[6] == 2: f.write("%6d, %6d, %6d\n"%(el[0], el[1], el[2]))
    f.write("*ELEMENT, TYPE=CGAX3H\n")
    for el in elements.Element:
        if el[6] == 3: f.write("%6d, %6d, %6d, %6d\n"%(el[0], el[1], el[2], el[3]))
    f.write("*ELEMENT, TYPE=CGAX4H\n")
    for el in elements.Element:
        if el[6] == 4: f.write("%6d, %6d, %6d, %6d, %6d\n"%(el[0], el[1], el[2], el[3], el[4]))
    isbd1 = 0 
    bd1set = []
    for eset in elsets.Elset: 
        ending = 0 
        for i, e in enumerate(eset): 
            if i ==0: 
                f.write("*ELSET, ELSET=%s\n"%(e))
                if e=="BD1": 
                    isbd1 = 1 
            else: 
                if eset[0] == "BEAD_R" or eset[0] == "BEAD_L": 
                    bd1set.append(e)

                f.write("%6d,"%(e))
                if i%10 ==0: 
                    f.write("\n")
                    ending = 1 
                else: 
                    ending = 0 
        if ending ==0: 
            f.write("\n")
    
    if isbd1 == 0: 
        ending = 0 
        f.write("*ELSET, ELSET=BD1\n")
        for e in bd1set: 
            f.write("%6d, "%(e))
            if i%10 ==0: 
                f.write("\n")
                ending = 1 
            else: 
                ending = 0 
        if ending ==0: 
            f.write("\n")
    

    for surf in surfaces.Surface: 
        if surf[0] == "CONT" : continue 
        ending = 0 
        for i, sf in enumerate(surf): 
            if i ==0: f.write("*SURFACE, TYPE=ELEMENT, NAME=%s\n"%(sf))
            else: 
                f.write(" %6d, %s\n"%(sf[0], sf[1]))

    for tie in ties.Tie: # tie = [name, slave_surface, master_surface]
        line = "*TIE, NAME=%s\n"%(tie[0])
        line += " %s, %s\n"%(tie[1], tie[2])
        f.write(line)

    f.write("*SURFACE, TYPE=ELEMENT, NAME=BODY2TREAD\n")
    for edge in interface.Edge: 
        f.write(" %6d, %s\n"%(edge[4], edge[3]))

    f.close()

    # print ("** Body_Mesh_Tread_Removed_%s.inp is created !!!"%(Profile.name))
    # print ("## Tread Removed layout mesh(-L1.inp) is created.")
    # print ("############################################")

def SolidComponents_checking(fname="Solid_Components.mat", trd='', axi='', return_value=0): 
    
    solids =[]
    cords =[]


    if trd: 
        with open(trd) as IN: 
            lines = IN.readlines()

       
        for line in lines: 
            if "**" in line : continue 
            if "*ELSET" in line: 
                if "ELSET=" in line: 
                    words  = line.split(",")
                    for word in words: 
                        if "*" in word: continue 
                        if "ELSET"  in word: 
                            name = word.split("=")[1]
                            name = name.strip().upper()
                            for mn in TireRubberComponents: 
                                if mn == name : 
                                    solids.append(name)
                            for mn in TireCordComponents: 
                                if mn == name : 
                                    cords.append(name)
    if axi: 
        with open(axi) as IN: 
            lines = IN.readlines()

        for line in lines: 
            if "**" in line : continue 
            if "*ELSET" in line: 
                if "ELSET=" in line: 
                    words  = line.split(",")
                    for word in words: 
                        if "*" in word: continue 
                        if "ELSET"  in word: 
                            name = word.split("=")[1]
                            name = name.strip().upper()
                            
                            for mn in TireRubberComponents: 
                                if mn == name : 
                                    solids.append(name)
                            for mn in TireCordComponents: 
                                if mn == name : 
                                    cords.append(name)
                        
    # f = open(fname, 'w')
    # f.write("*Rubber Components\n")
    
    i = 0
    while i < len(solids): 
        j = i +1
        while j < len(solids): 
            if solids[i] == solids[j]: 
                del(solids[j])
                j -= 1
            j += 1
        i += 1
        
    solids = sorted(solids)
    
    print ("* Continuum Components (%d EA)"%(len(solids)))
    for n in solids: 
        # f.write(" %s\n"%(n))
        print (" %s"%(n), end="  ")
    
    # f.write("\n*Membrane Components\n")
    i = 0
    while i < len(cords): 
        j = i +1
        while j < len(cords): 
            if cords[i] == cords[j]: 
                del(cords[j])
                j -= 1
            j += 1
        i += 1

    print ("\n* Structural Components (%d EA)"%(len(cords)))
    cords=sorted(cords)
    for n in cords: 
        # f.write(" %s\n"%(n))
        print (" %s"%(n), end="  ")

    # f.close()
    if return_value ==1: 
        return solids, cords 

def FricView_msh_creator(fname="", HalfOD=0.0, body_outer=[], body_node=[], body_offset=0, body_sector=0, profiles=[], curves=[],\
                          ptn_top=[],  ptn_free=[], ptn_npn=[], ptn_deleted_nodes=[], ptn_deleted=[], ptn_PN=0, ptn_PL=0.0, ptn_offset=0, shoulder="R", revPtn=False): 
    ## ]
    print ("\n* Generating 'FricView' input")
    if '.msh' in fname : 
        pass 
    elif "." in fname: 
        words = fname.split(".") 
        line = ''
        N = len(words)
        for i, word in enumerate(words): 
            if i != N-1 : line += word
        fname += ".msh"
    else: 
        fname += ".msh"

    flat_pattern_shift = 1.0 
    
    counting_surface = 0 

    f=open(fname, "w")
    f.write("*HOD: %.6f\n"%(HalfOD))
    f.write("*NODE_TIRE_BODY\n")
    #################################
    ## tire nodes
    #################################

    ndid = []
    for edge in body_outer.Edge:
        ndid.append(edge[0])
        ndid.append(edge[1])
    ndid = np.array(ndid)
    ndid = np.unique(ndid)
    bdn = np.array(body_node)

    bds = []
    for nid in ndid: 
        ix = np.where(bdn[:,0] == nid)[0][0]
        bds.append(bdn[ix])
    
    bds = np.array(bds)


    lines = ""
    PI = 3.14159265358979323846
    delta = 2*PI / float(body_sector) 
    for i in range(body_sector): 
        lf=float(i)
        for nd in bds:
            # lines +="%8d %15.6e %15.6e %15.6e\n"%( nd[0]+body_offset*i, nd[3]*sin(delta*lf), nd[2], nd[3]*cos(delta*lf) )
            f.write("%8d %15.6e %15.6e %15.6e\n"%( nd[0]+body_offset*i, nd[3]*sin(delta*lf), nd[2], nd[3]*cos(delta*lf) ))

    # f.write(lines)

    print ("    Body Nodes written.")

    #################################
    f.write("*MESH_TIRE_BODY\n")
    #################################
    ## tire body mesh
    #################################
    # bodysurf=[]
    # lines = ""

    for i in range(body_sector): 
        for edge in body_outer.Edge:
            counting_surface += 1 
            if i < body_sector -1:  
                f.write("%8d %9d %9d %9d %9d\n"%(counting_surface, edge[0]+ body_offset*(i+1),  edge[1]+ body_offset*(i+1), edge[1]+ body_offset*i, edge[0]+ body_offset*i ) )
                # lines += "%8d %9d %9d %9d %9d\n"%(counting_surface, edge[0]+ body_offset*(i+1),  edge[1]+ body_offset*(i+1), edge[1]+ body_offset*i, edge[0]+ body_offset*i ) 
            else: 
                f.write("%8d %9d %9d %9d %9d\n"%(counting_surface, edge[0],  edge[1], edge[1]+ body_offset*i, edge[0]+ body_offset*i) )
                # lines += "%8d %9d %9d %9d %9d\n"%(counting_surface, edge[0],  edge[1], edge[1]+ body_offset*i, edge[0]+ body_offset*i) 
    # f.write(lines)
    print ("    Body Mesh written")

    #################################
    ## pattern mesh  
    ## ptn_top=[],  ptn_free=[], ptn_npn=[], ptn_deleted_nodes=[deleted id, replaced id], ptn_PN=0, ptn_PL=0.0, ptn_offset=0
    #################################
    t0 = time.time()
    # f.write()
    # lines ="*MESH_PATTERN\n" 
    f.write("*MESH_PATTERN\n" )

    # ptn_surf = np.concatenate((ptn_top, ptn_free), axis=0)
    
    allnds = []
    for surf in ptn_top: 
        ix1 = np.where(ptn_deleted_nodes[:,0]==surf[7])[0]
        ix2 = np.where(ptn_deleted_nodes[:,0]==surf[8])[0]
        ix3 = np.where(ptn_deleted_nodes[:,0]==surf[9])[0]
        if surf[10] >= 10**7: ix4 = np.where(ptn_deleted_nodes[:,0]==surf[10])[0]
        for i in range(ptn_PN): 
            if i < ptn_PN-1: 
                if len(ix1) > 0: n1 = ptn_deleted_nodes[ix1[0]][1] + ptn_offset * (i+1)
                else:            n1 = surf[7] + ptn_offset * i 
                if len(ix2) > 0: n2 = ptn_deleted_nodes[ix2[0]][1] + ptn_offset * (i+1)
                else:            n2 = surf[8] + ptn_offset * i 
                if len(ix3) > 0: n3 = ptn_deleted_nodes[ix3[0]][1] + ptn_offset * (i+1)
                else:            n3 = surf[9] + ptn_offset * i 
                if surf[10] <10**7 :
                    n4 = n1 
                else: 
                    if len(ix4) > 0: n4 = ptn_deleted_nodes[ix4[0]][1] + ptn_offset * (i+1)
                    else:            n4 = surf[10] + ptn_offset * i 
            else : 
                if len(ix1) > 0: n1 = ptn_deleted_nodes[ix1[0]][1]
                else:            n1 = surf[7] + ptn_offset * i 
                if len(ix2) > 0: n2 = ptn_deleted_nodes[ix2[0]][1] 
                else:            n2 = surf[8] + ptn_offset * i 
                if len(ix3) > 0: n3 = ptn_deleted_nodes[ix3[0]][1] 
                else:            n3 = surf[9] + ptn_offset * i 
                if surf[10] <10**7 :
                    n4 = n1 
                else: 
                    if len(ix4) > 0: n4 = ptn_deleted_nodes[ix4[0]][1] 
                    else:            n4 = surf[10] + ptn_offset * i 
            
            allnds.append(n1); allnds.append(n2); allnds.append(n3); allnds.append(n4)
            counting_surface += 1 
            # lines += "%8d %9d %9d %9d %9d %9d %9d %9d %9d\n"%(counting_surface, n1, n2, n3, n4, i+1, 1, 1, 1)
            f.write( "%8d %9d %9d %9d %9d %9d %9d %9d %9d\n"%(counting_surface, n1, n2, n3, n4, i+1, 1, 1, 1))

    for surf in ptn_free: 
        ix1 = np.where(ptn_deleted_nodes[:,0]==surf[7])[0]
        ix2 = np.where(ptn_deleted_nodes[:,0]==surf[8])[0]
        ix3 = np.where(ptn_deleted_nodes[:,0]==surf[9])[0]
        if surf[10] >= 10**7: ix4 = np.where(ptn_deleted_nodes[:,0]==surf[10])[0]
        for i in range(ptn_PN): 
            if i < ptn_PN-1: 
                if len(ix1) > 0: n1 = ptn_deleted_nodes[ix1[0]][1] + ptn_offset * (i+1)
                else:            n1 = surf[7] + ptn_offset * i 
                if len(ix2) > 0: n2 = ptn_deleted_nodes[ix2[0]][1] + ptn_offset * (i+1)
                else:            n2 = surf[8] + ptn_offset * i 
                if len(ix3) > 0: n3 = ptn_deleted_nodes[ix3[0]][1] + ptn_offset * (i+1)
                else:            n3 = surf[9] + ptn_offset * i 
                if surf[10] <10**7 :
                    n4 = n1 
                else: 
                    if len(ix4) > 0: n4 = ptn_deleted_nodes[ix4[0]][1] + ptn_offset * (i+1)
                    else:            n4 = surf[10] + ptn_offset * i 
            else : 
                if len(ix1) > 0: n1 = ptn_deleted_nodes[ix1[0]][1]
                else:            n1 = surf[7] + ptn_offset * i 
                if len(ix2) > 0: n2 = ptn_deleted_nodes[ix2[0]][1] 
                else:            n2 = surf[8] + ptn_offset * i 
                if len(ix3) > 0: n3 = ptn_deleted_nodes[ix3[0]][1] 
                else:            n3 = surf[9] + ptn_offset * i 
                if surf[10] <10**7 :
                    n4 = n1 
                else: 
                    if len(ix4) > 0: n4 = ptn_deleted_nodes[ix4[0]][1] 
                    else:            n4 = surf[10] + ptn_offset * i 
            
            allnds.append(n1); allnds.append(n2); allnds.append(n3); allnds.append(n4)
            counting_surface += 1 
            if revPtn == False:     f.write( "%8d %9d %9d %9d %9d %9d %9d %9d %9d\n"%(counting_surface, n1, n2, n3, n4, i+1, 1, 0, 1))
            else:                   
                if surf[10] >=10**7:
                    if surf[1] < 2: f.write( "%8d %9d %9d %9d %9d %9d %9d %9d %9d\n"%(counting_surface, n4, n3, n2, n1, i+1, 1, 0, 1))
                    else:           f.write( "%8d %9d %9d %9d %9d %9d %9d %9d %9d\n"%(counting_surface, n2, n1, n4, n3, i+1, 1, 0, 1))
            # lines += "%8d %9d %9d %9d %9d %9d %9d %9d %9d\n"%(counting_surface, n1, n2, n3, n4, i+1, 1, 0, 1)
    # line_surface = lines 
    
    t2 = time.time()
    print ("    Pattern Mesh written (Δt=%.3f)"%(t2-t0))

    #################################
    #################################
    f.write("*NODE_PATTERN\n")
    ## profiles = [  [R1, L1], [R2, L2], ... ]
    ## curves   = [  [[Start 0, x, y, z], [End 0, x, y, z], [Center 0, x, y, z] ], .... ]
    ## Angles   = [  [start angle, end angle], [Start Angle, End Angle], ]
    ## lengths  = [ R1, R1+R2, R1+R2+R3, ...]
    ## sumlength(, lateral dist, vertical drop) = TD_Arc_length_calculator (profile, h_dist=??, totalwidth=0)  ## h_dist = horizental distance 


    Angles=[]
    for i, crv in enumerate(curves):
        vert = [0, 0, crv[2][2], crv[2][3]+1.0]
        angle_start = Angle_3nodes(vert, crv[2], crv[0], xy=23)
        angle_end = Angle_3nodes(vert, crv[2], crv[1], xy=23)

        if angle_start > PI/2.0: 
            delAngle = abs(angle_start - angle_end)
            angle_start = Angles[-1][1] 
            angle_end = angle_start + delAngle

        Angles.append([angle_start, angle_end])
        # print ("Angles %.3f, %.3f"%(degrees(angle_start), degrees(angle_end)))
        

    lengths = [0.0]
    sl = 0 
    for l in profiles: 
        sl += l[1]
        lengths.append(sl)
    ptn_delta = 360.0/ptn_PN 
    N0 = [0, 0.0, 0.0, 1.0]; N1 = [1, 0.0, 0.0, 0.0]

    #################################
    t0 = time.time()
    lines = ""
    nodecounting = 0 
    
    # tt0 = time.time()
    allnds = np.array(allnds)
    allnds = np.sort(np.unique(allnds))
    ptn_npn = np.concatenate((ptn_deleted[:,:4], ptn_npn), axis=0)
    ptn_npn = ptn_npn[ ptn_npn[:,0].argsort()[::1]]
    npnids = ptn_npn[:,0]

    pitch1 = np.where(ptn_npn[:,0] < 10**7 + ptn_offset)[0]
    pitch1 = ptn_npn[pitch1]
    pitch1 = pitch1[:, :4]
    angles = []
    P1 =[] 
    for i, nd in enumerate(pitch1): 
        cu = Angle_3nodes(N0, N1, nd, xy=13)    # circumferential angle from vertical line at center 
        if nd[1] < 0: cu = -cu 
        angles.append(cu)
        P1.append([nd[0], nd[1], nd[2], nd[3], cu])
    angles = np.array(angles)
    minangle =  np.min(angles) 
    delPitchAngle = np.max(angles) - minangle
    pitch1 = np.array(P1)
    
    r0 = profiles[0][0]

    cn = 10 
    N = len(allnds)
    N = int(N/cn)


    ## profile = [Tread R, Curve Width, accumulated width ]
    print ("    ", end="")
    cnt = 0 


    if shoulder == "S": 
        if profiles[-1][0] < 0: 
            del(profiles[-1])
        profiles[-1][1] +=0.5  
        profiles[-1][2] +=0.5 


    data = []
    for c, nid in enumerate(allnds): 
        if (c+1)%N ==0: 
            cnt += 1
            if cnt < 10: print("%d"%(cnt*10), end=">")
            else: print("%d%%"%(cnt*10))
        nd = ptn_npn[np.searchsorted(npnids, nid)]
        if nid != nd[0] : 
            print ("# no found, %d != %d"%(nid, nd[0]))
            continue 

        SL, r, i = TD_Arc_length_calculator(profiles, nd[2], msh_return=1)
        if nd[2] < 0: SL *= -1.0
        
        pn = int((nd[0] - 10**7) / ptn_offset)
        R = sqrt(nd[1]**2 + nd[3]**2)

        cu = Angle_3nodes(N0, N1, nd, xy=13)    # circumferential angle from vertical line at center 
        if nd[1] < 0: cu = 2*PI - cu 
        
        cv = Angles[i][0] + (Angles[i][1]-Angles[i][0]) * (abs(SL)-lengths[i]) / profiles[i][1]   # ratio = (abs(SL)-lengths[i]) / profiles[i][1] 
        if nd[2] < 0: cv *= -1.0

        Vx = -sin(cu)
        Vy = -tan(cv) 
        Vz = -cos(cu)
        MAG = sqrt(Vx**2 + Vy**2 + Vz**2) 

        
        ix = np.where(pitch1[:,0] == float(int(nd[0]) % ptn_offset) + 10**7 ) [0][0]
        angleratio = (pitch1[ix][4]-minangle) / delPitchAngle 
        
        f.write( "%8d %15.6e %15.6e %15.6e %15.6e %15.6e %15.6e %15.6e %15.6e %15.6e\n"%(nd[0], nd[1], nd[2], nd[3], \
                 HalfOD * (angleratio  + float(pn)) *delPitchAngle + flat_pattern_shift ,  SL, R - HalfOD, Vx/MAG, Vy/MAG , Vz/MAG) )
    
    f.close()
    t1 = time.time()
    print ("    Pattern nodes written (Δt=%.3f)"%(t1-t0))
    
    # print ("   %s"%(fname))

    fname = fname[:-3]+"ctr"
    f = open(fname, 'w')
    f.write("*CONFIG_FRAME     = 0\n")
    f.write("*CONFIG_FILE      = "+ fname[:-3] + "fen\n")
    f.write("*WSM_FILE         = "+ fname[:-3] + "wsm\n")
    f.write("*WND_FILE         = "+ fname[:-3] + "wnd\n")
    f.write("*PFL_FILE         = "+ fname[:-3] + "pfl\n")
    f.write("*WGT_FILE         = "+ fname[:-3] + "wgt\n")
    f.write("*DEP_FILE_CURRENT = "+ fname[:-3] + "dep\n")
    f.write("*DEP_FILE_OLD     = \n")
    f.write("*MAX_WEAR         = 0.0005\n")
    f.write("*C1_REF           = \n")
    f.write("*WEAR_RESULT      = 1\n")
    f.write("*FILE             = "+ fname[:-3] + "fen\n")
    f.write("*SUBCASES         = 1\n")
    f.write("01, 0.240, 1, 84.28, 100.0, 1\n")
    
    f.write("*************************************************************************\n")
    f.write("** Descriptions of output\n")
    f.write("*************************************************************************\n")
    f.write("** fen: simulation result\n")
    f.write("** wsm: wear summation\n")
    f.write("** snd: node coordinates after weared\n")
    f.write("** wgt: total wear\n")
    f.write("** pfl: total loss with lateral position \n")
    f.write("** dep: scalar value of wear \n")
    f.write("*************************************************************************\n")
    f.write("** more simulation results can be added *********************************\n")
    f.write("** *FILE             = WEAR2.fen\n")
    f.write("** *SUBCASES         = 1\n")
    f.write("** 2, Time at (Last -1) step, Rotations, Angular velocity, Vehicle speed(km/h), Wear Amplitude\n") 
    f.write("** *FILE             = WEAR3.fen\n")
    f.write("** *SUBCASES         = 1\n")
    f.write("** 3, Time at (Last -1) step, Rotations, Angular velocity, Vehicle speed(km/h), Wear Amplitude\n") 
    f.write("**")
    f.write("** wear amplitude can obtained from 'Frequency.dat'\n")
    f.write("** Frequency.dat : the result file of 'SimplifiedDataConversion9C'\n")
    f.write("*************************************************************************\n")
    f.close()
    print ("* 'FricView' Input (msh,ctr) was saved.\n")

    #############################################################
    ## FricVeiw Output file 
    #############################################################

    ## fricView output : *.dep
    ## Node ID, worn depth   (Max value of worn depth = m_MaxWear (user input))
    
    ## fricView output : *.wgt 
    ## Serial No, Weight value, (Weight value)*(Wear Amplitude), Wear Amplitude 
    ## Total Wear : (Weight value)*(Wear Amplitude)   { m_WeightValue[iFen]=(WearB-WearA)/(TimeB-TimeA) >> maybe wear speed?? }
    ## Max Wear   : (User input value)
    ## C1         : (Max Wear) / (Wear Limit)

    ## m_MaxWear : user input 
    ## m_Cwear   : sscanf(line, "*C1_REF=%lf",&m_Cwear) 
    ## WearLimit = AveWear + tri_Sdev   (tri_Sdev=3.*sqrt(SqrErrSum/nWornNod)  >> SqrErrSum = (Average Wear - Node Wear)**2), nWornNod : the No. of worn Nodes 
    
    ## C1 = m_Cwear = m_MaxWear / WearLimit (if  m_Cwear ==0 
    #                                  else: m_MaxWear = m_Cwear * WearLimit   (WearLimit=AveWear+tri_Sdev)
    ## WornDepth = m_Cwear * Wear (if WornDepth >= m_MaxWear : WornDepth = m_MaxWear)

    ## fricView output : *.wnd
    ## NodeID, worn node X, Y, Z 


    ## fricView output : *.pfl
    ## Accumulated wear  
    ## Coordinate Y, Accumulated Wear 01, Accumulated Wear 01, R position of Nodes..

    #############################################################

def TD_Arc_length_calculator(profile, h_dist=0, totalwidth=0, msh_return=0): 
    ## halfOD : for     square shoulder profile, to calculate the center of the circle with negative radius

    hx  = abs(h_dist)

    # curves = []
    c0x = 0
    c0y = 0 
    p_angle = 0 
    sum_length = 0
    pre_sum= 0  
    dist=0; drop=0
    length = 0 
    initR = profile[0][0]
    negR = 0 
    tangentLineCreated = 0 
    n_th = -1 
    # if showprofile ==1: print ("dist=%7.2f, drop=%7.2f, length=%7.2f"%(dist*1000, drop*1000, sum_length*1000))
    pm =0; pn=0 
    for i, pf in enumerate(profile):
        if pf[0] < 0 : negR = 1 
        ################################################################
        # if i == len(profile) -1 and totalwidth == 0:    ### I erased this line.. but I don't know why this is needed. 
        #     pf[1] += 10E-3 
        #########################################################
        current_R = pf[0] 
        r = abs(pf[0])
        sum_length += pf[1]
        angle = pf[1]/r ## arc angle 
        if i ==0: 
            drop = r - r * cos(angle)  # drop 
            dist = r*sin(angle)        # dist from center 
            # curves.append([dist, drop, sum_length, 0, r])
            p_drop = drop
            p_dist  =dist
            p_angle = angle 
            p_cx = 0
            p_cy = r 

            if hx <= dist and totalwidth==0:  
                theta = asin(hx/r) 
                length = r * sin(theta)
                n_th = i 
                break 

            pre_sum = sum_length

        else: 
            c = (p_drop - p_cy)/(p_dist-p_cx)   
            d = -p_dist * c + p_drop 
            e = d - p_drop 

            ## Ax^2 + Bx + C = 0  , 원의 중심에서 두 곡선의 교점을 지나는 직선 
            A = (c*c + 1)
            B = -2*p_dist + 2*e*c
            C = p_dist*p_dist + e*e - r*r 
            
            ## 직선과 원이 만나는 두 점을 찾음 
            cx1 = (-B + sqrt(B*B-4*A*C))/2/A 
            cx2 = (-B - sqrt(B*B-4*A*C))/2/A 
            
            if cx1 > cx2:  cx = cx2
            else: cx = cx1 

            cy = c * cx + d 
            
            angle_end   = p_angle + angle 
            drop = (cy - r) + (r-r*cos(angle_end))
            dist = cx + r*sin(angle_end)

            # print ("## dist=%.5f, drop=%.5f"%(dist, drop))

            if pf[0] < 0 and pm==0 and pn ==0:
                pm = p_dist 
                pn = p_drop 

            ## -R이 오면 +R로 Drop을 계산하고, -R이 시작되는 곳의 접선을 기준으로 대칭 이동하여 
            ## Drop과 dist 양을 계산할 수 있다...
            if negR ==1: 
                if tangentLineCreated ==0: 
                    ## 이전 곡선의 끝점에서 시작하는 접선 구함 

                    p_end =[p_dist, p_drop]
                    p_center = [p_cx, p_cy] 
                    # 곡선 끝 접선의 기울기 : ra 
                    ra = -(p_end[0]-p_center[0]) / (p_end[1]-p_center[1]) 
                    ## ra * x - y - ra*x_0 + y_0 = 0 >> rA*x + rB*y + rC = 0 
                    rA = ra 
                    rB = -1.0
                    rC = -ra * p_end[0] + p_end[1]
                    tangentLineCreated = 1 

                ## 대칭점 (px+qy+r=0 직선)
                ## (a,b) -> (m,n)
                ## m = (-ap^2 - 2bpq - 2pr + aq^2) / (p^2+q^2)
                ## n = (-bq^2 - 2apq - 2qr + bp^2 ) / (p^2 +q^2)

                m = ( -dist*rA**2 -2*drop* rA * rB - 2*rA *rC + dist*rB**2) / (rA**2 + rB**2)
                n = ( -drop*rB**2 -2*dist* rA * rB - 2*rB *rC + drop*rA**2) / (rA**2 + rB**2)

                # print ("%.5f, %.5f, dist, %.5f, drop, %.5f"%(dist, drop, m, n))

                if i == len(profile)- 1  : 
                    dist = m
                    drop = n 
                    n_th = i 

                if abs(hx) <= m and totalwidth==0:  
                    # if hx > 0.10: print ("    ", dist, drop, sum_length, cx, cy, r)
                    # print ("hx=", hx, "cx=", cx, "hx-cx = ", hx-cx, " r=", r, " > ", (hx-cx)/r)
                    n1 =[0, 0, pm, pn]
                    n2 = [0, 0, m, n]
                    # print (n1, n2)
                    centers = Circle_Center_with_2_nodes_radius(r, n1, n2, xy=23)
                    if centers[0][2]> centers[1][2]: 
                        cx = centers[0][2]
                    else: 
                        cx = centers[1][2]
                    theta = asin(abs(hx-cx)/r)
                    del_theta = theta - p_angle 
                    length = pre_sum + r * del_theta 
                    dist = m
                    drop = n 
                    n_th = i 
                    break 


            else: 
                if hx <= dist and totalwidth==0:  
                    # if hx > 0.10: print ("    ", dist, drop, sum_length, cx, cy)
                    theta = asin((hx-cx)/r)
                    del_theta = theta - p_angle 
                    length = pre_sum + r * del_theta 
                    n_th = i 
                    break 

            p_drop = drop
            p_dist = dist 
            p_angle = angle_end 
            p_cx = cx
            p_cy = cy 
            pre_sum = sum_length

            
            if negR ==1: 
                pm = m
                pn = n 
            
    if totalwidth ==1 and msh_return != 1:
        return sum_length, dist, drop 
    if msh_return == 1: 
        return length, current_R, n_th
    return length, current_R


def Circle3Nodes(n1, n2, n3, xy=23, radius=1, center=1, error=1):
    x = int(xy/10); y = int(xy%10)

    x1 = n1[x]; x2=n2[x]; x3=n3[x]
    y1 = n1[y]; y2=n2[y]; y3=n3[y]

    A = x1*(y2-y3) - y1 *(x2-x3) + x2*y3 - x3*y2
    B = (x1*x1 + y1*y1)*(y3-y2) +(x2**2 + y2**2)*(y1-y3) + (x3**2+y3**2)*(y2-y1)
    C = (x1**2 + y1**2)*(x2-x3)+(x2**2+y2**2)*(x3-x1) + (x3*x3 + y3*y3)*(x1-x2)
    D = (x1*x1 + y1*y1)*(x3*y2-x2*y3)+(x2*x2+y2*y2)*(x1*y3-x3*y1)+(x3*x3+y3*y3)*(x2*y1-x1*y2)
    SQRT = B*B + C*C - 4*A*D  

    if  A ==0 or SQRT < 0.0: 
        if error ==1: print (" The 3 nodes cannot make a circle.")
        R = 10**10
        CN = [-1]

    else: 
        cx = -B/A/2.0        ## center x
        cy = -C/A/2.0        ## center y
        
        R = sqrt(SQRT) / 2/abs(A)  ## radius 
        CN = [0, 0.0, 0.0, 0.0]
        CN[x] = cx 
        CN[y] = cy
    if radius ==1 and center ==1: return R, CN 
    if radius == 0 and center ==1: return CN 
    if radius == 1 and center ==0 : return R 


def checkJacobian2D(element, npn, xy=23): 
    x = int(xy/10); y = int(xy%10)

    NegJac=[]
    for e in element:
        if e[3] > 0 and e[4] > 0: 
            ix = np.where(npn[:,0]==e[1])[0][0]; x1 = npn[ix][x]; y1=npn[ix][y]
            ix = np.where(npn[:,0]==e[2])[0][0]; x2 = npn[ix][x]; y2=npn[ix][y]
            ix = np.where(npn[:,0]==e[3])[0][0]; x3 = npn[ix][x]; y3=npn[ix][y]
            ix = np.where(npn[:,0]==e[4])[0][0]; x4 = npn[ix][x]; y4=npn[ix][y]

            count = 0 
            for s in [1.0, -1.0]:
                for t in [1.0, -1.0]:
                    xs = 0.25 * ((-x1 + x2 + x3 - x4) + (x1 - x2 + x3 - x4) * t)
                    ys = 0.25 * ((-y1 + y2 + y3 - y4) + (y1 - y2 + y3 - y4) * t)
                    xt = 0.25 * ((-x1 - x2 + x3 + x4) + (x1 - x2 + x3 - x4) * s)
                    yt = 0.25 * ((-y1 - y2 + y3 + y4) + (y1 - y2 + y3 - y4) * s)
                    jacobian = xs * yt - ys * xt

                    if jacobian >= 0:
                        count += 1
            if count >0: 
                temp = e[2]
                e[2] = e[4]
                e[4] = temp 
                NegJac.append(e[0])
                
        elif e[3] > 0: 
            ix = np.where(npn[:,0]==e[1])[0][0]; x1 = npn[ix][x]; y1=npn[ix][y]
            ix = np.where(npn[:,0]==e[2])[0][0]; x2 = npn[ix][x]; y2=npn[ix][y]
            ix = np.where(npn[:,0]==e[3])[0][0]; x3 = npn[ix][x]; y3=npn[ix][y]

            det = NormalVector(x1, x2, x3, y1, y2, y3)
            if det > 0: 
                temp = e[2] 
                e[2] = e[3]
                e[3] = temp 
                NegJac.append(e[0])

    return element, NegJac  

def NormalVector(x1, x2, x3, y1, y2, y3):
    det = 0.0
    a1 = x2 - x1
    a2 = y2 - y1
    b1 = x3 - x2
    b2 = y3 - y2

    det = a1 * b2 - a2 * b1
    return det

##########################################################################################
# End of General Functions 
##########################################################################################
def OtherNodes_InSurface(surface, node_ids): 
    # Surface [ 0=EL ID, 1=Face, 2=No of nodes, 3=position, 4=cx, 5=cy, 6=cz, 7=N1, 8=n2, 9=n3, 10=n4, ... ] 
    lefts=[]
    nodes = node_ids 
    if len(node_ids) > surface[2]: 
        return lefts
    mch = []
    for i, nd in enumerate(nodes): 
        if nd == surface[7]: mch.append([nd, 1])
        if nd == surface[8]: mch.append([nd, 2])
        if nd == surface[9]: mch.append([nd, 3])
        if nd == surface[10]: mch.append([nd, 4])
    tmp = []
    for i in range(1, 5): 
        f = 0 
        for d in mch: 
            if d[1] == i : 
                f = 1 
                break 
        if f == 0 : 
            tmp.append(i)
    
    for i in tmp: 
        lefts.append([surface[6+i], i])
    # if nodes[0] == lefts[0][0] or nodes[0] == lefts[1][0] : 
    #     print (nodes, " UP..", lefts)
    # if nodes[1] == lefts[0][0] or nodes[1] == lefts[1][0] : 
    #     print (nodes, " UP..", lefts)
    return lefts 

########################################
def AddSolidon3DPlot(ax, solid, nodes): 
    ix = np.where(nodes[:,0] == solid[1])[0][0]; n1 = nodes[ix]
    ix = np.where(nodes[:,0] == solid[2])[0][0]; n2 = nodes[ix]
    ix = np.where(nodes[:,0] == solid[3])[0][0]; n3 = nodes[ix]
    ix = np.where(nodes[:,0] == solid[4])[0][0]; n4 = nodes[ix]
    ix = np.where(nodes[:,0] == solid[5])[0][0]; n5 = nodes[ix]
    ix = np.where(nodes[:,0] == solid[6])[0][0]; n6 = nodes[ix]
    
    

    if solid[7] > 0: 
        ix = np.where(nodes[:,0] == solid[7])[0][0]; n7 = nodes[ix]
        ix = np.where(nodes[:,0] == solid[8])[0][0]; n8 = nodes[ix]
        X = [n1[1], n2[1], n3[1], n4[1], n5[1], n6[1], n7[1], n8[1]]
        Y = [n1[2], n2[2], n3[2], n4[2], n5[2], n6[2], n7[2], n8[2]]
        Z = [n1[3], n2[3], n3[3], n4[3], n5[3], n6[3], n7[3], n8[3]]
        ax.scatter([n1[1]], [n1[2]], [n1[3]], c='black', marker='o')
        ax.scatter([n2[1]], [n2[2]], [n2[3]], c='blue', marker='o')
        ax.scatter([n3[1]], [n3[2]], [n3[3]], c='green', marker='o')
        ax.scatter([n4[1]], [n4[2]], [n4[3]], c='red', marker='o')
        ax.scatter([n5[1]], [n5[2]], [n5[3]], c='black', marker='o')
        ax.scatter([n6[1]], [n6[2]], [n6[3]], c='blue', marker='o')
        ax.scatter([n7[1]], [n7[2]], [n7[3]], c='green', marker='o')
        ax.scatter([n8[1]], [n8[2]], [n8[3]], c='red', marker='o')
        ax.text(n1[1], n1[2], n1[3], str(int(n1[0]-10**7)))
        ax.text(n2[1], n2[2], n2[3], str(int(n2[0]-10**7)))
        ax.text(n3[1], n3[2], n3[3], str(int(n3[0]-10**7)))
        ax.text(n4[1], n4[2], n4[3], str(int(n4[0]-10**7)))
        ax.text(n5[1], n5[2], n5[3], str(int(n5[0]-10**7)))
        ax.text(n6[1], n6[2], n6[3], str(int(n6[0]-10**7)))
        ax.text(n7[1], n7[2], n7[3], str(int(n7[0]-10**7)))
        ax.text(n8[1], n8[2], n8[3], str(int(n8[0]-10**7)))

        cx = np.average(np.array(X)); cy = np.average(np.array(Y)); cz = np.average(np.array(Z))
        ax.text(cx, cy, cz, "["+str(int(solid[0]-10**7))+"]")

        
        lx = [n1[1], n2[1], n3[1], n4[1], n1[1]]
        ly = [n1[2], n2[2], n3[2], n4[2], n1[2]]
        lz = [n1[3], n2[3], n3[3], n4[3], n1[3]]
        ax.plot(lx, ly, lz, 'b') 

        lx = [n5[1], n6[1], n7[1], n8[1], n5[1]]
        ly = [n5[2], n6[2], n7[2], n8[2], n5[2]]
        lz = [n5[3], n6[3], n7[3], n8[3], n5[3]]
        ax.plot(lx, ly, lz, 'r') 

        lx = [n1[1], n5[1]]
        ly = [n1[2], n5[2]]
        lz = [n1[3], n5[3]]
        ax.plot(lx, ly, lz)
        lx = [n2[1], n6[1]]
        ly = [n2[2], n6[2]]
        lz = [n2[3], n6[3]]
        ax.plot(lx, ly, lz)
        lx = [n3[1], n7[1]]
        ly = [n3[2], n7[2]]
        lz = [n3[3], n7[3]]
        ax.plot(lx, ly, lz)

    else: 
        X = [n1[1], n2[1], n3[1], n4[1], n5[1], n6[1]]
        Y = [n1[2], n2[2], n3[2], n4[2], n5[2], n6[2]]
        Z = [n1[3], n2[3], n3[3], n4[3], n5[3], n6[3]]
        # ax.scatter(X, Y, Z, c='r', marker='o') 
        ax.scatter([n1[1]], [n1[2]], [n1[3]], c='black', marker='o')
        ax.scatter([n2[1]], [n2[2]], [n2[3]], c='blue', marker='o')
        ax.scatter([n3[1]], [n3[2]], [n3[3]], c='green', marker='o')

        ax.scatter([n4[1]], [n4[2]], [n4[3]], c='black', marker='o')
        ax.scatter([n5[1]], [n5[2]], [n5[3]], c='blue', marker='o')
        ax.scatter([n6[1]], [n6[2]], [n6[3]], c='green', marker='o')
        
        lx = [n1[1], n2[1], n3[1], n1[1]]
        ly = [n1[2], n2[2], n3[2], n1[2]]
        lz = [n1[3], n2[3], n3[3], n1[3]]
        ax.plot(lx, ly, lz, 'b') 

        lx = [n4[1], n5[1], n6[1], n4[1]]
        ly = [n4[2], n5[2], n6[2], n4[2]]
        lz = [n4[3], n5[3], n6[3], n4[3]]
        ax.plot(lx, ly, lz, 'r') 

        lx = [n1[1], n4[1]]
        ly = [n1[2], n4[2]]
        lz = [n1[3], n4[3]]
        ax.plot(lx, ly, lz)
        lx = [n2[1], n5[1]]
        ly = [n2[2], n5[2]]
        lz = [n2[3], n5[3]]
        ax.plot(lx, ly, lz)

        X = [n1[1], n2[1], n3[1], n4[1], n5[1], n6[1]]
        Y = [n1[2], n2[2], n3[2], n4[2], n5[2], n6[2]]
        Z = [n1[3], n2[3], n3[3], n4[3], n5[3], n6[3]]
        ax.text(n1[1], n1[2], n1[3], str(int(n1[0]-10**7)))
        ax.text(n2[1], n2[2], n2[3], str(int(n2[0]-10**7)))
        ax.text(n3[1], n3[2], n3[3], str(int(n3[0]-10**7)))
        ax.text(n4[1], n4[2], n4[3], str(int(n4[0]-10**7)))
        ax.text(n5[1], n5[2], n5[3], str(int(n5[0]-10**7)))
        ax.text(n6[1], n6[2], n6[3], str(int(n6[0]-10**7)))

        cx = np.average(np.array(X)); cy = np.average(np.array(Y)); cz = np.average(np.array(Z))
        ax.text(cx, cy, cz, "["+str(int(solid[0]-10**7))+"]")


        
    return ax 

def ShowSolid(solids, nodes): 

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    try:
        NoSolid= len(solids) 
        print ("Image of %d solids"%(NoSolid))
    except: 
        NoSolid = 1 
    if NoSolid == 1: 
        ax = AddSolidon3DPlot(ax, solids, nodes)
    else: 
        for solid in solids: 
            ax = AddSolidon3DPlot(ax, solid, nodes)
    

    plt.tight_layout()  
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    plt.show()
def Image(file="IMAGE.png", dpi=300, xy=23, **kwargs): 
    nodes=[]; elements=[]; surfaces=[]; edges=[]; nlabel=""
    colors=['gray', 'blue', 'green', 'red', 'violet', 'darkorange', 'aqua', 'brown', 'navy', 'indigo']
    textsize = 2; size = 2 
    marker = 'o'; ls='-'; lc='black'; lw=0.1; color_depth=0.5
    nid = 0; eid=0; seid=0; snid=0; eeid=0; enid = 0 
    x = int(xy/10); y = int(xy%10)
    elnode = []; ednode=[]; sfnode=[]; 
    node_id_substraction = 0; 
    for key, value in kwargs.items(): 
        if "NODE" in key.upper() or "ND" in key.upper(): nodes.append(value)
        if "NLABEL" in key.upper() : nlabel=value 
        if "NID" in key.upper(): nid = value 
        if "SIZE" in key.upper(): size = value 
        if "TSIZE" in key.upper() or "TEXTSIZE" in key.upper(): textsize = value 
        if "ELEMENT" in key.upper() or "EL" in key.upper() : elements.append(value)
        if "SURFACE" in key.upper() or "SURF" in key.upper() : surfaces.append(value)
        if "EDGE" in key.upper() : edges.append(value) 
        if 'SUBSTRACTION' in key.upper() or 'TREAD' in key.upper(): node_id_substraction = value 
        if 'ELN' in key.upper(): elnode=value
        if 'EDN' in key.upper() or 'EGN' in key.upper(): ednode=value
        if 'SFN' in key.upper(): sfnode=value
        if 'LINESTYLE' in key.upper() or 'LS' in key.upper(): ls=value
        if 'LINECOLOR' in key.upper() or "LC" in key.upper(): lc=value 
        if 'LINEWIDTH' in key.upper() or 'LW' in key.upper(): lw=value 
        if 'ALPHA' in key.upper() or 'COLORDEPTH' in key.upper(): color_depth=value
        if 'SEID'  in key.upper() : seid=value
        if 'SNID'  in key.upper() : snid=value
        if 'EEID'  in key.upper() : eeid=value
        if 'ENID'  in key.upper() : enid=value

    
    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    fig, ax = plt.subplots()
    ax.axis('equal')
    ax.axis('on')
    if len(nodes) > 0: 
        for i, nds in enumerate(nodes):
            nds = np.array(nds)
            nx = nds[:,x]
            ny = nds[:,y]
            color = colors[int(i % len(colors))]
            if nlabel =="":    plt.scatter(nx, ny, c=color, s=size, marker=marker, edgecolors=None)
            else:    plt.scatter(nx, ny, c=color, s=size, marker=marker, edgecolors=None, label=nlabel)
            if nid != 0: 
                for nd in nds: 
                    plt.text(nd[x], nd[y], str(int(nd[0]-node_id_substraction)), size=textsize, c=color)
    if len(edges) > 0 :
        if len(ednode) ==0: ednode = nodes[0] 
        ednode = np.array(ednode)
        for i, edge in enumerate(edges):
            color = colors[int(i % len(colors))] 
            AddEdgeToImage(edge, linecolor=color, linewidth=lw, x=x, y=y, node=ednode, eid=eeid, nid=enid, textsize=textsize)

    if len(surfaces)>0: 
        if len(sfnode) ==0: sfnode = nodes[0]
        sfnode = np.array(sfnode)
        linecolor = 'gray'
        for i, surface in enumerate(surfaces): 
            color = colors[int(i % len(colors))] 
            AddSurfaceToImage(surface, colordepth=color_depth, linewidth=lw, linecolor=linecolor, shadow=color, ax=ax, x=x, y=y, eid=seid, nid=snid, tsize=textsize, nodes=sfnode, tread=node_id_substraction)
    plt.savefig(file, dpi=dpi, bbox_inches='tight')
    plt.close(fig)
    print ("## Image %s was saved."%(file))
def AddSurfaceToImage(surface, colordepth=0.5, linewidth=0.1, linecolor='black', shadow='gray', ax='', x=2, y=3, eid=0, nid=0, tsize=3, nodes=[], tread=0): 
    # print ("STARTING TO ADD SURFACE (NO=%6d)"%(len(surface)), end=" >> ")
    # t0=time.time()
    nsf = []
    for sf in surface: 
        temp = [sf[0], sf[1], sf[2], sf[3], sf[4], sf[5], sf[6], sf[7], sf[8], sf[9], sf[10] ]
        idx = np.where(nodes[:,0] == sf[7])[0][0]
        temp[7]= nodes[idx]
        idx = np.where(nodes[:,0] == sf[8])[0][0]
        temp[8]= nodes[idx]
        idx = np.where(nodes[:,0] == sf[9])[0][0]
        temp[9]= nodes[idx]
        if sf[10] != 0: 
            idx = np.where(nodes[:,0] == sf[10])[0][0]
            temp[10]= nodes[idx]
        else: 
            temp[10] = [0, 0, 0, 0]
        nsf.append(temp)

    # plt.plot([0., 0.0], [0, 0], linecolor, lw=0.0)

    for sf in nsf: 
        if nid ==1: 
            plt.text(sf[7][x], sf[7][y] , str(int(sf[7][0]-tread)), c='black', size=tsize)
            plt.text(sf[8][x], sf[8][y] , str(int(sf[8][0]-tread)), c='gray', size=tsize)
            plt.text(sf[9][x], sf[9][y] , str(int(sf[9][0]-tread)), c='gray', size=tsize)
            
            if sf[2] ==4 : 
                plt.text(sf[10][x], sf[10][y] , str(int(sf[10][0]-tread)), c='gray', size=tsize)

        if sf[2] ==3: 
            polygon = plt.Polygon([[sf[7][x], sf[7][y]], [sf[8][x], sf[8][y]], [sf[9][x], sf[9][y]]], color=shadow, alpha=colordepth, lw=linewidth, ec=linecolor)
            if eid ==1: 
                plt.text((sf[7][x]+sf[8][x]+sf[9][x])/3.0, (sf[7][y]+sf[8][y]+sf[9][y])/3.0, str(int(sf[0]-tread)), c='r', size=tsize)
        else: 
            plt.plot([sf[9][x], sf[10][x]], [sf[9][y],  sf[10][y]], linecolor, lw=linewidth)
            polygon = plt.Polygon([[sf[7][x], sf[7][y]], [sf[8][x], sf[8][y]], [sf[9][x], sf[9][y]], [sf[10][x], sf[10][y]]], color=shadow, alpha=colordepth, lw=linewidth, ec=linecolor)
            if eid ==1: 
                plt.text((sf[7][x]+sf[8][x]+sf[9][x]+sf[10][x])/4.0, (sf[7][y]+sf[8][y]+sf[9][y]+sf[10][y])/4.0, str(int(sf[0]-tread)), c='r', size=tsize)
        ax.add_patch(polygon)
def AddEdgeToImage(edge, linecolor='black', linewidth=0.1, x=2, y=3, node=[], eid=0, tsize=3, nid=0, textsize=3): 
    if len(node) ==0: 
        for ed in edge:
            ind = np.where(self.npn == ed[0])
            x1 = self.npn[ind[0][0]][x] 
            y1 = self.npn[ind[0][0]][y] 
            if nid ==1:  plt.text(x1, y1, str(int(self.npn[ind[0][0]][0])), color='red', fontsize=textsize*0.8)
            ind = np.where(self.npn == ed[1])
            x2 = self.npn[ind[0][0]][x] 
            y2 = self.npn[ind[0][0]][y] 
            plt.plot([x1, x2], [y1, y2], linecolor, lw=linewidth)
            if eid ==1: plt.text((x1+x2)/2.0, (y1+y2)/2.0, str(int(ed[4])), color='black', fontsize=textsize)
            if nid ==1: plt.text(x2, y2, str(int(self.npn[ind[0][0]][0])), color='blue', fontsize=textsize*0.8)
    else: 
        for ed in edge:
            ind = np.where(node == ed[0])[0][0]
            x1 = node[ind][x] 
            y1 = node[ind][y] 
            if nid ==1:  plt.text(x1, y1, str(int(node[ind][0])), color='red', fontsize=textsize*0.8)
            ind = np.where(node == ed[1])[0][0]
            x2 = node[ind][x] 
            y2 = node[ind][y] 
            plt.plot([x1, x2], [y1, y2], linecolor, lw=linewidth)
            if eid ==1: plt.text((x1+x2)/2.0, (y1+y2)/2.0, str(int(ed[4])), color='black', fontsize=textsize)
            if nid ==1: plt.text(x2, y2, str(int(node[ind][0])), color='blue', fontsize=textsize*0.8)
def WritePatternPitch(node, solid, file="scaled_pattern_mesh.inp", body_node=NODE(), body_element=ELEMENT()): 

    t0=time.time()
    line="*NODE, SYSTEM=R, NSET=PATTERN\n"
    for n in node: 
        line += "%10d, %15.8E, %15.8E, %15.8E\n"%(n[0], n[1], n[2], n[3])
    t1=time.time()
    ix6 = np.where(solid[:,9]==6)[0]
    if len(ix6) > 0 : 
        line+= "*ELEMENT, TYPE=C3D6, ELSET=SOLID6\n"
        solid6 = solid[ix6]
        for s in solid6: 
            line += "%10d, %10d, %10d, %10d, %10d, %10d, %10d\n"%(s[0], s[1], s[2], s[3], s[4], s[5], s[6])
    t2=time.time()
    ix8 = np.where(solid[:,9]==8)[0]
    if len(ix8) > 0 : 
        line+= "*ELEMENT, TYPE=C3D8R, ELSET=SOLID8\n"
        solid8 = solid[ix8]
        for s in solid8: 
            line += "%10d, %10d, %10d, %10d, %10d, %10d, %10d, %10d, %10d\n"%(s[0], s[1], s[2], s[3], s[4], s[5], s[6], s[7], s[8])
    t3=time.time()
    # print ("Writing TIME, Node=%.2f, 6 node=%.2f, 8 node=%.2f"%(t1-t0, t2-t1, t3-t2))


    if len(body_node.Node) != 0: 
        line+="*NODE, SYSTEM=R, NSET=BODY\n"
        xshift = 0.1E-03
        nshift = 10000
        for n in body_node.Node: 
            line += "%10d, %15.8E, %15.8E, %15.8E\n"%(n[0], n[1], n[2], n[3])
            line += "%10d, %15.8E, %15.8E, %15.8E\n"%(n[0]+nshift, n[1]+xshift, n[2], n[3])

        line+= "*ELEMENT, TYPE=M3D4R, ELSET=MEMBRANE\n"
        el3 =0 
        for e in body_element.Element:
            if e[6] == 2: 
                line += "%10d, %10d, %10d, %10d, %10d\n"%(e[0], e[1], e[2], e[1]+nshift, e[2]+nshift)
            if e[6] == 3: el3+=1

        if el3 > 0: 
            line+= "*ELEMENT, TYPE=C3D6, ELSET=SOLID3\n"
            for e in body_element.Element:
                if e[6] == 3: 
                    line += "%10d, %10d, %10d, %10d, %10d, %10d, %10d\n"%(e[0], e[1], e[2], e[3], e[1]+nshift, e[2]+nshift, e[3]+nshift)

        line+= "*ELEMENT, TYPE=C3D8R, ELSET=SOLID4\n"
        for e in body_element.Element:
            if e[6] == 4: 
                line += "%10d, %10d, %10d, %10d, %10d, %10d, %10d, %10d, %10d\n"%(e[0], e[1], e[2], e[3], e[4], e[1]+nshift, e[2]+nshift, e[3]+nshift, e[4]+nshift)


    print ("** Writing Pattern Mesh '%s'"%(file))
    f=open(file, "w")
    f.write(line)
    f.close()
def Save_2D_mesh_for_debugging(layout_node, layout_element, layout_elset, pattern_node, pattern_solid, bottom_surf=[]):

    file = "00-Debug-2D_mesh_with_pattern.msh" 

    f = open(file, 'w')
    f.write("*NODE, SYSTEM=R\n")
    for nd in layout_node.Node: 
        f.write("%6d, %10.6f, %10.6f, %10.6f\n"%(nd[0], nd[3], nd[2], nd[1]))
    f.write("*ELEMENT, TYPE=MGAX1\n")
    for el in layout_element.Element:
        if el[6] == 2: f.write("%6d, %6d, %6d\n"%(el[0], el[1], el[2]))
    f.write("*ELEMENT, TYPE=CGAX3H\n")
    for el in layout_element.Element:
        if el[6] == 3: f.write("%6d, %6d, %6d, %6d\n"%(el[0], el[1], el[2], el[3]))
    f.write("*ELEMENT, TYPE=CGAX4H\n")
    for el in layout_element.Element:
        if el[6] == 4: f.write("%6d, %6d, %6d, %6d, %6d\n"%(el[0], el[1], el[2], el[3], el[4]))
    for eset in layout_elset.Elset: 
        ending = 0 
        for i, e in enumerate(eset): 
            if i ==0: f.write("*ELSET, ELSET=%s\n"%(e))
            else: 
                f.write("%6d,"%(e))
                if i%10 ==0: 
                    f.write("\n")
                    ending = 1 
                else: 
                    ending = 0 
        if ending ==0: 
            f.write("\n")


    # solidid = [10001211, 10001212, 10001235, 10001236]
    if len(bottom_surf) > 0: 
        solidid=[]
        for sf in bottom_surf: 
            solidid.append(sf[0])
    ptn_nodes=[]
    surf = []
    
    for sd in solidid: 
        ix = np.where(pattern_solid[:, 0]==sd)[0][0]
        for i in range(1, 9): 
            if pattern_solid[ix][i] != 0: 
                # print (i, int(pattern_solid[ix][i]))
                nx = np.where(pattern_node[:,0]==pattern_solid[ix][i])[0][0]
                ptn_nodes.append(pattern_node[nx])
        if  pattern_solid[ix][8] > 0 : 
            surf.append([ pattern_solid[ix][0], pattern_solid[ix][1], pattern_solid[ix][2], pattern_solid[ix][3], pattern_solid[ix][4]])
            surf.append([ pattern_solid[ix][0]+20000, pattern_solid[ix][5], pattern_solid[ix][6], pattern_solid[ix][7], pattern_solid[ix][8]])

            surf.append([ pattern_solid[ix][0]+30000, pattern_solid[ix][1], pattern_solid[ix][2], pattern_solid[ix][6], pattern_solid[ix][5]])
            surf.append([ pattern_solid[ix][0]+40000, pattern_solid[ix][2], pattern_solid[ix][3], pattern_solid[ix][7], pattern_solid[ix][6]])
            surf.append([ pattern_solid[ix][0]+50000, pattern_solid[ix][3], pattern_solid[ix][4], pattern_solid[ix][8], pattern_solid[ix][7]])
            surf.append([ pattern_solid[ix][0]+60000, pattern_solid[ix][4], pattern_solid[ix][1], pattern_solid[ix][5], pattern_solid[ix][8]])
        else: 
            surf.append([ pattern_solid[ix][0], pattern_solid[ix][1], pattern_solid[ix][2], pattern_solid[ix][3], 0])
            surf.append([ pattern_solid[ix][0]+20000, pattern_solid[ix][4], pattern_solid[ix][5], pattern_solid[ix][6], 0])

            surf.append([ pattern_solid[ix][0]+30000, pattern_solid[ix][1], pattern_solid[ix][2], pattern_solid[ix][5], pattern_solid[ix][4]])
            surf.append([ pattern_solid[ix][0]+40000, pattern_solid[ix][2], pattern_solid[ix][3], pattern_solid[ix][6], pattern_solid[ix][5]])
            surf.append([ pattern_solid[ix][0]+50000, pattern_solid[ix][3], pattern_solid[ix][1], pattern_solid[ix][4], pattern_solid[ix][6]])
    
    txt = "*NODE, SYSTEM=R\n"
    f.write(txt)
    written=[]
    for nd in ptn_nodes: 
        fd = 0 

        for w in written: 
            if w == nd[0]: 
                fd =1
                break 
        if fd ==0:      
            written.append(nd[0])
            txt = "%10d, %15.8f, %15.8f, %15.8f\n"%(nd[0],  nd[3], nd[2], 0.0)
            f.write(txt)
    
    surfset=[]
    txt = "*ELEMENT, TYPE=MGAX1\n"
    f.write(txt)
    for el in surf: 
        if el[4] ==0: 
            txt = "%10d, %10d, %10d\n"%(el[0], el[1], el[2])
            f.write(txt)
            txt = "%10d, %10d, %10d\n"%(el[0]+100, el[2], el[3])
            f.write(txt)
            txt = "%10d, %10d, %10d\n"%(el[0]+200, el[3], el[1])
            f.write(txt)
            surfset.append(el[0])
            surfset.append(el[0]+100)
            surfset.append(el[0]+200)
        else: 
            txt = "%10d, %10d, %10d\n"%(el[0], el[1], el[2])
            f.write(txt)
            txt = "%10d, %10d, %10d\n"%(el[0]+100, el[2], el[3])
            f.write(txt)
            txt = "%10d, %10d, %10d\n"%(el[0]+200, el[3], el[4])
            f.write(txt)
            txt = "%10d, %10d, %10d\n"%(el[0]+300, el[4], el[1])
            f.write(txt)
            surfset.append(el[0])
            surfset.append(el[0]+100)
            surfset.append(el[0]+200)
            surfset.append(el[0]+400)
    
    line= "*ELSET, ELSET=TREAD\n"
    f.write(line)
    line = ""
    for i, en in enumerate(surfset): 
            if i%15 == 14: line += "%10d\n"%(en)
            else: line += "%10d,"%(en)
    if i %14 !=0: line+= "\n"
    f.write(line)

    f.close()
def NodeDuplication_check(nodes)   : 
    w = open("0_Nodes_duplication_check.txt", 'w')
    i = 0
    nodes = np.array(nodes)
    cnt = 0 
    while i < len(nodes): 
        ix = np.where(nodes[:, 0]==nodes[i][0])[0]
        if len(ix)>1: 
            if len(ix) == 2: 
                if nodes[ix[0]][1] == nodes[ix[1]][1] and nodes[ix[0]][2] == nodes[ix[1]][2] and nodes[ix[0]][3] == nodes[ix[1]][3]:  
                    nodes = np.delete(nodes, ix[1], axis=0)
                    i -=1 
                else: 
                    line = "%8d, %.6f, %.6f, %.6f, , %.6f, %.6f, %.6f\n"%(nodes[ix[0]][0],nodes[ix[0]][1], nodes[ix[0]][2], nodes[ix[0]][3],nodes[ix[1]][1], nodes[ix[1]][2], nodes[ix[1]][3])
                    print (line)
                    w.write(line)
                    cnt  += 1
        i += 1
    w.close()
    if cnt > 0: 
        sys.exit()
    else: 
        return nodes 
