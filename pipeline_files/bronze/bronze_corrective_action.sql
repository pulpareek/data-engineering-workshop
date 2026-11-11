-- ============================================================================
-- PREBUILT: finished and running. Read it, do not edit it.
-- Today you build the QC-results feed; this feed shows the same patterns, done.
-- ============================================================================
-- ============================================================================
-- BRONZE | bronze_corrective_action
-- Grain  : one row per source record, exactly as it arrived (append-only)
-- Pattern: the SAME Auto Loader block for every feed; only the folder and
--          the schema (the data contract) change. Every column is STRING:
--          Bronze keeps values exactly as sent, Silver casts them.
-- ============================================================================
CREATE OR REFRESH STREAMING TABLE bronze_corrective_action
COMMENT "Raw corrective/preventive action snapshots from the QMS feed (synthetic)."
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
  :landing_root || '/corrective_action_feed',
  format            => 'csv',
  header            => true,                           -- columns matched by NAME
  schema            => '
    source_action_id STRING,
    source_case_id   STRING,
    action_code      STRING,
    action_status    STRING,
    assigned_group   STRING,
    created_at       STRING,
    completed_at     STRING
  ',                                -- the Bronze data contract: names, all STRING (Silver casts)
  rescuedDataColumn => '_rescued_data'   -- anything outside the contract lands here
);
