from collections import defaultdict
from pandas import *
xls = ExcelFile('C:\\xampp\htdocs\SQL_parser\XlsFiles\MYSQL_out.xls')
df = xls.parse(xls.sheet_names[0])
excel_dict=df.to_dict()

table_name_dict=excel_dict['Table_name']
col_name_dict=excel_dict['Column_name']

tb_col_tuple=zip(table_name_dict.values(),col_name_dict.values())

ddl_dict=defaultdict(list)
c_list=[]
for tuple_itr in tb_col_tuple:
    ddl_dict[tuple_itr[0].encode('utf-8')].append(tuple_itr[1].encode('utf-8'))
# print dict(ddl_dict)


def compare_dict(dml_tbl_dict, ddl_tbl_dict):
    dif_dict = defaultdict(list)
    for tb_name, cl_names in dml_tbl_dict.items():
        # dif_dict[tb_name] = list(set(ddl_tbl_dict[tb_name]) - set(cl_names))
        for dml_col_itr in cl_names:
            # for ddl_col_itr in ddl_tbl_dict[tb_name]:
            if dml_col_itr not in ddl_tbl_dict[tb_name]:
                dif_dict[tb_name].append(dml_col_itr)
    return dict(dif_dict)

def mismatch_combination(dif_dict,alias_dict,tbl_query):
    mismatch_list=[]

    itr_dict=defaultdict(list)
    for tb_name in dif_dict.keys():
        for it in alias_dict[tb_name].values():
            if it =='--':
                continue
            else:
                itr_dict[tb_name].extend(it)
        itr_dict[tb_name].append(tb_name)
    for tb,tv in dif_dict.items():
        mismatch_list.extend([mis_alias + "." + mis_column for mis_alias in itr_dict[tb] for mis_column in tv])
    return mismatch_list



dml_tbl_dict={'courses': ['name', 'location', 'fees'], 'manager': ['branch_id'], 'suppliers': ['e_suppliername', 'phone', 'addressline1', 'addressline2', 'city', 'state', 'postalcode', 'country', 'e_pin', 'customernumber'], 'results': ['id', 'name'], 'physician': ['id', 'e_first_name', 'full_name', 'address', 'total']}
ddl_tbl_dict= {'courses': ['name', 'location', 'fees'], 'manager': ['branch_id', 'year'], 'results': ['id', 'name', 'result_state'], 'suppliers': ['suppliername', 'phone', 'addressline1', 'addressline2', 'city', 'state', 'postalcode', 'country', 'customernumber'], 'physician': ['id', 'full_name', 'address', 'total']}
alis_d={'courses': {'courses': '--'}, 'manager': {'du_manager': '--', 'branch_master': '--'}, 'physician': {'physician': '--', 'total_orders': ['to'], 'temp': ['tm']}, 'suppliers': {'suppliers': '--', 'customers': ['cs'], 'names': ['nm']}, 'results': {'names': ['f'], 'results': '--', 'people': ['d']}}
tb_query={'courses': ' insert into ccwd.courses( select c.name, c.location,c.fees from course c where c.cid = 2)', 'manager': " update ccwd.manager set status = 'y' where branch_id in ( select branch_id from (select * from ccwd.du_manager) as m2 where (branch_id, year) in ( select branch_id, year from ccwd.branch_master where type = 'finance' ) ))", 'physician': ' insert into ccwd.physician ( select to.id, to.e_first_name, to.full_name, to.address, to.total from ccwd.total_orders as to join temp as tm on tm.od=to.od where total > 10000)', 'suppliers': " insert into ccwd.suppliers ( select cs.e_suppliername, cs.phone, cs.addressline1, cs.addressline2, cs.city, cs.state , cs.postalcode, cs.country, cs.e_pin, cs.customernumber from ccwd.customers as cs join ccwd.names as nm on nm.as=cs.as where cd.country = 'usa' and cd.state = 'ca'", 'results': ' insert into ccwd.results ( select d.id, name from names f join people d on d.id = f.id where d.mid is not null)'}
xd=compare_dict(dml_tbl_dict,ddl_tbl_dict)
print mismatch_combination(xd,alis_d,tb_query)


