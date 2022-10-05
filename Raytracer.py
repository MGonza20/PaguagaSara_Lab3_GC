from gl import Raytracer, V3
from texture import *
from figures import *
from lights import *


width = 2056
height = 2056

# Materiales
brick = Material(diffuse = (0.8, 0.3, 0.3), spec = 16)
stone = Material(diffuse = (0.4, 0.4, 0.4), spec = 8)
wallMat = Material(diffuse = (37/255, 150/255, 190/255), spec = 8)
white = Material(diffuse = (0.1, 0.1, 0.1), spec = 8)
marble = Material(spec=64, texture= Texture("marble-tex-example.bmp"), matType= REFLECTIVE)

glass = Material(diffuse = (0.9, 0.9, 0.9), spec = 64, ior = 1.5, matType= TRANSPARENT)
diamond = Material(diffuse = (0.9, 0.9, 0.9), spec = 64, ior = 2.417, matType= TRANSPARENT)
mirror = Material(diffuse = (0.9, 0.9, 0.9), spec = 64, matType = REFLECTIVE)
blueMat = Material(diffuse = (0, 0, 1), spec = 64, matType = OPAQUE)
marble5 = Material( diffuse = (171/255, 240/255, 1), texture = Texture("colored-tex-8.bmp"), spec = 32,  ior = 1.5, matType = TRANSPARENT) 



rtx = Raytracer(width, height)
rtx.envMap = Texture("parkingLot.bmp")

rtx.lights.append( AmbientLight(intensity = 0.1 ))
rtx.lights.append( DirectionalLight(direction = (-1,-1,-1), intensity = 0.8 ))

rtx.scene.append(Triangle(A = (-0.5-1.5,0+0.5,-4), B = (1-1.5,1.7+0.5,-4), C = (0-1.5, 1.5+0.5, -4), material = marble5))
rtx.scene.append(Triangle(A = (-1*(-0.5-1.5)+0.25,-1*(0+0.5-1),-4), B = (-1*(1-1.5)+0.25, -1*(1.7+0.5-1),-4), C = (-1*(0-1.5)+0.25, -1*(1.5+0.5-1), -4), material = wallMat))
rtx.scene.append(Triangle(A = (-1,0,-3.5), B = (1,0,-3.5), C = (0, 1.5, -3.5), material = marble))


rtx.glRender()

rtx.glFinish("output.bmp")