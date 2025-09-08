from django.shortcuts import render
from .models import Article
from recommendation.utils import infer_vector, most_similar

# Create your views here.

def home(request):
    return render(request, 'articles/home.html')

def recommend_articles(request, article_id):
    article = Article.objects.get(paper_id=article_id)
    if not article.embedding:
        return render(request, 'articles/recommendations.html', {'error': 'No embedding available.'})

    # Get all other articles
    articles = Article.objects.exclude(paper_id=article_id)
    candidates = [(a.paper_id, a.embedding) for a in articles if a.embedding]

    similar_ids = most_similar(article.embedding, candidates)
    similar_articles = Article.objects.filter(paper_id__in=similar_ids)

    return render(request, 'articles/recommendations.html', {
        'similar_articles': similar_articles,
        'article_id': article_id
    })


def article_detail(request, article_id):
    article = Article.objects.get(paper_id=article_id)
    articles = Article.objects.exclude(paper_id=article_id)
    candidates = [(a.paper_id, a.embedding) for a in articles if a.embedding]

    if article.embedding:
        similar_ids = most_similar(article.embedding, candidates)
        similar_articles = Article.objects.filter(paper_id__in=similar_ids)
    else:
        similar_articles = []

    return render(request, 'articles/article_detail.html', {
        'article': article,
        'similar_articles': similar_articles
    })
