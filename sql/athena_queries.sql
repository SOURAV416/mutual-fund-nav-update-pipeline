-- Create Athena external table
CREATE EXTERNAL TABLE IF NOT EXISTS mf_nav_processed (
  fund_id STRING,
  fund_name STRING,
  nav_value DOUBLE,
  aum DOUBLE,
  category STRING
)
PARTITIONED BY (nav_date STRING)
STORED AS PARQUET
LOCATION 's3://mf-nav-data/processed/';

-- Load partitions
MSCK REPAIR TABLE mf_nav_processed;

-- Fetch latest NAV values
SELECT fund_name, nav_value
FROM mf_nav_processed
WHERE nav_date = '2026-01-15'
ORDER BY nav_value DESC;
