from tkinter import *
import math


class Point:
    def __init__(self, x0, y0, z0):
        self.x = x0
        self.y = y0
        self.z = z0

    def __str__(self):
        return f"({self.x},{self.y}, {self.z})"

    def __repr__(self):
        return f"Point({self.x},{self.y}, {self.z})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __ne__(self, other):
        return self.x != other.x or self.y != other.y or self.x != other.x

    def polar(self):
        if self.x > 0 and self.y >= 0:
            return math.atan(self.y / self.x)
        elif self.x > 0 and self.y < 0:
            return math.atan(self.y / self.x) + 2 * math.pi
        elif self.x < 0 and self.y >= 0:
            return math.atan(self.y / self.x) + math.pi
        elif self.x < 0 and self.y < 0:
            return math.atan(self.y / self.x) + math.pi
        elif self.x == 0:
            if self.y > 0:
                return math.pi / 2
            else:
                return math.pi * 1.5

    def rotateZ(self, other, angle):
        newx = self.x - other.x
        newy = self.y - other.y
        rotx = newx * math.cos(angle) - newy * math.sin(angle)
        roty = newy * math.cos(angle) + newx * math.sin(angle)
        rotx += other.x
        roty += other.y
        self.x = rotx
        self.y = roty

    def rotateY(self, other, angle):
        newx = self.x - other.x
        newz = self.z - other.z
        rotx = newx * math.cos(angle) + newz * math.sin(angle)
        rotz = newz * math.cos(angle) - newx * math.sin(angle)
        rotx += other.x
        rotz += other.z
        self.x = rotx
        self.z = rotz

    def rotateX(self, other, angle):
        newy = self.y - other.y
        newz = self.z - other.z
        roty = newy * math.cos(angle) - newz * math.sin(angle)
        rotz = newz * math.cos(angle) + newy * math.sin(angle)
        roty += other.y
        rotz += other.z
        self.y = roty
        self.z = rotz

    def rotate(self, other, angle):
        Point.rotateX(self, other, angle)
        Point.rotateY(self, other, angle)
        Point.rotateZ(self, other, angle)


class Vector:
    def __init__(self, p1, p2):
        self.x = (p2.x - p1.x)
        self.y = (p2.y - p1.y)
        self.z = (p2.z - p1.z)

    def __add__(self, p1):
        self.x += p1.x
        self.y += p1.y
        self.z += p1.z

    def __sub__(self, p1):
        self.x -= p1.x
        self.y -= p1.y
        self.z -= p1.z

    def __neg__(self, p1):
        self.x *= -1
        self.y *= -1
        self.z *= -1

    def __mul__(self, n):
        self.x *= n
        self.y *= n
        self.z *= n

    def leng(self):
        return (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5

    def scalar(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def vectorm(self, other):
        newx = self.y * other.z - self.z * other.y
        newy = self.z * other.x - self.x * other.z
        newz = self.x * other.y - self.y * other.x
        return Vector(Point(0, 0, 0), Point(newx, newy, newz))


class Face:
    def __init__(self, points):
        num = len(points)
        for i in range(num):
            self[i] = points[i]

    def normal(self):
        a = Vector(self[0], self[2])
        b = Vector(self[1], self[2])
        return Vector.vectorm(b, a)

    def rotate(self, based, angle):
        centerx = 0
        centery = 0
        for i in range(len(self)):
            Point.rotate(self[i], based, angle)
            centerx += self[i].x
            centery += self[i].y
        centerx = centerx / len(self)
        centery = centery / len(self)
        #self.sort(key=lambda a: Point.polar(Point(a.x - centerx, a.y - centery, 0)))

    def angle(self):
        return (Vector.scalar(Vector(Point(0, 0, 0), Point(0, 0, 1)), Face.normal(self)) / (
            Vector.leng(Face.normal(self))))

    def color(self):
        part = abs(Face.angle(self))
        pix = 1 / 255
        # print(part)
        num = int(part // pix)
        # print(Face.normal(self).x, Face.normal(self).y, Face.normal(self).z)
        print(num)
        col = hex(num)[2:]
        print(col*3)
        return col * 3

    def is_visible(self):
        f1 = self
        n = Face.normal(f1)
        print(n.z)
        return n.z >= 0


class Polyhedron:
    def __init__(self, faces):
        num = len(faces)
        for i in range(num):
            self[i] = faces[i]

    def rotate(self, based, angle):
        for elem in self:
            Face.rotate(elem, based, angle)



root = Tk()
w = Canvas(root, width=800, height=800) 
w.configure(background='#023389') 
w.pack()  


p1 = Point(200, 300, 200)
p2 = Point(100, 200, 200)
p3 = Point(200, 100, 200)
p4 = Point(300, 200, 200)
p5 = Point(200, 200, 100)
p6 = Point(200, 200, 300)

f1 = [p1, p2, p6]
f2 = [p2, p3, p6]
f3 = [p3, p4, p6]
f4 = [p4, p1, p6]
f5 = [p2, p1, p5]
f6 = [p3, p2, p5]
f7 = [p4, p3, p5]
f8 = [p1, p4, p5]
hg = [f1, f2, f3, f4, f5, f6, f7, f8]




based = Point(375, 300, 100)
angle = 0.001


def move():
    global viewPoint, rotate_direction
    w.delete(ALL)
    for rect in hg:
        if Face.is_visible(rect):
            w.create_polygon(rect[0].x, rect[0].y, rect[1].x, rect[1].y, rect[2].x, rect[2].y,
                     fill='#' + str(Face.color(rect)))
    Polyhedron.rotate(hg, based, angle)
    root.after(10, move)
move()
root.mainloop()
