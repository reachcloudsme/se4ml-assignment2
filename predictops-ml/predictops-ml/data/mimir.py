import logging
import time

import requests

logger = logging.getLogger(__name__)


def query_mimir(promql, mimir_url):
    end = int(time.time())
    start = end - 600

    logger.info("Fetching metrics from Mimir")

    try:
        response = requests.get(
            f"{mimir_url}/prometheus/api/v1/query_range",
            params={
                "query": promql,
                "start": start,
                "end": end,
                "step": 30,
            },
            timeout=10,
        )

        response.raise_for_status()
        data = response.json()

        logger.info("Successfully retrieved metrics from Mimir")
        return data

    except (requests.RequestException, ValueError):
        logger.exception("Failed to retrieve metrics from Mimir")
        raise
