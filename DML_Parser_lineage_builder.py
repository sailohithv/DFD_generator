import xlsxwriter
class depend_list:
    def dependant(self, dic, dics_list, dependancy_list):
        for key in dics_list:
            if key in dic.keys():
                if len(dic[key]) > 0:
                    k = dic[key][:]  # creating a copy of list
                    dependancy_list.append(k)
                    dependancy_list[len(dependancy_list) - 1].insert(0, key)
                    self.dependant(dic,dic[key],dependancy_list)  # calling a recursive function to create a dependant list
                elif len(dic[key]) == 0:
                    temp=[]
                    temp.append(key)
                    dependancy_list.append(temp) # calling a recursive function to create a dependant list

    def root(self, table_dic):
        # for k, v in table_dic.items():
        #     if len(v) == 0:
        #         del table_dic[k]
        dependancy_list = []
        keys = table_dic.keys()
        values = table_dic.values()
        new_list = []
        for i in values:
            new_list += i  # forming a single list that holds all the values in the dictionary

        for key in keys:
            if key not in new_list:
                root = key
        init_val = table_dic[root][:]  # creating a copy of the list
        init_val.insert(0, root)

        dependancy_list.append(init_val)
        self.dependant(table_dic, table_dic[root], dependancy_list)
        return dependancy_list

    def dic_column_list(self, column_dict):
        columns_list = []
        for key, val in column_dict.items():
            val.insert(0, str(key))
            columns_list.append(val)
        return columns_list


class table_positioning:
    dependancy_list=[]
    tbls_cols_list=[]
    tables_in_celllist = []
    main_list=[]
    t_celllist = []

    j = 0
    c = 1
    r = 1
    def __init__(self,dependancy_list,tbls_cols_list):
        self.dependancy_list=dependancy_list
        self.tbls_cols_list=tbls_cols_list


    # ---------------------------------------------
    def table_list(self):

        for table in self.main_list:
            if table[0] not in self.tables_in_celllist:
                self.tables_in_celllist.append(table[0])
        return self.tables_in_celllist



    def col_id(self, intv, cc, cr):

        li = []
        li.append(intv)
        li.append(cc)
        li.append(cr)

        for i in range(len(self.tbls_cols_list)):
            if self.tbls_cols_list[i][0] == intv:
                # print 'strange',col[i][0],intv
                no_of_rows = len(self.tbls_cols_list[i])
                er = cr + no_of_rows + 2
                # print er
                ec = cc
                # print ec
                li.append(ec)
                li.append(er)
            # print li

        self.main_list.append(li)
        # print self.main_list

    def case_5(self,i, j, ref_key, var):
        j = 0

        t_celllist=self.table_list()


        # print t_celllist
        #print t_celllist,ref_key,i
        if ref_key in t_celllist:
            # print t_celllist
            # print ref_key
    
            for table_id in range(len(t_celllist)):
                if ref_key == t_celllist[table_id]:


                    #print self.t_celllist
                    #print self.main_list
                    #print table_id
                    c = self.main_list[table_id][3]

                    r = self.main_list[len(self.main_list) - 1][4] + 2
                    if len(self.dependancy_list[i]) == 1:

                        #print self.dependancy_list[i][j], c, r
                        self.col_id(self.dependancy_list[i][j], c, r)
                        break

                    else:
                        # print l2[i][j],c,r
                        self.col_id(self.dependancy_list[i][j], c, r)

                        j = j + 1
                        self.check_condition(i, j)



    def check_condition(self, i, j):

        # print i,j
        
        #print self.dependancy_list[i][j]
        if i + 1 <= len(self.dependancy_list) - 1 and self.dependancy_list[i + 1][0] == self.dependancy_list[i][j] and j == 1:

            ic = 2
            ir = 0
            self.case_3(i, j, ic, ir)


        elif i + 1 <= len(self.dependancy_list) - 1 and self.dependancy_list[i + 1][0] != self.dependancy_list[i][j] and j == 1:
            ic = 2
            ir = 0
            self.case_3(i, j, ic, ir)
            if j + 1 <= len(self.dependancy_list[i]) - 1:
                j += 1
                self.check_condition(i, j)

        elif i + 1 <= len(self.dependancy_list) - 1 and self.dependancy_list[i + 1][0] == self.dependancy_list[i][j] and j > 1:
            ic = 0
            ir = 2
            c = self.main_list[len(self.main_list) - 1][3] + ic
            r = self.main_list[len(self.main_list) - 1][4] + ir
            self.col_id(self.dependancy_list[i][j], c, r)

        elif i + 1 <= len(self.dependancy_list) - 1 and self.dependancy_list[i + 1][0] != self.dependancy_list[i][j] and j > 1:
            ic = 0
            ir = 2
            c = self.main_list[len(self.main_list) - 1][3] + ic
            r = self.main_list[len(self.main_list) - 1][4] + ir
            self.col_id(self.dependancy_list[i][j], c, r)
            if j + 1 <= len(self.dependancy_list[i]) - 1:
                j += 1
                self.check_condition(i, j)

        elif i == len(self.dependancy_list) - 1 and j == 1:
            ic = 2
            ir = 0
            self.case_3(i, j, ic, ir)
            if j + 1 <= len(self.dependancy_list[i]) - 1:
                j += 1
                ic = 0
                ir = 2
                self.case_4(i, j, ic, ir)

    def case_2(self, i, j):
        r=1
        if self.main_list[i - 1][0] == self.dependancy_list[i - 1][0]:
            c = self.main_list[0][3] + 2

            self.col_id(self.dependancy_list[i][j], c, r)
            j = j + 1
            self.check_condition(i, j)


        else:
            c = self.main_list[len(self.main_list) - 1][3] + 2
            self.check_condition(i, j)

    def case_3(self,i, j, ic, ir):
        r = self.main_list[len(self.main_list) - 1][2]
        c = self.main_list[len(self.main_list) - 1][3] + ic
        self.col_id(self.dependancy_list[i][j], c, r)

    def case_4(self,i, j, ic, ir):
        r = self.main_list[len(self.main_list) - 1][4] + ir
        c = self.main_list[len(self.main_list) - 1][3]
        self.col_id(self.dependancy_list[i][j], c, r)


    def search_index(self, i, j):
        #print self.dependancy_list[i][j]
        var = 0
        index_key = self.dependancy_list[i][0]

        for k in range(len(self.dependancy_list)):
            if index_key in self.dependancy_list[k] and k < i:
                # print index_key

                var = k
                #print self.dependancy_list[var]
                search_index = self.dependancy_list[k].index(index_key)
                # print search_index
                ref_key = self.dependancy_list[k][search_index -1]
                # print ref_key
                # print index_key, 'cap',ref_key
                break

        self.case_5(i, j, ref_key, k)

    def dep_col_main(self, dependancy_list, j=0):
        for i in range(len(dependancy_list)):
            t_celllist = self.table_list()

            if i == 0:
                self.col_id(dependancy_list[0][0], 1, 1)

            elif i == 1 and dependancy_list[i][j] not in t_celllist:
                self.case_2(i, j)

            # elif (i > 1) and (dependancy_list[i][0] in t_celllist) and i != len(dependancy_list) - 1:
            elif (i > 1) and len(dependancy_list[i]) > 1 and (dependancy_list[i][0] in t_celllist) and i != len(dependancy_list) - 1:

                j = 0
                j = j + 1
                self.check_condition(i, j)

            elif i > 1 and dependancy_list[i][0] not in t_celllist:

                self.search_index(i, j)

            elif i == len(dependancy_list) - 1 and dependancy_list[i][0] != t_celllist[-1]:

                self.search_index(i, j)

    def get_position_list(self, dependancy_list):
        self.dep_col_main(dependancy_list)
        return self.main_list

class lineage_diagram:

    def excel_lineage(self,position_list,tbls_cols_list):

        workbook = xlsxwriter.Workbook(
            "C:\\xampp\htdocs\SQL_parser\XlsFiles\lineage_flow.xlsx")
        worksheet = workbook.add_worksheet()

        cellist = position_list
        arrow_pos = []
        cl = []
        for i in range(1, len(cellist)):
            cl.append(cellist[i][1] - 1)
            l = []
            l.append(cellist[i][1] - 1)
            l.append(cellist[i][2]+1)
            arrow_pos.append(l)

        # print arrow_pos
        # print cl

        maxm = max(cl) + 1

        val_chr = 'B1:'
        # print val_chr
        val_chr += chr(65 + maxm)
        # print val_chr
        val_chr += str(1)
        # print val_chr

        '''
        columnlist=[['hey','hey1','hey2','hey3'],['h','h1','h2','hey1','hey2'],['k','k1','k2','k3','k4'],['l','l1','l2','l3','l4'],['B','c1','c2','d1'],
                    ['bb','k1','k2','l1','l2'],['c','c1','c2','c3'],['d','d1','d2','d3'],['hi','hi1','hi2','hi3'],['p','hi1','hi2','h1','hey1'],
                    ['o','o1','o2','o3'],['aa','o1','hi1','h1','hey1','hi2'],['A','o1','hi1','h1','hey1','k1','l1'],['final','o1','hi1','h1','hey1','k1','l1','c1','d1']]'''

        columnlist = tbls_cols_list
        format2 = workbook.add_format({'border': 2})

        merge_format = workbook.add_format({
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': 'yellow'})

        cell_format = workbook.add_format()

        # Merge 3 cells.
        worksheet.merge_range(val_chr, 'Merged Range', merge_format)

        worksheet.freeze_panes(1, 1)
        for i in range(0, len(cellist)):
            sc = cellist[i][1]
            sr = cellist[i][2]
            for j in range(0, len(columnlist)):
                if columnlist[j][0] == cellist[i][0]:
                    for k in range(0, len(columnlist[j])):
                        value = columnlist[j][k]
                        worksheet.write(sr, sc, value, format2)
                        sr += 1

        for i in range(len(arrow_pos)):
            val = 65 + arrow_pos[i][0]
            val_chr = chr(val)
            val_chr += str(arrow_pos[i][1])
            worksheet.insert_image(val_chr, 'left.png')

        worksheet.protect()
        workbook.close()