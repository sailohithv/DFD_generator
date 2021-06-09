#!C:\Python27\python.exe

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
   open('q_uploads/q_file.sql', 'wb').write(fileitem.file.read())
   message = 'Query File: '+fn+' has been uploaded successfully'
else:
   message = 'Query File: '+ fn +' uploade failed'

print """\

<body align="center">
   <form id="validate" name="validate" method="get" action="DML_Validator_ddl_validate.py" >
      <h2>Database Selected: %s</h2><br>
      <h3>%s</h3><br>
      <input type="hidden" id="custId" name="db_select" value="%s">
      <input type="hidden" id="custId" name="filename" value="%s">
      <input type="submit" name="Fetch" value="Validate" />
   </form> 
   """% (db_select,message,db_select.lower(),fn)
   
print """</body>
</html>
 """

