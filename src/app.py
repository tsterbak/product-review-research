import json
from typing import List
from openai import OpenAI
from duckduckgo_search import DDGS
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

from promptmage import PromptMage, Prompt, MageResult

# Load the environment variables from the .env file
load_dotenv()

# Initialize the OpenAI client
client = OpenAI()

# Create a new PromptMage instance
mage = PromptMage(
    name="product-review-research",
    available_models=["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-4"],
)
# mage.prompt_store.store_prompt(
#     Prompt(
#         name="extract_facts",
#         system="You are an expert in extracting key facts from reviews.",
#         user="Extract the key facts from the following review: {review}",
#         template_vars=["review"],
#     )
# )
# mage.prompt_store.store_prompt(
#     Prompt(
#         name="summarize_facts",
#         system="You are an expert in summarizing key facts.",
#         user="Summarize the following key facts: {facts}",
#         template_vars=["facts"],
#     )
# )

####################
# Application code #
####################


@mage.step(name="search-product-reviews", initial=True)
def search_product_reviews(product_name: str) -> str:
    """Search for product reviews on the internet."""
    results = DDGS().text(
        f"reviews of {product_name}",
        safesearch="off",
        max_results=5,
    )
    youtube_results = DDGS().videos(
        f"reviews of {product_name}",
        safesearch="off",
        max_results=5,
    )
    return [
        MageResult(
            next_step="extract-facts",
            review=r["body"],
            source=r.get("href", "not found"),
        )
        for r in results
    ] + [
        MageResult(
            next_step="get-transcript",
            video_id=y["content"].split("watch?v=")[1],
        )
        for y in youtube_results
        if "content" in y and y.get("publisher") == "YouTube"
    ]


@mage.step(name="get-transcript")
def get_transcript(video_id: str) -> str:
    """Get the transcript of a YouTube video.

    Uses the YouTube API to get the transcript of a video with youtube-transcript-api.
    """
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
        transcript_text = TextFormatter().format_transcript(transcript)
    except Exception as e:
        transcript_text = f"Error: {str(e)}"
    return MageResult(
        next_step="extract-facts",
        review=transcript_text,
        source="https://www.youtube.com/watch?v=" + video_id,
    )


@mage.step(name="extract-facts", prompt_name="extract_facts", initial=True)
def extract_facts(
    review: str, source: str, prompt: Prompt, model: str = "gpt-4o-mini"
) -> List[MageResult]:
    """Extract the facts as a bullet list from an article."""
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": prompt.system},
            {
                "role": "user",
                "content": prompt.user.format(review=review),
            },
        ],
    )
    raw_facts = response.choices[0].message.content
    return MageResult(next_step="summarize", facts=f"{raw_facts}\n\nSource: {source}")


@mage.step(
    name="summarize",
    prompt_name="summarize_facts",
    many_to_one=True,
)
def summarize_facts(
    facts: str, prompt: Prompt  # , review: str | None = None
) -> MageResult:
    """Summarize the given facts as a single sentence."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt.system},
            {
                "role": "user",
                "content": prompt.user.format(facts="\n\n".join(facts)),
            },
        ],
    )
    return MageResult(result=response.choices[0].message.content)
