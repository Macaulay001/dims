import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.cm as cm
import csv
import umap.umap_ as umap

# Load the gene expression data
data = pd.read_csv('CRISPRGeneEffect.csv', index_col=0)

# Standardize the data
scaler=StandardScaler()
scaler.fit(data)
scaled_data=scaler.transform(data)

# Load the metadata and merge it with the gene expression data on the cell line names
metadata = pd.read_csv("Model.csv", index_col=0)
merged_data = pd.merge(data, metadata, left_index=True, right_index=True, how="inner")


# Perform PCA on the standardized gene expression data
pca=PCA(n_components=30)
pca.fit(scaled_data)
x_pca=pca.transform(scaled_data)

# Loop over each column in the metadata and create a UMAP plot colored by the values in that column
column_cont = list(metadata.columns)
for content in column_cont:
    metadata_subset = merged_data[[content]]

    # Get the values of the column we're interested in and create a colormap for them
    SSC_metadata_subset = merged_data[[content]]
    unique_categories = SSC_metadata_subset[content].unique()
    num_categories = len(unique_categories)
    cmap = cm.get_cmap('tab20', num_categories)

    # Perform UMAP dimensionality reduction on the PCA-transformed data
    umap_result = umap.UMAP(n_neighbors=5, min_dist=0.3, metric='correlation').fit_transform(x_pca)

    # Map each category to a color from the colormap
    category_to_color = {category: cmap(i) for i, category in enumerate(unique_categories)}
    colors_by_category = [category_to_color[category] for category in SSC_metadata_subset[content]]

    # Create the UMAP plot with the points colored by category
    plt.scatter(umap_result[:,0], umap_result[:,1], c=colors_by_category)

    # Add axis labels and a legend
    plt.xlabel("UMAP1")
    plt.ylabel("UMAP2")
    plt.legend(handles=[plt.scatter([],[], color=category_to_color[category], label=category) for category in unique_categories])

    # Show the plot
    plt.show()
