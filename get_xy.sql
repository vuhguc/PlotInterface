SELECT
    AVG(table_x.{%plot_column}) AS x,
    AVG((table_y.flesch_kincaid_grade + table_y.smog_index + table_y.gunning_fog) / 3) AS y
FROM {%schema}.{%table} AS table_x
INNER JOIN pubmed.scores_pbm AS table_y ON table_x.{%index_column} = table_y.ID
WHERE (table_y.flesch_kincaid_grade + table_y.smog_index + table_y.gunning_fog) / 3 <= {%max_readability}
GROUP BY table_y.ID