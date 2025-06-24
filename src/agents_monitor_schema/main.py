"""
main.py - Civic Interconnect Monitor Schema Agent

This agent monitors civic data sources for schema changes and generates daily reports.
It pulls OCD Divisions and OpenStates GraphQL schema.

MIT License — Civic Interconnect
"""

import os
import sys
from pathlib import Path

from civic_lib_core import config_utils, log_utils
from civic_lib_core.date_utils import today_utc_str
from civic_lib_core.path_utils import ensure_dir
from civic_lib_core.yaml_utils import write_yaml
from dotenv import load_dotenv

from agents_monitor_schema.parsers import ocd_parser, openstates_parser


def main() -> None:
    """
    Main function to run the agent.
    Expected config.yaml keys:
    - storage_path
    - report_path
    - ocd_repo_url
    """
    log_utils.init_logger()
    logger = log_utils.logger

    logger.info("===== Starting Monitor Schema Agent =====")
    load_dotenv()

    root_dir = Path.cwd()
    config = config_utils.load_yaml_config("config.yaml", root_dir=root_dir)
    version = config_utils.load_version("VERSION", root_dir=root_dir)
    api_key: str | None = os.getenv("OPENSTATES_API_KEY")
    today = today_utc_str()
    logger.info(f"Polling date: {today}")

    storage_path = ensure_dir(Path(config["storage_path"]) / today)
    report_path = ensure_dir(Path(config["report_path"]) / today)
    logger.info(f"Storage path: {storage_path}")
    logger.info(f"Report path: {report_path}")

    # Monitor OCD Divisions
    try:
        logger.info("Starting OCD Divisions monitoring...")
        ocd_changes = ocd_parser.run(storage_path, config)
        logger.info("OCD Divisions completed.")
    except Exception as e:
        ocd_changes = f"OCD pull failed: {str(e)}"
        logger.error(ocd_changes)

    # Monitor OpenStates, only if API key is set
    if api_key:
        try:
            logger.info("Starting OpenStates monitoring...")
            openstates_changes = openstates_parser.run(storage_path, config, api_key)
            logger.info("OpenStates completed.")
        except Exception as e:
            openstates_changes = f"OpenStates pull failed: {str(e)}"
            logger.error(openstates_changes)
    else:
        openstates_changes = "Skipped — OPENSTATES_API_KEY not set."
        logger.warning(openstates_changes)

    # Final report
    report = {
        "date": today,
        "version": version,
        "OCD Divisions": ocd_changes,
        "OpenStates": openstates_changes,
    }
    report_file = report_path / f"{today}-change-report.yaml"
    write_yaml(report, report_file)
    logger.info(f"Report created: {report_file}")


if __name__ == "__main__":
    try:
        main()
        sys.exit(0)
    except Exception:
        sys.exit(1)
