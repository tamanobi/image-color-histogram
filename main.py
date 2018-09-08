#coding:utf-8

import os

import numpy as np
from skimage import io
from skimage.exposure import histogram

from pathlib import Path

from PIL import Image as PImage

IMAGE_PATH=os.getenv('IMAGE_PATH')

def decreaseColor(d: np.ndarray) -> np.ndarray:
    d[(d >= 0) & (d < 64)] = 32
    d[(d >= 64) & (d < 128)] = 96
    d[(d >= 128) & (d < 192)] = 160
    d[(d >= 192) & (d < 256)] = 224
    return d

def split(d: np.ndarray) -> tuple:
    return (image[:,:,0], image[:,:,1], image[:,:,2])

def merge(r, g, b) -> np.ndarray:
    result = np.empty(shape=(r.shape[0], r.shape[1], 3), dtype=np.uint8)
    result[:,:,0] = r
    result[:,:,1] = g
    result[:,:,2] = b
    return result

def pattern1(input_image: Path, output: Path) -> None:
    """not using pillow"""

    image = io.imread(str(input_image))
    r, g, b = split(image)

    r = decreaseColor(r)
    b = decreaseColor(b)
    g = decreaseColor(g)

    io.imsave(str(output), merge(r, g, b))

def pattern2(input_image: Path, output: Path) -> None:
    """using pillow"""
    image_pillow = PImage.open(str(input_image))
    #(r, g, b) = image_pillow.split()
    #r, b, g = r.quantize(4).convert('L'),g.quantize(4).convert('L'),b.quantize(4).convert('L')
    #res = PImage.merge('RGB', [r,g,b])
    res = image_pillow.quantize(64).convert('RGB')
    res.save(str(output))

if __name__ == '__main__':
    p = Path(IMAGE_PATH)
    if not p.exists():
        exit()

    #pattern1(p, Path('./output.jpg'))
    pattern2(p, Path('./output2.jpg'))
