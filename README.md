## What is this?
This is the DB pool session available in the python 3.6.
This improves the efficiency of source code when querying by multiple access to DB.

## What is support db.
This suppoer is Postgresql.
To use it, you need to install "psycopg2".

## Used to
you should get sample code in "demo" directory

#### Connection example
	from cims_db import db_manager
	conn_state = dbmanager.Connect('<HOST_IP>', '<HOST_PORT>', '<DB_NAME>', '<ID>', '<PW>')
	if conn_state == True:
		print ("Connection is OK")
	else:
		print ("Connection is Failed")

#### Select example
	try:
		cursor = dbmanager.Select("select * from <table>")
		if cursor is not None:
			result = cursor.fotchone()
			cursor.close()
	except Exception as e:
		print e

#### Execute("DELETE, UPDATE") example
	try:
		result = dbmanager.Execute("INSERT INTO <TABLE>(VALUES....) VALUE(VAL1, VAL2)")
		if result is not None:
			print "Execute is OK"
	except Exception as e:
		print e
	
	
#### Execute is Multi("DELETE, UPDATE") example
	# If one query fails, the result is None.
	query_list = []
	query_list.append("INSERT INTO <TABLE>(VALUES....) VALUE(VAL1, VAL2)")
	query_list.append("INSERT INTO <TABLE>(VALUES....) VALUE(VAL1, VAL2)")
	query_list.append("INSERT INTO <TABLE>(VALUES....) VALUE(VAL1, VAL2)")
	query_list.append("INSERT INTO <TABLE>(VALUES....) VALUE(VAL1, VAL2)")
	
	try:
		result = dbmanager.Execute_List(query_list)
		if result is not None:
			print "Execute_List is OK"
	except Exception as e:
		print e

## License
This project is licensed under the Apache License 2.0 - see the LICENSE.md file for details.
