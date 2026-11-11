# Databricks notebook source
# MAGIC %md-sandbox
# MAGIC <div class="cw">
# MAGIC <style>
# MAGIC .cw { font-family: sans-serif; max-width: 1100px; margin: 0 auto; color: #0b2026; } .cw * { box-sizing: border-box; }
# MAGIC .ds-banner { display: flex; align-items: center; gap: 20px; width: 100%; border-radius: 10px; padding: 24px 28px; background: var(--bnr-bg); border-left: 8px solid var(--bnr-accent); box-shadow: 0 2px 10px rgba(27,49,57,0.08); }
# MAGIC .ds-banner-icon { width: 60px; height: 60px; border-radius: 50%; flex-shrink: 0; background: var(--bnr-accent); color: var(--bnr-icon-fg); font-size: 30pt; font-weight: 700; line-height: 1; display: flex; align-items: center; justify-content: center; }
# MAGIC .ds-banner-title { font-size: 22pt; font-weight: 700; color: var(--bnr-title); line-height: 1.2; margin-bottom: 4px; }
# MAGIC .ds-banner-tagline { font-size: 15pt; color: var(--bnr-tagline); line-height: 1.4; }
# MAGIC .ds-banner.info { --bnr-bg: #1B5162; --bnr-accent: #4299E0; --bnr-icon-fg: #FFFFFF; --bnr-title: #FFFFFF; --bnr-tagline: #F9F7F4; }
# MAGIC .ds-banner.caution { --bnr-bg: rgba(255,171,0,0.12); --bnr-accent: #FFAB00; --bnr-icon-fg: #0b2026; --bnr-title: #0b2026; --bnr-tagline: #5E7077; }
# MAGIC .ds-banner.danger { --bnr-bg: rgba(255,95,70,0.10); --bnr-accent: #FF5F46; --bnr-icon-fg: #FFFFFF; --bnr-title: #98102A; --bnr-tagline: #5E7077; }
# MAGIC </style>
# MAGIC <div class="ds-banner info"><div class="ds-banner-icon">6</div><div><div class="ds-banner-title">Lab 06 &middot; Gold: business outputs</div><div class="ds-banner-tagline">15 minutes &middot; grain first, then the dataset type</div></div></div>
# MAGIC </div>
# MAGIC <div style="height:18px"></div>
# MAGIC <div class="cw">
# MAGIC <style>
# MAGIC .cw { font-family: sans-serif; max-width: 1100px; margin: 0 auto; color: #0b2026; } .cw * { box-sizing: border-box; }
# MAGIC .flow-grid { display: grid; gap: 0; align-items: stretch; }
# MAGIC .flow-step { background: #F9F7F4; border: 3px solid var(--accent, #4299E0); border-radius: 10px; padding: 16px 12px; box-shadow: 0 2px 8px rgba(27,49,57,0.08); text-align: center; min-width: 0; }
# MAGIC .flow-num { font-size: 26pt; font-weight: 800; color: var(--accent, #4299E0); line-height: 1; margin-bottom: 8px; }
# MAGIC .flow-label { font-size: 14pt; font-weight: 600; color: #0b2026; line-height: 1.35; }
# MAGIC .flow-arrow { display: flex; align-items: center; justify-content: center; color: #618794; font-size: 22pt; line-height: 1; padding: 0 6px; }
# MAGIC .flow-step.dim { background: #EEEDE9; border-color: #C2C2C2; box-shadow: none; opacity: 0.7; }
# MAGIC .flow-step.dim .flow-num { color: #90A5B1; } .flow-step.dim .flow-label { color: #5A6F77; } .flow-arrow.dim { color: #C2C2C2; }
# MAGIC </style>
# MAGIC <div class="flow-grid" style="grid-template-columns:1fr auto 1fr auto 1fr auto 1fr auto 1fr auto 1fr;"><div class="flow-step dim" style="--accent:#4299E0;"><div class="flow-num">1</div><div class="flow-label">Land files</div></div><div class="flow-arrow dim">&rarr;</div><div class="flow-step dim" style="--accent:#00A972;"><div class="flow-num">2</div><div class="flow-label">Bronze</div></div><div class="flow-arrow dim">&rarr;</div><div class="flow-step dim" style="--accent:#FFAB00;"><div class="flow-num">3</div><div class="flow-label">Silver</div></div><div class="flow-arrow">&rarr;</div><div class="flow-step" style="--accent:#FF5F46;"><div class="flow-num">4</div><div class="flow-label">Gold</div></div><div class="flow-arrow dim">&rarr;</div><div class="flow-step dim" style="--accent:#98102A;"><div class="flow-num">5</div><div class="flow-label">New batch</div></div><div class="flow-arrow dim">&rarr;</div><div class="flow-step dim" style="--accent:#1B5162;"><div class="flow-num">6</div><div class="flow-label">Promote</div></div></div>
# MAGIC </div>

# COMMAND ----------

%run ./Includes/Classroom-Setup

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div class="cw">
# MAGIC <style>
# MAGIC .cw { font-family: sans-serif; max-width: 1100px; margin: 0 auto; color: #0b2026; } .cw * { box-sizing: border-box; }
# MAGIC .ds-row { display: flex; gap: 24px; align-items: stretch; flex-wrap: wrap; }
# MAGIC .ds-row > * { flex: 1; min-width: 240px; }
# MAGIC .ds-card { background: #F9F7F4; border-radius: 8px; box-shadow: 0 2px 8px rgba(27,49,57,0.06); padding: 20px; border-top: 8px solid var(--accent, #4299E0); }
# MAGIC .blue{--accent:#4299E0;} .green{--accent:#00A972;} .coral{--accent:#FF5F46;} .amber{--accent:#FFAB00;} .red{--accent:#98102A;}
# MAGIC .ds-card-title { font-size: 18pt; font-weight: 700; line-height: 1.25; margin: 0 0 8px; }
# MAGIC .ds-card-text { font-size: 14pt; color: #5E7077; line-height: 1.55; margin: 0; }
# MAGIC .ds-card ul, .ds-card ol { margin: 8px 0 0; padding-left: 20px; font-size: 14pt; line-height: 1.55; color: #0b2026; }
# MAGIC .ds-card li { margin-bottom: 10px; } .ds-card li:last-child { margin-bottom: 0; }
# MAGIC .tc { text-align: center; }
# MAGIC .ds-card-label { font-size: 14pt; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: var(--accent); margin-bottom: 4px; }
# MAGIC .ds-card-para { font-size: 14pt; color: #0b2026; line-height: 1.55; margin: 0; }
# MAGIC .ds-stat { font-size: 26pt; font-weight: 800; color: var(--accent); line-height: 1.1; }
# MAGIC .ds-stat-label { font-size: 14pt; color: #5E7077; margin-top: 6px; }
# MAGIC .dd-head { font-size: 20pt; font-weight: 700; margin: 4px 0 12px; color: var(--accent); }
# MAGIC .ds-card code, .ds-callout code { background: #EEEDE9; padding: 1px 5px; border-radius: 4px; font-size: 14pt; }
# MAGIC </style>
# MAGIC <div class="ds-row"><div class="ds-card green"><div class="ds-card-label">You build &middot; site x test x day</div><div class="ds-card-title">gold_inspection_quality</div><ul><li>pass rate, OOS count</li><li>+ <code>gold_oos_events</code>: 1 row per OOS result</li></ul></div><div class="ds-card coral"><div class="ds-card-label">Prebuilt &middot; 1 row per case</div><div class="ds-card-title">gold_deviation_lifecycle</div><ul><li>current status, age, overdue</li><li>action summary joined without fan-out</li></ul></div><div class="ds-card blue"><div class="ds-card-label">Prebuilt &middot; 1 row per change</div><div class="ds-card-title">gold_change_control_cycle_time</div><ul><li>submit &rarr; approve &rarr; close days</li></ul></div></div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div class="cw">
# MAGIC <style>
# MAGIC .cw { font-family: sans-serif; max-width: 1100px; margin: 0 auto; color: #0b2026; } .cw * { box-sizing: border-box; }
# MAGIC .ds-row { display: flex; gap: 24px; align-items: stretch; flex-wrap: wrap; }
# MAGIC .ds-row > * { flex: 1; min-width: 240px; }
# MAGIC .ds-card { background: #F9F7F4; border-radius: 8px; box-shadow: 0 2px 8px rgba(27,49,57,0.06); padding: 20px; border-top: 8px solid var(--accent, #4299E0); }
# MAGIC .blue{--accent:#4299E0;} .green{--accent:#00A972;} .coral{--accent:#FF5F46;} .amber{--accent:#FFAB00;} .red{--accent:#98102A;}
# MAGIC .ds-card-title { font-size: 18pt; font-weight: 700; line-height: 1.25; margin: 0 0 8px; }
# MAGIC .ds-card-text { font-size: 14pt; color: #5E7077; line-height: 1.55; margin: 0; }
# MAGIC .ds-card ul, .ds-card ol { margin: 8px 0 0; padding-left: 20px; font-size: 14pt; line-height: 1.55; color: #0b2026; }
# MAGIC .ds-card li { margin-bottom: 10px; } .ds-card li:last-child { margin-bottom: 0; }
# MAGIC .tc { text-align: center; }
# MAGIC .ds-card-label { font-size: 14pt; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: var(--accent); margin-bottom: 4px; }
# MAGIC .ds-card-para { font-size: 14pt; color: #0b2026; line-height: 1.55; margin: 0; }
# MAGIC .ds-stat { font-size: 26pt; font-weight: 800; color: var(--accent); line-height: 1.1; }
# MAGIC .ds-stat-label { font-size: 14pt; color: #5E7077; margin-top: 6px; }
# MAGIC .dd-head { font-size: 20pt; font-weight: 700; margin: 4px 0 12px; color: var(--accent); }
# MAGIC .ds-card code, .ds-callout code { background: #EEEDE9; padding: 1px 5px; border-radius: 4px; font-size: 14pt; }
# MAGIC </style>
# MAGIC <div class="ds-row"><div class="ds-card green"><div class="ds-card-title">Choose a materialized view when</div><ul><li>the answer is a current state or an aggregate</li><li>late or corrected data must change old rows</li></ul></div><div class="ds-card blue"><div class="ds-card-title">Choose a streaming table when</div><ul><li>each input row produces output rows once</li><li>you want an append-only event log (OOS alerts)</li></ul></div></div>
# MAGIC </div>
# MAGIC
# MAGIC ##### EXPAND FOR ADDITIONAL NOTES
# MAGIC
# MAGIC <details>
# MAGIC
# MAGIC Ask each participant to justify the type for both datasets in `gold/gold_inspection_quality.sql` *before* running. The fill-in deliberately says `STREAMING TABLE | MATERIALIZED VIEW`.
# MAGIC - `gold_inspection_quality` is an aggregate: MV.
# MAGIC - `gold_oos_events` turns each new OOS result into one row, enriched once with lot dates (stream-snapshot join): ST.
# MAGIC
# MAGIC </details>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div class="cw">
# MAGIC <style>
# MAGIC .cw { font-family: sans-serif; max-width: 1100px; margin: 0 auto; color: #0b2026; } .cw * { box-sizing: border-box; }
# MAGIC .ds-callout { border-left: 6px solid var(--accent, #1B5162); border-radius: 8px; padding: 18px 24px; background: var(--tint, #F8F9FC); box-shadow: 0 2px 8px rgba(27,49,57,0.06); font-size: 14pt; line-height: 1.55; color: #0b2026; }
# MAGIC .ds-eyebrow { font-size: 14pt; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: var(--accent, #1B5162); margin-bottom: 6px; }
# MAGIC .ds-callout ul { margin: 0; padding-left: 20px; font-size: 14pt; line-height: 1.55; color: #0b2026; }
# MAGIC .ds-callout li { margin-bottom: 10px; } .ds-callout li:last-child { margin-bottom: 0; }
# MAGIC .ds-callout.info { --accent:#1B5162; --tint:#F8F9FC; }
# MAGIC .ds-callout.caution { --accent:#FFAB00; --tint:rgba(255,171,0,0.12); }
# MAGIC .ds-callout.danger { --accent:#FF5F46; --tint:rgba(255,95,70,0.10); }
# MAGIC .ds-callout.success { --accent:#00A972; --tint:rgba(0,169,114,0.10); }
# MAGIC .ds-callout.row { display: flex; align-items: center; gap: 16px; }
# MAGIC .ds-callout-icon { width: 44px; height: 44px; border-radius: 50%; background: var(--accent); color: #fff; font-size: 22pt; font-weight: 700; line-height: 1; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
# MAGIC .ds-callout.caution .ds-callout-icon { color: #0b2026; }
# MAGIC .ds-callout-title { font-size: 16pt; font-weight: 700; color: #0b2026; margin-bottom: 10px; line-height: 1.3; }
# MAGIC </style>
# MAGIC <div class="ds-callout info"><div class="ds-eyebrow">Need help?</div><div>Stuck on syntax? Open <strong>Genie Code</strong> (the assistant panel) and ask, for example, <em>&quot;convert this CREATE TABLE into a streaming table that reads with Auto Loader&quot;</em>. Then compare with the CODE ANSWER.</div></div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC Write your code in the pipeline editor. Stuck? Expand a CODE ANSWER below, compare, then continue.

# COMMAND ----------

# MAGIC %md
# MAGIC <details><summary><strong>CODE ANSWER: gold_inspection_quality.sql</strong> (try first, then expand)</summary>
# MAGIC
# MAGIC ```sql
# MAGIC -- ============================================================================
# MAGIC -- GOLD | inspection quality
# MAGIC --   gold_inspection_quality : MV, grain site x test x day   (aggregate -> recompute)
# MAGIC --   gold_oos_events         : ST, grain one row per OOS result (event -> append)
# MAGIC -- Same source, two shapes: this is the streaming-table vs materialized-view choice.
# MAGIC -- ============================================================================
# MAGIC CREATE OR REFRESH MATERIALIZED VIEW gold_inspection_quality
# MAGIC COMMENT "QC pass rate and out-of-spec counts. Grain: site x test x measured date. Synthetic training data."
# MAGIC TBLPROPERTIES ('quality' = 'gold')
# MAGIC AS SELECT
# MAGIC   site_code,
# MAGIC   test_code,
# MAGIC   to_date(measured_at)                                    AS measured_date,
# MAGIC   count(*)                                                AS total_results,
# MAGIC   count_if(is_oos)                                        AS oos_results,
# MAGIC   round(100 * count_if(NOT is_oos) / count(*), 2)         AS pass_rate_pct
# MAGIC FROM silver_inspection_result
# MAGIC GROUP BY ALL;
# MAGIC
# MAGIC -- Stream-snapshot join: each NEW result is enriched with the batch record as it is now.
# MAGIC CREATE OR REFRESH STREAMING TABLE gold_oos_events
# MAGIC COMMENT "Every out-of-spec QC result, enriched with product and lot dates. Grain: one row per OOS result. Synthetic training data."
# MAGIC TBLPROPERTIES ('quality' = 'gold')
# MAGIC AS SELECT
# MAGIC   i.source_sample_id,
# MAGIC   i.lot_id,
# MAGIC   i.site_code,
# MAGIC   b.product_code,
# MAGIC   i.test_code,
# MAGIC   i.measured_value,
# MAGIC   i.lower_limit,
# MAGIC   i.upper_limit,
# MAGIC   i.measured_at,
# MAGIC   b.ended_at          AS lot_ended_at,
# MAGIC   i.source_file
# MAGIC FROM STREAM(silver_inspection_result) i
# MAGIC LEFT JOIN silver_batch_record b ON i.lot_id = b.lot_id
# MAGIC WHERE i.is_oos;
# MAGIC ```
# MAGIC
# MAGIC </details>

# COMMAND ----------

# MAGIC %md
# MAGIC ### Checkpoint after batch 1: run the pipeline first
# MAGIC Run the pipeline (**Run pipeline**, not full refresh). When the update finishes, run the next cell: every row should show a check mark.

# COMMAND ----------

checkpoint(run=1, layer='gold')

# COMMAND ----------

# MAGIC %md
# MAGIC ### Explore: the questions QA actually asks

# COMMAND ----------

display(spark.sql(f'''SELECT site_code, test_code, sum(total_results) AS results, sum(oos_results) AS oos,
       round(100 * sum(oos_results) / sum(total_results), 1) AS oos_rate_pct
FROM {FQ}.gold_inspection_quality GROUP BY ALL HAVING oos > 0 ORDER BY oos DESC'''))

# COMMAND ----------

# MAGIC %md
# MAGIC ### If you finish early: why the prebuilt deviation lifecycle aggregates actions first

# COMMAND ----------

display(spark.sql(f'''
WITH cases AS (SELECT DISTINCT source_case_id FROM {FQ}.silver_deviation_event)
SELECT
  (SELECT count(*) FROM cases)                                                     AS cases,
  (SELECT count(*) FROM cases c JOIN {FQ}.silver_corrective_action_event a USING (source_case_id)) AS naive_join_rows,
  (SELECT count(*) FROM cases c LEFT JOIN (SELECT source_case_id, count(*) n FROM {FQ}.silver_corrective_action GROUP BY 1) a
     USING (source_case_id))                                                       AS pre_aggregated_rows
'''))

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div class="cw">
# MAGIC <style>
# MAGIC .cw { font-family: sans-serif; max-width: 1100px; margin: 0 auto; color: #0b2026; } .cw * { box-sizing: border-box; }
# MAGIC .ds-row { display: flex; gap: 24px; align-items: stretch; flex-wrap: wrap; }
# MAGIC .ds-row > * { flex: 1; min-width: 240px; }
# MAGIC .ds-card { background: #F9F7F4; border-radius: 8px; box-shadow: 0 2px 8px rgba(27,49,57,0.06); padding: 20px; border-top: 8px solid var(--accent, #4299E0); }
# MAGIC .blue{--accent:#4299E0;} .green{--accent:#00A972;} .coral{--accent:#FF5F46;} .amber{--accent:#FFAB00;} .red{--accent:#98102A;}
# MAGIC .ds-card-title { font-size: 18pt; font-weight: 700; line-height: 1.25; margin: 0 0 8px; }
# MAGIC .ds-card-text { font-size: 14pt; color: #5E7077; line-height: 1.55; margin: 0; }
# MAGIC .ds-card ul, .ds-card ol { margin: 8px 0 0; padding-left: 20px; font-size: 14pt; line-height: 1.55; color: #0b2026; }
# MAGIC .ds-card li { margin-bottom: 10px; } .ds-card li:last-child { margin-bottom: 0; }
# MAGIC .tc { text-align: center; }
# MAGIC .ds-card-label { font-size: 14pt; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: var(--accent); margin-bottom: 4px; }
# MAGIC .ds-card-para { font-size: 14pt; color: #0b2026; line-height: 1.55; margin: 0; }
# MAGIC .ds-stat { font-size: 26pt; font-weight: 800; color: var(--accent); line-height: 1.1; }
# MAGIC .ds-stat-label { font-size: 14pt; color: #5E7077; margin-top: 6px; }
# MAGIC .dd-head { font-size: 20pt; font-weight: 700; margin: 4px 0 12px; color: var(--accent); }
# MAGIC .ds-card code, .ds-callout code { background: #EEEDE9; padding: 1px 5px; border-radius: 4px; font-size: 14pt; }
# MAGIC </style>
# MAGIC <div class="ds-row"><div class="ds-card green"><div class="dd-head">&check; DO</div><ul><li>Aggregate actions to <strong>one row per case</strong>, then join.</li><li>Check: Gold row count = number of cases.</li><li>Write the grain in the table COMMENT.</li></ul></div><div class="ds-card coral"><div class="dd-head">&times; DON'T</div><ul><li>Join raw actions to events and then <code>count(DISTINCT)</code> your way out.</li><li>Average a metric after a fan-out join.</li><li>Let a dashboard discover the grain for you.</li></ul></div></div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ## Optional: if you have time
# MAGIC The core lab ends above. Build the two prebuilt Gold tables yourself, or add a rollup. The pipeline already runs the prebuilt version, so skipping this costs nothing.
# MAGIC
# MAGIC 1. Deviation lifecycle: <code>pipeline_files_optional/gold/gold_deviation_lifecycle.sql</code>. Grain keys, dataset type, the overdue rule.
# MAGIC 2. Change-control cycle time: <code>pipeline_files_optional/gold/gold_change_control_cycle_time.sql</code>. Latest-snapshot key and durations.
# MAGIC 3. Rollup: add the site x month view below to the cycle-time file. We left it out of the core pipeline because a dashboard or metric view can do the same.

# COMMAND ----------

# MAGIC %md
# MAGIC <details><summary><strong>CODE ANSWER: gold_deviation_lifecycle.sql</strong> (try first, then expand)</summary>
# MAGIC
# MAGIC ```sql
# MAGIC -- ============================================================================
# MAGIC -- GOLD | deviation lifecycle  (materialized view)
# MAGIC -- Grain : one row per deviation case
# MAGIC -- Why MV: "current status" needs every event for a case, and late events can
# MAGIC --         arrive for old cases -> the answer must be recomputed, not appended.
# MAGIC -- Fan-out guard: actions are aggregated to one row per case BEFORE the join.
# MAGIC -- ============================================================================
# MAGIC CREATE OR REFRESH MATERIALIZED VIEW gold_deviation_lifecycle
# MAGIC COMMENT "Current lifecycle of each deviation with its corrective-action summary. Grain: one row per case. Synthetic training data, not a quality decision."
# MAGIC TBLPROPERTIES ('quality' = 'gold')
# MAGIC AS
# MAGIC WITH latest_event AS (          -- latest status per case, by source time (not arrival time)
# MAGIC   SELECT *
# MAGIC   FROM silver_deviation_event
# MAGIC   QUALIFY row_number() OVER (PARTITION BY source_case_id ORDER BY source_updated_at DESC) = 1
# MAGIC ),
# MAGIC case_facts AS (
# MAGIC   SELECT
# MAGIC     source_case_id,
# MAGIC     min(reported_at)                                               AS reported_at,
# MAGIC     max_by(severity, source_updated_at) FILTER (WHERE severity IS NOT NULL) AS severity,
# MAGIC     count(*)                                                       AS event_count
# MAGIC   FROM silver_deviation_event
# MAGIC   GROUP BY source_case_id
# MAGIC ),
# MAGIC action_summary AS (             -- 1 row per case: no fan-out when joined
# MAGIC   SELECT
# MAGIC     source_case_id,
# MAGIC     count(*)                                                AS action_count,
# MAGIC     count_if(action_status IN ('OPEN', 'IN_PROGRESS'))      AS open_action_count
# MAGIC   FROM silver_corrective_action
# MAGIC   GROUP BY source_case_id
# MAGIC )
# MAGIC SELECT
# MAGIC   e.source_case_id,
# MAGIC   e.site_code,
# MAGIC   e.lot_id,
# MAGIC   e.event_code,
# MAGIC   e.status_code                                             AS current_status,
# MAGIC   f.severity,
# MAGIC   f.reported_at,
# MAGIC   e.target_due_at,
# MAGIC   e.resolved_at,
# MAGIC   e.status_code NOT IN ('CLOSED', 'CANCELLED')              AS is_open,
# MAGIC   e.status_code NOT IN ('CLOSED', 'CANCELLED')
# MAGIC     AND to_date(:as_of_date) > to_date(e.target_due_at)      AS is_overdue,
# MAGIC   datediff(
# MAGIC     CASE WHEN e.status_code IN ('CLOSED', 'CANCELLED') AND e.resolved_at IS NOT NULL
# MAGIC          THEN to_date(e.resolved_at) ELSE to_date(:as_of_date) END,
# MAGIC     to_date(f.reported_at))                                 AS age_days,
# MAGIC   f.event_count,
# MAGIC   coalesce(a.action_count, 0)                               AS action_count,
# MAGIC   coalesce(a.open_action_count, 0)                          AS open_action_count,
# MAGIC   e.description,
# MAGIC   e.source_file                                             AS latest_source_file,
# MAGIC   to_date(:as_of_date)                                       AS as_of_date
# MAGIC FROM latest_event e
# MAGIC JOIN case_facts f USING (source_case_id)
# MAGIC LEFT JOIN action_summary a USING (source_case_id);
# MAGIC ```
# MAGIC
# MAGIC </details>

# COMMAND ----------

# MAGIC %md
# MAGIC <details><summary><strong>CODE ANSWER: gold_change_control_cycle_time.sql</strong> (try first, then expand)</summary>
# MAGIC
# MAGIC ```sql
# MAGIC -- ============================================================================
# MAGIC -- GOLD | change-control cycle time  (materialized view)
# MAGIC -- Grain : one row per change. Site or month rollups belong in the metric view
# MAGIC --         or the dashboard, not in another table.
# MAGIC -- ============================================================================
# MAGIC CREATE OR REFRESH MATERIALIZED VIEW gold_change_control_cycle_time
# MAGIC COMMENT "Latest state and milestone durations (days) for each change control. Grain: one row per change. Synthetic training data."
# MAGIC TBLPROPERTIES ('quality' = 'gold')
# MAGIC AS
# MAGIC WITH latest AS (
# MAGIC   SELECT *
# MAGIC   FROM silver_change_control
# MAGIC   QUALIFY row_number() OVER (PARTITION BY source_change_id ORDER BY source_file DESC) = 1
# MAGIC )
# MAGIC SELECT
# MAGIC   source_change_id,
# MAGIC   site_code,
# MAGIC   product_code,
# MAGIC   change_type,
# MAGIC   workflow_status,
# MAGIC   workflow_status IN ('SUBMITTED', 'APPROVED', 'IMPLEMENTED')       AS is_open,
# MAGIC   submitted_at,
# MAGIC   approved_at,
# MAGIC   effective_at,
# MAGIC   closed_at,
# MAGIC   datediff(to_date(approved_at),  to_date(submitted_at))            AS submit_to_approve_days,
# MAGIC   datediff(to_date(effective_at), to_date(approved_at))             AS approve_to_effective_days,
# MAGIC   datediff(to_date(closed_at),    to_date(submitted_at))            AS submit_to_close_days,
# MAGIC   datediff(coalesce(to_date(closed_at), to_date(:as_of_date)), to_date(submitted_at)) AS age_days,
# MAGIC   source_file                                                       AS latest_source_file,
# MAGIC   to_date(:as_of_date)                                               AS as_of_date
# MAGIC FROM latest;
# MAGIC ```
# MAGIC
# MAGIC </details>

# COMMAND ----------

# MAGIC %md
# MAGIC <details><summary><strong>CODE ANSWER: site x month rollup (optional table)</strong> (try first, then expand)</summary>
# MAGIC
# MAGIC ```sql
# MAGIC CREATE OR REFRESH MATERIALIZED VIEW gold_change_control_cycle_time_by_site_month
# MAGIC COMMENT "Change-control throughput and cycle time by site and submission month."
# MAGIC TBLPROPERTIES ('quality' = 'gold')
# MAGIC AS SELECT
# MAGIC   site_code,
# MAGIC   date_trunc('MONTH', submitted_at)            AS submit_month,
# MAGIC   count(*)                                     AS changes,
# MAGIC   count_if(is_open)                            AS open_changes,
# MAGIC   round(avg(submit_to_approve_days), 1)        AS avg_submit_to_approve_days,
# MAGIC   round(avg(submit_to_close_days), 1)          AS avg_submit_to_close_days
# MAGIC FROM gold_change_control_cycle_time
# MAGIC GROUP BY ALL;
# MAGIC ```
# MAGIC
# MAGIC </details>
