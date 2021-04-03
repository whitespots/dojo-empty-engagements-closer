FROM python:alpine3.7
LABEL MANTAINER="whitespots.io"

COPY requirements.txt .
RUN pip install --upgrade pip && \
  pip install -r requirements.txt
COPY . .

CMD [ "python", "closer.py" ]
