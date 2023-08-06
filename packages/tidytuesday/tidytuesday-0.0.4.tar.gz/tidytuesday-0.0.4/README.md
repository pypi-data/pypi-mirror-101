# tidytuesdayPy

Download TidyTuesday data.  Inspired by [tidytuesdayR](https://github.com/thebioengineer/tidytuesdayR).

## Usage

```python
from tidytuesday import TidyTuesday

tt = TidyTuesday("2021-04-06")
```

You can then access each data set as an attribute.  Hyphens (if present) are converted to underscores.

```python
df = tt.forest
```

You can also access the readme.

```python
print(tt.readme)
```

## TODO

- Rate limit checks
- Implement parsers for zip and rds formats
