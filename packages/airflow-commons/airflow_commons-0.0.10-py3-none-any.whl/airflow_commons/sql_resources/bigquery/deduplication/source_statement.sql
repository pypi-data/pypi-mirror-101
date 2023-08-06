  SELECT
    latest_row.*
  FROM (
    SELECT
      ARRAY_AGG(t
      ORDER BY
        {order_by_clause}
      LIMIT
        1)[
    OFFSET
      (0)] AS latest_row
    FROM (
      SELECT
        *
      FROM
        `{project_id}.{source_dataset}.{source_table}`
      WHERE
          {source_where_statement} ) AS t
    GROUP BY
        {group_by_clause} )
