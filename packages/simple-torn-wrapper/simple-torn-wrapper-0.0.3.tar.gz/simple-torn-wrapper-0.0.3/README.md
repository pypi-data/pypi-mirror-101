## Simple Torn Wrapper

A simple basis wrapper for the torn API. Handles sending and converting the response into a Python dictionary.

An example of the usage:
```python
from simple_torn_wrapper import TornWrapper
wrapper = TornWrapper(api_key='API_KEY')  # Find your API key in Torn
selections = ['selection1','selection2']  # Examples of selections are listed in the Torn API.
section = 'user'  # Other sections can be found in Torn API
data = wrapper.request(section, id, selections)
```

These can be chosen from the API as referenced on: https://www.torn.com/api.html#.
Section is one of the 6 main categories and selections should be a list of strings. 

Any issues or help required:

Discord @ https://discord.gg/myTajWNU6q

or by issue @ https://github.com/SolitudalDeveloper/SimpleTorn/issues

or by email @ innominatusofficial@gmail.com
