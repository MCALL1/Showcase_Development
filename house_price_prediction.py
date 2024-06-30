# -*- coding: utf-8 -*-
"""
Created on Sun March 3 14:08:40 2024

@author: mcall
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
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

    plt.figure(figsize=(10, 6))
    sns.histplot(df['SalePrice'], kde=True)
    plt.title('SalePrice Distribution')
    plt.show()

# Preprocess data
def preprocess_data(df):
    # Separate target variable
    X = df.drop('SalePrice', axis=1)
    y = df['SalePrice']

    # Numerical and categorical columns
    numeric_features = X.select_dtypes(include=['int64', 'float64']).columns
    categorical_features = X.select_dtypes(include=['object']).columns

    # Preprocessing pipelines for numerical and categorical data
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    return X_train, X_test, y_train, y_test, preprocessor

# Train model
def train_model(X_train, y_train, preprocessor):
    # Define model pipeline
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
    ])

    # Hyperparameter tuning
    param_grid = {
        'regressor__n_estimators': [50, 100, 200],
        'regressor__max_features': ['auto', 'sqrt', 'log2'],
        'regressor__max_depth': [None, 10, 20, 30]
    }

    grid_search = GridSearchCV(model, param_grid, cv=5, scoring='neg_mean_squared_error', n_jobs=-1)
    grid_search.fit(X_train, y_train)

    return grid_search.best_estimator_

# Evaluate model
def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)

    mse = mean

