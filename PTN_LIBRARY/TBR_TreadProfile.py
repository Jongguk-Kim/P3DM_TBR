from math import *


#######################################
## unit : m 
#######################################

# profile =[ [ 0.750, 0.04813], 
#            [0.1875, 0.00722] , 
#            [10.000, 0.06965] 
#         #    ,[-0.250, 0.039241]  ## negative value = curve on side .. 
#          ]
profile =[ [ 0.750, 0.052], 
           [10.000, 0.073] 
        #    ,[-0.250, 0.039241]  ## negative value = curve on side .. 
         ]
shoDrop = 9.3e-3
tireOD =  1.073

#######################################


def main(profile, shoDrop, tireOD):

    tireRadius = tireOD/2.0 
    
    isSTL = 0 
    saveProfile=[]
    for pf in profile: 
        if pf[0] >=10.000: 
            isSTL = 1 
        if pf[0] < 0: 
            break 
        saveProfile.append(pf)

    if isSTL ==1:
        dropDiff = 0
        dropDiff = CheckTBR_STL_Tangential(shoDrop, profile)

    if  dropDiff !=0: 
        if dropDiff > 0: r = -0.5 
        else: r = 0.5
        tempProfile, r = AddAdditionalRadiusForShoDrop(profile=profile, shiftDrop=dropDiff, r=r, halfOD=tireRadius)
        _, dst, drop = Call_TD_Arc_length_calculator(tempProfile, h_dist=0, totalwidth=1)
        lastPoint=[dst, tireRadius-drop]

        
        points=[[0.0, tireRadius]]
        pe = [0, 0, 0, tireRadius]
        tP = []
        for pf in profile:
            tP.append(pf)
            start = pe
            if pf[0]>=10.0 or pf[0]<0: 
                break 
            _, dst, drop = Call_TD_Arc_length_calculator(tP, h_dist=0, totalwidth=1)
            points.append([dst, tireRadius-drop])

        points.append(lastPoint)
    else: 
        points=[[0.0, tireRadius]]
        pe = [0, 0, 0, tireRadius]
        tP = []
        for pf in profile:
            tP.append(pf)
            start = pe
            if pf[0]<0: 
                break 
            _, dst, drop = Call_TD_Arc_length_calculator(tP, h_dist=0, totalwidth=1)
            points.append([dst, tireRadius-drop])

    for pf in saveProfile:
        print("r=%8.1f, l=%6.2f"%(pf[0]*1000, pf[1]*1000))

    for pt in points:
        print("position(x, y),%10.3f,%10.3f"%(pt[0]*1000, pt[1]*1000))



def CheckTBR_STL_Tangential(shoDrop, profile):
    if shoDrop ==0: 
        _, _, shoulderDrop = TD_Arc_length_calculator(profile, totalwidth=1)
        print ("## Shoulder Drop calculated.")
        print ("   Shoulder Drop =%.2fmm"%(self.shoulderDrop*1000))
        return 0 
    
    if profile[-1][0] < 0: 
        del(profile[-1])
    
    _, _, drop = TD_Arc_length_calculator(profile, totalwidth=1)
    if round(shoDrop, 4) == round(drop, 4): 
        print ("** Shoulder Drop =%.2fmm"%(shoDrop*1000))
        return 0 
    
    print ("* Profile Shoulder Drop =%.2f\n  Tangential Sho.Drop=%.2f, Drop shift=%.2f"%(shoDrop*1000, drop*1000, (shoDrop-drop)*1000))
    return round(drop - shoDrop, 5)


def Call_TD_Arc_length_calculator(profile, h_dist=0, totalwidth=0): 
    #  def TD_Arc_length_calculator(profile, h_dist=0, totalwidth=0, msh_return=0): 
    if totalwidth == 1: 
        length, dist, drop = TD_Arc_length_calculator(profile, h_dist=h_dist, totalwidth=totalwidth, msh_return=0)
        return length, dist, drop 
    else: 
        length, _ = TD_Arc_length_calculator(profile, h_dist=h_dist, totalwidth=totalwidth, msh_return=0)
        return length

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

def AddAdditionalRadiusForShoDrop(profile=[], shiftDrop=0.0, r=-0.5, halfOD=0.0): 
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
        _, dst, drop = Call_TD_Arc_length_calculator(tmp, h_dist=0, totalwidth=1)
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

    return profile, r 

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

if __name__=="__main__":


    main(profile, shoDrop, tireOD)
