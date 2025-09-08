from django.core.management.base import BaseCommand
from articles.models import Article
from recommendation.utils import train_doc2vec, infer_vector
from tqdm import tqdm

class Command(BaseCommand):
    help = "Train Doc2Vec model on Article data and persist per-article embeddings."

    def handle(self, *args, **options):
        texts = []
        ids = []
        for a in Article.objects.all().iterator():
            text = f"{a.paper_title}. {a.author_keywords}. {a.abstract}"
            texts.append(text)
            ids.append(a.id)

        if not texts:
            self.stdout.write(self.style.WARNING("No articles found. Import CSV first."))
            return

        self.stdout.write("Training Doc2Vec model...")
        train_doc2vec(texts)

        self.stdout.write("Inferring and saving embeddings...")
        for a in tqdm(Article.objects.all().iterator()):
            text = f"{a.paper_title}. {a.author_keywords}. {a.abstract}"
            a.embedding = infer_vector(text)
            a.save(update_fields=["embedding"])

        self.stdout.write(self.style.SUCCESS("Embeddings built and saved."))
