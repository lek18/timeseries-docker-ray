import collections
from typing import List

import pandas as pd
import pmdarima as pm
from data import data_preparation


def train(path: str, timeframe: str = "monthly") -> None:
    data_generation = data_preparation.GenerateData(path=path)

    data = data_generation.generate_data()

    time_series_length = {"monthly": 12, "weekly": 52, "daily": 365}

    results = collections.defaultdict(str)

    for product in data:
        # train the model
        ts = data[product][timeframe][["sale_amount"]].tolist()

        if len(ts) < time_series_length[timeframe]:
            results[product] = {"Not available, few data points"}

        max_date = data[product]["date"].max()
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
            sum([abs(test_hat[x] - test[x]) for x in range(len(test))])
            / len(test)
            * 100
        )

        # get results and save them

        results[product] = {
            "test_mape": mape,
            "future_dates": future_dates,
            "predictions": arima.predict(n_periods=len(future_dates)),
            "hit_production": "yes" if mape >= 0.75 else "no",
        }

    return results


def get_future_dates(max_date: pd.Timestamp, time_frame: str) -> List[str]:
    start_date = max_date + pd.DateOffset(days=1)
    end_date = max_date + pd.DateOffset(months=6)

    dates = pd.date_range(start_date, end_date)
    years = dates.year
    time_frames = ("daily", "weekly", "monthly")

    if time_frame not in time_frames:
        raise Exception(f"Please provide a time frame from {time_frames}")

    if time_frame == "daily":
        return [date.strftime("%Y-%m-%d") for date in dates]

    if time_frame == "weekly":
        weeks = dates.isocalendar().weeks

        df = pd.DataFrame({"year": years, "week": weeks}).drop_duplicates()
        df["year-week"] = df["year"] + df["week"]

        return df["year-week"].tolist()

    if time_frame == "monthly":
        months = dates.isocalendar().months

        df = pd.DataFrame({"year": years, "month": months}).drop_duplicates()
        df["year-week"] = df["year"] + df["month"]

        return df["year-month"].tolist()


results = train(path="data/forecasting_toy_data.csv")
