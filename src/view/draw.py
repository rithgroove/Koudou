import numpy as np
class Transform():
    def __init__(self):
        self.mat = np.identity(3)

    def reset(self):
        self.mat = np.identity(3)

    def _rotate(self, theta):
        pass

    def rotate(self, px, py, theta):
        #translate
        #rotate
        #translate back
        pass


    def translate(self, dx, dy):
        self.mat[0][2] += dx
        self.mat[1][2] += dy

    def scale(self, sx, sy):
        self.mat[0][0] *= sx
        self.mat[1][1] *= sy

        self.mat[0][2] *= sx
        self.mat[1][2] *= sy

    def apply(self, x, y):
        return np.matmul(self.mat, [x, y, 1])[:2]

class ViewPort():
    def __init__(self, h, w, pmin, pmax, x=0, y=0, s=100000):
        # todo proper python  get/set
        self.x = x
        self.y = y

        self.h = h
        self.w = w

        self.pmin = pmin
        self.pmax = pmax

        self.s = s

        self.__transform = Transform()
        self.__compute()
        print(self.__transform.mat)

    def __compute(self):
        self.__transform.reset()
        self.__transform.translate(-self.pmin[0], -self.pmin[1])

        # self.__transform.scale(self.s, self.s)
        # fit map
        cw = self.w/(self.pmax[1]-self.pmin[1])
        ch = self.h/(self.pmax[0]-self.pmin[0])
        self.__transform.scale(cw, ch)


        self.__transform.translate(self.x, self.y)

    def change_scale(self, s):
        self.s = s
        self.__compute()

    def update_scale(self, s):
        self.s += s
        self.__compute()

    def change_center(self, x, y):
        self.x = x
        self.y = y
        self.__compute()

    def update_center(self, dx, dy):
        vx, vy = self.x, self.y

        tx, ty = vx-dx, vy-dy
        # tx = min(0, tx) #if(self.view_port[0] > 0):  self.view_port = (0, self.view_port[1])
        # ty = min(0, ty) #if(self.view_port[1] > 0): self.view_port = (self.view_port[0], 0)

        # tx = max(tx, -1*self.s*self.pmax[0] + self.w)
        # ty = max(ty, -1*self.s*self.pmax[1] + self.h)

        self.x = tx
        self.y = ty
        self.__compute()

    def apply(self, x, y):
        return self.__transform.apply(x, y)

class Camera():
    def __init__(self):
        self.transform = Transform()
