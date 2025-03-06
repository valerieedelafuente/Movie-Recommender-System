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

#plotting missing values 
plt.figure(figsize = (18,8))
sns.heatmap(movies_df.isnull(), cmap = sns.color_palette("viridis", as_cmap = True))
plt.show()

