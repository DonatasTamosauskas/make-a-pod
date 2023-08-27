from pathlib import Path

from TTS.api import TTS  # type: ignore

from app.schemas import ArticleEntry
from app.settings import Settings

if Settings().development_mode:
    from app.git_processor import GitDatabaseMock as GitDatabase
else:
    from app.git_processor import GitDatabase  # type: ignore


def vits_synthesize_speech(
    text: str,
    file_path: Path,
    tts_model: str = "tts_models/en/vctk/vits",
    speaker: str | None = "p267",
) -> None:
    tts = TTS(tts_model)
    tts.tts_to_file(text=text, speaker=speaker, file_path=file_path)


def read_article(location: Path) -> ArticleEntry:
    with open(location) as file:
        print(f"INFO: Reading file {location}.")
        return ArticleEntry.model_validate_json(file.read())


def get_articles(db_location: Path) -> list[ArticleEntry]:
    git = GitDatabase()
    git.pull()

    articles = [
        read_article(article_file)
        for article_file in db_location.iterdir()
        if article_file.suffix == ".json"
    ]
    print(f"INFO: Found {len(articles)} articles.")
    return articles


def push_updates(updated_article: str) -> None:
    git = GitDatabase()
    git.pull()
    git.commit(updated_article)


def process_article_tts(article: ArticleEntry) -> Path:
    audio_file_loc = Path("podcasts") / f"{article.get_filename_root()}.wav"
    print(f"INFO: Synthesizing speech for {audio_file_loc}.")
    vits_synthesize_speech(text=article.article, file_path=audio_file_loc)
    return audio_file_loc


def main() -> None:
    all_articles = get_articles(Path("database"))
    unprocessed_articles = [
        article for article in all_articles if article.audio_location is None
    ]
    print(f"INFO: Found {len(unprocessed_articles)} articles ready for TTS processing")

    for article in unprocessed_articles:
        audio_loc = process_article_tts(article)
        article.audio_location = audio_loc
        article.dump_to_file()
        push_updates(f"{article.get_filename_root()}.json")

    print("INFO: Article processing complete.")


if __name__ == "__main__":
    if Settings().development_mode:
        print("INFO: Running in development mode.")
    else:
        print("INFO: Running in production mode.")

    main()
