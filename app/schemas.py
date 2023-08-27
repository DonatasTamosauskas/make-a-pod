from datetime import datetime
from pathlib import Path

from pydantic import BaseModel, HttpUrl, types


class ArticleEntry(BaseModel):
    id: types.UUID4
    created_at: datetime
    url: HttpUrl
    title: str
    podcast_title: str | None
    podcast_description: str | None
    audio_location: Path | None
    article: str

    def get_filename_root(self) -> str:
        article_name = (
            f"{str(self.created_at.date()).replace('-', '_')}-"
            + f"{self.title.lower().replace(' ', '_')}-"
            + f"{format_url(str(self.url))}"
        )
        return article_name

    def dump_to_file(self, location: Path | None = None) -> Path:
        if location is None:
            location = Path("database")

        storage_location = location / f"{self.get_filename_root()}.json"
        with open(storage_location, "w+") as article_file:
            article_file.write(self.model_dump_json(indent=2))

        return storage_location


def format_url(url: str) -> str:
    print(f"INFO: Formatting url: {url}")
    url = str(url)
    url = url.replace("http://", "").replace("https://", "")
    url_parent = str(Path(url).parent)
    url_parent = url_parent.replace(".", "_")
    url_parent = url_parent.replace("/", "_")

    print(f"INFO: Url formatted: {url_parent}")
    return url_parent
