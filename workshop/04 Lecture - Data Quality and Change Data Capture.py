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
# MAGIC <div class="ds-banner info"><div class="ds-banner-icon">4</div><div><div class="ds-banner-title">Data quality and change data capture</div><div class="ds-banner-tagline">10 minutes &middot; the two ideas behind every Silver table</div></div></div>
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
# MAGIC <div class="flow-grid" style="grid-template-columns:1fr auto 1fr auto 1fr auto 1fr auto 1fr auto 1fr;"><div class="flow-step dim" style="--accent:#4299E0;"><div class="flow-num">1</div><div class="flow-label">Land files</div></div><div class="flow-arrow dim">&rarr;</div><div class="flow-step dim" style="--accent:#00A972;"><div class="flow-num">2</div><div class="flow-label">Bronze</div></div><div class="flow-arrow">&rarr;</div><div class="flow-step" style="--accent:#FFAB00;"><div class="flow-num">3</div><div class="flow-label">Silver</div></div><div class="flow-arrow dim">&rarr;</div><div class="flow-step dim" style="--accent:#FF5F46;"><div class="flow-num">4</div><div class="flow-label">Gold</div></div><div class="flow-arrow dim">&rarr;</div><div class="flow-step dim" style="--accent:#98102A;"><div class="flow-num">5</div><div class="flow-label">New batch</div></div><div class="flow-arrow dim">&rarr;</div><div class="flow-step dim" style="--accent:#1B5162;"><div class="flow-num">6</div><div class="flow-label">Promote</div></div></div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## Overview
# MAGIC
# MAGIC Silver is where data becomes trustworthy. Two ideas do the work: **expectations** decide which rows are good, and **AUTO CDC** keeps one current row per record when a source keeps re-sending it. You use both in Lab 05.
# MAGIC
# MAGIC ## Learning Objectives
# MAGIC
# MAGIC By the end of this lecture, you will be able to:
# MAGIC
# MAGIC 1. **Write an expectation** with the `CONSTRAINT ... EXPECT` syntax
# MAGIC 2. **Choose an action**: warn, drop or fail
# MAGIC 3. **Keep rejected rows** in a quarantine table, and write NULL-tolerant rules
# MAGIC 4. **Explain change data capture**, SCD type 1 and SCD type 2
# MAGIC 5. **Read an `AUTO CDC INTO` statement** clause by clause

# COMMAND ----------

# MAGIC %md
# MAGIC ## A. Expectations: rules that run on every row

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
# MAGIC <div class="ds-row"><div class="ds-card blue"><div class="ds-card-title">What they are</div><ul><li>Data quality rules inside the table definition</li><li>Checked row by row, on every run</li><li>Counted in the pipeline metrics, rule by rule</li></ul></div><div class="ds-card green"><div class="ds-card-title">General syntax</div><div class="ds-card-para"><code>CONSTRAINT constraint_name</code><br><code>EXPECT (condition_true_for_good_rows)</code><br><code>[ON VIOLATION DROP ROW | FAIL UPDATE]</code></div></div></div>
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
# MAGIC <div style="font-size:20pt;font-weight:700;margin-bottom:14px;">Three actions</div><div class="ds-row"><div class="ds-card amber"><div class="ds-card-label">No ON VIOLATION</div><div class="ds-card-title">WARN</div><div class="ds-card-para">Row kept, violation counted. Ours: the zero-data-loss check.</div></div><div class="ds-card coral"><div class="ds-card-label">ON VIOLATION DROP ROW</div><div class="ds-card-title">DROP</div><div class="ds-card-para">Row left out, counted. Ours: every Silver rule.</div></div><div class="ds-card red"><div class="ds-card-label">ON VIOLATION FAIL UPDATE</div><div class="ds-card-title">FAIL</div><div class="ds-card-para">That flow stops until fixed. Ours: the QA gate.</div></div></div>
# MAGIC </div>
# MAGIC
# MAGIC ##### EXPAND FOR ADDITIONAL NOTES
# MAGIC
# MAGIC <details>
# MAGIC
# MAGIC - Each expectation is evaluated on its own. A row can fail several; the action of each one applies.
# MAGIC - FAIL stops only that flow; other tables in the pipeline keep running.
# MAGIC - Materialized views that have expectations are fully recomputed on every run, so keep row rules on streaming tables, as Silver does.
# MAGIC
# MAGIC </details>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div style="max-width: 900px; margin: 0 auto; font-family: sans-serif;"><svg width="100%" viewBox="0 0 920 370" role="img" aria-label="How a row moves through expectations" style="font-family: sans-serif;"><defs><marker id="xf-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1 1L9 5L1 9z" fill="#5E7077"/></marker></defs><rect x="10" y="128" width="120" height="44" rx="6" fill="#FFFFFF" stroke="#5E7077" stroke-width="1.5"/><text x="70.0" y="154.9" text-anchor="middle" font-size="14" font-weight="400" fill="#0b2026"><tspan x="70.0" dy="0">Bronze row</tspan></text><path d="M130 150 L176 150" fill="none" stroke="#5E7077" stroke-width="2" marker-end="url(#xf-arrow)"/><rect x="180" y="92" width="170" height="116" rx="6" fill="#F9F7F4" stroke="#5E7077" stroke-width="1.5"/><text x="265.0" y="137.25" text-anchor="middle" font-size="15" font-weight="700" fill="#0b2026"><tspan x="265.0" dy="0">Every</tspan><tspan x="265.0" dy="18.0">expectation</tspan><tspan x="265.0" dy="18.0">on this table</tspan></text><path d="M350 150 L380 150 L380 50 L520 50" fill="none" stroke="#00A972" stroke-width="2" marker-end="url(#xf-arrow)"/><text x="400" y="42" font-size="14" font-style="italic" fill="#00A972">all pass</text><path d="M380 150 L380 250 L440 250" fill="none" stroke="#FF5F46" stroke-width="2"/><text x="300" y="290" font-size="14" font-style="italic" fill="#FF5F46">a rule fails</text><rect x="524" y="28" width="170" height="44" rx="6" fill="#00A972"/><text x="609.0" y="54.9" text-anchor="middle" font-size="14" font-weight="700" fill="#FFFFFF"><tspan x="609.0" dy="0">Keep the row</tspan></text><path d="M440 250 L440 170 L520 170" fill="none" stroke="#FFAB00" stroke-width="2" marker-end="url(#xf-arrow)"/><path d="M440 250 L520 250" fill="none" stroke="#FF5F46" stroke-width="2" marker-end="url(#xf-arrow)"/><path d="M440 250 L440 330 L520 330" fill="none" stroke="#98102A" stroke-width="2" marker-end="url(#xf-arrow)"/><rect x="524" y="148" width="170" height="44" rx="6" fill="#FFAB00"/><text x="609.0" y="174.9" text-anchor="middle" font-size="14" font-weight="700" fill="#0b2026"><tspan x="609.0" dy="0">WARN: keep + count</tspan></text><rect x="524" y="228" width="170" height="44" rx="6" fill="#FF5F46"/><text x="609.0" y="254.9" text-anchor="middle" font-size="14" font-weight="700" fill="#FFFFFF"><tspan x="609.0" dy="0">DROP: leave out</tspan></text><rect x="524" y="308" width="170" height="44" rx="6" fill="#98102A"/><text x="609.0" y="334.9" text-anchor="middle" font-size="14" font-weight="700" fill="#FFFFFF"><tspan x="609.0" dy="0">FAIL: stop this flow</tspan></text><path d="M609 148 L609 76" fill="none" stroke="#FFAB00" stroke-width="2" stroke-dasharray="6 4" marker-end="url(#xf-arrow)"/><path d="M694 50 L770 50 L770 120" fill="none" stroke="#00A972" stroke-width="2" marker-end="url(#xf-arrow)"/><rect x="720" y="124" width="190" height="52" rx="6" fill="#00A972"/><text x="815.0" y="146.5" text-anchor="middle" font-size="14" font-weight="700" fill="#FFFFFF"><tspan x="815.0" dy="0">Continue with</tspan><tspan x="815.0" dy="16.8">the next rows</tspan></text><path d="M694 250 L740 250 L740 182" fill="none" stroke="#FF5F46" stroke-width="2" stroke-dasharray="6 4" marker-end="url(#xf-arrow)"/><path d="M694 262 L770 262 L770 300" fill="none" stroke="#FF5F46" stroke-width="2" stroke-dasharray="6 4" marker-end="url(#xf-arrow)"/><rect x="720" y="304" width="190" height="52" rx="6" fill="#1B5162"/><text x="815.0" y="326.5" text-anchor="middle" font-size="14" font-weight="700" fill="#FFFFFF"><tspan x="815.0" dy="0">Our pattern: a copy</tspan><tspan x="815.0" dy="16.8">goes to quarantine</tspan></text></svg></div>
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
# MAGIC <div class="ds-callout caution"><div class="ds-eyebrow">Good to know</div><div>A materialized view that has expectations is fully recomputed on every run. Keep row rules on streaming tables, as Silver does.</div></div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ### Build the expectations step by step
# MAGIC Click each step. This is the clean QC-results table you complete in Lab 05.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div class="acc-wrap" id="acc1">
# MAGIC <style>
# MAGIC .acc-wrap { max-width: 900px; margin: 0 auto; font-family: sans-serif; --accent: #1B5162; --tint: rgba(27,81,98,0.08); }
# MAGIC .acc-wrap * { box-sizing: border-box; }
# MAGIC .acc-item { border: 2px solid #EEEDE9; border-radius: 8px; margin-bottom: 8px; overflow: hidden; transition: border-color 0.2s; }
# MAGIC .acc-item.open { border-color: var(--accent); }
# MAGIC .acc-header { display: flex; align-items: center; gap: 14px; padding: 14px 18px; cursor: pointer; user-select: none; background: #F9F7F4; }
# MAGIC .acc-item.open .acc-header { background: var(--tint); }
# MAGIC .acc-num { width: 32px; height: 32px; border-radius: 50%; background: #EEEDE9; color: #5E7077; font-size: 14pt; font-weight: 700; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
# MAGIC .acc-item.open .acc-num { background: var(--accent); color: #fff; }
# MAGIC .acc-summary { flex: 1; font-size: 15pt; font-weight: 600; color: #0b2026; }
# MAGIC .acc-chevron { font-size: 14pt; color: #5E7077; transition: transform 0.25s; }
# MAGIC .acc-item.open .acc-chevron { transform: rotate(180deg); color: var(--accent); }
# MAGIC .acc-body { max-height: 0; opacity: 0; overflow: hidden; transition: max-height 0.3s ease, opacity 0.25s ease, padding 0.25s ease; padding: 0 18px 0 64px; font-size: 14pt; line-height: 1.7; color: #0b2026; }
# MAGIC .acc-item.open .acc-body { max-height: 700px; opacity: 1; padding: 4px 18px 18px 64px; }
# MAGIC .acc-body code { background: #EEEDE9; padding: 1px 5px; border-radius: 4px; }
# MAGIC .acc-fix { margin-top: 12px; padding: 10px 14px; border-left: 4px solid var(--accent); background: var(--tint); border-radius: 0 6px 6px 0; font-size: 14pt; }
# MAGIC </style>
# MAGIC <div class="acc-container"></div>
# MAGIC </div>
# MAGIC <script>
# MAGIC (function() {
# MAGIC   var root = document.getElementById('acc1'), box = root.querySelector('.acc-container'), DATA = [{"summary": "Define the streaming table with a constraint block", "detail": "<code>CREATE OR REFRESH STREAMING TABLE silver_inspection_result (</code><br>&nbsp;&nbsp;<code>-- constraints go here</code><br><code>) AS SELECT ... FROM STREAM(inspection_result_prepared)</code>", "fix": "Rules live inside the table definition, so they run on every update."}, {"summary": "DROP a record that cannot be traced: has_lot_id", "detail": "<code>CONSTRAINT has_lot_id EXPECT (lot_id IS NOT NULL) ON VIOLATION DROP ROW</code>", "fix": "A result with no lot cannot be reviewed. It leaves the clean table and lands in quarantine."}, {"summary": "DROP an impossible value, NULL-tolerant: non_negative", "detail": "<code>CONSTRAINT non_negative EXPECT (measured_value IS NULL OR measured_value &gt;= 0) ON VIOLATION DROP ROW</code>", "fix": "A missing value is handled by its own rule, so this one only judges values that are present."}, {"summary": "DROP inverted limits: ordered_limits", "detail": "<code>CONSTRAINT ordered_limits EXPECT (lower_limit IS NULL OR upper_limit IS NULL OR lower_limit &lt;= upper_limit) ON VIOLATION DROP ROW</code>", "fix": "The pH record with its limits swapped fails here: a bad record, not a bad result."}];
# MAGIC   DATA.forEach(function(item, i) {
# MAGIC     var div = document.createElement('div'); div.className = 'acc-item';
# MAGIC     div.innerHTML = '<div class="acc-header"><div class="acc-num">' + (i + 1) + '</div><div class="acc-summary">' + item.summary
# MAGIC       + '</div><div class="acc-chevron">&#9660;</div></div><div class="acc-body"><div style="margin-bottom:10px;">' + item.detail
# MAGIC       + '</div><div class="acc-fix">' + item.fix + '</div></div>';
# MAGIC     div.querySelector('.acc-header').onclick = function() {
# MAGIC       root.querySelectorAll('.acc-item').forEach(function(el) { if (el !== div) el.classList.remove('open'); });
# MAGIC       div.classList.toggle('open');
# MAGIC     };
# MAGIC     box.appendChild(div);
# MAGIC   });
# MAGIC })();
# MAGIC </script>

# COMMAND ----------

# MAGIC %md
# MAGIC **Result** (shortened; the full file has eight rules):
# MAGIC ```sql
# MAGIC CREATE OR REFRESH STREAMING TABLE silver_inspection_result (
# MAGIC   CONSTRAINT has_lot_id     EXPECT (lot_id IS NOT NULL)                                 ON VIOLATION DROP ROW,
# MAGIC   CONSTRAINT non_negative   EXPECT (measured_value IS NULL OR measured_value >= 0)      ON VIOLATION DROP ROW,
# MAGIC   CONSTRAINT ordered_limits EXPECT (lower_limit IS NULL OR upper_limit IS NULL
# MAGIC                                     OR lower_limit <= upper_limit)                      ON VIOLATION DROP ROW
# MAGIC )
# MAGIC AS SELECT * EXCEPT (dq_issues), CASE WHEN is_oos THEN 'OOS' ELSE 'PASS' END AS result_status
# MAGIC FROM STREAM(inspection_result_prepared);
# MAGIC ```

# COMMAND ----------

# MAGIC %md
# MAGIC ## B. Drop the row, but keep it: quarantine

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
# MAGIC <div class="flow-grid" style="grid-template-columns:1fr auto 1fr auto 1fr auto 1fr;"><div class="flow-step" style="--accent:#4299E0;"><div class="flow-num">1</div><div class="flow-label">Bronze row</div></div><div class="flow-arrow">&rarr;</div><div class="flow-step" style="--accent:#00A972;"><div class="flow-num">2</div><div class="flow-label">Prepared view<br>lists its problems</div></div><div class="flow-arrow">&rarr;</div><div class="flow-step" style="--accent:#FFAB00;"><div class="flow-num">3</div><div class="flow-label">Clean table<br>EXPECT ... DROP ROW</div></div><div class="flow-arrow">&rarr;</div><div class="flow-step" style="--accent:#FF5F46;"><div class="flow-num">4</div><div class="flow-label">Quarantine table<br>the same rows, with a reason</div></div></div>
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
# MAGIC <div class="ds-row"><div class="ds-card coral"><div class="ds-card-label">Bad record: quarantine</div><div class="ds-card-title">Titer -1.2 g/L</div><div class="ds-card-para">A negative value cannot be a measurement. Reason: <em>negative measured value</em>.</div></div><div class="ds-card green"><div class="ds-card-label">Bad result: keep and flag</div><div class="ds-card-title">pH 7.6, limit 7.4</div><div class="ds-card-para">A valid measurement outside its limits. Kept, <code>is_oos = true</code>: it is the quality signal.</div></div></div>
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
# MAGIC <div class="ds-callout success"><div class="ds-eyebrow">Zero data loss</div><div class="ds-callout-title">bronze rows = clean rows + quarantine rows</div><div>DROP alone hides bad rows. The quarantine table keeps each one with its reason, so a data steward can fix the source.</div></div>
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
# MAGIC <div class="ds-callout caution row"><div class="ds-callout-icon">!</div><div><div class="ds-eyebrow">NULL-tolerant rules</div><div class="ds-callout-title">Validate a value only when it is there.</div><ul><li><code>approved_at &gt;= submitted_at</code> rejects every change that is not approved yet (NULL is not TRUE).</li><li>Write <code>approved_at IS NULL OR approved_at &gt;= submitted_at</code>.</li><li>Same for columns added later: <code>severity IS NULL OR severity IN (...)</code>.</li></ul></div></div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## C. Change data capture: records that change

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
# MAGIC <div class="ds-row"><div class="ds-card blue"><div class="ds-card-title">Append-only feed</div><ul><li>Every row is new information</li><li>Deviation events, QC results</li><li>Keep them all</li></ul></div><div class="ds-card amber"><div class="ds-card-title">Changing records</div><ul><li>The same record arrives again with new values</li><li>Corrective actions: re-sent at every status change</li><li>You want the latest version, or its history</li></ul></div></div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ### SCD type 1: one row per action, always the latest

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
# MAGIC .dt { width: 100%; border-collapse: collapse; font-size: 14pt; background: #FFFFFF; border-radius: 8px; overflow: hidden; }
# MAGIC .dt th { text-align: left; padding: 8px 8px; background: #EEEDE9; color: #0b2026; font-weight: 700; }
# MAGIC .dt td { padding: 8px 8px; white-space: nowrap; border-top: 1px solid #EEEDE9; color: #0b2026; }
# MAGIC .dt tr.hl td { background: rgba(0,169,114,0.10); font-weight: 600; }
# MAGIC .dt tr.old td { color: #5E7077; }
# MAGIC .dt-title { font-size: 16pt; font-weight: 700; margin: 0 0 8px; }
# MAGIC .dt-note { font-size: 14pt; color: #5E7077; margin-top: 8px; line-height: 1.5; }
# MAGIC .scd { display: grid; grid-template-columns: 1fr auto 1fr auto 1fr; gap: 14px; align-items: center; }
# MAGIC .scd-arrow { font-size: 26pt; color: #618794; }
# MAGIC .scd-tag { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 14pt; font-weight: 700; color: #fff; }
# MAGIC .scd-up { background: #FFAB00; color: #0b2026; } .scd-ins { background: #00A972; }
# MAGIC .dt tr.up td { background: rgba(255,171,0,0.16); } .dt tr.ins td { background: rgba(0,169,114,0.12); }
# MAGIC .scd-legend { display: flex; flex-direction: column; gap: 10px; }
# MAGIC .scd-legend div { padding: 8px 12px; border-radius: 6px; font-size: 14pt; font-weight: 600; color: #fff; }
# MAGIC </style>
# MAGIC <div class="scd"><div class="ds-card blue"><div class="dt-title">Silver after batch 1</div><table class="dt"><tr><th>source_action_id</th><th>action_status</th></tr><tr class=""><td>CA-000012</td><td>OPEN</td></tr></table></div><div class="scd-arrow">+</div><div class="ds-card amber"><div class="dt-title">Batch 2 sends</div><table class="dt"><tr><th>source_action_id</th><th>action_status</th></tr><tr class="up"><td>CA-000012</td><td>IN_PROGRESS <span class="scd-tag scd-up">Update</span></td></tr><tr class="ins"><td>CA-000088</td><td>OPEN <span class="scd-tag scd-ins">Insert</span></td></tr></table></div><div class="scd-arrow">&rarr;</div><div class="ds-card green"><div class="dt-title">Silver after batch 2</div><table class="dt"><tr><th>source_action_id</th><th>action_status</th></tr><tr class="up"><td>CA-000012</td><td>IN_PROGRESS</td></tr><tr class="ins"><td>CA-000088</td><td>OPEN</td></tr></table></div></div>
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
# MAGIC <div class="ds-callout info"><div><strong>CA-000012</strong> was updated in place (OPEN &rarr; IN_PROGRESS). <strong>CA-000088</strong> is new, so it was inserted. No history is kept: this answers &quot;what is the status now?&quot;</div></div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ### SCD type 2: every version, with when it was current

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
# MAGIC .dt { width: 100%; border-collapse: collapse; font-size: 14pt; background: #FFFFFF; border-radius: 8px; overflow: hidden; }
# MAGIC .dt th { text-align: left; padding: 8px 8px; background: #EEEDE9; color: #0b2026; font-weight: 700; }
# MAGIC .dt td { padding: 8px 8px; white-space: nowrap; border-top: 1px solid #EEEDE9; color: #0b2026; }
# MAGIC .dt tr.hl td { background: rgba(0,169,114,0.10); font-weight: 600; }
# MAGIC .dt tr.old td { color: #5E7077; }
# MAGIC .dt-title { font-size: 16pt; font-weight: 700; margin: 0 0 8px; }
# MAGIC .dt-note { font-size: 14pt; color: #5E7077; margin-top: 8px; line-height: 1.5; }
# MAGIC .scd { display: grid; grid-template-columns: 1fr auto 1fr auto 1fr; gap: 14px; align-items: center; }
# MAGIC .scd-arrow { font-size: 26pt; color: #618794; }
# MAGIC .scd-tag { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 14pt; font-weight: 700; color: #fff; }
# MAGIC .scd-up { background: #FFAB00; color: #0b2026; } .scd-ins { background: #00A972; }
# MAGIC .dt tr.up td { background: rgba(255,171,0,0.16); } .dt tr.ins td { background: rgba(0,169,114,0.12); }
# MAGIC .scd-legend { display: flex; flex-direction: column; gap: 10px; }
# MAGIC .scd-legend div { padding: 8px 12px; border-radius: 6px; font-size: 14pt; font-weight: 600; color: #fff; }
# MAGIC </style>
# MAGIC <div class="ds-row"><div class="ds-card green" style="flex:2;"><div class="dt-title">silver_corrective_action_history (SCD type 2)</div><table class="dt"><tr><th>source_action_id</th><th>action_status</th><th>__START_AT</th><th>__END_AT</th></tr><tr class="old"><td>CA-000012</td><td>OPEN</td><td>batch 1</td><td>batch 2</td></tr><tr class="old"><td>CA-000012</td><td>IN_PROGRESS</td><td>batch 2</td><td>batch 3</td></tr><tr class="hl"><td>CA-000012</td><td>COMPLETED</td><td>batch 3</td><td>NULL</td></tr></table></div><div style="flex:1;align-self:center;"><div class="scd-legend"><div style="background:#00A972;">__END_AT is NULL: the current row</div><div style="background:#FF5F46;">__END_AT filled: history (no longer current)</div></div></div></div>
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
# MAGIC <div class="ds-callout info"><div>The same action after all three batches. Each status keeps its validity window, so you can answer &quot;how long was it IN_PROGRESS?&quot; Current rows: <code>WHERE __END_AT IS NULL</code>.</div></div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## D. AUTO CDC INTO, clause by clause

# COMMAND ----------

# MAGIC %md
# MAGIC ```sql
# MAGIC CREATE OR REFRESH STREAMING TABLE silver_corrective_action;
# MAGIC
# MAGIC CREATE FLOW corrective_action_current AS AUTO CDC INTO silver_corrective_action
# MAGIC FROM STREAM(corrective_action_changes)
# MAGIC KEYS (source_action_id)                          -- which row a change belongs to
# MAGIC SEQUENCE BY STRUCT(source_file, status_rank)     -- which version is newer
# MAGIC COLUMNS * EXCEPT (status_rank)                   -- which columns land in the table
# MAGIC STORED AS SCD TYPE 1;                            -- latest only (TYPE 2 = history)
# MAGIC ```

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
# MAGIC <div class="ds-row"><div class="ds-card blue"><div class="ds-card-title">No MERGE to write</div><div class="ds-card-para">AUTO CDC replaces a hand-written <code>MERGE</code> with keys, ordering and late-row handling built in.</div></div><div class="ds-card green"><div class="ds-card-title">Order by the source</div><div class="ds-card-para">A late or re-sent row never overwrites a newer one. With a real source timestamp: <code>SEQUENCE BY updated_at</code>.</div></div><div class="ds-card amber"><div class="ds-card-title">Deletes, when sent</div><div class="ds-card-para"><code>APPLY AS DELETE WHEN operation = 'DELETE'</code>. Our feed never sends deletes, so we leave it out.</div></div></div>
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
# MAGIC var QZ=[{"q": "A QC record has <code>measured_value = -1.2</code>. What should Silver do?", "opts": ["Keep it and flag OOS", "Drop it and keep it in quarantine", "Fail the pipeline"], "ans": 1, "fb": "It is a bad record, not a bad result: drop it from the clean table, keep it in quarantine with a reason."}, {"q": "Which action fits a release gate that must stop promotion?", "opts": ["WARN", "DROP ROW", "FAIL UPDATE"], "ans": 2, "fb": "FAIL UPDATE stops that flow; the QA target uses it."}, {"q": "You need to know how long each corrective action stayed OPEN. Which storage?", "opts": ["SCD type 1", "SCD type 2"], "ans": 1, "fb": "Type 2 keeps every version with __START_AT and __END_AT."}];
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
# MAGIC 1. Wrote expectations with <code>CONSTRAINT ... EXPECT</code> and chose warn, drop or fail
# MAGIC 2. Kept rejected rows in quarantine, so nothing is lost, and wrote NULL-tolerant rules
# MAGIC 3. Saw how change data capture handles records that change, with SCD type 1 and type 2
# MAGIC 4. Read an <code>AUTO CDC INTO</code> statement clause by clause
# MAGIC
# MAGIC ### Next Steps
# MAGIC
# MAGIC In **05 Lab - Silver Quality and Quarantine**, you write the expectations for two Silver tables and read the AUTO CDC flow on real data.
