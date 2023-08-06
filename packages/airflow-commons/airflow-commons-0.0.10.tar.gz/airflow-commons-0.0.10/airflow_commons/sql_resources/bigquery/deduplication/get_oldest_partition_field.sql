SELECT
  MIN({target_partition_field}) AS oldest_value
FROM
  `{project_id}.{source_dataset}.{source_table}`
WHERE
    {source_partition_field} BETWEEN '{start_date}'
    AND '{end_date}' AND {target_partition_field} >= '{oldest_allowable_target_partition}';