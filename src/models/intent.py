from datetime import date
from enum import Enum
from typing import Annotated

from pydantic import BaseModel, Field, RootModel


class Intents(str, Enum):
    TOTAL_VIDEOS = "total_videos"
    CREATOR_VIDEOS_IN_PERIOD = "creator_videos_in_period"
    VIDEOS_OVER_VIEWS = "videos_over_views"
    VIEWS_GROWTH_ON_DATE = "views_growth_on_date"


class EmptyParams(BaseModel):
    pass


class CreatorVideosInPeriodParams(BaseModel):
    creator_id: str
    start_date: date
    end_date: date


class VideosOverViewsQueryParams(BaseModel):
    views: int


class ViewsGrowthOnDateParams(BaseModel):
    dt: date


class TotalVideosQuery(BaseModel):
    intent: Intents = Intents.TOTAL_VIDEOS
    params: EmptyParams


class CreatorVideosInPeriodQuery(BaseModel):
    intent: Intents = Intents.CREATOR_VIDEOS_IN_PERIOD
    params: CreatorVideosInPeriodParams


class VideosOverViewsQuery(BaseModel):
    intent: Intents = Intents.VIDEOS_OVER_VIEWS
    params: VideosOverViewsQueryParams


class ViewsGrowthOnDateQuery(BaseModel):
    intent: Intents = Intents.VIEWS_GROWTH_ON_DATE
    params: ViewsGrowthOnDateParams


Queries = Annotated[
    TotalVideosQuery
    | CreatorVideosInPeriodQuery
    | VideosOverViewsQuery
    | ViewsGrowthOnDateQuery,
    Field(discriminator="intent"),
]


class Query(RootModel[Queries]):
    pass
