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
# MAGIC <div class="ds-banner info"><div class="ds-banner-icon">5</div><div><div class="ds-banner-title">Lab 05 &middot; Silver: quality and conformance</div><div class="ds-banner-tagline">15 minutes &middot; two Silver tables: rules become expectations</div></div></div>
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
# MAGIC <div style="font-size:20pt;font-weight:700;margin-bottom:14px;">The one distinction that matters in Silver</div><div class="ds-row"><div class="ds-card coral"><div class="ds-card-label">Quarantine</div><div class="ds-card-title">Bad record</div><ul><li>No lot id, no site</li><li><code>'&lt;LOQ'</code> where a number belongs</li><li>Negative titer, inverted spec limits</li></ul></div><div class="ds-card green"><div class="ds-card-label">Keep + flag</div><div class="ds-card-title">Bad result</div><ul><li>Valid record, value out of spec</li><li><code>is_oos = true</code></li><li>It is the quality signal: never hide it</li></ul></div></div>
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
# MAGIC <div class="flow-grid" style="grid-template-columns:1fr auto 1fr auto 1fr auto 1fr auto 1fr;"><div class="flow-step" style="--accent:#4299E0;"><div class="flow-num">1</div><div class="flow-label">Bronze row<br><code>DEV-2026-0017</code></div></div><div class="flow-arrow">&rarr;</div><div class="flow-step" style="--accent:#00A972;"><div class="flow-num">2</div><div class="flow-label"><code>site_code</code> is NULL</div></div><div class="flow-arrow">&rarr;</div><div class="flow-step" style="--accent:#FFAB00;"><div class="flow-num">3</div><div class="flow-label"><code>has_site_code</code><br>fails</div></div><div class="flow-arrow">&rarr;</div><div class="flow-step" style="--accent:#FF5F46;"><div class="flow-num">4</div><div class="flow-label">Dropped from<br>clean table</div></div><div class="flow-arrow">&rarr;</div><div class="flow-step" style="--accent:#98102A;"><div class="flow-num">5</div><div class="flow-label">Kept in quarantine<br>reason: missing site_code</div></div></div>
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
# MAGIC <div class="ds-callout info"><div class="ds-eyebrow">Trace one row</div><div>Every rule is evaluated on every row. One failure is enough to leave the clean path; the quarantine row keeps <em>all</em> reasons.</div></div>
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
# MAGIC <div class="flow-grid" style="grid-template-columns:1fr auto 1fr auto 1fr auto 1fr auto 1fr;"><div class="flow-step" style="--accent:#4299E0;"><div class="flow-num">1</div><div class="flow-label">QC-results Silver:<br>uncomment, write <code>EXPECT</code>s</div></div><div class="flow-arrow">&rarr;</div><div class="flow-step" style="--accent:#00A972;"><div class="flow-num">2</div><div class="flow-label">Change-control Silver:<br>same, NULL-tolerant</div></div><div class="flow-arrow">&rarr;</div><div class="flow-step" style="--accent:#FFAB00;"><div class="flow-num">3</div><div class="flow-label">Uncomment prebuilt<br>change-control Gold</div></div><div class="flow-arrow">&rarr;</div><div class="flow-step" style="--accent:#FF5F46;"><div class="flow-num">4</div><div class="flow-label">Run pipeline</div></div><div class="flow-arrow">&rarr;</div><div class="flow-step" style="--accent:#98102A;"><div class="flow-num">5</div><div class="flow-label">Checkpoint</div></div></div>
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
# MAGIC <div class="ds-callout info"><div class="ds-eyebrow">Translate a rule</div><div><code>CASE WHEN site_code IS NULL THEN 'missing site_code' END</code> &nbsp;&rarr;&nbsp; <code>CONSTRAINT has_site_code EXPECT (site_code IS NOT NULL) ON VIOLATION DROP ROW</code></div></div>
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
# MAGIC <div class="ds-callout info"><div class="ds-eyebrow">Your file: silver/silver_inspection_result.sql</div><div class="ds-callout-title">QC results: bad record vs bad result</div><ul><li>Quarantine: missing ids, a value that is not a number or is negative, missing or inverted spec limits.</li><li>Keep and flag: a valid result outside its limits (<code>is_oos = true</code>).</li><li>Bronze keeps <code>'&lt;LOQ'</code> as text. Silver's <code>try_cast</code> returns NULL, the row is quarantined as <em>measured_value not numeric</em>, and <code>measured_value_raw</code> keeps the original text.</li></ul></div>
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
# MAGIC <div class="ds-row"><div class="ds-card blue"><div class="ds-card-label">Prebuilt, read the AUTO CDC flow</div><div class="ds-card-title">Corrective actions</div><div class="ds-card-para"><code>AUTO CDC INTO</code> keeps one current row per action: <code>KEYS</code> = which row, <code>SEQUENCE BY</code> = which version is newer, <code>SCD TYPE 1</code> = keep only the latest.</div></div><div class="ds-card green"><div class="ds-card-label">Your second file: silver/silver_change_control.sql</div><div class="ds-card-title">Change controls</div><div class="ds-card-para">Messy states (<code>appr</code>, <code>Approved</code>) are mapped for you. Write the milestone rules NULL-tolerant: <code>approved_at IS NULL OR approved_at &gt;= submitted_at</code>. Then uncomment the prebuilt <code>gold_change_control_cycle_time.sql</code>.</div></div></div>
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
# MAGIC <div class="ds-callout info"><div class="ds-eyebrow">Need help?</div><div>Stuck on syntax? Open <strong>Genie Code</strong> (the assistant panel) and ask, for example, <em>&quot;convert this CREATE TABLE into a streaming table that reads with Auto Loader&quot;</em>. Then compare with the CODE ANSWER.</div></div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC Write your code in the pipeline editor. Stuck? Expand a CODE ANSWER below, compare, then continue.

# COMMAND ----------

# MAGIC %md
# MAGIC <details><summary><strong>CODE ANSWER: silver_inspection_result.sql</strong> (try first, then expand)</summary>
# MAGIC
# MAGIC ```sql
# MAGIC -- ============================================================================
# MAGIC -- SILVER | inspection results
# MAGIC -- Grain  : one row per valid QC measurement
# MAGIC -- Key distinction:
# MAGIC --   * a BAD RECORD (no lot, '<LOQ' text, negative titer) -> quarantine
# MAGIC --   * a BAD RESULT (valid record, value outside spec)    -> kept, flagged is_oos
# MAGIC -- ============================================================================
# MAGIC
# MAGIC CREATE TEMPORARY VIEW inspection_result_prepared AS
# MAGIC WITH typed AS (            -- Bronze is all STRING: cast here. try_* gives NULL, never an error
# MAGIC   SELECT measured_value AS measured_value_raw,   -- the text exactly as sent, e.g. '<LOQ'
# MAGIC          * EXCEPT (measured_at, measured_value, lower_limit, upper_limit),
# MAGIC     try_to_timestamp(measured_at, 'yyyy-MM-dd HH:mm:ss') AS measured_at,
# MAGIC     try_cast(measured_value AS DOUBLE) AS measured_value,
# MAGIC     try_cast(lower_limit AS DOUBLE) AS lower_limit,
# MAGIC     try_cast(upper_limit AS DOUBLE) AS upper_limit
# MAGIC   FROM STREAM(bronze_inspection_result)
# MAGIC )
# MAGIC SELECT
# MAGIC   source_sample_id,
# MAGIC   lot_id,
# MAGIC   site_code,
# MAGIC   test_code,
# MAGIC   measured_value,
# MAGIC   measured_value_raw,
# MAGIC   lower_limit,
# MAGIC   upper_limit,
# MAGIC   measured_at,
# MAGIC   (measured_value < lower_limit OR measured_value > upper_limit) AS is_oos,
# MAGIC   source_file,
# MAGIC   ingested_at,
# MAGIC   filter(array(
# MAGIC     CASE WHEN source_sample_id IS NULL THEN 'missing source_sample_id' END,
# MAGIC     CASE WHEN lot_id IS NULL           THEN 'missing lot_id' END,
# MAGIC     CASE WHEN site_code IS NULL        THEN 'missing site_code' END,
# MAGIC     CASE WHEN measured_at IS NULL      THEN 'missing measured_at' END,
# MAGIC     CASE WHEN measured_value IS NULL   THEN 'measured_value not numeric' END,
# MAGIC     CASE WHEN measured_value < 0       THEN 'negative measured_value' END,
# MAGIC     CASE WHEN lower_limit IS NULL OR upper_limit IS NULL THEN 'missing spec limits' END,
# MAGIC     CASE WHEN lower_limit > upper_limit THEN 'lower_limit above upper_limit' END
# MAGIC   ), x -> x IS NOT NULL) AS dq_issues
# MAGIC FROM typed;
# MAGIC
# MAGIC CREATE OR REFRESH STREAMING TABLE silver_inspection_result (
# MAGIC   CONSTRAINT has_sample_id     EXPECT (source_sample_id IS NOT NULL) ON VIOLATION DROP ROW,
# MAGIC   CONSTRAINT has_lot_id        EXPECT (lot_id IS NOT NULL)           ON VIOLATION DROP ROW,
# MAGIC   CONSTRAINT has_site_code     EXPECT (site_code IS NOT NULL)        ON VIOLATION DROP ROW,
# MAGIC   CONSTRAINT has_measured_at   EXPECT (measured_at IS NOT NULL)      ON VIOLATION DROP ROW,
# MAGIC   CONSTRAINT numeric_value     EXPECT (measured_value IS NOT NULL)   ON VIOLATION DROP ROW,
# MAGIC   CONSTRAINT non_negative      EXPECT (measured_value IS NULL OR measured_value >= 0) ON VIOLATION DROP ROW,
# MAGIC   CONSTRAINT has_spec_limits   EXPECT (lower_limit IS NOT NULL AND upper_limit IS NOT NULL) ON VIOLATION DROP ROW,
# MAGIC   CONSTRAINT ordered_limits    EXPECT (lower_limit IS NULL OR upper_limit IS NULL OR lower_limit <= upper_limit) ON VIOLATION DROP ROW
# MAGIC )
# MAGIC COMMENT "Validated QC results with an out-of-spec flag. Grain: one row per measurement."
# MAGIC TBLPROPERTIES ('quality' = 'silver')
# MAGIC AS SELECT * EXCEPT (dq_issues), CASE WHEN is_oos THEN 'OOS' ELSE 'PASS' END AS result_status
# MAGIC FROM STREAM(inspection_result_prepared);
# MAGIC
# MAGIC CREATE OR REFRESH STREAMING TABLE silver_inspection_result_quarantine
# MAGIC COMMENT "QC rows that failed at least one record-quality rule, with the reasons."
# MAGIC TBLPROPERTIES ('quality' = 'quarantine')
# MAGIC AS SELECT *, array_join(dq_issues, '; ') AS quarantine_reason
# MAGIC FROM STREAM(inspection_result_prepared)
# MAGIC WHERE size(dq_issues) > 0;
# MAGIC ```
# MAGIC
# MAGIC </details>

# COMMAND ----------

# MAGIC %md
# MAGIC <details><summary><strong>CODE ANSWER: silver_change_control.sql</strong> (try first, then expand)</summary>
# MAGIC
# MAGIC ```sql
# MAGIC -- ============================================================================
# MAGIC -- SILVER | change controls
# MAGIC -- Grain  : one row per valid workflow snapshot (a change re-sends as it moves)
# MAGIC -- Teaches: map messy source states to one vocabulary + milestone ordering.
# MAGIC -- ============================================================================
# MAGIC
# MAGIC CREATE TEMPORARY VIEW change_control_prepared AS
# MAGIC WITH typed AS (            -- Bronze is all STRING: cast here. try_* gives NULL, never an error
# MAGIC   SELECT * EXCEPT (submitted_at, approved_at, effective_at, closed_at),
# MAGIC     try_to_timestamp(submitted_at, 'yyyy-MM-dd HH:mm:ss') AS submitted_at,
# MAGIC     try_to_timestamp(approved_at, 'yyyy-MM-dd HH:mm:ss') AS approved_at,
# MAGIC     try_to_timestamp(effective_at, 'yyyy-MM-dd HH:mm:ss') AS effective_at,
# MAGIC     try_to_timestamp(closed_at, 'yyyy-MM-dd HH:mm:ss') AS closed_at
# MAGIC   FROM STREAM(bronze_change_control)
# MAGIC ),
# MAGIC mapped AS (
# MAGIC   SELECT
# MAGIC     *,
# MAGIC     CASE upper(trim(workflow_status))
# MAGIC       WHEN 'SUBMITTED' THEN 'SUBMITTED'  WHEN 'SUBMIT' THEN 'SUBMITTED'
# MAGIC       WHEN 'APPROVED'  THEN 'APPROVED'   WHEN 'APPR'   THEN 'APPROVED'
# MAGIC       WHEN 'IMPLEMENTED' THEN 'IMPLEMENTED' WHEN 'IMPL' THEN 'IMPLEMENTED'
# MAGIC       WHEN 'CLOSED'    THEN 'CLOSED'
# MAGIC       WHEN 'REJECTED'  THEN 'REJECTED'
# MAGIC     END AS workflow_status_std
# MAGIC   FROM typed
# MAGIC )
# MAGIC SELECT
# MAGIC   source_change_id,
# MAGIC   site_code,
# MAGIC   product_code,
# MAGIC   change_type,
# MAGIC   workflow_status_std AS workflow_status,
# MAGIC   workflow_status     AS workflow_status_raw,
# MAGIC   submitted_at,
# MAGIC   approved_at,
# MAGIC   effective_at,
# MAGIC   closed_at,
# MAGIC   source_file,
# MAGIC   ingested_at,
# MAGIC   filter(array(
# MAGIC     CASE WHEN source_change_id IS NULL     THEN 'missing source_change_id' END,
# MAGIC     CASE WHEN site_code IS NULL            THEN 'missing site_code' END,
# MAGIC     CASE WHEN submitted_at IS NULL         THEN 'missing submitted_at' END,
# MAGIC     CASE WHEN workflow_status_std IS NULL  THEN 'unknown workflow_status' END,
# MAGIC     CASE WHEN approved_at  < submitted_at  THEN 'approved_at before submitted_at' END,
# MAGIC     CASE WHEN effective_at < approved_at   THEN 'effective_at before approved_at' END,
# MAGIC     CASE WHEN closed_at    < submitted_at  THEN 'closed_at before submitted_at' END
# MAGIC   ), x -> x IS NOT NULL) AS dq_issues
# MAGIC FROM mapped;
# MAGIC
# MAGIC CREATE OR REFRESH STREAMING TABLE silver_change_control (
# MAGIC   CONSTRAINT has_change_id    EXPECT (source_change_id IS NOT NULL) ON VIOLATION DROP ROW,
# MAGIC   CONSTRAINT has_site_code    EXPECT (site_code IS NOT NULL)        ON VIOLATION DROP ROW,
# MAGIC   CONSTRAINT has_submitted_at EXPECT (submitted_at IS NOT NULL)     ON VIOLATION DROP ROW,
# MAGIC   CONSTRAINT known_status     EXPECT (workflow_status IS NOT NULL)  ON VIOLATION DROP ROW,
# MAGIC   -- Milestones may be missing (not reached yet) but never out of order.
# MAGIC   CONSTRAINT approved_after_submitted  EXPECT (approved_at IS NULL OR approved_at >= submitted_at)  ON VIOLATION DROP ROW,
# MAGIC   CONSTRAINT effective_after_approved  EXPECT (effective_at IS NULL OR approved_at IS NULL OR effective_at >= approved_at) ON VIOLATION DROP ROW,
# MAGIC   CONSTRAINT closed_after_submitted    EXPECT (closed_at IS NULL OR closed_at >= submitted_at)      ON VIOLATION DROP ROW
# MAGIC )
# MAGIC COMMENT "Validated change-control snapshots. Grain: one row per change per file."
# MAGIC TBLPROPERTIES ('quality' = 'silver')
# MAGIC AS SELECT * EXCEPT (dq_issues) FROM STREAM(change_control_prepared);
# MAGIC
# MAGIC CREATE OR REFRESH STREAMING TABLE silver_change_control_quarantine
# MAGIC COMMENT "Change-control rows that failed at least one rule, with the reasons."
# MAGIC TBLPROPERTIES ('quality' = 'quarantine')
# MAGIC AS SELECT *, array_join(dq_issues, '; ') AS quarantine_reason
# MAGIC FROM STREAM(change_control_prepared)
# MAGIC WHERE size(dq_issues) > 0;
# MAGIC ```
# MAGIC
# MAGIC </details>

# COMMAND ----------

# MAGIC %md
# MAGIC ### SQL and Python in one pipeline (5 minutes)
# MAGIC One pipeline can mix `.sql` and `.py` files: SDP builds one graph from all of them. To show it, add the **batch record** feed (MES) in Python. Lab 06 uses it: `gold_oos_events` takes product and lot dates from `silver_batch_record`.
# MAGIC
# MAGIC 1. In the pipeline editor, next to `bronze/`, `silver/` and `gold/`, create a folder `python/` (**+** &rarr; **Create folder**).
# MAGIC 2. In `python/`, **+** &rarr; **Create file** &rarr; `batch_record.py`. Paste the code block below. It defines both tables, `bronze_batch_record` and `silver_batch_record`.
# MAGIC 3. Run the pipeline with the rest of your Silver work (next step).
# MAGIC
# MAGIC | In SQL | In Python (`from pyspark import pipelines as dp`) |
# MAGIC |---|---|
# MAGIC | `CREATE OR REFRESH STREAMING TABLE t AS ...` | `@dp.table(name="t")` on a function that returns a **streaming** DataFrame |
# MAGIC | `CREATE OR REFRESH MATERIALIZED VIEW t AS ...` | `@dp.materialized_view(name="t")` on a function that returns a batch DataFrame |
# MAGIC | `FROM STREAM read_files(path, format => 'csv', ...)` | `spark.readStream.format("cloudFiles").option("cloudFiles.format", "csv").load(path)` |
# MAGIC | `FROM STREAM(bronze_x)` | `spark.readStream.table("bronze_x")` |
# MAGIC | `CONSTRAINT r EXPECT (cond) ON VIOLATION DROP ROW` | `@dp.expect_or_drop("r", "cond")`, or `@dp.expect_all_or_drop({...})` for several |
# MAGIC | `:landing_root` (pipeline parameter) | `spark.conf.get("landing_root")` (pipeline **Configuration**, already set by the bundle) |

# COMMAND ----------

# MAGIC %md
# MAGIC **`python/batch_record.py`**
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
# MAGIC
# MAGIC
# MAGIC @dp.table(
# MAGIC     name="bronze_batch_record",
# MAGIC     comment="Raw batch records from the MES feed (synthetic).",
# MAGIC     table_properties={"quality": "bronze", "pipelines.reset.allowed": "false"},
# MAGIC )
# MAGIC def bronze_batch_record():
# MAGIC     return bronze_feed(
# MAGIC         "batch_record_feed",
# MAGIC         "lot_id STRING, product_code STRING, site_code STRING, process_step STRING, started_at STRING, "
# MAGIC         "ended_at STRING, planned_yield_g STRING, actual_yield_g STRING",   # all STRING: Silver casts
# MAGIC     )
# MAGIC
# MAGIC
# MAGIC @dp.table(
# MAGIC     name="silver_batch_record",
# MAGIC     comment="Validated batch records with yield %. Grain: one row per lot.",
# MAGIC     table_properties={"quality": "silver"},
# MAGIC )
# MAGIC @dp.expect_all_or_drop({
# MAGIC     "has_lot_id": "lot_id IS NOT NULL",
# MAGIC     "has_dates": "started_at IS NOT NULL AND ended_at IS NOT NULL",
# MAGIC     "positive_planned_yield": "planned_yield_g > 0",
# MAGIC })
# MAGIC def silver_batch_record():
# MAGIC     return (
# MAGIC         spark.readStream.table("bronze_batch_record")  # noqa: F821
# MAGIC         # Bronze is all STRING: cast here, in Silver. try_* returns NULL instead of failing on bad values.
# MAGIC         .withColumn("started_at", F.expr("try_to_timestamp(started_at, 'yyyy-MM-dd HH:mm:ss')"))
# MAGIC         .withColumn("ended_at", F.expr("try_to_timestamp(ended_at, 'yyyy-MM-dd HH:mm:ss')"))
# MAGIC         .withColumn("planned_yield_g", F.expr("try_cast(planned_yield_g AS DOUBLE)"))
# MAGIC         .withColumn("actual_yield_g", F.expr("try_cast(actual_yield_g AS DOUBLE)"))
# MAGIC         .withColumn("yield_pct", F.round(F.col("actual_yield_g") / F.col("planned_yield_g") * 100, 1))
# MAGIC         .drop("_rescued_data")
# MAGIC     )
# MAGIC ```

# COMMAND ----------

# MAGIC %md
# MAGIC ### Checkpoint after batch 1: run the pipeline first
# MAGIC Run the pipeline (**Run pipeline**, not full refresh). When the update finishes, run the next cell: every row should show a check mark.

# COMMAND ----------

checkpoint(run=1, layer='silver')

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
# MAGIC <div class="ds-callout info"><div class="ds-eyebrow">Read the prebuilt file: silver/silver_corrective_action.sql</div><div class="ds-callout-title">The AUTO CDC flow from Lecture 04, on real data</div><ul><li><code>KEYS (source_action_id)</code>: one current row per action.</li><li><code>SEQUENCE BY STRUCT(source_file, status_rank)</code>: the newer snapshot wins.</li><li><code>STORED AS SCD TYPE 1</code>: keep only the latest version.</li></ul></div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ### AUTO CDC at work
# MAGIC The corrective-action feed re-sends an action each time its status changes. The event table keeps every snapshot; AUTO CDC keeps one current row per action.

# COMMAND ----------

display(spark.sql(f'''SELECT (SELECT count(*) FROM {FQ}.silver_corrective_action_event) AS snapshots_received,
       (SELECT count(DISTINCT source_action_id) FROM {FQ}.silver_corrective_action_event) AS distinct_actions,
       (SELECT count(*) FROM {FQ}.silver_corrective_action) AS current_rows_auto_cdc'''))

# COMMAND ----------

# MAGIC %md
# MAGIC ### Explore: why was a row quarantined?

# COMMAND ----------

display(spark.sql(f'''SELECT source_sample_id, lot_id, test_code, measured_value, quarantine_reason, source_file
FROM {FQ}.silver_inspection_result_quarantine'''))

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
# MAGIC <div class="ds-callout info"><div class="ds-eyebrow">See it in the pipeline</div><ul><li>Bottom panel &rarr; <strong>Tables</strong> &rarr; select <code>silver_inspection_result</code> &rarr; <strong>Table metrics</strong>.</li><li><strong>Output records</strong>: rows written. <strong>Expectations</strong>: met / unmet. <strong>Dropped</strong>: rows a <code>DROP ROW</code> rule kept out.</li><li>After batch 1 the QC file is clean: 1,539 read, 1,539 written, 0 dropped. Batch 2 in Lab 07 brings the bad rows.</li><li>Click the expectations link for per-rule counts: named constraints (<code>has_lot_id</code>, <code>ordered_limits</code>) read like a checklist.</li></ul></div>
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
# MAGIC <div class="ds-callout success"><div class="ds-eyebrow">Takeaway</div><div class="ds-callout-title">Rules are written once and enforced every run.</div><ul><li>Clean rows flow on; bad rows wait in quarantine with a reason.</li><li>Out-of-spec results are data, not errors.</li></ul></div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ## Optional: if you have time
# MAGIC The core lab ends above. Write the corrective-action Silver yourself, and add AUTO CDC history. The pipeline already runs the prebuilt version, so skipping this costs nothing.
# MAGIC
# MAGIC 1. Corrective actions: <code>pipeline_files_optional/silver/silver_corrective_action.sql</code>. Rules plus the AUTO CDC key and SCD type.
# MAGIC 2. AUTO CDC with history: copy <code>pipeline_files_optional/silver/silver_corrective_action_cdc.sql</code> into your pipeline's <code>silver/</code> folder (SCD type 2), run, then query <code>silver_corrective_action_history</code>: one row per status change.
# MAGIC 3. Swap a practice copy in for the prebuilt file, fill the blanks, run, re-run the checkpoint.

# COMMAND ----------

# MAGIC %md
# MAGIC <details><summary><strong>CODE ANSWER: silver_corrective_action.sql</strong> (try first, then expand)</summary>
# MAGIC
# MAGIC ```sql
# MAGIC -- ============================================================================
# MAGIC -- SILVER | corrective actions
# MAGIC -- The feed re-sends an action every time its status changes (snapshots).
# MAGIC --   silver_corrective_action_event : every valid snapshot   (streaming table)
# MAGIC --   silver_corrective_action       : latest snapshot per id (AUTO CDC, SCD type 1)
# MAGIC -- ============================================================================
# MAGIC
# MAGIC CREATE TEMPORARY VIEW corrective_action_prepared AS
# MAGIC WITH typed AS (            -- Bronze is all STRING: cast here. try_* gives NULL, never an error
# MAGIC   SELECT * EXCEPT (created_at, completed_at),
# MAGIC     try_to_timestamp(created_at, 'yyyy-MM-dd HH:mm:ss') AS created_at,
# MAGIC     try_to_timestamp(completed_at, 'yyyy-MM-dd HH:mm:ss') AS completed_at
# MAGIC   FROM STREAM(bronze_corrective_action)
# MAGIC )
# MAGIC SELECT
# MAGIC   source_action_id,
# MAGIC   source_case_id,
# MAGIC   action_code,
# MAGIC   upper(regexp_replace(trim(action_status), '[ -]+', '_')) AS action_status,
# MAGIC   assigned_group,
# MAGIC   created_at,
# MAGIC   completed_at,
# MAGIC   source_file,
# MAGIC   ingested_at,
# MAGIC   filter(array(
# MAGIC     CASE WHEN source_action_id IS NULL THEN 'missing source_action_id' END,
# MAGIC     CASE WHEN source_case_id IS NULL   THEN 'missing source_case_id' END,
# MAGIC     CASE WHEN created_at IS NULL       THEN 'missing created_at' END,
# MAGIC     CASE WHEN upper(regexp_replace(trim(action_status), '[ -]+', '_'))
# MAGIC               NOT IN ('OPEN','IN_PROGRESS','COMPLETED','CANCELLED')
# MAGIC               OR action_status IS NULL THEN 'unknown action_status' END,
# MAGIC     CASE WHEN completed_at < created_at THEN 'completed_at before created_at' END
# MAGIC   ), x -> x IS NOT NULL) AS dq_issues
# MAGIC FROM typed;
# MAGIC
# MAGIC CREATE OR REFRESH STREAMING TABLE silver_corrective_action_event (
# MAGIC   CONSTRAINT has_action_id  EXPECT (source_action_id IS NOT NULL) ON VIOLATION DROP ROW,
# MAGIC   CONSTRAINT has_case_id    EXPECT (source_case_id IS NOT NULL)   ON VIOLATION DROP ROW,
# MAGIC   CONSTRAINT has_created_at EXPECT (created_at IS NOT NULL)       ON VIOLATION DROP ROW,
# MAGIC   CONSTRAINT known_status   EXPECT (action_status IN ('OPEN','IN_PROGRESS','COMPLETED','CANCELLED')) ON VIOLATION DROP ROW,
# MAGIC   CONSTRAINT completed_after_created EXPECT (completed_at IS NULL OR completed_at >= created_at)      ON VIOLATION DROP ROW
# MAGIC )
# MAGIC COMMENT "Every valid corrective-action snapshot. Grain: one row per action per file."
# MAGIC TBLPROPERTIES ('quality' = 'silver')
# MAGIC AS SELECT * EXCEPT (dq_issues) FROM STREAM(corrective_action_prepared);
# MAGIC
# MAGIC CREATE OR REFRESH STREAMING TABLE silver_corrective_action_quarantine
# MAGIC COMMENT "Corrective-action rows that failed at least one rule, with the reasons."
# MAGIC TBLPROPERTIES ('quality' = 'quarantine')
# MAGIC AS SELECT *, array_join(dq_issues, '; ') AS quarantine_reason
# MAGIC FROM STREAM(corrective_action_prepared)
# MAGIC WHERE size(dq_issues) > 0;
# MAGIC
# MAGIC -- Latest state per action with AUTO CDC (SCD type 1): the platform keeps one row per key and applies
# MAGIC -- each new snapshot in sequence order -- no hand-written dedupe, and late or re-sent rows are handled.
# MAGIC -- The feed has no source timestamp, so the sequence is (file, status rank): latest file wins, and inside
# MAGIC -- one file the most advanced status wins. With a real source updated_at: SEQUENCE BY source_updated_at.
# MAGIC CREATE TEMPORARY VIEW corrective_action_changes AS
# MAGIC SELECT *,
# MAGIC        CASE action_status WHEN 'OPEN' THEN 1 WHEN 'IN_PROGRESS' THEN 2 ELSE 3 END AS status_rank
# MAGIC FROM STREAM(silver_corrective_action_event);
# MAGIC
# MAGIC CREATE OR REFRESH STREAMING TABLE silver_corrective_action
# MAGIC COMMENT "Current state of each corrective action, maintained by AUTO CDC (SCD type 1). Grain: one row per source_action_id."
# MAGIC TBLPROPERTIES ('quality' = 'silver');
# MAGIC
# MAGIC CREATE FLOW corrective_action_current AS AUTO CDC INTO silver_corrective_action
# MAGIC FROM STREAM(corrective_action_changes)
# MAGIC KEYS (source_action_id)
# MAGIC SEQUENCE BY STRUCT(source_file, status_rank)
# MAGIC COLUMNS * EXCEPT (status_rank)
# MAGIC STORED AS SCD TYPE 1;
# MAGIC ```
# MAGIC
# MAGIC </details>

# COMMAND ----------

# MAGIC %md
# MAGIC ```sql
# MAGIC -- ============================================================================
# MAGIC -- OPTIONAL (Lab 05) / S6 | AUTO CDC with history (SCD type 2)
# MAGIC -- Same changes as the core file silver/silver_corrective_action.sql, kept as history:
# MAGIC --   silver_corrective_action_history : every status change, with __START_AT / __END_AT
# MAGIC -- Current rows: WHERE __END_AT IS NULL (equals silver_corrective_action).
# MAGIC -- Reuses the temporary view corrective_action_changes from the core file.
# MAGIC -- ============================================================================
# MAGIC CREATE OR REFRESH STREAMING TABLE silver_corrective_action_history
# MAGIC COMMENT "Status history per corrective action via AUTO CDC (SCD type 2). Current rows: __END_AT IS NULL.";
# MAGIC
# MAGIC CREATE FLOW corrective_action_history_flow AS AUTO CDC INTO silver_corrective_action_history
# MAGIC FROM STREAM(corrective_action_changes)
# MAGIC KEYS (source_action_id)
# MAGIC SEQUENCE BY STRUCT(source_file, status_rank)
# MAGIC COLUMNS * EXCEPT (status_rank)
# MAGIC STORED AS SCD TYPE 2
# MAGIC TRACK HISTORY ON action_status, completed_at;
# MAGIC ```

# COMMAND ----------

display(spark.sql(f'''SELECT source_action_id, action_status, __START_AT, __END_AT
FROM {FQ}.silver_corrective_action_history
WHERE source_action_id IN (SELECT source_action_id FROM {FQ}.silver_corrective_action_history GROUP BY 1 HAVING count(*) > 1 LIMIT 3)
ORDER BY source_action_id, __START_AT'''))
