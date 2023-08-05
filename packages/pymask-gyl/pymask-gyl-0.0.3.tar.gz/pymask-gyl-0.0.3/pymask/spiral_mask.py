import numpy as np


class SpiralGenerator(object):
    """
    描述: 可以生成 shape 大小的 mask \n
    shape: 一个长度为 2 的 tuple 或 list 表示需要生成的 mask 长 和 宽 \n
    ring: 需要生成的螺纹圈数， 可由 alpha 或 beta 计算出, +表示逆时针，-表示顺时针 \n
    alpha: 表示螺纹中心起点距离0点的距离，螺纹默认会从0点向外圈生成 \n
    beta: 表示螺纹每圈远离中心的增幅, +表示逆时针，-表示顺时针 \n
    edsm: 生成等距螺旋 mask \n
    easm: 生成等角螺旋 mask \n
    example: \n
    sg = SpiralGenerator(shape=(256, 256), ring=10) \n
    equidistance_mask = sg.edsm() \n
    equiangle_mask = sg.easm() \n
    """

    def __init__(self, shape=None, ring=None, alpha=0., beta=1.):
        self.shape = shape

        if self.shape is None or len(self.shape) != 2:
            raise AttributeError("仅能生成二维的mask")
        self.min_shape = min(self.shape)
        self.ring = ring
        self.alpha = alpha
        self.beta = beta
        self.sample_rate = 0

    def edsm(self):
        if self.ring is None:
            self.ring = (self.min_shape / 2 - self.alpha) / (self.beta * 2 * np.pi)
        else:
            self.beta = (self.min_shape / 2 - self.alpha) / (self.ring * 2 * np.pi)
        return self.__equidistance_spiral()

    def easm(self):
        if self.alpha == 0:
            self.alpha = 0.1
        if self.ring is None:
            self.ring = np.log(self.min_shape / 2 / self.alpha) / (self.beta * 2 * np.pi)
        else:
            self.beta = np.log(self.min_shape / 2 / self.alpha) / (self.ring * 2 * np.pi)
        return self.__equiangle_spiral()

    def __equidistance_spiral(self):
        def get_spiral(alpha, beta):
            def x(theta):
                return (alpha + beta * theta) * np.cos(theta)

            def y(theta):
                return (alpha + beta * theta) * np.sin(theta)

            return x, y

        x, y = get_spiral(self.alpha, self.beta)
        return self.__generate_mask(x, y)

    def __equiangle_spiral(self):
        def get_spiral(alpha, beta):
            def x(theta):
                return alpha * np.exp(beta * theta) * np.cos(theta)

            def y(theta):
                return alpha * np.exp(beta * theta) * np.sin(theta)

            return x, y

        x, y = get_spiral(self.alpha, self.beta)
        return self.__generate_mask(x, y)

    def __generate_mask(self, x, y):
        theta = np.linspace(0, self.ring * 2 * np.pi, self.shape[0] * self.shape[1])
        x_value = x(theta).astype(np.int_) + self.shape[0] // 2
        y_value = y(theta).astype(np.int_) + self.shape[1] // 2
        x_idx = x_value <= self.shape[0]-1
        y_idx = y_value <= self.shape[1]-1
        x_new = x_value[x_idx]
        y_new = y_value[y_idx]
        if len(x_new) < len(y_new):
            y_new = y_value[x_idx]
        elif len(x_new) > len(y_new):
            x_new = x_value[y_idx]
        mask = np.zeros(self.shape)
        mask[x_new, y_new] = 1
        s = list(mask.flatten()).count(1)
        self.sample_rate = s / (self.shape[0] * self.shape[1])
        return mask
