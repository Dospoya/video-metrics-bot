from datetime import date
from typing import Annotated, Literal

from pydantic import BaseModel, Field


class EmptyParams(BaseModel):
    pass


class CreatorVideosInPeriodParams(BaseModel):
    creator_id: str
    start_date: date
    end_date: date


class VideosOverViewsQueryParams(BaseModel):
    views: int


class ViewsGrowthOnDateParams(BaseModel):
    on_date: date


class TotalVideosQuery(BaseModel):
    intent: Literal["total_videos"]
    params: EmptyParams


class CreatorVideosInPeriodQuery(BaseModel):
    intent: Literal["creator_videos_in_period"]
    params: CreatorVideosInPeriodParams


class VideosOverViewsQuery(BaseModel):
    intent: Literal["videos_over_views"]
    params: VideosOverViewsQueryParams


class ViewsGrowthOnDateQuery(BaseModel):
    intent: Literal["views_growth_on_date"]
    params: ViewsGrowthOnDateParams


class Query(BaseModel):
    query: (
        TotalVideosQuery
        | CreatorVideosInPeriodQuery
        | VideosOverViewsQuery
        | ViewsGrowthOnDateQuery
    )
