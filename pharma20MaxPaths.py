from collections import defaultdict
import random
import colorsys

import os
import sys

placement= {1:1,2:2,3:2,4:2,5:2,6:3,7:3,8:4,9:4,10:4,11:4,12:5,13:5,14:6,15:6,16:6,17:6,18:7,19:7,20:8,21:8,22:8,23:8,24:9,25:9,26:10,27:10,28:10,29:10}

ordering = defaultdict(list)
for i in placement: ordering[placement[i]].append(i)

block_width = 20
block_space = 30
block_height = 10
row_space=35

def get_corners(nodeId,xstart):
    row = placement[nodeId]
    order = ordering[row].index(nodeId)
    x_blc = block_space*order+xstart
    if row==1:
        x_blc = x_blc+block_space*1.5
        y_blc = 3*row_space+5
    elif row%2==1:
        x_blc = 2*block_space*order+xstart
        x_blc = x_blc+block_space*.5
        y_blc = row*row_space+5
    else:
        y_blc = row*row_space+5
    x_brc = x_blc+block_width
    y_brc = y_blc
    x_trc = x_brc
    y_trc = y_brc+block_height
    x_tlc = x_blc
    y_tlc = y_trc
    return [(x_blc,y_blc),(x_brc,y_brc),(x_trc,y_trc),(x_tlc,y_tlc)]

def draw_squares(nodeId, weight, xstart):
    #h, s, l = 0.15029761904761904, 1.00, .4 + .6*(1.-weight)
    global MAXEND
    h, s, l = 0.15029761904761904, 1.00, .5 + .5*(1.-weight/MAXEND)
    r, g, b = colorsys.hls_to_rgb(h,l,s)
    row = placement[nodeId]
    order = ordering[row].index(nodeId)
    (x_blc,y_blc),(x_brc,y_brc),(x_trc,y_trc),(x_tlc,y_tlc) = get_corners(nodeId, xstart)
    print("newline poly pcfill %s %s %s linethickness 0.25 pts"%(r,g,b))
    print("    %s %s %s %s %s %s %s %s"%(x_blc,y_blc,x_brc,y_brc,x_trc,y_trc,x_tlc,y_tlc))
    print("")
    label = str(nodeId)
    duration = "0"
    if order == 0: duration = "<2"
    elif order == 1: duration = "2-4"
    elif order == 2: duration = "4-9"
    elif order == 3: duration = "9+"
    duration += " months"
    if row==1: 
        label = "Start Drug"
        duration = "at 20-39 mg"
    elif row==2:
        label = "<20mg for"
    elif row==3:
        if order ==0:
            label = "Increase to"
        else:
            label = "Decrease to"
        duration = "20-39mg"
    elif row==4:
        label = "20-39mg for"
    elif row==5:
        if order ==0:
            label = "Increase to"
        else:
            label = "Decrease to"
        duration = "40-59mg"
    elif row==6:
        label = "40-59mg for"
    elif row==7:
        if order ==0:
            label = "Increase to"
        else:
            label = "Decrease to"
        duration = "60-80mg"
    elif row==8:
        label = "60-80mg for"
    elif row==9:
        if order ==0:
            label = "Increase to"
        else:
            label = "Decrease to"
        duration = " Above Max"
    elif row==10:
        label = "Above Max for"

    print("newstring hjc vjc fontsize 5")
    print(" font Times-Roman x %s y %s : %s"%( x_blc+block_width*.5,y_blc+block_height*.75,label))
    print("")
    print("newstring hjc vjc fontsize 5")
    print(" font Times-Roman x %s y %s : %s"%( x_blc+block_width*.5,y_blc+block_height*.5,duration))
    print("")
    print("newstring hjc vjc fontsize 5")
    print(" font Times-Roman x %s y %s : (%.3f)"%( x_blc+block_width*.5,y_blc+block_height*.25, weight))
    print("")

from math import log2
def draw_arrows(n1,n2, weight, xstart):
    # draw a triangle and a line to make an arrow
    MIN_WIDTH= .25 #*8
    MAX_WIDTH = 7.5*2
    thickness = MIN_WIDTH + (MAX_WIDTH - MIN_WIDTH)*weight
    src_row = placement[n1]
    dest_row = placement[n2]
    src_order = ordering[src_row].index(n1)
    (sx_blc,sy_blc),(sx_brc,sy_brc),(sx_trc,sy_trc),(sx_tlc,sy_tlc) = get_corners(n1,xstart)
    (dx_blc,dy_blc),(dx_brc,dy_brc),(dx_trc,dy_trc),(dx_tlc,dy_tlc) = get_corners(n2,xstart)

    if src_row < dest_row:
        x_src, y_src = (sx_trc+sx_tlc)/2., sy_trc 
        x_dest, y_dest = (dx_blc+dx_brc)/2., dy_blc
    elif src_row >= dest_row:
        x_src, y_src = (sx_brc+sx_blc)/2., sy_blc 
        x_dest, y_dest = (dx_tlc+dx_trc)/2., dy_tlc

    height = abs(y_dest - y_src)
    width = abs(x_dest - x_src)
    #if width <= block_space*.75: 
    #    # FIX: width = max(width*.25,1)
    #    width = max(width*.25,1)
    #    height = max(height*.25,1)
    #    #if weight < .05: 
    #    #    width = width/2.
    #    #    height = height/2.
    #elif width > block_space*2: 
    #    width = max(width*.25,1)
    #    height = max(height*.5,1)
    #    #if weight < .05: 
    #    #    width = width*5.
    #    #    height = height*5.
    #else:
    #    width = width*.75
    #    height = height*.75
    if src_row %2 ==0 and src_row<dest_row: # going from even to odd upward (eou) so curve inward
        x_src = x_src - block_width*.25
        x_dest = x_dest
        # inward curve left
        if x_dest < x_src:
            xp1 = x_src-log2(height) #*.25
            yp1 = y_src + log2(width) # special
            xp2 = x_dest - log2(height) #*.25
            yp2 = y_dest - log2(width) #*.25
        # inward curve right
        if x_dest >= x_src:
            xp1 = x_src + log2(height) #*.25 #todo
            yp1 = y_src + log2(width)# special
            xp2 = x_dest+log2(height) #*.25 #todo
            yp2 = y_dest - log2(width) #*.25 #todo
    elif src_row %2 ==0 and src_row>=dest_row: # going from even to odd downward (eod)
        x_src = x_src + block_width*.25
        if x_dest < x_src: #curve left
            xp1 = x_src - log2(height) #*.25 #todo
            yp1 = y_src - log2(width) # special
            xp2 = x_dest-log2(height) #*.25 #todo
            yp2 = y_dest - log2(width) #*.25 #todo
        elif x_dest >= x_src: #curve right
            xp1 = x_src + log2(height) #*.25 #todo
            yp1 = y_src - log2(width) # special
            xp2 = x_dest + log2(height) #*.25 #todo
            yp2 = y_dest + log2(width) #*.25 #todo
    elif src_row %2==1 and src_row < dest_row: # going from odd to even upward (oeu)
        x_dest = x_dest - block_width*.25
        if x_dest < x_src: # curve left
            xp1 = x_src - log2(height) #*.25
            yp1 = y_src + log2(width) # special
            xp2 = x_dest - log2(height) #*.25
            yp2 = y_dest - log2(width) # * .25
        if x_dest >= x_src: # curve right
            xp1 = x_src + log2(height) #*.25
            yp1 = y_src + log2(width) # special
            xp2 = x_dest + log2(height) #*.25
            yp2 = y_dest - log2(width) # * .25
            if abs(x_dest - x_src) >=block_space*2:
                yp2-=5
                xp2+=5
    elif src_row %2==1 and src_row >= dest_row: # odd to even downward (oed)
        x_dest = x_dest + block_width*.25
        if x_dest < x_src: # curve left
            xp1 = x_src - log2(height) #*.25
            yp1 = y_src - log2(width) # special
            xp2 = x_dest - log2(height) #*.25
            yp2 = y_dest + log2(width) # * .25
        if x_dest >= x_src: # curve right
            xp1 = x_src + log2(height) #*.25
            yp1 = y_src - log2(width) # special
            xp2 = x_dest + log2(height) #*.25
            yp2 = y_dest - log2(width) # * .25

    #print("newline poly pcfill .0 .0 .0 pts")
    #print("    %s %s %s %s %s %s"%(x_dest,y_dest,x_dest+thickness+2,y_dest-1.5,x_dest-thickness-2,y_dest-1.5))
    print("newline bezier linethickness %s asize %s %s pts"%(thickness, thickness,thickness+1))
    if src_row<dest_row:
        toffset = min(thickness,5)
        midy = (y_src+y_dest)/2
        midx = (x_src+x_dest)/2
        _34y = (y_src+midy)/2.
        #print("    %s %s %s %s %s %s %s %s %s %s %s %s %s %s"%(x_src,y_src+toffset*.25,xp1,yp1,xp2,yp2-toffset,x_dest,y_dest-toffset*.55,x_dest,y_dest-toffset*.5,x_dest,y_dest-toffset*.35,x_dest,y_dest-toffset*.3))
        print("    %s %s %s %s %s %s %s %s"%(x_src,y_src+toffset*.25,midx,midy,x_dest,midy,x_dest,y_dest-toffset*.5))
        print("newline rarrow linethickness .25 asize %s %s pts %s %s %s %s"%(4,thickness+1,x_dest,y_dest-toffset*.5,x_dest,y_dest))
    elif src_row>dest_row:
        toffset = min(thickness,5)
        midy = (y_src+y_dest)/2
        _34y = (y_src+midy)/2.
        midx = (x_src+x_dest)/2
        print("    %s %s %s %s %s %s %s %s"%(x_src,y_src-toffset*.25,midx,midy,x_dest,midy,x_dest,y_dest+toffset*.5))
        #print("    %s %s %s %s %s %s %s %s %s %s %s %s %s %s"%(x_src,y_src-thickness*.25,xp1,yp1,xp2,yp2+2,x_dest,y_dest+thickness*.55,x_dest,y_dest+thickness*.5,x_dest,y_dest+thickness*.35,x_dest,y_dest+thickness*.3))
        print("newline rarrow linethickness .25 asize %s %s pts %s %s %s %s"%(4,thickness+1,x_dest,y_dest+toffset*.5,x_dest,y_dest))

def draw_legend(xstart):
    # draw color grid
    hbw = block_width*.5
    xblc = xstart+block_width
    yblc = 350 + 35 * 2
    leg_block_width = block_width * 4
    leg_block_height = block_height
    lwidth = 2
    bb = yblc - block_height - 7.5
    # box in the legend
    print("newline poly linethickness 1 color 0 0 0 pfill -1 pts")
    print("    %s %s %s %s %s %s %s %s"%(xblc-hbw,bb,xblc+leg_block_width+hbw,bb,xblc+leg_block_width+hbw,bb+leg_block_height*3.5,xblc-hbw,bb+leg_block_height*3.5))
    print("")
    # box in the gradient colors
    print("newline poly linethickness 1 color 0 0 0 pfill -1 pts")
    #print("    %s %s %s %s %s %s %s %s"%(xblc-lwidth*.25,yblc-lwidth*.25,xblc+leg_block_width+lwidth*1.25,yblc-lwidth*.25,xblc+leg_block_width+lwidth*1.25,leg_block_height+lwidth*.25,xblc-lwidth*.25,leg_block_height+lwidth*.25))
    print("    %s %s %s %s %s %s %s %s"%(xblc-.5,yblc-.5,xblc+leg_block_width+lwidth+.5,yblc-.5,xblc+leg_block_width+lwidth+.5,yblc+leg_block_height+.5,xblc-.5,yblc+leg_block_height+.5))
    # draw_scale
    GRAD_SCALE = "0."+str(int(round(MAXEND*10)))
    HALF_GRAD_SCALE = str(round(MAXEND*10)/20)
    print("newstring hjc vjc fontsize 5")
    print(" font Times-Roman x %s y %s : %s"%( xblc,yblc-3,"0.0"))
    print("")
    print("newstring hjc vjc fontsize 5")
    print(" font Times-Roman x %s y %s : %s"%( xblc+leg_block_width*.5,yblc-3,HALF_GRAD_SCALE))
    print("")
    print("newstring hjc vjc fontsize 5")
    print(" font Times-Roman x %s y %s : %s"%( xblc+leg_block_width,yblc-3,GRAD_SCALE))
    print("")
    # draw gradient
    weights = range(0,41)
    for i in weights:
        h, s, l = 0.15029761904761904, 1.00, .5 + .5*(1.-i/40.)
        r, g, b = colorsys.hls_to_rgb(h,l,s)
        x_blc = lwidth*i+xblc
        y_blc = yblc
        x_brc = x_blc+lwidth #*1.05
        y_brc = yblc
        x_trc = x_brc
        y_trc = y_brc+block_height #*1.05
        x_tlc = x_blc
        y_tlc = y_trc
        print("newline poly pcfill %s %s %s color %s %s %s linethickness 0.0000001 pts"%(r,g,b,r,g,b))
        print("    %s %s %s %s %s %s %s %s"%(x_blc,y_blc,x_brc,y_brc,x_trc,y_trc,x_tlc,y_tlc))
        print("")
    # draw example lines
    line_start = xblc #+ leg_block_width*2
    line_y = 350 + 35 * 2 -block_height #yblc + leg_block_height*.5
    line_width = 1
    # draw_scale
    ticks = 75
    print("newstring hjc vjc fontsize 5")
    print(" font Times-Roman x %s y %s : %s"%( line_start,line_y-5,"%.2f"%MAXWEIGHT))
    print("")
    print("newstring hjc vjc fontsize 5")
    print(" font Times-Roman x %s y %s : %s"%( line_start+ticks*line_width*.5,line_y-5,"%.2f"%(MAXWEIGHT/2)))
    print("")
    print("newstring hjc vjc fontsize 5")
    print(" font Times-Roman x %s y %s : %s"%( line_start+ticks*line_width,line_y-5,"0.0"))
    print("")
    # arrow_legend
    thicknesses = range(ticks,1,-1)
    for i in thicknesses:
        print("newline linethickness %s pts %s %s %s %s"%((2*i)/10.,line_start,line_y,line_start+line_width,line_y))
        print("")
        line_start = line_start+line_width
    

def write_text():
    pass


MAXEND =0
from collections import Counter
def load_data(filename):
    global MAXWEIGHT,MAXEND
    G = Counter()
    with open(filename) as f:
        for i,line in enumerate(f.readlines()):
            if i == 0: header = line.strip()
            else:
                src,dest,weight = line.strip().split(",")
                G[(int(src),int(dest))]=float(weight)
                if int(dest)==-1: MAXEND=max(MAXEND,float(weight))
                else: MAXWEIGHT=max(MAXWEIGHT,float(weight))
    return header,G

def draw_graph(t,G,xstart):
    nodes= set()
    for i,j in G:
        nodes.add(i)
        nodes.add(j)
    #print(G)
    nodes.remove(-1)
    for i in nodes:
        draw_squares(i,G[(i,-1)],xstart)
    for i,j in G:
        if j==-1: continue
        draw_arrows(i,j,G[(i,j)],xstart)

    offset = 10
    topper = 20
    print("newline poly pfill -1 linethickness 1.0 pts")
    print("    %s %s %s %s %s %s %s %s"%(xstart-offset,5+row_space-offset,xstart+block_space*3+block_width+offset,5+row_space-offset,xstart+block_space*3+block_width+offset,5-offset+row_space*10+block_height+offset+topper,xstart-offset,5-offset+row_space*10+block_height+offset+topper))
    print("")
    print("newstring hjc vjc fontsize 15")
    print(" font Times-Roman x %s y %s : %s"%( (xstart+xstart+block_space*3+block_width)/2.,5-offset+row_space*10+block_height+offset+topper-6,t))
    print("")


MAXWEIGHT=0
def gen_data():
    G = {}
    global MAXWEIGHT,MAXEND
    for i in range(1,24):
        G[(i,-1)]=ra()
        MAXEND = max(MAXEND,G[(i,-1)])
    arrows = {1:[2,3,4,5],2:[6],3:[6],4:[6],5:[6],6:[8,9,10,11],7:[2,3,4,5],8:[12,7],9:[12,7],10:[12,7],11:[12,7],12:[14,15,16,17],14:[13,18],15:[18],16:[18],18:[20,21,22,23]}
    for i in arrows:
        for j in arrows[i]:
            G[(i,j)]=ra()
            MAXWEIGHT = max(MAXWEIGHT,G[(i,j)])
    return G

def scale(G):
    global MAXWEIGHT
    for k in G:
        if k[-1]==-1: continue
        G[k] = G[k]/MAXWEIGHT

ra = random.random
def main(*fs):
    #try: f1,f2 = fs
    #except: f1,f2=fs[0],None
    #if not (f1 is None):
    #    t1,G1 = load_data(f1)
    #    scale(G1)
    
    GRAPHSPACE=30
    xstart = 25
    end = xstart + GRAPHSPACE + block_space*10+10
    end = 55*len(fs)
    print("newgraph")
    print("xaxis min 0 max %s nodraw"%end) #110
    print("yaxis min 5 max 125 nodraw")
    print("")
    #draw_graph(t1,G1,xstart)
    for i,f in enumerate(fs):
        t,G = load_data(f)

    for i,f in enumerate(fs):
        if i == 0:
            xstart = 25
        else:
            xstart = xstart + GRAPHSPACE + block_space*4
        t,G = load_data(f)
        scale(G)
        draw_graph(t,G,xstart)
    #for i in range(1,24):
    #    draw_squares(i,ra(),xstart)
    #arrows = {1:[2,3,4,5],2:[6],3:[6],4:[6],5:[6],6:[8,9,10,11],7:[2,3,4,5],8:[12,7],9:[12,7],10:[12,7],11:[12,7]}
    #for i in arrows:
    #    for j in arrows[i]:
    #        draw_arrows(i,j,ra(),xstart)

    # draw square and set title
    #print("newline poly pfill -1 linethickness 1.0 pts")
    #print("    %s %s %s %s %s %s %s %s"%(xstart-offset,5+row_space-offset,xstart+block_space*3+block_width+offset,5+row_space-offset,xstart+block_space*3+block_width+offset,5-offset+row_space*8+block_height+offset+topper,xstart-offset,5-offset+row_space*8+block_height+offset+topper))
    #print("")
    #print("newstring hjc vjc fontsize 15")
    #print(" font Times-Roman x %s y %s : %s"%( (xstart+xstart+block_space*3+block_width)/2.,5-offset+row_space*8+block_height+offset+topper-6,"VISN 9"))
    #print("")

    draw_legend(xstart)

if __name__=="__main__":
    main(*sys.argv[1:])
