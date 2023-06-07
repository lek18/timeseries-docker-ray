import collections

import pandas as pd

# read the data


class GenerateData:
    def __init__(self, path: str) -> None:
        self.path = path
        self.ts_columns = ["timestamp", "product_title", "sale_amount"]

    def generate_data(self) -> dict:
        # read the raw data
        time_series_data = self.read_data()

        # extract the date components (week, month, year, date)
        time_series_data = self.get_dates(time_series_data)

        # get the full time series data between min and max date of each product
        time_series_data_filled = self.fill_dates(time_series_data)

        # get the partition averages for our time series
        time_series_data = self.get_partitions_averages(time_series_data)

        # do the imputation if required
        time_series_data = self.impute_data(
            filled_sales_df=time_series_data_filled, sales_df=time_series_data
        )

        # get aggregates for each product

        output = self.get_aggregates(time_series_data)

        return output

    def read_data(self):
        return pd.read_csv(self.path, sep=",")

    def get_dates(self, df: pd.DataFrame) -> pd.DataFrame:
        # Convert 'timestamp' column to datetime type

        timestamp_dupe = "timestamp_dupe"
        df[timestamp_dupe] = pd.to_datetime(df["timestamp"])

        # Extract the date component into a new column
        df["date"] = df[timestamp_dupe].dt.date
        df["year"] = df[timestamp_dupe].dt.year
        df["month"] = df[timestamp_dupe].dt.month
        df["quarter"] = df[timestamp_dupe].dt.quarter
        df["week"] = df[timestamp_dupe].dt.isocalendar().week

        return df

    def fill_dates(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        time series data need to be filled, and this should be done
        between the min and max date available per product.
        """
        # get the min and max date for each product

        products = df.groupby(["product_title"])["date"].agg(["min", "max"])
        products.columns = ["min_date", "max_date"]

        products = products.reset_index()

        # Create an empty DataFrame to store the filled dates
        filled_dates_df = pd.DataFrame()

        # Iterate over each row in the 'result' DataFrame
        for _, row in products.iterrows():
            product = row["product_title"]
            min_date = row["min_date"]
            max_date = row["max_date"]

            # Create a date range between the minimum and maximum dates
            date_range = pd.date_range(min_date, max_date, freq="D")

            # Create a temporary DataFrame with the product and filled dates
            temp_df = pd.DataFrame(
                {"product_title": [product] * len(date_range), "date": date_range}
            )

            # add the week, month, quarter, year
            temp_df["year"] = temp_df["date"].dt.year
            temp_df["month"] = temp_df["date"].dt.month
            temp_df["quarter"] = temp_df["date"].dt.quarter
            temp_df["week"] = temp_df["date"].dt.isocalendar().week
            temp_df["date"] = temp_df["date"].dt.date
            # Append the temporary DataFrame to the filled_dates_df
            filled_dates_df = pd.concat([filled_dates_df, temp_df], axis=0)

        return filled_dates_df.sort_values(["product_title", "date"], ascending=True)

    def get_partitions_averages(self, df: pd.DataFrame) -> pd.DataFrame:
        # compute the weekly,monthly, and yearly daily averages
        p = "sale_amount"
        df["weekly"] = df.groupby(["year", "week"])[p].transform("mean")
        df["monthly"] = df.groupby(["year", "month"])[p].transform("mean")
        df["quarterly"] = df.groupby(["year", "quarter"])[p].transform("mean")
        df["yearly"] = df.groupby(["year"])["sale_amount"].transform("mean")

        return df

    def impute_data(
        self, filled_sales_df: pd.DataFrame, sales_df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Impute the full time series data if required by the first nonnull value
        from [weekly, monthly, quarterly, yearly]
        """

        # create a df for each group of time
        weeks = sales_df[["product_title", "year", "week", "weekly"]].drop_duplicates()
        months = sales_df[
            ["product_title", "year", "month", "monthly"]
        ].drop_duplicates()
        quarters = sales_df[
            ["product_title", "year", "quarter", "quarterly"]
        ].drop_duplicates()
        years = sales_df[["product_title", "year", "yearly"]].drop_duplicates()

        # add the sales to filled_sales_df from sales_df

        filled_sales_df = filled_sales_df.merge(
            sales_df[["product_title", "date", "sale_amount"]],
            on=["product_title", "date"],
            how="left",
        )

        # now i must add the missing date to filled_sales_df
        filled_sales_df = filled_sales_df.merge(weeks, how="left")
        filled_sales_df = filled_sales_df.merge(months, how="left")
        filled_sales_df = filled_sales_df.merge(quarters, how="left")
        filled_sales_df = filled_sales_df.merge(years, how="left")

        #  Impute missing values with the first non-null mean value in order
        filled_sales_df["sale_amount"] = filled_sales_df["sale_amount"].fillna(
            filled_sales_df["weekly"].fillna(
                filled_sales_df["monthly"].fillna(
                    filled_sales_df["quarterly"].fillna(filled_sales_df["yearly"])
                )
            )
        )

        return filled_sales_df

    def get_aggregates(self, df: pd.DataFrame) -> collections.defaultdict:
        result = collections.defaultdict(lambda: collections.defaultdict(str))

        products = df["product_title"].unique().tolist()

        daily_ts = df[["product_title", "date", "sale_amount"]].copy()
        weekly_ts = (
            df[["product_title", "sale_amount", "week", "year"]]
            .groupby(["product_title", "week", "year"], as_index=False)
            .sum()
        )
        monthly_ts = (
            df[["product_title", "sale_amount", "month", "year"]]
            .groupby(["product_title", "month", "year"], as_index=False)
            .sum()
        )

        for product in products:
            result[product]["daily"] = daily_ts[daily_ts["product_title"] == product]
            result[product]["weekly"] = weekly_ts[weekly_ts["product_title"] == product]
            result[product]["monthly"] = monthly_ts[
                monthly_ts["product_title"] == product
            ]

        return result
