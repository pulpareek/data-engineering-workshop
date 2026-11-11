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
# MAGIC <div class="ds-banner info"><div class="ds-banner-icon">12</div><div><div class="ds-banner-title">Recap: the whole pipeline, end to end</div><div class="ds-banner-tagline">15 minutes &middot; facilitator-led, then questions</div></div></div>
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
# MAGIC <div class="flow-grid" style="grid-template-columns:1fr auto 1fr auto 1fr auto 1fr auto 1fr;"><div class="flow-step" style="--accent:#4299E0;"><div class="flow-num">1</div><div class="flow-label">Two Gold outputs</div></div><div class="flow-arrow">&rarr;</div><div class="flow-step" style="--accent:#00A972;"><div class="flow-num">2</div><div class="flow-label">One data-quality case</div></div><div class="flow-arrow">&rarr;</div><div class="flow-step" style="--accent:#FFAB00;"><div class="flow-num">3</div><div class="flow-label">One new-file arrival</div></div><div class="flow-arrow">&rarr;</div><div class="flow-step" style="--accent:#FF5F46;"><div class="flow-num">4</div><div class="flow-label">One QA deployment</div></div><div class="flow-arrow">&rarr;</div><div class="flow-step" style="--accent:#98102A;"><div class="flow-num">5</div><div class="flow-label">Dashboard + app</div></div></div>
# MAGIC </div>
# MAGIC
# MAGIC ##### EXPAND FOR ADDITIONAL NOTES
# MAGIC
# MAGIC <details>
# MAGIC
# MAGIC **Run this on the reference schema** (widgets: team = your ref team, target = ref) so every number exists even if nobody finished.
# MAGIC - Point at one row per section and ask the room *where did this come from?* before showing the answer.
# MAGIC - Keep 5 minutes for questions and the decisions table at the end.
# MAGIC
# MAGIC </details>

# COMMAND ----------

%run ./Includes/Classroom-Setup

# COMMAND ----------

# MAGIC %md
# MAGIC ### 1. Two Gold outputs, and the grain of each

# COMMAND ----------

display(spark.sql(f'SELECT site_code, count_if(is_open) open_cases, count_if(is_overdue) overdue FROM {FQ}.gold_deviation_lifecycle GROUP BY ALL ORDER BY site_code'))

# COMMAND ----------

display(spark.sql(f'SELECT site_code, test_code, sum(total_results) results, sum(oos_results) oos FROM {FQ}.gold_inspection_quality GROUP BY ALL ORDER BY oos DESC'))

# COMMAND ----------

# MAGIC %md
# MAGIC ### 2. One data-quality case: a quarantined row and the rule that caught it

# COMMAND ----------

display(spark.sql(f'SELECT quarantine_reason, count(*) n FROM {FQ}.silver_inspection_result_quarantine GROUP BY ALL ORDER BY n DESC'))

# COMMAND ----------

# MAGIC %md
# MAGIC ### 3. One new-file arrival: only new files were read

# COMMAND ----------

display(spark.sql(f'SELECT source_file, count(*) n, min(ingested_at) ingested_at FROM {FQ}.bronze_deviation_event GROUP BY ALL ORDER BY source_file'))

# COMMAND ----------

# MAGIC %md
# MAGIC ### 4. One QA deployment
# MAGIC Show the bundle's **Deployments** panel with the `qa` target and the QA pipeline run: same code, production mode, QA gate passed.

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
# MAGIC <div class="ds-callout info"><div class="ds-eyebrow">5. Dashboard and app (stretch, prebuilt)</div><ul><li>Open the published dashboard and the lot app from <code>databricks bundle summary -t ref</code>.</li><li>Pick a BLOCKED lot in the app and trace one reason to its source file.</li><li>Both read the same Gold tables you built: no extra copies.</li></ul></div>
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
# MAGIC <div class="ds-callout success"><div class="ds-eyebrow">Questions to take back</div><ul><li>Which feed would you onboard first for real, and who owns its rules?</li><li>Where should quarantined rows go: a steward queue, a ticket, a report?</li><li>Who approves a promotion to QA and to production?</li></ul></div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ### Decisions and owners
# MAGIC | Decision | Owner | By when |
# MAGIC |---|---|---|
# MAGIC | | | |
# MAGIC | | | |
