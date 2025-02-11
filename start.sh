source venv/bin/activate

gunicorn server:app -b 127.0.0.1:8050 -w 8