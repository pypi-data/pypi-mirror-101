from enum import Enum
from typing import Optional

import requests
from fake_useragent import UserAgent


class SortBy(Enum):
    name = "name"
    main_story = "main"
    main_extra = "mainp"
    completionist = "comp"
    average_time = "averagea"
    top_rated = "rating"
    most_popular = "popular"
    most_backlogs = "backlog"
    most_submissions = "usersp"
    most_played = "playing"
    most_speedruns = "speedruns"
    release_date = "release"


class SpecialQuery(Enum):
    recently_updated = "recently updated"
    recently_added = "recently added"


class HowLongToBeatWebsite:
    base_url = "https://howlongtobeat.com/"

    @classmethod
    def search_results(
        cls,
        query_string: str = "",
        page: Optional[int] = None,
        sort_by: SortBy = SortBy.most_popular,
    ):
        ua = UserAgent()
        headers = {
            "content-type": "application/x-www-form-urlencoded",
            "accept": "*/*",
            "User-Agent": ua.random,
        }
        data = {
            "queryString": query_string,
            "t": "games",
            "sorthead": sort_by.value,
            "sortd": "Normal Order",
            "plat": "",
            "length_type": "main",
            "length_min": "",
            "length_max": "",
            "detail": "",
        }
        page_param = f"?page={page}" if page else ""
        res = requests.post(
            f"{cls.base_url}search_results.php{page_param}",
            data=data,
            headers=headers,
        )
        return res.text
