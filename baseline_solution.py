"""
Template for submissions to the market-making game

"""

import numpy as np
import pandas as pd
import statsmodels.api as sm

s

train_data = pd.read_csv("train.csv")
test_data = pd.read_csv("test.csv")

rets = train_data["P"].pct_change().dropna()
ret_std = rets.std()
mean_abs_ret = rets.abs().mean()

X = sm.add_constant(rets.iloc[:-1].values)
y = rets.iloc[1:].values

model = sm.OLS(y, X).fit(cov_type="HAC", cov_kwds={"maxlags": 5})
print(model.summary())

CONST = model.params[0]
ALPHA = model.params[1]
MEAN_ABS_RET = mean_abs_ret
RET_STD = ret_std

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