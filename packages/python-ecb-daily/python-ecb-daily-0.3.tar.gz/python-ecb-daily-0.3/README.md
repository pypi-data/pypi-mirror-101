Python ECB Daily
========

This library gets currency rates from European Central Bank daily exchange rates from ECB Rss Feeds.

## Installation


#### From command line:

`pip install python-ecb-daily`

#### From source code:

`git clone git@github.com:fatihsucu/python-ecb-daily.git`

`cd python-ecb-daily`

`python setup.py install`

## Basic Usage

```
from ecb import get_rate

rate = get_rate('USD', 'JPY')
```

### License
MIT licensed. Check the [`LICENSE`](https://github.com/fatihsucu/python-ecb-daily/blob/master/LICENSE) file for full details.