SELECT 	BOOK.BOOKID as book_id, book.title as title, SUM(ORDERLINE.QUANTITY) as total_qty,SUM(ORDERLINE.UNITSELLINGPRICE)*SUM(ORDERLINE.QUANTITY) 
	as totalsellingprice,SUM(book.price)*SUM(ORDERLINE.QUANTITY) as totaloriginalgprice ,extract(year from orderdate) as year, 
	extract (month from orderdate) as month, count(orderline.shoporderid) as total_orders
FROM orderline
join shoporder on shoporder.shoporderid=orderline.shoporderid
join book on orderline.bookid= book.bookid 
join publisher on publisher.publisherid= book.publisherid
WHERE publisher.name = 'PB1'  
group by book.bookid, month, year order by month,year