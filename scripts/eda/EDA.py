import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import textwrap

missing_values = movies_df.isnull().sum()

missing_values = missing_values[missing_values > 0]
missing_values.sort_values(inplace = True)

plt.figure(figsize = (14,10))
missing_values.plot(kind = "barh", color = "green")
plt.show()
