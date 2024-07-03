FROM python:3.10-slim


ENV PORT 8000
ENV PYTHONUNBUFFERED True


WORKDIR /app


COPY . /app/


RUN pip install -r requirements.txt


EXPOSE ${PORT}


CMD hypercorn src.app:asgi_app --bind 0.0.0.0:${PORT} --workers 1 --log-level debug --reload --keep-alive 75
