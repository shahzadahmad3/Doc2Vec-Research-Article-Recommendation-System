import pandas as pd
from .models import Article

def import_csv_data(file_path):
    df = pd.read_csv(file_path, encoding="latin1")  # or encoding="ISO-8859-1"
    for index, row in df.iterrows():
        Article.objects.create(
            paper_id=row['paper_id'],
            paper_title=row['paper_title'],
            author_keywords=row['author_keywords'],
            abstract=row['abstract'],
            area=row['area']
        )