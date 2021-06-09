import os
import re
import xlwt

def get_queries():
    fd = open('hive_queryFile', 'r')
    sqlFile = fd.read()
    fd.close()
    sqlCommands = sqlFile.split(';')

    queries=[]

    for i in sqlCommands:
        queries.append(i.lower())

    return queries
def query_parsing(qlist):
    t = []
    for i in qlist:
        t.append(re.findall('table (.+?)\(', i))
    # print t
    tab_names = [item.encode('utf-8') for sublist in t for item in sublist]
    #print tab_names
    table_names = []
    for i in tab_names:
        table_names.append(i.strip(" "))

    tableName_Create_query = dict(zip(table_names, qlist))
    ftables=[]
    for i in tableName_Create_query:
        ftables.append(i)
    return tableName_Create_query,ftables

def tab_split(query_list):
    li=[]
    for q in query_list.values():
        spos = q.find('(')
        q = q.replace(q[spos], '|', 1)
        rev = q[::-1]
        rev = rev.replace(')', '|', 1)
        q = rev[::-1]
        a = q.split('|')
        out = a[1].split(',')

        li.append(out)
    return li

def table_constraints(query_ll):
    #query_ll=self.tab_split()
    query_list=[]
    constraints = ['unique key', 'primary key', 'foreign key']
    for out in query_ll:
        str1 = ','.join(out)

        cons_name = []
        di = {}
        for c in constraints:
            if c in str1:
                cons_name.append(c)
                r = re.findall(c + '\s\((.*?)\)', str1)
                for j in r:
                    di.setdefault(j, c)

        dictionary = {}
        for k in di:
            li1 = str(k).split(',')
            for h in li1:
                h = h.strip()
                dictionary.setdefault(h, di.get(k))

        list_strip = []
        for i in out:
            list_strip.append(i.strip(" "))

        indices = []
        for i in list_strip:
            if (re.search('\(([a-zA-Z].*?)\)', i)):
                indices.append(list_strip.index(i))

        for i in indices:
            list_strip.pop()

        output = []
        for i in list_strip:
            output.append(i.split(" ", 2))

        for i in output:
            for key in dictionary:
                if key in i:
                    i.append(dictionary[key])

        #print output

        for i, l in enumerate(output):
            for j, col in enumerate(l):
                if (j > 2):
                    output[i][j - 1] = output[i][j - 1] + ' ' + output[i][j]
                    output[i].remove(output[i][j])

        query_list.append(output)

    return query_list

def adding_tabnames(queries,table_names):
    #queries=self.table_constraints()
    headers = ['Table_name', 'Column_name', 'Data_type', 'Constraints']

    for k in range(len(table_names)):
        for i, l in enumerate(queries[k]):
            for j, col in enumerate(l):
                if j == 0:
                    l.insert(j, table_names[k])

    li2=[]
    li2.append(headers)
    queries.insert(0,li2)

    return [item for i in queries for item in i]




