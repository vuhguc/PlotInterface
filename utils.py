import sqlalchemy as sa
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt



def make_db_path(host, port, username, password):
    return 'mysql+pymysql://{}:{}@{}:{}'.format(username, password, host, port)



def test_db_connection(db_path):
    engine = sa.create_engine(db_path)
    con = engine.connect()
    con.close()



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



def read_formatted_sql_file(file_path, replacements):
    with open(file_path, 'r') as sql_file:
        sql_statement = sql_file.read()
        for wild_card in replacements:
            sql_statement = sql_statement.replace('{{%{}}}'.format(wild_card), replacements[wild_card])
        return sql_statement



def execute_sql_statement(db_path, sql_statement):
    engine = sa.create_engine(db_path)
    df = pd.read_sql_query(sql_statement, engine)
    return df



def generate_plot(df, plot_path, xlabel, ylabel, title):
    fig, ax = plt.subplots()
    ax.scatter(df['x'], df['y'], marker='.')
    ax.set(xlabel=xlabel, ylabel=ylabel, title=title)
    fig.savefig(plot_path)