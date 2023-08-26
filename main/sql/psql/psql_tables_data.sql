-- info about all tables
select
      table_catalog as db
    , table_schema as "schema"
    , table_name as "table"
    , string_agg(column_name, ';') as "columns" 
from information_schema.columns
where table_schema not in ('pg_catalog', 'information_schema')
group by 1, 2, 3;