# GeoUK Python Library

The GeoUK Python library provides a pythonic interface to the GeoUK API. It includes an API client class, and a set of resource classes.


## Installation

```
pip install geouk
```

## Requirements

- Python 3.7+


# Usage

```Python

import geouk


client = geouk.Client('your_api_key...')

# Get a list of place names and postcodes starting with the query string's
# first 2 characters (ideal for use with a typeahead).
suggestions = geouk.resources.Place.typeahead(client, 'wo...')

# Fetch a list of `Place`s that match the given query string
places = geouk.resources.Place.search(client, 'worcester')

print(places[0].humanized_name, places[0].geo_coords)

>> Worcester [52.18935, -2.22001]

# Fetch all the (data) sources
sources = geouk.resources.Source.all(client)

# Fetch a single (data) source
source = geouk.resources.Source.one(client, 'geonames')

```
