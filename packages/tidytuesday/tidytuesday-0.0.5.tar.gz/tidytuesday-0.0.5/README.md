# tidytuesdayPy

Download TidyTuesday data.  Inspired by [tidytuesdayR](https://github.com/thebioengineer/tidytuesdayR).

## Usage

```python
from tidytuesday import TidyTuesday

tt = TidyTuesday("2021-04-06")
```

You can then access each data set from the data field.

```python
df = tt.data["forest"]
```

You can also access the readme.

```python
print(tt.readme)
```

## TODO

- Implement parsers for rds formats
- Documentation
