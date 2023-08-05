# YouLess Python Data Bridge
[![PyPI version](https://badge.fury.io/py/youless-api.svg)](https://badge.fury.io/py/youless-api)

This package contains support classes to fetch data from the YouLess sensors.

## Contributing

To request new features or report bugs please use:

    https://jongsoftdev.atlassian.net/jira/software/c/projects/YA/issues/

## Using the python integration

To use the API use the following code:

```python

from youless_api.youless_api import YoulessAPI

if __name__ == '__main__':
    api = YoulessAPI("192.168.1.2")  # use the ip address of the youless device
    api.update()

    gasUsage = api.gas_meter.value

```