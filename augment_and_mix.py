# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Reference implementation of AugMix's data augmentation method in numpy."""
import augmentations
import numpy as np
import random
from PIL import Image
from torchvision import transforms

# CIFAR-10 constants
MEAN = [0.4914, 0.4822, 0.4465]
STD = [0.2023, 0.1994, 0.2010]


def normalize(image):
    """Normalize input image channel-wise to zero mean and unit variance."""
    '''
    image = image.transpose(2, 0, 1)  # Switch to channel-first
    mean, std = np.array(MEAN), np.array(STD)
    image = (image - mean[:, None, None]) / std[:, None, None]
    return image.transpose(1, 2, 0)
    '''
    return image


def apply_op(image, op, severity):
    image = np.clip(image * 255., 0, 255).astype(np.uint8)
    pil_img = Image.fromarray(image)  # Convert to PIL.Image
    pil_img = op(pil_img, severity)
    return np.asarray(pil_img) / 255.


# cxq 将图像随机缩小0.4~0.8倍
def scale(image):
    image = np.clip(image * 255., 0, 255).astype(np.uint8)
    pil_img = Image.fromarray(image)  # Convert to PIL.Image
    pil_img = transforms.RandomAffine(degrees=0, scale=(0.4, 0.8))(pil_img)
    return np.asarray(pil_img) / 255.


def augment_and_mix(image, severity=3, width=3, depth=-1, alpha=1.):
    """Perform AugMix augmentations and compute mixture.

    Args:
      image: Raw input image as float32 np.ndarray of shape (h, w, c)
      severity: Severity of underlying augmentation operators (between 1 to 10).
      width: Width of augmentation chain
      depth: Depth of augmentation chain. -1 enables stochastic depth uniformly
             from [1, 3]
      alpha: Probability coefficient for Beta and Dirichlet distributions.

    Returns:
      mixed: Augmented and mixed image.
    """
    width += 1  # cxq

    ws = np.float32(
        np.random.dirichlet(
            [alpha] * width))  # ws like [0.01519703 0.3264288  0.6583742 ] 其值即为论文中的w_i 与论文中不同，这里只有3个，文中是4个
    m = np.float32(np.random.beta(alpha, alpha))  # m is a scaler from 0~1 即为论文中的w

    mix = np.zeros_like(image)  # 即论文中的 R_mix


    for i in range(width-1):  # i = 0, 1, 2
        image_aug = image.copy()
        depth = depth if depth > 0 else np.random.randint(2, 4)  # [2, 4) 也就是说当depth设置为-1时， 会随机从 2, 3 中选择
        for _ in range(depth):
            op = np.random.choice(augmentations.augmentations)
            # print(op)
            image_aug = apply_op(image_aug, op, severity)  # 在image_aug上实施操作op, 实施的程度(level) 是 severity
        # Preprocessing commutes since all coefficients are convex
        mix += ws[i] * normalize(image_aug)

    # cxq--------------------------------------------------------------------
    image_aug = mix.copy()
    mix += ws[width-1] * normalize(scale(image_aug))
    # cxq--------------------------------------------------------------------

    max_ws = max(ws)
    rate = 1.0 / max_ws
    # print(rate)

    # mixed = (random.randint(5000, 9000)/10000) * normalize(image) + (random.randint((int)(rate*3000), (int)(rate*10000))/10000) * mix
    mixed = max((1 - m), 0.7) * normalize(image) + max(m, rate * 0.5) * mix
    # 实际用的式子， 好像控制了R_mix的成分 不太清楚rate是拿来干嘛的
    # rate是因为level不同而控制的？op里也有个rate

    # mixed = (1 - m) * normalize(image) + m * mix  # 这是论文算法中用的式子
    return mixed

