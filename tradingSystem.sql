create database masy;

DROP TABLE IF EXISTS user_coin_account;
CREATE TABLE user_coin_account (
    user_id        integer,
    coin    VARCHAR(45),
    number  integer,
  vwp   integer,
  
    PRIMARY KEY ( user_id,coin,number,vwp)
);


DROP TABLE IF EXISTS blotter;
CREATE TABLE blotter (
    real_time         timestamp,
    coin             varchar(3),
    quantity    double,
    price  double,
    buy_sell     varchar(4),
    PRIMARY KEY ( real_time,coin)
);

DROP TABLE IF EXISTS pnl;
CREATE TABLE pnl (
    user_id        integer,
    coin    VARCHAR(45),
    realized_pnl     VARCHAR(45),
    unrealized_pnl   VARCHAR(45),
    timestamp            VARCHAR(45),
  
    PRIMARY KEY ( user_id,coin,timestamp)
  
);

DROP TABLE IF EXISTS marketplace;
CREATE TABLE marketplace (
  symbol VARCHAR(25),
   real_time  timestamp,
    open_pr DOUBLE ,
    high_pr DOUBLE,
low_pr  DOUBLE,
close_pr  DOUBLE,
volume DOUBLE,
PRIMARY KEY(symbol,real_time)
);

DROP TABLE IF EXISTS users;
CREATE TABLE users (
    user_pk         INTEGER AUTO_INCREMENT NOT NULL,
    full_name            VARCHAR(255),
    email           VARCHAR(255),
    pwd        VARCHAR(255),
    cash_availble   INTEGER,
    PRIMARY KEY ( user_pk )
);

INSERT INTO users(full_name,email,pwd,cash_availble) values('Bill Gates','billgate@microsoft.com','123456','100000');

DROP TABLE IF EXISTS ordertype;
create table ordertype(
   side_pk INTEGER,
   side VARCHAR(25),
   primary key(SIDE_PK)
   );
   
insert INTO ordertype(side_pk,side) values ('1','buy');
insert INTO ordertype(side_pk,side) values ('2','sell')

