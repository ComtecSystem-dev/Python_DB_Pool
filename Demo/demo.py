from cims_db import dbmanager
import copy

dbmanager.Connect('10.201.5.101', '5432', 'cims', 'comtec', 'comtec')

ip_info = None
try :
	query = "SELECT IP_SEQ, "\
			"        GROUP_SEQ, "\
			"        IP_ADDR, "\
			"        IP_DESC, "\
			"        ip_assign_flag, "\
			"        ip_assign_user_id, "\
			"        ip_assign_time, "\
			"        IP_ACTIVE_FLAG, "\
			"        IP_ACTIVE_TIME, "\
			"        IP_ACTIVE_CLOSE_TIME "\
			"FROM TB_D_IP "\
			"WHERE IP_SEQ = %s" % ('46')
	cursor = dbmanager.Select(query)
	if cursor is not None:
		result = cursor.fetchone()
		ip_info = copy.deepcopy(result)
		cursor.close()
except Exception as e:
	print e

print ip_info