import re
from collections import defaultdict

# File handling Class which reads and writes with File name
class File_handling:
    def readFromFile(self,file_name):
        MFile=open(file_name,'r')
        return MFile.read().replace('\n',' ')
    def writeToFile(self,file_name,values):
        MFile= open(file_name,'w')
        MFile.write(values)

# Class to Proccess Query File
class query_processing(File_handling):
    # Get Database name
    def get_db_name(self,tb_query):
        db=[]
        for tb,query in tb_query.items():
            x=re.search(r"(\w+)\."+tb,query)
            if (x):
                db.append(x.group(1))
            else:
                continue
        return db[0]
    # Fetch volatile Queries and Normal Queries
    def query_sep(self,filename):
        volatile_queries_list = []
        normal_queries_list=[]
        file_to_string = File_handling().readFromFile(filename).lower()
        file_to_string = re.sub("\s\s*", " ", file_to_string)
        # print file_to_string
        queries=file_to_string.split(';')
        for query_itr in queries:
            q_check=re.search("(create\s+volatile\s+table)", query_itr)
            if (q_check):
                volatile_queries_list.append(query_itr)
            else:
                normal_queries_list.append(query_itr)

        return volatile_queries_list,normal_queries_list

    def table_nameList_query(self, queryList):
        identifiers=["into","update","table"]
        table_names=[]
        table_query={}
        for trgt_idntfr in identifiers:
            for query in queryList:
                match_exist=re.search(r"\b"+trgt_idntfr+"\s+(.*?)\(", query)
                if(match_exist):
                    tb_name=match_exist.group(1).strip().split(' ')[0].split('.')[-1]
                    table_names.append(tb_name)
                    table_query[tb_name]=query
                else:
                    continue
        return table_names,table_query

    # Fetch temp table alias names with temp table queries in a dictionary
    def get_temp_table_names(self, query_str, t_name):
        tempTable_alias_dict = {}
        braces_itr_list_regex = [r"\b(from)\s*(\()", r"\b(join)\s*(\()"]
        for itr_regex in braces_itr_list_regex:
            from_iter = re.finditer(itr_regex, query_str)
            start_paranthesis_index = [itr.start(2) for itr in from_iter]
            stack = 0
            end_paranthesis_index = []
            for paranthesis in start_paranthesis_index:
                for ind in range(paranthesis, len(query_str)):
                    if query_str[ind] == "(":
                        stack += 1
                    if query_str[ind] == ")":
                        stack -= 1
                        if stack == 0:
                            end_paranthesis_index.append(ind)
                            break
                start_end_paranthesis_dict = dict(zip(start_paranthesis_index, end_paranthesis_index))
                if (bool(start_end_paranthesis_dict)):
                    for pind_itr in start_end_paranthesis_dict.keys():
                        inside_brac_string = re.search("(\))\s*(\w+)", query_str[
                                                                       start_end_paranthesis_dict[pind_itr]:len(
                                                                           query_str)])
                        tempTable_alias_dict[inside_brac_string.group(2)] = query_str[
                                                                            pind_itr:start_end_paranthesis_dict[
                                                                                         pind_itr] + 1]
        return tempTable_alias_dict

    # Fetch table names and its alias names if any from a TABLE query
    def get_tableNames_aliasNames(self, query_str, tb_name):
        temp_table_list = []
        tables_list = []
        tables_alias_name_dict = defaultdict(list)
        table_chk_identifiers = [r"\b(into)\s+([a-z\._\s+]+)\(", r"(from)\s+(.*?)\s+(join)", r"(from)\s+(.*?)\s+(left)",
                                 r"(from)\s+(.*?)\s+(right)", r"(from)\s+(.*?)\s+(full)", r"(join)\s+(.*?)\s+\b(on)",
                                 r"(from)\s+([a-z\._]+)\s*(\))$", r"(from)\s+([a-z\._]+)\s+(where)",
                                 r"(from)\s+(.*?)\s+(union)"]
        for identifier in table_chk_identifiers:
            temp_table_list.extend(re.findall(identifier, query_str))
            # print temp_table_list
        for tup in range(0, len(temp_table_list)):
            if (str(temp_table_list[tup][1]).__contains__('(') or str(temp_table_list[tup][1]).__contains__(')')):
                continue

            else:
                alias_spliting = re.split(r"\s", temp_table_list[tup][1].strip())
                # print alias_spliting
                t_name=alias_spliting[0].split('.')[-1]
                if len(alias_spliting)<4:
                    # print alias_spliting
                    if alias_spliting[0] in tables_list:
                        continue
                    else:
                        if t_name!=tb_name:
                            tables_list.append(t_name)

                    if (len(alias_spliting) > 1):
                        tables_alias_name_dict[t_name].append(alias_spliting[- 1])
                    else:
                        tables_alias_name_dict[t_name] .append("--")
        return tables_list, dict(tables_alias_name_dict)

    def list_all_tables(self, table_queryDict, table_names):
        tables_table_name_dict={}
        tables_alias_name_dict={}
        for table in table_names:
            # print table
            # print table_queryDict[table]
            tblist, tb_alias_dic = self.get_tableNames_aliasNames(table_queryDict[table], table)
            # print tblist
            # print tb_alias_dic
            table_alias = self.get_temp_table_names(table_queryDict[table], table)
            # print table_alias
            # print table_alias.keys()
            for i in table_alias.keys():
                alias_tbs,alias_tb_alias_dic=self.get_tableNames_aliasNames(table_alias[i], table)
                tblist.extend(alias_tbs)
                tb_alias_dic.update(alias_tb_alias_dic)
            tables_table_name_dict[table]=list(set(tblist))
            tables_alias_name_dict[table]=tb_alias_dic
        return tables_table_name_dict,tables_alias_name_dict

    # Merge target and volatile tables,alias_dict,queries
    def table_names_list_with_Query(self, normal_query, volatile_query):
        target_tb_names, target_tb_query = self.table_nameList_query(normal_query)
        vt_tb_names, vt_tb_query = self.table_nameList_query(volatile_query)
        # print target_tb_names
        target_tb_names_dict, target_alias_name_dict = self.list_all_tables(target_tb_query, target_tb_names)
        vt_tb_names_dict, vt_alias_name_dict = self.list_all_tables(vt_tb_query, vt_tb_names)
        # print target_tb_names_dict

        final_table_dict = target_tb_names_dict.copy()
        final_table_dict.update(vt_tb_names_dict)

        f_temp_alias_dict=target_alias_name_dict.copy()
        f_temp_alias_dict.update(vt_alias_name_dict)

        final_table_query_dict=target_tb_query.copy()
        final_table_query_dict.update(vt_tb_query)

        toDel = []
        for vt_tbl in vt_tb_names:
            for tbl_key, tbl_list in final_table_dict.items():
                if vt_tbl in tbl_list:
                    tbl_list.extend(final_table_dict.get(vt_tbl))
                    tbl_list.remove(vt_tbl)
                    toDel.append(vt_tbl)

        for i in list(set(toDel)):
            final_table_dict.__delitem__(i)
        final_alias_dict={}
        # for k,v in f_temp_alias_dict.items():
        #     final_alias_dict.update(dict(v))

        return final_table_dict, f_temp_alias_dict,final_table_query_dict

    # Fetch column names of corresponding table
    # def get_column_names(self, tbName_query_dict, tbName_alias_dict,tbName_dict):
    #     selecter_cols=[]
    #     joiner_cols=[]
    #     tb_col_dict={}
    #     final_tb_col_di={}
    #     for target_tb,target_tb_val in tbName_alias_dict.items():
    #         t_dict = {}
    #         for tname,alias in target_tb_val.items():
    #             columns_list = []
    #             # check_condition = re.search(r"\b" + tname + "\s*\((.*)\)\s*select", tbName_query_dict[target_tb])
    #             # if (check_condition):
    #             #     columns_list.extend(
    #             #         re.findall(r"\b" + tname + "\s*\((.*)\)\s*select", tbName_query_dict[target_tb]))
    #             #     if tname != target_tb:
    #             #         t_dict[tname] = columns_list
    #
    #             # else:
    #             columns_list.extend(re.findall(r"\b" + tname + "\.(\w+)", tbName_query_dict[target_tb]))
    #             for alias_itr in alias:
    #                 if alias_itr != "--" and alias_itr!=tname:
    #                     columns_list.extend(re.findall(r"\b" + alias_itr + "\.(\w+)", tbName_query_dict[target_tb]))
    #                 if tname!=target_tb:
    #                     t_dict[tname] = columns_list
    #         tb_col_dict[target_tb] = t_dict
    #     print tb_col_dict
    #
    #     for main_tb in tb_col_dict.keys():
    #         x=re.search(r'select(.*?)\bfrom',tbName_query_dict[main_tb])
    #         if(x):
    #             final_tb_col_di[main_tb]=re.findall(r'(\w+)\s*,',x.group().replace("from",",from"))
    #         del(tb_col_dict[main_tb])
    #     for i in tb_col_dict:
    #         final_tb_col_di.update(i)
    #     return final_tb_col_di

# Fetch column names of corresponding table
    def get_column_names(self, tbName_query_dict, tbName_alias_dict, tbName_dict):
        modified_alias_dict=defaultdict(list)

        #Simplify table alias name dictionary
        for tbl_alias_dict in tbName_alias_dict.values():
            for key,val in tbl_alias_dict.items():
                modified_alias_dict[key].extend(val)

        temp_alias_list=[]
        temp_alias_list.extend(modified_alias_dict.keys())
        for i in modified_alias_dict.values():
            temp_alias_list.extend(i)

        tb_col_dict = {}
        for tb_name,query in tbName_query_dict.items():
            column_list=[]
            into_check_cond = re.search(r"\b" + tb_name + "\s*\((.*)\)\s*select", tbName_query_dict[tb_name])
            create_check_cond= re.search(r"\bcreate\s+table\s+" + tb_name + "\s*\((.*)\)", tbName_query_dict[tb_name])
            if(into_check_cond):
                column_list.extend(re.split(r',',into_check_cond.group(1)))
                tb_col_dict[tb_name]=column_list
            elif(create_check_cond):
                ignore_idtfrs=['primary','constraint','foreign','references']
                comma_sep_list=create_check_cond.group(1).split(',')
                for isep in comma_sep_list:
                    clname=isep.strip().split(' ')[0]
                    if clname not in ignore_idtfrs:
                        column_list.append(clname)
                tb_col_dict[tb_name] = column_list

            else:
                c_list=[]
                selector_col_check = re.search(r'select(.*?)\bfrom', tbName_query_dict[tb_name])
                if(selector_col_check):
                    c_list.extend( re.findall(r'(\w+)\s*,',selector_col_check.group().replace("from",",from")))
                    joiner_col_check =tbName_query_dict[tb_name].replace(selector_col_check.group(),'')
                    for alias_itr in temp_alias_list:
                        c_list.extend(re.findall(r"\b" + alias_itr + "\.(\w+)",joiner_col_check))
                    tb_col_dict[tb_name]=list(set(c_list))


        return tb_col_dict

