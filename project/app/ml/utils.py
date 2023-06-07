from typing import List

import pandas as pd


def get_future_dates(max_date: pd.Timestamp, time_frame: str) -> List[str]:
    start_date = max_date + pd.DateOffset(days=1)
    end_date = start_date + pd.DateOffset(months=6)
    dates = pd.date_range(start_date, end_date)
    years = dates.year
    time_frames = ("daily", "weekly", "monthly")

    if time_frame not in time_frames:
        raise Exception(f"Please provide a time frame from {time_frames}")

    if time_frame == "daily":
        return [date.strftime("%Y-%m-%d") for date in dates]

    if time_frame == "weekly":
        weeks = dates.isocalendar().week
        df = pd.DataFrame({"year": years, "week": weeks}).drop_duplicates()
        df["year-week"] = df["year"].astype(str) + df["week"].astype(str)
        df = df.sort_values(["year", "week"], ascending=True)
        return df["year-week"].tolist()

    if time_frame == "monthly":
        months = dates.month
        print("hello", months)
        df = pd.DataFrame({"year": years, "month": months}).drop_duplicates()
        df = df.sort_values(["year", "month"], ascending=True)
        df["year-month"] = df["year"].astype(str) + df["month"].astype(str)
        return df["year-month"].tolist()
