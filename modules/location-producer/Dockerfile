FROM arm64v8/python:3.10-alpine3.17

ENV PYTHONUNBUFFERED 1

WORKDIR .

RUN apk add --no-cache gcc g++ musl-dev linux-headers geos libc-dev postgresql-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5005

COPY . .
CMD ["python", "main.py"]