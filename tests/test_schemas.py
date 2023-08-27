from datetime import datetime
from uuid import uuid4

from pydantic import AnyUrl

from app.schemas import ArticleEntry


def test_ArticleEntry_get_filename_root_http() -> None:
    article = ArticleEntry(
        id=uuid4(),
        created_at=datetime(2000, 1, 1, 1, 1, 1),
        url=AnyUrl("http://www.paulgraham.com/wisdom.html"),
        title="Is It Worth Being Wise?",
        podcast_title="Title",
        podcast_description="Description",
        article="A few days ago I finally figured out something I've wondered about for 25 years: the relationship between wisdom and intelligence. \n",
        audio_location=None,
    )

    filename_root = article.get_filename_root()

    filename_root == "2020_01_01-is_it_worth_being_wise-paulgraham_com"
