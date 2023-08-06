# Applipy New Relic

    pip install applipy_newrelic

Send logs and metrics to New Relic.

## Usage

Minimal applipy application definition using the New Relic module.

```yaml
# dev.yaml

app:
    name: demo
    modules:
        - applipy_newrelic.NewRelicModule

newrelic:
  license: XXX  # required
  logs:
    enabled: true
    host: null
    port: 443
  metrics:
    enabled: true
    host: null
    port: 443
    report_interval: 60  # in seconds
    common_tags: {}
```

Values in the example above are the default ones.
