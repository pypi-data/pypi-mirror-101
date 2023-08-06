# SomeRandomWrapper
This Wrapper is written for **Some Random API**. It is used in the main core of our bot, or rather in **fun commands**.

### Installing the library:
To install it, you will need the standard Python package manager - **pip**. To install the library, type **pip install -U somerandomwrapper** in the console.

### Dependencies to install:
- [http3 [**^0.6.7**]](https://pypi.org/project/http3/)
- [googletrans [**^3.0.0**]](https://pypi.org/project/googletrans/)

### Some examples:
```python
from somerandomwrapper import SomeRandomWrapper
from asyncio import run

wrapperAPI = SomeRandomWrapper()
request_fact = run(await wrapperAPI.get_fact())

print(request_fact)
```

You can see other examples [here](https://github.com/Kerdokan/SomeRandomWrapper/tree/main/examples). You can also create your own example by simply making a [Pull Request](https://github.com/Kerdokan/SomeRandomWrapper/pulls).


