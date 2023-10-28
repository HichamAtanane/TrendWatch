FROM python:3.11.6

WORKDIR /usr/code/trendwatch

COPY ./requirements.txt .

RUN python3 -m pip install --no-cache-dir --upgrade -r ./requirements.txt

COPY . /usr/code/trendwatch

CMD tail -f /dev/null

