# pyfabrik

`pyfabrik` is a simple library created to interface with Fabrik, the data access layer component of `OpenAristos`.

## Installation

Use 

```bash
pip install pyfabrik
```

## Usage

```python
import os

from pyfabrik.client import FabrikClient
from pyfabrik.data import DefaultDataFrameFacade
from pyfabrik.models import FabrikReadRequest, FabrikReadResponse

client = FabrikClient(
    endpoint=os.getenv("FABRIK_HOST"),
    token=os.getenv("FABRIK_JWT_TOKEN"),
    df_facade=DefaultDataFrameFacade(),
)

query: str = "index:ix[msci_benchmark_code='701431']>index_has_constituent>.effective.instrument_region:ir[]@axioma:a axioma.axww4_attribution_security.by_instrument_region[a,ir,price,effective_dt] e 2015-01-01 2015-02-01 b"

r: FabrikReadRequest = FabrikReadRequest(
    definition=query,
    warehouse="redshift",
)

res: FabrikReadResponse = client.read(r)
res.df.show()
```

## License
[AGPLV3](https://choosealicense.com/licenses/agpl-3.0/)
