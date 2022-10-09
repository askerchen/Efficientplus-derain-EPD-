这里都是用rain100H训练出来的模型

version:
v3: 原efficientderain基本结构+膨胀卷积+L1与SSIMloss;
v4: v3+原rainmix;
v3s: v3+se;
v4s: v4+se;
v3p: v3+新改进rainmix;
v3sp: v3+新改进rainmix+se

_1000表示epoch = 1000;
_done表示已经测试过;