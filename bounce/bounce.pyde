import random
g = 0.01
wind = 0.0

# electron shell radius
er = 1

#random number
rn = lambda a,b: map(random.random(),0,1,a,b)
cbrt = lambda a: pow(a,1.0/3.0)

elements = {
            
            1:{'symbol':'H', 'd':cbrt(10.0)+er, 'col':[255,0,0]},
            2:{'symbol':'He', 'd':cbrt(20.0)+er, 'col':[255,192,203]},
            3:{'symbol':'Li', 'd':cbrt(30.0)+er, 'col':[175,175,175]},
            4:{'symbol':'Be', 'd':cbrt(40.0)+er, 'col':[230,150,255]},
            5:{'symbol':'B', 'd':cbrt(50.0)+er, 'col':[105,110,160]},
            6:{'symbol':'C', 'd':cbrt(60.0)+er, 'col':[0,0,0]}

            }
class Circle:
    def __init__(self, x, y, d=10.0, vx=2.0, vy=0.0, ax=wind, ay=g, ele=1):
        self.ele = random.randint(1,len(elements))
        self.pos = PVector(x,y)
        self.d = elements[self.ele]['d']
        self.v = PVector(vx,vy)
        self.a = PVector(ax,ay)
        self.m = 4.0/3.0*PI*pow((self.d/2),3)
        #mechanical energy (initial)
        self.mE = 0.5*self.m*self.v.mag()**2+(height-self.pos.y)*self.m*g
        
        # idt=inverse dt (1/dt) -> bigger = more precise
        self.idt = 5.0
        self.col = elements[self.ele]['col']
        
    def render(self):
        fill(self.col[0],self.col[1],self.col[2])
        circle(self.pos.x,self.pos.y,self.d)
        
    def move(self):
        for i in range(int(self.idt)):
            self.pos += self.v*(1/self.idt)+self.a*pow(1/self.idt,2)*0.5
            self.v.add(self.a*(1/self.idt))
        self.a = PVector(wind,g)
        
        if self.pos.x > width - self.d/2:
            self.v.x = -abs(self.v.x)
        elif self.pos.x < self.d/2:
            self.v.x = abs(self.v.x)
        if self.pos.y > height - self.d/2:
            self.v.y = -abs(self.v.y)
        elif self.pos.y < self.d/2:
            self.v.y = abs(self.v.y)
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
n = 30

def setup():
    size(1000, 700)
    background(255)
    noStroke()
    for i in range(n):
        list1.append(Circle(width/2+rn(-width/2,width/2),height/2+rn(-height/2,height/2),d=rn(1,15),vx=rn(-6.0,6.0),vy=rn(-6.0,6.0)))
        
            
    
def draw():
    mE = 0
    background(255)
    for i in list1:
        i.render()
        i.move()
        mE += i.mE
    print(str(mE) + " J")
    for j in range(len(list1)):
        for k in range(j+1,len(list1)):
            list1[k].check_collide(list1[j])

    
