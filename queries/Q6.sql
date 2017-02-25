﻿SELECT SALESREP.SALESREPID as salerep_id, COALESCE(SUM(ORDERLINE.QUANTITY),0) AS total_sales, 
	COALESCE(SUM(ORDERLINE.QUANTITY*ORDERLINE.UNITSELLINGPRICE),0) AS total_value
FROM SalesRep
left JOIN ShopOrder ON SHOPORDER.SALESREPID = SALESREP.SALESREPID 
left JOIN ORDERLINE ON ORDERLINE.SHOPORDERID = SHOPORDER.SHOPORDERID
and SHOPORDER.ORDERDATE BETWEEN '2010-12-02' AND '2016-12-02'
GROUP BY SALESREP.SALESREPID
ORDER BY total_value desc
