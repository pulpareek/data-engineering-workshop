-- ============================================================================
-- SILVER | deviation events
-- Grain  : one row per valid status event (a case has many events)
-- Rule of the layer: conform + validate. Never aggregate here.
-- ============================================================================

-- 1) Prepare once: cast, normalize, and list every rule a row breaks.
CREATE TEMPORARY VIEW deviation_event_prepared AS
SELECT
  source_case_id,
  site_code,
  lot_id,
  event_code,
  upper(regexp_replace(trim(status_code), '[ -]+', '_')) AS status_code,   -- ' Open ' -> OPEN
  status_code                                             AS status_code_raw,
  reported_at,
  target_due_at,
  resolved_at,
  source_updated_at,
  description,
  upper(trim(_rescued_data:severity::string))            AS severity,       -- promoted from rescued data (arrives in batch 3)
  source_file,
  ingested_at,
  filter(array(
    CASE WHEN source_case_id IS NULL THEN 'missing source_case_id' END,
    CASE WHEN site_code IS NULL      THEN 'missing site_code' END,
    CASE WHEN reported_at IS NULL    THEN 'missing reported_at' END,
    CASE WHEN upper(regexp_replace(trim(status_code), '[ -]+', '_'))
              NOT IN ('OPEN','IN_INVESTIGATION','PENDING_CAPA','CLOSED','CANCELLED')
              OR status_code IS NULL THEN 'unknown status_code' END,
    CASE WHEN resolved_at < reported_at   THEN 'resolved_at before reported_at' END,
    CASE WHEN target_due_at < reported_at THEN 'target_due_at before reported_at' END,
    CASE WHEN upper(trim(_rescued_data:severity::string)) NOT IN ('MINOR','MAJOR','CRITICAL')
         THEN 'invalid severity' END
  ), x -> x IS NOT NULL) AS dq_issues
FROM STREAM(bronze_deviation_event);

-- 2) Clean path: one named expectation per rule -> per-rule metrics in the pipeline UI.
CREATE OR REFRESH STREAMING TABLE silver_deviation_event (
  CONSTRAINT has_case_id      EXPECT (source_case_id IS NOT NULL)                          ON VIOLATION DROP ROW,
  CONSTRAINT has_site_code    EXPECT (site_code IS NOT NULL)                               ON VIOLATION DROP ROW,
  CONSTRAINT has_reported_at  EXPECT (reported_at IS NOT NULL)                             ON VIOLATION DROP ROW,
  CONSTRAINT known_status     EXPECT (status_code IN ('OPEN','IN_INVESTIGATION','PENDING_CAPA','CLOSED','CANCELLED')) ON VIOLATION DROP ROW,
  CONSTRAINT resolved_after_reported EXPECT (resolved_at IS NULL OR resolved_at >= reported_at)     ON VIOLATION DROP ROW,
  CONSTRAINT due_after_reported      EXPECT (target_due_at IS NULL OR target_due_at >= reported_at) ON VIOLATION DROP ROW,
  -- NULL-tolerant: older files have no severity at all, and that is fine.
  CONSTRAINT valid_severity_when_present EXPECT (severity IS NULL OR severity IN ('MINOR','MAJOR','CRITICAL')) ON VIOLATION DROP ROW
)
COMMENT "Validated deviation status events. Grain: one row per event."
TBLPROPERTIES ('quality' = 'silver')
AS SELECT * EXCEPT (dq_issues) FROM STREAM(deviation_event_prepared);

-- 3) Quarantine path: the inverse. Nothing is lost: bronze = clean + quarantine.
CREATE OR REFRESH STREAMING TABLE silver_deviation_event_quarantine
COMMENT "Deviation events that failed at least one rule, with the reasons."
TBLPROPERTIES ('quality' = 'quarantine')
AS SELECT *, array_join(dq_issues, '; ') AS quarantine_reason
FROM STREAM(deviation_event_prepared)
WHERE size(dq_issues) > 0;
