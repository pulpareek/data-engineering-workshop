-- ============================================================================
-- QA GATE (qa target only) | FAIL UPDATE: the promotion stops if any fails
-- Included by resources/iops_quality.pipeline.yml only for the qa target.
-- ============================================================================
CREATE OR REFRESH MATERIALIZED VIEW qa_gate_results (
  CONSTRAINT zero_data_loss     EXPECT (lost_rows = 0)            ON VIOLATION FAIL UPDATE,
  CONSTRAINT unique_case_grain  EXPECT (duplicate_cases = 0)      ON VIOLATION FAIL UPDATE,
  CONSTRAINT unique_change_grain EXPECT (duplicate_changes = 0)   ON VIOLATION FAIL UPDATE,
  CONSTRAINT gold_not_empty     EXPECT (gold_cases > 0)           ON VIOLATION FAIL UPDATE
)
COMMENT "Release gate evaluated on every QA update."
TBLPROPERTIES ('quality' = 'dq')
AS SELECT
  (SELECT sum(abs(bronze_rows - clean_rows - quarantine_rows)) FROM dq_reconciliation) AS lost_rows,
  (SELECT count(*) - count(DISTINCT source_case_id) FROM gold_deviation_lifecycle)      AS duplicate_cases,
  (SELECT count(*) - count(DISTINCT source_change_id) FROM gold_change_control_cycle_time) AS duplicate_changes,
  (SELECT count(*) FROM gold_deviation_lifecycle)                                       AS gold_cases;
