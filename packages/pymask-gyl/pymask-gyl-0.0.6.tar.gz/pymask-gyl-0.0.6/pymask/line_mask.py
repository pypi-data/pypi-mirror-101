import numpy as np


class LineGenerator(object):
    """
    描述: 生成一个 2d 的线性采样 mask, 暂仅支持 均匀采样 和 高斯采样 \n
    shape: 暂时只支持 2d shape 的 mask, \n
    acc: 越大表示采样率越低 \n
    example: \n
    shape = (256, 256) \n
    lg = LineGenerator(shape, acc=4) \n
    mask = lg.uniform_2d() \n
    print(lg.sample_rate) \n
    mask = lg.norm_2d() \n
    print(lg.sample_rate)
    """
    def __init__(self, shape=None, acc=5):
        self.shape = shape
        if self.shape is None or len(self.shape) != 2:
            raise AttributeError("暂仅支持 2d mask, 请检查 shape")
        self.acc = acc
        if self.acc <= 0:
            raise AttributeError("acc 必须为正数")
        self.sample_rate = 0

    def uniform_2d(self):
        line_num = int(self.shape[0] / (self.acc + 1) + 0.5)
        x = np.linspace(0, self.shape[0], line_num+1).astype(np.int_)
        x_new = x + self.shape[0]//2 - x[len(x)//2]
        return self.__get_mask(x_new)

    def norm_2d(self, u=0, theta=None):
        """
        :param u: 表示多采样的位置，以 0 表示 mask 中心位置
        :param theta: 采样的集中程度， 数值越大表示越分散
        :return: 返回一个 mask
        """
        u += self.shape[0] // 2
        if u < 0 or u >= self.shape[0]:
            raise Warning("高采位置已超出 mask 尺寸范围")
        if theta is None:
            theta = self.shape[0] / 5
        if theta < 0:
            raise ValueError("theta 必须为正数")
        line_num = int(self.shape[0] / (self.acc + 1) + 0.5)
        x = np.random.normal(u, theta, line_num).astype(np.int_)
        return self.__get_mask(x)

    def __get_mask(self, x):
        x_new = x[np.where(x >= 0, x < self.shape[0], x >= 0)]
        mask = np.zeros(self.shape)
        mask[x_new, :] = 1
        self.sample_rate = len(x_new) / self.shape[0]
        return mask
