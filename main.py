"""
main.py - Civic Interconnect Monitor Schema Agent

This agent monitors civic data sources for schema changes and generates daily reports.
It pulls OCD Divisions and OpenStates GraphQL schema.

MIT License — Civic Interconnect
"""

import sys
from pathlib import Path

from dotenv import load_dotenv

from civic_lib_core import log_utils, config_utils
from civic_lib_core.date_utils import today_utc_str
from civic_lib_core.path_utils import ensure_dir
from civic_lib_core.yaml_utils import write_yaml

from parsers import ocd_parser, openstates_parser

log_utils.init_logger()
logger = log_utils.logger


def main():
    """
    Main function to run the agent.
    Expected config.yaml keys:
    - storage_path
    - report_path
    - ocd_repo_url
    """
    logger.info("===== Starting Monitor Schema Agent =====")
    load_dotenv()

    ROOT_DIR = Path(__file__).resolve().parent
    config = config_utils.load_yaml_config("config.yaml", root_dir=ROOT_DIR)
    version = config_utils.load_version("VERSION", root_dir=ROOT_DIR)
    api_key = config_utils.load_openstates_api_key()
    today = today_utc_str()
    logger.info(f"Polling date: {today}")

    storage_path = ensure_dir(Path(config["storage_path"]) / today)
    report_path = ensure_dir(Path(config["report_path"]) / today)
    logger.info(f"Storage path: {storage_path}")
    logger.info(f"Report path: {report_path}")

    try:
        logger.info("Starting OCD Divisions monitoring...")
        ocd_changes = ocd_parser.run(storage_path, config)
        logger.info("OCD Divisions completed.")
    except Exception as e:
        ocd_changes = f"OCD pull failed: {str(e)}"
        logger.error(ocd_changes)

    try:
        logger.info("Starting OpenStates monitoring...")
        openstates_changes = openstates_parser.run(storage_path, config, api_key)
        logger.info("OpenStates completed.")
    except Exception as e:
        openstates_changes = f"OpenStates pull failed: {str(e)}"
        logger.error(openstates_changes)

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
    except Exception as e:
        logger.exception(f"Agent failed unexpectedly. {e}")
        sys.exit(1)
