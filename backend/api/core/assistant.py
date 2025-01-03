import os
from datetime import datetime

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnableConfig
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

from .state import State
from ..services.customers import (
    fetch_user_and_cart_info,
    add_account_balance,
)
from ..services.products import (
    search_products,
    get_product_by_name,
    get_product_by_category,
    recommend_products,
)
from ..services.carts import (
    get_current_cart,
    update_cart,
    add_a_product_to_cart,
)

from ..services.orders import (
    place_order,
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


llm = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-3.5-turbo",
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
safe_tools = [
    TavilySearchResults(max_results=1),
    fetch_user_and_cart_info,
    search_products,
    get_product_by_name,
    get_product_by_category,
    get_current_cart,
    update_cart,
    add_a_product_to_cart,
    recommend_products,
]

# These tools all change the user's reservations.
# The user has the right to control what decisions are made
sensitive_tools = [
    place_order,
    add_account_balance,
]

sensitive_tool_names = {t.name for t in sensitive_tools}
# Our LLM doesn't have to know which nodes it has to route to. In its 'mind', it's just invoking functions.
assistant_runnable = assistant_prompt | llm.bind_tools(safe_tools + sensitive_tools)
