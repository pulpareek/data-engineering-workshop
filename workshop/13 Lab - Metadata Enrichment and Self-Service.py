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
# MAGIC <div class="ds-banner info"><div class="ds-banner-icon">13</div><div><div class="ds-banner-title">Metadata enrichment and self-service analytics</div><div class="ds-banner-tagline">20-minute facilitator demo in the session &middot; run every cell yourself afterwards</div></div></div>
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
# MAGIC <div class="flow-grid" style="grid-template-columns:1fr auto 1fr auto 1fr auto 1fr auto 1fr auto 1fr auto 1fr;"><div class="flow-step" style="--accent:#4299E0;"><div class="flow-num">1</div><div class="flow-label">AI drafts<br>descriptions</div></div><div class="flow-arrow">&rarr;</div><div class="flow-step" style="--accent:#00A972;"><div class="flow-num">2</div><div class="flow-label">Steward<br>approves</div></div><div class="flow-arrow">&rarr;</div><div class="flow-step" style="--accent:#FFAB00;"><div class="flow-num">3</div><div class="flow-label">Metadata<br>as code</div></div><div class="flow-arrow">&rarr;</div><div class="flow-step" style="--accent:#FF5F46;"><div class="flow-num">4</div><div class="flow-label">Tags follow<br>lineage</div></div><div class="flow-arrow">&rarr;</div><div class="flow-step" style="--accent:#98102A;"><div class="flow-num">5</div><div class="flow-label">Certified vs<br>sandbox</div></div><div class="flow-arrow">&rarr;</div><div class="flow-step" style="--accent:#1B5162;"><div class="flow-num">6</div><div class="flow-label">Promotion<br>radar</div></div><div class="flow-arrow">&rarr;</div><div class="flow-step" style="--accent:#4299E0;"><div class="flow-num">7</div><div class="flow-label">Impact before<br>change</div></div></div>
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
# MAGIC <div class="ds-row"><div class="ds-card blue"><div class="ds-card-title">AI-ready data</div><div class="ds-card-para">Genie and agents answer well only when every column has a precise description and grain.</div></div><div class="ds-card green"><div class="ds-card-title">Stewards own meaning</div><div class="ds-card-para">AI drafts, people approve. Approved text lives in git, not in someone's head.</div></div><div class="ds-card amber"><div class="ds-card-title">Fast, not ungoverned</div><div class="ds-card-para">Sandboxes stay quick; heavy use triggers promotion into a certified, bundled asset.</div></div></div>
# MAGIC </div>
# MAGIC
# MAGIC ##### EXPAND FOR ADDITIONAL NOTES
# MAGIC
# MAGIC <details>
# MAGIC
# MAGIC Common asks from analytics teams: tags were lost when sandbox views were created, sandbox assets never left the sandbox,
# MAGIC and model changes surprised downstream users. Each section below answers one of those.
# MAGIC - Alation stays the enterprise catalog; Unity Catalog is the technical catalog. The sync is a separate workshop.
# MAGIC
# MAGIC **20-minute demo path:** the six-layer slide, A (AI drafts), D (certified), G (metric view), H (evaluate). B, C, E and F are take-home.
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
# MAGIC <div style="font-size:20pt;font-weight:700;margin-bottom:14px;">Context for Genie and agents: six layers, and where you built each one</div><div class="ds-row"><div class="ds-card blue"><div class="ds-card-label">Layer 0</div><div class="ds-card-title">Data foundation</div><div class="ds-card-para">Gold tables with one stated grain; one <code>lot_id</code> across every feed. <em>Labs 03-06.</em></div></div><div class="ds-card green"><div class="ds-card-label">Layer 1</div><div class="ds-card-title">Metadata</div><div class="ds-card-para">Descriptions with key, joins and caveats; tags as code in every environment. <em>A-C.</em></div></div><div class="ds-card amber"><div class="ds-card-label">Layer 2</div><div class="ds-card-title">Semantics</div><div class="ds-card-para">A metric view with display names and synonyms: one definition of <em>overdue</em>. <em>G.</em></div></div><div class="ds-card coral"><div class="ds-card-label">Layer 3</div><div class="ds-card-title">Trusted assets</div><div class="ds-card-para">Unity Catalog certification on Gold; sandbox radar retires the rest. <em>D-E.</em></div></div><div class="ds-card red"><div class="ds-card-label">Layer 4</div><div class="ds-card-title">Governance</div><div class="ds-card-para">Grants to groups and row filters decide what Genie may read for each user. <em>Lab 11.</em></div></div><div class="ds-card blue"><div class="ds-card-label">Layer 5</div><div class="ds-card-title">Evaluate</div><div class="ds-card-para">Benchmark questions with known answers, rerun after every change. <em>H.</em></div></div></div>
# MAGIC </div>
# MAGIC
# MAGIC ##### EXPAND FOR ADDITIONAL NOTES
# MAGIC
# MAGIC <details>
# MAGIC
# MAGIC From the Databricks guide *Operationalizing Genie Ontology*: model the important definitions deliberately, and let Genie infer the rest from your assets.
# MAGIC - **Layer 0** is the pipeline itself. No metadata can fix mixed grains or two ids for one lot.
# MAGIC - **Layer 1:** write descriptions for a new analyst, including what the table is *not*. Our readiness table says a lot can look ready while QC records sit in quarantine.
# MAGIC - **Layer 2:** metric views carry `display_name`, `synonyms` and `format`, so "late deviations" finds *Overdue cases*. Pages and Domains (business glossary and grouping) come next where enabled.
# MAGIC - **Layer 3:** `system.certification_status = certified` is the Unity Catalog badge Genie treats as authoritative. Deprecate what you no longer stand behind.
# MAGIC - **Layer 4:** two people can get different answers to the same question, because Genie only reads what each one may see.
# MAGIC - **Layer 5:** a failing benchmark is fixed where the meaning lives: metadata, the metric view, or the Genie instructions.
# MAGIC - Start with one domain (here: lot release readiness), harden it, then expand.
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
# MAGIC <div style="font-size:20pt;font-weight:700;margin-bottom:4px;">Layer 1: enrich your metadata</div><div style="font-size:15pt;color:#5E7077;margin-bottom:14px;">Give people and agents real meaning to reason with, starting with the tables they query. Hands-on: sections A-C.</div><div class="ds-row"><div class="ds-card blue"><div class="ds-card-label">1</div><div class="ds-card-title">Describe your assets</div><div class="ds-card-para"><code>is_overdue</code> &rarr; &quot;open, and past <code>target_due_at</code> on the as-of date&quot;. Write for a new analyst: what it is, its grain, its caveats.</div></div><div class="ds-card blue"><div class="ds-card-label">2</div><div class="ds-card-title">Tag and classify</div><div class="ds-card-para"><code>layer = gold</code>, <code>domain = quality</code>, <code>contains_free_text</code> on descriptions. Governed tags keep the values the same everywhere.</div></div><div class="ds-card blue"><div class="ds-card-label">3</div><div class="ds-card-title">Automate at scale</div><div class="ds-card-para">AI drafts every description, a steward approves, <code>metadata.yml</code> keeps it in Git. Nothing reaches Unity Catalog unreviewed.</div></div></div>
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
# MAGIC <div style="font-size:20pt;font-weight:700;margin-bottom:4px;">Layer 2: model the business with a semantic layer</div><div style="font-size:15pt;color:#5E7077;margin-bottom:14px;">Define what a metric means once, and say how tables connect. Hands-on: section G.</div><div class="ds-row"><div class="ds-card amber"><div class="ds-card-label">1</div><div class="ds-card-title">Declare relationships</div><div class="ds-card-para"><code>gold_oos_events.lot_id</code> = <code>gold_deviation_lifecycle.lot_id</code>. Keys and joins in descriptions and in Genie, so nobody guesses.</div></div><div class="ds-card amber"><div class="ds-card-label">2</div><div class="ds-card-title">Metric views</div><div class="ds-card-para"><code>mv_deviation_kpis</code>: <em>Overdue cases</em> = <code>COUNT_IF(is_overdue)</code>, by site, status, severity. One definition.</div></div><div class="ds-card amber"><div class="ds-card-label">3</div><div class="ds-card-title">Agent metadata</div><div class="ds-card-para"><code>display_name</code>, <code>synonyms</code> (&quot;late deviations&quot;), <code>format</code>. People's words land on the right measure.</div></div><div class="ds-card amber"><div class="ds-card-label">4</div><div class="ds-card-title">Domains and Pages</div><div class="ds-card-para">Domain <em>Quality</em>; a Page for &quot;Ready for QA review&quot; owned by QA. Owner-reviewed definitions win over guesses.</div></div></div>
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
# MAGIC <div style="font-size:20pt;font-weight:700;margin-bottom:4px;">Layer 3: curate context-rich assets</div><div style="font-size:15pt;color:#5E7077;margin-bottom:14px;">Genie learns from the dashboards, queries and spaces you already have. Make them worth learning from. Hands-on: sections D-E.</div><div class="ds-row"><div class="ds-card green"><div class="ds-card-label">1</div><div class="ds-card-title">A well-used asset base</div><div class="ds-card-para">The ops dashboard, the Genie space, these notebooks: documented and used, so their context counts.</div></div><div class="ds-card green"><div class="ds-card-label">2</div><div class="ds-card-title">Context-rich assets</div><div class="ds-card-para">Genie instructions plus example SQL such as &quot;open deviations on blocked lots&quot;. One good example fixes a whole class of answers.</div></div><div class="ds-card green"><div class="ds-card-label">3</div><div class="ds-card-title">Certify, and deprecate</div><div class="ds-card-para">Gold tables <code>certified</code>; an old copy or retired view <code>deprecated</code>. Certified beats popular beats unvetted.</div></div><div class="ds-card green"><div class="ds-card-label">4</div><div class="ds-card-title">Classify and monitor quality</div><div class="ds-card-para">Expectations, quarantine and <code>dq_reconciliation</code> catch bad data before people or agents use it.</div></div></div>
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
# MAGIC <div style="font-size:20pt;font-weight:700;margin-bottom:4px;">Layer 4: build the governance layer</div><div style="font-size:15pt;color:#5E7077;margin-bottom:14px;">Genie only uses what the person asking may see. Hands-on: Lab 11, Lecture 10.</div><div class="ds-row"><div class="ds-card coral"><div class="ds-card-label">1</div><div class="ds-card-title">Access controls</div><div class="ds-card-para"><code>GRANT SELECT ON SCHEMA ... TO `quality-analysts`</code>. Same question, correctly different answers per person.</div></div><div class="ds-card coral"><div class="ds-card-label">2</div><div class="ds-card-title">Fine-grained controls</div><div class="ds-card-para">A row filter by site, applied wherever a governed tag says so (ABAC). The policy follows the tag, not the table.</div></div><div class="ds-card coral"><div class="ds-card-label">3</div><div class="ds-card-title">AI Gateway</div><div class="ds-card-para">One control point for the model endpoint behind AI descriptions and Genie: rate limits, logging, cost.</div></div></div>
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
# MAGIC <div style="font-size:20pt;font-weight:700;margin-bottom:4px;">Layer 5: evaluate and improve</div><div style="font-size:15pt;color:#5E7077;margin-bottom:14px;">Definitions drift as the business changes. Measure answer quality before users notice. Hands-on: section H.</div><div class="ds-row"><div class="ds-card red"><div class="ds-card-label">1</div><div class="ds-card-title">Validate before rollout</div><div class="ds-card-para"><code>genie_benchmarks.yml</code>: six questions with known answers, graded by <code>eval_genie.py</code>.</div></div><div class="ds-card red"><div class="ds-card-label">2</div><div class="ds-card-title">Monitor answers and usage</div><div class="ds-card-para">Genie monitoring shows questions, answers and feedback; query history shows what ran.</div></div><div class="ds-card red"><div class="ds-card-label">3</div><div class="ds-card-title">Fix at the right layer</div><div class="ds-card-para">Wrong word &rarr; a synonym. Wrong measure &rarr; the metric view. Wrong join &rarr; Genie instructions. Vague column &rarr; <code>metadata.yml</code>.</div></div><div class="ds-card red"><div class="ds-card-label">4</div><div class="ds-card-title">Watch for drift</div><div class="ds-card-para">Tag-drift check, sandbox radar, re-run the benchmarks after every deploy. Owners and a review cadence per domain.</div></div></div>
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
# MAGIC <div class="ds-callout info"><div class="ds-eyebrow">Run what your rights allow; read the rest</div><div>Sections A, C, E and F need Foundation Model access or system tables. Without them, each cell shows what is missing and who grants it. B, D, G and H work for everyone. Lecture 10 has the admin checklist to switch everything on.</div></div>
# MAGIC </div>

# COMMAND ----------

%run ./Includes/Classroom-Setup

# COMMAND ----------

dbutils.widgets.text("llm_endpoint", "databricks-claude-sonnet-5-5", "Foundation model endpoint")
LLM = dbutils.widgets.get("llm_endpoint")
import os
DOC = f"{STAGING}/docs/qms_vendor_data_dictionary.txt"
try:
    dbutils.fs.ls(DOC)
except Exception:  # shared volume not staged: use the copy that ships in the repo (data/docs)
    DOC = "file:" + os.path.join(ROOT, "data", "docs", "qms_vendor_data_dictionary.txt")
print(LLM, DOC)

# COMMAND ----------

# MAGIC %md
# MAGIC ## A. AI drafts the descriptions
# MAGIC Inputs: column names, a few sample values, and the vendor's own documentation (here a fictional QMS field reference that stands in for scraped vendor docs).

# COMMAND ----------

vendor_doc = "\n".join(r.value for r in spark.read.text(DOC).collect())
print(vendor_doc[:500], "...")

# COMMAND ----------

with needs('Foundation Model APIs and CAN QUERY on the endpoint in the llm_endpoint widget',
           'A workspace admin: enable Foundation Model APIs (Serving) or grant CAN QUERY on a model serving endpoint.',
           'An AI draft of every column description lands in metadata_suggestions for a steward to review.'):
    import json

    TABLE = "gold_deviation_lifecycle"
    cols = [(f.name, f.dataType.simpleString()) for f in spark.table(f"{FQ}.{TABLE}").schema.fields]
    sample = spark.table(f"{FQ}.{TABLE}").limit(3).toPandas().astype(str).to_dict("records")
    prompt = (
        "You are a data steward assistant for a biopharma quality data product. "
        f"Write a one-sentence business description for each column of table {TABLE}. "
        "Use the vendor documentation when it applies, state units and allowed values, never invent facts. "
        'Reply with JSON only: {"columns": [{"column": "...", "description": "...", "confidence": "high|medium|low"}]}\n'
        f"COLUMNS: {cols}\nSAMPLE ROWS: {sample}\nVENDOR DOCUMENTATION:\n{vendor_doc}"
    )
    spark.createDataFrame([(prompt,)], "prompt STRING").createOrReplaceTempView("steward_prompt")
    reply = spark.sql(f"SELECT ai_query('{LLM}', prompt) FROM steward_prompt").first()[0]
    raw = reply[reply.find("{"): reply.rfind("}") + 1]  # tolerate code fences or a preamble
    rows = [(TABLE, c["column"], c["description"], c["confidence"], "PROPOSED") for c in json.loads(raw)["columns"]]
    (spark.createDataFrame(rows, "table_name STRING, column_name STRING, proposed_description STRING, confidence STRING, status STRING")
          .write.mode("overwrite").saveAsTable(f"{FQ}.metadata_suggestions"))
    display(spark.table(f"{FQ}.metadata_suggestions"))

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
# MAGIC <div class="ds-callout info"><div class="ds-eyebrow">UI equivalent</div><div>Catalog Explorer &rarr; table &rarr; <strong>AI generate</strong> beside the description. Same idea, one table at a time. The SQL route scales to a whole schema and keeps a review queue.</div></div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## B. The steward approves (human in the loop)
# MAGIC Only approved text is exported to `governance/metadata.yml` and goes through a pull request.

# COMMAND ----------

with needs('The metadata_suggestions table from step A',
           'Run step A first (it needs Foundation Model access).',
           'High-confidence drafts are approved and printed as YAML to paste into governance/metadata.yml.'):
    spark.sql(f"UPDATE {FQ}.metadata_suggestions SET status = 'APPROVED' WHERE confidence = 'high'")
    approved = spark.sql(f"SELECT column_name, proposed_description FROM {FQ}.metadata_suggestions WHERE status = 'APPROVED'").collect()
    print("# paste under tables.gold_deviation_lifecycle.columns in governance/metadata.yml, then open a PR")
    for r in approved:
        print(f"      {r.column_name}: {json.dumps(r.proposed_description)}")

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
# MAGIC <div class="flow-grid" style="grid-template-columns:1fr auto 1fr auto 1fr auto 1fr auto 1fr;"><div class="flow-step" style="--accent:#4299E0;"><div class="flow-num">1</div><div class="flow-label">Edit <code>metadata.yml</code></div></div><div class="flow-arrow">&rarr;</div><div class="flow-step" style="--accent:#00A972;"><div class="flow-num">2</div><div class="flow-label">Pull request<br>+ review</div></div><div class="flow-arrow">&rarr;</div><div class="flow-step" style="--accent:#FFAB00;"><div class="flow-num">3</div><div class="flow-label"><code>bundle deploy</code></div></div><div class="flow-arrow">&rarr;</div><div class="flow-step" style="--accent:#FF5F46;"><div class="flow-num">4</div><div class="flow-label">Job task<br><code>apply_metadata</code></div></div><div class="flow-arrow">&rarr;</div><div class="flow-step" style="--accent:#98102A;"><div class="flow-num">5</div><div class="flow-label">Same tags in<br>dev, QA, prod</div></div></div>
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
# MAGIC <div class="ds-callout success"><div class="ds-eyebrow">Metadata as code</div><div class="ds-callout-title">Tags are part of the release, not a manual step.</div><ul><li><code>resources/iops_workshop.job.yml</code>: refresh pipeline &rarr; <code>apply_metadata</code>.</li><li>Idempotent; tag-policy rejections are reported per tag, never silently dropped.</li><li>Answers &quot;tags never made it from dev to QA&quot;.</li></ul></div>
# MAGIC </div>

# COMMAND ----------

display(spark.sql(f"""SELECT table_name, tag_name, tag_value FROM {CATALOG}.information_schema.table_tags
WHERE schema_name = '{SCHEMA}' ORDER BY table_name, tag_name"""))

# COMMAND ----------

# MAGIC %md
# MAGIC ## C. Tags that follow lineage
# MAGIC An analyst builds a sandbox view on two Gold tables. Does the view carry the sources' tags?

# COMMAND ----------

with needs('SELECT on the system tables system.access.* (lineage)',
           'A metastore or account admin: enable the system schema, then GRANT USE CATALOG ON CATALOG system, USE SCHEMA ON SCHEMA system.access and SELECT ON SCHEMA system.access TO your group.',
           'Tags that the sources carry but the derived sandbox view lost (tag drift).'):
    spark.sql(f"""CREATE OR REPLACE VIEW {FQ}.sandbox_site_quality_view AS
    SELECT d.site_code, count_if(d.is_overdue) AS overdue_cases, max(q.oos) AS oos_results
    FROM {FQ}.gold_deviation_lifecycle d
    JOIN (SELECT site_code, sum(oos_results) AS oos FROM {FQ}.gold_inspection_quality GROUP BY site_code) q USING (site_code)
    GROUP BY d.site_code""")
    drift = spark.sql(f"""
    WITH src AS (SELECT DISTINCT source_table_full_name AS src, target_table_full_name AS tgt FROM system.access.table_lineage
                 WHERE target_table_full_name = '{FQ}.sandbox_site_quality_view'),
    tags AS (SELECT concat_ws('.', catalog_name, schema_name, table_name) AS t, tag_name, tag_value
             FROM {CATALOG}.information_schema.table_tags)
    SELECT s.tgt AS derived_object, s.src AS source_object, st.tag_name, st.tag_value AS source_value
    FROM src s JOIN tags st ON st.t = s.src
    LEFT JOIN tags dt ON dt.t = s.tgt AND dt.tag_name = st.tag_name
    WHERE dt.tag_value IS NULL""")
    display(drift)  # empty right after creation: lineage reaches system tables within minutes, re-run later

# COMMAND ----------

with needs('SELECT on the system tables system.access.* (lineage), and APPLY TAG on the view',
           'A metastore or account admin: enable the system schema, then GRANT USE CATALOG ON CATALOG system, USE SCHEMA ON SCHEMA system.access and SELECT ON SCHEMA system.access TO your group. APPLY TAG comes with owning the view.',
           'The view gets the strictest source tags back.'):
    # Fix: copy source tags onto the derived object (schedule this over every sandbox schema)
    for r in drift.select("derived_object", "tag_name", "source_value").distinct().collect():
        try:
            spark.sql(f"ALTER VIEW {r.derived_object} SET TAGS ('{r.tag_name}' = '{r.source_value}')")
        except Exception as e:
            print("not applied:", r.tag_name, str(e).splitlines()[0][:120])

# COMMAND ----------

# MAGIC %md
# MAGIC ## D. Certified vs sandbox
# MAGIC Certified = bundle-deployed, described, owned by a group, and carrying Unity Catalog's own marker `system.certification_status = certified` (set by `apply_metadata` from `metadata.yml`). Catalog Explorer and search show the badge, and Genie prefers certified sources. Everything else is sandbox.

# COMMAND ----------

display(spark.sql(f"""SELECT t.table_name, t.table_owner, tg.tag_value AS certification, t.comment IS NOT NULL AS described
FROM {CATALOG}.information_schema.tables t
LEFT JOIN {CATALOG}.information_schema.table_tags tg
  ON tg.schema_name = t.table_schema AND tg.table_name = t.table_name AND tg.tag_name = 'system.certification_status'
WHERE t.table_schema = '{SCHEMA}' ORDER BY certification NULLS LAST, t.table_name"""))

# COMMAND ----------

# MAGIC %md
# MAGIC ## E. Sandbox promotion radar
# MAGIC Used by many people for a long time? Promote it into a bundle. Unused for 90 days? Retire it.

# COMMAND ----------

with needs('SELECT on the system tables system.access.* (lineage)',
           'A metastore or account admin: enable the system schema, then GRANT USE CATALOG ON CATALOG system, USE SCHEMA ON SCHEMA system.access and SELECT ON SCHEMA system.access TO your group.',
           'Which sandbox objects to promote into a bundle and which to retire.'):
    display(spark.sql(f"""
    SELECT source_table_full_name AS object,
           count(DISTINCT created_by)          AS distinct_users,
           count(DISTINCT to_date(event_time)) AS active_days,
           max(event_time)                     AS last_read,
           CASE WHEN count(DISTINCT created_by) >= 3 AND count(DISTINCT to_date(event_time)) >= 20 THEN 'PROMOTE: move into a bundle'
                WHEN max(event_time) < current_date() - INTERVAL 90 DAYS THEN 'RETIRE: no reads in 90 days'
                ELSE 'KEEP in sandbox' END     AS recommendation
    FROM system.access.table_lineage
    WHERE source_table_catalog = '{CATALOG}' AND source_table_schema = '{SCHEMA}'
      AND event_time > current_date() - INTERVAL 180 DAYS
    GROUP BY ALL ORDER BY distinct_users DESC"""))

# COMMAND ----------

# MAGIC %md
# MAGIC ## F. Impact before you change a Gold column
# MAGIC Who reads `is_overdue`? Notify them before the definition changes.

# COMMAND ----------

with needs('SELECT on the system tables system.access.* (column lineage)',
           'A metastore or account admin: enable the system schema, then GRANT USE CATALOG ON CATALOG system, USE SCHEMA ON SCHEMA system.access and SELECT ON SCHEMA system.access TO your group.',
           'Everyone who reads is_overdue, to notify before the definition changes.'):
    display(spark.sql(f"""SELECT target_table_full_name, target_column_name, entity_type, created_by, max(event_time) AS last_seen
    FROM system.access.column_lineage
    WHERE source_table_full_name = '{FQ}.gold_deviation_lifecycle' AND source_column_name = 'is_overdue'
    GROUP BY ALL ORDER BY last_seen DESC"""))
    # Change log of a pipeline-owned table = its pipeline updates (data) + git history of its SQL file (definition)
    display(spark.sql(f"""SELECT timestamp, origin.update_id, details:create_update:cause::string AS cause,
           details:user_action:user_name::string AS triggered_by, message
    FROM {FQ}.event_log_iops_quality
    WHERE event_type IN ('create_update', 'user_action') ORDER BY timestamp DESC LIMIT 10"""))

# COMMAND ----------

# MAGIC %md
# MAGIC ## G. A semantic layer: one definition per KPI
# MAGIC Dashboards and Genie use the metric view, so *overdue* means the same thing everywhere. `display_name`, `synonyms` and `format` are written for people and agents: someone asking for *late deviations* lands on *Overdue cases*.

# COMMAND ----------

spark.sql(f"""CREATE OR REPLACE VIEW {FQ}.mv_deviation_kpis
WITH METRICS LANGUAGE YAML AS $$
version: 1.1
source: {FQ}.gold_deviation_lifecycle
comment: "Deviation KPIs for IOPS quality (synthetic training data)"
dimensions:
  - name: Site
    expr: site_code
    display_name: Manufacturing site
    synonyms: [plant, facility]
  - name: Status
    expr: current_status
    comment: "Latest normalized deviation status."
  - name: Severity
    expr: coalesce(severity, 'NOT CLASSIFIED')
    comment: "NOT CLASSIFIED for cases reported before the QMS sent severity."
measures:
  - name: Cases
    expr: COUNT(1)
    display_name: Deviation cases
    synonyms: [deviations, cases]
  - name: Open cases
    expr: COUNT_IF(is_open)
    comment: "Cases not CLOSED or CANCELLED."
    synonyms: [open deviations, active deviations]
  - name: Overdue cases
    expr: COUNT_IF(is_overdue)
    comment: "Open cases past target_due_at on the as-of date."
    display_name: Overdue deviations
    synonyms: [late deviations, past due deviations]
  - name: Overdue rate pct
    expr: ROUND(100 * COUNT_IF(is_overdue) / NULLIF(COUNT_IF(is_open), 0), 1)
    comment: "Overdue cases as a percentage of open cases."
    display_name: Overdue rate (%)
    format:
      type: number
      decimal_places:
        type: exact
        places: 1
$$""")
display(spark.sql(f"""SELECT Site, MEASURE(`Open cases`) AS open_cases, MEASURE(`Overdue cases`) AS overdue,
       MEASURE(`Overdue rate pct`) AS overdue_rate_pct FROM {FQ}.mv_deviation_kpis GROUP BY Site ORDER BY Site"""))

# COMMAND ----------

# MAGIC %md
# MAGIC ## H. Evaluate: does Genie give the right number?
# MAGIC `governance/genie_benchmarks.yml` holds the questions people ask, each with validated SQL and an expected answer taken from the same metrics the checkpoints use. `facilitator/eval_genie.py` asks the Genie space every question and grades it. Rerun it after any change to tables, metadata, the metric view or the Genie instructions.

# COMMAND ----------

import yaml, json
bench = yaml.safe_load(open(f"{ROOT}/governance/genie_benchmarks.yml"))["questions"]
expected = json.load(open(f"{ROOT}/data/expected_metrics.json"))["after_run"]["3"]
rows = []
for b in bench:
    table, key = b["expected"].split(".")
    if not spark.catalog.tableExists(f"{FQ}.{table}"):
        rows.append((b["question"], expected[table][key], None, "skipped: your pipeline does not build " + table))
        continue
    got = spark.sql(b["sql"].format(s=FQ)).first()[0]
    rows.append((b["question"], expected[table][key], got, "matches" if got == expected[table][key] else "DIFFERENT"))
display(spark.createDataFrame(rows, "question STRING, expected LONG, answer_key LONG, result STRING"))

# COMMAND ----------

# MAGIC %md
# MAGIC Then grade the Genie space itself (web terminal or laptop, after S3 created it):
# MAGIC ```bash
# MAGIC python facilitator/eval_genie.py --space-id <space id> --schema <catalog>.<your_schema> --warehouse <warehouse id>
# MAGIC ```
# MAGIC A failure points at the layer to fix: a vague column (metadata.yml), a missing synonym (metric view), or a wrong join (Genie instructions).

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
# MAGIC <div class="ds-row"><div class="ds-card green"><div class="ds-card-title">Unity Catalog does</div><ul><li>Technical metadata, lineage, tags, policies</li><li>AI-drafted descriptions</li><li>Certified badges in search and Genie</li></ul></div><div class="ds-card blue"><div class="ds-card-title">Alation does</div><ul><li>Enterprise glossary across platforms</li><li>Business stewardship workflow</li><li>Sync with UC via API or MCP (separate session)</li></ul></div><div class="ds-card amber"><div class="ds-card-title">Process does</div><ul><li>PR review of metadata.yml</li><li>Change records for Gold changes</li><li>Quarterly sandbox radar review</li></ul></div></div>
# MAGIC </div>
