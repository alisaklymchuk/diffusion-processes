
import backtest
import solution
import pandas as pd
import statsmodels.api as sm
import numpy as np

train_data = pd.read_csv("train.csv")
test_data = pd.read_csv("test.csv")

rets = train_data["P"].pct_change().dropna()
ret_std = rets.std()
mean_abs_ret = rets.abs().mean()

X = sm.add_constant(rets.iloc[:-1].values)
y = rets.iloc[1:].values

model = sm.OLS(y, X).fit(cov_type="HAC", cov_kwds={"maxlags": 5})
print(model.summary())

solution.CONST = model.params[0]
solution.MEAN_ABS_RET = mean_abs_ret
solution.RET_STD = ret_std

price_scale = train_data["P"].mean() * ret_std
alphas = np.array([-0.5, -0.3, -0.1])
gammas = price_scale * np.array([0, 0.02, 0.05, 0.1])
spreads = price_scale * np.array([0.5, 1, 2])
lambdas = np.array([0, 0.5, 1])

results = []

for alpha in alphas:
    for gamma in gammas:
        for s0 in spreads:
            for lam in lambdas:
                solution.ALPHA = alpha
                solution.GAMMA = gamma
                solution.S0 = s0
                solution.LAM = lam

                result = backtest._run(solution.make_market, train_data)

                results.append([
                    alpha, gamma, s0, lam,
                    result["total pnl"].sum(),
                    result["position"].abs().max()
                ])

grid = pd.DataFrame(
    results,
    columns=["alpha", "gamma", "s0", "lam", "pnl", "max_inventory"]
)

grid = grid.sort_values("pnl", ascending=False)
print(grid.head(15))
