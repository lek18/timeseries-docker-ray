# timeseries_docker_ray
Arima Time Series Forecasting using python in a docker container.


## Project Structure
```bash
.
├── README.md
└── project
    ├── Dockerfile
    ├── app
    │   ├── __init__.py
    │   ├── data
    │   │   ├── __init__.py
    │   │   ├── data_preparation.py
    │   │   └── forecasting_toy_data.csv
    │   ├── main.py
    │   └── ml
    │       ├── __init__.py
    │       ├── train.py
    │       └── utils.py
    ├── poetry.lock
    ├── pyproject.toml
    └── tests
        ├── __init__.py
        └── test_data_preparation.py
```

## Build the Container
```bash
1. cd project
2. docker build . -t arima_model
```

## Run Container
timeframe values are ["weekly, "monthly", "daily"]
1. To get predictions run: `docker run -di -v $(pwd):/src/app/data arima_model python app/main.py --timeframe "weekly" --filepath "/src/app/data/predictions"`
2. Results are saved in `{pwd}/predictions_{timeframe}.csv`. Ensure to have docker write privilages to this location `pwd`
3. To run the available test run: `docker run arima_model python -s -m pytest .`
