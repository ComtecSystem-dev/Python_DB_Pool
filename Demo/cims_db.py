# -*- coding: utf-8 -*-
################################################################################
#        _____                _                                                #
#       / ____               | |                                               #
#      | |     ___  _ __ ____| |__ ___  ___                                    #
#      | |    / _ \/ '_ ` _ \_  __/ _ \/ __/                                   #
#      | |___| (_) | | | | | | |_| /__/ (_                                     #
#       \_____\___/|_| |_| |_/\___\___|\___\                                   #
#                                 _____           _                            #
#                                / ____|         | |                           #
#                               | (___  _   _ ___| |_ ___ _ __ ___  ___        #
#                                \___ \| | | / __| __/ _ \ '_ ` _ \/ __|       #
#                                ____) | |_| \__ \ ||  __/ | | | | \__ \       #
#                               |_____/ \__, |___/\__\___|_| |_| |_|___/       #
#                                        __/ |                                 #
#                                       |___/                                  #
#                                                                              #
################################################################################
#                                                                              #
# Copyright (c) 2018 Comtec Systems                                            #
# All Rights Reserved.                                                         #
#                                                                              #
# Licensed under the Apache License, Version 2.0 (the "License"); you may      #
# not use this file except in compliance with the License. You may obtain      #
# a copy of the License at                                                     #
#                                                                              #
# http://www.apache.org/licenses/LICENSE-2.0                                   #
#                                                                              #
# Unless required by applicable law or agreed to in writing, software          #
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT #
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the  #
#    License for the specific language governing permissions and limitations   #
#    under the License.                                                        #
#                                                                              #
################################################################################
import psycopg2
from psycopg2 import pool

class DBManager(object):
    
    def __init__(self):
        self.ip = '127.0.0.1'
        self.port = '5432'
        self.dbname = ''
        self.user_id = ''
        self.user_pw = ''
        self.conn = None
        pass
    
    def print_dbinfo(self):
        print "[IP=%s][PORT=%s][DB Name=%s][User ID=%s][User PW=%s]" % (self.ip, self.port, self.dbname, self.user_id, self.user_pw)
        
    def Connect(self, ip, port, dbname, user_id, user_pw):
        self.ip = ip
        self.port = port
        self.dbname = dbname
        self.user_id = user_id
        self.user_pw = user_pw
        self.print_dbinfo()
        #self.conn = psycopg2.connect("host='%s' port='%s' dbname='%s' user='%s' password='%s'" % (self.ip, self.port, self.dbname, self.user_id, self.user_pw))
        self.conn= psycopg2.pool.ThreadedConnectionPool(1
                                                      , 20
                                                      , user = user_id
                                                      , password = user_pw
                                                      , host = ip
                                                      , port = port
                                                      , database = dbname)
        
        if self.conn is None:
            return False
        return True
        
    def Get_Conn(self):
        if self.conn is None:
            return None
        return self.conn.getconn()
    
    def Put_Conn(self, conn):
        if self.conn is None:
            return None
        self.conn.putconn(conn)
    
    def Select(self, strQuery):
        #print strQuery
        # Init
        conn = self.Get_Conn()
        if conn is None:return None
        cursor = conn.cursor()
        #cursor = self.conn.cursor()
        # Query 실행
        try:
            cursor.execute(strQuery)
        except psycopg2.IntegrityError :
            conn.rollback()
            print "(Select) psycopg2.IntegrityError"
        except Exception as e:
            conn.rollback()
            cursor.close()
            print "(Select) Exception : %s" % (e)
            
        self.Put_Conn(conn);
        return cursor
    
    def Execute(self, strQuery):
        return_state = None
        #print "(Query Execute) %s " % strQuery
        # Init
        conn = self.Get_Conn()
        if conn is None:return None
        cursor = conn.cursor()
        #cursor = self.conn.cursor()
        # Query 실행
        try :
            cursor.execute(strQuery)
            conn.commit()
            return_state = True
            
        except psycopg2.IntegrityError :
            conn.rollback()
            return_state = False
            print "(Execute) psycopg2.IntegrityError"

        except Exception as e:
            conn.rollback()
            return_state = False
            print "(Execute) Exception : %s" % (e)
        
        self.Put_Conn(conn);
        cursor.close()
        
        return return_state
    
    def Execute_List(self, list_query):
        return_state = True
        # Init
        conn = self.Get_Conn()
        if conn is None:return None
        cursor = conn.cursor()
        #cursor = self.conn.cursor()
        for strQuery in list_query:
            #print "(Query Execute) %s " % strQuery
            # Query 실행
            try :
                cursor.execute(strQuery)
            except psycopg2.IntegrityError :
                print "(Execute_List) psycopg2.IntegrityError"
                return_state = False;
                break;
            except Exception as e:
                print "(Execute_List) Exception : %s" % (e)
                return_state = False;
                break;
        if return_state == None or return_state==False:
            conn.rollback()
        else:
            conn.commit()
        cursor.close()
        self.Put_Conn(conn);
        return return_state
        
dbmanager = DBManager()