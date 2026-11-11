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
# MAGIC <div class="ds-banner info"><div class="ds-banner-icon">10</div><div><div class="ds-banner-title">Unity Catalog: govern what you built</div><div class="ds-banner-tagline">10 minutes &middot; then explore your own tables in Lab 11</div></div></div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## Overview
# MAGIC
# MAGIC Everything you built lives in Unity Catalog. Learn how it is organised, who can see it, and how tags, lineage and the event log let you find, trace and watch your tables, then apply it to your own schema in Lab 11.
# MAGIC
# MAGIC ## Learning Objectives
# MAGIC
# MAGIC By the end of this lecture, you will be able to:
# MAGIC
# MAGIC 1. **Navigate the three-level namespace**: catalog, schema, table or volume
# MAGIC 2. **Grant access to groups**, not people, with the privilege ladder
# MAGIC 3. **Use tags, lineage and the event log** to find, trace and monitor tables
# MAGIC 4. **Explain why tags must live in code** (`metadata.yml`) to reach every environment
# MAGIC 5. **Describe site-based access** with a row filter

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
# MAGIC <div style="font-size:20pt;font-weight:700;margin-bottom:14px;">Three-level namespace</div><div class="ds-row"><div class="ds-card blue"><div class="ds-card-title">Catalog</div><div class="ds-card-para">Environment or domain boundary: <code>quality_dev</code>, <code>quality_qa</code>, sandbox.</div></div><div class="ds-card green"><div class="ds-card-title">Schema</div><div class="ds-card-para">Data product, or a person in a workshop: <code>iops_sandbox.‹you›</code>. Grants usually live here.</div></div><div class="ds-card amber"><div class="ds-card-title">Table / volume</div><div class="ds-card-para">Bronze &rarr; Gold tables and the landing volume, all governed the same way.</div></div></div>
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
# MAGIC <div class="ds-row"><div class="ds-card green"><div class="dd-head">Sandbox</div><ul><li><strong>Sandbox</strong>: personal or team schemas, fast, uncertified, reviewed every 90 days.</li><li>Promotion = code in the bundle, deployed to a certified schema.</li></ul></div><div class="ds-card coral"><div class="dd-head">Certified</div><ul><li><strong>Certified</strong>: only bundle-deployed, tagged, owned by a group.</li><li>Never hand-edit; consumers see the certified badge.</li></ul></div></div>
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
# MAGIC <div class="flow-grid" style="grid-template-columns:1fr auto 1fr auto 1fr;"><div class="flow-step" style="--accent:#4299E0;"><div class="flow-num">1</div><div class="flow-label">USE CATALOG</div></div><div class="flow-arrow">&rarr;</div><div class="flow-step" style="--accent:#00A972;"><div class="flow-num">2</div><div class="flow-label">USE SCHEMA</div></div><div class="flow-arrow">&rarr;</div><div class="flow-step" style="--accent:#FFAB00;"><div class="flow-num">3</div><div class="flow-label">SELECT on table</div></div></div>
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
# MAGIC <div class="ds-callout info"><div class="ds-eyebrow">Grant to groups, not people</div><div>Analysts get the Gold tables; they never need Bronze. Ownership belongs to a group so people can leave.</div></div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC Grants are plain SQL, always to groups:
# MAGIC ```sql
# MAGIC GRANT USE CATALOG ON CATALOG <catalog> TO `iops-analysts`;
# MAGIC GRANT USE SCHEMA  ON SCHEMA  <catalog>.<schema> TO `iops-analysts`;
# MAGIC GRANT SELECT      ON TABLE   <catalog>.<schema>.gold_deviation_lifecycle TO `iops-analysts`;
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
# MAGIC <div style="font-size:20pt;font-weight:700;margin-bottom:14px;">Find it, trace it, watch it</div><div class="ds-row"><div class="ds-card blue"><div class="ds-card-title">Tags</div><ul><li>Classify once: domain, layer, classification, owner</li><li>Search, policies and Genie use them</li><li>Governed tags: an admin fixes the allowed values</li></ul></div><div class="ds-card green"><div class="ds-card-title">Lineage</div><ul><li>Captured automatically, table and column level</li><li>Catalog Explorer &rarr; Lineage tab</li><li>Queryable: <code>system.access.table_lineage</code></li></ul></div><div class="ds-card amber"><div class="ds-card-title">Event log</div><ul><li>Every pipeline update, flow and expectation</li><li>Published to UC as a table</li><li>Data-quality metrics without extra code</li></ul></div></div>
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
# MAGIC <div class="ds-callout caution row"><div class="ds-callout-icon">!</div><div><div class="ds-eyebrow">Tags typed in a notebook do not travel</div><div>A tag set by hand in dev is missing in QA. Lab 13 moves tags and descriptions into the bundle so every environment gets them.</div></div></div>
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
# MAGIC <div class="ds-row"><div class="ds-card blue"><div class="ds-card-title">Site-based access (demo)</div><ul><li>Row filter: SITE-A QA sees only SITE-A</li><li><code>is_account_group_member('site-a-qa')</code></li><li>Applied once on the table, honored everywhere</li></ul></div><div class="ds-card green"><div class="ds-card-title">Monitor in production</div><ul><li>Alert on quarantine growth</li><li>Alert on failed updates</li><li>Cost via system.billing</li></ul></div><div class="ds-card amber"><div class="ds-card-title">Out of scope today</div><ul><li>Alation sync</li><li>ServiceNow change flow</li><li>ABAC policies at scale</li></ul></div></div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## What each capability needs, and who grants it
# MAGIC Some of this needs rights a workshop sandbox may not give you. The lab still shows what it does; in your own workspace, ask for the right below.

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
# MAGIC </style>
# MAGIC <div class="ds-row"><div class="ds-card blue"><table class="dt"><tr><th>Capability</th><th>You need</th><th>Granted by</th><th>Without it</th></tr><tr class=""><td>Grants on your schema</td><td>own the schema</td><td>you</td><td>always works</td></tr><tr class=""><td>Groups (stewards, site QA)</td><td>manage groups</td><td>account admin (or workspace admin)</td><td>grant to yourself, read the pattern</td></tr><tr class=""><td>Tags on schemas, tables, columns</td><td>own the object (or APPLY TAG)</td><td>you</td><td>always works</td></tr><tr class=""><td>Governed tags (fixed values)</td><td>ASSIGN on the governed tag</td><td>account admin (tag policy)</td><td>plain tags, same YAML</td></tr><tr class=""><td>Certified / deprecated badge</td><td>ASSIGN on <code>system.certification_status</code></td><td>account or metastore admin</td><td>a <code>certification</code> tag</td></tr><tr class=""><td>Row filters, column masks</td><td>own the table + a SQL function</td><td>you (ABAC: an admin)</td><td>a filtered view</td></tr><tr class=""><td>Domain on the Discover page</td><td>MANAGE DISCOVER + ASSIGN on the domain tag</td><td>workspace or account admin</td><td>a <code>domain</code> tag</td></tr><tr class=""><td>Pages, wikis (business terms)</td><td>MANAGE PAGES / table owner</td><td>admin or domain manager</td><td>table and column comments</td></tr><tr class=""><td>Lineage, audit, query history</td><td>SELECT on <code>system.access</code>, <code>system.query</code></td><td>metastore admin enables system tables</td><td>Catalog Explorer &rarr; Lineage tab</td></tr><tr class=""><td>Cost by tag</td><td>SELECT on <code>system.billing</code></td><td>account admin</td><td>ask for a cost dashboard</td></tr><tr class=""><td>AI-drafted descriptions</td><td>Foundation Model APIs (CAN QUERY)</td><td>workspace admin</td><td>Catalog Explorer &rarr; AI generate</td></tr></table></div></div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## Switching it on in your workspace: the admin checklist
# MAGIC Click each step. An admin does them once; after that every team gets the full governance flow you saw today.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div class="acc-wrap" id="acc2">
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
# MAGIC   var root = document.getElementById('acc2'), box = root.querySelector('.acc-container'), DATA = [{"summary": "Turn on the system tables", "detail": "<code>databricks system-schemas enable ‹metastore-id› access</code> (repeat for <code>billing</code> and <code>query</code>).", "fix": "Gives lineage, audit, query history and billing as SQL tables."}, {"summary": "Grant them to a group, not to people", "detail": "<code>GRANT USE CATALOG ON CATALOG system TO `data-stewards`;</code><br><code>GRANT USE SCHEMA, SELECT ON SCHEMA system.access TO `data-stewards`;</code>", "fix": "Stewards and platform owners can now run Lab 11 section C and Lab 13 sections C to F."}, {"summary": "Create governed tags for the vocabulary you must enforce", "detail": "Catalog Explorer &rarr; <strong>Govern</strong> &rarr; <strong>Governed tags</strong>: key (for example <code>data_classification</code>), allowed values, and <strong>ASSIGN</strong> for the steward group.", "fix": "Wrong values are rejected at write time; <code>metadata.yml</code> uses the same keys in every environment."}, {"summary": "Let stewards certify and deprecate", "detail": "Grant ASSIGN on the system tag <code>system.certification_status</code> to the steward group.", "fix": "Certified tables get a badge in search, Catalog Explorer and Genie."}, {"summary": "Create the groups", "detail": "Account console &rarr; <strong>User management</strong> &rarr; <strong>Groups</strong>: for example <code>data-stewards</code>, <code>site-a-qa</code>. Add people, then use the group in every GRANT and policy.", "fix": "Access follows the team, not the person; leavers and joiners are one change."}, {"summary": "Protect sensitive data by tag (ABAC)", "detail": "Write one mask function, then one policy on the schema:<br><code>CREATE POLICY mask_free_text ON SCHEMA \u2039catalog\u203a.\u2039schema\u203a<br>COLUMN MASK \u2039catalog\u203a.\u2039schema\u203a.redact_text TO `account users` EXCEPT `data-stewards`<br>FOR TABLES MATCH COLUMNS has_tag_value('masking_rule', 'redact') AS c ON COLUMN c;</code>", "fix": "One rule covers every column with that governed tag, today and in tables built later. Needs MANAGE on the schema and a governed tag. Live demo: Lab 11 section F."}, {"summary": "Publish a domain", "detail": "Discover page &rarr; <strong>Create domain</strong>: pick a governed tag (the domain name, for example <em>Manufacturing and Quality</em>), add owners, <strong>Publish</strong>. Tag a schema with it and all its tables join the domain.", "fix": "Consumers browse by business area; Genie and search can filter on it. Pages and wikis add the business terms."}, {"summary": "Allow AI help for metadata", "detail": "Enable Foundation Model APIs and grant CAN QUERY on an endpoint to the steward group.", "fix": "Lab 13 section A: AI drafts, stewards approve, Git keeps the result."}];
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
# MAGIC ## Conclusion
# MAGIC
# MAGIC In this lecture, you:
# MAGIC
# MAGIC 1. Navigated catalogs, schemas, tables and volumes
# MAGIC 2. Learned to grant access to groups with the privilege ladder
# MAGIC 3. Used tags, lineage and the event log to find, trace and watch tables
# MAGIC 4. Saw why tags belong in code, and how a row filter limits rows per site
# MAGIC
# MAGIC ### Next Steps
# MAGIC
# MAGIC In **11 Lab - Govern and Observe Your Pipeline**, you apply grants, tags, lineage and event-log queries to your own tables.
