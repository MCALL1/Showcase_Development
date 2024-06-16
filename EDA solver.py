# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 10:10:43 2024

@author: mcall
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.impute import SimpleImputer
import io

# Sample DataFrames for different data types

# Numeric Data
numeric_data = pd.DataFrame({
    'A': np.random.rand(100),
    'B': np.random.rand(100) * 100,
    'C': np.random.randn(100)
})

# Categorical Data
categorical_data = pd.DataFrame({
    'Category': np.random.choice(['A', 'B', 'C'], 100),
    'Values': np.random.randint(1, 10, 100)
})

# Datetime Data
datetime_data = pd.DataFrame({
    'Date': pd.date_range(start='1/1/2020', periods=100, freq='D'),
    'Value': np.random.randn(100)
})

def handle_missing_values(df):
    imputer = SimpleImputer(strategy='mean')
    df_imputed = pd.DataFrame(imputer.fit_transform(df.select_dtypes(include=[np.number])))
    df_imputed.columns = df.select_dtypes(include=[np.number]).columns
    df[df_imputed.columns] = df_imputed
    return df

def visualize_data(df):
    # Generate histograms for numeric columns
    df.hist(figsize=(10, 10))
    plt.show()

    # Generate box plots for numeric columns
    df.plot(kind='box', figsize=(10, 10))
    plt.show()

    # Pairplot for relationships between numeric columns
    sns.pairplot(df)
    plt.show()

def perform_chi_square_test(df):
    # Chi-square test for categorical data
    chi2_results = {}
    for col in df.select_dtypes(include=['category', 'object']):
        freq_table = df[col].value_counts()
        chi2, p = stats.chisquare(freq_table)
        chi2_results[col] = {'chi2': chi2, 'p-value': p}
    return chi2_results

def perform_anova(df):
    # ANOVA for numeric data
    anova_results = {}
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 1:
        f_val, p_val = stats.f_oneway(*[df[col] for col in numeric_cols])
        anova_results = {'F-value': f_val, 'p-value': p_val}
    return anova_results

def analyze_sheet(sheet_df):
    # Perform basic EDA
    analysis_recommendations = []
    
    # Data overview
    buffer = io.StringIO()
    sheet_df.info(buf=buffer)
    info_str = buffer.getvalue()
    print(f"Data Overview:\n{info_str}\n")
    
    # Check for missing values
    missing_values = sheet_df.isnull().sum().sum()
    if missing_values > 0:
        analysis_recommendations.append(("Handle missing values using appropriate imputation techniques.", missing_values))
        print(f"Missing Values:\n{sheet_df.isnull().sum()}\n")
        sheet_df = handle_missing_values(sheet_df)
    
    # Descriptive statistics
    desc_stats = sheet_df.describe()
    print(f"Descriptive Statistics:\n{desc_stats}\n")
    
    # Visualize data
    visualize_data(sheet_df)
    
    # Perform chi-square test if applicable
    chi_square_results = perform_chi_square_test(sheet_df)
    if chi_square_results:
        print("Chi-Square Test Results:")
        for col, result in chi_square_results.items():
            print(f"Column '{col}': chi2 = {result['chi2']}, p-value = {result['p-value']}")
        print()
        analysis_recommendations.append(("Perform chi-square test for categorical variables.", 2))
    
    # Perform ANOVA if applicable
    anova_results = perform_anova(sheet_df)
    if anova_results:
        print(f"ANOVA Results: F-value = {anova_results['F-value']}, p-value = {anova_results['p-value']}\n")
        analysis_recommendations.append(("Perform ANOVA for numeric variables.", 3))
    
    # Frequency distribution for categorical data
    freq_dist = {}
    for col in sheet_df.select_dtypes(include=['category', 'object']):
        freq_dist[col] = sheet_df[col].value_counts()
        print(f"Frequency Distribution for '{col}':\n{freq_dist[col]}\n")
        analysis_recommendations.append((f"Analyze frequency distribution for '{col}'.", 2))
    
    # Data types and possible analysis
    for column in sheet_df.columns:
        if pd.api.types.is_numeric_dtype(sheet_df[column]):
            analysis_recommendations.append((f"Perform correlation analysis, regression, or time-series analysis on '{column}'.", 3))
        elif pd.api.types.is_categorical_dtype(sheet_df[column]):
            analysis_recommendations.append((f"Conduct frequency analysis or chi-square tests on '{column}'.", 2))
        elif pd.api.types.is_datetime64_any_dtype(sheet_df[column]):
            analysis_recommendations.append((f"Perform time-series analysis on '{column}'.", 3))
    
    # Correlation analysis for numeric data
    if any(pd.api.types.is_numeric_dtype(sheet_df[col]) for col in sheet_df.columns):
        corr = sheet_df.corr()
        sns.heatmap(corr, annot=True, cmap='coolwarm')
        plt.title('Correlation Matrix')
        plt.show()
        analysis_recommendations.append(("Analyze the correlation matrix for numeric variables.", 3))
    
    # Sort recommendations by relevance
    sorted_recommendations = sorted(analysis_recommendations, key=lambda x: x[1], reverse=True)
    top_recommendations = [rec[0] for rec in sorted_recommendations[:3]]
    
    return top_recommendations, desc_stats

def recommend_analysis(dataframes):
    # Iterate through each sample DataFrame and analyze
    for df_name, sheet_df in dataframes.items():
        print(f"Analyzing DataFrame: {df_name}\n")
        recommendations, desc_stats = analyze_sheet(sheet_df)
        print(f"Top 3 Recommendations for DataFrame '{df_name}':\n")
        for recommendation in recommendations:
            print(f"- {recommendation}")
        print("\n")
        print(f"Sample Descriptive Statistics for DataFrame '{df_name}':\n{desc_stats}\n")

# Example usage with sample data
sample_dataframes = {
    'Numeric Data': numeric_data,
    'Categorical Data': categorical_data,
    'Datetime Data': datetime_data
}

recommend_analysis(sample_dataframes)
