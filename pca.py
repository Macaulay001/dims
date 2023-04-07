import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.cm as cm
data = pd.read_csv('CRISPRGeneEffect.csv', index_col=0)
print(data.head())
scaler=StandardScaler()
scaler.fit(data)
scaled_data=scaler.transform(data)
# scaled_data
# print(scaled_data.shape)
metadata = pd.read_csv("Model.csv", index_col=0)
# Merge the metadata with the gene expression data on the cell line names
merged_data = pd.merge(data, metadata, left_index=True, right_index=True, how="inner")

# print(merged_data.head())
metadata_subset = merged_data[["Sex"]]
# print(metadata_subset["Sex"].unique())
pca=PCA(n_components=50)
pca.fit(scaled_data)
x_pca=pca.transform(scaled_data)
# print(x_pca.shape)

# Create a scatter plot of the first two principal components
# plt.scatter(x_pca[:,0], x_pca[:,1])

# # Color the scatter plot based on the sex of the patients
# colors = {"Male": "blue", "Female": "red", "Unknown": "gray"} 
# colors_by_sex = [colors.get(sex, "black") for sex in metadata_subset["Sex"]] 

# Create the scatter plot
# plt.scatter(x_pca[:,0], x_pca[:,1], c=colors_by_sex)

# # Add axis labels and a legend
# plt.xlabel("PC1")
# plt.ylabel("PC2")
# plt.legend(handles=[plt.scatter([],[], color=color, label=sex) for sex, color in colors.items()])

# # Show the plot
# plt.show()


import umap.umap_ as umap

# Perform PCA to reduce the dimensionality of the data


# Perform UMAP on the PCA-reduced data
umap_result = umap.UMAP(n_neighbors=5, min_dist=0.3, metric='correlation').fit_transform(x_pca) #use metric cosine, number of neighbors 30, min distance 0.3
# umap_result = umap.UMAP(n_neighbors=30, min_dist=0.3, metric='cosine').fit_transform(x_pca) #use metric cosine, number of neighbors 30, min distance 0.3

# Color the UMAP plot based on the sex of the patients
colors = {"Male": "blue", "Female": "red", "Unknown": "gray"} # add 'Unknown' to colors dictionary
colors_by_sex = [colors.get(sex, "black") for sex in metadata_subset["Sex"]] # use 'get' method to handle unknown categories

# Create the UMAP plot
plt.scatter(umap_result[:,0], umap_result[:,1], c=colors_by_sex)

# Add axis labels and a legend
plt.xlabel("UMAP1")
plt.ylabel("UMAP2")
plt.legend(handles=[plt.scatter([],[], color=color, label=sex) for sex, color in colors.items()])

# Show the plot
plt.show()

