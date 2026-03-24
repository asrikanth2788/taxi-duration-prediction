FROM python:3.9-slim

workdir /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN useradd --create-home appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 9696

CMD [ "gunicorn", "-b 0.0.0.0:9696", "predict:app" ]