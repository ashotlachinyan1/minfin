"""Repository paths used by every pipeline stage."""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = REPO_ROOT / "config"
SEED_DIR = REPO_ROOT / "seed"
DATA_DIR = REPO_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
MANUAL_DROP_DIR = DATA_DIR / "manual_drop"
MANUAL_DIR = DATA_DIR / "manual"
INTERIM_DIR = DATA_DIR / "interim"
WAREHOUSE_PATH = DATA_DIR / "warehouse" / "armbudget.duckdb"
EXPORT_DIR = DATA_DIR / "export"
DOCS_DIR = REPO_ROOT / "docs"
