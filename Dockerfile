FROM python:3.9-slim

ENV PYTHONBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update && apt-get -y install && apt-get clean

RUN pip install --upgrade pip

COPY . /app

WORKDIR /app


RUN pip3 install -r Backend/requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--reload"]