# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 16:38:00 2024

@author: mcall
"""

import requests
from bs4 import BeautifulSoup
import tkinter as tk
import json

# Function to search Google
def search_google(query):
    url = f"https://www.google.com/search?q={query}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all('div', class_='BNeawe s3v9rd AP7Wnd')
    return [result.get_text() for result in results[:10]]

# Function to search Reddit
def search_reddit(query):
    url = f"https://www.reddit.com/search/?q={query}"
    headers = {'User-Agent': 'Mozilla/5.0', 'Accept-Language': 'en-US,en;q=0.5'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all('a', {'data-click-id': 'body'})
    return [result.get_text() for result in results[:10]]

# Function to search LinkedIn
def search_linkedin(query):
    url = f"https://www.linkedin.com/search/results/people/?keywords={query}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all('span', {'class': 'name actor-name'})
    return [result.get_text() for result in results[:10]]

# Function to search Instagram
def search_instagram(query):
    url = f"https://www.instagram.com/web/search/topsearch/?query={query}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    data = response.json()
    return [user['user']['username'] for user in data.get('users', [])[:10]]

# Function to display results in the text box
def display_results(results, platform):
    result_text.insert(tk.END, f"Results from {platform}:\n")
    for result in results:
        if len(result) > 500:
            result_text.insert(tk.END, result[:500] + "... more to follow\n")
        else:
            result_text.insert(tk.END, result + "\n")
    result_text.insert(tk.END, "\n")

# Function to start search
def start_search():
    name_query = name_entry.get()
    location_query = location_entry.get()
    age_query = age_entry.get()
    sex_query = sex_entry.get()
    full_query = f"{name_query} {location_query} {age_query} {sex_query}"
    result_text.delete('1.0', tk.END)
    
    try:
        google_results = search_google(full_query)
        display_results(google_results, "Google")
    except Exception as e:
        display_results([str(e)], "Google")

    try:
        reddit_results = search_reddit(full_query)
        display_results(reddit_results, "Reddit")
    except Exception as e:
        display_results([str(e)], "Reddit")

    try:
        linkedin_results = search_linkedin(full_query)
        display_results(linkedin_results, "LinkedIn")
    except Exception as e:
        display_results([str(e)], "LinkedIn")

    try:
        instagram_results = search_instagram(full_query)
        display_results(instagram_results, "Instagram")
    except Exception as e:
        display_results([str(e)], "Instagram")

# Create the main window
root = tk.Tk()
root.title("OSINT Search Tool")

# Create a text entry box for name
name_label = tk.Label(root, text="Enter First and Last Name:")
name_label.pack(pady=5)
name_entry = tk.Entry(root, width=50)
name_entry.pack(pady=5)

# Create a text entry box for location
location_label = tk.Label(root, text="Enter Location:")
location_label.pack(pady=5)
location_entry = tk.Entry(root, width=50)
location_entry.pack(pady=5)

# Create a text entry box for age
age_label = tk.Label(root, text="Enter Age:")
age_label.pack(pady=5)
age_entry = tk.Entry(root, width=50)
age_entry.pack(pady=5)

# Create a text entry box for sex
sex_label = tk.Label(root, text="Enter Sex (Male/Female):")
sex_label.pack(pady=5)
sex_entry = tk.Entry(root, width=50)
sex_entry.pack(pady=5)

# Create a search button
search_button = tk.Button(root, text="Search", command=start_search)
search_button.pack(pady=10)

# Create a text box to display results
result_text = tk.Text(root, width=100, height=30)
result_text.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()

