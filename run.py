from utils import *
from constants import *



def run_main(input_data, run_data, session):
    db_path = make_db_path(username=session.username, password=session.password, host=DB_HOST, port=DB_PORT)

    if 'input_mode' in input_data:
        run_data['input_mode'] = input_data['input_mode']
    if 'limit_readability' in input_data:
        run_data['limit_readability'] = input_data['limit_readability']
    if 'max_readability' in input_data:
        run_data['max_readability'] = input_data['max_readability']
    if 'plot_type' in input_data:
        run_data['plot_type'] = input_data['plot_type']

    try:
        run_data['schema_list'] = get_schema_list(db_path=db_path)
        if 'schema' in input_data and input_data['schema']:
            run_data['schema'] = input_data['schema']
            run_data['table_list'] = get_table_list(db_path=db_path, schema=input_data['schema'])
            if 'table' in input_data and input_data['table']:
                run_data['table'] = input_data['table']
                run_data['column_list'] = get_column_list(db_path=db_path, schema=input_data['schema'], table=input_data['table'])
                if 'index_column' in input_data and input_data['index_column']:
                    run_data['index_column'] = input_data['index_column']
                if 'plot_column' in input_data and input_data['plot_column']:
                    run_data['plot_column'] = input_data['plot_column']
    except Exception as e:
        pass

    if 'submitted' in input_data and input_data['submitted'] == 'True':
        try:
            if run_data['input_mode'] == 'UI':
                if run_data['limit_readability'] == 'True':
                    max_readability = float(run_data['max_readability'])
                elif run_data['limit_readability'] == 'False':
                    max_readability = DEFAULT_MAX_READABILITY
                else:
                    raise Exception()
                sql_statement = read_formatted_file(
                    file_path=GET_XY_SQL_FILE_PATH,
                    replacements={
                        'schema':run_data['schema'],
                        'table':run_data['table'],
                        'index_column':run_data['index_column'],
                        'plot_column':run_data['plot_column'],
                        'max_readability':str(max_readability)
                    }
                )
            elif run_data['input_mode'] == 'SQL':
                sql_statement = bytes_to_string(bytes_data=input_data['sql_file'])
            else:
                raise Exception()
            df = execute_sql_statement(db_path=db_path, sql_statement=sql_statement)
            plot_path = PLOT_PATH.format(session.session_id)
            generate_plot(
                plot_type=run_data['plot_type'],
                df=df,
                plot_path=plot_path,
                xlabel='Plot Column',
                ylabel='Readability Score',
                title='Readability Score over Plot Column'
            )
            run_data['submitted'] = 'True'
            run_data['plot_path'] = plot_path

        except Exception as e:
            run_data['status_messages'] = [{'status':'failure', 'message':'Failure! Cannot process input information.'}]



def run_login(input_data, run_data, session):
    try:
        username = input_data['username']
        password = input_data['password']
        db_path = make_db_path(username=username, password=password, host=DB_HOST, port=DB_PORT)
        test_db_connection(db_path=db_path)
        run_data['logged_in'] = True
        session.logged_in = True
        session.username = username
        session.password = password
    except Exception as e:
        run_data['logged_in'] = False
        session.logged_in = False
        session.username = ''
        session.password = ''
        run_data['status_messages'] = [{'status':'failure', 'message':'Failure! Cannot connect to the database with given username and password.'}]



def run_logout(input_data, run_data, session):
    try:
        plot_path = PLOT_PATH.format(session.session_id)
        remove_file(file_path=plot_path)
    except Exception as e:
        pass
    session.kill()