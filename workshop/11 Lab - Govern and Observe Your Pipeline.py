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
# MAGIC <div class="ds-banner info"><div class="ds-banner-icon">11</div><div><div class="ds-banner-title">Lab 11 &middot; Govern and observe your pipeline</div><div class="ds-banner-tagline">15 minutes &middot; grants, tags, lineage and data quality on your own tables</div></div></div>
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
# MAGIC <div class="ds-callout info"><div class="ds-eyebrow">Some steps need admin rights</div><div>Cells that read system tables or billing say what they need. Without access they show who grants it and what you would see, instead of an error. The table in Lecture 10 lists every right.</div></div>
# MAGIC </div>

# COMMAND ----------

%run ./Includes/Classroom-Setup

# COMMAND ----------

# MAGIC %md
# MAGIC ### A. Who can see my schema?

# COMMAND ----------

display(spark.sql(f'SHOW GRANTS ON SCHEMA {FQ}'))

# COMMAND ----------

# MAGIC %md
# MAGIC ### B. Tag your Gold tables

# COMMAND ----------

for t in ('gold_deviation_lifecycle', 'gold_change_control_cycle_time', 'gold_inspection_quality'):
    spark.sql(f"ALTER TABLE {FQ}.{t} SET TAGS ('domain' = 'quality', 'layer' = 'gold')")
display(spark.sql(f'''SELECT table_name, tag_name, tag_value FROM {CATALOG}.information_schema.table_tags
WHERE schema_name = '{SCHEMA}' ORDER BY table_name, tag_name'''))

# COMMAND ----------

# MAGIC %md
# MAGIC Governed tags: the platform enforces the vocabulary. If an admin created a tag policy, only its allowed values are accepted. Try a value the policy does not allow:

# COMMAND ----------

try:
    spark.sql(f"ALTER TABLE {FQ}.gold_deviation_lifecycle SET TAGS ('data_classification' = 'internal')")
    print("Accepted: this workspace has no policy on data_classification.")
except Exception as e:
    msg = str(e).splitlines()[0]
    print("Rejected by the tag policy (this is the point):")
    print(msg[msg.find('Tag value'):][:200] if 'Tag value' in msg else msg[:300])

# COMMAND ----------

# MAGIC %md
# MAGIC ### C. Lineage from system tables: who reads my Gold table?

# COMMAND ----------

with needs('SELECT on the system tables system.access.* (lineage)',
           'A metastore or account admin: enable the system schema, then GRANT USE CATALOG ON CATALOG system, USE SCHEMA ON SCHEMA system.access and SELECT ON SCHEMA system.access TO your group.',
           'Every table, view, notebook and dashboard that reads or writes your table, with who and when.'):
    display(spark.sql(f'''SELECT source_table_full_name, target_table_full_name, entity_type, max(event_time) AS last_seen
    FROM system.access.table_lineage
    WHERE target_table_full_name = '{FQ}.gold_deviation_lifecycle' OR source_table_full_name = '{FQ}.gold_deviation_lifecycle'
    GROUP BY ALL ORDER BY last_seen DESC'''))

# COMMAND ----------

# MAGIC %md
# MAGIC ### D. Data quality from the event log

# COMMAND ----------

display(spark.sql(f'''
WITH dq AS (
  SELECT explode(from_json(details:flow_progress:data_quality:expectations,
         'array<struct<name: string, dataset: string, passed_records: int, failed_records: int>>')) AS e
  FROM {FQ}.event_log_iops_quality
  WHERE event_type = 'flow_progress')
SELECT e.dataset, e.name AS expectation, sum(e.passed_records) AS passed, sum(e.failed_records) AS failed
FROM dq GROUP BY ALL HAVING sum(e.failed_records) > 0 ORDER BY failed DESC'''))

# COMMAND ----------

display(spark.sql(f'''SELECT timestamp, origin.flow_name, details:flow_progress:metrics:num_output_rows::bigint AS rows_out
FROM {FQ}.event_log_iops_quality WHERE event_type = 'flow_progress' AND details:flow_progress:status = 'COMPLETED'
ORDER BY timestamp DESC LIMIT 20'''))

# COMMAND ----------

# MAGIC %md
# MAGIC ### E. Cost: which tags reached billing?
# MAGIC Two kinds of tags. Unity Catalog tags describe data (meaning, owner, sensitivity). Compute tags attribute cost. Check which of your tags actually arrived in `system.billing.usage`.

# COMMAND ----------

with needs('SELECT on system.billing.usage',
           'An account admin: GRANT USE SCHEMA ON SCHEMA system.billing and SELECT ON TABLE system.billing.usage TO your group.',
           'DBUs per product with the tags that reached billing, so cost can be split by team or project.'):
    display(spark.sql(f'''SELECT billing_origin_product, custom_tags, round(sum(usage_quantity), 2) AS dbus
    FROM system.billing.usage
    WHERE usage_date >= current_date() - INTERVAL 7 DAYS
      AND (usage_metadata.dlt_pipeline_id IN (SELECT pipeline_id FROM system.lakeflow.pipelines WHERE {MY_PIPELINES})
           OR usage_metadata.job_id IN (SELECT job_id FROM system.lakeflow.jobs WHERE {MY_JOBS}))
    GROUP BY ALL'''))

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
# MAGIC <div class="ds-callout caution"><div class="ds-eyebrow">What the billing table shows</div><div class="ds-callout-title">Job tags arrive. Serverless pipeline tags do not.</div><ul><li>The job's <code>tags</code> (<code>workshop</code>) appear in <code>custom_tags</code>.</li><li>The pipeline's <code>tags</code> do not: serverless pipelines are attributed through a <strong>serverless usage policy</strong> (<code>usage_policy_id</code> in the bundle, one per team or cost center).</li><li>Never put people or sensitive values in tags: they are plain text and replicated.</li></ul></div>
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
# MAGIC <div class="ds-callout success"><div class="ds-eyebrow">Takeaway</div><div class="ds-callout-title">Governance came with the pipeline.</div><ul><li>Lineage and data-quality metrics needed no extra code.</li><li>Tags set by hand stay here: Lab 13 makes them code.</li></ul></div>
# MAGIC </div>
