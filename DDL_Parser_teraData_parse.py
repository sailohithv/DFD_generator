import re
import xlwt

def get_queries():
    fd = open('teraData_queryFile', 'r')
    sqlFile = fd.read()
    fd.close()

    # all SQL commands (split on ';')
    sqlCommands = sqlFile.split(';')

    queries=[]

    for i in sqlCommands:
        queries.append(i.lower())

    return queries

def tab_clean(qlist):
    create_queries = []
    for i in qlist:
        i = re.sub("\s\s+", " ", i)
        i = i.lower()
        li1 = i.split('\n')
        # print li1
        i = ''.join(li1)
        create_queries.append(i.encode('utf-8'))
    return create_queries

def query_parsing(create_queries):
    t=[]
    for i in create_queries:
        t.append(re.findall('table (.+?)\,', i))
    tabs = [item.encode('utf-8') for sublist in t for item in sublist]
    li=[]
    dbname=[]
    tabname=[]

    for i in tabs:
        li.append(i.split('.'))

    for i,l in enumerate(li):
        for j,col in enumerate(l):
            if j==0:
                dbname.append(col)
            else:
                tabname.append(col)

    tableName_Create_query = dict(zip(tabname, create_queries))
    ftables = []
    for i in tableName_Create_query:
        ftables.append(i)

    pk = []
    for q in create_queries:
        pk.append(re.findall('index ' + '\((.*)\)', q))
    pk_cols = [item for i in pk for item in i]
    pk_dict=dict(zip(ftables,pk_cols))


    return tableName_Create_query,ftables,dbname,pk_dict

def tab_split(query_list):
    li=[]
    for q in query_list.values():
        spos = q.find('(')
        q = q.replace(q[spos], '|', 1)
        rev = q[::-1]
        rev = rev.replace(')', '|', 2)
        q = rev[::-1]
        a = q.split('|')
        out = a[1].split(',')
        li.append(out)
    return li

def table_constraints( query_ll,pk_dict):
    query_list = []
    for out in query_ll:
        str1 = ','.join(out)

        list_strip = []
        for i in out:
            list_strip.append(i.strip(" "))

        output = []
        for i in list_strip:
            output.append(i.split(" ", 2))

        for i in output:
            for val in pk_dict.values():
                if val in i:
                    i.append('unique primary index')

        for i, l in enumerate(output):
            for j, col in enumerate(l):
                if (j > 2):
                    output[i][j - 1] = output[i][j - 1] + ' ' + output[i][j]
                    output[i].remove(output[i][j])

        query_list.append(output)

    return query_list

def adding_tabnames(queries, dbnames, table_names):
    # queries=self.table_constraints()
    headers = ['Database_name','Table_name', 'Column_name', 'Data_type','Data_length', 'Constraints']

    for k in range(len(table_names)):
        for i, l in enumerate(queries[k]):
            for j, col in enumerate(l):
                if j == 0:
                    l.insert(j, dbnames[k])
                if j == 1:
                    l.insert(j, table_names[k])

    li2 = []
    li2.append(headers)
    queries.insert(0, li2)
    return [item for i in queries for item in i]


















