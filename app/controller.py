from typing import Type

from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

from app.api.base import Api, SearchResults


class ApiController:
    def __init__(self, api: Type[Api]) -> None:
        self._api = api

    def _normalize(self, s: str) -> str:
        return s.strip().lower()

    def _create_html_a(self, href: str, url: str) -> str:
        return f"""<a href="{href}">{url}</a>"""

    async def handle_query(self, query: str, message: Message) -> Message:
        _search_results: SearchResults = await self._api.search(query)
        _processed_message = message

        if _search_results.total > 0:
            if self._normalize(_title := _search_results.results[0]) == self._normalize(
                query
            ):
                # exact
                _url = await self._api.get_page_link(_title)

                _processed_message = await message.answer(
                    text=self._create_html_a(_title, _url),
                    parse_mode="html",
                    reply_markup=ReplyKeyboardRemove(),
                )
            else:
                _markup = ReplyKeyboardMarkup()
                for _r in _search_results.results:
                    _markup.add(KeyboardButton(_r))
                _processed_message = await message.answer(
                    text=f"Total results: {_search_results.total}",
                    reply_markup=_markup,
                )
        else:
            _processed_message = await message.answer("Nothing found")
        return _processed_message
