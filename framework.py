from datetime import datetime
import psycopg2, psycopg2.extras
from flask import Flask, render_template, request

app = Flask(__name__)
  
def getConn():
    #function to retrieve the password, construct
    #the connection string, make a connection and return it.
    pwFile = open("pw.txt", "r")
    pw = pwFile.read();
    pwFile.close()
    connStr = "host='localhost' \
               dbname= 'coursework' user='postgres' password = " +pw
    conn=psycopg2.connect(connStr)          
    return  conn
	
@app.route('/')
def home():
	return render_template('homepage.html')

@app.route('/addCategory', methods =['POST'])
def addCategory():
	try:
		conn=None
		conn=getConn()
		cur = conn.cursor()
		cur.execute('SET search_path to public')
		
		newCategoryID = request.form['categoryID']
		newname = request.form['name']
		newtype = request.form['categorytype']
		
		cur.execute('INSERT INTO category(CategoryID, Name, CategoryType)\
					VALUES (%s, %s, %s)',[newCategoryID, newname, newtype])
		
		conn.commit()
		
	except Exception as e:
		return render_template('homepage.html', msg1='Category did not create', error=e)
	finally:
		if conn:
			conn.close()
	return render_template('homepage.html', msg1='Category succesfully created')
	
@app.route('/deleteCategory', methods =['POST'])
def removeCategory():
	try:
		conn=None
		conn=getConn()
		cur = conn.cursor()
		cur.execute('SET search_path to public')
		
		newCategoryID = request.form['categoryID']
		
		cur.execute('SELECT * FROM CATEGORY WHERE CATEGORYID=%s',[newCategoryID])
		category=cur.fetchall()
		if (len(category) ==0):
			raise Exception('There is no category with this ID')
			
		cur.execute('DELETE FROM Category WHERE CategoryID = %s', [newCategoryID])
		
		conn.commit()
		       
	except Exception as e:
		return render_template('homepage.html', msg1='Category did not delete', error=e)
	finally:
		if conn:
			conn.close()
	return render_template('homepage.html', msg1='Category succesfully deleted')
	
@app.route('/booksAvailable', methods =['GET'])
def availabilityReport():
	try:
		conn=None
		conn=getConn()
		cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
		cur.execute('SET search_path to public')
		
		cur.execute('SELECT NAME as categ_name,COUNT(TITLE)as book_count, round(avg(price), 2)\
					as avg_price FROM BOOK FULL JOIN CATEGORY ON CATEGORY.CATEGORYID = \
					BOOK.CATEGORYID GROUP BY CATEGORY.CATEGORYID ORDER BY CATEGORY.CATEGORYID')
		books=cur.fetchall()
		
		cur.execute('SELECT DISTINCT(SELECT COUNT(CATEGORY.CATEGORYID) as categ_count FROM CATEGORY),\
					COUNT(BOOK.TITLE) as book_count, SUM(BOOK.PRICE) as price_sum FROM BOOK')
		totals=cur.fetchall()
		 
	except Exception as e:
		return render_template('homepage.html', msg1='Report not created', error=e)
	finally:
		if conn:
			conn.close()
	return render_template('results.html', books=books, totals=totals)

@app.route('/reportPublisher', methods =['GET'])
def publisherReport():
	try:
		conn=None
		conn=getConn()
		cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
		cur.execute('SET search_path to public')
		
		newPublisherName = request.args.get('publishername')
		
		cur.execute('SELECT 	BOOK.BOOKID as book_id, book.title as title, SUM(ORDERLINE.QUANTITY) as total_qty,\
								SUM(ORDERLINE.UNITSELLINGPRICE)*SUM(ORDERLINE.QUANTITY) \
								as totalsellingprice,SUM(book.price)*SUM(ORDERLINE.QUANTITY)\
								as totaloriginalprice ,extract(year from orderdate) as year,\
								extract (month from orderdate) as month, count(orderline.shoporderid)\
								as total_orders\
					FROM orderline\
						 join shoporder on shoporder.shoporderid=orderline.shoporderid\
						 join book on orderline.bookid= book.bookid \
						 join publisher on publisher.publisherid= book.publisherid\
					WHERE publisher.name = %s  \
					group by book.bookid, month, year \
					order by month,year',[newPublisherName])
		
		publisher=cur.fetchall()
		   
	except Exception as e:
		return render_template('homepage.html', msg1='Report not created', error=e)
	finally:
		if conn:
			conn.close()
	return render_template('results.html', publisher=publisher)

@app.route('/reportBook', methods =['GET'])
def bookReport():
	try:
		conn=None
		conn=getConn()
		cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
		cur.execute('SET search_path to public')
		
		newBookID = request.args.get('bookID')
		
		cur.execute('SELECT SHOPORDER.ORDERDATE as date, BOOK.TITLE as title, BOOK.PRICE as price,\
					 ORDERLINE.UNITSELLINGPRICE as selling_price, ORDERLINE.QUANTITY as qty,\
					 ORDERLINE.UNITSELLINGPRICE*ORDERLINE.QUANTITY AS ORDER_VALUE, SHOP.NAME as shop\
					 FROM orderline\
					 join shoporder on shoporder.shoporderid=orderline.shoporderid\
					 join book on orderline.bookid= book.bookid \
					 JOIN SHOP ON SHOPORDER.SHOPID = SHOP.SHOPID\
					 WHERE BOOK.BOOKID= %s\
					 group by shoporder.orderdate, book.bookid , ORDERLINE.UNITSELLINGPRICE ,\
							 ORDERLINE.QUANTITY, SHOP.NAME \
					 order by shoporder.orderdate',[newBookID])
		
		history =cur.fetchall()
		
		cur.execute('SELECT SUM(ORDERLINE.QUANTITY) as total_qty,\
					SUM(ORDERLINE.QUANTITY*ORDERLINE.UNITSELLINGPRICE) as total_value\
					FROM ORDERLINE\
					WHERE BOOKID=%s',[newBookID])
		
		totals = cur.fetchall()
		   
	except Exception as e:
		return render_template('homepage.html', msg1='Report not created', error=e)
	finally:
		if conn:
			conn.close()
	return render_template('results.html', history = history, totals = totals)

@app.route('/salesRepPerformance', methods =['GET'])
def salesRepReport():
	try:
		conn=None
		conn=getConn()
		cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
		cur.execute('SET search_path to public')
		
		StartDate = request.args.get('start')
		EndDate = request.args.get('end')
		
		newStartDate = datetime.strptime(StartDate, "%Y-%m-%d").date()
		newEndDate = datetime.strptime(EndDate, "%Y-%m-%d").date()
		
		cur.execute('SELECT SALESREP.SALESREPID as salesrep_id, COALESCE(SUM(ORDERLINE.QUANTITY),0) AS total_sales,\
					 COALESCE(SUM(ORDERLINE.QUANTITY*ORDERLINE.UNITSELLINGPRICE),0) AS total_value\
					 FROM SalesRep\
					 left JOIN ShopOrder ON SHOPORDER.SALESREPID = SALESREP.SALESREPID\
					 left JOIN ORDERLINE ON ORDERLINE.SHOPORDERID=SHOPORDER.SHOPORDERID\
					 AND SHOPORDER.ORDERDATE BETWEEN %s AND %s\
					 GROUP BY SALESREP.SALESREPID\
					 ORDER BY TOTAL_VALUE desc',[newStartDate, newEndDate])
		
		performance =cur.fetchall()
	except Exception as e:
		return render_template('homepage.html', msg1='Report not created', error=e)
	finally:
		if conn:
			conn.close()
	return render_template('results.html', performance=performance)

@app.route('/discountCategory', methods =['POST'])
def applyDiscount():
	try:
		conn=None
		conn=getConn()
		cur = conn.cursor()
		cur.execute('SET search_path to public')
		
		newCategoryID = request.form['categoryID']
		discount= request.form['discount']
		newDiscount= float(float(discount)/100)
		
		cur.execute('SELECT * FROM CATEGORY WHERE CATEGORYID=%s',[newCategoryID])
		test=cur.fetchall()
		if (len(test) ==0):
			raise Exception('There is no category with this ID')
		
		cur.execute('Select price from book where categoryID=%s', [newCategoryID])
		books=cur.fetchall()
		
		for bookprice in books:
			bookprice=float(bookprice[0])
			newprice=bookprice-(bookprice*newDiscount)
		
		cur.execute('UPDATE Book SET Price=%s WHERE Book.CategoryID =%s', [newprice, newCategoryID])
		
		conn.commit()
		      
	except Exception as e:
		return render_template('homepage.html', msg1='Discount not applied', error=e)
	finally:
		if conn:
			conn.close()
	return render_template('homepage.html', msg1='Discount applied') 

if __name__ == "__main__":
    app.run(debug = True)