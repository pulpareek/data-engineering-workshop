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
# MAGIC <div class="ds-banner info"><div class="ds-banner-icon">8</div><div><div class="ds-banner-title">Bundles: one project, every environment</div><div class="ds-banner-tagline">10 minutes &middot; then you promote your own pipeline in Lab 09</div></div></div>
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
# MAGIC <div class="flow-grid" style="grid-template-columns:1fr auto 1fr auto 1fr auto 1fr auto 1fr auto 1fr;"><div class="flow-step dim" style="--accent:#4299E0;"><div class="flow-num">1</div><div class="flow-label">Land files</div></div><div class="flow-arrow dim">&rarr;</div><div class="flow-step dim" style="--accent:#00A972;"><div class="flow-num">2</div><div class="flow-label">Bronze</div></div><div class="flow-arrow dim">&rarr;</div><div class="flow-step dim" style="--accent:#FFAB00;"><div class="flow-num">3</div><div class="flow-label">Silver</div></div><div class="flow-arrow dim">&rarr;</div><div class="flow-step dim" style="--accent:#FF5F46;"><div class="flow-num">4</div><div class="flow-label">Gold</div></div><div class="flow-arrow dim">&rarr;</div><div class="flow-step dim" style="--accent:#98102A;"><div class="flow-num">5</div><div class="flow-label">New batch</div></div><div class="flow-arrow">&rarr;</div><div class="flow-step" style="--accent:#1B5162;"><div class="flow-num">6</div><div class="flow-label">Promote</div></div></div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## Overview
# MAGIC
# MAGIC Your pipeline works in dev. Now make it a project you can ship: a bundle describes the pipeline, its schema and its job in YAML next to the code, and one command deploys the same thing to dev, QA or production with only a few values changed.
# MAGIC
# MAGIC ## Learning Objectives
# MAGIC
# MAGIC By the end of this lecture, you will be able to:
# MAGIC
# MAGIC 1. **Explain what a bundle is**: what runs, what it runs on, where it runs
# MAGIC 2. **Read `databricks.yml`** and say what changes per target (dev, qa)
# MAGIC 3. **Use variables** (built-in, custom, lookup) to keep the project portable
# MAGIC 4. **Run the bundle lifecycle** (validate, deploy, run) and describe the QA gate
# MAGIC 5. **Explain the Git workflow**: a pull request deploys dev, a merge deploys QA, run by GitHub Actions
# MAGIC 6. **List the production controls**: schedule, notifications, run as a service principal, CI

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
# MAGIC <div style="font-size:20pt;font-weight:700;margin-bottom:14px;">A Databricks project is three things</div><div class="ds-row"><div class="ds-card blue"><div class="ds-card-label">Code</div><div class="ds-card-title">What runs</div><div class="ds-card-para">Pipeline SQL and Python, notebooks.</div></div><div class="ds-card green"><div class="ds-card-label">Resources</div><div class="ds-card-title">What it runs on</div><div class="ds-card-para">Pipeline, job, schema, volume, dashboard, app.</div></div><div class="ds-card amber"><div class="ds-card-label">Environment</div><div class="ds-card-title">Where it runs</div><div class="ds-card-para">Workspace, catalog, compute, identity.</div></div></div>
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
# MAGIC <div class="ds-callout success"><div class="ds-eyebrow">Write once, deploy everywhere</div><div>A bundle describes all three in YAML next to the code. The CLI validates, deploys and runs it; dev, QA and prod differ only in a few target values.</div></div>
# MAGIC </div>
# MAGIC
# MAGIC ##### EXPAND FOR ADDITIONAL NOTES
# MAGIC
# MAGIC <details>
# MAGIC
# MAGIC - **Why not click it together in the UI?** Clicks do not repeat, and nobody can review them.
# MAGIC - **Why not REST / SDK scripts or Terraform?** Scripts make you track state yourself; Terraform is another language and lives apart from the code.
# MAGIC - **Bundles** keep code and configuration in one Git repo, reviewed in one PR, deployed with one command per environment.
# MAGIC
# MAGIC </details>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div style="max-width: 1100px; margin: 0 auto; font-family: sans-serif; color: #0b2026;"><div style="text-align: center; margin-bottom: 12px;"><div style="font-size: 22pt; font-weight: 700;">One project, three environments</div><div style="font-size: 14pt; color: #618794; margin-top: 4px;">Code and configuration are versioned together; only target values change</div></div><svg width="100%" viewBox="0 0 1158 336" role="img" style="font-family: sans-serif;"><defs><marker id="med-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="#5E7077" stroke-width="1.5"/></marker></defs><path d="M854 155.0 L894 155.0" fill="none" stroke="#5E7077" stroke-width="1.6" marker-end="url(#med-arrow)"/><path d="M558 155.0 L598 155.0" fill="none" stroke="#5E7077" stroke-width="1.6" marker-end="url(#med-arrow)"/><path d="M262 196.0 L302 155.0" fill="none" stroke="#5E7077" stroke-width="1.6" marker-end="url(#med-arrow)"/><path d="M262 114.0 L302 155.0" fill="none" stroke="#5E7077" stroke-width="1.6" marker-end="url(#med-arrow)"/><rect x="10" y="10" width="250" height="32" rx="16" fill="#1B5162"/><text x="135.0" y="31" text-anchor="middle" font-size="14" font-weight="700" fill="#FFFFFF" letter-spacing="2">YOUR GIT FOLDER</text><rect x="10" y="82.0" width="250" height="64" rx="8" fill="#1B5162" fill-opacity="0.10" stroke="#1B5162" stroke-width="1.5"/><g transform="translate(20,100.0)"><rect x="0" y="2" width="24" height="18" rx="2" fill="none" stroke="#1B5162" stroke-width="1.5"/><rect x="0" y="2" width="24" height="6" rx="2" fill="#1B5162"/><line x1="8" y1="8" x2="8" y2="20" stroke="#1B5162" stroke-width="1.2"/><line x1="16" y1="8" x2="16" y2="20" stroke="#1B5162" stroke-width="1.2"/><line x1="0" y1="14" x2="24" y2="14" stroke="#1B5162" stroke-width="1.2"/></g><text x="54" y="110.0" font-size="14" font-weight="700" fill="#0b2026" font-family="monospace">databricks.yml</text><text x="54" y="130.0" font-size="14" fill="#5E7077">targets + variables</text><rect x="10" y="164.0" width="250" height="64" rx="8" fill="#1B5162" fill-opacity="0.10" stroke="#1B5162" stroke-width="1.5"/><g transform="translate(20,182.0)"><rect x="0" y="2" width="24" height="18" rx="2" fill="none" stroke="#1B5162" stroke-width="1.5"/><rect x="0" y="2" width="24" height="6" rx="2" fill="#1B5162"/><line x1="8" y1="8" x2="8" y2="20" stroke="#1B5162" stroke-width="1.2"/><line x1="16" y1="8" x2="16" y2="20" stroke="#1B5162" stroke-width="1.2"/><line x1="0" y1="14" x2="24" y2="14" stroke="#1B5162" stroke-width="1.2"/></g><text x="54" y="192.0" font-size="14" font-weight="700" fill="#0b2026" font-family="monospace">src/‹pipeline›/</text><text x="54" y="212.0" font-size="14" fill="#5E7077">SQL + Python</text><rect x="10" y="246.0" width="250" height="64" rx="8" fill="#1B5162" fill-opacity="0.10" stroke="#1B5162" stroke-width="1.5"/><g transform="translate(20,264.0)"><rect x="0" y="2" width="24" height="18" rx="2" fill="none" stroke="#1B5162" stroke-width="1.5"/><rect x="0" y="2" width="24" height="6" rx="2" fill="#1B5162"/><line x1="8" y1="8" x2="8" y2="20" stroke="#1B5162" stroke-width="1.2"/><line x1="16" y1="8" x2="16" y2="20" stroke="#1B5162" stroke-width="1.2"/><line x1="0" y1="14" x2="24" y2="14" stroke="#1B5162" stroke-width="1.2"/></g><text x="54" y="274.0" font-size="14" font-weight="700" fill="#0b2026" font-family="monospace">resources/*.yml</text><text x="54" y="294.0" font-size="14" fill="#5E7077">the pipeline</text><rect x="306" y="10" width="250" height="32" rx="16" fill="#4299E0"/><text x="431.0" y="31" text-anchor="middle" font-size="14" font-weight="700" fill="#FFFFFF" letter-spacing="2">DEV (per person)</text><rect x="306" y="123.0" width="250" height="64" rx="8" fill="#4299E0" fill-opacity="0.10" stroke="#4299E0" stroke-width="1.5"/><g transform="translate(316,141.0)"><rect x="0" y="2" width="24" height="18" rx="2" fill="none" stroke="#4299E0" stroke-width="1.5"/><rect x="0" y="2" width="24" height="6" rx="2" fill="#4299E0"/><line x1="8" y1="8" x2="8" y2="20" stroke="#4299E0" stroke-width="1.2"/><line x1="16" y1="8" x2="16" y2="20" stroke="#4299E0" stroke-width="1.2"/><line x1="0" y1="14" x2="24" y2="14" stroke="#4299E0" stroke-width="1.2"/><circle cx="22" cy="18" r="7" fill="#FFFFFF"/><path d="M23 13 L18.5 19 L21.5 19 L20 23.5 L26 16.5 L23 16.5 Z" fill="#4299E0" stroke="#FFFFFF" stroke-width="0.5"/></g><text x="350" y="151.0" font-size="14" font-weight="700" fill="#0b2026" font-family="monospace">‹you› (personal schema)</text><text x="350" y="171.0" font-size="14" fill="#5E7077">mode: development</text><rect x="306" y="205.0" width="250" height="64" rx="8" fill="#4299E0" fill-opacity="0.10" stroke="#4299E0" stroke-width="1.5"/><g transform="translate(316,223.0)"><rect x="0" y="2" width="24" height="18" rx="2" fill="none" stroke="#4299E0" stroke-width="1.5"/><rect x="0" y="2" width="24" height="6" rx="2" fill="#4299E0"/><line x1="8" y1="8" x2="8" y2="20" stroke="#4299E0" stroke-width="1.2"/><line x1="16" y1="8" x2="16" y2="20" stroke="#4299E0" stroke-width="1.2"/><line x1="0" y1="14" x2="24" y2="14" stroke="#4299E0" stroke-width="1.2"/><circle cx="22" cy="18" r="8" fill="#FFFFFF"/><circle cx="19" cy="18" r="2.6" fill="none" stroke="#0b2026" stroke-width="1.3"/><circle cx="25.5" cy="18" r="2.6" fill="none" stroke="#0b2026" stroke-width="1.3"/><line x1="21.6" y1="17.6" x2="22.9" y2="17.6" stroke="#0b2026" stroke-width="1.3"/></g><text x="350" y="233.0" font-size="14" font-weight="700" fill="#0b2026" font-family="monospace">[dev you] iops_quality</text><text x="350" y="253.0" font-size="14" fill="#5E7077">paused, isolated</text><rect x="602" y="10" width="250" height="32" rx="16" fill="#00A972"/><text x="727.0" y="31" text-anchor="middle" font-size="14" font-weight="700" fill="#FFFFFF" letter-spacing="2">QA (per person today)</text><rect x="602" y="123.0" width="250" height="64" rx="8" fill="#00A972" fill-opacity="0.10" stroke="#00A972" stroke-width="1.5"/><g transform="translate(612,141.0)"><rect x="0" y="2" width="24" height="18" rx="2" fill="none" stroke="#00A972" stroke-width="1.5"/><rect x="0" y="2" width="24" height="6" rx="2" fill="#00A972"/><line x1="8" y1="8" x2="8" y2="20" stroke="#00A972" stroke-width="1.2"/><line x1="16" y1="8" x2="16" y2="20" stroke="#00A972" stroke-width="1.2"/><line x1="0" y1="14" x2="24" y2="14" stroke="#00A972" stroke-width="1.2"/><circle cx="22" cy="18" r="7" fill="#FFFFFF"/><path d="M23 13 L18.5 19 L21.5 19 L20 23.5 L26 16.5 L23 16.5 Z" fill="#00A972" stroke="#FFFFFF" stroke-width="0.5"/></g><text x="646" y="151.0" font-size="14" font-weight="700" fill="#0b2026" font-family="monospace">‹you›_qa</text><text x="646" y="171.0" font-size="14" fill="#5E7077">mode: production</text><rect x="602" y="205.0" width="250" height="64" rx="8" fill="#00A972" fill-opacity="0.10" stroke="#00A972" stroke-width="1.5"/><g transform="translate(612,223.0)"><rect x="0" y="2" width="24" height="18" rx="2" fill="none" stroke="#00A972" stroke-width="1.5"/><rect x="0" y="2" width="24" height="6" rx="2" fill="#00A972"/><line x1="8" y1="8" x2="8" y2="20" stroke="#00A972" stroke-width="1.2"/><line x1="16" y1="8" x2="16" y2="20" stroke="#00A972" stroke-width="1.2"/><line x1="0" y1="14" x2="24" y2="14" stroke="#00A972" stroke-width="1.2"/><circle cx="22" cy="18" r="8" fill="#FFFFFF"/><circle cx="19" cy="18" r="2.6" fill="none" stroke="#0b2026" stroke-width="1.3"/><circle cx="25.5" cy="18" r="2.6" fill="none" stroke="#0b2026" stroke-width="1.3"/><line x1="21.6" y1="17.6" x2="22.9" y2="17.6" stroke="#0b2026" stroke-width="1.3"/></g><text x="646" y="233.0" font-size="14" font-weight="700" fill="#0b2026" font-family="monospace">+ qa_gate.sql</text><text x="646" y="253.0" font-size="14" fill="#5E7077">FAIL UPDATE</text><rect x="898" y="10" width="250" height="32" rx="16" fill="#98102A"/><text x="1023.0" y="31" text-anchor="middle" font-size="14" font-weight="700" fill="#FFFFFF" letter-spacing="2">PROD (gated)</text><rect x="898" y="123.0" width="250" height="64" rx="8" fill="#98102A" fill-opacity="0.10" stroke="#98102A" stroke-width="1.5"/><g transform="translate(908,141.0)"><rect x="0" y="2" width="24" height="18" rx="2" fill="none" stroke="#98102A" stroke-width="1.5"/><rect x="0" y="2" width="24" height="6" rx="2" fill="#98102A"/><line x1="8" y1="8" x2="8" y2="20" stroke="#98102A" stroke-width="1.2"/><line x1="16" y1="8" x2="16" y2="20" stroke="#98102A" stroke-width="1.2"/><line x1="0" y1="14" x2="24" y2="14" stroke="#98102A" stroke-width="1.2"/></g><text x="942" y="151.0" font-size="14" font-weight="700" fill="#0b2026" font-family="monospace">service principal</text><text x="942" y="171.0" font-size="14" fill="#5E7077">CI only</text><rect x="898" y="205.0" width="250" height="64" rx="8" fill="#98102A" fill-opacity="0.10" stroke="#98102A" stroke-width="1.5"/><g transform="translate(908,223.0)"><rect x="0" y="2" width="24" height="18" rx="2" fill="none" stroke="#98102A" stroke-width="1.5"/><rect x="0" y="2" width="24" height="6" rx="2" fill="#98102A"/><line x1="8" y1="8" x2="8" y2="20" stroke="#98102A" stroke-width="1.2"/><line x1="16" y1="8" x2="16" y2="20" stroke="#98102A" stroke-width="1.2"/><line x1="0" y1="14" x2="24" y2="14" stroke="#98102A" stroke-width="1.2"/></g><text x="942" y="233.0" font-size="14" font-weight="700" fill="#0b2026" font-family="monospace">approvals</text><text x="942" y="253.0" font-size="14" fill="#5E7077">change record</text></svg><div style="margin-top: 18px; padding: 16px 20px; background: #F9F7F4; border: 2px solid #1B5162; border-radius: 8px; font-size: 14pt; line-height: 1.55;"><strong>Dev is personal</strong> (names prefixed, schedules paused), <strong>QA</strong> runs the reviewed, merged code, <strong>prod</strong> is deployed only by CI as a service principal. Today we stop at QA.</div></div>

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
# MAGIC <div style="font-size:20pt;font-weight:700;margin-bottom:14px;">What changes per target (databricks.yml)</div><div class="ds-row"><div class="ds-card blue"><div class="ds-card-title">dev</div><ul><li><code>mode: development</code></li><li>schema <code>‹you›</code> (personal)</li><li>names prefixed <code>[dev you]</code>, runs as you</li></ul></div><div class="ds-card green"><div class="ds-card-title">qa</div><ul><li><code>mode: production</code></li><li>schema <code>‹you›_qa</code></li><li>adds the QA gate file <code>qa/qa_gate.sql</code></li></ul></div><div class="ds-card amber"><div class="ds-card-title">prod (not today)</div><ul><li><code>mode: production</code></li><li>deployed only by CI</li><li>runs as a service principal</li></ul></div></div>
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
# MAGIC <div style="font-size:20pt;font-weight:700;margin-bottom:14px;">Variables make it portable</div><div class="ds-row"><div class="ds-card blue"><div class="ds-card-title">Built-in substitutions</div><ul><li><code>${bundle.target}</code> &rarr; dev or qa</li><li><code>${workspace.current_user.short_name}</code></li><li><code>${workspace.current_user.userName}</code></li></ul></div><div class="ds-card green"><div class="ds-card-title">Custom variables</div><ul><li><code>catalog</code> and <code>schema</code> in your <code>databricks.yml</code></li><li>Override per target or with <code>--var catalog=...</code></li></ul></div><div class="ds-card amber"><div class="ds-card-title">Lookup variables</div><ul><li><code>warehouse</code> is found by name</li><li>Same YAML works in any workspace</li></ul></div></div>
# MAGIC </div>
# MAGIC
# MAGIC ##### EXPAND FOR ADDITIONAL NOTES
# MAGIC
# MAGIC <details>
# MAGIC
# MAGIC This is why the same bundle runs in any workspace: the workspace is wherever you deploy it, the catalog comes from one variable.
# MAGIC ```yaml
# MAGIC # databricks.yml
# MAGIC variables:
# MAGIC   catalog:
# MAGIC     default: iops_sandbox
# MAGIC   warehouse:
# MAGIC     lookup:
# MAGIC       warehouse: Shared SQL Warehouse
# MAGIC ```
# MAGIC
# MAGIC </details>

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
# MAGIC <div class="flow-grid" style="grid-template-columns:1fr auto 1fr auto 1fr auto 1fr;"><div class="flow-step" style="--accent:#4299E0;"><div class="flow-num">1</div><div class="flow-label"><strong>Validate</strong><br>config is valid</div></div><div class="flow-arrow">&rarr;</div><div class="flow-step" style="--accent:#00A972;"><div class="flow-num">2</div><div class="flow-label"><strong>Deploy</strong><br>create or update</div></div><div class="flow-arrow">&rarr;</div><div class="flow-step" style="--accent:#FFAB00;"><div class="flow-num">3</div><div class="flow-label"><strong>Run</strong><br>pipeline update</div></div><div class="flow-arrow">&rarr;</div><div class="flow-step" style="--accent:#FF5F46;"><div class="flow-num">4</div><div class="flow-label"><strong>Bundle resources</strong><br>what is deployed</div></div></div>
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
# MAGIC <div class="ds-callout info"><div>In the workspace these are the buttons of the bundle's <strong>Deployments</strong> panel. From a laptop or CI the same steps are <code>databricks bundle validate | deploy | run | summary</code>.</div></div>
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
# MAGIC <div class="ds-callout danger row"><div class="ds-callout-icon">!</div><div><div class="ds-eyebrow">The QA gate</div><div class="ds-callout-title">qa/qa_gate.sql is added only in the qa target.</div><ul><li><code>zero_data_loss</code>: bronze = clean + quarantine for every feed.</li><li><code>unique_case_grain</code> / <code>unique_change_grain</code>: Gold keeps its grain.</li><li>Any failure is <code>FAIL UPDATE</code>: the QA update stops and nothing downstream refreshes.</li></ul></div></div>
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
# MAGIC <div style="font-size:20pt;font-weight:700;margin-bottom:14px;">Operationalize, all in YAML</div><div class="ds-row"><div class="ds-card blue"><div class="ds-card-title">Schedule</div><ul><li>Job <code>trigger</code> or <code>schedule</code> in the bundle</li><li>Paused automatically in dev mode</li></ul></div><div class="ds-card amber"><div class="ds-card-title">Notify</div><ul><li><code>email_notifications.on_failure</code></li><li>Or webhooks to Teams / ServiceNow</li></ul></div><div class="ds-card green"><div class="ds-card-title">Monitor</div><ul><li>Event log in UC (Lab 11)</li><li>Alert on quarantine growth</li></ul></div></div>
# MAGIC </div>
# MAGIC
# MAGIC ##### EXPAND FOR ADDITIONAL NOTES
# MAGIC
# MAGIC <details>
# MAGIC
# MAGIC ```yaml
# MAGIC # a job in resources/ (production additions)
# MAGIC       schedule:
# MAGIC         quartz_cron_expression: "0 0 6 * * ?"   # 06:00 daily
# MAGIC         timezone_id: America/New_York
# MAGIC       email_notifications:
# MAGIC         on_failure: [iops-data-oncall@example.com]
# MAGIC ```
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
# MAGIC <div class="ds-row"><div class="ds-card red"><div class="ds-card-title">Production gates</div><ul><li>Deploy only from CI (Jenkins / Bitbucket Pipelines)</li><li><code>run_as</code> a service principal</li><li>Change record + approval before deploy</li></ul></div><div class="ds-card blue"><div class="ds-card-title">In the repo</div><ul><li>Feature branch &rarr; PR &rarr; main</li><li><code>bundle validate</code> in every PR</li><li>Tags and descriptions as code (Lab 13)</li></ul></div><div class="ds-card coral"><div class="ds-card-title">Never</div><ul><li>Click-deploy to prod</li><li>Personal tokens in pipelines</li><li>Edit prod tables by hand</li></ul></div></div>
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
# MAGIC var QZ=[{"q": "Why do two participants not overwrite each other in dev?", "opts": ["They use different catalogs", "Development mode prefixes names per user", "Luck"], "ans": 1, "fb": "mode: development prefixes resources ([dev you]), uses your personal schema and pauses schedules."}, {"q": "Which file decides that QA fails on data loss?", "opts": ["dq_checks.sql", "qa_gate.sql", "variables.yml"], "ans": 1, "fb": "qa_gate.sql uses FAIL UPDATE and is attached only by the qa target."}];
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
# MAGIC ## Git workflow: GitHub Actions deploys your bundle
# MAGIC In production nobody clicks Deploy. Git changes trigger the same bundle commands you used, run by a service principal.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div style="max-width: 1100px; margin: 0 auto; font-family: sans-serif; color: #0b2026;"><div style="text-align: center; margin-bottom: 12px;"><div style="font-size: 22pt; font-weight: 700;">How GitHub Actions deploys your bundle</div><div style="font-size: 14pt; color: #618794; margin-top: 4px;">Top row: every pull request &middot; bottom row: every merge &middot; Actions signs in as a service principal (OIDC)</div></div><svg width="100%" viewBox="0 0 1158 254" role="img" style="font-family: sans-serif;"><defs><marker id="med-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="#5E7077" stroke-width="1.5"/></marker></defs><path d="M854 196.0 L894 196.0" fill="none" stroke="#5E7077" stroke-width="1.6" marker-end="url(#med-arrow)"/><path d="M558 196.0 L598 196.0" fill="none" stroke="#5E7077" stroke-width="1.6" marker-end="url(#med-arrow)"/><path d="M262 196.0 L302 196.0" fill="none" stroke="#5E7077" stroke-width="1.6" marker-end="url(#med-arrow)"/><path d="M854 114.0 L894 114.0" fill="none" stroke="#5E7077" stroke-width="1.6" marker-end="url(#med-arrow)"/><path d="M558 114.0 L598 114.0" fill="none" stroke="#5E7077" stroke-width="1.6" marker-end="url(#med-arrow)"/><path d="M262 114.0 L302 114.0" fill="none" stroke="#5E7077" stroke-width="1.6" marker-end="url(#med-arrow)"/><rect x="10" y="10" width="250" height="32" rx="16" fill="#1B5162"/><text x="135.0" y="31" text-anchor="middle" font-size="14" font-weight="700" fill="#FFFFFF" letter-spacing="2">YOU</text><rect x="10" y="82.0" width="250" height="64" rx="8" fill="#1B5162" fill-opacity="0.10" stroke="#1B5162" stroke-width="1.5"/><g transform="translate(20,100.0)"><rect x="0" y="2" width="24" height="18" rx="2" fill="none" stroke="#1B5162" stroke-width="1.5"/><rect x="0" y="2" width="24" height="6" rx="2" fill="#1B5162"/><line x1="8" y1="8" x2="8" y2="20" stroke="#1B5162" stroke-width="1.2"/><line x1="16" y1="8" x2="16" y2="20" stroke="#1B5162" stroke-width="1.2"/><line x1="0" y1="14" x2="24" y2="14" stroke="#1B5162" stroke-width="1.2"/></g><text x="54" y="110.0" font-size="14" font-weight="700" fill="#0b2026" font-family="monospace">Git folder: branch</text><text x="54" y="130.0" font-size="14" fill="#5E7077">edit the bundle</text><rect x="10" y="164.0" width="250" height="64" rx="8" fill="#1B5162" fill-opacity="0.10" stroke="#1B5162" stroke-width="1.5"/><g transform="translate(20,182.0)"><rect x="0" y="2" width="24" height="18" rx="2" fill="none" stroke="#1B5162" stroke-width="1.5"/><rect x="0" y="2" width="24" height="6" rx="2" fill="#1B5162"/><line x1="8" y1="8" x2="8" y2="20" stroke="#1B5162" stroke-width="1.2"/><line x1="16" y1="8" x2="16" y2="20" stroke="#1B5162" stroke-width="1.2"/><line x1="0" y1="14" x2="24" y2="14" stroke="#1B5162" stroke-width="1.2"/></g><text x="54" y="192.0" font-size="14" font-weight="700" fill="#0b2026" font-family="monospace">Review + merge</text><text x="54" y="212.0" font-size="14" fill="#5E7077">approve the change</text><rect x="306" y="10" width="250" height="32" rx="16" fill="#4299E0"/><text x="431.0" y="31" text-anchor="middle" font-size="14" font-weight="700" fill="#FFFFFF" letter-spacing="2">GITHUB</text><rect x="306" y="82.0" width="250" height="64" rx="8" fill="#4299E0" fill-opacity="0.10" stroke="#4299E0" stroke-width="1.5"/><g transform="translate(316,100.0)"><rect x="0" y="2" width="24" height="18" rx="2" fill="none" stroke="#4299E0" stroke-width="1.5"/><rect x="0" y="2" width="24" height="6" rx="2" fill="#4299E0"/><line x1="8" y1="8" x2="8" y2="20" stroke="#4299E0" stroke-width="1.2"/><line x1="16" y1="8" x2="16" y2="20" stroke="#4299E0" stroke-width="1.2"/><line x1="0" y1="14" x2="24" y2="14" stroke="#4299E0" stroke-width="1.2"/></g><text x="350" y="110.0" font-size="14" font-weight="700" fill="#0b2026" font-family="monospace">Pull request</text><text x="350" y="130.0" font-size="14" fill="#5E7077">to main</text><rect x="306" y="164.0" width="250" height="64" rx="8" fill="#4299E0" fill-opacity="0.10" stroke="#4299E0" stroke-width="1.5"/><g transform="translate(316,182.0)"><rect x="0" y="2" width="24" height="18" rx="2" fill="none" stroke="#4299E0" stroke-width="1.5"/><rect x="0" y="2" width="24" height="6" rx="2" fill="#4299E0"/><line x1="8" y1="8" x2="8" y2="20" stroke="#4299E0" stroke-width="1.2"/><line x1="16" y1="8" x2="16" y2="20" stroke="#4299E0" stroke-width="1.2"/><line x1="0" y1="14" x2="24" y2="14" stroke="#4299E0" stroke-width="1.2"/></g><text x="350" y="192.0" font-size="14" font-weight="700" fill="#0b2026" font-family="monospace">main branch</text><text x="350" y="212.0" font-size="14" fill="#5E7077">the reviewed code</text><rect x="602" y="10" width="250" height="32" rx="16" fill="#FFAB00"/><text x="727.0" y="31" text-anchor="middle" font-size="14" font-weight="700" fill="#0b2026" letter-spacing="2">GITHUB ACTIONS</text><rect x="602" y="82.0" width="250" height="64" rx="8" fill="#FFAB00" fill-opacity="0.10" stroke="#FFAB00" stroke-width="1.5"/><g transform="translate(612,100.0)"><rect x="0" y="2" width="24" height="18" rx="2" fill="none" stroke="#FFAB00" stroke-width="1.5"/><rect x="0" y="2" width="24" height="6" rx="2" fill="#FFAB00"/><line x1="8" y1="8" x2="8" y2="20" stroke="#FFAB00" stroke-width="1.2"/><line x1="16" y1="8" x2="16" y2="20" stroke="#FFAB00" stroke-width="1.2"/><line x1="0" y1="14" x2="24" y2="14" stroke="#FFAB00" stroke-width="1.2"/><circle cx="22" cy="18" r="7" fill="#FFFFFF"/><path d="M23 13 L18.5 19 L21.5 19 L20 23.5 L26 16.5 L23 16.5 Z" fill="#FFAB00" stroke="#FFFFFF" stroke-width="0.5"/></g><text x="646" y="110.0" font-size="14" font-weight="700" fill="#0b2026" font-family="monospace">dev-deployment.yml</text><text x="646" y="130.0" font-size="14" fill="#5E7077">deploy + run, target dev</text><rect x="602" y="164.0" width="250" height="64" rx="8" fill="#FFAB00" fill-opacity="0.10" stroke="#FFAB00" stroke-width="1.5"/><g transform="translate(612,182.0)"><rect x="0" y="2" width="24" height="18" rx="2" fill="none" stroke="#FFAB00" stroke-width="1.5"/><rect x="0" y="2" width="24" height="6" rx="2" fill="#FFAB00"/><line x1="8" y1="8" x2="8" y2="20" stroke="#FFAB00" stroke-width="1.2"/><line x1="16" y1="8" x2="16" y2="20" stroke="#FFAB00" stroke-width="1.2"/><line x1="0" y1="14" x2="24" y2="14" stroke="#FFAB00" stroke-width="1.2"/><circle cx="22" cy="18" r="7" fill="#FFFFFF"/><path d="M23 13 L18.5 19 L21.5 19 L20 23.5 L26 16.5 L23 16.5 Z" fill="#FFAB00" stroke="#FFFFFF" stroke-width="0.5"/></g><text x="646" y="192.0" font-size="14" font-weight="700" fill="#0b2026" font-family="monospace">qa-deployment.yml</text><text x="646" y="212.0" font-size="14" fill="#5E7077">deploy + run, target qa</text><rect x="898" y="10" width="250" height="32" rx="16" fill="#00A972"/><text x="1023.0" y="31" text-anchor="middle" font-size="14" font-weight="700" fill="#FFFFFF" letter-spacing="2">DATABRICKS</text><rect x="898" y="82.0" width="250" height="64" rx="8" fill="#00A972" fill-opacity="0.10" stroke="#00A972" stroke-width="1.5"/><g transform="translate(908,100.0)"><rect x="0" y="2" width="24" height="18" rx="2" fill="none" stroke="#00A972" stroke-width="1.5"/><rect x="0" y="2" width="24" height="6" rx="2" fill="#00A972"/><line x1="8" y1="8" x2="8" y2="20" stroke="#00A972" stroke-width="1.2"/><line x1="16" y1="8" x2="16" y2="20" stroke="#00A972" stroke-width="1.2"/><line x1="0" y1="14" x2="24" y2="14" stroke="#00A972" stroke-width="1.2"/><circle cx="22" cy="18" r="8" fill="#FFFFFF"/><circle cx="19" cy="18" r="2.6" fill="none" stroke="#0b2026" stroke-width="1.3"/><circle cx="25.5" cy="18" r="2.6" fill="none" stroke="#0b2026" stroke-width="1.3"/><line x1="21.6" y1="17.6" x2="22.9" y2="17.6" stroke="#0b2026" stroke-width="1.3"/></g><text x="942" y="110.0" font-size="14" font-weight="700" fill="#0b2026" font-family="monospace">[dev] pipeline</text><text x="942" y="130.0" font-size="14" fill="#5E7077">dev schema</text><rect x="898" y="164.0" width="250" height="64" rx="8" fill="#00A972" fill-opacity="0.10" stroke="#00A972" stroke-width="1.5"/><g transform="translate(908,182.0)"><rect x="0" y="2" width="24" height="18" rx="2" fill="none" stroke="#00A972" stroke-width="1.5"/><rect x="0" y="2" width="24" height="6" rx="2" fill="#00A972"/><line x1="8" y1="8" x2="8" y2="20" stroke="#00A972" stroke-width="1.2"/><line x1="16" y1="8" x2="16" y2="20" stroke="#00A972" stroke-width="1.2"/><line x1="0" y1="14" x2="24" y2="14" stroke="#00A972" stroke-width="1.2"/><circle cx="22" cy="18" r="8" fill="#FFFFFF"/><circle cx="19" cy="18" r="2.6" fill="none" stroke="#0b2026" stroke-width="1.3"/><circle cx="25.5" cy="18" r="2.6" fill="none" stroke="#0b2026" stroke-width="1.3"/><line x1="21.6" y1="17.6" x2="22.9" y2="17.6" stroke="#0b2026" stroke-width="1.3"/></g><text x="942" y="192.0" font-size="14" font-weight="700" fill="#0b2026" font-family="monospace">QA pipeline</text><text x="942" y="212.0" font-size="14" fill="#5E7077">qa schema + QA gate</text></svg><div style="margin-top: 18px; padding: 16px 20px; background: #F9F7F4; border: 2px solid #1B5162; border-radius: 8px; font-size: 14pt; line-height: 1.55;"><strong>Same commands, new driver.</strong> The workflows run <code>databricks bundle deploy</code> and <code>databricks bundle run</code>, exactly what the Deployments panel does for you. Nobody deploys QA or production by hand.</div></div>
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
# MAGIC <div class="flow-grid" style="grid-template-columns:1fr auto 1fr auto 1fr auto 1fr auto 1fr;"><div class="flow-step" style="--accent:#4299E0;"><div class="flow-num">1</div><div class="flow-label">Branch<br>in your Git folder</div></div><div class="flow-arrow">&rarr;</div><div class="flow-step" style="--accent:#00A972;"><div class="flow-num">2</div><div class="flow-label">Change + deploy<br>to <code>dev</code> (you)</div></div><div class="flow-arrow">&rarr;</div><div class="flow-step" style="--accent:#FFAB00;"><div class="flow-num">3</div><div class="flow-label">Pull request<br>CI deploys <code>dev</code> + runs</div></div><div class="flow-arrow">&rarr;</div><div class="flow-step" style="--accent:#FF5F46;"><div class="flow-num">4</div><div class="flow-label">Review + merge<br>to <code>main</code></div></div><div class="flow-arrow">&rarr;</div><div class="flow-step" style="--accent:#98102A;"><div class="flow-num">5</div><div class="flow-label">CD deploys <code>qa</code><br>+ runs, QA gate</div></div></div>
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
# MAGIC <div class="ds-callout info"><div class="ds-eyebrow">The only new idea</div><div>The commands do not change: <code>databricks bundle deploy</code> and <code>databricks bundle run</code>. What changes is <strong>who</strong> runs them (a service principal, not you) and <strong>when</strong> (on a pull request, on a merge).</div></div>
# MAGIC </div>
# MAGIC
# MAGIC ##### EXPAND FOR ADDITIONAL NOTES
# MAGIC
# MAGIC <details>
# MAGIC
# MAGIC - This is the Databricks-recommended path: develop in your own Git folder and dev target, review through a pull request, deploy shared environments only from CI as a service principal.
# MAGIC - The facilitator demo repo runs exactly the two files below.
# MAGIC - Start simple: deploy and run. Add unit tests, data checks and approvals later, one at a time.
# MAGIC
# MAGIC </details>

# COMMAND ----------

# MAGIC %md
# MAGIC **`.github/workflows/dev-deployment.yml`**: a pull request to `main` deploys the bundle to `dev` and runs the pipeline.
# MAGIC ```yaml
# MAGIC name: Dev deployment
# MAGIC on:
# MAGIC   pull_request:
# MAGIC     branches: [main]
# MAGIC permissions:
# MAGIC   id-token: write          # lets GitHub sign in to Databricks (no stored password)
# MAGIC   contents: read
# MAGIC jobs:
# MAGIC   deploy:
# MAGIC     runs-on: ubuntu-latest
# MAGIC     environment: dev
# MAGIC     env:
# MAGIC       DATABRICKS_AUTH_TYPE: github-oidc
# MAGIC       DATABRICKS_HOST: ${{ vars.DATABRICKS_HOST }}
# MAGIC       DATABRICKS_CLIENT_ID: ${{ secrets.DATABRICKS_CLIENT_ID }}   # the service principal
# MAGIC       DATABRICKS_BUNDLE_TARGET: dev
# MAGIC     steps:
# MAGIC       - uses: actions/checkout@v4
# MAGIC       - uses: databricks/setup-cli@main             # installs the Databricks CLI
# MAGIC       - run: databricks bundle deploy               # validates, then deploys
# MAGIC       - run: databricks bundle run iops_quality_etl # runs the pipeline
# MAGIC ```
# MAGIC
# MAGIC **`.github/workflows/qa-deployment.yml`**: the same steps on a merge to `main`, with `environment: qa` and `DATABRICKS_BUNDLE_TARGET: qa`.
# MAGIC ```yaml
# MAGIC name: QA deployment
# MAGIC on:
# MAGIC   push:
# MAGIC     branches: [main]
# MAGIC # ... same permissions, env (target qa) and steps as above
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
# MAGIC <div style="font-size:20pt;font-weight:700;margin-bottom:14px;">Set up once, then it is just Git</div><div class="ds-row"><div class="ds-card blue"><div class="ds-card-label">In Databricks (an admin, once)</div><div class="ds-card-title">A service principal</div><ul><li>Owns and runs the QA pipeline</li><li>A <strong>federation policy</strong> trusts this repo + environment</li><li>Grants on the catalog and schemas</li></ul></div><div class="ds-card green"><div class="ds-card-label">In GitHub (once)</div><div class="ds-card-title">Environments and a variable</div><ul><li>Environments <code>dev</code> and <code>qa</code></li><li>Variable <code>DATABRICKS_HOST</code></li><li>Secret <code>DATABRICKS_CLIENT_ID</code></li></ul></div><div class="ds-card amber"><div class="ds-card-label">Then, every change</div><div class="ds-card-title">Just Git</div><ul><li>Branch, commit, pull request</li><li>CI deploys and runs dev</li><li>Merge: CD deploys and runs QA</li></ul></div></div>
# MAGIC </div>
# MAGIC
# MAGIC ##### EXPAND FOR ADDITIONAL NOTES
# MAGIC
# MAGIC <details>
# MAGIC
# MAGIC - Why a federation policy: GitHub proves who it is with a short-lived token; Databricks trusts that token for one repo and environment. No secret to leak or rotate.
# MAGIC - Docs: GitHub Actions with Databricks (Public Preview), and Enable workload identity federation for GitHub Actions.
# MAGIC
# MAGIC </details>

# COMMAND ----------

# MAGIC %md
# MAGIC ## Conclusion
# MAGIC
# MAGIC In this lecture, you:
# MAGIC
# MAGIC 1. Described a project as a bundle: code and configuration in one repo
# MAGIC 2. Read what changes per target in `databricks.yml`
# MAGIC 3. Used variables to make the same project run in any workspace
# MAGIC 4. Saw how the QA gate stops a bad promotion
# MAGIC 5. Saw GitHub Actions deploy the same bundle on a pull request and on a merge
# MAGIC 6. Listed the controls a production deployment needs
# MAGIC
# MAGIC ### Next Steps
# MAGIC
# MAGIC In **09 Lab - Promote dev to QA**, you promote your own pipeline through the QA gate.
