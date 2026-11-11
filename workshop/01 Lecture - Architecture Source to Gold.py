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
# MAGIC <div class="ds-banner info"><div class="ds-banner-icon">1</div><div><div class="ds-banner-title">Architecture: source files to Gold</div><div class="ds-banner-tagline">Map the grain first. Code second.</div></div></div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## Overview
# MAGIC
# MAGIC Before writing any code, map the problem: which source systems send which files, what one row of each feed means, and what each layer of the pipeline is responsible for. You also see how changing records are handled with AUTO CDC, and exactly which parts of the pipeline you build today.
# MAGIC
# MAGIC ## Learning Objectives
# MAGIC
# MAGIC By the end of this lecture, you will be able to:
# MAGIC
# MAGIC 1. **Explain the declarative approach**: what you write with SDP and what the platform does for you
# MAGIC 2. **Name the five feeds** and state the grain of each (event, snapshot, measurement)
# MAGIC 3. **Assign responsibilities** to Bronze, Silver and Gold
# MAGIC 4. **Distinguish append-only feeds from changing records**, and describe AUTO CDC with SCD type 1 and type 2
# MAGIC 5. **Read the pipeline diagram** and say which tables you build, switch on or read in the labs

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
# MAGIC <div style="font-size:20pt;font-weight:700;margin-bottom:14px;">Declarative: say what, not how</div><div class="ds-row"><div class="ds-card coral"><div class="ds-card-title">What you used to own</div><ul><li>Checkpoints, retries, backfills</li><li>Dependency order between tables</li><li>Orchestration, compute, scaling</li><li>Quality checks bolted on later</li></ul></div><div class="ds-card green"><div class="ds-card-title">What you write with SDP</div><ul><li><strong>Your transformation logic</strong>, in SQL or Python</li><li>Rules as expectations</li><li>That is it</li></ul></div><div class="ds-card blue"><div class="ds-card-title">What the platform does</div><ul><li>Builds the graph from your queries</li><li>Tracks files and rows already processed</li><li>Retries, scales, logs every update</li></ul></div></div>
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
# MAGIC <div class="ds-row"><div class="ds-card blue"><div class="ds-card-label">Lakeflow</div><div class="ds-card-title">Connect</div><div class="ds-card-para">Managed ingestion from SaaS and databases. Today: files, so Auto Loader.</div></div><div class="ds-card green"><div class="ds-card-label">Lakeflow</div><div class="ds-card-title">Declarative Pipelines</div><div class="ds-card-para">Bronze &rarr; Silver &rarr; Gold with quality built in. Today's focus.</div></div><div class="ds-card amber"><div class="ds-card-label">Lakeflow</div><div class="ds-card-title">Jobs</div><div class="ds-card-para">Orchestrates pipeline + metadata + checks on a schedule.</div></div></div>
# MAGIC </div>
# MAGIC
# MAGIC ##### EXPAND FOR ADDITIONAL NOTES
# MAGIC
# MAGIC <details>
# MAGIC
# MAGIC - Ask: *how many lines of your current ETL are about checkpoints, retries and ordering rather than business rules?*
# MAGIC - The point of the day: everything you write is the middle card.
# MAGIC
# MAGIC </details>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div style="max-width: 1100px; margin: 0 auto; font-family: sans-serif; color: #0b2026;"><div style="text-align: center; margin-bottom: 12px;"><div style="font-size: 22pt; font-weight: 700;">One pipeline, five feeds: what you do with each</div><div style="font-size: 14pt; color: #618794; margin-top: 4px;">Highlighted: you build, switch on or read it in the labs &middot; grey: prebuilt, already running &middot; bolt = streaming table, glasses = materialized view</div></div><svg width="100%" viewBox="0 0 1158 500" role="img" style="font-family: sans-serif;"><defs><marker id="med-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="#5E7077" stroke-width="1.5"/></marker></defs><path d="M854 442.0 L894 401.0" fill="none" stroke="#5E7077" stroke-width="1.6" marker-end="url(#med-arrow)"/><path d="M854 360.0 L894 401.0" fill="none" stroke="#5E7077" stroke-width="1.6" marker-end="url(#med-arrow)"/><path d="M854 360.0 L894 319.0" fill="none" stroke="#5E7077" stroke-width="1.6" marker-end="url(#med-arrow)"/><path d="M854 278.0 L894 237.0" fill="none" stroke="#5E7077" stroke-width="1.6" marker-end="url(#med-arrow)"/><path d="M854 196.0 L894 155.0" fill="none" stroke="#5E7077" stroke-width="1.6" marker-end="url(#med-arrow)"/><path d="M854 114.0 L894 155.0" fill="none" stroke="#5E7077" stroke-width="1.6" marker-end="url(#med-arrow)"/><path d="M558 442.0 L598 442.0" fill="none" stroke="#5E7077" stroke-width="1.6" marker-end="url(#med-arrow)"/><path d="M558 360.0 L598 360.0" fill="none" stroke="#5E7077" stroke-width="1.6" marker-end="url(#med-arrow)"/><path d="M558 278.0 L598 278.0" fill="none" stroke="#5E7077" stroke-width="1.6" marker-end="url(#med-arrow)"/><path d="M558 196.0 L598 196.0" fill="none" stroke="#5E7077" stroke-width="1.6" marker-end="url(#med-arrow)"/><path d="M558 114.0 L598 114.0" fill="none" stroke="#5E7077" stroke-width="1.6" marker-end="url(#med-arrow)"/><path d="M262 442.0 L302 442.0" fill="none" stroke="#5E7077" stroke-width="1.6" marker-end="url(#med-arrow)"/><path d="M262 360.0 L302 360.0" fill="none" stroke="#5E7077" stroke-width="1.6" marker-end="url(#med-arrow)"/><path d="M262 278.0 L302 278.0" fill="none" stroke="#5E7077" stroke-width="1.6" marker-end="url(#med-arrow)"/><path d="M262 196.0 L302 196.0" fill="none" stroke="#5E7077" stroke-width="1.6" marker-end="url(#med-arrow)"/><path d="M262 114.0 L302 114.0" fill="none" stroke="#5E7077" stroke-width="1.6" marker-end="url(#med-arrow)"/><rect x="10" y="10" width="250" height="32" rx="16" fill="#1B5162"/><text x="135.0" y="31" text-anchor="middle" font-size="14" font-weight="700" fill="#FFFFFF" letter-spacing="2">FILES</text><g opacity="0.4"><rect x="10" y="82.0" width="250" height="64" rx="8" fill="#1B5162" fill-opacity="0.10" stroke="#1B5162" stroke-width="1.5"/><g transform="translate(20,100.0)"><rect x="0" y="2" width="24" height="18" rx="2" fill="none" stroke="#1B5162" stroke-width="1.5"/><rect x="0" y="2" width="24" height="6" rx="2" fill="#1B5162"/><line x1="8" y1="8" x2="8" y2="20" stroke="#1B5162" stroke-width="1.2"/><line x1="16" y1="8" x2="16" y2="20" stroke="#1B5162" stroke-width="1.2"/><line x1="0" y1="14" x2="24" y2="14" stroke="#1B5162" stroke-width="1.2"/></g><text x="54" y="110.0" font-size="14" font-weight="700" fill="#0b2026" font-family="monospace">deviation_event_feed</text><text x="54" y="130.0" font-size="14" fill="#5E7077">CSV, QMS</text></g><g opacity="0.4"><rect x="10" y="164.0" width="250" height="64" rx="8" fill="#1B5162" fill-opacity="0.10" stroke="#1B5162" stroke-width="1.5"/><g transform="translate(20,182.0)"><rect x="0" y="2" width="24" height="18" rx="2" fill="none" stroke="#1B5162" stroke-width="1.5"/><rect x="0" y="2" width="24" height="6" rx="2" fill="#1B5162"/><line x1="8" y1="8" x2="8" y2="20" stroke="#1B5162" stroke-width="1.2"/><line x1="16" y1="8" x2="16" y2="20" stroke="#1B5162" stroke-width="1.2"/><line x1="0" y1="14" x2="24" y2="14" stroke="#1B5162" stroke-width="1.2"/></g><text x="54" y="192.0" font-size="14" font-weight="700" fill="#0b2026" font-family="monospace">corrective_action_feed</text><text x="54" y="212.0" font-size="14" fill="#5E7077">CSV, QMS</text></g><rect x="10" y="246.0" width="250" height="64" rx="8" fill="#1B5162" fill-opacity="0.10" stroke="#1B5162" stroke-width="1.5"/><g transform="translate(20,264.0)"><rect x="0" y="2" width="24" height="18" rx="2" fill="none" stroke="#1B5162" stroke-width="1.5"/><rect x="0" y="2" width="24" height="6" rx="2" fill="#1B5162"/><line x1="8" y1="8" x2="8" y2="20" stroke="#1B5162" stroke-width="1.2"/><line x1="16" y1="8" x2="16" y2="20" stroke="#1B5162" stroke-width="1.2"/><line x1="0" y1="14" x2="24" y2="14" stroke="#1B5162" stroke-width="1.2"/></g><text x="54" y="274.0" font-size="14" font-weight="700" fill="#0b2026" font-family="monospace">change_control_feed</text><text x="54" y="294.0" font-size="14" fill="#5E7077">CSV</text><rect x="10" y="328.0" width="250" height="64" rx="8" fill="#1B5162" fill-opacity="0.10" stroke="#1B5162" stroke-width="1.5"/><g transform="translate(20,346.0)"><rect x="0" y="2" width="24" height="18" rx="2" fill="none" stroke="#1B5162" stroke-width="1.5"/><rect x="0" y="2" width="24" height="6" rx="2" fill="#1B5162"/><line x1="8" y1="8" x2="8" y2="20" stroke="#1B5162" stroke-width="1.2"/><line x1="16" y1="8" x2="16" y2="20" stroke="#1B5162" stroke-width="1.2"/><line x1="0" y1="14" x2="24" y2="14" stroke="#1B5162" stroke-width="1.2"/></g><text x="54" y="356.0" font-size="14" font-weight="700" fill="#0b2026" font-family="monospace">inspection_result_feed</text><text x="54" y="376.0" font-size="14" fill="#5E7077">CSV, LIMS</text><rect x="10" y="410.0" width="250" height="64" rx="8" fill="#1B5162" fill-opacity="0.10" stroke="#1B5162" stroke-width="1.5"/><g transform="translate(20,428.0)"><rect x="0" y="2" width="24" height="18" rx="2" fill="none" stroke="#1B5162" stroke-width="1.5"/><rect x="0" y="2" width="24" height="6" rx="2" fill="#1B5162"/><line x1="8" y1="8" x2="8" y2="20" stroke="#1B5162" stroke-width="1.2"/><line x1="16" y1="8" x2="16" y2="20" stroke="#1B5162" stroke-width="1.2"/><line x1="0" y1="14" x2="24" y2="14" stroke="#1B5162" stroke-width="1.2"/></g><text x="54" y="438.0" font-size="14" font-weight="700" fill="#0b2026" font-family="monospace">batch_record_feed</text><text x="54" y="458.0" font-size="14" fill="#5E7077">CSV, MES</text><rect x="306" y="10" width="250" height="32" rx="16" fill="#CD7F32"/><text x="431.0" y="31" text-anchor="middle" font-size="14" font-weight="700" fill="#FFFFFF" letter-spacing="2">BRONZE</text><g opacity="0.4"><rect x="306" y="82.0" width="250" height="64" rx="8" fill="#CD7F32" fill-opacity="0.10" stroke="#CD7F32" stroke-width="1.5"/><g transform="translate(316,100.0)"><rect x="0" y="2" width="24" height="18" rx="2" fill="none" stroke="#CD7F32" stroke-width="1.5"/><rect x="0" y="2" width="24" height="6" rx="2" fill="#CD7F32"/><line x1="8" y1="8" x2="8" y2="20" stroke="#CD7F32" stroke-width="1.2"/><line x1="16" y1="8" x2="16" y2="20" stroke="#CD7F32" stroke-width="1.2"/><line x1="0" y1="14" x2="24" y2="14" stroke="#CD7F32" stroke-width="1.2"/><circle cx="22" cy="18" r="7" fill="#FFFFFF"/><path d="M23 13 L18.5 19 L21.5 19 L20 23.5 L26 16.5 L23 16.5 Z" fill="#CD7F32" stroke="#FFFFFF" stroke-width="0.5"/></g><text x="350" y="110.0" font-size="14" font-weight="700" fill="#0b2026" font-family="monospace">bronze_deviation_event</text><text x="350" y="130.0" font-size="14" fill="#5E7077">worked example</text></g><g opacity="0.4"><rect x="306" y="164.0" width="250" height="64" rx="8" fill="#CD7F32" fill-opacity="0.10" stroke="#CD7F32" stroke-width="1.5"/><g transform="translate(316,182.0)"><rect x="0" y="2" width="24" height="18" rx="2" fill="none" stroke="#CD7F32" stroke-width="1.5"/><rect x="0" y="2" width="24" height="6" rx="2" fill="#CD7F32"/><line x1="8" y1="8" x2="8" y2="20" stroke="#CD7F32" stroke-width="1.2"/><line x1="16" y1="8" x2="16" y2="20" stroke="#CD7F32" stroke-width="1.2"/><line x1="0" y1="14" x2="24" y2="14" stroke="#CD7F32" stroke-width="1.2"/><circle cx="22" cy="18" r="7" fill="#FFFFFF"/><path d="M23 13 L18.5 19 L21.5 19 L20 23.5 L26 16.5 L23 16.5 Z" fill="#CD7F32" stroke="#FFFFFF" stroke-width="0.5"/></g><text x="350" y="192.0" font-size="14" font-weight="700" fill="#0b2026" font-family="monospace">bronze_corrective_action</text><text x="350" y="212.0" font-size="14" fill="#5E7077">prebuilt</text></g><rect x="306" y="246.0" width="250" height="64" rx="8" fill="#CD7F32" fill-opacity="0.10" stroke="#CD7F32" stroke-width="1.5"/><g transform="translate(316,264.0)"><rect x="0" y="2" width="24" height="18" rx="2" fill="none" stroke="#CD7F32" stroke-width="1.5"/><rect x="0" y="2" width="24" height="6" rx="2" fill="#CD7F32"/><line x1="8" y1="8" x2="8" y2="20" stroke="#CD7F32" stroke-width="1.2"/><line x1="16" y1="8" x2="16" y2="20" stroke="#CD7F32" stroke-width="1.2"/><line x1="0" y1="14" x2="24" y2="14" stroke="#CD7F32" stroke-width="1.2"/><circle cx="22" cy="18" r="7" fill="#FFFFFF"/><path d="M23 13 L18.5 19 L21.5 19 L20 23.5 L26 16.5 L23 16.5 Z" fill="#CD7F32" stroke="#FFFFFF" stroke-width="0.5"/></g><text x="350" y="274.0" font-size="14" font-weight="700" fill="#0b2026" font-family="monospace">bronze_change_control</text><text x="350" y="294.0" font-size="14" fill="#5E7077">you build (Lab 03)</text><rect x="306" y="328.0" width="250" height="64" rx="8" fill="#CD7F32" fill-opacity="0.10" stroke="#CD7F32" stroke-width="1.5"/><g transform="translate(316,346.0)"><rect x="0" y="2" width="24" height="18" rx="2" fill="none" stroke="#CD7F32" stroke-width="1.5"/><rect x="0" y="2" width="24" height="6" rx="2" fill="#CD7F32"/><line x1="8" y1="8" x2="8" y2="20" stroke="#CD7F32" stroke-width="1.2"/><line x1="16" y1="8" x2="16" y2="20" stroke="#CD7F32" stroke-width="1.2"/><line x1="0" y1="14" x2="24" y2="14" stroke="#CD7F32" stroke-width="1.2"/><circle cx="22" cy="18" r="7" fill="#FFFFFF"/><path d="M23 13 L18.5 19 L21.5 19 L20 23.5 L26 16.5 L23 16.5 Z" fill="#CD7F32" stroke="#FFFFFF" stroke-width="0.5"/></g><text x="350" y="356.0" font-size="14" font-weight="700" fill="#0b2026" font-family="monospace">bronze_inspection_result</text><text x="350" y="376.0" font-size="14" fill="#5E7077">you build (Lab 03)</text><rect x="306" y="410.0" width="250" height="64" rx="8" fill="#CD7F32" fill-opacity="0.10" stroke="#CD7F32" stroke-width="1.5"/><g transform="translate(316,428.0)"><rect x="0" y="2" width="24" height="18" rx="2" fill="none" stroke="#CD7F32" stroke-width="1.5"/><rect x="0" y="2" width="24" height="6" rx="2" fill="#CD7F32"/><line x1="8" y1="8" x2="8" y2="20" stroke="#CD7F32" stroke-width="1.2"/><line x1="16" y1="8" x2="16" y2="20" stroke="#CD7F32" stroke-width="1.2"/><line x1="0" y1="14" x2="24" y2="14" stroke="#CD7F32" stroke-width="1.2"/><circle cx="22" cy="18" r="7" fill="#FFFFFF"/><path d="M23 13 L18.5 19 L21.5 19 L20 23.5 L26 16.5 L23 16.5 Z" fill="#CD7F32" stroke="#FFFFFF" stroke-width="0.5"/></g><text x="350" y="438.0" font-size="14" font-weight="700" fill="#0b2026" font-family="monospace">bronze_batch_record</text><text x="350" y="458.0" font-size="14" fill="#5E7077">you add (Lab 05, Python)</text><rect x="602" y="10" width="250" height="32" rx="16" fill="#5A6F77"/><text x="727.0" y="31" text-anchor="middle" font-size="14" font-weight="700" fill="#FFFFFF" letter-spacing="2">SILVER</text><g opacity="0.4"><rect x="602" y="82.0" width="250" height="64" rx="8" fill="#5A6F77" fill-opacity="0.10" stroke="#5A6F77" stroke-width="1.5"/><g transform="translate(612,100.0)"><rect x="0" y="2" width="24" height="18" rx="2" fill="none" stroke="#5A6F77" stroke-width="1.5"/><rect x="0" y="2" width="24" height="6" rx="2" fill="#5A6F77"/><line x1="8" y1="8" x2="8" y2="20" stroke="#5A6F77" stroke-width="1.2"/><line x1="16" y1="8" x2="16" y2="20" stroke="#5A6F77" stroke-width="1.2"/><line x1="0" y1="14" x2="24" y2="14" stroke="#5A6F77" stroke-width="1.2"/><circle cx="22" cy="18" r="7" fill="#FFFFFF"/><path d="M23 13 L18.5 19 L21.5 19 L20 23.5 L26 16.5 L23 16.5 Z" fill="#5A6F77" stroke="#FFFFFF" stroke-width="0.5"/></g><text x="646" y="110.0" font-size="14" font-weight="700" fill="#0b2026" font-family="monospace">silver_deviation_event</text><text x="646" y="130.0" font-size="14" fill="#5E7077">worked example</text></g><rect x="602" y="164.0" width="250" height="64" rx="8" fill="#5A6F77" fill-opacity="0.10" stroke="#5A6F77" stroke-width="1.5"/><g transform="translate(612,182.0)"><rect x="0" y="2" width="24" height="18" rx="2" fill="none" stroke="#5A6F77" stroke-width="1.5"/><rect x="0" y="2" width="24" height="6" rx="2" fill="#5A6F77"/><line x1="8" y1="8" x2="8" y2="20" stroke="#5A6F77" stroke-width="1.2"/><line x1="16" y1="8" x2="16" y2="20" stroke="#5A6F77" stroke-width="1.2"/><line x1="0" y1="14" x2="24" y2="14" stroke="#5A6F77" stroke-width="1.2"/><circle cx="22" cy="18" r="7" fill="#FFFFFF"/><path d="M23 13 L18.5 19 L21.5 19 L20 23.5 L26 16.5 L23 16.5 Z" fill="#5A6F77" stroke="#FFFFFF" stroke-width="0.5"/></g><text x="646" y="192.0" font-size="14" font-weight="700" fill="#0b2026" font-family="monospace">silver_corrective_action</text><text x="646" y="212.0" font-size="14" fill="#5E7077">AUTO CDC, read in Lab 05</text><rect x="602" y="246.0" width="250" height="64" rx="8" fill="#5A6F77" fill-opacity="0.10" stroke="#5A6F77" stroke-width="1.5"/><g transform="translate(612,264.0)"><rect x="0" y="2" width="24" height="18" rx="2" fill="none" stroke="#5A6F77" stroke-width="1.5"/><rect x="0" y="2" width="24" height="6" rx="2" fill="#5A6F77"/><line x1="8" y1="8" x2="8" y2="20" stroke="#5A6F77" stroke-width="1.2"/><line x1="16" y1="8" x2="16" y2="20" stroke="#5A6F77" stroke-width="1.2"/><line x1="0" y1="14" x2="24" y2="14" stroke="#5A6F77" stroke-width="1.2"/><circle cx="22" cy="18" r="7" fill="#FFFFFF"/><path d="M23 13 L18.5 19 L21.5 19 L20 23.5 L26 16.5 L23 16.5 Z" fill="#5A6F77" stroke="#FFFFFF" stroke-width="0.5"/></g><text x="646" y="274.0" font-size="14" font-weight="700" fill="#0b2026" font-family="monospace">silver_change_control</text><text x="646" y="294.0" font-size="14" fill="#5E7077">you build (Lab 05)</text><rect x="602" y="328.0" width="250" height="64" rx="8" fill="#5A6F77" fill-opacity="0.10" stroke="#5A6F77" stroke-width="1.5"/><g transform="translate(612,346.0)"><rect x="0" y="2" width="24" height="18" rx="2" fill="none" stroke="#5A6F77" stroke-width="1.5"/><rect x="0" y="2" width="24" height="6" rx="2" fill="#5A6F77"/><line x1="8" y1="8" x2="8" y2="20" stroke="#5A6F77" stroke-width="1.2"/><line x1="16" y1="8" x2="16" y2="20" stroke="#5A6F77" stroke-width="1.2"/><line x1="0" y1="14" x2="24" y2="14" stroke="#5A6F77" stroke-width="1.2"/><circle cx="22" cy="18" r="7" fill="#FFFFFF"/><path d="M23 13 L18.5 19 L21.5 19 L20 23.5 L26 16.5 L23 16.5 Z" fill="#5A6F77" stroke="#FFFFFF" stroke-width="0.5"/></g><text x="646" y="356.0" font-size="14" font-weight="700" fill="#0b2026" font-family="monospace">silver_inspection_result</text><text x="646" y="376.0" font-size="14" fill="#5E7077">you build (Lab 05)</text><rect x="602" y="410.0" width="250" height="64" rx="8" fill="#5A6F77" fill-opacity="0.10" stroke="#5A6F77" stroke-width="1.5"/><g transform="translate(612,428.0)"><rect x="0" y="2" width="24" height="18" rx="2" fill="none" stroke="#5A6F77" stroke-width="1.5"/><rect x="0" y="2" width="24" height="6" rx="2" fill="#5A6F77"/><line x1="8" y1="8" x2="8" y2="20" stroke="#5A6F77" stroke-width="1.2"/><line x1="16" y1="8" x2="16" y2="20" stroke="#5A6F77" stroke-width="1.2"/><line x1="0" y1="14" x2="24" y2="14" stroke="#5A6F77" stroke-width="1.2"/><circle cx="22" cy="18" r="7" fill="#FFFFFF"/><path d="M23 13 L18.5 19 L21.5 19 L20 23.5 L26 16.5 L23 16.5 Z" fill="#5A6F77" stroke="#FFFFFF" stroke-width="0.5"/></g><text x="646" y="438.0" font-size="14" font-weight="700" fill="#0b2026" font-family="monospace">silver_batch_record</text><text x="646" y="458.0" font-size="14" fill="#5E7077">you add (Lab 05, Python)</text><rect x="898" y="10" width="250" height="32" rx="16" fill="#FFAB00"/><text x="1023.0" y="31" text-anchor="middle" font-size="14" font-weight="700" fill="#0b2026" letter-spacing="2">GOLD</text><g opacity="0.4"><rect x="898" y="123.0" width="250" height="64" rx="8" fill="#FFAB00" fill-opacity="0.10" stroke="#FFAB00" stroke-width="1.5"/><g transform="translate(908,141.0)"><rect x="0" y="2" width="24" height="18" rx="2" fill="none" stroke="#FFAB00" stroke-width="1.5"/><rect x="0" y="2" width="24" height="6" rx="2" fill="#FFAB00"/><line x1="8" y1="8" x2="8" y2="20" stroke="#FFAB00" stroke-width="1.2"/><line x1="16" y1="8" x2="16" y2="20" stroke="#FFAB00" stroke-width="1.2"/><line x1="0" y1="14" x2="24" y2="14" stroke="#FFAB00" stroke-width="1.2"/><circle cx="22" cy="18" r="8" fill="#FFFFFF"/><circle cx="19" cy="18" r="2.6" fill="none" stroke="#0b2026" stroke-width="1.3"/><circle cx="25.5" cy="18" r="2.6" fill="none" stroke="#0b2026" stroke-width="1.3"/><line x1="21.6" y1="17.6" x2="22.9" y2="17.6" stroke="#0b2026" stroke-width="1.3"/></g><text x="942" y="151.0" font-size="14" font-weight="700" fill="#0b2026" font-family="monospace">gold_deviation_lifecycle</text><text x="942" y="171.0" font-size="14" fill="#5E7077">prebuilt, 1 row / case</text></g><rect x="898" y="205.0" width="250" height="64" rx="8" fill="#FFAB00" fill-opacity="0.10" stroke="#FFAB00" stroke-width="1.5"/><g transform="translate(908,223.0)"><rect x="0" y="2" width="24" height="18" rx="2" fill="none" stroke="#FFAB00" stroke-width="1.5"/><rect x="0" y="2" width="24" height="6" rx="2" fill="#FFAB00"/><line x1="8" y1="8" x2="8" y2="20" stroke="#FFAB00" stroke-width="1.2"/><line x1="16" y1="8" x2="16" y2="20" stroke="#FFAB00" stroke-width="1.2"/><line x1="0" y1="14" x2="24" y2="14" stroke="#FFAB00" stroke-width="1.2"/><circle cx="22" cy="18" r="8" fill="#FFFFFF"/><circle cx="19" cy="18" r="2.6" fill="none" stroke="#0b2026" stroke-width="1.3"/><circle cx="25.5" cy="18" r="2.6" fill="none" stroke="#0b2026" stroke-width="1.3"/><line x1="21.6" y1="17.6" x2="22.9" y2="17.6" stroke="#0b2026" stroke-width="1.3"/></g><text x="942" y="233.0" font-size="14" font-weight="700" fill="#0b2026" font-family="monospace">gold_change_control_cycle</text><text x="942" y="253.0" font-size="14" fill="#5E7077">switch on in Lab 05</text><rect x="898" y="287.0" width="250" height="64" rx="8" fill="#FFAB00" fill-opacity="0.10" stroke="#FFAB00" stroke-width="1.5"/><g transform="translate(908,305.0)"><rect x="0" y="2" width="24" height="18" rx="2" fill="none" stroke="#FFAB00" stroke-width="1.5"/><rect x="0" y="2" width="24" height="6" rx="2" fill="#FFAB00"/><line x1="8" y1="8" x2="8" y2="20" stroke="#FFAB00" stroke-width="1.2"/><line x1="16" y1="8" x2="16" y2="20" stroke="#FFAB00" stroke-width="1.2"/><line x1="0" y1="14" x2="24" y2="14" stroke="#FFAB00" stroke-width="1.2"/><circle cx="22" cy="18" r="8" fill="#FFFFFF"/><circle cx="19" cy="18" r="2.6" fill="none" stroke="#0b2026" stroke-width="1.3"/><circle cx="25.5" cy="18" r="2.6" fill="none" stroke="#0b2026" stroke-width="1.3"/><line x1="21.6" y1="17.6" x2="22.9" y2="17.6" stroke="#0b2026" stroke-width="1.3"/></g><text x="942" y="315.0" font-size="14" font-weight="700" fill="#0b2026" font-family="monospace">gold_inspection_quality</text><text x="942" y="335.0" font-size="14" fill="#5E7077">you build (Lab 06)</text><rect x="898" y="369.0" width="250" height="64" rx="8" fill="#FFAB00" fill-opacity="0.10" stroke="#FFAB00" stroke-width="1.5"/><g transform="translate(908,387.0)"><rect x="0" y="2" width="24" height="18" rx="2" fill="none" stroke="#FFAB00" stroke-width="1.5"/><rect x="0" y="2" width="24" height="6" rx="2" fill="#FFAB00"/><line x1="8" y1="8" x2="8" y2="20" stroke="#FFAB00" stroke-width="1.2"/><line x1="16" y1="8" x2="16" y2="20" stroke="#FFAB00" stroke-width="1.2"/><line x1="0" y1="14" x2="24" y2="14" stroke="#FFAB00" stroke-width="1.2"/><circle cx="22" cy="18" r="7" fill="#FFFFFF"/><path d="M23 13 L18.5 19 L21.5 19 L20 23.5 L26 16.5 L23 16.5 Z" fill="#FFAB00" stroke="#FFFFFF" stroke-width="0.5"/></g><text x="942" y="397.0" font-size="14" font-weight="700" fill="#0b2026" font-family="monospace">gold_oos_events</text><text x="942" y="417.0" font-size="14" fill="#5E7077">you build (Lab 06)</text></svg><div style="margin-top: 18px; padding: 16px 20px; background: #F9F7F4; border: 2px solid #1B5162; border-radius: 8px; font-size: 14pt; line-height: 1.55;"><strong>Read it left to right.</strong> You build 2 Bronze and 2 Silver tables (QC results, change controls), then the QC-results Gold. You switch on the change-control Gold and read the AUTO CDC flow for corrective actions. Corrective actions, change controls and deviation Gold also have optional exercises at the end of each lab.</div></div>
# MAGIC
# MAGIC ##### EXPAND FOR ADDITIONAL NOTES
# MAGIC
# MAGIC <details>
# MAGIC
# MAGIC - Point at the **two Gold shapes** from the same Silver source (`gold_inspection_quality` vs `gold_oos_events`). That is the ST-vs-MV choice of Lab 06.
# MAGIC - `silver_corrective_action` is kept current by **AUTO CDC**: the feed re-sends each action as its status changes, and CDC keeps the latest row per key.
# MAGIC - `batch_record` is the one feed written in Python: same pattern, different language.
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
# MAGIC <div class="ds-row"><div class="ds-card coral"><div class="ds-card-label">Grain</div><div class="ds-card-title">Deviation events</div><ul><li>1 row = one status <strong>event</strong></li><li>a case has many events</li><li>late events arrive for old cases</li></ul></div><div class="ds-card amber"><div class="ds-card-label">Grain</div><div class="ds-card-title">Corrective actions</div><ul><li>1 row = one action <strong>snapshot</strong></li><li>re-sent when status changes</li><li>many actions per case (fan-out risk)</li></ul></div><div class="ds-card blue"><div class="ds-card-label">Grain</div><div class="ds-card-title">Change controls</div><ul><li>1 row = one workflow snapshot</li><li>messy states: <code>appr</code>, <code>Impl</code></li><li>milestones must be in order</li></ul></div><div class="ds-card green"><div class="ds-card-label">Grain</div><div class="ds-card-title">QC results</div><ul><li>1 row = one measurement</li><li>limits travel with the row</li><li>OOS is a valid record with a bad result</li></ul></div></div>
# MAGIC </div>
# MAGIC
# MAGIC ##### EXPAND FOR ADDITIONAL NOTES
# MAGIC
# MAGIC <details>
# MAGIC
# MAGIC Ask before revealing: *what is one row of each feed?* Grain mistakes cause most wrong dashboards (double counting after a join).
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
# MAGIC <div style="font-size:20pt;font-weight:700;margin-bottom:14px;">Responsibilities per layer</div><div class="ds-row"><div class="ds-card amber"><div class="ds-card-title">Bronze</div><ul><li>Keep everything, exactly as it arrived</li><li>Add lineage: <code>source_file</code>, <code>ingested_at</code></li><li>Never fix data here</li></ul></div><div class="ds-card blue"><div class="ds-card-title">Silver</div><ul><li>Type, conform, validate</li><li>Quarantine bad records, keep the reason</li><li>Keep the source grain: no aggregation</li></ul></div><div class="ds-card green"><div class="ds-card-title">Gold</div><ul><li>Answer one business question per table</li><li>State the grain in the table comment</li><li>Combine feeds only here</li></ul></div></div>
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
# MAGIC <div class="ds-row"><div class="ds-card green"><div class="dd-head">&check; Append-only</div><ul><li><strong>Append-only events</strong>: deviations, QC results. Every row is new information.</li><li>Current state (latest status) is computed in Gold from the full history.</li><li>Simple to reason about, easy to replay.</li></ul></div><div class="ds-card coral"><div class="dd-head">&rarr; AUTO CDC</div><ul><li><strong>Changing records</strong>: corrective actions are re-sent every time their status changes.</li><li><code>AUTO CDC INTO</code> keeps the latest row per key (SCD 1) or every version (SCD 2).</li><li>Our <code>silver_corrective_action</code> uses SCD 1; Lab 05 optional adds SCD 2 history.</li></ul></div></div>
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
# MAGIC <div class="ds-callout info"><div class="ds-eyebrow">Coming up in Lecture 04</div><div>How AUTO CDC works, SCD type 1 vs type 2, on our corrective actions.</div></div>
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
# MAGIC var QZ=[{"q": "Where should a corrective-action summary be <strong>joined</strong> to deviations?", "opts": ["Bronze", "Silver", "Gold", "Anywhere"], "ans": 2, "fb": "Feeds are combined only in Gold, after each side is at the right grain."}, {"q": "A QC result of 7.6 with an upper limit of 7.4 is...", "opts": ["a bad record: quarantine it", "a bad result: keep it and flag OOS", "dropped"], "ans": 1, "fb": "The record is valid; the measurement is out of spec. Quarantining it would hide a real quality signal."}, {"q": "What is the grain of <code>gold_deviation_lifecycle</code>?", "opts": ["one row per event", "one row per case", "one row per site"], "ans": 1, "fb": "Events are collapsed to the case's current state."}];
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
# MAGIC 1. Saw that SDP is declarative: you write the transformation, the platform runs the graph
# MAGIC 2. Mapped the five feeds and their grains
# MAGIC 3. Assigned clear responsibilities to Bronze, Silver and Gold
# MAGIC 4. Learned when to use AUTO CDC (SCD type 1 or 2) instead of append-only processing
# MAGIC 5. Identified what you build, switch on and read in today's labs
# MAGIC
# MAGIC ### Next Steps
# MAGIC
# MAGIC In **02 Lecture - Auto Loader and SDP Concepts**, you learn the SDP building blocks you use in the labs.
