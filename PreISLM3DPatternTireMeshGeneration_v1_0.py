import numpy as np
from math import sqrt, radians
from operator import mul as OP_mul 
import ptn_library as PTN
from os.path import isfile
from os import getcwd, environ, remove
import sys, glob, json  

try: 
    import CheckExecution, StoreFile
    inISLM = 1
except: 
    inISLM = 0 


BodySector = 240
PI = 3.14159265358979323846
Pattern_start_number = 10**7 
BodyOffsetNo = 10000 
PatternOffsetNo = 10000 


def ChaferDivide(Elements, ChaferName, Elset, Node):
    els = []
    for el in Elements: 
        els.append(el[:5])

    el = np.array(els)
    nd = np.array(Node)

    for eset in Elset: 
        for cn in ChaferName: 
            if cn == eset[0].upper(): 
                left=[]
                right=[]
                left.append(cn + '_L')
                right.append(cn + '_R')
                # print (eset)
                for en in range(1, len(eset)): 
                    ix = np.where(el[:,0] == eset[en])[0][0]
                    ixd = np.where(nd[:,0] == el[ix][1])[0][0]
                    
                    if nd[ixd][2] > 0: 
                        # print ("right", nd[ixd],  el[ix])
                        right.append(el[ix][0])
                    else:
                        # print ("left", nd[ixd],  el[ix])
                        left.append(el[ix][0])
                if len(right) > 0: 
                    Elset.append(right)
                    Elset.append(left)

    return Elements, Elset

 

class PATTERN_EXPANSION(): 
    def __init__(self, layoutmesh, patternmesh, pn, direction, No_pattern): 
        self.layoutmesh=layoutmesh
        self.patternmesh=patternmesh
        self.user_number_pitch = pn 
        self.direction = direction 
        self.user_sector = 240 
        self.PI = 3.14159265358979323846
        self.Pattern_start_number = No_pattern
        self.BodyOffset  = BodyOffsetNo
        self.POFFSET = PatternOffsetNo

        L_profile, R_profile, OD, TW, TDW, GD = PTN.ReadMoldProfileFromPatternMeshFile(self.patternmesh)

        self.layout = PTN.MESH2D(self.layoutmesh)
        ## chafer divide 
        ChaferName = ['CH1', 'CH2', 'CH3']
        self.layout.Element.Element, self.layout.Elset.Elset = ChaferDivide(self.layout.Element.Element, ChaferName, self.layout.Elset.Elset, self.layout.Node.Node)

        self.InitialLayout = PTN.COPYLAYOUT(self.layout)
        self.pattern = PTN.PATTERN(self.patternmesh, test=0)

        if self.pattern.TreadDesignWidth==0: 
            print ("\n***********************************************************")
            print (" ERROR!! Tread Design Width is not in the pattern mesh file.")
            print (" Insert 'Tread Design Width' into *.ptn")
            print ("*TREAD_DESIGN_WIDTH : OOO.OO")
            print ("***********************************************************\n")
            sys.exit()


        if len(self.pattern.errsolid) > 0: 
            for sd in self.pattern.errsolid: 
                print (" Distored %d"%(sd[0]))
            
            print ("ERROR, Some of Pattern Elements are distorted")
            sys.exit()

        if self.layout.shoulderType == 'R':
            self.layout.EliminateTread(self.layoutmesh, self.patternmesh, self.pattern.leftprofile, self.pattern.rightprofile,\
                self.pattern.diameter, self.pattern.TreadDesignWidth, self.pattern.PatternWidth, self.pattern.ModelGD, t3dm=self.layout.T3DMMODE, result=0, layoutProfile=self.layout.RightProfile)
        else: 
            self.layout.ElimateSquareTread(self.pattern.leftprofile, self.pattern.rightprofile)
            try: M=len(self.layout.tdnodes.Node)
            except: 
                print ("'ERROR, Fail to delete tread (SQUARE)!!")
                sys.exit()

        if self.layout.shoulderType == 'R':
            self.flattened_Tread_bottom_sorted, self.layout.GD = PTN.Unbending_layoutTread(self.layout.tdnodes, self.layout.Tread, \
                self.layout.LeftProfile, self.layout.RightProfile, self.layout.L_curves, self.layout.R_curves, self.layout.OD, \
                ptn_node=self.pattern.npn, GD=self.layout.GD)
            self.shoulderGa = PTN.ShoulderTreadGa(self.layout.OD, self.layout.RightProfile, self.layout.R_curves, \
                self.flattened_Tread_bottom_sorted, self.layout.TDW, shoR=self.layout.r_shocurve)

            self.layout.TargetPatternWidth = np.max(self.flattened_Tread_bottom_sorted[:,2]) -  np.min(self.flattened_Tread_bottom_sorted[:,2]) 

        elif self.layout.shoulderType == 'S'  and len(self.layout.tdnodes.Node) > 0 and self.layout.T3DMMODE ==0: 
            self.flattened_Tread_bottom_sorted,   self.layout.sideNodes=PTN.Unbending_squareLayoutTread(self.layout.tdnodes, self.layout.Tread, \
                self.layout.LeftProfile, self.layout.RightProfile, self.layout.OD, self.layout.R_curves, shoDrop=self.layout.shoulderDrop,\
                     edgeBtm=self.layout.Edge_treadBottom)
            self.shoulderGa = 1.0

            if len(self.flattened_Tread_bottom_sorted) ==0: 
                print ("'ERROR, Layout Tread Area was not found!!")
                sys.exit()
            

        auto_pitch=self.pattern.Expansion(self.layout.OD, self.layout.TDW, self.layout.TargetPatternWidth,\
                 self.layout.GD, user_pitch_no=self.user_number_pitch, t3dm=self.layout.T3DMMODE, shoulder=self.layout.shoulderType)
        
        self.generation_mesh()

    def generation_mesh(self): 

        Mesh2DInp = self.layoutmesh[:-4] + "-tmp.tmp"
        layoutms = self.layoutmesh.split("/")[-1].split(".")[0]
        ptnms = self.patternmesh.split("/")[-1].split(".")[0]
        cwd = getcwd() 

        print ("# 3D Full mesh file : %s"%(layoutms+"-"+ptnms))

        solid_err=[]
        self.pd=0
        if self.layout.shoulderType=="R":
            if  self.layout.r_shocurve < 6.0E-03 or self.shoulderGa >= self.layout.r_shocurve  + 2.0e-03:       self.Check_ShoulderGaugeCheck = 1
            if self.layout.T3DMMODE == 0: 
                gauge_constant_range=self.layout.TDW/2.0 # + 10.0E-3
                if self.shoulderGa > self.layout.r_shocurve - 1.0e-03: 
                    gauge_constant_range=self.layout.TDW/2.0 - 10.0E-3

                self.pattern.npn, ptn_elset=PTN.Pattern_Gauge_Adjustment_ToBody(self.flattened_Tread_bottom_sorted, self.pattern.npn, \
                        self.pattern.freebottom, self.pattern.nps, self.layout.OD, gauge_constant_range,\
                        self.pattern.Node_Origin, self.pattern.surf_pattern_pos_side, self.pattern.surf_pattern_neg_side)
                
        self.ptn_gauged = PTN.COPYPTN(self.pattern)   

        if self.layout.shoulderType=="R" and self.layout.T3DMMODE== 0: 
            self.pattern.npn =PTN.BendingPattern(OD=self.layout.OD, Rprofiles=self.layout.RightProfile, \
                Rcurves=self.layout.R_curves, Lprofiles=self.layout.LeftProfile , Lcurves=self.layout.L_curves , nodes=self.pattern.npn,  xy=23)
        else:
            self.pattern.npn = PTN.BendingSquarePattern(OD=self.layout.OD, profiles=self.layout.RightProfile, curves=self.layout.R_curves,\
                    nodes=self.pattern.npn, xy=23)

        if self.layout.T3DMMODE == 1: 
            self.pattern.npn = PTN.NodesOnSolids(self.pattern.npn, self.pattern.nps)
        
        if self.layout.shoulderType=="R"  : 
            self.pattern.npn, self.edge_body, self.pd, pf_ending = PTN.Adjust_PatternBottomSideNodes(self.layout.Node, self.layout.Element, \
                self.layout.Tread, self.pattern.npn, self.pattern.surf_pattern_neg_side, self.pattern.surf_pattern_pos_side,\
                self.pattern.Node_Origin, self.pattern.freebottom, TDW=self.layout.TDW, t3dm=self.layout.T3DMMODE)

        elif self.layout.shoulderType=="S" and self.layout.T3DMMODE == 0:
            self.pattern.npn, self.pattern.sideBtmNode = PTN.AttatchSquarePatternSideNodes(self.layout.sideNodes, self.pattern.npn, self.pattern.Node_Origin, \
                                self.pattern.surf_pattern_neg_side, self.pattern.surf_pattern_pos_side)
        
        self.ptn_bended = PTN.COPYPTN(self.pattern)      
        if len(self.layout.Tread.Element)  : 
            self.nodes_layout_treadbottom = PTN.Get_layout_treadbottom(self.flattened_Tread_bottom_sorted, np.array(self.InitialLayout.Node.Node))

        if self.layout.shoulderType=="R" : #and self.layout.T3DMMODE ==0: 
            self.pattern.npn = PTN.RepositionNodesAfterShoulder(pf_ending, self.ptn_gauged.npn, self.pattern.surf_pattern_pos_side, self.pattern.surf_pattern_neg_side, \
                    self.pattern.npn,  self.layout.TDW, self.layout.RightProfile, self.layout.R_curves, self.layout.L_curves,\
                    btm_surf=self.pattern.freebottom, ptn_R=self.pattern.diameter/2.0, ptn_TDW=self.pattern.TreadDesignWidth,\
                    bodynodes=self.layout.Node, bodybottom=self.nodes_layout_treadbottom, ptn_orgn=self.pattern.Node_Origin)

        # self.ptn_bended = PTN.COPYPTN(self.pattern)
        if self.layout.shoulderType=="S" and self.layout.T3DMMODE==0: 
            self.pattern.npn = PTN.ShiftShoulderNodesSquarePattern(self.pattern.npn, self.pattern.Node_Origin, self.layout.RightProfile, self.layout.R_curves,\
                    self.layout.sideNodes, self.pattern.surf_pattern_pos_side, self.pattern.surf_pattern_neg_side,\
                    self.pattern.TreadDesignWidth, self.layout.TDW, self.pattern.sideBtmNode )
        start = 0             
        self.pattern.npn = PTN.AttatchBottomNodesToBody(bodynodes=self.layout.Node, \
            bodyelements=self.layout.Element, ptnnodes=self.pattern.npn, \
                ptnbottom=self.pattern.freebottom, start=start, \
                    shoulder=self.layout.shoulderType, ptnelements=self.pattern.nps)

        ## Sub Tread is  ... : subtread = False 
        isSubTread = True

        if self.layout.shoulderType == 'S' :   self.layout.group ="TBR"
        if self.layout.group =="TBR" : subGa_margin = 0.001 
        elif self.layout.group =="LTR": subGa_margin = 0.0003 
        else: subGa_margin = 0.0003
        
        self.ptn_elset, self.pattern.nps, self.pattern.npn, self.pattern.surf_pitch_up, self.pattern.surf_pitch_down, \
                 self.pattern.surf_pattern_neg_side, self.pattern.surf_pattern_pos_side, NewELMatching, NewSurfs\
                 = PTN.PatternElsetDefinition(self.pattern.nps, self.pattern.npn, self.layout.Tread, self.layout.Node,\
                 subtread=isSubTread, btm=1, surf_btm=self.pattern.freebottom, subGaMargin=subGa_margin,\
                 shoulder=self.layout.shoulderType,  tdw=self.layout.TDW, pitchUp=self.pattern.surf_pitch_up, \
                     pitchDown=self.pattern.surf_pitch_down, sideNeg=self.pattern.surf_pattern_neg_side, sidePos=self.pattern.surf_pattern_pos_side, backupSolid=self.ptn_bended)

        if len(self.pattern.SF_fulldepthgroove) and len(NewELMatching):
            NewELMatching = np.array(NewELMatching)

            for nem in NewELMatching: 
                ix = np.where(self.pattern.Free_Surface_without_BTM[:,0]==nem[0])[0]
                if len(ix)>0: 
                    for x in ix: 
                        if self.pattern.Free_Surface_without_BTM[x][1] ==2: 
                            self.pattern.Free_Surface_without_BTM[x][0] = nem[1]

                ix = np.where(self.pattern.SF_fulldepthgroove[:,0]==nem[0])[0]
                if len(ix)>0: 
                    for x in ix: 
                        if self.pattern.SF_fulldepthgroove[x][1] ==2: 
                            self.pattern.SF_fulldepthgroove[x][0] = nem[1]

                ix = np.where(self.pattern.PTN_AllFreeSurface[:,0]==nem[0])[0]
                if len(ix)>0: 
                    for x in ix: 
                        if self.pattern.PTN_AllFreeSurface[x][1] ==2: 
                            self.pattern.PTN_AllFreeSurface[x][0] = nem[1]
                            # print("GRV", self.pattern.PTN_AllFreeSurface[x][0], "Face", self.pattern.PTN_AllFreeSurface[x][1])

            self.pattern.PTN_AllFreeSurface = np.concatenate((self.pattern.PTN_AllFreeSurface, NewSurfs), axis=0)   
        ###################################################################
        ## pattern direction change 
        ###################################################################
        if self.direction != 0: self.PTN_Direction_Change()
        ###################################################################
       
        
        self.pattern.npn = PTN.BendintPatternInCircumferentialDirection(self.pattern.npn, self.layout.OD)

        NN = len(self.pattern.npn); NS= len(self.pattern.nps)

        solid_err, text, _, _=PTN.Jacobian_check(self.pattern.npn, self.pattern.nps)  ## deformed pattern mesh check 

        

        if len(solid_err) > 0 : 
            soler = np.array(solid_err)
            soler = soler[:,0]
            btmel = self.pattern.freebottom[:,0]
            btmer = np.intersect1d(btmel, soler)
            txt = "### Elements distorted\n"
            for sd in solid_err: 
                txt += " %d, "%(sd[0])
            txt += "\n>Trying to relocate the nodes on the bottom solids"
            print (txt)
            if len(btmer) == 0 : 
                ## Checking the elements of Jacobian < 0.01 
                
                free_surface_nodes= self.ptn_model.Free_Surface_without_BTM[:,7:]

                free_surface_nodes = np.unique(free_surface_nodes)

                unchecked = []
                checked = []
                for sl in solid_err: 
                    
                    ernodes = []
                    ernodes.append(sl[1]); ernodes.append(sl[2]); ernodes.append(sl[3]); ernodes.append(sl[4]); 
                    ernodes.append(sl[5]); ernodes.append(sl[6])
                    if sl[7] > 0: 
                        ernodes.append(sl[7]); ernodes.append(sl[8])

                    ernodes = np.array(ernodes)
                    ern = np.setdiff1d(ernodes, free_surface_nodes)
                    tmp=[sl[0], sl[1], sl[2], sl[3], sl[4], sl[5], sl[6], sl[7], sl[8], len(ern), ern]
                    checked.append(tmp)
                checked = sorted(checked, key = lambda val : val[9])
                for sl in checked: 
                    if sl[9] > 0 : 
                        for nd in sl[10]: 
                            ix1=0; ix2 = 0 
                            if nd == sl[1] : 
                                ix1 = np.where(self.pattern.npn[:,0]==nd)[0][0]
                                if sl[7] > 0: 
                                    ix2 = np.where(self.pattern.npn[:,0]==sl[5])[0][0]
                                else: 
                                    ix2 = np.where(self.pattern.npn[:,0]==sl[4])[0][0]
                                self.pattern.npn[ix1][1] = self.pattern.npn[ix2][1] 
                                self.pattern.npn[ix1][2] = self.pattern.npn[ix2][2] 
                                # print ("   N1 ", self.pattern.npn[ix1][0]-10**7, self.pattern.npn[ix2][0]-10**7)

                            elif nd == sl[2]: 
                                ix1 = np.where(self.pattern.npn[:,0]==nd)[0][0]
                                if sl[7] > 0: 
                                    ix2 = np.where(self.pattern.npn[:,0]==sl[6])[0][0]
                                else: 
                                    ix2 = np.where(self.pattern.npn[:,0]==sl[5])[0][0]
                                self.pattern.npn[ix1][1] = self.pattern.npn[ix2][1] 
                                self.pattern.npn[ix1][2] = self.pattern.npn[ix2][2]
                                # print ("   N2 ", self.pattern.npn[ix1][0]-10**7, self.pattern.npn[ix2][0]-10**7)

                            elif nd == sl[3]: 
                                ix1 = np.where(self.pattern.npn[:,0]==nd)[0][0]
                                if sl[7] > 0: 
                                    ix2 = np.where(self.pattern.npn[:,0]==sl[7])[0][0]
                                else: 
                                    ix2 = np.where(self.pattern.npn[:,0]==sl[6])[0][0]
                                # print ("   N3 ", self.pattern.npn[ix1][0]-10**7, self.pattern.npn[ix2][0]-10**7)
                                # print ("    %6.2f, %6.2f,     %6.2f,%6.2f"%( self.pattern.npn[ix1][1]*1000, self.pattern.npn[ix1][2]*1000, self.pattern.npn[ix2][1]*1000, self.pattern.npn[ix2][2]*1000))
                                self.pattern.npn[ix1][1] = self.pattern.npn[ix2][1] 
                                self.pattern.npn[ix1][2] = self.pattern.npn[ix2][2] 
                                # print (" >> %6.2f, %6.2f "%(self.pattern.npn[ix1][1]*1000, self.pattern.npn[ix1][2]*1000))

                            elif nd == sl[4] and sl[7] > 0: 
                                ix1 = np.where(self.pattern.npn[:,0]==nd)[0][0]
                                if sl[7] > 0: 
                                    ix2 = np.where(self.pattern.npn[:,0]==sl[8])[0][0]
                                self.pattern.npn[ix1][1] = self.pattern.npn[ix2][1] 
                                self.pattern.npn[ix1][2] = self.pattern.npn[ix2][2] 
                                # print ("   N4 ", self.pattern.npn[ix1][0]-10**7, self.pattern.npn[ix2][0]-10**7)
                    else:
                        unchecked.append(sl)
                
                for sl in unchecked:     
                    ix1 = np.where(self.pattern.npn[:,0]==sl[1])[0][0]
                    if sl[7] > 0: 
                        ix2 = np.where(self.pattern.npn[:,0]==sl[5])[0][0]
                    else: 
                        ix2 = np.where(self.pattern.npn[:,0]==sl[4])[0][0]
                    self.pattern.npn[ix1][1] = self.pattern.npn[ix2][1] 
                    self.pattern.npn[ix1][2] = self.pattern.npn[ix2][2] 

                    ix1 = np.where(self.pattern.npn[:,0]==sl[2])[0][0]
                    if sl[7] > 0: 
                        ix2 = np.where(self.pattern.npn[:,0]==sl[6])[0][0]
                    else: 
                        ix2 = np.where(self.pattern.npn[:,0]==sl[5])[0][0]
                    self.pattern.npn[ix1][1] = self.pattern.npn[ix2][1] 
                    self.pattern.npn[ix1][2] = self.pattern.npn[ix2][2] 

                    ix1 = np.where(self.pattern.npn[:,0]==sl[3])[0][0]
                    if sl[7] > 0: 
                        ix2 = np.where(self.pattern.npn[:,0]==sl[7])[0][0]
                    else: 
                        ix2 = np.where(self.pattern.npn[:,0]==sl[6])[0][0]
                    self.pattern.npn[ix1][1] = self.pattern.npn[ix2][1] 
                    self.pattern.npn[ix1][2] = self.pattern.npn[ix2][2] 

                    if sl[7] > 0: 
                        ix1 = np.where(self.pattern.npn[:,0]==sl[4])[0][0]
                        ix2 = np.where(self.pattern.npn[:,0]==sl[8])[0][0]
                        self.pattern.npn[ix1][1] = self.pattern.npn[ix2][1] 
                        self.pattern.npn[ix1][2] = self.pattern.npn[ix2][2] 

                solid_err, text, negative_ht, sm_lth=PTN.Jacobian_check(self.pattern.npn, self.pattern.nps)  ## deformed pattern mesh check 

        if len(solid_err) > 0 : 
            print (text)
            print ("#############################################")
            print ("### %d elements in Pattern mesh is distorted"%(len(solid_err)))
            print ("#############################################\n")
            # PTN.WritePatternPitch(self.pattern.npn, self.pattern.nps, file=self.cwd+"0-Distorted-"+self.layoutms+"-"+self.ptnms +".inp", body_node=self.layout.Node, body_element=self.layout.Element)

            txt = "### Elements distorted\n"
            for sd in solid_err: 
                txt += " %d, "%(sd[0])
            print (txt)

        BodySector = self.user_sector
        BodyOffset = self.BodyOffset
        BodyStartNo = 1

        NN = len(self.pattern.npn); NS= len(self.pattern.nps)
        NN = int(np.max(self.pattern.npn[:,0])) - 10**7
        NS = int(np.max(self.pattern.nps[:,0])) - 10**7 
        if NN > NS: POFFSET=int(NN/10000) * 10000 + 10000
        else:       POFFSET=int(NS/10000) * 10000 + 10000
        self.poffset = POFFSET
        print ("* The max number of nodes  %d"%(NN))
        print ("* The max number of solids %d"%(NS))

        print ("\n** Full 3D Mesh ")
        print ("** Pattern Start =%d, Offset=%d\n** Layout Start=%d, Offset=%d\n** No. of body sectors=%d\n"%(self.Pattern_start_number, POFFSET, BodyStartNo, BodyOffset, BodySector))
        
        self.nd_deleted=[]
        self.fullnodes=[]
        self.fullsolids=[]

        if self.direction ==1: ROTATE = True 
        else: ROTATE = False

        pitch_side = [self.pattern.surf_pattern_neg_side, self.pattern.surf_pattern_pos_side]
        self.fullnodes, self.fullsolids, self.elset3d, self.surf_XTRD1001, self.surf_YTIE1001, self.nd_deleted, self.deletednode, \
        XTRD_surface, YTIE_surface= PTN.GenerateFullPatternMesh(self.pattern.npn, self.pattern.nps, self.pattern.NoPitch, self.layout.OD, self.pattern.surf_pitch_up, self.pattern.surf_pitch_down, \
            surf_free=self.pattern.PTN_AllFreeSurface, surf_btm=self.pattern.freebottom, surf_side=pitch_side, elset=self.ptn_elset, \
            offset=POFFSET, pl=self.pattern.TargetPL, ptn_org=self.pattern.Node_Origin, ptn_pl=self.pattern.pitchlength, pd=self.pd , \
                rev=ROTATE, shoulderType=self.layout.shoulderType)
        self.XTRD_surface = XTRD_surface
        self.YTIE_surface =  YTIE_surface

        if self.layout.T3DMMODE ==1 or self.layout.shoulderType == "S":   
            self.edge_body = self.layout.Element.OuterEdge(self.layout.Node)
        self.B3Dnodes, self.B3Del4, self.B3Del6, self.B3Del8, self.B3Delset, self.B3Dsurface, self.Bodysurf = \
        PTN.GenerateFullBodyMesh(self.layout.body_nodes, self.layout.Element, self.layout.Elset, \
            surfaces=self.layout.Surface, body_outer=self.edge_body, sectors=BodySector, offset=BodyOffset)
            


        isCtb=0
        isSut=0 
        for eset in self.layout.Elset.Elset: 
            if eset[0] == "CTR" or eset[0] == 'CTB': isCtb = 1
            if eset[0] == "UTR" or eset[0] == 'SUT': isSut = 1
        namechange = [isCtb, isSut]

        savefileTRD =  cwd +"/" + ptnms 
        savefileAXI =  cwd +"/" + layoutms 
        savefile =  cwd +"/" + layoutms +"-" + ptnms
        abq = 0 
        PTN.Write_SMART_PatternMesh(file=savefileTRD +".trd", nodes=self.fullnodes, elements=self.fullsolids , elsets=self.elset3d, XTRD=self.surf_XTRD1001, \
            YTIE=self.surf_YTIE1001, ties=[], start=self.Pattern_start_number, offset=self.poffset, namechange=namechange, abaqus=abq, revPtn=ROTATE)#self.poffset)
        PTN.Write_SMART_TireBodyMesh(file=savefileAXI  + ".axi", nodes=self.B3Dnodes, el4=self.B3Del4, el6=self.B3Del6, el8=self.B3Del8, elsets=self.B3Delset, surfaces=self.B3Dsurface,\
            surf_body=self.Bodysurf, ties=self.layout.Tie, txtelset=self.layout.TxtElset, start=BodyStartNo, offset=BodyOffset, abaqus=abq)

        components = PTN.SolidComponents_checking(trd=savefileTRD +".trd", axi=savefileAXI +".axi", return_value= 1)
        self.solidElset=components[0]
        self.rebarElset=components[1]
        print("")
        f = open(savefile+".cpn", 'w')
        f.write("*SOLID\n")
        for cm in components[0]: 
            f.write("%s\n"%(cm))
        f.write("*REBAR\n")
        for cm in components[1]: 
            f.write("%s\n"%(cm))
        f.close()

    def PTN_Direction_Change(self):

        rot =radians(180.0)
        for i, npn in enumerate(self.pattern.npn) :
            self.pattern.npn[i] = PTN.RotateNode(npn, angle=rot, xy=21)

        tempSurf = []
        for sf in self.pattern.surf_pitch_up: 
            tempSurf.append(sf)
        tempSf = []
        for sf in self.pattern.surf_pitch_down: 
            tempSf.append(sf)

        self.pattern.surf_pitch_up = np.array(tempSf)
        self.pattern.surf_pitch_down = np.array(tempSurf)


        tempSurf = []
        for sf in self.pattern.surf_pattern_neg_side: 
            tempSurf.append(sf)
        tempSf = []
        for sf in self.pattern.surf_pattern_pos_side: 
            tempSf.append(sf)

        self.pattern.surf_pattern_neg_side = np.array(tempSf)
        self.pattern.surf_pattern_pos_side = np.array(tempSurf)

        print ("************************************")
        print ("** Pattern was ROTATED.")
        print ("************************************")

if __name__ == "__main__": 
    if inISLM == 1: CheckExecution.getProgramTime(str(sys.argv[0]), "Start")

    user_number_pitch = 0 
    no_ptn = Pattern_start_number

    cwd=getcwd()
    snsFiles = glob.glob(cwd+"/*.sns")
    if len(snsFiles) ==0 : 
        layoutmesh = ""
        patternmesh = ""
        patternmesh = ""
        if len(sys.argv) > 1: 
            for arg in sys.argv: 
                line = arg.split("=")
                if line[0].lower() == 'ptn' or line[0].lower() == 'p': patternmesh=line[1].strip()
                if line[0].lower() == 'layout' or line[0].lower() == 'l': layoutmesh=line[1].strip()
                if line[0].lower() == 'pn' or line[0].lower() == 'n': user_number_pitch=int(line[1].strip())
                if line[0].lower() == 'direction' or line[0].lower() == 'd': patternDirection=int(line[1].strip())
                if line[0] == 'sns': snsFile = line[1]
    else:
        snsFile = snsFiles[0]
        ptnFiles = glob.glob(cwd+"/*.ptn")
        patternmesh = ptnFiles[0]

        with open(snsFile) as SNS:
            snsInfo = json.load(SNS)
        
        layoutmesh = cwd+"/"+str(snsInfo["VirtualTireBasicInfo"]["VirtualTireID"]) + "-" + str(snsInfo["VirtualTireBasicInfo"]["HiddenRevision"]) + ".inp"

        print (layoutmesh)
        print (patternmesh)

        try: 
            patternDirection = int(snsInfo["AnalysisInformation"]["PatternMeshInfo"]["PatternReverse"])
        except: 
            patternDirection = 0 


    if patternmesh !="" and layoutmesh !="": 
        pattern = PATTERN_EXPANSION(layoutmesh, patternmesh, user_number_pitch, patternDirection, no_ptn)

    if len(snsFiles)  : 
        solidInfo = snsInfo["ElsetMaterialInfo"]["Mixing"]
        cordInfo = snsInfo["ElsetMaterialInfo"]["Calendered"]

        compounds =[]
        for solid in solidInfo: 
            compounds.append([solid['Elset'], solid['Compound']])
            # print (compounds[-1])
        calendered =[]
        for cord in cordInfo: 
            if cord['Direction'] == 'L': 
                calendered.append([cord['Elset'], cord['MatCode'], -float(cord['Angle']), cord['Compound'], float(cord['EPI']), float(cord['Gauge'])])
            else: 
                calendered.append([cord['Elset'], cord['MatCode'], float(cord['Angle']), cord['Compound'],   float(cord['EPI']), float(cord['Gauge'])])
            # print(calendered[-1])

    if inISLM == 1: CheckExecution.getProgramTime(str(sys.argv[0]), "End")

