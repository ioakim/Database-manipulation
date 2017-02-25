﻿CREATE TABLE Category
(
CategoryID INTEGER PRIMARY KEY,
Name VARCHAR(50),
CategoryType VARCHAR(20) CHECK(VALUE IN('fiction','Non-fiction'));

CREATE TABLE SalesRep
(
SalesRepID INTEGER PRIMARY KEY,
Name VARCHAR(50)
);
CREATE TABLE Shop
(
ShopID INTEGER PRIMARY KEY,
Name VARCHAR(50)
);
CREATE TABLE Publisher
(
PublisherID INTEGER PRIMARY KEY,
Name VARCHAR(50)
);
CREATE TABLE Book
(
BookID INTEGER PRIMARY KEY,
Title VARCHAR(50),
Price DECIMAL(10,2),
CategoryID INTEGER,
PublisherID INTEGER
);
CREATE TABLE ShopOrder
(
ShopOrderID INTEGER PRIMARY KEY,
OrderDate DATE,
ShopID INTEGER,
SalesRepID INTEGER
);
CREATE TABLE Orderline
(
ShopOrderID INTEGER,
BookID INTEGER,
Quantity INTEGER,
UnitSellingPrice DECIMAL (10,2)
);