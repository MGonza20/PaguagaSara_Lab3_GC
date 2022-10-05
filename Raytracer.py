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
# rtx.lights.append( PointLight( point = (0, 0, 0) ))
# rtx.lights.append( PointLight( point = (0, 20, 0) ))

# rtx.scene.append(Plane(position=(0,-3,-10), normal=(0,1,0), material= brick))
# rtx.scene.append(Disk(position=(0,-3,-10), radius = 3, normal=(0,1,0), material= brick))
# rtx.scene.append( AABB(position= (2, 2, -10), size = (2,2,2), material = marble))

rtx.scene.append(Triangle(position = (0, 0, 0), v0 = (3, 0, 0), v1 = (0, 3, 0), v2=(0, 0, 3), normal = (0, 1, 0), material = wallMat))
# rtx.scene.append(Plane(position = (0, 20, 0), normal = (0, -1, 0), material = wallMat))
# rtx.scene.append(Plane(position = (-10, 0, 0), normal = (1, 0, 0), material = stone))
# rtx.scene.append(Plane(position = (10, 0, 0), normal = (-1, 0, 0), material = stone))
# rtx.scene.append(Plane(position = (0, 0, -50), normal = (0, 0, 1), material = stone))
# rtx.scene.append(Plane(position = (-60, 0, 0), normal = (1, 0, 0), material = white))

# rtx.scene.append( AABB(position= (-2, -2, -10), size = (2,2,2), material = brick))
# rtx.scene.append( AABB(position= (2, -2, -10), size = (2,2,2), material = stone))

# rtx.scene.append( AABB(position= (2, 2, -10), size = (2,2,2), material = blueMat))
# rtx.scene.append( AABB(position= (2, 2, -10), size = (2,2,2), material = glass))


rtx.glRender()

rtx.glFinish("output.bmp")