# Peano

Decorator for performance measurement

- Measures function calls: TPS and Latency
- Reports to InfluxDB

## Example

```python
        peano.init(url, organization, token, bucket)

        @measured()
        def do_something()
```

## TODO

- tests
- async commit to influx

## dev

poetry shell
poetry update
pytest
poetry build