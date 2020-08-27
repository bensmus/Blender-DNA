import bpy
import math
import random

# adopted from https://blender.stackexchange.com/questions/6750/poly-bezier-curve-from-a-list-of-coordinates

''' sample data
coors = [(1,1,1), (2,2,2), (1,2,1)] '''


COUNT = 50
bpy.ops.curve.primitive_bezier_circle_add()
BEVEL = bpy.context.active_object

# rgba floats
COLORMAP = {'a': (1, 0, 0, 1), 'c': (52/255, 219/255, 235/255, 1),
            'g': (83/255, 235/255, 52/255, 1), 't': (110/255, 52/255, 235/255, 1)}


def other(base):
    '''gets the corresponding base'''

    if base == 'a':
        return 'g'
    if base == 'g':
        return 'a'
    if base == 'c':
        return 't'
    if base == 't':
        return 'c'


def scale(object, ratio):
    '''reduces object size in all dimensions'''

    object.scale[0] = ratio
    object.scale[1] = ratio
    object.scale[2] = ratio


scale(BEVEL, 0.2)


def getHelixCoors(offset):
    '''Gets coordinates for a helix'''

    coors = []

    for t in range(COUNT):
        x = math.cos(t)
        y = math.sin(t)
        z = t
        coors.append((x, y, z + offset))

    return coors


def createPipeFromCoors(name, coors):
    '''Creates pipe object'''

    curveData = bpy.data.curves.new(name, type='CURVE')
    curveData.dimensions = '3D'
    curveData.resolution_u = 2
    curveData.bevel_object = BEVEL

    # Map coors to spline
    polyline = curveData.splines.new('NURBS')
    polyline.points.add(COUNT)

    for i, coor in enumerate(coors):
        x, y, z = coor
        polyline.points[i].co = (x, y, z, 1)

    print(polyline.points[0].co)
    curveOB = bpy.data.objects.new(name, curveData)
    bpy.context.collection.objects.link(curveOB)


lower_helix_coors = getHelixCoors(0)
print(lower_helix_coors)
upper_helix_coors = getHelixCoors(2)
print(upper_helix_coors)

createPipeFromCoors('LowerHelix', lower_helix_coors)
createPipeFromCoors('UpperHelix', upper_helix_coors)


def createBase(location, base):
    '''make a cylinder with certain color'''

    bpy.ops.mesh.primitive_cylinder_add(location=location)
    cylinder = bpy.context.active_object
    cylinder.scale[0] = 0.2
    cylinder.scale[1] = 0.2
    cylinder.scale[2] = 0.5

    mat = bpy.data.materials.new(name='Material')
    cylinder.data.materials.append(mat)
    cylinder.active_material.diffuse_color = COLORMAP[base]


def createBases(lower_helix_coors, string):
    '''
    - Creates bases for DNA
    - Looks at points at same index in coordinate list and
    creates cylinder between
    '''

    for t in range(2, COUNT-1):
        bot = list(lower_helix_coors[t])
        bot[2] += 0.5
        top = list(bot)
        top[2] += 1

        createBase(bot, string[t])
        createBase(top, other(string[t]))


def randomDNASide():
    '''returns a string of random DNA Side with length COUNT'''

    bases = ['a', 'c', 'g', 't']
    string = ''

    for _ in range(COUNT):
        string += random.choice(bases)

    return string


string = randomDNASide()
createBases(lower_helix_coors, string)
