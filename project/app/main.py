import sys
import time

import pandas as pd
from ml.train import train


def main():
    # Specify the file path
    file_path = sys.argv[1]
    print("-------------Fitting Arima Model ---------")
    results = train(path="data/forecasting_toy_data.csv")

    # Convert dictionary to JSON string

    output = pd.DataFrame()
    for key, val in results.items():
        df = pd.DataFrame(val)
        df["product_title"] = key
        output = pd.concat([output, df], axis=0)

    print("------------Saving Data-----------------")
    output.to_csv(file_path, index=False)
    print("------------Complete-----------------")


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
