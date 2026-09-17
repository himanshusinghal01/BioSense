import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class SimpleRetriever:
    def __init__(self, knowledge_path="data/knowledge.json"):
        self.documents = []
        if os.path.exists(knowledge_path):
            with open(knowledge_path, "r", encoding="utf-8") as f:
                self.documents = json.load(f)
        
        self.vectorizer = TfidfVectorizer(stop_words="english")
        if self.documents:
            corpus = [doc["keywords"] + " " + doc["content"] for doc in self.documents]
            self.tfidf_matrix = self.vectorizer.fit_transform(corpus)

    def retrieve(self, query, top_k=2):
        if not self.documents:
            return []
        
        query_vec = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
        
        top_indices = similarities.argsort()[::-1][:top_k]
        results = []
        for idx in top_indices:
            if similarities[idx] > 0.05:
                doc = self.documents[idx].copy()
                doc["score"] = float(similarities[idx])
                results.append(doc)
        
        return results
