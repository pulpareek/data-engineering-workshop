-- ============================================================================
-- OPTIONAL (Lab 05) / S6 | AUTO CDC with history (SCD type 2)
-- Same changes as the core file silver/silver_corrective_action.sql, kept as history:
--   silver_corrective_action_history : every status change, with __START_AT / __END_AT
-- Current rows: WHERE __END_AT IS NULL (equals silver_corrective_action).
-- Reuses the temporary view corrective_action_changes from the core file.
-- ============================================================================
CREATE OR REFRESH STREAMING TABLE silver_corrective_action_history
COMMENT "Status history per corrective action via AUTO CDC (SCD type 2). Current rows: __END_AT IS NULL.";

CREATE FLOW corrective_action_history_flow AS AUTO CDC INTO silver_corrective_action_history
FROM STREAM(corrective_action_changes)
KEYS (source_action_id)
SEQUENCE BY STRUCT(source_file, status_rank)
COLUMNS * EXCEPT (status_rank)
STORED AS SCD TYPE 2
TRACK HISTORY ON action_status, completed_at;
