FROM python:alpine

RUN apk update && apk upgrade && \
    apk add --no-cache git

WORKDIR /Users/erili/Desktop/trading-system

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN git clone https://github.com/Ellyisme/trading-system /Users/erili/Desktop/trading-system
EXPOSE 5000
CMD [ "python", "/Users/erili/Desktop/trading-system/BTC.py" ]
CMD [ "python", "/Users/erili/Desktop/trading-system/ETH.py" ]
CMD [ "python", "/Users/erili/Desktop/trading-system/LTC.py" ]
CMD [ "python", "/Users/erili/Desktop/trading-system/main.py" ]


