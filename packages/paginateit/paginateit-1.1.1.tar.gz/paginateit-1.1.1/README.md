
# paginateit

[![Python application](https://github.com/manjesh23/paginateit/actions/workflows/python-app.yml/badge.svg)](https://github.com/manjesh23/paginateit/actions/workflows/python-app.yml)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://gitHub.com/manjesh23/paginateit/graphs/commit-activity)
![PyPI - Downloads](https://img.shields.io/pypi/dm/paginateit)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/paginateit.svg)](https://pypi.python.org/pypi/paginateit/)

Used to paginate REST API Calls / Mostly on MultiThreaded API Calls via Python

## Description

Takes 2 inputs:
* count -> total number of items in all pages
* max_workers -> number of threads need to be created (Based upon the number provided, skip and limits are calculated dynamically)

## Getting Started

### Dependencies
Python 3.6 and further releases.

### Installing

```
pip install paginateit
```

### Executing program
```
from paginateit import paginateit as pg
pg.page(23052, 4)

----------------|---------------|---------------|------------|
|SKIP           | LIMIT         | FLIMIT        | COUNT      |
|---------------|---------------|---------------|------------|
|skip1: 0       |limit1: 5763	|flimit1: 763	|count1: 5763|
|---------------|---------------|---------------|------------|
|skip2: 5763	|limit2: 11526	|flimit2: 1526	|count2: 5763|
|---------------|---------------|---------------|------------|
|skip3: 11526	|limit3: 17289	|flimit3: 7289	|count3: 5763|
|---------------|---------------|---------------|------------|
|skip4: 17289	|limit4: 23052	|flimit4: 3052	|count4: 5763|
|---------------|---------------|---------------|------------|
|skip5: 23052	|limit5: 28815	|flimit5: 8815	|count5: 5763|
|---------------|---------------|---------------|------------|
```
```

We can now use the variables like skip(x) or limit(x) in the API where filter.

SKIP: A skip filter omits the specified number of returned records
LIMIT: A limit filter limits the number of records returned to the specified number
FLIMIT (Custome field): A flimit filter can be used to fetch all the remaining records at the last page of every thread
COUNT: A count filter tell the maximum number of records available in that page.

Other examples:

pg.page(1700, 8) --> Max records availabe in all pages is 1700 and are creating 8 threads / loops (We see skip[1-9] values)
pg.page(90005, 6) --> Max records availabe in all pages is 90005 and are creating 6 threads / loops (We see skip[1-7] values)
pg.page(5025) --> Max records availabe in all pages is 1700 and are creating 8 threads /loops (We see skip[1-3] values)

pg.page(count, max_workers) # max_workers defaults to 2 unless specified

```
## Usage

Access the dynamic calculated variables as shown below:

pg.skip1, pg.skip3, pg.limit2, pg.flimit4, pg.count2

## Help

Any advise for common problems or issues, please feel free to create a issue in Github

## Authors

Manjesh N
[manjesh_n@hotmail.com](mailto:manjesh_n@hotmail.com)


## License

This project is licensed under the Apache License 2.0 License - see the LICENSE file for details

## Acknowledgments