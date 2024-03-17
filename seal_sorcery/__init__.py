import itertools
from typing import Optional, Union, Literal

import cv2
import numpy as np
from stl import mesh


def _三角化(l):
    r = []
    for i in range(1, len(l) - 1):
        r.append([l[0], l[i], l[i + 1]])
    return np.array(r)


def _tc(contour) -> np.array:
    r = []
    c = contour.tolist()
    for qq, ww in itertools.pairwise(c + [c[0]]):
        a = qq[0][0], qq[0][1], 1
        b = ww[0][0], ww[0][1], 1
        a0 = qq[0][0], qq[0][1], 0
        b0 = ww[0][0], ww[0][1], 0
        r.append(_三角化([a0, b0, b, a]))
    return np.concatenate(r)


def seal(img: Union[np.array, str], 长: int = 40, 宽: Optional[int] = None, 印章高度: int = 2, 尾部高度: int = 50, 尾部形状: Literal['凸包', '长方形'] = '凸包') -> mesh.Mesh:
    if not isinstance(img, np.ndarray):
        img = cv2.imread(img)
    img = img
    if 宽 is None:
        宽 = 长 * img.shape[1] / img.shape[0]
    img = 255 - img
    _, img_2 = cv2.threshold(img[:, :, 0], 128, 255, 0)
    contours, _ = cv2.findContours(img_2,  cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)
    x, y = img.shape[:2]
    if 尾部形状 == '凸包':
        包 = cv2.convexHull(np.concatenate(contours))
    elif 尾部形状 == '长方形':
        包 = np.array([[[0, 0]], [[0, x]], [[y, x]], [[y, 0]]])
    r = np.concatenate([_tc(c) * [长/x, 宽/y, 印章高度] for c in contours])
    盖 = _三角化(包.reshape(-1, 2))
    盖 = np.concatenate([盖, np.zeros((len(盖), 3, 1))], axis=2)
    r = np.concatenate([r, _tc(包) * [长/x, 宽/y, -尾部高度], 盖 * [长/x, 宽/y, 1], 盖 * [长/x, 宽/y, 1] - [0, 0, 尾部高度]])
    data = np.zeros(len(r), dtype=mesh.Mesh.dtype)
    for i, l in enumerate(r):
        data['vectors'][i] = np.array(l)
    m = mesh.Mesh(data)
    return m
