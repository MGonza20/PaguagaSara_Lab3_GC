from gl import Raytracer, V3
from texture import *
from figures import *
from lights import *


width = 256
height = 256

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


rtx = Raytracer(width, height)
rtx.envMap = Texture("parkingLot.bmp")

rtx.lights.append( AmbientLight(intensity = 0.1 ))
rtx.lights.append( DirectionalLight(direction = (-1,-1,-1), intensity = 0.8 ))

rtx.scene.append(Triangle(A = (-1,0,-8), B = (1,0,-8), C = (0, 1.5, -8), material = wallMat))
rtx.scene.append(Triangle(A = (-1-2,0,-8), B = (1-2,0,-8), C = (0-2, 1.5, -8), material = wallMat))
rtx.scene.append(Triangle(A = (-1+2,0,-8), B = (1+2,0,-8), C = (0+2, 1.5, -8), material = wallMat))

rtx.glRender()

rtx.glFinish("output.bmp")