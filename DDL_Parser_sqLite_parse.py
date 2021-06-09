import re
import xlwt

import cgi
import cgitb
cgitb.enable()


class DbConnection:
    def __init__(self):
        pass

    def show_tables(self, cursor,field_Data):
        table_names = []
        res = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        for name in res:
            table_names.append(name[0])
        t_name = []
        for i in table_names:
            t_name.append(i.encode('utf-8'))
        # print(t_name)
        # dic2 = {1: "all tables", 2: "selected table/tables"}
        # print dic2
        # user_type = input("enter the tables to be executed:")
        user_type=field_Data.getvalue('tb_name')
        if user_type == "all tables":
            return t_name
        else:
            # print t_name
            user_tables = list(map(str, user_type.split()))
            return user_tables

    def show_create_tables(self, cursor, tables_list):
        result = {}
        create_queries = []
        cursor.execute(
            "SELECT sql FROM (SELECT sql sql, type type, tbl_name tbl_name, name name FROM sqlite_master UNION ALL "
            "SELECT sql, type, tbl_name, name FROM sqlite_temp_master) WHERE type != 'meta' AND sql NOTNULL AND name "
            "NOT LIKE 'sqlite_%' ORDER BY substr(type, 2, 1), name")
        res = cursor.fetchall()
        queries = [item for sublist in res for item in sublist]

        for i in queries:
            i = re.sub("\s\s+", " ", i)
            i = i.lower()
            li1 = i.split('\n')
            i = ''.join(li1)
            create_queries.append(i.encode('utf-8'))

        t = []
        for i in create_queries:
            t.append(re.findall('table (.+?)\(', i))
        tab_names = [item.encode('utf-8') for sublist in t for item in sublist]
        table_names = []
        for i in tab_names:
            table_names.append(i.strip(" "))

        table_name_create_query = dict(zip(table_names, create_queries))

        for i in tables_list:
            result.setdefault(i, table_name_create_query.get(i))
        return result

    def tab_split(self, create_table_dict):
        encoded_table_name = []
        q_list = []
        for q in create_table_dict.values():
            start_pos = q.find('(')

            table_name = re.findall('table (.+?)\(', q)

            for i in table_name:
                encoded_table_name.append(i.encode('utf-8'))

            q = q.replace(q[start_pos], '|', 1)
            rev = q[::-1]
            rev = rev.replace(')', '|', 1)
            q = rev[::-1]
            a = q.split('|')
            out = a[1].split(',')
            q_list.append(out)

        return q_list

    def table_constraints(self, query_ll):
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

            query_list.append(output)

        return query_list

    def data_length(self, query_cons_list):
        query_len_split=[]
        for output in query_cons_list:
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
                    if (j > 3):
                        output[i][j - 1] = output[i][j - 1] + ' ' + output[i][j]
                        output[i].remove(output[i][j])

            query_len_split.append(output)

        return query_len_split

    def adding_dbnames(self, query_list, db_name):
        added_db_queries=[]
        for output in query_list:
            for i, l in enumerate(output):
                for j, col in enumerate(l):
                    if (j == 2):
                        if (col.isdigit()):
                            pass
                        else:
                            l.insert(j, ' ')

            for i, l in enumerate(output):
                for j, out in enumerate(l):
                    if j == 0:
                        l.insert(j, db_name)
            added_db_queries.append(output)

        return added_db_queries

    def adding_tab_db_names(self, output, table_names):
        for k in range(len(table_names)):
            for i, l in enumerate(output[k]):
                for j, col in enumerate(l):
                    if j == 1:
                        l.insert(j, table_names[k])
        headers = ['Database_name', 'Table_name', 'Column_name', 'Data_type', 'Data_length', 'Constraints']
        x = [item for i in output for item in i]
        x.insert(0, headers)
        return x

