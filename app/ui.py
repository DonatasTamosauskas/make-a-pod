from datetime import datetime
from uuid import uuid4

import gradio as gr  # type: ignore
from pydantic import AnyHttpUrl

from app.schemas import ArticleEntry
from app.settings import Settings

if Settings().development_mode:
    from app.git_processor import GitDatabaseMock as GitDatabase
else:
    from app.git_processor import GitDatabase  # type: ignore


def create_article(
    title: str,
    url: AnyHttpUrl,
    podcast_title: str,
    podcast_description: str,
    article_text: str,
) -> str:
    print(f"INFO: Received an article: {title}")
    article = ArticleEntry(
        id=uuid4(),
        created_at=datetime.now(),
        url=url,
        title=title,
        podcast_title=podcast_title,
        podcast_description=podcast_description,
        article=article_text,
        audio_location=None,
    )

    article_loc = article.dump_to_file()
    print(f"INFO: Article stored in: {article_loc}")
    return article_loc.name


def git_store_article(article_file: str) -> None:
    git_db = GitDatabase()
    git_db.commit(article_file)


def submit_button_action(
    title: str,
    url: AnyHttpUrl,
    podcast_title: str,
    podcast_description: str,
    article: str,
) -> str:
    article_filename = create_article(
        title, url, podcast_title, podcast_description, article
    )
    return article_filename


with gr.Blocks() as demo:
    with gr.Row():
        title_textbox = gr.Textbox(
            label="Article Title", placeholder="How to do great work"
        )
        url_textbox = gr.Textbox(
            label="Article Url", placeholder="http://paulgraham.com/greatwork.html"
        )

    with gr.Row():
        podcast_title = gr.Textbox(
            label="Podcast Title", placeholder="#? How to Do Great Work - Paul Graham"
        )
        podcast_description = gr.Textbox(
            label="Podcast Description",
            placeholder="""Excerpt from the source material:

"If you collected lists of techniques for doing great work in a lot of different fields, what would the intersection look like? I decided to find out by making it.
Partly my goal was to create a guide that could be used by someone working in any field. But I was also curious about the shape of the intersection. And one thing this exercise shows is that it does have a definite shape; it's not just a point labelled "work hard."
The following recipe assumes you're very ambitious."

Link to the original article: http://paulgraham.com/greatwork.html

""",
        )

    article_textbox = gr.Textbox(
        label="Article",
        placeholder="If you collected lists of techniques for doing great work...",
        lines=10,
        max_lines=30,
        autofocus=True,
    )
    submit_btn = gr.Button("Submit", variant="primary")

    with gr.Row():
        upload_filename_textbox = gr.Textbox(
            value="No files are added...", label="File to commit"
        )
        commit_btn = gr.Button("Commit", variant="secondary")
        clear_btn = gr.ClearButton(
            components=[
                title_textbox,
                url_textbox,
                podcast_title,
                podcast_description,
                article_textbox,
            ]
        )

    submit_btn.click(
        fn=submit_button_action,
        inputs=[
            title_textbox,
            url_textbox,
            podcast_title,
            podcast_description,
            article_textbox,
        ],
        outputs=upload_filename_textbox,
    )
    commit_btn.click(
        fn=git_store_article,
        inputs=upload_filename_textbox,
    )


if __name__ == "__main__":
    if Settings().development_mode:
        print("INFO: Running in development mode.")
    else:
        print("INFO: Running in production mode.")

    demo.launch(server_name="0.0.0.0")
