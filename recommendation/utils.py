from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.utils import simple_preprocess
from django.conf import settings
from pathlib import Path
from typing import List
import numpy as np

MODEL_DIR = Path(settings.BASE_DIR) / "models"
MODEL_DIR.mkdir(exist_ok=True)
MODEL_PATH = MODEL_DIR / "doc2vec.model"

def train_doc2vec(texts: List[str], vector_size: int = 100, epochs: int = 40) -> Doc2Vec:
    documents = [TaggedDocument(simple_preprocess(t), [i]) for i, t in enumerate(texts)]
    model = Doc2Vec(vector_size=vector_size, min_count=2, workers=2, epochs=epochs)
    model.build_vocab(documents)
    model.train(documents, total_examples=model.corpus_count, epochs=model.epochs)
    model.save(str(MODEL_PATH))
    return model

def load_model() -> Doc2Vec:
    return Doc2Vec.load(str(MODEL_PATH))

def infer_vector(text: str) -> List[float]:
    model = load_model()
    vec = model.infer_vector(simple_preprocess(text)).tolist()
    return vec

def cosine_sim_matrix(X: np.ndarray) -> np.ndarray:
    # Normalize
    norms = np.linalg.norm(X, axis=1, keepdims=True) + 1e-8
    Y = X / norms
    return Y @ Y.T

def most_similar(vec, candidates, topn: int = 10):
    """
    Given a vector and a list of (paper_id, embedding),
    return topn paper_ids sorted by cosine similarity.
    """
    import numpy as np
    if not candidates:
        return []

    X = np.array([emb for _, emb in candidates], dtype=float)
    v = np.array(vec, dtype=float)
    v = v / (np.linalg.norm(v) + 1e-8)
    Xn = X / (np.linalg.norm(X, axis=1, keepdims=True) + 1e-8)
    sims = Xn @ v
    ranked = sorted(zip(candidates, sims), key=lambda x: x[1], reverse=True)[:topn]
    return [pid for (pid, _), _ in ranked]

