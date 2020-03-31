FROM python:3.7.5-alpine3.9
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app .

CMD [ "python", "main.py" ]