import argparse
import time

import pandas as pd
from ml.train import train


def main():
    # specifying arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeframe", help="First argument", default="weekly")
    args = parser.parse_args()

    # Specify the file path
    timeframe = args.timeframe
    print("-------------Fitting Arima Model ---------")

    results = train(path="app/data/forecasting_toy_data.csv", timeframe=timeframe)

    # Convert dictionary to JSON string

    output = pd.DataFrame()
    for key, val in results.items():
        df = pd.DataFrame(val)
        df["product_title"] = key
        output = pd.concat([output, df], axis=0)

    print("------------Saving Data-----------------")
    output.to_csv(f"app/predictions/predictions_{timeframe}.csv", index=False)
    print("------------Complete-----------------")


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
