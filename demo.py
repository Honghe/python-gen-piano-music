# -*- coding: utf-8 -*-
import numpy as np

fs = 48000  # 采样频率

# 各个音对应的基频
aa = 440 * 2. ** ((np.arange(0, 36) - 22) / 12)  # 中音区（小字组-小字二组）
aa1 = 440 * 2. ** ((np.arange(0, 12) - 34) / 12)  # 低音区（大字组）
aa2 = 440 * 2. ** ((np.arange(0, 12) + 14) / 12)  # 高音区（小字三组）
mi = 41.204
so = 49.001
la = 55.001
xi = 61.737


# 包络函数
# y=t^a/e^(kt)
# 分别为旋律音和伴奏音都构建了一个包络函数，
# 原因是旋律音集中在中高音区，伴奏音集中在中低音区，频率越低能量衰减的时间会更长一点
def y1(ylen):
    yt = np.arange(ylen)
    shap_y1 = (yt / 48000) ** (1 / 5) / np.exp(yt / 48000 * 2)
    shap_y1 = shap_y1 / max(shap_y1)
    return shap_y1


def y2(ylen):
    yt = np.arange(ylen)
    shap_y2 = (yt / 48000) ** (1 / 15) / np.exp(yt / 48000 * 2)
    shap_y2 = shap_y2 / max(shap_y2)
    return shap_y2


import matplotlib.pyplot as plt

x_len = 48000
x = np.arange(x_len)
y = y2(x_len)
plt.figure(figsize=(10, 5))
plt.plot(x / x_len, y)
plt.show()

# tone1是旋律音
tone1 = [0, aa[16], aa[24], aa[23]]
# tone2是伴奏音
tone2 = [0, 0, aa1[10], aa[5]]

# 节拍
rym1 = [1, 1 / 2, 1 / 2, 1]
rym1 = np.array(rym1) * fs
rym1 = rym1.astype(int)

rym2 = [1, 1, 1 / 2, 1 / 2]
rym2 = np.array(rym2) * fs
rym2 = rym2.astype(int)


# 构造信号
def gen_signal(tone1, y1):
    x1 = []
    for n in range(len(tone1)):
        t = range(rym1[n])
        t = np.array(t) / fs
        N = len(t)
        # 琴弦振动的频率是和谐，即基频+谐频。公式为:f_{n}=\frac{n}{2 l} \sqrt{\frac{T}{\mu}}
        # 其中，i为弦长，T为弦的张力，μ为弦的线密度。当n=1时，f₁是弦振动最低的固有频率也就是弦的基频,
        # 其余的高次频率称为泛频，它们都为基频的整数倍，因而也称具有这样简单关系的固有频率为谐频。
        # 弦振动时激发的固有频率都是谐频，所以弦乐器一般听起来音色都是和谐的。
        # Ref: 21db的文章《钢琴竟然是这样发声的》
        a1 = (0.6882 * np.sin(2 * np.pi * tone1[n] * t) + np.sin(4 * np.pi * tone1[n] * t) + 0.9217 * np.sin(
            6 * np.pi * tone1[n] * t) + 0.2318 * np.sin(8 * np.pi * tone1[n] * t) + 0.0524 * np.sin(
            10 * np.pi * tone1[n] * t) + 0.1355 * np.sin(
            12 * np.pi * tone1[n] * t) + 0.1797 * np.sin(14 * np.pi * tone1[n] * t) + 0.09109 * np.sin(
            16 * np.pi * tone1[n] * t) + 0.0055 * np.sin(
            18 * np.pi * tone1[n] * t) + 0.1127 * np.sin(20 * np.pi * tone1[n] * t)) * y1(N)
        x1.extend(a1)
    return x1


x1 = gen_signal(tone1, y1)
x2 = gen_signal(tone2, y2)

# 旋律音和伴奏音结合
melody = np.array(x1) + np.array(x2)
melody = melody / max(melody)

# 保存wav
from scipy.io.wavfile import write

write("demo.wav", fs, melody)
