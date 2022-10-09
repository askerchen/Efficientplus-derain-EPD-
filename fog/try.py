import random

import torch
import torch.nn as nn
import cv2, math
import torch.nn.functional as F
import numpy as np
class SE_block(nn.Module):
    def __init__(self,channel:int):
        super().__init__()
        self.se = nn.Sequential(
            nn.AdaptiveAvgPool2d((1,1)), #global pooling
            nn.Conv2d(channel,channel//16,kernel_size=1), #ker=1其实就相当于全连接
            nn.ReLU(),
            nn.Conv2d(channel//16,channel,kernel_size=1),
            nn.Sigmoid()
        )
    def forward(self,x):
        x2 = self.se(x)
        print("-------")
        print(x2.shape)
        print("-------")
        x = x*x2 #scale
        return x


class KPN(nn.Module):
    def __init__(self):
        super(KPN, self).__init__()
        self.conv1 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, stride=1, padding=1)
        self.se1 = SE_block(64)

    # 前向传播函数
    def forward(self,x):
        x = self.conv1(x)
        x = self.se1(x)
        return x
def demo():
    img_path = 'test.png'
    img = cv2.imread(img_path)
    # img = torch.rand(8,8,3)
    img_f = img / 255.0
    cv2.imshow("before process", img_f)

    (row, col, chs) = img.shape
    A = 0.8  # 亮度
    beta = random.random()/32
    #beta = 0.03  # 雾的浓度
    size = math.sqrt(max(row, col))  # 雾化尺寸
    center = (row // 2, col // 2)  # 雾化中心
    for j in range(row):
        for l in range(col):
            d = -0.04 * math.sqrt((j - center[0]) ** 2 + (l - center[1]) ** 2) + size
            td = math.exp(-beta * d)
            img_f[j][l][:] = img_f[j][l][:] * td + A * (1 - td)

    print(img_f.shape)
    print(img.shape)
    cv2.imshow("src", img)
    cv2.imshow("dst", img_f * 255)
    cv2.waitKey()
# net = KPN()
# x = torch.rand(3,32,16,16)  #[B,C,H,W]
# x = net(x)
# print(x.shape)
if __name__ == '__main__':
    demo()