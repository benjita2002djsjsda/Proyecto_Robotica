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

#-------------------------------------------------------------------------------------------------
# Definicion del Mundo 3D y sus Objetos.-
#-------------------------------------------------------------------------------------------------
scene.title = 'Demo'
scene.width = 900
scene.height = 600
scene.center = vector(0, 0, 0)
scene.background = color.black

MyMap = box(pos=(0,0,0),size=(1800,3,1000),color=color.gray(0.5))

#Ball  = sphere(pos=(-900,2,1),radius=10,color=color.blue)
#Ball  = sphere(pos=(-900,2,1),radius=1,color=color.blue,make_trail=True,interval=2,retain=3,trail_type='points')

Ball = sphere(pos=(-900, 2, 1),radius=10,color = color.blue,make_trail=True,trail_color = color.yellow, interval=2, retain=50)


g = 9.8 # Aceleracion de Fuerza Gravedad en la Tierra
v = 130 # Velocidad de Disparo de la bala
e = 60  # Angulo de elevacion del canon respecto de la base
h = -30  # Angulo de Direccion (Heading..) de la bala

Py = v*cos(math.radians(e)) # Proyeccion Bala Eje Y a la Base (Plano XZ)

Vx = Py*cos(math.radians(h)) # Velocidad Bala en Eje X
Vy = v*sin(math.radians(e))  # Velocidad Bala en Eje y
Vz = Py*sin(math.radians(h)) # Velocidad Bala en Eje Z

# Solucion Alternativa
#V_y = v * sin(math.radians(e))                   # Componente vertical
#V_x = v * cos(math.radians(e)) * cos(math.radians(h))  # Componente horizontal X
#V_z = v * cos(math.radians(e)) * sin(math.radians(h))  # Componente horizontal Z


#Vf = vector(Vx,Vy,Vz)        # Vector Velocidad Final

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
