FROM python:3.11-slim-buster

RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    apt clean && \
    rm -rf /var/cache/apt/* && \
    apt-get install dos2unix

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=utf-8

COPY ./requirements/ /tmp/requirements

RUN pip install -U pip && \
    pip install --no-cache-dir -r /tmp/requirements/dev.txt

COPY . .

# Add wait-for-it.sh
COPY compose/local/wait-for-it.sh /wait-for-it.sh
COPY compose/local/run_app.sh /run_app.sh
RUN chmod +x /wait-for-it.sh
RUN chmod +x /run_app.sh
RUN dos2unix /run_app.sh
RUN dos2unix /wait-for-it.sh


# Run Django management commands and then start the server
CMD ["/run_app.sh"]