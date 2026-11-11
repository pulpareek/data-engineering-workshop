-- ============================================================================
-- BRONZE | bronze_deviation_event
-- Grain  : one row per source record, exactly as it arrived (append-only)
-- Pattern: the SAME Auto Loader block for every feed; only the folder and
--          the schema (the data contract) change. Every column is STRING:
--          Bronze keeps values exactly as sent, Silver casts them.
-- ============================================================================
CREATE OR REFRESH STREAMING TABLE bronze_deviation_event
COMMENT "Raw deviation status events from the QMS feed (synthetic)."
TBLPROPERTIES (
  'quality' = 'bronze',
  'pipelines.reset.allowed' = 'false'   -- protect raw history from accidental full refresh
)
AS SELECT
  *,                                                   -- every source column + _rescued_data
  _metadata.file_path              AS source_file,     -- lineage: which file
  _metadata.file_modification_time AS source_file_modified_at,
  current_timestamp()              AS ingested_at      -- lineage: when we read it
FROM STREAM read_files(
  :landing_root || '/deviation_event_feed',
  format            => 'csv',
  header            => true,                           -- columns matched by NAME
  schema            => '
    source_case_id    STRING,
    site_code         STRING,
    lot_id            STRING,
    event_code        STRING,
    status_code       STRING,
    reported_at       STRING,
    target_due_at     STRING,
    resolved_at       STRING,
    source_updated_at STRING,
    description       STRING
  ',                                -- the Bronze data contract: names, all STRING (Silver casts)
  rescuedDataColumn => '_rescued_data'   -- anything outside the contract lands here
);
