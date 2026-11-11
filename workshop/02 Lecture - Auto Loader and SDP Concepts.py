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
# MAGIC <div class="ds-banner info"><div class="ds-banner-icon">2</div><div><div class="ds-banner-title">Auto Loader and SDP: how it works</div><div class="ds-banner-tagline">15 minutes &middot; explained on the deviation feed &middot; you run it yourself in Lab 03</div></div></div>
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

# MAGIC %md
# MAGIC ## Overview
# MAGIC
# MAGIC Learn the handful of SDP and Auto Loader ideas the labs use: why a declarative pipeline beats hand-written batch or streaming code, how Auto Loader ingests only new files, and the three dataset types.
# MAGIC
# MAGIC ## Learning Objectives
# MAGIC
# MAGIC By the end of this lecture, you will be able to:
# MAGIC
# MAGIC 1. **Compare** batch SQL, Structured Streaming and a declarative pipeline for the same files
# MAGIC 2. **Describe the four Auto Loader ideas**: `STREAM read_files`, the schema contract, `_rescued_data`, `_metadata.file_path`
# MAGIC 3. **Check which files a stream has read** with `cloud_files_state`
# MAGIC 4. **Choose between** a streaming table, a materialized view and a temporary view
# MAGIC 5. **Write expectations** with the three actions (warn, drop, fail) and explain quarantine and NULL-tolerant rules

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div class="cw">
# MAGIC <style>
# MAGIC .cw { font-family: sans-serif; max-width: 1100px; margin: 0 auto; color: #0b2026; } .cw * { box-sizing: border-box; }
# MAGIC .fc-card { background: #F9F7F4; border-radius: 10px; padding: 20px; border-top: 8px solid var(--accent); box-shadow: 0 2px 8px rgba(27,49,57,0.06); }
# MAGIC .fc-row { display: flex; gap: 24px; align-items: stretch; flex-wrap: wrap; }
# MAGIC .fc-row > .fc-card { flex: 1; min-width: 300px; display: flex; flex-direction: column; }
# MAGIC .fc-title { font-size: 18pt; font-weight: 700; color: #0b2026; margin-bottom: 14px; }
# MAGIC .fc-intro { font-size: 14pt; line-height: 1.55; color: #0b2026; margin-bottom: 16px; }
# MAGIC .fc-intro code, .fc-val code { background: #EEEDE9; padding: 1px 5px; border-radius: 4px; font-size: 14pt; }
# MAGIC .fc-list { margin-bottom: 18px; flex: 1; }
# MAGIC .fc-item { display: grid; grid-template-columns: 1fr; gap: 4px; padding: 12px 0; border-bottom: 1px solid #EEEDE9; align-items: start; }
# MAGIC .fc-item:first-child { padding-top: 4px; }
# MAGIC .fc-item:last-child { border-bottom: none; padding-bottom: 4px; }
# MAGIC .fc-key { font-size: 14pt; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; line-height: 1.3; color: var(--accent); }
# MAGIC .fc-val { font-size: 14pt; color: #0b2026; line-height: 1.55; }
# MAGIC .fc-example { border-left: 4px solid var(--accent); border-radius: 0 8px 8px 0; padding: 14px 16px; font-size: 14pt; line-height: 1.55; background: var(--tint); }
# MAGIC .fc-example strong:first-child { text-transform: uppercase; font-size: 14pt; letter-spacing: 1.5px; display: block; margin-bottom: 6px; }
# MAGIC </style>
# MAGIC <div style="font-size:20pt;font-weight:700;margin-bottom:14px;">Three ways to load the same deviation files</div><div class="fc-row"><div class="fc-card" style="--accent:#FF5F46; --tint:rgba(255,95,70,0.10);"><div class="fc-title">Batch SQL</div><div class="fc-intro"><code>CREATE OR REPLACE TABLE ... read_files</code></div><div class="fc-list"><div class="fc-item"><div class="fc-key">Each run</div><div class="fc-val">Re-reads <strong>every</strong> file. Batch 3 re-reads batches 1 and 2.</div></div><div class="fc-item"><div class="fc-key">Plumbing</div><div class="fc-val">Little code, but you order and schedule each step yourself.</div></div><div class="fc-item"><div class="fc-key">Data quality</div><div class="fc-val">Separate validation queries that you write and maintain.</div></div><div class="fc-item"><div class="fc-key">Visibility</div><div class="fc-val">None built in. Row counts and failures need custom logging.</div></div></div><div class="fc-example"><strong>Fits</strong>Looking at a file once. We do this in Lab 03, step A.</div></div><div class="fc-card" style="--accent:#FFAB00; --tint:rgba(255,171,0,0.12);"><div class="fc-title">Structured Streaming</div><div class="fc-intro"><code>readStream ... writeStream</code></div><div class="fc-list"><div class="fc-item"><div class="fc-key">Each run</div><div class="fc-val">Only new files, thanks to the Auto Loader checkpoint.</div></div><div class="fc-item"><div class="fc-key">Plumbing</div><div class="fc-val">Checkpoint paths, triggers, <code>foreachBatch</code> + <code>MERGE</code> for upserts.</div></div><div class="fc-item"><div class="fc-key">Data quality</div><div class="fc-val">Still hand-written.</div></div><div class="fc-item"><div class="fc-key">Visibility</div><div class="fc-val">Per-stream metrics only. No graph, no table-to-table lineage.</div></div></div><div class="fc-example"><strong>Fits</strong>Low-level control you really need, at the cost of more code.</div></div><div class="fc-card" style="--accent:#00A972; --tint:rgba(0,169,114,0.10);"><div class="fc-title">Declarative pipeline (SDP)</div><div class="fc-intro"><code>CREATE OR REFRESH STREAMING TABLE</code></div><div class="fc-list"><div class="fc-item"><div class="fc-key">Each run</div><div class="fc-val">Only new files. Materialized views recompute only what changed, where they can.</div></div><div class="fc-item"><div class="fc-key">Plumbing</div><div class="fc-val">You declare tables. SDP orders them and runs checkpoints, retries and compute.</div></div><div class="fc-item"><div class="fc-key">Data quality</div><div class="fc-val"><code>EXPECT</code> with warn, drop or fail, counted per rule.</div></div><div class="fc-item"><div class="fc-key">Visibility</div><div class="fc-val">Pipeline graph, event log, data preview and Unity Catalog lineage.</div></div></div><div class="fc-example"><strong>Fits</strong>Today: five feeds, three layers, one pipeline.</div></div></div>
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
# MAGIC <div class="ds-callout caution"><div class="ds-eyebrow">What SDP asks of you in return</div><ul><li>Write <code>CREATE OR REFRESH</code> datasets, not free-form scripts with side effects.</li><li>A dataset cannot switch between streaming table and materialized view in place: rename it or drop it.</li><li>A full refresh re-reads every file, so we block it on Bronze (<code>pipelines.reset.allowed = false</code>).</li></ul></div>
# MAGIC </div>
# MAGIC
# MAGIC ##### EXPAND FOR ADDITIONAL NOTES
# MAGIC
# MAGIC <details>
# MAGIC
# MAGIC **Why this slide**
# MAGIC - Batch SQL is how most teams start. It works until the landing folder holds months of files: cost and runtime then grow with the total number of files, not with what is new.
# MAGIC - Structured Streaming fixes re-reading, but each layer needs its own checkpoint path, trigger, schema location and start/stop handling. Upserts become a `foreachBatch` function with a `MERGE`. Quality checks and run history are still yours to build.
# MAGIC - SDP keeps the incremental behaviour and removes the plumbing. The dependency graph comes from the queries, so there is no hand-written ordering.
# MAGIC
# MAGIC **What Structured Streaming would need for one Bronze table**
# MAGIC ```python
# MAGIC (spark.readStream.format("cloudFiles")
# MAGIC     .option("cloudFiles.format", "csv")
# MAGIC     .option("cloudFiles.schemaLocation", f"{checkpoints}/bronze_deviation_schema")
# MAGIC     .schema(deviation_schema)
# MAGIC     .load(f"{landing}/deviation_event_feed")
# MAGIC     .writeStream
# MAGIC     .option("checkpointLocation", f"{checkpoints}/bronze_deviation")
# MAGIC     .trigger(availableNow=True)
# MAGIC     .toTable("bronze_deviation_event"))
# MAGIC ```
# MAGIC Repeat for every feed and every layer, then add validation and logging. The SDP version is the SQL file shown below.
# MAGIC
# MAGIC **The trade-offs are real, but small for this use case**
# MAGIC - SDP owns the tables it creates. Change them by changing the pipeline code, not with ad-hoc `INSERT`s.
# MAGIC - Changing a dataset's type needs a rename or a drop (see the gotchas at the end of this lecture).
# MAGIC
# MAGIC </details>

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
# MAGIC <div style="font-size:20pt;font-weight:700;margin-bottom:14px;">Auto Loader in four ideas</div><div class="ds-row"><div class="ds-card blue"><div class="ds-card-title">FROM STREAM read_files</div><div class="ds-card-para"><code>STREAM</code> turns a one-off read into Auto Loader: a checkpoint remembers which files were read.</div></div><div class="ds-card green"><div class="ds-card-title">schema =&gt; '...'</div><div class="ds-card-para">The Bronze <strong>data contract</strong>: columns matched by header name, every column <code>STRING</code>. Bronze keeps values exactly as sent; Silver casts them.</div></div><div class="ds-card amber"><div class="ds-card-title">_rescued_data</div><div class="ds-card-para">Anything outside the contract (a new column the source starts sending) lands here as JSON. Nothing is lost.</div></div><div class="ds-card coral"><div class="ds-card-title">_metadata.file_path</div><div class="ds-card-para">Lineage for every row: which file, when we read it. Traceability starts in Bronze.</div></div></div>
# MAGIC </div>
# MAGIC
# MAGIC ##### EXPAND FOR ADDITIONAL NOTES
# MAGIC
# MAGIC <details>
# MAGIC
# MAGIC **Talking points**
# MAGIC - Read the Bronze file below top to bottom: `STREAM`, the schema contract, `_rescued_data`, `_metadata.file_path`. That is all of Auto Loader learners need today.
# MAGIC - Do not run anything here. In Lab 03 they land batch 1, run this exact file and see the second run add 0 rows.
# MAGIC
# MAGIC **Why every Bronze column is STRING.** Databricks recommends storing most Bronze fields as string (or VARIANT) so an unexpected value or type change can never break ingestion; casting and validation belong in Silver. Our Silver files do it with `try_cast` and `try_to_timestamp`, which return NULL instead of failing, and the matching rule sends the row to quarantine.
# MAGIC
# MAGIC **Why an explicit schema, not inference?** In preflight we landed all three batches at once into a fresh schema. Inference sampled the batch 3 header, `severity` became a real column, and a validation rule silently stopped seeing it. With an explicit contract the result is identical no matter when files arrive.
# MAGIC
# MAGIC </details>

# COMMAND ----------

# MAGIC %md
# MAGIC ```sql
# MAGIC -- ============================================================================
# MAGIC -- BRONZE | bronze_deviation_event
# MAGIC -- Grain  : one row per source record, exactly as it arrived (append-only)
# MAGIC -- Pattern: the SAME Auto Loader block for every feed; only the folder and
# MAGIC --          the schema (the data contract) change. Every column is STRING:
# MAGIC --          Bronze keeps values exactly as sent, Silver casts them.
# MAGIC -- ============================================================================
# MAGIC CREATE OR REFRESH STREAMING TABLE bronze_deviation_event
# MAGIC COMMENT "Raw deviation status events from the QMS feed (synthetic)."
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
# MAGIC   :landing_root || '/deviation_event_feed',
# MAGIC   format            => 'csv',
# MAGIC   header            => true,                           -- columns matched by NAME
# MAGIC   schema            => '
# MAGIC     source_case_id    STRING,
# MAGIC     site_code         STRING,
# MAGIC     lot_id            STRING,
# MAGIC     event_code        STRING,
# MAGIC     status_code       STRING,
# MAGIC     reported_at       STRING,
# MAGIC     target_due_at     STRING,
# MAGIC     resolved_at       STRING,
# MAGIC     source_updated_at STRING,
# MAGIC     description       STRING
# MAGIC   ',                                -- the Bronze data contract: names, all STRING (Silver casts)
# MAGIC   rescuedDataColumn => '_rescued_data'   -- anything outside the contract lands here
# MAGIC );
# MAGIC ```

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
# MAGIC <div class="ds-callout info"><div class="ds-eyebrow">Ask Auto Loader what it has read</div><div class="ds-callout-title">cloud_files_state(TABLE(bronze_deviation_event))</div><div>A table-valued function that returns one row per file in the stream's checkpoint: path, size, when the file was created, when Auto Loader discovered it, and which flow read it. You run it in Lab 03 after the first run, and again after batch 2 lands to see that batch 1 was not read twice.</div><ul><li>Answers &quot;was this file ingested?&quot; without counting rows.</li><li>Works on streaming tables built with <code>read_files</code> or Auto Loader, including tables a pipeline owns.</li><li>Docs: <a href="https://docs.databricks.com/aws/en/sql/language-manual/functions/cloud_files_state" target="_blank">cloud_files_state</a>.</li></ul></div>
# MAGIC </div>
# MAGIC
# MAGIC ##### EXPAND FOR ADDITIONAL NOTES
# MAGIC
# MAGIC <details>
# MAGIC
# MAGIC ```sql
# MAGIC SELECT regexp_extract(path, '[^/]+$', 0) AS file, size AS bytes, discovery_time
# MAGIC FROM cloud_files_state(TABLE(bronze_deviation_event))
# MAGIC ORDER BY discovery_time
# MAGIC ```
# MAGIC - `path` is the storage path behind the volume, so we keep only the file name.
# MAGIC - After batch 1 you see one file per feed. After batch 2 there are two, and the batch 1 row keeps its original `discovery_time`: that is exactly-once ingestion, visible.
# MAGIC - The checkpoint is the state. A full refresh resets it, which is why Bronze blocks full refresh.
# MAGIC
# MAGIC </details>

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
# MAGIC <div style="font-size:20pt;font-weight:700;margin-bottom:14px;">The Lakeflow Pipelines Editor</div><div class="ds-row"><div class="ds-card blue"><div class="ds-card-title">Asset browser</div><div class="ds-card-para">All pipeline files in one tree: <code>bronze/</code>, <code>silver/</code>, <code>gold/</code>, <code>checks/</code>.</div></div><div class="ds-card green"><div class="ds-card-title">Graph (DAG)</div><div class="ds-card-para">Built from your queries. Click a node for rows, schema, expectations.</div></div><div class="ds-card amber"><div class="ds-card-title">Data preview</div><div class="ds-card-para">See sample output under each table without leaving the editor.</div></div><div class="ds-card coral"><div class="ds-card-title">Run file / dry run</div><div class="ds-card-para">Validate or run just the file you are editing; full pipeline when ready.</div></div></div>
# MAGIC </div>
# MAGIC <div style="height:18px"></div>
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
# MAGIC <div class="ds-row"><div class="ds-card blue"><div class="ds-card-label">pipeline.yml</div><div class="ds-card-title">catalog + schema</div><div class="ds-card-para">Where tables publish: your personal schema.</div></div><div class="ds-card green"><div class="ds-card-label">pipeline.yml</div><div class="ds-card-title">parameters</div><div class="ds-card-para"><code>landing_root</code>, <code>as_of_date</code> are read in SQL as <code>:landing_root</code>, bound when the update starts.</div></div><div class="ds-card amber"><div class="ds-card-label">pipeline.yml</div><div class="ds-card-title">serverless + triggered</div><div class="ds-card-para">Runs when started or scheduled; continuous mode is one setting away.</div></div><div class="ds-card coral"><div class="ds-card-label">pipeline.yml</div><div class="ds-card-title">event_log</div><div class="ds-card-para">Published to UC as <code>event_log_iops_quality</code> for monitoring.</div></div></div>
# MAGIC </div>

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
# MAGIC <div class="flow-grid" style="grid-template-columns:1fr auto 1fr auto 1fr auto 1fr;"><div class="flow-step" style="--accent:#4299E0;"><div class="flow-num">1</div><div class="flow-label">Run 1<br>batch_01 files</div></div><div class="flow-arrow">&rarr;</div><div class="flow-step" style="--accent:#00A972;"><div class="flow-num">2</div><div class="flow-label">Bronze ST<br>+287 rows</div></div><div class="flow-arrow">&rarr;</div><div class="flow-step" style="--accent:#FFAB00;"><div class="flow-num">3</div><div class="flow-label">Silver ST<br>+286 rows</div></div><div class="flow-arrow">&rarr;</div><div class="flow-step" style="--accent:#FF5F46;"><div class="flow-num">4</div><div class="flow-label">Gold MV<br>111 cases</div></div></div>
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
# MAGIC <div class="flow-grid" style="grid-template-columns:1fr auto 1fr auto 1fr auto 1fr;"><div class="flow-step" style="--accent:#4299E0;"><div class="flow-num">1</div><div class="flow-label">batch_02 files<br>(batch_01 skipped)</div></div><div class="flow-arrow">&rarr;</div><div class="flow-step" style="--accent:#00A972;"><div class="flow-num">2</div><div class="flow-label">Bronze ST<br>+24 new rows</div></div><div class="flow-arrow">&rarr;</div><div class="flow-step" style="--accent:#FFAB00;"><div class="flow-num">3</div><div class="flow-label">Silver ST<br>+21 new rows</div></div><div class="flow-arrow">&rarr;</div><div class="flow-step" style="--accent:#FF5F46;"><div class="flow-num">4</div><div class="flow-label">Gold MV<br>recomputed: 119 cases</div></div></div>
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
# MAGIC <div class="ds-callout info"><div class="ds-eyebrow">Run 1 vs Run 2, with our numbers</div><div>Top: the first run reads batch 1. Bottom: after batch 2 lands, streaming tables append <strong>only the new rows</strong>; the materialized view recomputes so late events can change old cases.</div></div>
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
# MAGIC <div style="font-size:20pt;font-weight:700;margin-bottom:14px;">Three dataset types</div><div class="ds-row"><div class="ds-card blue"><div class="ds-card-title">Streaming table</div><ul><li>Appends only <strong>new</strong> input</li><li>Exactly-once per file / row</li><li>Bronze, Silver, event-level Gold</li></ul></div><div class="ds-card green"><div class="ds-card-title">Materialized view</div><ul><li>Result always matches current inputs</li><li>Recomputes (incrementally on serverless when it can)</li><li>Aggregates, joins, &quot;latest state&quot;</li></ul></div><div class="ds-card amber"><div class="ds-card-title">Temporary view</div><ul><li>No storage, pipeline-private</li><li>Shared prep logic (we use it in Silver)</li><li>Not visible in Unity Catalog</li></ul></div></div>
# MAGIC </div>

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
# MAGIC <div class="ds-callout info"><div class="ds-eyebrow">Coming up in Lecture 04</div><div>Data quality (expectations, quarantine) and change data capture (AUTO CDC) get their own short lecture, right before you build Silver.</div></div>
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
# MAGIC <div style="font-size:20pt;font-weight:700;margin-bottom:14px;">Join types</div><div class="ds-row"><div class="ds-card blue"><div class="ds-card-title">Stream-snapshot join</div><ul><li>Streaming table + static table &rarr; streaming table</li><li>Each <strong>new</strong> row is enriched once</li><li>Our <code>gold_oos_events</code></li></ul></div><div class="ds-card green"><div class="ds-card-title">Join in a materialized view</div><ul><li>All rows of both sides, every run</li><li>Always consistent</li><li>Our <code>gold_deviation_lifecycle</code></li></ul></div><div class="ds-card amber"><div class="ds-card-title">Stream-stream join</div><ul><li>Needs watermarks and time bounds</li><li>Advanced</li><li>Out of scope today</li></ul></div></div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ### The same pattern in Python
# MAGIC `python/batch_record.py` (you add it in Lab 05) writes Bronze once as a function. In Python, a pattern becomes a reusable function or a loop over feeds.

# COMMAND ----------

# MAGIC %md
# MAGIC ```python
# MAGIC # ============================================================================
# MAGIC # PYTHON EXAMPLE | batch record feed (MES): Bronze + Silver in one file
# MAGIC # Shows that .sql and .py files run together in one pipeline, and what the
# MAGIC # Python syntax looks like. The Auto Loader pattern is a reusable function.
# MAGIC # ============================================================================
# MAGIC from pyspark import pipelines as dp
# MAGIC from pyspark.sql import functions as F
# MAGIC
# MAGIC LANDING_ROOT = spark.conf.get("landing_root")  # noqa: F821  (spark is provided by the pipeline)
# MAGIC
# MAGIC
# MAGIC def bronze_feed(feed: str, schema: str):
# MAGIC     """Incrementally read one landing folder with Auto Loader, keeping lineage columns."""
# MAGIC     return (
# MAGIC         spark.readStream.format("cloudFiles")  # noqa: F821
# MAGIC         .option("cloudFiles.format", "csv")
# MAGIC         .option("header", "true")
# MAGIC         .option("rescuedDataColumn", "_rescued_data")
# MAGIC         .schema(schema)  # the Bronze data contract
# MAGIC         .load(f"{LANDING_ROOT}/{feed}")
# MAGIC         .select(
# MAGIC             "*",
# MAGIC             F.col("_metadata.file_path").alias("source_file"),
# MAGIC             F.col("_metadata.file_modification_time").alias("source_file_modified_at"),
# MAGIC             F.current_timestamp().alias("ingested_at"),
# MAGIC         )
# MAGIC     )
# MAGIC ```

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
# MAGIC <div class="ds-callout danger row"><div class="ds-callout-icon">!</div><div><div class="ds-eyebrow">Gotchas we hit while building this</div><ul><li><code>CREATE OR REPLACE</code> is not SDP syntax: use <code>CREATE OR REFRESH</code>.</li><li>Forgetting <code>STREAM</code> makes a batch read: an ST cannot be built from a batch query.</li><li>An empty landing folder cannot be read: land batch 1 before the first run.</li><li>Changing a dataset from ST to MV needs a new name or a drop; a full refresh does not convert it.</li></ul></div></div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC This check is **ungraded**. Pick an answer and click **Check**.
# MAGIC
# MAGIC <style>
# MAGIC .qz-shell{display:flex;border:1px solid #DCE0E2;border-radius:12px;overflow:hidden;min-height:380px;font-family:sans-serif}
# MAGIC .qz-nav{flex:0 0 200px;background:#F8F9FC;border-right:1px solid #DCE0E2;padding:12px 0}
# MAGIC .qz-nav-item{padding:10px 16px;font-size:14pt;font-weight:500;color:#5E7077;cursor:pointer;user-select:none;display:flex;align-items:center;gap:10px}
# MAGIC .qz-nav-item:hover{background:#EEEDE9;color:#0b2026}
# MAGIC .qz-nav-item.active{color:#0b2026;border-right:3px solid #4299E0}
# MAGIC .qz-dot{width:10px;height:10px;border-radius:50%;border:2px solid #C2C2C2;flex-shrink:0}
# MAGIC .qz-dot.answered{border-color:#4299E0;background:#4299E0}.qz-dot.correct{border-color:#00A972;background:#00A972}.qz-dot.wrong{border-color:#FF5F46;background:#FF5F46}
# MAGIC .qz-btn{margin-top:14px;padding:10px 24px;border:none;border-radius:8px;font-size:14pt;font-weight:600;cursor:pointer;background:#4299E0;color:#fff}
# MAGIC .qz-btn:disabled{opacity:.35;cursor:default}
# MAGIC .qz-main{flex:1;padding:24px 28px;display:flex;flex-direction:column;justify-content:center}
# MAGIC .qz-q{font-size:14pt;font-weight:500;color:#0b2026;margin-bottom:16px;line-height:1.5}
# MAGIC .qz-q code{background:#EEEDE9;padding:1px 5px;border-radius:4px;font-size:14pt}
# MAGIC .qz-opts{display:flex;flex-direction:column;gap:10px}
# MAGIC .qz-opt{display:flex;align-items:center;gap:12px;padding:12px 16px;border-radius:8px;border:1px solid #DCE0E2;background:#fff;cursor:pointer;font-size:14pt;color:#0b2026;user-select:none}
# MAGIC .qz-opt:hover{background:#EEEDE9;border-color:#C2C2C2}
# MAGIC .qz-opt.selected{border-color:#4299E0;background:#F8F9FC;font-weight:500}
# MAGIC .qz-opt.right{border-color:#00A972;background:rgba(0,169,114,0.10);color:#00A972;font-weight:500}
# MAGIC .qz-opt.wrong-pick{border-color:#FF5F46;background:rgba(255,95,70,0.10);color:#FF5F46}
# MAGIC .qz-opt.locked{pointer-events:none}
# MAGIC .qz-opt code{background:#EEEDE9;padding:1px 5px;border-radius:4px}
# MAGIC .qz-fb{margin-top:14px;padding:12px 16px;border-radius:8px;font-size:14pt;line-height:1.5}
# MAGIC .qz-fb.ok{background:rgba(0,169,114,0.10);color:#00A972}.qz-fb.no{background:rgba(255,95,70,0.10);color:#98102A}
# MAGIC </style>
# MAGIC <div class="qz-shell"><div class="qz-nav" id="qz-nav"></div><div class="qz-main" id="qz-main"></div></div>
# MAGIC <script>
# MAGIC var QZ=[{"q": "You run the pipeline twice without new files. How many rows does Bronze add the second time?", "opts": ["All rows again", "0", "Only changed rows"], "ans": 1, "fb": "The Auto Loader checkpoint remembers files already read."}, {"q": "A file has an extra column <code>severity</code> that is not in the schema. Where does it go?", "opts": ["The pipeline fails", "It is dropped", "<code>_rescued_data</code>"], "ans": 2, "fb": "With an explicit schema and rescued data, unknown fields are kept as JSON."}];
# MAGIC var qzPick=new Array(QZ.length).fill(-1),qzCur=0,qzChecked=new Array(QZ.length).fill(false);
# MAGIC function qzNav(){var n=document.getElementById('qz-nav');n.innerHTML='';QZ.forEach(function(q,i){var d=document.createElement('div');
# MAGIC  d.className='qz-nav-item'+(i===qzCur?' active':'');var c='qz-dot';if(qzChecked[i]){c+=qzPick[i]===q.ans?' correct':' wrong';}else if(qzPick[i]>=0){c+=' answered';}
# MAGIC  d.innerHTML='<div class="'+c+'"></div>Question '+(i+1);d.onclick=function(){qzCur=i;qzNav();qzShow();};n.appendChild(d);});}
# MAGIC function qzShow(){var q=QZ[qzCur],h='<div class="qz-q">'+(qzCur+1)+'. '+q.q+'</div><div class="qz-opts">';
# MAGIC  q.opts.forEach(function(o,oi){var c='qz-opt';if(qzChecked[qzCur]){c+=' locked';if(oi===q.ans)c+=' right';else if(oi===qzPick[qzCur])c+=' wrong-pick';}
# MAGIC  else if(oi===qzPick[qzCur])c+=' selected';h+='<div class="'+c+'" onclick="qzSel('+oi+')">'+o+'</div>';});h+='</div>';
# MAGIC  if(qzChecked[qzCur]){var ok=qzPick[qzCur]===q.ans;h+='<div class="qz-fb '+(ok?'ok':'no')+'">'+(ok?'&#10003; Correct. ':'&#10007; Not quite. ')+q.fb+'</div>';}
# MAGIC  else{h+='<button class="qz-btn" '+(qzPick[qzCur]<0?'disabled':'')+' onclick="qzChk()">Check</button>';}
# MAGIC  document.getElementById('qz-main').innerHTML=h;}
# MAGIC function qzSel(oi){if(qzChecked[qzCur])return;qzPick[qzCur]=oi;qzNav();qzShow();}
# MAGIC function qzChk(){qzChecked[qzCur]=true;qzNav();qzShow();}
# MAGIC qzNav();qzShow();
# MAGIC </script>

# COMMAND ----------

# MAGIC %md
# MAGIC ## Conclusion
# MAGIC
# MAGIC In this lecture, you:
# MAGIC
# MAGIC 1. Compared batch SQL, Structured Streaming and SDP for the same deviation files
# MAGIC 2. Learned how Auto Loader ingests only new files, and how to check it with `cloud_files_state`
# MAGIC 3. Chose between streaming tables, materialized views and temporary views
# MAGIC 4. Saw how expectations and quarantine keep bad records visible and out of Silver
# MAGIC
# MAGIC ### Next Steps
# MAGIC
# MAGIC In **03 Lab - Bronze with Auto Loader**, you open your pipeline and build your first two Bronze tables.
