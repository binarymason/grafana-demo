# Prometheus + Grafana Demo

![screenshot](.assets/screenshot.png)

# How to get it working locally

1) Ensure you have docker-compose installed on your machine, then run:

  ```
  docker-compose up
  ```

2) Go to [localhost:3000](http://localhost:3000)

3) Add prometheus as a datasource using docker DNS name: `prometheus:9090`

4) Import dashboard located [here](.assets/grafana_dashboard.json)

5) Watch the metrics
