FROM python:3.10-alpine

COPY ./src /app
COPY ./entrypoint.sh /entrypoint.sh
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN chmod +x /entrypoint.sh
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "/entrypoint.sh" ]
CMD [ "python", "app.py" ]

EXPOSE 5000