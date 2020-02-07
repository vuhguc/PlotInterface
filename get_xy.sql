SELECT
    table_x.{%plot_column} AS x,
    (CASE
        WHEN table_y.flesch_kincaid_grade > 16 THEN 16
        ELSE table_y.flesch_kincaid_grade
    END + CASE
        WHEN table_y.smog_index > 16 THEN 16
        ELSE table_y.smog_index
    END + CASE 
        WHEN table_y.gunning_fog > 16 THEN 16
        ELSE table_y.gunning_fog
    END) / 3 AS y
FROM {%schema}.{%table} AS table_x
INNER JOIN pubmed.scores_pbm AS table_y ON table_x.{%index_column} = table_y.ID;