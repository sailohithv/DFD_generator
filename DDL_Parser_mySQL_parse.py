import mysql.connector
import re
import DDL_Parser_mySQL_config as Conf



# def mysql_connection(field_Data):
#     databases = []
#     encoded_dames = []
#     db = mysql.connector.connect(host=Conf.DATABASE_CONFIG['host'],user=Conf.DATABASE_CONFIG['user'], password=Conf.DATABASE_CONFIG['password'])
#     cursor = db.cursor()
#     query_db = "show databases;"
#     cursor.execute(query_db)
#     res = cursor.fetchall()
#
#     for i in res:
#         databases.append(list(i))
#
#     flat_db = [item for sublist in databases for item in sublist]
#
#     for i in flat_db:
#         encoded_dames.append(i.encode('utf-8'))
#     db_inp = field_Data.getvalue('db_name')
#     # db_inp="hotel_db"
#     return db_inp

def show_tables(db_name,field_Data):
    # print field_Data
    tables = []
    encoded_tames = []
    conn = mysql.connector.connect(host=Conf.DATABASE_CONFIG['host'], database=db_name,
                                   user=Conf.DATABASE_CONFIG['user'],
                                   password=Conf.DATABASE_CONFIG['password'])
    cur = conn.cursor()
    query_tb = "show tables;"
    cur.execute(query_tb)
    res = cur.fetchall()

    for i in res:
        tables.append(list(i))

    flat_db = [item for sublist in tables for item in sublist]

    for i in flat_db:
        encoded_tames.append(i.encode('utf-8'))

    dic2 = {1: "all the tables", 2: "selected table/tables"}
    # print dic2
    # user_choice = input("enter the choice to be done:")
    user_tb_choice=field_Data.getvalue('tb_name')
    # user_tb_choice="guest"
    # print user_choice
    if user_tb_choice == "all tables":
        return encoded_tames
    else:
        # print encoded_tames
        user_tables = list(map(str, user_tb_choice.split()))
        return user_tables

def create_table(table_names, db_name):
    query_list=[]
    conn = mysql.connector.connect(host=Conf.DATABASE_CONFIG['host'], database=db_name,
                                   user=Conf.DATABASE_CONFIG['user'],
                                   password=Conf.DATABASE_CONFIG['password'])
    cursor = conn.cursor()
    for table in table_names:
        cursor.execute("show create table " + table + ";")
        res=cursor.fetchall()
        queries = [item for sublist in res for item in sublist]
        queries_final = []
        for i in queries:
            queries_final.append(i)
        query_list.append(queries_final)

    return query_list

def tab_info(query_list):
    q_list = []
    for queries in query_list:
        li1=queries[1].split('\n')
        str1 = ''.join(li1)
        str1 = re.sub("\s\s+", "", str1)
        str1 = str1.lower()
        q_list.append(str1)
    return q_list

def tab_split(queries):
    q_list=[]
    for q in queries:
        spos = q.find('(')
        table_names = []
        table_name = re.findall('table (.+?)\(', q)
        for i in table_name:
            table_names.append(i.encode('utf-8'))
        q = q.replace(q[spos], '|', 1)
        rev = q[::-1]
        rev = rev.replace(')', '|', 1)
        q = rev[::-1]
        a = q.split('|')
        out = a[1].split(',')
        q_list.append(out)
    return q_list

def add_table_constraints(q_list):
    constraints = ['unique key', 'primary key', 'foreign key']
    cons_list=[]
    for out in q_list:
        col_names = []
        dictionary = {}
        flat_col_names = []
        cons_name = []
        for j in out:
            for i in constraints:
                if i in j:
                    cons_name.append(i)
                    col_name = re.findall('\((.*?)\)', j)
                    col_names.append(col_name)
                    flat_col_names = [item for sublist in col_names for item in sublist]
        dictionary = dict(zip(flat_col_names, cons_name))

        list1 = []
        for i in out:
            list1.append(i.encode('utf-8'))

        indices = []
        for i in list1:
            if re.search('\(\`([a-zA-Z].*?)\`\)', i):
                indices.append(list1.index(i))
        for _ in indices:
            list1.pop()

        output = []
        for i in list1:
            output.append(i.split(" ", 2))

        for i in output:
            for key in dictionary:
                if key in i:
                    i.append(dictionary[key])
        cons_list.append(output)

    return cons_list

def data_length(cons_list):
    q_len=[]
    for output in cons_list:
        column_len = []
        for i in output:
            braces = re.search(r'\((.*?)\)', i[1])
            if braces:
                column_len.append(braces.group(1))
            else:
                column_len.append('NULL')
        for idx, val in enumerate(column_len):
            if val == "NULL":
                continue
            else:
                output[idx].insert(2, val)
        for i in output:
            x = re.search(r'\((.*?)\)', i[1])
            if x:
                i[1] = i[1].replace(x.group(0), "")
            else:
                i[1] = i[1]

        for i, l in enumerate(output):
            for j, col in enumerate(l):
                if j > 3:
                    output[i][j - 1] = output[i][j - 1] + ' ' + output[i][j]
                    output[i].remove(output[i][j])
        q_len.append(output)

    return q_len

def adding_headers(output, db_name, table_list):
    hd_list=[]
    for x in range(len(output)):
        for i, l in enumerate(output[x]):
            for j, col in enumerate(l):
                if j == 2:
                    if col.isdigit():
                        pass
                    else:
                        l.insert(j, ' ')

        for i, l in enumerate(output[x]):
            for j, col in enumerate(l):
                if j == 0:
                    l.insert(j, db_name)
                if j == 1:
                    l.insert(j, table_list[x])

        hd_list.append(output)
    headers = ['Database_name', 'Table_name', 'Column_name', 'Data_type', 'Data_length', 'Constraints']
    x=[]
    for flist in hd_list:
        x = [item for i in flist for item in i]
    x.insert(0, headers)
    return x



