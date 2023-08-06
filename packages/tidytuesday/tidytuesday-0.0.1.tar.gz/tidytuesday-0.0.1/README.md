# tidytuesdayPy

Download TidyTuesday data.

## Usage

```python
from tidytuesday import TidyTuesday

tt = TidyTuesday("2021-04-06")
```

You can then access each data set as an attribute.

```python
df = tt.forest
```

You can also access the readme.

```python
print(tt.readme)
```
