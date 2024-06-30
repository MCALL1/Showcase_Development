# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 14:32:48 2024

@author: mcall
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from docx import Document

# Function to load data from Excel
def load_data_from_excel(file_path):
    return pd.read_excel(file_path)

# Function to load data from Word document
def load_data_from_word(file_path):
    doc = Document(file_path)
    data = []
    keys = None
    for i, table in enumerate(doc.tables):
        for j, row in enumerate(table.rows):
            text = (cell.text for cell in row.cells)
            if j == 0:
                keys = tuple(text)
                continue
            row_data = dict(zip(keys, text))
            data.append(row_data)
    return pd.DataFrame(data)

# Perform EDA
def perform_eda(df):
    print("Data Overview:")
    print(df.head())
    print("\nData Description:")
    print(df.describe())
    print("\nMissing Values:")
    print(df.isnull().sum())

    # Visualizations
    plt.figure(figsize=(10, 6))
    sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
    plt.title('Correlation Matrix')
    plt.show()

# Preprocess data
def preprocess_data(df):
    # Fill missing values
    df = df.fillna(df.median())

    # Standardize the data
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df)

    return df_scaled

# Determine the optimal number of clusters using the Elbow Method
def determine_optimal_clusters(data):
    wcss = []
    for i in range(1, 11):
        kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=42)
        kmeans.fit(data)
        wcss.append(kmeans.inertia_)
    
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, 11), wcss)
    plt.title('Elbow Method')
    plt.xlabel('Number of clusters')
    plt.ylabel('WCSS')
    plt.show()

# Perform K-Means clustering
def perform_kmeans(data, num_clusters):
    kmeans = KMeans(n_clusters=num_clusters, init='k-means++', max_iter=300, n_init=10, random_state=42)
    clusters = kmeans.fit_predict(data)
    
    return clusters

# Main function to run the workflow
def main(file_path, file_type):
    if file_type == 'excel':
        df = load_data_from_excel(file_path)
    elif file_type == 'word':
        df = load_data_from_word(file_path)
    else:
        raise ValueError("Unsupported file type. Use 'excel' or 'word'.")

    perform_eda(df)

    df_scaled = preprocess_data(df)

    determine_optimal_clusters(df_scaled)
    
    # Assuming the optimal number of clusters is 5 for this example
    num_clusters = 5
    clusters = perform_kmeans(df_scaled, num_clusters)
    
    df['Cluster'] = clusters
    
    print("Clustered Data:")
    print(df.head())

if __name__ == "__main__":
    # Update with your dataset path and file type
    file_path = 'path_to_your_file.xlsx'  # or 'path_to_your_file.docx'
    file_type = 'excel'  # or 'word'
    main(file_path, file_type)
