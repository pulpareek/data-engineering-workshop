# Databricks notebook source
# MAGIC %md
# MAGIC ### Classroom setup (every notebook runs `%run ./Includes/Classroom-Setup`)
# MAGIC Resolves your schema and paths, and provides three helpers:
# MAGIC - `land_batch(n)` copies source batch *n* into your landing volume (simulates files arriving)
# MAGIC - `checkpoint(run, layer)` compares your tables with the expected numbers
# MAGIC - `show_paths()` prints everything you need to paste into the pipeline settings

# COMMAND ----------

import json
import os
import re



def _bundle_root():
    """The workshop root: the folder holding data/staging (the facilitator bundle, or the participant's Git folder)."""
    up = os.getcwd()
    for _ in range(5):
        if os.path.isdir(os.path.join(up, "data", "staging")):
            return up
        up = os.path.dirname(up)
    return ""


def _bundle_default_catalog():
    """Catalog default from resources/variables.yml, so the workshop is configured in one place."""
    root = _bundle_root()
    if root and os.path.isfile(os.path.join(root, "resources", "variables.yml")):
        m = re.search(r"^  catalog:\n(?:    .*\n)*?    default:\s*([A-Za-z0-9_]+)", open(os.path.join(root, "resources", "variables.yml")).read(), re.M)
        if m:
            return m.group(1)
    return ""


ROOT = _bundle_root()  # repo files (governance/, data/, pipeline_files/) for notebooks that read them
# Git-folder mode: participants create their own bundle in the Git folder (no facilitator bundle files at ROOT).
GIT_FOLDER_MODE = bool(ROOT) and not os.path.isfile(os.path.join(ROOT, "resources", "variables.yml"))


# Workshop-wide defaults: one catalog, and one shared landing folder that every participant's pipeline reads.
# Each is used only if it exists in this workspace; otherwise the per-person defaults below apply.
WORKSHOP_CATALOG = "iops_sandbox"                                            # catalog for every participant schema
WORKSHOP_LANDING = "/Volumes/iops_sandbox/iops_databricks_workshop/landing"  # shared files: iops_sandbox.iops_databricks_workshop.landing


def _exists(path):
    try:
        dbutils.fs.ls(path)  # noqa: F821
        return True
    except Exception:
        return False


def _catalog_exists(name):
    return spark.sql(f"SHOW CATALOGS LIKE '{name}'").count() > 0  # noqa: F821


# Every value can be overridden with a widget; blank = the default.
if not GIT_FOLDER_MODE:  # facilitator bundle only; participants are identified by their user name
    dbutils.widgets.text("team", "", "Team name (same as --var team)")  # noqa: F821
dbutils.widgets.text("catalog", WORKSHOP_CATALOG if GIT_FOLDER_MODE else "", "Catalog")  # noqa: F821
dbutils.widgets.text("schema", "", "Schema (blank = your personal schema)")  # noqa: F821
dbutils.widgets.text("landing", WORKSHOP_LANDING if GIT_FOLDER_MODE else "", "Landing folder the pipeline reads")  # noqa: F821
dbutils.widgets.text("source_files", "", "Source batches (facilitator; blank = default)")  # noqa: F821
dbutils.widgets.dropdown("target", "dev", ["dev", "qa", "ref"], "Bundle target")  # noqa: F821

TEAM = "" if GIT_FOLDER_MODE else dbutils.widgets.get("team").strip()  # noqa: F821
CATALOG = (dbutils.widgets.get("catalog").strip()  # noqa: F821
           or (WORKSHOP_CATALOG if _catalog_exists(WORKSHOP_CATALOG) else _bundle_default_catalog()))
if not CATALOG:
    raise ValueError("Set the catalog widget (or the catalog default in resources/variables.yml).")
TARGET = dbutils.widgets.get("target")  # noqa: F821
ME = spark.sql("SELECT current_user()").first()[0]  # noqa: F821
SHORT = re.sub(r"[^a-z0-9]+", "_", ME.split("@")[0].lower())
TEAM = TEAM or SHORT  # the bundle default is your short user name

# Same naming rule as the bundle: the schema variable (iops_ws_<team>, or iops_ws_<team>_qa in qa),
# and development mode (dev, ref) prefixes dev_<user>_ to keep everyone isolated.
if GIT_FOLDER_MODE:  # your own bundle: personal schema = your short user name (ETL pipeline template), _qa for QA
    SCHEMA = dbutils.widgets.get("schema").strip() or (f"{SHORT}_qa" if TARGET == "qa" else SHORT)  # noqa: F821
else:
    BASE_SCHEMA = dbutils.widgets.get("schema").strip() or (f"iops_ws_{TEAM}_qa" if TARGET == "qa" else f"iops_ws_{TEAM}")  # noqa: F821
    SCHEMA = BASE_SCHEMA if TARGET == "qa" else f"dev_{SHORT}_{BASE_SCHEMA}"
FQ = f"{CATALOG}.{SCHEMA}"
if GIT_FOLDER_MODE:
    spark.sql(f"CREATE SCHEMA IF NOT EXISTS {FQ}")  # noqa: F821  (your pipeline publishes here)
# Where the pipeline reads files (pipeline parameter landing_root). Shared = the facilitator lands batches for everyone.
LANDING = (dbutils.widgets.get("landing").strip()  # noqa: F821
           or (WORKSHOP_LANDING if _exists(WORKSHOP_LANDING) else f"/Volumes/{CATALOG}/{SCHEMA}/landing")).rstrip("/")
SHARED_LANDING = not LANDING.startswith(f"/Volumes/{CATALOG}/{SCHEMA}/")
if GIT_FOLDER_MODE and not SHARED_LANDING:
    spark.sql(f"CREATE VOLUME IF NOT EXISTS {FQ}.landing")  # noqa: F821
# SQL filters that find your own pipeline / job by name (system tables, Lab 11).
MY_PIPELINES = (f"(name LIKE '%{SHORT}%' AND name LIKE '%iops_quality%')" if GIT_FOLDER_MODE
                else f"(name LIKE '%iops_quality_{TEAM}')")
MY_JOBS = "(false)" if GIT_FOLDER_MODE else f"(name LIKE '%iops_workshop_refresh_{TEAM}')"
STAGING = (dbutils.widgets.get("source_files").strip() or f"/Volumes/{CATALOG}/iops_ws_shared/staging").rstrip("/")  # noqa: F821
FEEDS = ["deviation_event_feed", "corrective_action_feed", "change_control_feed", "inspection_result_feed",
         "batch_record_feed"]


def _repo_data_dir():
    """Fallback copy of the synthetic files that ships inside the bundle (if the shared volume is absent)."""
    here = os.getcwd()
    for up in (here, os.path.dirname(here), os.path.dirname(os.path.dirname(here)),
               os.path.dirname(os.path.dirname(os.path.dirname(here)))):
        cand = os.path.join(up, "data", "staging")
        if os.path.isdir(cand):
            return cand
    return None


def _source_root():
    try:
        dbutils.fs.ls(STAGING)  # noqa: F821
        return STAGING
    except Exception:  # shared volume not staged yet -> use the copy inside the bundle
        local = _repo_data_dir()
        if local is None:
            raise RuntimeError(f"No source files: stage them in {STAGING} or deploy the bundle (data/staging).")
        return "file:" + local


def land_batch(n: int, force: bool = False):
    """Make batch n (1, 2 or 3) arrive in the landing folder. Safe to re-run.
    Shared landing: the facilitator runs land_batch(n, force=True) once for everyone; for participants this
    only shows which files have arrived."""
    if SHARED_LANDING and not force:
        rows = []
        for feed in FEEDS:
            names = [f.name for f in dbutils.fs.ls(f"{LANDING}/{feed}")] if _exists(f"{LANDING}/{feed}") else []  # noqa: F821
            rows.append((feed, f"batch_{n:02d} " + ("arrived" if any(f"batch_{n:02d}" in x for x in names) else "not yet: ask the facilitator"),
                         ", ".join(sorted(names)) or "-"))
        displayHTML(_card_table(f"Shared landing folder: batch_{n:02d} (the facilitator lands files for everyone)",  # noqa: F821
                                ["feed", f"batch_{n:02d}", "files present"], rows, "blue"))
        return
    src = f"{_source_root()}/batch_{n:02d}"
    copied = []
    for feed in FEEDS:
        try:
            files = dbutils.fs.ls(f"{src}/{feed}")  # noqa: F821
        except Exception:
            continue
        for f in files:
            dbutils.fs.cp(f.path, f"{LANDING}/{feed}/{f.name}")  # noqa: F821
            copied.append((feed, f.name))
    where = "the shared landing folder" if SHARED_LANDING else "your landing volume"
    displayHTML(_card_table(f"Landed batch_{n:02d} into {where}", ["feed", "file"], copied, "green"))  # noqa: F821


def _expected():
    for p in (f"{STAGING}/expected_metrics.json",):
        try:
            return json.loads(dbutils.fs.head(p, 1_000_000))  # noqa: F821
        except Exception:
            pass
    local = _repo_data_dir()
    with open(os.path.join(os.path.dirname(local), "expected_metrics.json")) as fh:
        return json.load(fh)


_LAYER_QUERIES = {
    "bronze": [
        ("bronze_deviation_event", "bronze.deviation_event_feed"),
        ("bronze_corrective_action", "bronze.corrective_action_feed"),
        ("bronze_change_control", "bronze.change_control_feed"),
        ("bronze_inspection_result", "bronze.inspection_result_feed"),
    ],
    "silver": [
        ("silver_deviation_event", "silver_clean.deviation_event_feed"),
        ("silver_deviation_event_quarantine", "silver_quarantine.deviation_event_feed"),
        ("silver_corrective_action_event", "silver_clean.corrective_action_feed"),
        ("silver_corrective_action_quarantine", "silver_quarantine.corrective_action_feed"),
        ("silver_corrective_action", "silver_corrective_action_dedup_rows"),
        ("silver_change_control", "silver_clean.change_control_feed"),
        ("silver_change_control_quarantine", "silver_quarantine.change_control_feed"),
        ("silver_inspection_result", "silver_clean.inspection_result_feed"),
        ("silver_inspection_result_quarantine", "silver_quarantine.inspection_result_feed"),
        ("bronze_batch_record", "bronze.batch_record_feed"),          # Python, added in Lab 05
        ("silver_batch_record", "silver_clean.batch_record_feed"),
    ],
    "gold": [
        ("gold_deviation_lifecycle", "gold_deviation_lifecycle.rows"),
        ("gold_change_control_cycle_time", "gold_change_control_cycle_time.rows"),
        ("gold_inspection_quality", "gold_inspection_quality.rows"),
        ("gold_oos_events", "gold_oos_events.rows"),
    ],
}


def _lookup(d, dotted):
    for k in dotted.split("."):
        d = d[k]
    return d


# Tables participants write themselves (everything else in _LAYER_QUERIES is prebuilt): table -> file to edit.
_YOURS = {
    "bronze_inspection_result": "bronze/bronze_inspection_result.sql",
    "bronze_change_control": "bronze/bronze_change_control.sql",
    "silver_inspection_result": "silver/silver_inspection_result.sql",
    "silver_inspection_result_quarantine": "silver/silver_inspection_result.sql",
    "silver_change_control": "silver/silver_change_control.sql",
    "silver_change_control_quarantine": "silver/silver_change_control.sql",
    "gold_inspection_quality": "gold/gold_inspection_quality.sql",
    "gold_oos_events": "gold/gold_inspection_quality.sql",
    "gold_change_control_cycle_time": "gold/gold_change_control_cycle_time.sql (uncomment it)",
    "bronze_batch_record": "python/batch_record.py (Lab 05, SQL and Python step)",
    "silver_batch_record": "python/batch_record.py (Lab 05, SQL and Python step)",
}


def checkpoint(run: int, layer: str):
    """Row counts for one layer after landing batch `run` and running the pipeline. Your tables first."""
    exp = _expected()["after_run"][str(run)]
    rows, ok_all = [], True
    for table, key in sorted(_LAYER_QUERIES[layer], key=lambda tk: tk[0] not in _YOURS):
        want = _lookup(exp, key)
        mine = table in _YOURS
        try:
            got = spark.table(f"{FQ}.{table}").count()  # noqa: F821
        except Exception:
            got = f"missing: finish {_YOURS[table]}" if mine else "missing: run the pipeline"
        ok = got == want
        ok_all &= ok
        rows.append((("&#10003; " if ok else "&#10007; ") + table, "you" if mine else "prebuilt", want, got))
    title = (f"Checkpoint {layer.upper()} after batch {run}: all good" if ok_all
             else f"Checkpoint {layer.upper()} after batch {run}: check the &#10007; rows")
    displayHTML(_card_table(title, ["table", "built by", "expected", "actual"], rows, "green" if ok_all else "coral"))  # noqa: F821


from contextlib import contextmanager


@contextmanager
def needs(what: str, ask: str, once_granted: str):
    """Run a step that needs extra rights. Without them, explain instead of failing:
    what is missing, who grants it, and what the step does once you have it."""
    try:
        yield
    except Exception as e:  # permission, feature not enabled, or table not visible
        err = str(e).strip().splitlines()[0][:240]
        displayHTML(_card_table("This step needs access you may not have yet", ["", ""], [  # noqa: F821
            ("Needs", what), ("Who grants it", ask), ("Once granted", once_granted), ("Message", err)], "coral"))


def pipeline_settings():
    """The lines to add to your pipeline YAML (resources/<name>.pipeline.yml), with your values filled in."""
    displayHTML(_card_table("Add these lines to your pipeline YAML, under the pipeline name, then deploy", ["yaml"], [  # noqa: F821
        ("<pre style='margin:0;font-size:14pt;'>"
         "      parameters:                      # read in SQL as :landing_root, :as_of_date\n"
         f"        landing_root: {LANDING}\n"
         "        as_of_date: \"2026-10-31\"\n"
         "      configuration:                   # read in Python with spark.conf.get()\n"
         f"        landing_root: {LANDING}\n"
         "      event_log:                       # pipeline events as a table (Lab 11)\n"
         "        catalog: ${var.catalog}\n"
         "        schema: ${var.schema}\n"
         "        name: event_log_iops_quality</pre>",)], "blue"))


def show_paths():
    try:
        src = _source_root()
    except RuntimeError as e:
        src = str(e)
    rows = [("catalog", CATALOG), ("your schema", FQ), ("landing folder = pipeline parameter landing_root" + (" (shared)" if SHARED_LANDING else ""), LANDING),
            ("source files used by land_batch()", src.replace("file:", "bundle copy: ")),
            ("pipeline name", ("[dev " + SHORT + "] iops_quality_etl" if TARGET != "qa" else "iops_quality_etl_" + SHORT)
             if GIT_FOLDER_MODE else (f"[dev {SHORT}] iops_quality_{TEAM}" if TARGET != "qa" else f"iops_quality_{TEAM}"))]
    displayHTML(_card_table("Your workshop paths", ["what", "value"], rows, "blue"))  # noqa: F821


def _card_table(title, header, rows, accent):
    color = {"green": "#00A972", "coral": "#FF5F46", "blue": "#4299E0"}[accent]
    th = "".join(f'<th style="text-align:left;padding:8px 12px;border-bottom:2px solid #EEEDE9;">{h}</th>' for h in header)
    tr = "".join("<tr>" + "".join(f'<td style="padding:8px 12px;border-bottom:1px solid #EEEDE9;font-family:monospace;">{c}</td>'
                                  for c in r) + "</tr>" for r in rows)
    return (f'<div style="font-family:sans-serif;max-width:1000px;background:#F9F7F4;border-radius:8px;'
            f'box-shadow:0 2px 8px rgba(27,49,57,0.06);border-top:8px solid {color};padding:16px 20px;color:#0b2026;font-size:14pt;">'
            f'<div style="font-size:18pt;font-weight:700;margin-bottom:10px;">{title}</div>'
            f'<table style="border-collapse:collapse;width:100%;font-size:14pt;">{th}{tr}</table></div>')


spark.sql(f"USE CATALOG {CATALOG}")  # noqa: F821
print(f"User {SHORT} | target {TARGET} | schema {FQ}" if GIT_FOLDER_MODE else f"Team {TEAM} | target {TARGET} | schema {FQ}")
