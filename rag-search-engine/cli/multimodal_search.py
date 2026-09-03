from PIL import Image
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pickle
import os
from semantic_search_cli import load_movies

class MultimodalSearch:
    CACHE_FILE = ".embeddings_cache.pkl"

    def __init__(self, model_name= "clip-ViT-B-32"):
        self.model = SentenceTransformer(model_name)
        self.documents = load_movies()

        if self.documents:
            self.texts = [f"{doc['title']}: {doc['description']}" for doc in self.documents]

            if os.path.exists(self.CACHE_FILE):
                with open(self.CACHE_FILE, 'rb') as f:
                    self.text_embeddings = pickle.load(f)
            else:
                self.text_embeddings = self.model.encode(self.texts, show_progress_bar=True)
                with open(self.CACHE_FILE, 'wb') as f:
                    pickle.dump(self.text_embeddings, f)

    def embed_image(self, image_path: str):
        image = Image.open(image_path).convert("RGB")
        return self.model.encode(image)

    def embed_text(self, text: str):
        return self.model.encode(text)

    def search_with_image(self, image_path: str, top_k: int = 5):
        '''Generate an embedding for the provided image.
            Iterate over the text embeddings, calculating cosine similarity 
            between each of them and the image embedding.
            Sort the results by similarity score, in descending order, and 
            return the first 5 results.
            Return a list of dicts, each containing the document ID, title, description, and similarity score.'''

        image_embedding = self.embed_image(image_path)
        if not hasattr(self, "text_embeddings"):
            raise ValueError("No text embeddings available for search")

        similarities = cosine_similarity([image_embedding], self.text_embeddings)[0]
        top_indices = np.argsort(similarities)[::-1][:top_k]
        results = []
        for idx in top_indices:
            doc = self.documents[idx]
            results.append({
                "id": doc.get("id"),
                "title": doc.get("title"),
                "description": doc.get("description"),
                "similarity": float(similarities[idx])
            })
        return results  

def image_search_command(model: MultimodalSearch, image_path: str, top_k: int = 5):
    results = model.search_with_image(image_path, top_k=top_k)
    for idx, result in enumerate(results):
        print(f"{idx + 1}. {result['title']} (similarity: {result['similarity']:.3f})")
        desc = result['description'].replace('\n', ' ').strip()
        if len(desc) > 100:
            desc = desc[:100] + "..."
        print(f"   {desc}\n")


def verify_image_embedding(model: MultimodalSearch, image_path: str):
    embedding = model.embed_image(image_path)
    if embedding is None:
        raise ValueError("Failed to generate image embedding")
    else:
        print("Image embedding generated successfully")
        print(f"Embedding shape: {embedding.shape[0]} dimensions")