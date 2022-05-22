import random
g = 0.1
wind = 0.0

# electron shell radius
er = 1.0

mv = PVector(0.0,0.0) # speed of mouse dragged

#random number
rn = lambda a,b: map(random.random(),0,1,a,b)
cbrt = lambda a: pow(a,1.0/3.0)

elements = {
            
            1:{'symbol':'H', 'd':cbrt(10.0)+er, 'freq': 75, 'vfx':{'col':[255,255,255], 'stroke':1}},
            2:{'symbol':'He', 'd':cbrt(20.0)+er, 'freq': 35, 'vfx':{'col':[255,192,203], 'stroke':0}},
            
            3:{'symbol':'Li', 'd':cbrt(30.0)+2*er, 'freq': 20, 'vfx':{'col':[175,175,175], 'stroke':0}},
            4:{'symbol':'Be', 'd':cbrt(40.0)+2*er, 'freq': 10, 'vfx':{'col':[230,150,255], 'stroke':0}},
            5:{'symbol':'B', 'd':cbrt(50.0)+2*er, 'freq': 10, 'vfx':{'col':[105,110,160], 'stroke':0}},
            6:{'symbol':'C', 'd':cbrt(60.0)+2*er, 'freq': 40, 'vfx':{'col':[0,0,0], 'stroke':0}},
            7:{'symbol':'N', 'd':cbrt(70.0)+2*er, 'freq': 50, 'vfx':{'col':[0,0,255], 'stroke':0}},
            8:{'symbol':'O', 'd':cbrt(80.0)+2*er, 'freq': 30, 'vfx':{'col':[255,0,0], 'stroke':0}},
            9:{'symbol':'F', 'd':cbrt(90.0)+2*er, 'freq': 10, 'vfx':{'col':[0,200,0], 'stroke':0}},
            10:{'symbol':'Ne', 'd':cbrt(100.0)+2*er, 'freq': 15, 'vfx':{'col':[255,100,0], 'stroke':0}}

            }
# compiles a list of elements, where each element appears at a specific frequency
t_freq = []
for i in range(1,len(elements)+1):
    for j in range(elements[i]['freq']):
        t_freq.append(i)
    
class Circle:
    def __init__(self, x, y, d=10.0, vx=2.0, vy=0.0, ax=wind, ay=g, ele=1, ch=0):
        self.ele = t_freq[random.randint(0,len(t_freq)-1)] # element number
        self.pos = PVector(x,y)
        self.d = elements[self.ele]['d'] # diameter
        self.v = PVector(vx,vy) # velocity
        self.a = PVector(ax,ay) # acceleration
        self.m = 4.0/3.0*PI*pow((self.d/2),3) # mass
        self.ch = 0 # charge
        # mechanical energy (initial)
        self.mE = 0.5*self.m*self.v.mag()**2+(height-self.pos.y)*self.m*g
        
        # idt=inverse dt (1/dt) -> bigger = more precise
        self.idt = 5.0
        self.col = elements[self.ele]['vfx']['col']
        
    def render(self):
        """
        stroke(0)
        strokeWeight(0.5)
        """
        stroke(0) # not sure if this is necessary but just in case
        if elements[self.ele]['vfx']['stroke'] == 0:
            noStroke()
        elif elements[self.ele]['vfx']['stroke'] != 0:
            stroke(0)
            strokeWeight(0.2)
        fill(self.col[0],self.col[1],self.col[2])
        circle(self.pos.x,self.pos.y,self.d)
        
    def move(self):
        for i in range(int(self.idt)):
            self.pos += self.v*(1/self.idt)+self.a*pow(1/self.idt,2)*0.5
            self.v.add(self.a*(1/self.idt))
        self.a = PVector(wind,g)
        
        if self.pos.x > box_BR.x - self.d/2:
            #self.pos.x = box_BR.x - self.d/2
            self.v.x = -abs(self.v.x)
            self.v.add(mv)
        elif self.pos.x < box_UL.x + self.d/2:
            #self.pos.x = box_UL.x + self.d/2
            self.v.x = abs(self.v.x)
            self.v.add(mv)
        if self.pos.y > box_BR.y - self.d/2:
            #self.pos.y = box_BR.y - self.d/2
            self.v.y = -abs(self.v.y)
            self.v.add(mv)
        elif self.pos.y < box_UL.y + self.d/2:
            #self.pos.y = box_UL.y + self.d/2
            self.v.y = abs(self.v.y)
            self.v.add(mv)
        self.mE = 0.5*self.m*self.v.mag()**2+(height-self.pos.y)*self.m*g
        # mechanical energy of each particle
        # print(0.5*self.m*self.v.mag()**2+(height-self.pos.y)*self.m*g)
        
    def check_collide(self,c2):
        if dist(self.pos.x,self.pos.y,c2.pos.x,c2.pos.y) <= self.d/2+c2.d/2:
            n = self.pos.copy().sub(c2.pos)
            dif = (self.d/2+c2.d/2) - n.mag() 
            r = self.m/(self.m+c2.m)
            self.pos.sub(n.normalize().mult(-dif/r))
            c2.pos.sub(n.normalize().mult(-dif/(1-r)))
            v1 = (self.v*(self.m-c2.m)+2*c2.m*c2.v)/(self.m+c2.m)
            v2 = (c2.v*(c2.m-self.m)+2*self.m*self.v)/(c2.m+self.m)
            self.v = v1
            c2.v = v2
            fill(255,0,0)
            #circle((self.pos.x+c2.pos.x)/2,(self.pos.y+c2.pos.y)/2,(self.d+c2.d)*2)
        

list1 = []
n = 12

w = 1000
h = 700
# box width and height
bw = 850
bh = 600

def setup():
    size(w, h)
    background(255)
    #noStroke()
    for i in range(n):
        list1.append(Circle(width/2+rn(-bw/2,bw/2),height/2+rn(-bh/2,bh/2),d=rn(1,15),vx=rn(-6.0,6.0),vy=rn(-6.0,6.0)))
        

box_UL = PVector((w-bw)/2,(h-bh)/2)
box_UR = PVector((w-bw)/2+bw,(h-bh)/2)
box_BR = PVector((w-bw)/2+bw,(h-bh)/2+bh)
box_BL = PVector((w-bw)/2,(h-bh)/2+bh)
box_d = PVector(0,0) # box's displacement
    
def draw():
    mE = 0
    background(255)
    pushMatrix()
    translate(box_d.x,box_d.y)
    fill(255)
    stroke(1)
    rect(box_UL.x,box_UL.y,bw,bh)
    popMatrix()
    for i in list1:
        i.render()
        i.move()
        mE += i.mE
    print(str(mE) + " J")
    for j in range(len(list1)):
        for k in range(j+1,len(list1)):
            list1[k].check_collide(list1[j])
    
def mouseDragged():
    box_UL.x,box_UR.x,box_BR.x,box_BL.x = box_UL.x+mouseX-pmouseX,box_UR.x+mouseX-pmouseX,box_BR.x+mouseX-pmouseX,box_BL.x+mouseX-pmouseX
    box_UL.y,box_UR.y,box_BR.y,box_BL.y = box_UL.y+mouseY-pmouseY,box_UR.y+mouseY-pmouseY,box_BR.y+mouseY-pmouseY,box_BL.y+mouseY-pmouseY
    global mv
    mv = PVector(float(mouseX-pmouseX),float(mouseY-pmouseY))

def mouseReleased():
    global mv
    mv = PVector(0,0)
    

    
