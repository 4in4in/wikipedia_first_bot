import json
import logging

from aiohttp import ClientSession, ClientResponse
from urllib.parse import unquote
from app.api.base import Api, SearchResults

logger = logging.getLogger(__name__)


class WikipediaApi(Api):
    def __init__(self, lang: str = "ru") -> None:
        self._lang = lang

    @property
    def base_url(self):
        return f"https://{self._lang}.wikipedia.org"

    @property
    def api_uri(self):
        return "/w/api.php"

    @property
    def index_uri(self):
        return "/w/index.php"

    async def _get_request(self, *args, **kwargs) -> ClientResponse:
        async with ClientSession(base_url=self.base_url) as session:
            return await session.get(*args, **kwargs)

    async def search(self, query: str) -> list[str]:
        response = await self._get_request(
            url=self.api_uri,
            params={
                "format": "json",
                "action": "query",
                "list": "search",
                "srsearch": query,
            },
        )
        json_result = await response.json()
        logger.info("result: %s", json.dumps(json_result, indent=4, ensure_ascii=False))

        total = json_result["query"]["searchinfo"]["totalhits"]
        pre_results = json_result["query"]["search"]

        return SearchResults(total=total, results=[_r["title"] for _r in pre_results])

    async def get_page_link(self, title: str) -> str:
        response = await self._get_request(
            url=self.index_uri,
            params={"search": title},
        )
        return unquote(str(response.url))
