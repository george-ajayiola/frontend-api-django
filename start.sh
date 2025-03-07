#!/bin/sh

# Run consumer.py in the background
python consumer.py &

# Start the Django server using Gunicorn
gunicorn --bind 0.0.0.0:8000 frontend.wsgi:application