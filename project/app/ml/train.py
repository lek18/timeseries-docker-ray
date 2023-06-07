import collections

import pmdarima as pm
from app.data import data_preparation
from app.ml.utils import get_future_dates

# import json


def train(path: str, timeframe: str = "monthly") -> dict:
    data_generation = data_preparation.GenerateData(path=path)

    data = data_generation.generate_data()

    time_series_length = {"monthly": 12, "weekly": 52, "daily": 365}

    results = collections.defaultdict(str)

    for product in data:
        # train the model
        ts = data[product][timeframe]["sale_amount"].tolist()

        if len(ts) < time_series_length[timeframe]:
            results[product] = {"Not available, few data points"}

        max_date = data[product]["daily"]["date"].max()

        future_dates = get_future_dates(max_date, timeframe)

        cutoff = round(len(ts) * 0.70)
        cutoff_ = cutoff + 1
        train = ts[0:cutoff]
        test = ts[cutoff_:]  #
        # use pdarmia auto arima

        # Fit a simple auto_arima model on train to get an error rate,
        # and then train on the full data set to get the actual predictions
        test_arima = pm.auto_arima(
            train,
            error_action="ignore",
            trace=True,
            suppress_warnings=True,
            maxiter=10,
            seasonal=False,
        )

        arima = pm.auto_arima(
            ts,
            error_action="ignore",
            trace=True,
            suppress_warnings=True,
            maxiter=10,
            seasonal=False,
        )

        # get MAPE
        test_hat = test_arima.predict(n_periods=len(test))

        mape = (
            sum([abs(test_hat[x] - test[x]) / test[x] for x in range(len(test))])
            / len(test)
            * 100
        )

        # get results and save them

        results[product] = {
            "test_mape": mape,
            "future_dates": future_dates,
            "predictions": arima.predict(n_periods=len(future_dates)),
            "hit_production": "yes" if mape >= 75 else "no",
        }

    return results


if __name__ == "__main__":
    results = train(path="data/forecasting_toy_data.csv")
