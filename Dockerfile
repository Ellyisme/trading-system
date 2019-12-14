FROM python:alpine

RUN apk update && apk upgrade && \
    apk add --no-cache git

WORKDIR /Users/erili/PycharmProjects/trading

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN git clone https://github.com/Ellyisme/trading-system /Users/erili/PycharmProjects/trading
EXPOSE 5000
CMD [ "python", "/Users/erili/PycharmProjects/trading/BTC.py" ]
CMD [ "python", "/Users/erili/PycharmProjects/trading/ETH.py" ]
CMD [ "python", "/Users/erili/PycharmProjects/trading/LTC.py" ]
CMD [ "python", "/Users/erili/PycharmProjects/trading/main.py" ]


