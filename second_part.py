"""Junior Data Analyst test task
Part 2. Plotting"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def multline(line):
    """Split keyword string with multiple words into two lines"""

    s_line = line.split()
    s_line.insert(len(s_line)//2, '<br>')

    return ' '.join(s_line)


# Load preprocessed data
df = pd.read_csv('tz_data_out.csv')

# Unique cluster names
unique_clusters = df.cluster_name.unique()

# Hex color codes
plotly_colors = px.colors.qualitative.Plotly

# Mapping from color code to cluster name
color_map = {color: cluster for cluster, color in zip(unique_clusters, plotly_colors)}

# Group dataframe by area
groups_area = [df_area[1] for df_area in df.groupby(by='area')]


def scatter_area(df_area):
    """Plot points from a single are"""

    fig = go.Figure()

    # Split dataframe by clusters to properly display legend
    groups_clusers = [df_cluster[1] for df_cluster in df_area.groupby(by='cluster_name')]

    for cluster_name, df_cluster in zip(unique_clusters, groups_clusers):

        # Multline point labels
        keywords = [multline(keyword) for keyword in df_cluster.keyword.to_list()]

        # Scatter plot
        fig.add_trace(go.Scatter(
            x=df_cluster.x,
            y=df_cluster.y,
            text=keywords,
            name=cluster_name,
            mode='text+markers',
            marker=dict(line=dict(width=2,
                                  color='DarkSlateGrey'),
                        size=df_cluster['count'].to_numpy()/10,
                        color=df_cluster['color']
                        ),
            showlegend=True
        ))

    area_name = df_area.iloc[0].area
    area_name = area_name.replace('\\', '-')

    # Set layout
    fig.update_layout(
        font_family="Times New Roman",
        font_size=34,
        font_color="black",
        plot_bgcolor='white',
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        title=dict(
          text=f'<i>Диаграмма для области "{area_name}"<i>',
          x=0.8,
          y=0.05
        ),
        legend=dict(
            title='<b>Кластеры<b>',
            itemsizing='trace',
            x=1,
            y=0.5,
            bordercolor="Grey",
            borderwidth=2)
        )

    # Save figure
    fig.write_image(f"images/{area_name}.png", width=3840, height=2160)


if __name__ == '__main__':
    for df_area in groups_area:
        scatter_area(df_area)
