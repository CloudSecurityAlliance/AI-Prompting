#!/usr/bin/env python3

#
# Usage: nltk-compare-fields.py python3  input.csv output
# Requires a bunch of pip3 install, see imports
#

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import AgglomerativeClustering
import argparse
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string

# Ensure NLTK data is downloaded
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

# Setup command line arguments
parser = argparse.ArgumentParser(description='Group items based on textual similarity.')
parser.add_argument('input_file', type=str, help='Path to the input CSV file')
parser.add_argument('output_file', type=str, help='Path to the output file where related CSA-IDs will be listed')
args = parser.parse_args()

# Load CSV data
df = pd.read_csv(args.input_file)

# Preprocessing function
def preprocess_text(text):
    text = text.lower()
    tokens = word_tokenize(text.translate(str.maketrans('', '', string.punctuation)))
    stemmer = PorterStemmer()
    stemmed = [stemmer.stem(token) for token in tokens if token not in stopwords.words('english') and token.isalpha()]
    return ' '.join(stemmed)

# Preprocess data
df.fillna('', inplace=True)
for column in ['NAME_OF_ITEM', 'ALSO_KNOWN_AS', 'DESCRIPTION']:
    df[column] = df[column].apply(preprocess_text)
df['combined_text'] = df['NAME_OF_ITEM'] + ' ' + df['ALSO_KNOWN_AS'] + ' ' + df['DESCRIPTION']

# TF-IDF Vectorization
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(df['combined_text'])

# Clustering
clustering = AgglomerativeClustering(n_clusters=None, distance_threshold=0.7, compute_full_tree=True)
labels = clustering.fit_predict(tfidf_matrix.toarray())

# Group CSA-IDs by cluster
clusters = pd.Series(index=df.index, data=labels).to_dict()
clustered_ids = {}
for index, cluster_id in clusters.items():
    if cluster_id not in clustered_ids:
        clustered_ids[cluster_id] = []
    clustered_ids[cluster_id].append(df.iloc[index]['CSA_ID'])

# Output clusters to file
with open(args.output_file, 'w') as f:
    for cluster_id, ids in clustered_ids.items():
        f.write(f"Cluster {cluster_id}: {', '.join(ids)}\n")

print(f'Clusters saved to {args.output_file}')

