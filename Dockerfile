FROM python:3.9.20-alpine3.20

COPY ./src /app
COPY ./entrypoint.sh /entrypoint.sh
COPY ./requeriments.txt /app/requeriments.txt

WORKDIR /app

RUN chmod +x /entrypoint.sh
RUN pip install --no-cache-dir -r requeriments.txt

ENTRYPOINT [ "/entryproint.sh" ]
CMD [ "python", "app.py" ]

EXPOSE 5000