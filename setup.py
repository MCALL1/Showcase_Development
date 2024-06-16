# -*- coding: utf-8 -*-
"""
This script will:

    Set up a virtual environment.
    Install a list of common libraries used in data science and machine learning.
    Configure Jupyter Notebook with useful extensions.
    Set up pre-commit hooks to ensure code quality.

@author: mcall
"""

import subprocess
import os

# List of common libraries to install
libraries = [
    "numpy", "pandas", "matplotlib", "seaborn", "scikit-learn",
    "tensorflow", "keras", "nltk", "spacy", "textblob", "gensim",
    "beautifulsoup4", "requests", "openpyxl", "xlrd", "python-docx",
    "pillow", "flask", "django", "tweepy", "jupyter", "jupyterlab",
    "jupyter_contrib_nbextensions", "pyspark", "hdfs", "geopandas",
    "shapely", "folium", "pre-commit", "flake8", "black"
]

# Function to install libraries
def install_libraries(libraries):
    for library in libraries:
        try:
            subprocess.check_call(["pip", "install", library])
            print(f"Successfully installed {library}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {library}: {e}")

# Function to set up Jupyter Notebook with extensions
def setup_jupyter():
    try:
        subprocess.check_call(["pip", "install", "jupyter", "jupyterlab", "jupyter_contrib_nbextensions"])
        subprocess.check_call(["jupyter", "contrib", "nbextension", "install", "--user"])
        subprocess.check_call(["jupyter", "nbextension", "enable", "--py", "widgetsnbextension", "--sys-prefix"])
        print("Successfully set up Jupyter Notebook with extensions")
    except subprocess.CalledProcessError as e:
        print(f"Failed to set up Jupyter: {e}")

# Function to set up a virtual environment
def setup_virtualenv():
    try:
        subprocess.check_call(["python", "-m", "venv", "venv"])
        if os.name == 'nt':
            subprocess.check_call([os.path.join("venv", "Scripts", "activate.bat")])
        else:
            subprocess.check_call(["source", "venv/bin/activate"])
        subprocess.check_call(["pip", "install", "--upgrade", "pip"])
        print("Successfully set up virtual environment")
    except subprocess.CalledProcessError as e:
        print(f"Failed to set up virtual environment: {e}")

# Function to set up pre-commit hooks
def setup_precommit():
    try:
        subprocess.check_call(["pip", "install", "pre-commit"])
        subprocess.check_call(["pre-commit", "install"])
        with open(".pre-commit-config.yaml", "w") as f:
            f.write("repos:\n- repo: https://github.com/pre-commit/pre-commit-hooks\n  rev: v3.4.0\n  hooks:\n    - id: trailing-whitespace\n    - id: end-of-file-fixer\n    - id: check-yaml\n    - id: check-json\n")
        print("Successfully set up pre-commit hooks")
    except subprocess.CalledProcessError as e:
        print(f"Failed to set up pre-commit hooks: {e}")

# Main function to run the setup
def main():
    setup_virtualenv()
    install_libraries(libraries)
    setup_jupyter()
    setup_precommit()

if __name__ == "__main__":
    main()
