# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 16:06:26 2024

@author: mcall
"""
import requests
from bs4 import BeautifulSoup
import tkinter as tk

# Function to search Google
def search_google(query):
    url = f"https://www.google.com/search?q={query}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all('h3')
    return [result.get_text() for result in results[:10]]

# Function to search Reddit
def search_reddit(query):
    url = f"https://www.reddit.com/search/?q={query}"
    headers = {'User-Agent': 'Mozilla/5.0'}
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
        result_text.insert(tk.END, result + "\n")
    result_text.insert(tk.END, "\n")

# Function to start search
def start_search():
    query = entry.get()
    result_text.delete('1.0', tk.END)
    
    google_results = search_google(query)
    reddit_results = search_reddit(query)
    linkedin_results = search_linkedin(query)
    instagram_results = search_instagram(query)

    display_results(google_results, "Google")
    display_results(reddit_results, "Reddit")
    display_results(linkedin_results, "LinkedIn")
    display_results(instagram_results, "Instagram")

# Create the main window
root = tk.Tk()
root.title("OSINT Search Tool")

# Create a text entry box
entry = tk.Entry(root, width=50)
entry.pack(pady=10)

# Create a search button
search_button = tk.Button(root, text="Search", command=start_search)
search_button.pack(pady=10)

# Create a text box to display results
result_text = tk.Text(root, width=100, height=30)
result_text.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()

