install:
	pip install -r requirements.txt

ingest:
	python src/ingestion/real_weather_ingestion.py

quality:
	python src/utils/data_quality_checks.py

silver:
	python src/transformations/bronze_to_silver_weather.py

gold:
	python src/transformations/silver_to_gold_weather.py

pyspark:
	python src/transformations/pyspark_weather_transformation.py

pipeline:
	make ingest
	make quality
	make silver
	make gold
