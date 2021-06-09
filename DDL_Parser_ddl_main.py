#!C:\Python27\python.exe

import cgi
import cgitb
import xlwt
cgitb.enable()
import os
import sqlite3
import DDL_Parser_sqLite_parse as sq_P
import DDL_Parser_mySQL_parse as my_P
import DDL_Parser_hive_parse as h_P
import DDL_Parser_teraData_parse as td_P
import DDL_Parser_sqLite_config as sqlConf
import re
field_Data = cgi.FieldStorage()
DEFAULT=object()
class DDL_parsing:

    def get_user_selection(self, db_select=DEFAULT, d_name=DEFAULT, t_list=DEFAULT):
        if db_select is DEFAULT:
            db_select = field_Data.getvalue('select_db')

        if db_select== "mysql":
            # db_name = my_P.mysql_connection(field_Data)
            if d_name is DEFAULT:
                d_name=field_Data.getvalue('db_name')

            # tables_list=my_P.show_tables(db_name ,field_Data)
            # t_list=None
            if t_list is DEFAULT:
                t_list=field_Data.getvalue('tb_name')
                # print list(map(str, t_list.split()))
                query_list = my_P.create_table(list(map(str, t_list.split())), d_name)
            else:
                query_list=my_P.create_table(t_list,d_name)
            queries=my_P.tab_info(query_list)
            q_list=my_P.tab_split(queries)
            q_cons=my_P.add_table_constraints(q_list)
            q_len=my_P.data_length(q_cons)
            tb_list=my_P.adding_headers(q_len,d_name,t_list)
            return tb_list, db_select
        elif db_select == "teradata":
            q_list1 =td_P.get_queries()
            q_list2 = td_P.tab_clean(q_list1)
            query_dict, tables, dbnames, pk_dict = td_P.query_parsing(q_list2)
            q_list2 = td_P.tab_split(query_dict)
            q_list3 = td_P.table_constraints(q_list2, pk_dict)
            tb_list = td_P.adding_tabnames(q_list3, dbnames, tables)
            return tb_list, db_select

        elif db_select == "hadoop":
            q_l = h_P.get_queries()
            create_dict, tables = h_P.query_parsing(q_l)
            q_ll = h_P.tab_split(create_dict)
            cons_l = h_P.table_constraints(q_ll)
            tb_list = h_P.adding_tabnames(cons_l, tables)
            return tb_list, db_select

        elif db_select == "sqlite":
            dic1 = {1: sqlConf.DATABASE_CONFIG['database_name1'], 2: sqlConf.DATABASE_CONFIG['database_name2']}
            user_db=field_Data.getvalue('db_name')

            dict_tables=[]
            d_name = re.search('(.*?)\.', user_db)
            db = sqlite3.connect(user_db)
            cursor = db.cursor()
            obj1 = sq_P.DbConnection()
            user_type = field_Data.getvalue('tb_name')
            # create_table_dict=obj1.show_create_tables(cursor,obj1.show_tables(cursor,field_Data))
            create_table_dict=obj1.show_create_tables(cursor,list(map(str, user_type.split())))
            query_list_of_list = obj1.tab_split(create_table_dict)
            query_cons_list=obj1.table_constraints(query_list_of_list)
            query_len_list=obj1.data_length(query_cons_list)
            db_queries=None
            tb_list=None
            if (d_name):
                db_queries=obj1.adding_dbnames(query_len_list, d_name.group(1))
            for tables in create_table_dict:
                dict_tables.append(tables)
            tb_list=obj1.adding_tab_db_names(db_queries, dict_tables)
            return tb_list, db_select


    def excel_write(self,list_of_values,db_type):

        book = xlwt.Workbook(encoding="utf-8")
        sheet1 = book.add_sheet("Sheet 1")

        for i, l in enumerate(list_of_values):
            for j, col in enumerate(l):
                sheet1.write(i, j, col.strip('`'))
        file_name=db_type.upper()+'_out.xls'
        book.save("XlsFiles\\"+file_name)
        return file_name

if __name__== "__main__":
    out_list,db_type=DDL_parsing().get_user_selection()
    f_name=DDL_parsing().excel_write(out_list,db_type)
    print "Content-type:text/html\r\n\r\n"
    print """<Html>
                      <head>
                          <script>
                          function download_file()
                          {
                            window.open('XlsFiles/"""+f_name+"""')
                          }
                          </script>
                      </head>
    <body align="center">
    <h3> DDL dictionary has been created :"""+f_name+"""</h3>
    <input type="submit" name="download_file" value="Download" onclick="download_file()" >
             </body>
                   </html>"""
