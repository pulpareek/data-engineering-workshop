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
# MAGIC <div class="ds-banner info"><div class="ds-banner-icon">3</div><div><div class="ds-banner-title">Lab 03 &middot; Bronze with Auto Loader</div><div class="ds-banner-tagline">15 minutes &middot; run the worked feed, then build two Bronze tables</div></div></div>
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
# MAGIC <div class="flow-grid" style="grid-template-columns:1fr auto 1fr auto 1fr auto 1fr auto 1fr auto 1fr;"><div class="flow-step dim" style="--accent:#4299E0;"><div class="flow-num">1</div><div class="flow-label">Land files</div></div><div class="flow-arrow">&rarr;</div><div class="flow-step" style="--accent:#00A972;"><div class="flow-num">2</div><div class="flow-label">Bronze</div></div><div class="flow-arrow dim">&rarr;</div><div class="flow-step dim" style="--accent:#FFAB00;"><div class="flow-num">3</div><div class="flow-label">Silver</div></div><div class="flow-arrow dim">&rarr;</div><div class="flow-step dim" style="--accent:#FF5F46;"><div class="flow-num">4</div><div class="flow-label">Gold</div></div><div class="flow-arrow dim">&rarr;</div><div class="flow-step dim" style="--accent:#98102A;"><div class="flow-num">5</div><div class="flow-label">New batch</div></div><div class="flow-arrow dim">&rarr;</div><div class="flow-step dim" style="--accent:#1B5162;"><div class="flow-num">6</div><div class="flow-label">Promote</div></div></div>
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
# MAGIC <div class="ds-row"><div class="ds-card blue"><div class="ds-card-title">Goal</div><div class="ds-card-para">Two Bronze streaming tables, QC results and change controls, with lineage columns and a schema contract.</div></div><div class="ds-card green"><div class="ds-card-title">You change</div><div class="ds-card-para">Only three things per file: table name, folder, schema. Corrective actions are prebuilt with the same pattern.</div></div><div class="ds-card amber"><div class="ds-card-title">Done when</div><div class="ds-card-para">The checkpoint below is all green after batch 1.</div></div></div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ### A. Set up your pipeline (inside your bundle)
# MAGIC
# MAGIC You created the bundle `iops_quality` in notebook 00. Now give its pipeline the workshop files and settings.
# MAGIC
# MAGIC 1. **Move the workshop files into your pipeline.** In the workspace browser, open your Git folder &rarr; `pipeline_files/`. For each folder `bronze`, `silver`, `gold` and `checks`: kebab menu &rarr; **Move** &rarr; choose `iops_quality/src/iops_quality_etl/transformations/`. Then delete the template's two `sample_*.sql` files in `transformations/`. Leave `pipeline_files/qa/` where it is: you use it in Lab 09.
# MAGIC 2. **Add the pipeline settings.** Open `resources/iops_quality_etl.pipeline.yml` in your bundle:
# MAGIC    - paste the lines printed by `pipeline_settings()` right under `serverless: true` (same indent);
# MAGIC    - delete the template's `environment:` block (the 4 lines ending in `--editable ${workspace.file_path}`). It installs the bundle as a Python package, which this project does not have, and would fail once you add the Python file in Lab 05.
# MAGIC    - Save.
# MAGIC 3. **Deploy.** Open the bundle &rarr; **Open in editor** &rarr; **Deployments** panel (rocket icon) &rarr; **Deploy**.
# MAGIC 4. **Open the pipeline.** In the Deployments panel, under **Bundle resources**, select the pipeline. It opens in the **Lakeflow Pipelines Editor**.
# MAGIC
# MAGIC **What `:landing_root` means.** Every Bronze file reads `:landing_root || '/<feed>'`. `landing_root` is a **pipeline parameter**: its value is bound when the update starts, so the same SQL reads dev files in dev and QA files in QA. `:as_of_date` works the same way. If a parameter is missing, the update fails straight away instead of reading the wrong folder. Python files cannot read parameters, so the Python file you add in Lab 05 reads the same value from **Configuration** with `spark.conf.get("landing_root")`.
# MAGIC
# MAGIC ![Pipeline settings panel](./Includes/img/pipeline_configuration.png)
# MAGIC
# MAGIC *Pipeline settings: source code folder, default catalog and schema, serverless compute, and the `landing_root` parameter.*
# MAGIC
# MAGIC **Change settings in the YAML, not in the UI.** The bundle owns the pipeline: the next deploy puts the YAML values back.
# MAGIC
# MAGIC Explore the editor:
# MAGIC - The **Pipeline** tab lists the pipeline's files: `bronze/`, `silver/`, `gold/`, `checks/` (and `python/` after Lab 05).
# MAGIC - Write code in the file editor. **Run file** runs only the file you are editing; **Run pipeline** runs everything.
# MAGIC - The **pipeline graph** panel draws the tables from your queries; the bottom panel shows run details, data previews and expectation results.
# MAGIC
# MAGIC <img src="https://files.training.databricks.com/binder/prod_main/build-data-pipelines-with-apache-spark-declarative-pipelines-en_us-3.2.2/images/20261022T095913Z/Build%20Data%20Pipelines%20with%20Apache%20Spark%20Declarative%20Pipelines/Includes/images/creating-a-pipeline/lakeflow-editor-overview.png" alt="Lakeflow Pipelines Editor" width="900">
# MAGIC
# MAGIC [Lakeflow Pipelines Editor overview](https://docs.databricks.com/aws/en/ldp/multi-file-editor#overview-of-the-lakeflow-pipelines-editor-ui)

# COMMAND ----------

show_paths()

# COMMAND ----------

pipeline_settings()

# COMMAND ----------

# MAGIC %md
# MAGIC ### B. Warm-up: run the worked example (deviation feed)
# MAGIC The deviation feed is already complete in your pipeline. Land batch 1, then look at a file before ingesting it: a plain batch `read_files` (no `STREAM`) shows the file and saves nothing.

# COMMAND ----------

land_batch(1)

# COMMAND ----------

display(spark.sql(f"SELECT * FROM read_files('{LANDING}/deviation_event_feed', format => 'csv', header => true) LIMIT 10"))

# COMMAND ----------

# MAGIC %md-sandbox
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
# MAGIC <div class="flow-grid" style="grid-template-columns:1fr auto 1fr auto 1fr auto 1fr auto 1fr;"><div class="flow-step" style="--accent:#4299E0;"><div class="flow-num">1</div><div class="flow-label">Open your pipeline<br>(Jobs &amp; Pipelines)</div></div><div class="flow-arrow">&rarr;</div><div class="flow-step" style="--accent:#00A972;"><div class="flow-num">2</div><div class="flow-label">Open<br><code>bronze_deviation_event.sql</code></div></div><div class="flow-arrow">&rarr;</div><div class="flow-step" style="--accent:#FFAB00;"><div class="flow-num">3</div><div class="flow-label">Run pipeline</div></div><div class="flow-arrow">&rarr;</div><div class="flow-step" style="--accent:#FF5F46;"><div class="flow-num">4</div><div class="flow-label">Graph + row counts</div></div><div class="flow-arrow">&rarr;</div><div class="flow-step" style="--accent:#98102A;"><div class="flow-num">5</div><div class="flow-label">Run again:<br>0 new rows</div></div></div>
# MAGIC </div>
# MAGIC <div style="height:18px"></div>
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
# MAGIC <div class="ds-callout info"><div class="ds-eyebrow">Why the second run adds nothing</div><div>The Auto Loader checkpoint remembers which files it read. New files only, exactly once.</div></div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ### C. Look at one raw file you are about to ingest

# COMMAND ----------

display(spark.sql(f"SELECT * FROM read_files('{LANDING}/inspection_result_feed', format => 'csv', header => true) LIMIT 5"))

# COMMAND ----------

# MAGIC %md-sandbox
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
# MAGIC <div class="flow-grid" style="grid-template-columns:1fr auto 1fr auto 1fr auto 1fr auto 1fr;"><div class="flow-step" style="--accent:#4299E0;"><div class="flow-num">1</div><div class="flow-label">Open the pipeline<br>editor</div></div><div class="flow-arrow">&rarr;</div><div class="flow-step" style="--accent:#00A972;"><div class="flow-num">2</div><div class="flow-label">Open <code>bronze_inspection_result.sql</code>, then <code>bronze_change_control.sql</code></div></div><div class="flow-arrow">&rarr;</div><div class="flow-step" style="--accent:#FFAB00;"><div class="flow-num">3</div><div class="flow-label">Uncomment<br>(Cmd/Ctrl + /)</div></div><div class="flow-arrow">&rarr;</div><div class="flow-step" style="--accent:#FF5F46;"><div class="flow-num">4</div><div class="flow-label">Replace each<br><code>‹FILL-IN›</code></div></div><div class="flow-arrow">&rarr;</div><div class="flow-step" style="--accent:#98102A;"><div class="flow-num">5</div><div class="flow-label">Run pipeline</div></div></div>
# MAGIC </div>
# MAGIC
# MAGIC ##### EXPAND FOR ADDITIONAL NOTES
# MAGIC
# MAGIC <details>
# MAGIC
# MAGIC The recipe is in the header of each TODO file. Two to do: QC results first, then change controls (the second one takes two minutes: that is the point of a pattern). Pairs can split them. Corrective actions are prebuilt.
# MAGIC - Run with **Run pipeline** (not *full refresh*). Bronze tables refuse full refresh on purpose (`pipelines.reset.allowed = false`).
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
# MAGIC <details><summary><strong>CODE ANSWER: bronze_inspection_result.sql</strong> (try first, then expand)</summary>
# MAGIC
# MAGIC ```sql
# MAGIC -- ============================================================================
# MAGIC -- BRONZE | bronze_inspection_result
# MAGIC -- Grain  : one row per source record, exactly as it arrived (append-only)
# MAGIC -- Pattern: the SAME Auto Loader block for every feed; only the folder and
# MAGIC --          the schema (the data contract) change. Every column is STRING:
# MAGIC --          Bronze keeps values exactly as sent, Silver casts them.
# MAGIC -- ============================================================================
# MAGIC CREATE OR REFRESH STREAMING TABLE bronze_inspection_result
# MAGIC COMMENT "Raw QC inspection results from the LIMS feed (synthetic)."
# MAGIC TBLPROPERTIES (
# MAGIC   'quality' = 'bronze',
# MAGIC   'pipelines.reset.allowed' = 'false'   -- protect raw history from accidental full refresh
# MAGIC )
# MAGIC AS SELECT
# MAGIC   *,                                                   -- every source column + _rescued_data
# MAGIC   _metadata.file_path              AS source_file,     -- lineage: which file
# MAGIC   _metadata.file_modification_time AS source_file_modified_at,
# MAGIC   current_timestamp()              AS ingested_at      -- lineage: when we read it
# MAGIC FROM STREAM read_files(
# MAGIC   :landing_root || '/inspection_result_feed',
# MAGIC   format            => 'csv',
# MAGIC   header            => true,                           -- columns matched by NAME
# MAGIC   schema            => '
# MAGIC     source_sample_id STRING,
# MAGIC     lot_id           STRING,
# MAGIC     site_code        STRING,
# MAGIC     test_code        STRING,
# MAGIC     measured_value   STRING,
# MAGIC     lower_limit      STRING,
# MAGIC     upper_limit      STRING,
# MAGIC     measured_at      STRING
# MAGIC   ',                                -- the Bronze data contract: names, all STRING (Silver casts)
# MAGIC   rescuedDataColumn => '_rescued_data'   -- anything outside the contract lands here
# MAGIC );
# MAGIC ```
# MAGIC
# MAGIC </details>

# COMMAND ----------

# MAGIC %md
# MAGIC <details><summary><strong>CODE ANSWER: bronze_change_control.sql</strong> (try first, then expand)</summary>
# MAGIC
# MAGIC ```sql
# MAGIC -- ============================================================================
# MAGIC -- BRONZE | bronze_change_control
# MAGIC -- Grain  : one row per source record, exactly as it arrived (append-only)
# MAGIC -- Pattern: the SAME Auto Loader block for every feed; only the folder and
# MAGIC --          the schema (the data contract) change. Every column is STRING:
# MAGIC --          Bronze keeps values exactly as sent, Silver casts them.
# MAGIC -- ============================================================================
# MAGIC CREATE OR REFRESH STREAMING TABLE bronze_change_control
# MAGIC COMMENT "Raw change-control workflow snapshots (synthetic)."
# MAGIC TBLPROPERTIES (
# MAGIC   'quality' = 'bronze',
# MAGIC   'pipelines.reset.allowed' = 'false'   -- protect raw history from accidental full refresh
# MAGIC )
# MAGIC AS SELECT
# MAGIC   *,                                                   -- every source column + _rescued_data
# MAGIC   _metadata.file_path              AS source_file,     -- lineage: which file
# MAGIC   _metadata.file_modification_time AS source_file_modified_at,
# MAGIC   current_timestamp()              AS ingested_at      -- lineage: when we read it
# MAGIC FROM STREAM read_files(
# MAGIC   :landing_root || '/change_control_feed',
# MAGIC   format            => 'csv',
# MAGIC   header            => true,                           -- columns matched by NAME
# MAGIC   schema            => '
# MAGIC     source_change_id STRING,
# MAGIC     site_code        STRING,
# MAGIC     product_code     STRING,
# MAGIC     change_type      STRING,
# MAGIC     workflow_status  STRING,
# MAGIC     submitted_at     STRING,
# MAGIC     approved_at      STRING,
# MAGIC     effective_at     STRING,
# MAGIC     closed_at        STRING
# MAGIC   ',                                -- the Bronze data contract: names, all STRING (Silver casts)
# MAGIC   rescuedDataColumn => '_rescued_data'   -- anything outside the contract lands here
# MAGIC );
# MAGIC ```
# MAGIC
# MAGIC </details>

# COMMAND ----------

# MAGIC %md
# MAGIC ### D. Checkpoint: run the pipeline first
# MAGIC Run the pipeline (**Run pipeline**, not full refresh). When the update finishes, run the next cell: every row should show a check mark.

# COMMAND ----------

checkpoint(run=1, layer='bronze')

# COMMAND ----------

# MAGIC %md
# MAGIC ### E. Explore: lineage is free
# MAGIC Every row knows its file. This is what makes the Gold numbers traceable later.

# COMMAND ----------

display(spark.sql(f'''SELECT source_file, count(*) AS rows, min(ingested_at) AS ingested_at
FROM {FQ}.bronze_inspection_result GROUP BY ALL'''))

# COMMAND ----------

# MAGIC %md
# MAGIC ### F. Ask Auto Loader which files it has read
# MAGIC `cloud_files_state` reads the stream's checkpoint: one row per file, with when it was discovered. This is why the second run added 0 rows. Run it again in Lab 07 after batch 2 lands: the batch 1 row keeps its original time.

# COMMAND ----------

display(spark.sql(f'''SELECT regexp_extract(path, '[^/]+$', 0) AS file, size AS bytes, discovery_time
FROM cloud_files_state(TABLE({FQ}.bronze_deviation_event))
ORDER BY discovery_time'''))

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
# MAGIC <div class="ds-callout success"><div class="ds-eyebrow">Takeaway</div><div class="ds-callout-title">One Auto Loader pattern, any number of feeds.</div><ul><li>Only the folder and the contract change between feeds: compare yours with the prebuilt ones.</li><li>The checkpoint means re-running is always safe.</li><li>After batch 1 Bronze holds 287 deviation events and 1539 QC results.</li></ul></div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ## Optional: if you have time
# MAGIC The core lab ends above. Build the third Bronze table, corrective actions, with the same pattern. The pipeline already runs the prebuilt version, so skipping this costs nothing.
# MAGIC
# MAGIC 1. Open <code>pipeline_files_optional/bronze/bronze_corrective_action.sql</code> in your Git folder: the recipe is in its header.
# MAGIC 2. In your pipeline, comment out the prebuilt <code>bronze/bronze_corrective_action.sql</code>, paste the practice copy over it, fill the three blanks.
# MAGIC 3. Run the pipeline. The checkpoint above must still be all green.

# COMMAND ----------

# MAGIC %md
# MAGIC <details><summary><strong>CODE ANSWER: bronze_corrective_action.sql</strong> (try first, then expand)</summary>
# MAGIC
# MAGIC ```sql
# MAGIC -- ============================================================================
# MAGIC -- BRONZE | bronze_corrective_action
# MAGIC -- Grain  : one row per source record, exactly as it arrived (append-only)
# MAGIC -- Pattern: the SAME Auto Loader block for every feed; only the folder and
# MAGIC --          the schema (the data contract) change. Every column is STRING:
# MAGIC --          Bronze keeps values exactly as sent, Silver casts them.
# MAGIC -- ============================================================================
# MAGIC CREATE OR REFRESH STREAMING TABLE bronze_corrective_action
# MAGIC COMMENT "Raw corrective/preventive action snapshots from the QMS feed (synthetic)."
# MAGIC TBLPROPERTIES (
# MAGIC   'quality' = 'bronze',
# MAGIC   'pipelines.reset.allowed' = 'false'   -- protect raw history from accidental full refresh
# MAGIC )
# MAGIC AS SELECT
# MAGIC   *,                                                   -- every source column + _rescued_data
# MAGIC   _metadata.file_path              AS source_file,     -- lineage: which file
# MAGIC   _metadata.file_modification_time AS source_file_modified_at,
# MAGIC   current_timestamp()              AS ingested_at      -- lineage: when we read it
# MAGIC FROM STREAM read_files(
# MAGIC   :landing_root || '/corrective_action_feed',
# MAGIC   format            => 'csv',
# MAGIC   header            => true,                           -- columns matched by NAME
# MAGIC   schema            => '
# MAGIC     source_action_id STRING,
# MAGIC     source_case_id   STRING,
# MAGIC     action_code      STRING,
# MAGIC     action_status    STRING,
# MAGIC     assigned_group   STRING,
# MAGIC     created_at       STRING,
# MAGIC     completed_at     STRING
# MAGIC   ',                                -- the Bronze data contract: names, all STRING (Silver casts)
# MAGIC   rescuedDataColumn => '_rescued_data'   -- anything outside the contract lands here
# MAGIC );
# MAGIC ```
# MAGIC
# MAGIC </details>
