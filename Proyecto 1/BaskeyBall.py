# By Alberto Caro
# Ingeniero Civil Informatico
# Dr.(c) Ciencias de la Ingenieria - PUC
# Ingeniero IoT and DataScience
#--------------------------------------------------------
#__________      ___.           __  .__               
#\______   \ ____\_ |__   _____/  |_|__| ____ _____   
# |       _//  _ \| __ \ /  _ \   __\  |/ ___\\__  \  
# |    |   (  <_> ) \_\ (  <_> )  | |  \  \___ / __ \_
# |____|_  /\____/|___  /\____/|__| |__|\___  >____  /
#        \/           \/    Alberto Caro    \/     \/ 
#--------------------------------------------------------
from __future__ import division
from vpython import *

import math, random as ra, ctypes as ct

nMAX_ROBOTS = 10

#-----------------------------------------------------------------------------------------------------
# Estructura de Datos del Robot la cual la puede modificar para configurar 
# el modelo del robot Uniciclo
#-----------------------------------------------------------------------------------------------------
class eRobot(ct.Structure):
  _fields_ = [
              ('nBoId',ct.c_ubyte), # Identificador del Robot
              ('nAngu',ct.c_int  ), # Direcion Robot Plano XZ
              ('nVelo',ct.c_float), # Velocidad Robot {0.7,1,1.5,2,2.5,3}
              ('nStep',ct.c_int  ), # Pasos a mover Robot
              ('nPryX',ct.c_float), # Proyeccion en X-> nVelo*cos(rad(nAngu))
              ('nPryZ',ct.c_float), # Proyeccion en Z-> nVelo*sin(rad(nAngu))
              ('nPosX',ct.c_float), # Posicion X Robot en cancha-> x += nPryX
              ('nPosZ',ct.c_float), # Posicion Z Robot en cancha-> z += nPryZ
              ('nTime',ct.c_int  )  # Contador Disparo Ball
             ]

#-----------------------------------------------------------------------------------------------------
# Estructura de Datos de la Pelota la cual la puede modificar para configurar 
# el modelo del robot Uniciclo
#-----------------------------------------------------------------------------------------------------
class ePelo(ct.Structure):
  _fields_ = [
              ('nAccG',ct.c_float), # Aceleracion de Gravedad (9.8m/s^2)
              ('nVelo',ct.c_int  ), # Velocidad Disparo de la Pelota (m/s) 
              ('nAngE',ct.c_uint ), # Angulo Elevacion de la Pelota antes del Disparo Plano XY Grados
              ('nAngD',ct.c_int  ), # Angulo Direccion de la Pelota (Heading) (Plano XZ) en Grados
              ('nPryY',ct.c_float), # Proyeccion de la Pelota Eje Y (Plano XY)
              ('nVe_X',ct.c_float), # Velocidad  de la Pelota Eje X 
              ('nVe_Y',ct.c_float), # Velocidad  de la Pelota Eje Y 
              ('nVe_Z',ct.c_float), # Velocidad  de la Pelota Eje Z
              ('nPosX',ct.c_float), # Posicion de la Pelota   Eje X
              ('nPosY',ct.c_float), # Posicion de la Pelota   Eje Y
              ('nPosZ',ct.c_float), # Posicion de la Pelota   Eje Z
              ('nSamp',ct.c_float), # Sample Euler Integracion 
              ('nDi_T',ct.c_float), # Diferencial del Tiempo Sampling
              ('lSw_T',ct.c_float)  # Switch Timer Pelotas
             ]

#-----------------------------------------------------------------------------------------------------
# Retorna el Angulo de Direccion Aleatorio del Robot.-
#-----------------------------------------------------------------------------------------------------
def Get_Angulo_R():
    return ra.choice([0,15,30,45,60,75,90,105,120,135,150,165,180,195,210,225,240,255,270,285,300,315
                      ,330,345])

#-----------------------------------------------------------------------------------------------------
# Retorna la Velocidad Aleatoria del Robot.-
#-----------------------------------------------------------------------------------------------------
def Get_Velocidad_R():
    return ra.choice([0.0,1.0,2.0,4.0,5.0,6.0])

#-----------------------------------------------------------------------------------------------------
# Retorna el Angulo Elevacion de la Pelota.-
#-----------------------------------------------------------------------------------------------------
def Get_Angulo_P():
    return ra.choice([5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80])

#-----------------------------------------------------------------------------------------------------
# Retorna el Angulo Direccion de la Pelota.-
#-----------------------------------------------------------------------------------------------------
def Get_Angulo_D():
    return ra.choice([-50,-45,-40,-35,-30,-25,-20,-15,-10,-5,0,5,10,15,20,25,30,35,40,45,50])

#-----------------------------------------------------------------------------------------------------
# Retorna la Velocidad de Disparo de la Pelota.-
#-----------------------------------------------------------------------------------------------------
def Get_Velocidad_P():
    return ra.choice([10,20,30,40,50,60,70,80,90,100,110,120,130])

#-----------------------------------------------------------------------------------------------------
# Init Valores de todos los Robots.-
#-----------------------------------------------------------------------------------------------------
def Robot_Init(nPos):
    aRobots[nPos].nBoId = nPos
    aRobots[nPos].nAngu = Get_Angulo_R()
    aRobots[nPos].nVelo = Get_Velocidad_R()
    aRobots[nPos].nStep = ra.randint(10,200)
    aRobots[nPos].nPryX = aRobots[nPos].nVelo*cos(math.radians(aRobots[nPos].nAngu))
    aRobots[nPos].nPryZ = aRobots[nPos].nVelo*sin(math.radians(aRobots[nPos].nAngu))
    aRobots[nPos].nPosX = aRobots[nPos].nPryX
    aRobots[nPos].nPosZ = aRobots[nPos].nPryZ
    aRobots[nPos].nTime = ra.randint(5000,10000)
    return

#-----------------------------------------------------------------------------------------------------
# Init Valores de las Pelotas
#-----------------------------------------------------------------------------------------------------
def Pelotas_Init():
    for i in range(nMAX_ROBOTS):
        aPelota[i].nAccG = 9.8
        aPelota[i].nVelo = Get_Velocidad_P() # Velocidad de Disparo de la Pelota
        aPelota[i].nAngE = Get_Angulo_P()    # Angulo de Elevacion  de la Pelota
        aPelota[i].nAngD = Get_Angulo_D()    # Angulo de Direccion  de la Pelota (Heading)
        # Proyecciones de los componentes (X,Y,Z)
        aPelota[i].nPryY = aPelota[i].nVelo * math.cos(math.radians(aPelota[i].nAngE))
        aPelota[i].nVe_X = aPelota[i].nPryY * math.cos(math.radians(aPelota[i].nAngD))
        aPelota[i].nVe_Y = aPelota[i].nVelo * math.sin(math.radians(aPelota[i].nAngE))
        aPelota[i].nVe_Z = aPelota[i].nPryY * math.sin(math.radians(aPelota[i].nAngD))
        aPelota[i].nSamp = 0 ; aPelota[i].nDi_T = 0.1
        # Posicion de la Pelota en (X,Y,Z)
        aPelota[i].nPosX = aPelota[i].nVe_X*(aPelota[i].nDi_T)
        aPelota[i].nPosY = aPelota[i].nVe_Y*(aPelota[i].nDi_T)-0.5*aPelota[i].nAccG*(aPelota[i].nDi_T)**2
        aPelota[i].nPosZ = aPelota[i].nVe_Z*(aPelota[i].nDi_T)
        # Timer/Contador para el disparo. Dispara cuando nTime = 0 -> lSw_T = False
        aPelota[i].lSw_T = 'A' > 'B'
    return


#-----------------------------------------------------------------------------------------------------
# Ball Init para Graficar
#-----------------------------------------------------------------------------------------------------
def Ball_Init():
    for i in range(nMAX_ROBOTS):
        aBall[i].pos = aPlayer[i].pos        
    return

#-----------------------------------------------------------------------------------------------------
# Actualiza y Pinta las Pelotas
#-----------------------------------------------------------------------------------------------------
def UpDate_Pelotas():
    for i in range(nMAX_ROBOTS):
        aRobots[i].nTime -= 1
        if aRobots[i].nTime <= 0: 
           aRobots[i].nTime = ra.randint(5000,10000)
           aPelota[i].lSw_T = True
        if aPelota[i].lSw_T:
           aPelota[i].nSamp = aPelota[i].nSamp + aPelota[i].nDi_T
           aPelota[i].nPosX = aPelota[i].nVe_X*(aPelota[i].nSamp)
           aPelota[i].nPosY = aPelota[i].nVe_Y*(aPelota[i].nSamp)-0.5*aPelota[i].nAccG*(aPelota[i].nSamp)**2
           aPelota[i].nPosZ = aPelota[i].nVe_Z*(aPelota[i].nSamp)
           aBall[i].pos = (aPelota[i].nPosX,aPelota[i].nPosY,aPelota[i].nPosZ)
           if aBall[i].pos.y < 0:
              aPelota[i].nSamp = 0 
              aPelota[i].lSw_T = 'A' > 'B'
              aRobots[i].nTime = ra.randint(5000,10000)
              Pelotas_Init() 
    return

#-----------------------------------------------------------------------------------------------------
# Mueve los Robots Blue
#-----------------------------------------------------------------------------------------------------
def Robot_Blue_Move():
    for i in range(0,5):
     aRobots[i].nStep -= 1
     if aRobots[i].nStep <= 0: 
        Robot_Init(i)

     aPlayer[i].pos.x += aRobots[i].nPosX
     aPlayer[i].pos.z += aRobots[i].nPosZ

     if aPlayer[i].pos.x <= -870:
        aPlayer[i].pos.x =  -870
        aRobots[i].nStep = 0
     if aPlayer[i].pos.x >= -50:
        aPlayer[i].pos.x =  -50
        aRobots[i].nStep = 0
     if aPlayer[i].pos.z <= -470:
        aPlayer[i].pos.z =  -470
        aRobots[i].nStep = 0
     if aPlayer[i].pos.z >= +470:
        aPlayer[i].pos.z =  +470
        aRobots[i].nStep = 0
    return

#-----------------------------------------------------------------------------------------------------
# Mueve los Robots Red
#-----------------------------------------------------------------------------------------------------
def Robot_Red_Move():
    for i in range(5,10):
     aRobots[i].nStep -= 1
     if aRobots[i].nStep <= 0: 
        Robot_Init(i)

     aPlayer[i].pos.x += aRobots[i].nPosX
     aPlayer[i].pos.z += aRobots[i].nPosZ

     if aPlayer[i].pos.x <= +50:
        aPlayer[i].pos.x =  +50
        aRobots[i].nStep = 0
     if aPlayer[i].pos.x >= +870:
        aPlayer[i].pos.x =  +870
        aRobots[i].nStep = 0
     if aPlayer[i].pos.z <= -470:
        aPlayer[i].pos.z =  -470
        aRobots[i].nStep = 0
     if aPlayer[i].pos.z >= +470:
        aPlayer[i].pos.z =  +470
        aRobots[i].nStep = 0
    return

#-----------------------------------------------------------------------------------------------------
# Definicion del Mundo 3D y sus Objetos.-
#-----------------------------------------------------------------------------------------------------
scene = canvas(title='Demo', width=1900, height=600, center=vector(0,0,0), background=color.black)


MyMap = box(pos=vector(0,0,0),size=vector(1800,3,1000),color=color.red)
MyBas = box(pos=vector(0,2,0),size=vector(1780,5,980),color=color.gray(0.5))

MyLin = box(pos=vector(0,4,0),size=vector(3,3,1000),color=color.white)

MyBoD = box(pos=vector(900,150,0),size=vector(4,70,140),color=color.red)
MyViI = box(pos=vector(900,60,0),size=vector(3,120,6),color=color.white)
MyArD = ring(pos=vector(874,130,0),radius=25,color=color.white,axis=vector(0,4,0),thickness=2)

MyBoD = box(pos=vector(-900,150,0),size=vector(4,70,140),color=color.blue)
MyViI = box(pos=vector(-900,60,0),size=vector(3,120,6),color=color.white)
MyArI = ring(pos=vector(-874,130,0),radius=25,color=color.white,axis=vector(0,4,0),thickness=2)

MyCy1 = cylinder(pos=vector(0,0,0),radius=50,color=color.red,axis=vector(0,6,0),opacity=1)
MyCy2 = cylinder(pos=vector(0,0,0),radius=20,color=color.white,axis=vector(0,8,0),opacity=1)

#-----------------------------------------------------------------------------------------------------
# Definicion de las propiedades de la Pelota
#-----------------------------------------------------------------------------------------------------
oFr_B1 = compound([sphere(pos=vector(0, 0, 0), radius=6, color=color.blue)])
oFr_B2 = compound([sphere(pos=vector(0, 0, 0), radius=6, color=color.blue)])
oFr_B3 = compound([sphere(pos=vector(0, 0, 0), radius=6, color=color.blue)])
oFr_B4 = compound([sphere(pos=vector(0, 0, 0), radius=6, color=color.blue)])
oFr_B5 = compound([sphere(pos=vector(0, 0, 0), radius=6, color=color.blue)])
oFr_B6 = compound([sphere(pos=vector(0, 0, 0), radius=6, color=color.blue)])
oFr_B7 = compound([sphere(pos=vector(0, 0, 0), radius=6, color=color.blue)])
oFr_B8 = compound([sphere(pos=vector(0, 0, 0), radius=6, color=color.blue)])
oFr_B9 = compound([sphere(pos=vector(0, 0, 0), radius=6, color=color.blue)])
oFr_BA = compound([sphere(pos=vector(0, 0, 0), radius=6, color=color.blue)])
#-----------------------------------------------------------------------------------------------------
# Definicion Robots Equipo Blue
#-----------------------------------------------------------------------------------------------------
# [Resto del código permanece igual hasta la definición de los robots...]

#-----------------------------------------------------------------------------------------------------
# Definicion Robots Equipo Blue - MODIFICADO: frame -> compound
#-----------------------------------------------------------------------------------------------------
# Robot Basket 1
oFr_1 = compound([
    cylinder(pos=vector(0,0,0), radius=15, color=color.blue, axis=vector(0,15,0), opacity=1),
    cylinder(pos=vector(0,13,0), radius=8, color=color.yellow, axis=vector(0,10,0), opacity=1)
], pos=vector(-800,1,-400))

# Robot Basket 2
oFr_2 = compound([
    cylinder(pos=vector(0,0,0), radius=15, color=color.blue, axis=vector(0,15,0), opacity=1),
    cylinder(pos=vector(0,13,0), radius=8, color=color.yellow, axis=vector(0,10,0), opacity=1)
], pos=vector(-400,1,0))

# Robot Basket 3
oFr_3 = compound([
    cylinder(pos=vector(0,0,0), radius=15, color=color.blue, axis=vector(0,15,0), opacity=1),
    cylinder(pos=vector(0,13,0), radius=8, color=color.yellow, axis=vector(0,10,0), opacity=1)
], pos=vector(-800,1,400))

# Robot Basket 4
oFr_4 = compound([
    cylinder(pos=vector(0,0,0), radius=15, color=color.blue, axis=vector(0,15,0), opacity=1),
    cylinder(pos=vector(0,13,0), radius=8, color=color.yellow, axis=vector(0,10,0), opacity=1)
], pos=vector(-800,1,200))

# Robot Basket 5
oFr_5 = compound([
    cylinder(pos=vector(0,0,0), radius=15, color=color.blue, axis=vector(0,15,0), opacity=1),
    cylinder(pos=vector(0,13,0), radius=8, color=color.yellow, axis=vector(0,10,0), opacity=1)
], pos=vector(-800,1,200))

#-----------------------------------------------------------------------------------------------------
# Definicion Robots Equipo Red - MODIFICADO: frame -> compound
#-----------------------------------------------------------------------------------------------------
# Robot Basket 6
oFr_6 = compound([
    cylinder(pos=vector(0,0,0), radius=15, color=color.red, axis=vector(0,15,0), opacity=1),
    cylinder(pos=vector(0,13,0), radius=8, color=color.green, axis=vector(0,10,0), opacity=1)
], pos=vector(800,1,-400))

# Robot Basket 7
oFr_7 = compound([
    cylinder(pos=vector(0,0,0), radius=15, color=color.red, axis=vector(0,15,0), opacity=1),
    cylinder(pos=vector(0,13,0), radius=8, color=color.green, axis=vector(0,10,0), opacity=1)
], pos=vector(400,1,0))

# Robot Basket 8
oFr_8 = compound([
    cylinder(pos=vector(0,0,0), radius=15, color=color.red, axis=vector(0,15,0), opacity=1),
    cylinder(pos=vector(0,13,0), radius=8, color=color.green, axis=vector(0,10,0), opacity=1)
], pos=vector(800,1,400))

# Robot Basket 9
oFr_9 = compound([
    cylinder(pos=vector(0,0,0), radius=15, color=color.red, axis=vector(0,15,0), opacity=1),
    cylinder(pos=vector(0,13,0), radius=8, color=color.green, axis=vector(0,10,0), opacity=1)
], pos=vector(800,1,-200))

# Robot Basket 10
oFr_10 = compound([
    cylinder(pos=vector(0,0,0), radius=15, color=color.red, axis=vector(0,15,0), opacity=1),
    cylinder(pos=vector(0,13,0), radius=8, color=color.green, axis=vector(0,10,0), opacity=1)
], pos=vector(800,1,200))



#-----------------------------------------------------------------------------------------------------
# Logica principal.-
#-----------------------------------------------------------------------------------------------------
aRobots = [eRobot() for r in range(nMAX_ROBOTS)]  
aPlayer = [oFr_1,oFr_2,oFr_3,oFr_4,oFr_5,oFr_6,oFr_7,oFr_8,oFr_9,oFr_10]
aPelota = [ePelo() for i in range(10)]
aBall   = [oFr_B1,oFr_B2,oFr_B3,oFr_B4,oFr_B5,oFr_B6,oFr_B7,oFr_B8,oFr_B9,oFr_BA]

MyTxt   = label(pos = vector(0,100,-600),text = 'By Alberto Caro - Basket Bot',color = color.blue, 
                height = 30,box = True)

for i in range(nMAX_ROBOTS): 
    Robot_Init(i)

#Pelotas_Init()
#Ball_Init()

while 1:
 Robot_Blue_Move()
 Robot_Red_Move()
# UpDate_Pelotas()
 rate(100)


#[ Formulas Utiles----------]

'''
Ball = sphere(pos=(-900, 2, 1),radius=10,color = color.blue,make_trail=False,trail_color = color.yellow, interval=2, retain=50)


g = 9.8 # Aceleracion de Fuerza Gravedad en la Tierra
v = 130 # Velocidad de Disparo de la bala
e = 80  # Angulo de elevacion del canon respecto de la base
h = -50  # Angulo de Direccion (Heading..) de la bala

Py = v*cos(math.radians(e)) # Proyeccion Bala Eje Y a la Base (Plano XZ)

Vx = Py*cos(math.radians(h)) # Velocidad Bala en Eje X
Vy = v*sin(math.radians(e))  # Velocidad Bala en Eje y
Vz = Py*sin(math.radians(h)) # Velocidad Bala en Eje Z

s = 0
dt = 0.1 # Diferencial del tiempo
#-------------------------------------------------------------------------------------------------
# Logica principal.-
#-------------------------------------------------------------------------------------------------
while 1:
 s += dt
 x = Vx*s
 y = Vy*s - 0.5*g*s**2 # Formula de Posicion Proyectil Eje Y
 z = Vz*s
 Ball.pos = vector(-900 + x,y,z) # Partimos del extremo Izquierdo
 if Ball.pos.y < 0: 
    s = 0 # Chequeamos impacto de bala en el piso
    h += 5
    Py = v*cos(math.radians(e)) # Proyeccion Bala Eje Y a la Base (Plano XZ)
    Vx = Py*cos(math.radians(h)) # Velocidad Bala en Eje X
    Vy = v*sin(math.radians(e))  # Velocidad Bala en Eje y
    Vz = Py*sin(math.radians(h)) # Velocidad Bala en Eje Z
    if h >= 50: h = -50
 print(h)      
 rate(100) # FPS : Frame por segundo...


# if nPos == 0: aPlayer[nPos].Cy2.rotate(angle=radians(aRobots[nPos].nAngu),axis=(0,1,0))
# if nPos == 1: aPlayer[nPos].Cy2.rotate(angle=radians(aRobots[nPos].nAngu),axis=(0,1,0)) 
# if nPos == 2: aPlayer[nPos].Cy2.rotate(angle=radians(aRobots[nPos].nAngu),axis=(0,1,0)) 
# Fr_1.Cy2 = cylinder(frame=oFr_1,pos=(00,10,00),radius=2,color=color.white,axis=(40,0,0),opacity=1)

#V_y = v * sin(math.radians(e))                   # Componente vertical
#V_x = v * cos(math.radians(e)) * cos(math.radians(h))  # Componente horizontal X
#V_z = v * cos(math.radians(e)) * sin(math.radians(h))  # Componente horizontal Z

#Vf = vector(Vx,Vy,Vz)        # Vector Velocidad Final

oFr_B1.Ball = sphere(pos=(-900,2,1),radius = 10,color = color.blue,make_trail = False,
               trail_color = color.yellow, interval = 2, retain = 50)



'''