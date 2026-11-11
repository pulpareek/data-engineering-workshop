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
# MAGIC <div class="ds-banner info"><div class="ds-banner-icon">&#9670;</div><div><div class="ds-banner-title">Lot Release Readiness: from raw files to a trusted answer</div><div class="ds-banner-tagline">Lakeflow Spark Declarative Pipelines workshop &middot; IOPS Quality &middot; 3.5 hours</div></div></div>
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
# MAGIC <div class="ds-row"><div class="ds-card coral"><div class="ds-card-label">QMS</div><div class="ds-card-title">Deviations</div><div class="ds-card-para">What went wrong, is it still open, is it overdue?</div></div><div class="ds-card amber"><div class="ds-card-label">QMS</div><div class="ds-card-title">Corrective actions</div><div class="ds-card-para">Are the fixes done?</div></div><div class="ds-card blue"><div class="ds-card-label">Change mgmt</div><div class="ds-card-title">Change controls</div><div class="ds-card-para">Did something change while the lot was made?</div></div><div class="ds-card green"><div class="ds-card-label">LIMS</div><div class="ds-card-title">QC results</div><div class="ds-card-para">Is every result in spec?</div></div></div>
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
# MAGIC <div class="ds-callout danger row"><div class="ds-callout-icon">?</div><div><div class="ds-eyebrow">The problem</div><div class="ds-callout-title">&quot;Is lot LT26B008 ready for QA review?&quot; takes 4 systems and a spreadsheet.</div><ul><li>Lots wait in QA review for days while people reconcile exports.</li><li>Nobody can say which file a number came from.</li><li>Today you build the pipeline that answers it in seconds, with lineage.</li></ul></div></div>
# MAGIC </div>
# MAGIC
# MAGIC ##### EXPAND FOR ADDITIONAL NOTES
# MAGIC
# MAGIC <details>
# MAGIC
# MAGIC **Open with the pain, not the product.**
# MAGIC - Ask the room: *who has reconciled a deviation export with a LIMS export by hand?* Most hands go up.
# MAGIC - Each card is a real system boundary. The pipeline's job is to make them one governed model.
# MAGIC
# MAGIC **Ground rule:** all data is synthetic. Nothing here is a release or compliance decision.
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
# MAGIC <div style="font-size:20pt;font-weight:700;margin-bottom:14px;">Four ideas you will use today</div><div class="ds-row"><div class="ds-card blue"><div class="ds-card-title">1. Files are read once</div><div class="ds-card-para">Auto Loader + streaming tables ingest only what is new.</div></div><div class="ds-card green"><div class="ds-card-title">2. Bad data is visible</div><div class="ds-card-para">Expectations + quarantine: in = clean + quarantine.</div></div><div class="ds-card amber"><div class="ds-card-title">3. Append vs recompute</div><div class="ds-card-para">Streaming table or materialized view, chosen by grain.</div></div><div class="ds-card coral"><div class="ds-card-title">4. Same code, new environment</div><div class="ds-card-para">A bundle promotes dev &rarr; QA without edits.</div></div></div>
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
# MAGIC <div class="flow-grid" style="grid-template-columns:1fr auto 1fr auto 1fr auto 1fr auto 1fr auto 1fr;"><div class="flow-step dim" style="--accent:#4299E0;"><div class="flow-num">1</div><div class="flow-label">Land files</div></div><div class="flow-arrow dim">&rarr;</div><div class="flow-step dim" style="--accent:#00A972;"><div class="flow-num">2</div><div class="flow-label">Bronze</div></div><div class="flow-arrow dim">&rarr;</div><div class="flow-step dim" style="--accent:#FFAB00;"><div class="flow-num">3</div><div class="flow-label">Silver</div></div><div class="flow-arrow dim">&rarr;</div><div class="flow-step dim" style="--accent:#FF5F46;"><div class="flow-num">4</div><div class="flow-label">Gold</div></div><div class="flow-arrow dim">&rarr;</div><div class="flow-step dim" style="--accent:#98102A;"><div class="flow-num">5</div><div class="flow-label">New batch</div></div><div class="flow-arrow dim">&rarr;</div><div class="flow-step dim" style="--accent:#1B5162;"><div class="flow-num">6</div><div class="flow-label">Promote</div></div></div>
# MAGIC </div>
# MAGIC
# MAGIC ##### EXPAND FOR ADDITIONAL NOTES
# MAGIC
# MAGIC <details>
# MAGIC
# MAGIC Everything today hangs off these four ideas. If a learner leaves with only these, the session worked.
# MAGIC - CDC, multi-flow, liquid clustering and sinks are mentioned and left in take-home notebooks.
# MAGIC
# MAGIC </details>

# COMMAND ----------

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
# MAGIC <div class="ds-banner info"><div class="ds-banner-icon">&#9719;</div><div><div class="ds-banner-title">Today's agenda</div><div class="ds-banner-tagline">1:00-4:30 &middot; 3.5 hours with a 10-minute break &middot; take-home stretch notebooks S1-S6</div></div></div>
# MAGIC </div>
# MAGIC <div style="height:18px"></div>
# MAGIC <div class="cw">
# MAGIC <style>
# MAGIC .cw { font-family: sans-serif; max-width: 1100px; margin: 0 auto; color: #0b2026; } .cw * { box-sizing: border-box; }
# MAGIC .ag { display: flex; flex-direction: column; gap: 8px; }
# MAGIC .ag-row { display: grid; grid-template-columns: 150px 70px 1fr 230px; gap: 16px; align-items: center; background: #F9F7F4; border-radius: 8px; box-shadow: 0 2px 8px rgba(27,49,57,0.06); padding: 12px 18px; border-left: 8px solid var(--accent, #4299E0); }
# MAGIC .ag-row.dim { background: #EEEDE9; box-shadow: none; border-left-color: #C2C2C2; }
# MAGIC .ag-time { font-size: 15pt; font-weight: 700; color: #0b2026; }
# MAGIC .ag-min { font-size: 14pt; color: #5E7077; }
# MAGIC .ag-title { font-size: 15pt; font-weight: 700; color: #0b2026; line-height: 1.3; }
# MAGIC .ag-sub { font-size: 14pt; color: #5E7077; line-height: 1.4; margin-top: 2px; }
# MAGIC .ag-nb { font-size: 14pt; color: #1B5162; font-weight: 600; text-align: right; }
# MAGIC .ag-legend { display: flex; gap: 22px; flex-wrap: wrap; margin-top: 12px; font-size: 14pt; color: #5E7077; }
# MAGIC .ag-dot { display: inline-block; width: 14px; height: 14px; border-radius: 3px; margin-right: 6px; vertical-align: -1px; background: var(--accent); }
# MAGIC </style>
# MAGIC <div class="ag"><div class="ag-row" style="--accent:#4299E0;"><div class="ag-time">1:00-1:10</div><div class="ag-min">10 min</div><div><div class="ag-title">Welcome and outcomes</div><div class="ag-sub">The lot release readiness problem, how we work, the feeds and today's deliverable</div></div><div class="ag-nb">00 Overview</div></div><div class="ag-row" style="--accent:#4299E0;"><div class="ag-time">1:10-1:25</div><div class="ag-min">15 min</div><div><div class="ag-title">Architecture: source to Gold</div><div class="ag-sub">Five feeds and their grains; Bronze / Silver / Gold responsibilities; append-only vs changing records</div></div><div class="ag-nb">01 Lecture</div></div><div class="ag-row" style="--accent:#4299E0;"><div class="ag-time">1:25-1:40</div><div class="ag-min">15 min</div><div><div class="ag-title">Auto Loader and SDP concepts</div><div class="ag-sub">Why a declarative pipeline, one Auto Loader pattern, rescued data, dataset types, join types</div></div><div class="ag-nb">02 Lecture</div></div><div class="ag-row dim"><div class="ag-time">1:40-1:50</div><div class="ag-min">10 min</div><div><div class="ag-title">Break</div><div class="ag-sub">Finish notebook 00: Git folder, setup cell, your bundle with an ETL pipeline</div></div><div class="ag-nb"></div></div><div class="ag-row" style="--accent:#00A972;"><div class="ag-time">1:50-2:05</div><div class="ag-min">15 min</div><div><div class="ag-title">Hands-on: Bronze</div><div class="ag-sub">Open your pipeline, build two Bronze tables with Auto Loader</div></div><div class="ag-nb">03 Lab</div></div><div class="ag-row" style="--accent:#4299E0;"><div class="ag-time">2:05-2:15</div><div class="ag-min">10 min</div><div><div class="ag-title">Data quality and change data capture</div><div class="ag-sub">Expectations, quarantine, NULL-tolerant rules; AUTO CDC with SCD type 1 and 2</div></div><div class="ag-nb">04 Lecture</div></div><div class="ag-row" style="--accent:#00A972;"><div class="ag-time">2:15-3:05</div><div class="ag-min">50 min</div><div><div class="ag-title">Hands-on: Silver, Gold, new files</div><div class="ag-sub">Silver (2 tables) + quarantine 15, then SQL and Python together 5 &middot; Gold 15 &middot; new files, schema change, trace a number 15</div></div><div class="ag-nb">05-07 Labs</div></div><div class="ag-row" style="--accent:#FFAB00;"><div class="ag-time">3:05-3:30</div><div class="ag-min">25 min</div><div><div class="ag-title">Bundle validation and dev &rarr; QA promotion</div><div class="ag-sub">Bundles and variables (10), then promote your own pipeline to QA through its quality gate (15); production controls</div></div><div class="ag-nb">08 Lecture + 09 Lab</div></div><div class="ag-row" style="--accent:#FFAB00;"><div class="ag-time">3:30-3:55</div><div class="ag-min">25 min</div><div><div class="ag-title">Unity Catalog and platform practices</div><div class="ag-sub">Boundaries, access, sandbox vs certified (10), then grants, tags, lineage and event log on your own tables (15)</div></div><div class="ag-nb">10 Lecture + 11 Lab</div></div><div class="ag-row" style="--accent:#FFAB00;"><div class="ag-time">3:55-4:15</div><div class="ag-min">20 min</div><div><div class="ag-title">AI-ready data: context for Genie and agents</div><div class="ag-sub">Metadata as code, certified assets, a metric view with synonyms, Genie benchmarks (facilitator demo of Lab 13)</div></div><div class="ag-nb">13 Lab (demo)</div></div><div class="ag-row" style="--accent:#FF5F46;"><div class="ag-time">4:15-4:25</div><div class="ag-min">10 min</div><div><div class="ag-title">Recap and Q&amp;A</div><div class="ag-sub">Facilitator walks the finished pipeline end to end: Gold outputs, a data-quality case, a new-file arrival, the QA deployment, dashboard and app. Then questions</div></div><div class="ag-nb">12 Recap</div></div><div class="ag-row" style="--accent:#FF5F46;"><div class="ag-time">4:25-4:30</div><div class="ag-min">5 min</div><div><div class="ag-title">Wrap-up</div><div class="ag-sub">Decisions, owners and next steps to productionize</div></div><div class="ag-nb">99 Summary</div></div><div class="ag-row dim"><div class="ag-time">Take-home</div><div class="ag-min">40 min</div><div><div class="ag-title">Optional: metadata enrichment hands-on</div><div class="ag-sub">Run Lab 13 yourself: AI-drafted descriptions, steward review, tag drift, sandbox radar, lineage impact</div></div><div class="ag-nb">13 Lab</div></div></div><div class="ag-legend"><span><span class="ag-dot" style="--accent:#4299E0;"></span>Concepts</span><span><span class="ag-dot" style="--accent:#00A972;"></span>Hands-on</span><span><span class="ag-dot" style="--accent:#FFAB00;"></span>Promote and govern</span><span><span class="ag-dot" style="--accent:#FF5F46;"></span>Recap and close</span></div>
# MAGIC </div>
# MAGIC
# MAGIC ##### EXPAND FOR ADDITIONAL NOTES
# MAGIC
# MAGIC <details>
# MAGIC
# MAGIC **Pacing**
# MAGIC - The 60-minute build block has four timeboxed checkpoints. If someone is more than one checkpoint behind, switch them to the reference code so they keep pace for promotion.
# MAGIC - Participants build two Bronze and two Silver tables (QC results, change controls) and the QC-results Gold; the rest is prebuilt.
# MAGIC - Lab 13 runs as a 20-minute facilitator demo (3:45); the full hands-on version is take-home.
# MAGIC - Stretch notebooks S1-S6 (readiness, dashboard, Genie, Apps lecture + lab, AUTO CDC) are take-home; the facilitator demos the finished versions in the recap.
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
# MAGIC <div class="ds-row"><div class="ds-card blue"><div class="ds-card-title">How we work</div><ul><li>I show it on the <strong>deviation</strong> feed</li><li>You build <strong>QC results</strong> Bronze to Gold, plus <strong>change-control</strong> Bronze and Silver</li><li>The other feeds are prebuilt: read them, do not rebuild them</li><li>Checkpoints tell you exact expected numbers</li></ul></div><div class="ds-card green"><div class="ds-card-title">Everyone builds their own</div><ul><li>Your tables go to your personal schema: <code>iops_sandbox.‹you›</code></li><li>Names are unique by your user name: <code>[dev ‹you›]</code> pipeline, <code>‹you›_qa</code> schema</li><li>Everyone reads the same shared landing folder</li></ul></div><div class="ds-card amber"><div class="ds-card-title">When stuck</div><ul><li>Every TODO has a collapsed CODE ANSWER</li><li>Genie Code can explain any error</li><li>Facilitators can switch you to the reference code</li></ul></div></div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## Setup: three steps, once
# MAGIC
# MAGIC **Step 1. Bring the workshop into your workspace as a Git folder**
# MAGIC 1. If your workspace asks for Git credentials: your user icon &rarr; **Settings** &rarr; **Linked accounts** &rarr; **Add Git credential** &rarr; provider **GitHub** &rarr; **Link Git account** &rarr; **Link** &rarr; **Authorize Databricks** (the Databricks GitHub App).
# MAGIC 2. **Workspace** &rarr; your user folder &rarr; **Create** &rarr; **Git folder**.
# MAGIC 3. Git repository URL: `https://github.com/pulpareek/data-engineering-workshop` &rarr; **Create Git folder**.
# MAGIC
# MAGIC You now have `workshop/` (these notebooks), `data/` (the source files), `pipeline_files/` (the pipeline code you will use) and `governance/`.
# MAGIC
# MAGIC **Step 2. Run the setup cell below**
# MAGIC The widgets already hold the workshop values; change them only if the facilitator says so. Everything you create is named after your user name, so nobody overwrites anyone.
# MAGIC
# MAGIC **Step 3. Create your bundle with an ETL pipeline**
# MAGIC 1. Open your Git folder &rarr; **Create** &rarr; **Bundle**.
# MAGIC 2. Name: `iops_quality`. Template: **ETL pipeline**. Default catalog: `iops_sandbox`. Personal schema: **Yes** (your tables go to `iops_sandbox.<your user name>`). Language: **SQL**.
# MAGIC 3. **Create and deploy**.
# MAGIC
# MAGIC The bundle is a folder with a `databricks.yml` (the project file, almost empty for now), a pipeline definition in `resources/`, and a `src/` folder for the pipeline code. You build the pipeline inside it in Labs 03-07, and complete `databricks.yml` in Lab 09.

# COMMAND ----------

%run ./Includes/Classroom-Setup

# COMMAND ----------

show_paths()

# COMMAND ----------

# MAGIC %md
# MAGIC | Widget | Set it when | Default |
# MAGIC |---|---|---|
# MAGIC | **catalog** | the facilitator says so | `iops_sandbox` |
# MAGIC | **schema** | your bundle uses another schema | your personal schema (your user name) |
# MAGIC | **landing** | your pipeline reads another folder | `/Volumes/iops_sandbox/iops_databricks_workshop/landing` (shared by everyone) |
# MAGIC | **source files** | facilitator only | the batches in `data/staging` |
# MAGIC | **target** | you work in QA (Lab 09) | `dev` |
