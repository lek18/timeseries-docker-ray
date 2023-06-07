# timeseries_docker_ray
Time Series Forecasting using python in a docker container.

# Build the Container
1. `cd project`
2. `docker build . -t arima_model`

# Run Container
timeframe values are ["weekly, "monthly", "daily"]
1. `docker run -v $(pwd):/src/app/data arima_model --timeframe "weekly" --filepath "/src/app/data/predictions"`
2. Results are saved in `{pwd}/predictions_{timeframe}.csv`. Ensure to have docker write privilages to this location `pwd`
