import os
from dagster import AssetSelection, Definitions, define_asset_job, load_assets_from_modules, ScheduleDefinition

from src import assets
from src.resources import LlamaResource

all_assets = load_assets_from_modules([assets])

llama = LlamaResource(endpoint=os.getenv("LLAMA_CPP_ENDPOINT"))

hackernews_job = define_asset_job("hackernews_job", selection=AssetSelection.all())

hackernews_schedule = ScheduleDefinition(
    job=hackernews_job,
    cron_schedule="0 * * * *",  # every hour
)

defs = Definitions(
    assets=all_assets, jobs=[hackernews_job], resources={"llama": llama}, schedules=[hackernews_schedule]
)
