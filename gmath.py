import math
from display import *

# IMPORTANT NOTE

# Ambient light is represented by a color value

# Point light sources are 2D arrays of doubles.
#      - The fist index (LOCATION) represents the vector to the light.
#      - The second index (COLOR) represents the color.

# Reflection constants (ka, kd, ks) are represented as arrays of
# doubles (red, green, blue)

AMBIENT = 0
DIFFUSE = 1
SPECULAR = 2
LOCATION = 0
COLOR = 1
SPECULAR_EXP = 4


# lighting functions
def get_lighting(normal, view, ambient, light, areflect, dreflect, sreflect):
    normalize(normal)
    normalize(light[0])
    normalize(view)
    ambient = calculate_ambient(ambient, areflect)
    diffuse = calculate_diffuse(light, dreflect, normal)
    specular = calculate_specular(light, sreflect, view, normal)
    return limit_color([ambient[0] + diffuse[0] + specular[0],
                        ambient[1] + diffuse[1] + specular[1],
                        ambient[2] + diffuse[2] + specular[2]])


def calculate_ambient(alight, areflect):
    return [alight[i] * areflect[i] for i in range(3)]


def calculate_diffuse(light, dreflect, normal):
    dot = dot_product(light[0], normal)
    return [light[1][i] * dreflect[i] * dot for i in range(3)]


def calculate_specular(light, sreflect, view, normal):
    dot = dot_product(light[0], normal)
    v = [2 * dot * normal[i] - light[0][i] for i in range(3)]
    prod = dot_product(view, v)
    return [light[1][i] * sreflect[i] * (prod ** SPECULAR_EXP) for i in range(3)]


def limit_color(color):
    result = []
    for i in color:
        if i < 0:
            result.append(0)
        elif i > 255:
            result.append(255)
        else:
            result.append(i)
    return [int(i) for i in result]


# vector functions
# normalize vector, should modify the parameter
def normalize(vector):
    magnitude = math.sqrt(vector[0] * vector[0] +
                          vector[1] * vector[1] +
                          vector[2] * vector[2])
    for i in range(3):
        vector[i] = vector[i] / magnitude


# Return the dot product of a . b
def dot_product(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


# Calculate the surface normal for the triangle whose first
# point is located at index i in polygons
def calculate_normal(polygons, i):
    A = [0, 0, 0]
    B = [0, 0, 0]
    N = [0, 0, 0]

    A[0] = polygons[i + 1][0] - polygons[i][0]
    A[1] = polygons[i + 1][1] - polygons[i][1]
    A[2] = polygons[i + 1][2] - polygons[i][2]

    B[0] = polygons[i + 2][0] - polygons[i][0]
    B[1] = polygons[i + 2][1] - polygons[i][1]
    B[2] = polygons[i + 2][2] - polygons[i][2]

    N[0] = A[1] * B[2] - A[2] * B[1]
    N[1] = A[2] * B[0] - A[0] * B[2]
    N[2] = A[0] * B[1] - A[1] * B[0]

    return N
