
# coding: utf-8

from os import path
import os
import pandas as pd
import numpy as np
import pymysql
import logging
from sqlalchemy import create_engine

class IO_tools():
    def get_database_conn(self):
        conn = pymysql.connect(host='127.0.0.1',port=3306,user='analyzer',password='analyzer@tbs2016',database='dp_relation',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        return conn
    def get_close(self,conn,cur=''):
        if cur:
            cur.close()
        conn.close()
    def get_engine(self):
        engine = create_engine('mysql+pymysql://analyzer:analyzer@tbs2016@127.0.0.1:3306/dp_relation?charset=utf8mb4', encoding='utf-8', echo=False) # create a proxy for writing data to mysql.   
        return engine

    def get_data_from_file(self, read_url, read_type, sheet_name=0):
        doc = None
        try:
            read_url = self.return_right_filename(read_url,read_type)
            print('read_url:',read_url)
            if read_type == 'excel':
                if sheet_name:
                    doc = pd.read_excel(read_url,sheetname=sheet_name)
                else:
                    doc = pd.read_excel(read_url)
            elif read_type == 'csv':
                doc = pd.read_csv(read_url,encoding = 'utf-8')
            elif read_type == 'doc':
                doc = pd.read_table(read_url,sep = '\t',encoding = 'utf-8')
            else:
                logging.error('错误的文件格式')
            print('doc 示例：')
            print(doc[:3])
        except:
            logging.error('类型为%s的文件找不到，请确认路径是否在%s'%(read_type, read_url))
        return doc

    def get_tablename_from_db(self, project, keyword):
        '''
        从info_source_sheet 中获取存储表的名字
        '''
        conn = self.get_database_conn()
        cur = conn.cursor()
        sql_query = ("SELECT project_id,keyword_id,info_source_sheet FROM project_key where project_name='%s' and keyword = '%s'"%(project, keyword))
        cur.execute(sql_query)
        try:
            id_num = cur.fetchall()[0]
            project_id = id_num['project_id']
            keyword_id = id_num['keyword_id']
            table_name = id_num['info_source_sheet']
        except:
            raise NameError('找不到对应的项目与关键词 !')
        self.get_close(conn,cur)
        return project_id,keyword_id,table_name

    def readmysql(self, project_id, keyword_id, table_name, sql=''):
        '''
        除了关键字查询，也允许用户直接传入sql语句进行查询操作
        '''
        conn = self.get_database_conn()
        if sql:
            doc = pd.read_sql_query(sql, conn)
        else :
            doc = pd.read_sql_query("SELECT * FROM %s where project_id=%d and keyword_id = '%s'" %(table_name, project_id, keyword_id), conn)
        doc = pd.DataFrame(doc)
        for column in doc.columns:
            if len(np.where(doc[column].isnull())[0]) == len(doc):
                del doc[column]
        self.get_close(conn)
        return doc

    def write2excel(self, write_url,**kwargs):
        '''
        将dataframe数据写入excel文件
        '''
        write_url = write_url if write_url.endswith(".xlsx") else write_url + ".xlsx"
        writer = pd.ExcelWriter(write_url)
        for key in kwargs:
            if isinstance(kwargs[key], pd.DataFrame):
                print("key ,",key)
                kwargs[key]['project_id'] = kwargs['project_id']
                kwargs[key]['keyword_id'] = kwargs['keyword_id']
                kwargs[key].to_excel(writer, sheet_name = key, encoding = 'utf-8')
        writer.save()
        print("write successfully!")

    def write2sql(**kwargs):
        '''
        将dataframe数据写入sql文件
        '''
        conn = self.get_database_conn()
        cur = conn.cursor()
        engine = self.get_engine()
        sheet_names = kwargs['sheet_names']
        for table in sheet_names:
            sql_query = ("select keyword_id from %s where project_id = %d and keyword_id = '%s'"%(table,kwargs['project_id'],kwargs['keyword_id']))
            cur.execute(sql_query)
            length = len(cur.fetchall())
            if length != 0:
                print('Former data found in MySQL, trying to erase them!')
                sheet_names = kwargs['sheet_names']   #('srs_sents','srs_roles', 'srs_words')
                for sheet in sheet_names:
                    sql_query = ("DELETE FROM %s WHERE keyword_id='%s' and project_id=%d "%(sheet, kwargs['keyword_id'],kwargs['project_id']))
                    cur.execute(sql_query)
                print('Data erased successfully!')
                conn.commit()
            break
        for key in kwargs:
            if key in sheet_names:
                if len(kwargs[key]) == 0:
                    kwargs[key]['project_id'] = pd.Series([])
                    kwargs[key]['keyword_id'] = pd.Series([])
                else:
                    kwargs[key].loc[:,'project_id'] = kwargs['project_id']
                    kwargs[key].loc[:,'keyword_id'] = kwargs['keyword_id']
                kwargs[key].to_sql(name=key, con=engine, if_exists='append', index=False, chunksize=1000, dtype=None) # write to mysql with sqlalchemy method
        self.get_close(conn,cur)
        print("write successfully!")

    def return_right_filename(self, read_url,read_type):
        '''
        判断文件类型，返回完整正确的文件名
        '''
        if read_type == 'excel':
            read_url = read_url if read_url.endswith(".xlsx") else read_url+".xlsx"
        elif read_type == 'csv':
            read_url = read_url if read_url.endswith(".csv") else read_url+".csv"
        elif read_type == 'doc':
            read_url = read_url if read_url.endswith((".txt", ".tsv")) else read_url+".txt"
        return read_url

    def delete_temp(self, filepath, filetype=''):
        filepath = self.return_right_filename(filepath,filetype)
        if os.path.exists(filepath):
            os.remove(filepath)
        print("remove file:",filepath)

