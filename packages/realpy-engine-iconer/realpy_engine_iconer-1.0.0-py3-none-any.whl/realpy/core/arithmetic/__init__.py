""" Arithmetic
    ---
    ```
    from realpy.core import arithmetic
    ```
"""
import math
import random

__all__ = [
    "sqr", "sign", "degtorad", "radtodeg", "irandom", "irandom_range", "bezier4", "choose",
    "distribute", "probability_test", "lengthdir_x", "lengthdir_y", "line_interact",
    "point_distance", "point_direction"
]


def sqr(v: float) -> float:
    return v * v


def sign(x: float) -> int:
    ret = 0
    if x > 0:
        ret = 1
    elif x < 0:
        ret = - 1
    return ret


def degtorad(degree: float) -> float:
    return math.radians(degree)


def radtodeg(radian: float) -> float:
    return math.degrees(radian)


def bezier4(t: float, x1, x2, x3, x4) -> float:
    factor = 1 - t

    return factor * (factor * (factor * x1 + t * x2)
                     + t * (factor * x2 + t * x3)) + t * (factor * (factor * x2 + t * x3) + t * (factor * x3 + t * x4))


def lengthdir_x(length: float, direction: float) -> float:
    return math.cos(degtorad(direction)) * length


def lengthdir_y(length: float, direction: float):
    return -math.sin(degtorad(direction)) * length


def point_distance(x1: float, y1: float, x2: float, y2: float) -> float:
    return math.dist([x1, y1], [x2, y2])


def point_direction(x1: float, y1: float, x2: float, y2: float) -> float:
    return radtodeg(math.atan2(y2 - y1, x1 - x2))


def line_interact(Sx1: float, Sy1: float, Sx2: float, Sy2: float, Dx1: float, Dy1: float, Dx2: float, Dy2: float,
                  Seg: bool) -> float:
    Sx = Sx2 - Sx1
    Sy = Sy2 - Sy1
    Dx = Dx2 - Dx1
    Dy = Dy2 - Dy1
    wx = Sx1 - Dx1
    wy = Sy1 - Dy1

    ua = 0
    ud = Dy * Sx - Dx * Sy

    if ud != 0:
        ua = (Dx * wy - Dy * wx) / ud
        if Seg:
            if ua < 0 or ua > 1:
                return 0

            ub = (Sx * wy - Sy * wx) / ud
            if ub < 0 or ub > 1:
                return 0
    return ua


def irandom(n) -> int:
    return random.randint(0, int(n))


def irandom_range(n1, n2) -> int:
    return random.randint(int(n1), int(n2))


def distribute(x1: float, x2: float, ratio: float) -> float:
    if irandom(100) <= ratio * 100:
        return x1
    else:
        return x2


def probability_test(max_value) -> bool:
    return bool(irandom(max_value - 1) == 0)


def choose(*args):
    length = len(args)
    if length <= 0:
        raise RuntimeError("choose 함수에 값이 제대로 전달되지 않았습니다!" + __name__)

    pick = None
    try:
        pick = args[irandom(length - 1)]
    except ValueError:
        pass
    return pick
