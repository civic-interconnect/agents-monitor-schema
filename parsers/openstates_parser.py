"""
parsers/openstates_parser.py

Fetches the OpenStates GraphQL schema and extracts field names for each type.
"""

import json
import asyncio
from pathlib import Path
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

from civic_lib import log_utils, error_utils
from civic_lib.path_utils import ensure_dir

logger = log_utils.logger


def run(storage_path: str | Path, config: dict, api_key: str) -> dict | str:
    """
    Main entry point for the schema monitoring agent.

    Args:
        storage_path (str | Path): Daily storage path.
        config (dict): Loaded YAML configuration.
        api_key (str): OpenStates API key.

    Returns:
        dict or str: Parsed schema or access message.
    """
    storage_path = ensure_dir(storage_path)
    url = config["openstates_graphql_url"]
    headers = {"Authorization": f"Bearer {api_key}"}

    logger.info(f"Connecting to OpenStates GraphQL: {url}")
    transport = AIOHTTPTransport(url=url, headers=headers, ssl=True)
    client = Client(transport=transport, fetch_schema_from_transport=True)

    introspection_query = gql("""
    {
      __schema {
        types {
          name
          fields {
            name
          }
        }
      }
    }
    """)

    async def fetch_schema():
        try:
            logger.info("Sending introspection query to OpenStates...")
            result = await client.execute_async(introspection_query)
            logger.info("Successfully received schema from OpenStates.")
            return result
        except Exception as e:
            return error_utils.handle_transport_errors(
                e, resource_name="OpenStates Introspection"
            )

    schema = asyncio.run(fetch_schema())

    if isinstance(schema, str):
        return schema

    types = schema["__schema"]["types"]
    parsed_schema = {}

    for t in types:
        name = t.get("name")
        fields = t.get("fields")
        if fields:
            parsed_schema[name] = [f["name"] for f in fields]

    schema_file = storage_path / "openstates_schema_fields.json"
    schema_file.write_text(json.dumps(parsed_schema, indent=2), encoding="utf-8")

    logger.info(f"Schema written to {schema_file}")
    return parsed_schema
