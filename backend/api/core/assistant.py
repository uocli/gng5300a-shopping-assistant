import os
from datetime import datetime
from typing import Annotated

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnableConfig
from typing_extensions import TypedDict

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

from .state import State
from ..services.customers import fetch_user_order_information
from ..services.products import (
    get_product,
    search_products,
)

load_dotenv()


class Assistant:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    def __call__(self, state: State, config: RunnableConfig):
        while True:
            result = self.runnable.invoke(state)
            # If the LLM happens to return an empty response, we will re-prompt it
            # for an actual response.
            if not result.tool_calls and (
                not result.content
                or isinstance(result.content, list)
                and not result.content[0].get("text")
            ):
                messages = state["messages"] + [("user", "Respond with a real output.")]
                state = {**state, "messages": messages}
            else:
                break
        return {"messages": result}


# Haiku is faster and cheaper, but less accurate
# llm = ChatAnthropic(model="claude-3-haiku-20240307")
# llm = ChatAnthropic(model="claude-3-sonnet-20240229", temperature=1)
# You can update the LLMs, though you may need to update the prompts


llm = ChatOpenAI(
    base_url="https://api.studio.nebius.ai/v1/",
    api_key=os.getenv("NEBIUS_API_KEY"),
    model="meta-llama/Meta-Llama-3.1-70B-Instruct",
)


assistant_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful shopping assistant. "
            " Use the provided tools to search for products, policies, and other information to assist the user's queries. "
            " When searching, be persistent. Expand your query bounds if the first search returns no results. "
            " If a search comes up empty, expand your search before giving up."
            "\n\nCurrent user:\n<User>\n{user_info}\n</User>"
            "\nCurrent time: {time}.",
        ),
        ("placeholder", "{messages}"),
    ]
).partial(time=datetime.now())

# "Read"-only tools (such as retrievers) don't need a user confirmation to use
safe_tools = [TavilySearchResults(max_results=1), fetch_user_order_information]

# These tools all change the user's reservations.
# The user has the right to control what decisions are made
sensitive_tools = [
    get_product,
    search_products,
]
sensitive_tool_names = {t.name for t in sensitive_tools}
# Our LLM doesn't have to know which nodes it has to route to. In its 'mind', it's just invoking functions.
assistant_runnable = assistant_prompt | llm.bind_tools(safe_tools + sensitive_tools)
