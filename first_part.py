"""Junior Data Analyst test task
Part 1. Data processing"""

import pandas as pd
import plotly.express as px


# Load data
df = pd.read_csv('tz_data.csv')

# Drop rows with missing data
df = df.dropna()

# 'count' column data type is str, convert to int. Drop row if not convertible.
for index, row in df.iterrows():
    try:
        df.loc[index, 'count'] = int(row['count'])
    except:
        df = df.drop([index])

# Sort values according to 1.4
df = df.sort_values(['area', 'cluster', 'count'], ascending=[True, True, False])

# Unique cluster names
unique_clusters = df.cluster_name.unique()

# Hex color codes
plotly_colors = px.colors.qualitative.Plotly

# Mapping from cluster name to color code
color_map = {cluster: color for cluster, color in zip(unique_clusters, plotly_colors)}

# Create color column
color = [color_map[cluster] for cluster in df.cluster_name]

# Add color column to dataframe
df['color'] = color

# Drop duplicate keyword for each area
groups_area = [df_area[1].drop_duplicates(subset=['keyword']) for df_area in df.groupby(by='area')]
df = pd.concat(groups_area)

# Save results
df.to_csv('tz_data_out.csv', index=False)
