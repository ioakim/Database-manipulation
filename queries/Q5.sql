SELECT SHOPORDER.ORDERDATE as date, BOOK.TITLE as title, BOOK.PRICE as price, ORDERLINE.UNITSELLINGPRICE as selling_price, ORDERLINE.QUANTITY as qty, 
	ORDERLINE.UNITSELLINGPRICE*ORDERLINE.QUANTITY AS ORDER_VALUE, SHOP.NAME as shop
FROM orderline
join shoporder on shoporder.shoporderid=orderline.shoporderid
join book on orderline.bookid= book.bookid 
JOIN SHOP ON SHOPORDER.SHOPID = SHOP.SHOPID
WHERE BOOK.BOOKID= '21'  
group by shoporder.orderdate, book.bookid , ORDERLINE.UNITSELLINGPRICE , ORDERLINE.QUANTITY, SHOP.NAME 
order by shoporder.orderdate;

SELECT SUM(ORDERLINE.QUANTITY) as total_qty, SUM(ORDERLINE.QUANTITY*ORDERLINE.UNITSELLINGPRICE) as total_value FROM ORDERLINE
WHERE BOOKID='21' ;