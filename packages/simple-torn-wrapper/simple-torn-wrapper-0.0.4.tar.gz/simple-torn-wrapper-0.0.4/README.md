# Simple Torn Wrapper
A simple basis wrapper for the torn API. Handles sending and converting the response into a Python dictionary.

## Example
An example of the usage:
```python
from simple_torn_wrapper import TornWrapper
wrapper = TornWrapper(api_key='API_KEY')  # Find your API key in Torn
selections = ['selection1','selection2']  # Examples of selections are listed in the Torn API.
section = 'user'  # Other sections can be found in Torn API
data = wrapper.request(section, id, selections)
```

Request also accepts parameters `tsfrom` and `tsto` for a timestamp search range.

These can be chosen from the API as referenced on: https://www.torn.com/api.html#.
Section is one of the 6 main categories and selections should be a list of strings. 

## Issues and Contact
- Discord @ https://discord.gg/myTajWNU6q
- issue @ https://github.com/SolitudalDeveloper/SimpleTorn/issues
- email @ innominatusofficial@gmail.com

## Development
To develop onto this repository, feel free to fork/clone.
Pipfile has all requirements.
Testing is done using Pytest. 

_Will add guide on development setup later._ 


