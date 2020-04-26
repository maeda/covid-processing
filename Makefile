freeze:
	pipenv lock --pre
	pipenv lock -r > requirements.txt

setup:
	pipenv install --dev
	pipenv shell

tests:
	pytest -v --disable-warnings

deploy: freeze
	gcloud functions deploy covid-processing --runtime python37 --memory 256MB --entry-point run --trigger-http --allow-unauthenticated --env-vars-file .env.yaml