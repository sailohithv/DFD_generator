#!C:\Python27\python.exe
import DML_Parser_main as dml_P
import cgi, os
form = cgi.FieldStorage()
print """\
Content-type:text/html\r\n\r\n
<html>"""

import sys
sys.stderr = sys.stdout

fileitem = form['filename']
db_select=form.getvalue('db_type')

message=os.path.basename(fileitem.filename)

fn = os.path.basename(fileitem.filename)
if fileitem.filename:
   open('q_uploads/dml_q_file.sql', 'wb').write(fileitem.file.read())
   message = 'Query File: '+fn+' has been uploaded successfully'
else:
   message = 'Query File: '+ fn +' uploade failed'

print """\

<body align="center">
   <form id="validate" name="validate" method="get" action="DML_Validator_ddl_validate.py" >
      <h2>Database Selected: %s</h2><br>
      <h3>%s</h3><br>
   </form> 
   """ % (db_select,message)



if __name__== "__main__":
    dml_P.dml_parser_lineage_build('dml_q_file.sql')
    print """
        <html>
                <head>
                      <script>
                      function download_file()
                      {
                         window.open('XlsFiles/lineage_flow.xlsx')
                      }
                              </script>
                          </head>   
            <body align="center">
            <input type="submit" name="download_file" value="Download" onclick="download_file()" >
        """
    # print mismatch_list
    # print ddl_tbl_dict
    # print column_names_dict
    # print dif_dict
    print """</body>
        </html>
        """