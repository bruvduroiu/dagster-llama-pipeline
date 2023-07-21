import requests

from dagster import (
    asset,
    DynamicOut,
    DynamicOutput,
    MetadataValue,
    get_dagster_logger,
    graph_asset,
    op,
    Output,
)

from src.ops import get_paragraph_text, summarise_text


HN_TOPSTORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
HN_ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{item_id}.json"

# TODO: Move this as a Dagster configuration
TOPSTORY_LIMIT = 5


@asset
def topstory_ids():
    top_new_story_ids = requests.get(HN_TOPSTORIES_URL).json()[:TOPSTORY_LIMIT]
    return top_new_story_ids


@asset
def topstories(topstory_ids):
    logger = get_dagster_logger()

    results = []
    for item_id in topstory_ids:
        item = requests.get(HN_ITEM_URL.format(item_id=item_id)).json()
        results.append(item)

        if len(results) % 5 == 0:
            logger.info(f"Got {len(results)} items so far.")

    return Output(
        value=results,
        metadata={
            "num_records": len(results),
            "preview": MetadataValue.json(results),
        },
    )


@graph_asset
def topstories_summaries(topstories):
    @op(out=DynamicOut())
    def _fan_out(topstories):
        for i, topstory in enumerate(topstories):
            yield DynamicOutput(topstory.get("url"), mapping_key=str(topstory.get("id", i)))

    @op
    def _process(topstories_collection):
        summaries = list(topstories_collection)
        return Output(summaries, metadata={"n": len(summaries), "preview": MetadataValue.json(summaries)})

    fanned_topstories = _fan_out(topstories)
    topstories_text = fanned_topstories.map(get_paragraph_text)
    topstories_summaries = topstories_text.map(summarise_text)

    summaries = _process(topstories_summaries.collect())

    return summaries


@asset
def daily_summaries(topstories_summaries):
    return Output(
        topstories_summaries,
        metadata={"n": len(topstories_summaries), "preview": MetadataValue.json(topstories_summaries)},
    )
