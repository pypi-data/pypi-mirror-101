import numpy as np


class RadialGenerator(object):
    """
    描述: 生成辐射状的 2d mask, 暂时仅支持均匀的 2d mask \n
    shape: 暂时只支持 2d shape 的 mask, \n
    line_num: 采样线的数目，原点对称的线算一条直线, \n
    example:
    shape = (512, 512)
    rg = RadialGenerator(shape=shape, line_num=62)
    mask = rg.uniform_rm2d()
    print(rg.sample_rate)
    """
    def __init__(self, shape=None, line_num=1):
        self.shape = shape
        if self.shape is None or len(self.shape) != 2:
            raise AttributeError("目前仅支持 2d mask 生成, 请检查 shape")
        if self.shape[0] <= 2 or self.shape[1] <= 2:
            raise ValueError("shape太小")
        if line_num <= 0:
            raise ValueError("采样线数目必须为正数")
        self.min_shape = min(shape)
        self.line_num = line_num
        self.sample_rate = 0

    def uniform_rm2d(self):
        r_max = int(np.sqrt((self.shape[0]/2)**2 + (self.shape[1]/2)**2))
        r = np.linspace(-r_max, r_max, 2*r_max)
        theta = np.linspace(0, np.pi, self.line_num+1)
        mask = np.zeros(self.shape)
        for t in theta:
            x = (r * np.cos(t)).astype(np.int_) + self.shape[0] // 2
            y = (r * np.sin(t)).astype(np.int_) + self.shape[1] // 2
            x_idx = np.where(x >= 0, x < self.shape[0], x >= 0)
            y_idx = np.where(y >= 0, y < self.shape[1], y >= 0)
            x_idx, y_idx = self.__get_short_idx(x, y, x_idx, y_idx)
            mask[x[x_idx], y[y_idx]] = 1
        s = list(mask.flatten()).count(1)
        self.sample_rate = s / (self.shape[0] * self.shape[1])
        return mask

    def __get_short_idx(self, x, y, x_idx, y_idx):
        if len(x[x_idx]) < len(y[y_idx]):
            return x_idx, x_idx
        elif len(x[x_idx]) > len(y[y_idx]):
            return y_idx, y_idx
        return x_idx, y_idx
