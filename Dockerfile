FROM python:alpine3.7

COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV DOJO_TOKEN="113h5gk24j5h2k4j5h2k4j5
ENV DOJO_BASE_URL=https://dojo.site.com 

CMD [ "python", "closer.py" ]
