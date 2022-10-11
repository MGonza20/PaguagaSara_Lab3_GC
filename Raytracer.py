from gl import Raytracer, V3
from texture import *
from figures import *
from lights import *


width = 4096
height = 4096

# Materiales
skyBlueMat = Material(diffuse = (37/255, 150/255, 190/255), spec = 8)
marble = Material(spec=64, texture= Texture("marble-tex-example.bmp"), matType= REFLECTIVE)
transparentNTexMat = Material( diffuse = (171/255, 240/255, 1), texture = Texture("colored-tex-8.bmp"), spec = 32,  ior = 1.5, matType = TRANSPARENT) 


rtx = Raytracer(width, height)
rtx.envMap = Texture("parkingLot.bmp")

# Luces
rtx.lights.append( AmbientLight(intensity = 0.1 ))
rtx.lights.append( DirectionalLight(direction = (-1,-1,-1), intensity = 0.8 ))

rtx.scene.append(Triangle(A = (-0.5-1.5,0+0.5-0.5,-4), B = (1-1.5,1.7+0.5-0.5,-4), C = (0-1.5, 1.5+0.5-0.5, -4), material = transparentNTexMat))
rtx.scene.append(Triangle(A = (-1*(-0.5-1.5)-0.5 +0.35 ,-1*(0+0.5-1)-0.5-0.25,-4), B = (-1*(1-1.5)-0.5 + 0.35, -1*(1.7+0.5-1)-0.5-0.25,-4), C = (-1*(0-1.5)+0.25 + 0.35, -1*(1.5+0.5-1)-0.5-0.25, -4), material = skyBlueMat))
rtx.scene.append(Triangle(A = (-1 -0.1,0-0.5,-3.5), B = (1 -0.1,0-0.5,-3.5), C = (0 -0.1, 1.5-0.5, -3.5), material = marble))


rtx.glRender()

rtx.glFinish("output.bmp")