import pandas as pd
from sentence_transformers import SentenceTransformer, util

file_path = 'projections/projections_summary_webgpt.csv'

# Reading the CSV file
data = pd.read_csv(file_path)

# Initialize the Sentence Transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Iterate over each row
for index, row in data.iterrows():
    # Extract texts from the two columns
    text1 = row['Original']
    text2 = row['GPT']

    # Compute embeddings
    embeddings1 = model.encode(text1, convert_to_tensor=True)
    embeddings2 = model.encode(text2, convert_to_tensor=True)

    # Compute cosine similarity
    cos_sim = util.pytorch_cos_sim(embeddings1, embeddings2)

    # Print the similarity score
    print(f"Row {index + 1} Similarity Score: {cos_sim.item():.4f}")
