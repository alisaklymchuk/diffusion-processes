
import numpy as np

CONST = 0.0009
ALPHA = -0.4
GAMMA = 0.0
S0 = 0.1
LAM = 0.0

MEAN_ABS_RET = 0.0
RET_STD = 1.0


def make_market(p, d, v, x):
    price = p[-1]
    ret = price / p[-2] - 1

    p_fair = price * (1 + CONST + ALPHA * ret)
    p_skewed = p_fair - GAMMA * x

    z_score = (abs(ret) - MEAN_ABS_RET) / RET_STD
    spread = S0 * (1 + LAM * max(z_score, 0))

    buy = max(p_skewed - spread / 2, 1e-5)
    sell = max(p_skewed + spread / 2, buy + 1e-5)

    return np.array([buy, sell])
