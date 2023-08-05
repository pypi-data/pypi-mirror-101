import numpy as np
import random


class PoissonGenerator(object):
    """
    生成一个 shape 尺寸的泊松采样 mask, \n
    shape: 暂时只支持 2d shape 的 mask, \n
    min_distance: 任意两点间最小距离， \n
    max_distance: 任意两点间的最大距离， \n
    search_timses: 尝试在选定点周围找一个符合要求的点的尝试次数，超过尝试次数还未找到则认为当前点周围已经没有合适点, \n
    example: \n
    pg = PoissonGenerator(shape)
    mask = pg.mask2d()
    """
    def __init__(self, shape=None, min_distance=5, max_distance=0, search_times=0):
        if shape is None or len(shape) != 2:
            raise AttributeError("当前版本仅支持 2d mask，请检查 shape")
        self.shape = shape
        self.min_shape = min(shape)
        self.min_distance = min_distance
        self.max_distance = max_distance
        self.search_times = search_times
        if self.max_distance == 0 or self.max_distance <= self.min_distance:
            self.max_distance = min(self.min_distance * 2, self.min_distance + 20)
        if self.search_times == 0:
            self.search_times = int((self.min_distance + (self.max_distance - self.min_distance)/2) * np.pi)
        self.sample_rate = 0

    def mask2d(self):
        process_points = []
        rs_points = []
        mask = np.zeros(self.shape)
        x = int(random.random() * self.shape[0])
        y = int(random.random() * self.shape[1])
        process_points.append((x, y))
        rs_points.append((x, y))
        mask[x, y] = 1
        while len(process_points) > 0:
            x, y = random.choice(process_points)
            idx = process_points.index((x, y))
            for i in range(self.search_times):
                theta = random.random() * 2 * np.pi
                r = random.random() * (self.max_distance - self.min_distance) + self.min_distance
                x_next = int(x + np.cos(theta) * r)
                y_next = int(y + np.sin(theta) * r)
                if x_next < 0 or x_next >= self.shape[0] or y_next < 0 or y_next >= self.shape[1]:
                    continue
                dis = np.sqrt(np.sum((np.array((x_next, y_next)) - np.array(rs_points))**2, axis=1))
                if np.any(dis < self.min_distance):
                    if i == (self.search_times - 1):
                        process_points.pop(idx)
                    continue
                else:
                    process_points.append((x_next, y_next))
                    rs_points.append((x_next, y_next))
                    mask[x_next, y_next] = 1
                    break
        s = list(mask.flatten()).count(1)
        self.sample_rate = s / self.shape[0] * self.shape[1]
        return mask
