from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest
from articles.models import Article
from recommendation.utils import infer_vector, cosine_sim_matrix
import numpy as np
from django.contrib.auth.decorators import login_required

@login_required
def recommend_by_article(request: HttpRequest, paper_id: str):
    target = get_object_or_404(Article, paper_id=paper_id)
    articles = list(Article.objects.exclude(id=target.id).filter(embedding__isnull=False))
    if not target.embedding or not articles:
        return render(request, "recommendation/empty.html", {"reason": "Embeddings missing. Run: python manage.py build_embeddings"})

    X = np.array([target.embedding] + [a.embedding for a in articles], dtype=float)
    S = cosine_sim_matrix(X)
    sims = S[0, 1:]  # similarity with others
    ranked = sorted(zip(articles, sims), key=lambda x: x[1], reverse=True)[:10]
    return render(request, "recommendation/list.html", {"query": target.paper_title, "results": ranked})

@login_required
def recommend_by_query(request: HttpRequest):
    q = request.GET.get("q", "").strip()
    if not q:
        return render(request, "recommendation/search.html")
    vec = np.array(infer_vector(q), dtype=float)
    articles = list(Article.objects.filter(embedding__isnull=False))
    if not articles:
        return render(request, "recommendation/empty.html", {"reason": "No embeddings found. Run: python manage.py build_embeddings"})
    X = np.array([a.embedding for a in articles], dtype=float)
    S = cosine_sim_matrix(np.vstack([vec, X]))
    sims = S[0, 1:]
    ranked = sorted(zip(articles, sims), key=lambda x: x[1], reverse=True)[:10]
    return render(request, "recommendation/list.html", {"query": q, "results": ranked})
