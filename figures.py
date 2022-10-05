from code import interact
from mathLib import *
from math import *

WHITE = (1,1,1)
BLACK = (0,0,0)

OPAQUE = 0
REFLECTIVE = 1
TRANSPARENT = 2


class Intersect(object):
    def __init__(self, distance, point, normal, texcoords, sceneObj):
        self.distance = distance
        self.point = point
        self.normal = normal
        self.texcoords = texcoords
        self.sceneObj = sceneObj

class Material(object):
    def __init__(self, diffuse = WHITE, spec = 1.0, ior = 1.0, texture = None, matType = OPAQUE):
        self.diffuse = diffuse
        self.spec = spec
        self.ior = ior
        self.texture = texture
        self.matType = matType


class Sphere(object):
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

    def ray_intersect(self, orig, dir):
        L = subtractVList(self.center, orig)
        tca = dotProduct(L, dir)
        d = (norm(L) ** 2 - tca ** 2) ** 0.5

        if d > self.radius:
            return None

        thc = (self.radius ** 2 - d ** 2) ** 0.5

        t0 = tca - thc
        t1 = tca + thc

        if t0 < 0:
            t0 = t1
        if t0 < 0:
            return None
        
        # P = O + t0 * D
        P = addVectors(orig, [t0*dir[0], t0*dir[1], t0*dir[2]])
        normal = subtractVList(P, self.center)
        normal = normV(normal)

        u = 1 - ((atan2(normal[2], normal[0])) / (2 * pi) + 0.5)
        v = acos(-1*normal[1]) / pi

        uvs = (u, v)

        return Intersect(distance = t0,
                         point = P,
                         normal = normal,
                         texcoords = uvs,
                         sceneObj = self)


class Plane(object):
    def __init__(self, position, normal, material):
        self.position = position
        self.normal = normV(normal)
        self.material = material

    def ray_intersect(self, orig, dir):
        # Distancia = (( planePos - origRayo) o normal) / (direccionRayo o normal)
        denom = dotProduct(dir, self.normal)

        if abs(denom) > 0.0001:
            num = dotProduct(subtractVList(self.position, orig), self.normal) 
            t = num / denom

            if t > 0:
                # P = O + t*D
                P = addVectors(orig, [t * dir[0], t * dir[1], t * dir[2]])
                return Intersect(distance = t,
                                 point = P,
                                 normal = self.normal,
                                 texcoords = None, # Para aplicar las uvs en todo el plano habria que repetir lq textura 
                                                   # una y otra vez en el plano
                                 sceneObj = self)

        return None

class Disk(object):
    def __init__(self, position, radius, normal, material):
        self.plane = Plane(position, normal, material)
        self.material = material
        self.radius = radius

    def ray_intersect(self, orig, dir):
        intersect = self.plane.ray_intersect(orig, dir)

        if intersect is None:
            return None
        
        contact = subtractVList(intersect.point, self.plane.position)
        contact = norm(contact)

        if contact > self.radius:
            return None

        return Intersect(distance = intersect.distance,
                         point = intersect.point,
                         normal = self.plane.normal,
                         texcoords = None,
                         sceneObj = self)


def baryCoords(A, B, C, P):

    areaPBC = (B[1] - C[1]) * (P[0] - C[0]) + (C[0] - B[0]) * (P[1] - C[1])
    areaPAC = (C[1] - A[1]) * (P[0] - C[0]) + (A[0] - C[0]) * (P[1] - C[1])
    areaABC = (B[1] - C[1]) * (A[0] - C[0]) + (C[0] - B[0]) * (A[1] - C[1])

    try:
        u = areaPBC / areaABC
        v = areaPAC / areaABC
        w = 1 - u - v
    except:
        return -1, -1, -1
    else:
        return u, v, w


class Triangle(object):
    def __init__(self, A, B, C, material):
        
        position = [(A[0]+B[0]+C[0])/3, (A[1]+B[1]+C[1])/3, (A[2]+B[2]+C[2])/3]

        edge1 = subtractVList(B, A)
        edge2 = subtractVList(C, A)

        triangleNormal = crossProduct(edge1, edge2)
        triangleNormal = normV(triangleNormal)

        self.normal = triangleNormal
        self.plane = Plane(position, triangleNormal, material)
        self.material = material
        self.A = A
        self.B = B
        self.C = C

    def ray_intersect(self, orig, dir):

        A = self.A  
        B = self.B  
        C = self.C  

        intersect = self.plane.ray_intersect(orig, dir)
        if intersect is not None:
            u, v, w = baryCoords(A, B, C, intersect.point)
            if 0<=u and 0<=v and 0<=w:
                return Intersect(distance = intersect.distance,
                                point = intersect.point,
                                normal = self.normal,
                                texcoords = None,
                                sceneObj = self)
        else:
            return None





class AABB(object):
    # Axis Aliigned Bounding Boxs
    def __init__(self, position, size, material):
        self.position = position
        self.size = size
        self.material = material

        self.planes = []
        halfSizes = [0, 0, 0]

        halfSizes[0] = size[0] / 2
        halfSizes[1] = size[1] / 2
        halfSizes[2] = size[2] / 2

        # Sides
        self.planes.append(Plane(addVectors(position, (halfSizes[0], 0, 0)), (1, 0, 0), material))
        self.planes.append(Plane(addVectors(position, (-halfSizes[0], 0, 0)), (-1, 0, 0), material))

        # Up and Down
        self.planes.append(Plane(addVectors(position, (0, halfSizes[1], 0)), (0, 1, 0), material))
        self.planes.append(Plane(addVectors(position, (0, -halfSizes[1], 0)), (0, -1, 0), material))

        # Front and back
        self.planes.append(Plane(addVectors(position, (0, 0, halfSizes[2])), (0, 0, 1), material))
        self.planes.append(Plane(addVectors(position, (0, 0, -halfSizes[2])), (0, 0, -1), material))

        self.boundsMin = [0, 0, 0]
        self.boundsMax = [0, 0, 0]

        epsilon = 0.001

        for i in range(3):
            self.boundsMin[i] = self.position[i] - (epsilon + halfSizes[i])
            self.boundsMax[i] = self.position[i] + (epsilon + halfSizes[i])

    
    def ray_intersect(self, orig, dir):
        intersect = None
        t = float('inf')

        for plane in self.planes:
            planeInter = plane.ray_intersect(orig, dir)

            if planeInter is not None:
                planePoint = planeInter.point

                if self.boundsMin[0] <= planePoint[0] <= self.boundsMax[0]:
                    if self.boundsMin[1] <= planePoint[1] <= self.boundsMax[1]:
                        if self.boundsMin[2] <= planePoint[2] <= self.boundsMax[2]:

                            if planeInter.distance < t:
                                t = planeInter.distance
                                intersect = planeInter

                                # Tex coords
                                u, v = 0, 0

                                # Las uvs de las caras de los lados
                                if abs(plane.normal[0]) > 0:
                                    # Mapear uvs para el eje x, usando las coordenadas de Y y Z
                                    u = (planeInter.point[1] - self.boundsMin[1]) / self.size[1]
                                    v = (planeInter.point[2] - self.boundsMin[2]) / self.size[2]

                                elif abs(plane.normal[1]) > 0:
                                    # Mapear uvs para el eje y, usando las coordenadas de X y Z
                                    u = (planeInter.point[0] - self.boundsMin[0]) / self.size[0]
                                    v = (planeInter.point[2] - self.boundsMin[2]) / self.size[2]

                                elif abs(plane.normal[2]) > 0:
                                    # Mapear uvs para el eje z, usando las coordenadas de X y Y
                                    u = (planeInter.point[0] - self.boundsMin[0]) / self.size[0]
                                    v = (planeInter.point[1] - self.boundsMin[1]) / self.size[1]


        if intersect is None:
            return None

        return Intersect(distance = t,
                         point = intersect.point,
                         normal = intersect.normal,
                         texcoords = (u, v), 
                         sceneObj = self)
