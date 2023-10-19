FROM python:3.11.6

WORKDIR /usr/code/trendwatch

COPY . .

RUN python3 -m pip install -r requirements.txt --no-cache-dir

CMD tail -f /dev/null

