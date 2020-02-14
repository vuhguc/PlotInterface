import sqlalchemy as sa
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os



def make_db_path(host, port, username, password):
    return 'mysql+pymysql://{}:{}@{}:{}'.format(username, password, host, port)



def test_db_connection(db_path):
    engine = sa.create_engine(db_path)
    con = engine.connect()
    con.close()



def remove_file(file_path):
    os.remove(file_path)



def get_schema_list(db_path):
    engine = sa.create_engine(db_path)
    insp = sa.inspect(engine)
    schema_list = insp.get_schema_names()
    return schema_list



def get_table_list(db_path, schema):
    engine = sa.create_engine(db_path)
    insp = sa.inspect(engine)
    table_list = insp.get_table_names(schema=schema)
    return table_list



def get_column_list(db_path, schema, table):
    engine = sa.create_engine(db_path)
    insp = sa.inspect(engine)
    columns = insp.get_columns(schema=schema, table_name=table)
    column_list = [column['name'] for column in columns]
    return column_list



def read_formatted_file(file_path, replacements):
    with open(file_path, 'r') as sql_file:
        sql_statement = sql_file.read()
        for wild_card in replacements:
            sql_statement = sql_statement.replace('{{%{}}}'.format(wild_card), replacements[wild_card])
        return sql_statement



def bytes_to_string(bytes_data):
    return bytes_data.decode('utf-8')



def execute_sql_statement(db_path, sql_statement):
    engine = sa.create_engine(db_path)
    df = pd.read_sql_query(sql_statement, engine)
    return df



def generate_plot(plot_type, df, plot_path, xlabel, ylabel, title):
    if plot_type == 'scatter':
        ax = df.plot.scatter(x='x', y='y', s=3)
    elif plot_type== 'box':
        ax = df.boxplot(column='y', by='x')
    else:
        raise Exception()
    ax.set(xlabel=xlabel, ylabel=ylabel, title=title)
    ax.get_figure().savefig(plot_path)