"""Build a dataframe from a list of values."""

import pandas as pd

values = [1.0, 2.0, 3.0]
dataframe = pd.DataFrame({"value": values})

print(dataframe)
