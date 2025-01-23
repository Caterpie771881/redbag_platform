FROM python:3.10-alpine

COPY ./src /app
COPY requeriments.txt /app/requeriments.txt

WORKDIR /app

RUN pip install -r requeriments.txt

ENTRYPOINT [ "entryproint.sh" ]
CMD [ "python", "app.py" ]