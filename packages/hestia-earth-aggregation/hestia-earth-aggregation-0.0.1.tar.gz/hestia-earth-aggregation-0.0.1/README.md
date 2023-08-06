# Hestia Aggregation Engine

[![Pipeline Status](https://gitlab.com/hestia-earth/hestia-aggregation-engine/badges/master/pipeline.svg)](https://gitlab.com/hestia-earth/hestia-aggregation-engine/commits/master)
[![Coverage Report](https://gitlab.com/hestia-earth/hestia-aggregation-engine/badges/master/coverage.svg)](https://gitlab.com/hestia-earth/hestia-aggregation-engine/commits/master)

## Install

1. Install the module:
```bash
pip install hestia_earth.aggregation
```

### Usage

```python
import os
from hestia_earth.aggregation import aggregate

os.environ['API_URL'] = 'https://api.hestia.earth'
aggregates = aggregate(country_name='Japan')
```
