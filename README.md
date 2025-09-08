"# Doc2Vec-Research-Article-Recommendation-System" 


## Recommendation App Usage

- Import data (if needed): `python manage.py shell -c "from articles.import_csv import import_csv_data; import_csv_data('Papers data.csv')"`
- Build embeddings: `python manage.py build_embeddings`
- Open search UI: visit `/reco/search/`
- Recommend by specific article: `/reco/by-article/<paper_id>/`
