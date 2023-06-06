import datetime

import numpy as np
import pandas as pd
import pytest
from data import data_preparation


class TestGenerateData:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.mockGenerateData = data_preparation.GenerateData(path="fakepath")
        self.mock_time_series, self.time_range = self.generate_mock_time_series_data()

    def generate_mock_time_series_data(self) -> pd.DataFrame:
        # Example DataFrame

        # Set the random seed for reproducibility
        np.random.seed(42)

        # Generate dates for one year
        start_date = pd.Timestamp("2021-01-01")
        end_date = pd.Timestamp("2023-12-31")
        dates = pd.date_range(start_date, end_date, freq="D")

        # Generate random sales data for each date
        sales = np.random.randint(100, 1000, len(dates))

        # Create a DataFrame with dates and sales
        df = pd.DataFrame({"timestamp": dates, "sale_amount": sales})

        # Randomly remove 50% of the rows
        df = df.sample(frac=0.5, random_state=42)

        # Reset the index of the DataFrame
        df.reset_index(drop=True, inplace=True)

        # repeat the df above for say 5 products.
        time_series_df = pd.DataFrame()
        N = 5
        for i in range(N):
            product_title = str(i)
            df["product_title"] = product_title
            time_series_df = pd.concat([time_series_df, df], axis=0)

        return time_series_df, len(dates) * N

    def test_get_dates(self):
        generate_data = data_preparation.GenerateData(path="fake_path")

        df = pd.DataFrame(
            {
                "timestamp": [
                    "2019-10-17 17:00:00",
                    "2020-11-18 18:30:00",
                    "2021-12-19 19:45:00",
                ]
            }
        )
        output = generate_data.get_dates(df=df)

        expected = [
            {
                "timestamp": "2019-10-17 17:00:00",
                "timestamp_dupe": pd.Timestamp("2019-10-17 17:00:00"),
                "date": datetime.date(2019, 10, 17),
                "year": 2019,
                "month": 10,
                "quarter": 4,
                "week": 42,
            },
            {
                "timestamp": "2020-11-18 18:30:00",
                "timestamp_dupe": pd.Timestamp("2020-11-18 18:30:00"),
                "date": datetime.date(2020, 11, 18),
                "year": 2020,
                "month": 11,
                "quarter": 4,
                "week": 47,
            },
            {
                "timestamp": "2021-12-19 19:45:00",
                "timestamp_dupe": pd.Timestamp("2021-12-19 19:45:00"),
                "date": datetime.date(2021, 12, 19),
                "year": 2021,
                "month": 12,
                "quarter": 4,
                "week": 50,
            },
        ]
        assert output.to_dict("records") == expected

    def test_fill_dates(self):
        # Sample DataFrame
        df = pd.DataFrame(
            {
                "product_title": ["A", "A", "B", "B", "B", "C", "C", "C"],
                "sales": [10, 15, 20, 12, 18, 30, 25, 20],
                "date": [
                    "2022-01-01",
                    "2022-02-02",
                    "2022-01-01",
                    "2022-02-03",
                    "2022-01-04",
                    "2022-02-01",
                    "2022-04-02",
                    "2022-05-04",
                ],
            }
        )

        # Convert 'dates' column to datetime
        df["date"] = pd.to_datetime(df["date"])

        output = self.mockGenerateData.fill_dates(df=df)

        expected = [
            {
                "product_title": "A",
                "date": 33,
                "year": 33,
                "month": 33,
                "quarter": 33,
                "week": 33,
            },
            {
                "product_title": "B",
                "date": 34,
                "year": 34,
                "month": 34,
                "quarter": 34,
                "week": 34,
            },
            {
                "product_title": "C",
                "date": 93,
                "year": 93,
                "month": 93,
                "quarter": 93,
                "week": 93,
            },
        ]

        output = (
            output.groupby(["product_title"], as_index=False).count().to_dict("records")
        )
        print(output)
        assert output == expected

    def test_impute_data(self):
        # get mock time series data
        time_series_df = self.mock_time_series.copy()

        # add weeks, years, months, quarters
        time_series_df = self.mockGenerateData.get_dates(time_series_df)

        # get the partition averages
        time_series_df = self.mockGenerateData.get_partitions_averages(time_series_df)

        # get time series with all the filled dates
        filled_sales_df = self.mockGenerateData.fill_dates(time_series_df)

        output = self.mockGenerateData.impute_data(
            filled_sales_df=filled_sales_df, sales_df=time_series_df
        )

        assert output.shape[0] == self.time_range
