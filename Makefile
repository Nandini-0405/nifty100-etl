setup:
	pip install -r requirements.txt

test:
	pytest

load:
	python src/etl/loader.py

clean:
	rm -rf __pycache__