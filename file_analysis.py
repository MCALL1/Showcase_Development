# -*- coding: utf-8 -*-
"""
Created on Sun Jun 23 19:32:03 2024

@author: mcall
"""
import os
import docx
from openpyxl import load_workbook
from datetime import datetime
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from textblob import TextBlob  # for sentiment analysis
from spacy.lang.en import English  # for entity recognition
import matplotlib.pyplot as plt

def read_docx(filename):
    doc = docx.Document(filename)
    text = []
    for paragraph in doc.paragraphs:
        text.append(paragraph.text)
    return '\n'.join(text), extract_docx_metadata(doc)

def read_xlsx():
    wb = load_workbook(filename)
    ws = wb.active
    # Assuming financial data is organized with headers (e.g., 'Quarter', 'Revenue', 'Expenses', 'Profit')
    df = pd.DataFrame(ws.values)
    df.columns = df.iloc[0]  # Use the first row as headers
    df = df[1:]  # Skip the first row (headers)
    
    return df, extract_xlsx_metadata(wb)

def extract_docx_metadata(doc):
    metadata = {
        "Title": doc.core_properties.title,
        "Author": doc.core_properties.author,
        "Created": doc.core_properties.created,
        "Modified": doc.core_properties.modified,
        "Last Modified By": doc.core_properties.last_modified_by,
    }
    return metadata

def extract_xlsx_metadata(wb):
    metadata = {
        "Title": wb.properties.title,
        "Author": wb.properties.creator,
        "Created": wb.properties.created,
        "Modified": wb.properties.modified,
    }
    return metadata

def perform_basic_stats(text):
    # Tokenize words
    words = text.split()
    
    # Basic statistics
    word_count = len(words)
    unique_words = len(set(words))
    avg_word_length = np.mean([len(word) for word in words])

    # Explanation
    explanation = f"Total words: {word_count}, Unique words: {unique_words}, Average word length: {avg_word_length:.2f}"
    
    return explanation

def perform_sentiment_analysis(text):
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity
    sentiment_label = "Positive" if sentiment_score > 0 else "Negative" if sentiment_score < 0 else "Neutral"

    # Explanation
    explanation = f"Sentiment score: {sentiment_score:.2f} (Overall sentiment: {sentiment_label})"
    
    return explanation

def perform_topic_modeling(text):
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform([text])

    # Topic modeling with LDA
    lda = LatentDirichletAllocation(n_components=3, random_state=42)
    lda.fit(X)

    # Display top words per topic
    feature_names = vectorizer.get_feature_names_out()
    topics = []
    for topic_idx, topic in enumerate(lda.components_):
        top_words = [feature_names[i] for i in topic.argsort()[:-10 - 1:-1]]
        topics.append(f"Topic {topic_idx + 1}: {' | '.join(top_words)}")

    # Explanation
    explanation = "\n".join(topics)
    
    return explanation

def perform_entity_recognition(text):
    nlp = English()
    doc = nlp(text)
    entities = [entity.text for entity in doc.ents if entity.label_ in ['ORG', 'PERSON', 'GPE']]

    # Explanation
    explanation = f"Entities found: {', '.join(entities)}"
    
    return explanation

def perform_cluster_analysis(text):
    # Example analysis: Tokenize text for clustering
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform([text])

    # Perform clustering
    kmeans = KMeans(n_clusters=3, random_state=42)
    kmeans.fit(X)
    labels = kmeans.labels_

    # Principal Component Analysis for visualization
    pca = PCA(n_components=2, random_state=42)
    reduced_features = pca.fit_transform(X.toarray())
    plt.scatter(reduced_features[:, 0], reduced_features[:, 1], c=labels, cmap='viridis')
    plt.title('Clustering Visualization')
    plt.xlabel('PCA Component 1')
    plt.ylabel('PCA Component 2')
    plt.show()

    # Explanation
    explanation = "Performed clustering analysis. See visualization for cluster distribution."
    
    return explanation

def calculate_financial_statistics(df):
    # Assuming columns: 'Quarter', 'Revenue', 'Expenses', 'Profit'
    quarters = df['Quarter']
    revenue = df['Revenue'].astype(float)
    expenses = df['Expenses'].astype(float)
    profit = df['Profit'].astype(float)
    
    # Basic statistics
    total_quarters = len(quarters)
    mean_revenue = np.mean(revenue)
    std_expenses = np.std(expenses)
    max_profit = np.max(profit)
    min_profit = np.min(profit)
    
    # Explanation
    explanation = (
        f"Total quarters: {total_quarters}\n"
        f"Mean revenue: ${mean_revenue:.2f}\n"
        f"Standard deviation of expenses: ${std_expenses:.2f}\n"
        f"Maximum profit: ${max_profit:.2f} (Quarter {quarters.iloc[np.argmax(profit)]})\n"
        f"Minimum profit: ${min_profit:.2f} (Quarter {quarters.iloc[np.argmin(profit)]})"
    )
    
    return explanation

def main():
    try:
        filename = input("Enter the file path: ")

        if filename.endswith('.docx'):
            text, metadata = read_docx(filename)
            # Perform text analytics
            stats_explanation = perform_basic_stats(text)
            sentiment_explanation = perform_sentiment_analysis(text)
            topics_explanation = perform_topic_modeling(text)
            entities_explanation = perform_entity_recognition(text)
            cluster_explanation = perform_cluster_analysis(text)

            # Output text analytics results
            print("===== Text Analytics Results =====")
            print("1. Basic Statistics:")
            print(stats_explanation)
            print("\n2. Sentiment Analysis:")
            print(sentiment_explanation)
            print("\n3. Topic Modeling:")
            print(topics_explanation)
            print("\n4. Entity Recognition:")
            print(entities_explanation)
            print("\n5. Cluster Analysis:")
            print(cluster_explanation)
        
        elif filename.endswith('.xlsx'):
            df, metadata = read_xlsx(filename)
            # Perform financial data analysis
            stats_explanation = calculate_financial_statistics(df)

            # Output financial data analytics results
            print("===== Financial Data Analytics Results =====")
            print("1. Basic Statistics:")
            print(stats_explanation)
        
        else:
            raise ValueError("Unsupported file type. Only .docx and .xlsx are supported.")

        # Output Metadata
        print("\n===== Metadata =====")
        for key, value in metadata.items():
            print(f"{key}: {value}")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
