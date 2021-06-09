#!C:\Python27\python.exe

import DDL_Parser_mySQL_config as Conf
import mysql.connector

def get_db_names():
    temp_dbs = []
    db = mysql.connector.connect(host=Conf.DATABASE_CONFIG['host'], user=Conf.DATABASE_CONFIG['user'],
                                 password=Conf.DATABASE_CONFIG['password'])
    cursor = db.cursor()
    query_db = "show databases;"
    cursor.execute(query_db)
    res = cursor.fetchall()
    for i in res:
        temp_dbs.append(list(i))

    db_names = [item.encode('utf-8') for sublist in temp_dbs for item in sublist]
    return db_names

def get_table_names():
    db = mysql.connector.connect(host='localhost',user='root', password='root' ,database='hotel_db')
    cursor = db.cursor()
    sql = 'show tables'
    cursor.execute(sql)
    list_tested = cursor.fetchall()
    list_tested = [i.encode('utf-8') for sub in list_tested for i in sub]
    return list_tested

def print_dropdown(db_names,tb_names):  # Print the dropdown
    print "Content-type:text/html\r\n\r\n"
    print '''
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">   
    <html xmlns="http://www.w3.org/1999/xhtml">
    <head>
    <script language="javascript" type="text/javascript">    '''
    print '''
             function listboxchange1(p_index) 
             {
                                    
                 document.form1.db_name.options.length = 0;
                 document.form1.tb_name.options.length = 0;
                 document.form1.tb_name.options[0] = new Option("Select tb_name", "");
              '''
    print '''
                 switch (p_index) 
                 {
                 
                 case "mysql":
           '''
    for i in range(0, len(db_names)):
                print 'document.form1.db_name.options[%s]=new Option("%s", "%s");'%(i, db_names[i], db_names[i])
    print '''
                break;
                
                case "sqlite":

 document.form1.db_name.options[0] = new Option("Select db_name", "");

 document.form1.db_name.options[1] = new Option("studentdb.db", "studentdb.db");

 document.form1.db_name.options[2] = new Option("employeedb.db", "employeedb.db");

 break;

 case "hadoop":

 document.form1.db_name.options[0] = new Option("Select db_name", "");

 document.form1.db_name.options[1] = new Option("hadoopdb", "hadoopdb");

 break;

 case "teradata":

 document.form1.db_name.options[0] = new Option("Select db_name", "");

 document.form1.db_name.options[1] = new Option("teradatadb", "teradatadb");

 break;

                }
                
                return true;
            }
            
            function listboxchange2(p_index) 
            {
                 document.form1.tb_name.options.length = 0;
                
                 switch (p_index) 
                 {
                
                 case "empoloyee_dept_db":
                
                 document.form1.tb_name.options[0] = new Option("Select tb_name", "");
                
                 document.form1.tb_name.options[1] = new Option("all tables", "all tables");
                
                 document.form1.tb_name.options[2] = new Option("auth_group", "auth_group");
                
                 document.form1.tb_name.options[3] = new Option("auth_group_permissions", "auth_group_permissions");
                
                 document.form1.tb_name.options[4] = new Option("dept", "dept");
                
                 document.form1.tb_name.options[5] = new Option("django_admin_log", "django_admin_log");
                
                 break;
                
                 case "employees":
                
                 document.form1.tb_name.options[0] = new Option("Select tb_name", "");
                
                 document.form1.tb_name.options[1] = new Option("all tables", "all tables");
                
                 document.form1.tb_name.options[2] = new Option("departments", "departments");
                
                 document.form1.tb_name.options[3] = new Option("dept_emp", "dept_emp");
                
                 document.form1.tb_name.options[4] = new Option("dept_manager", "dept_manager");
                
                 break;
                
                 case "hotel_db":
                
                 document.form1.tb_name.options[0] = new Option("Select tb_name", "");
                
                 document.form1.tb_name.options[1] = new Option("booking", "booking");
                
                 document.form1.tb_name.options[2] = new Option("guest", "guest");
                
                 document.form1.tb_name.options[3] = new Option("hotel", "hotel");
                
                 break;
                
                 case "studentdb.db":
                 document.form1.tb_name.options[0] = new Option("Select tb_name", "");
                
                 document.form1.tb_name.options[1] = new Option("all tables", "all tables");
                
                 document.form1.tb_name.options[2] = new Option("student", "student");
                
                 document.form1.tb_name.options[3] = new Option("marks", "marks");
                
                 document.form1.tb_name.options[4] = new Option("contacts", "contacts");
                
                 break;
                
                 case "employeedb.db":
                
                 document.form1.tb_name.options[0] = new Option("Select tb_name", "");
                
                 document.form1.tb_name.options[1] = new Option("all tables", "all tables");
                
                 document.form1.tb_name.options[2] = new Option("employee", "employee");
                
                 document.form1.tb_name.options[3] = new Option("manager", "manager");
                
                 break;
                
                 case "hadoopdb":
                
                 document.form1.tb_name.options[0] = new Option("Select tb_name", "");
                
                 document.form1.tb_name.options[1] = new Option("all tables", "all tables");
                
                 break;
                
                 case "teradatadb":
                
                 document.form1.tb_name.options[0] = new Option("Select tb_name", "");
                
                 document.form1.tb_name.options[1] = new Option("all tables", "all tables");
                
                 break;
                 
                 case "ccwd":
                 

                
                document.form1.tb_name.options[0] = new Option("Select tb_name", "");
                
                document.form1.tb_name.options[1] = new Option("all tables", "all tables");
                
                document.form1.tb_name.options[2] = new Option("suppliers", "suppliers");
                
                document.form1.tb_name.options[3] = new Option("manager", "manager");
                
                document.form1.tb_name.options[4] = new Option("courses", "courses");
                 
                document.form1.tb_name.options[5] = new Option("results", "results");
                 
                document.form1.tb_name.options[6] = new Option("physician", "physician");
                 
                
                 break;
                 
                }
            
            return true;
            
            }

    </script>
    </head>
    <body>
        <form id="form1" name="form1" method="post" action="DDL_Parser_ddl_main.py" >
        <table width="50%" border="1" align="center" cellpadding="2" cellspacing="0">

        <tr>
         <td width="21%" align="right" valign="middle">
         <strong>Database Type :</strong>
         </td>
         <td width="79%" align="left" valign="middle">
        
        <select name="select_db" id="category" onchange="javascript: listboxchange1(this.options[this.selectedIndex].value);">
        
         <option value="">Select Category</option>
         <option value="sqlite">SQLite</option>
         <option value="mysql">MySQL</option>
         <option value="hadoop">Hadoop</option>
         <option value="teradata">Teradata</option>
         </select>
         </td>
         </tr>
         
         
     <tr>
     <td align="right" valign="middle">
     <strong>Database Name:</strong>
     </td>
     <td align="left" valign="middle">
     <script type="text/javascript" language="javascript">
     <!--
     document.write('<select name="db_name" onChange="javascript: listboxchange2(this.options[this.selectedIndex].value);"><option value="">Select database name</option></select>')
     -->
     </script>
     </td>
     </tr>
    <tr>
    <td align="right" valign="middle">
    <strong>Select Tables :</strong>
    </td>
    <td align="left" valign="middle">
    <script type="text/javascript" language="javascript">
    <!--
    document.write('<select name="tb_name"><option value="">Select tables</option></select>')   
    -->
    </script>
    </td>
    </tr>
    <tr>
    
    <center><td ><input type="submit" name="Fetch" value="Submit" /></td></center>
    </tr>
     </table>
     </form>'''


    print """</Body>
    </html>"""


if __name__== "__main__":
    dbs=get_db_names()
    tbs=get_table_names()
    # print li
    print_dropdown(dbs,tbs)
