## Simple Torn Wrapper

A simple basis wrapper for the torn API. Handles sending and decoding the request.

To use
```python
from Wrapper import TornWrapper
wrapper = TornWrapper(api_key='API_KEY')
data = wrapper.request(section, id, selections)
```
where section is either: `torn`, `user`, `faction`, `properties`, `company`, `market`. ID should be a string/int and selections should be a python list of strings.
e.g `['stocks','levels']`.  These can be chosen from the API as referenced on: https://www.torn.com/api.html#. The data will be in dictionary form.

https://discord.gg/myTajWNU6q
