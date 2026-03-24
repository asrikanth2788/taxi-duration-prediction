FROM python:3.9.6

workdir app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 9696

CMD [ "gunicorn", "-b 0.0.0.0:9696", "predict:app" ]