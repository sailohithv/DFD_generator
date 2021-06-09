import sys
import DML_Parser_query_sep as Qs
import DML_Parser_lineage_builder as lb
# import DDL_validator.q_uploads as q
import os

import os.path

def dml_parser(file_name):

    vt_queries,normal_queries=Qs.query_processing().query_sep(os.getcwd()+"\q_uploads\\"+file_name)

    target_tb_names, target_tb_query = Qs.query_processing().table_nameList_query(normal_queries)
    vt_tb_names, vt_tb_query = Qs.query_processing().table_nameList_query(vt_queries)
    # print target_tb_names
    target_tb_names_dict, target_alias_name_dict = Qs.query_processing().list_all_tables(target_tb_query, target_tb_names)
    vt_tb_names_dict, vt_alias_name_dict =Qs.query_processing().list_all_tables(vt_tb_query, vt_tb_names)
    # print target_tb_names_dict

    final_table_dict = target_tb_names_dict.copy()
    final_table_dict.update(vt_tb_names_dict)

    f_temp_alias_dict=target_alias_name_dict.copy()
    f_temp_alias_dict.update(vt_alias_name_dict)

    final_table_query_dict=target_tb_query.copy()
    final_table_query_dict.update(vt_tb_query)

    tableName_dict,aliasName_dict,tableQuery_dict=Qs.query_processing().table_names_list_with_Query(normal_queries,vt_queries)

    # print tableName_dict
    # print aliasName_dict


    # Qs.query_processing().get_column_names(tableQuery_dict,aliasName_dict,tableName_dict)
    column_names_dict=Qs.query_processing().get_column_names(final_table_query_dict,f_temp_alias_dict,final_table_dict)
    db_name=Qs.query_processing().get_db_name(final_table_query_dict)


    return db_name,final_table_dict,aliasName_dict,column_names_dict,final_table_query_dict

def dml_parser_lineage_build(file_name):

    db_name, final_table_dict, aliasName_dict, column_names_dict, final_table_query_dict=dml_parser(file_name)
    # Lineage Building
    dependancy_list = lb.depend_list().root(final_table_dict)
    tbls_cols_list = lb.depend_list().dic_column_list(column_names_dict)
    position_list = lb.table_positioning(dependancy_list, tbls_cols_list).get_position_list(dependancy_list)
    lb.lineage_diagram().excel_lineage(position_list, tbls_cols_list)

