from cims_db import dbmanager
import copy

dbmanager.Connect('<HOST_IP>', '<HOST_PORT>', '<DB_NAME>', '<ID>', '<PW>')

return_result = None
try :
	query = "SELECT * FROM <TABLE>"
	cursor = dbmanager.Select(query)
	if cursor is not None:
		result = cursor.fetchone()
		return_result = copy.deepcopy(result)
		cursor.close()
except Exception as e:
	print e

print return_result
