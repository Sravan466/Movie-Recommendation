import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

# Load your dataset
movies = pd.read_csv("moviedataset.csv")

# Ensure there are no missing values in the 'overview' column
movies['overview'] = movies['overview'].fillna('')

# Convert the 'overview' into feature vectors
vectorizer = CountVectorizer(stop_words='english')
vectors = vectorizer.fit_transform(movies['overview'])

# Compute the cosine similarity matrix
similarity = cosine_similarity(vectors)

# Save the similarity matrix and movies data
with open("similarity.pkl", "wb") as sim_file:
    pickle.dump(similarity, sim_file)

with open("movies_list.pkl", "wb") as movies_file:
    pickle.dump(movies, movies_file)

print("Similarity matrix and movies list saved successfully!")
