import openai

from src.config.config import settings
from src.schemas.intent import Query
from src.service.render_template import render_template

SYSTEM_PROMPT = render_template("instruction.md.jinja2")

client = openai.OpenAI(api_key=settings.openai_api_key)


def converter(user_input: str) -> Query | None:
    response = client.responses.parse(
        model="gpt-4o-mini",
        input=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {"role": "user", "content": user_input},
        ],
        text_format=Query,
    )
    return response.output_parsed
