import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from langchain_core.messages import ToolMessage, AIMessage

from .core.langchaingraph import graph
from .services.customers import get_user_info
from .helpers.utilities import print_event


@csrf_exempt
def query_view(request):
    """
    This view is used to handle the user's query.
    :param request: the query from the user
    :return: the response to the bot
    """
    data = json.loads(request.body.decode("utf-8"))
    customer_id = data.get("customerID", 0)
    interrupted = data.get(
        "interrupted", False
    )  # This is a indicator to check if the process has been interrupted by sensitive tools
    query = data.get("query", "")

    user_info = get_user_info(customer_id)
    thread_id = user_info["thread_id"]

    if thread_id is None:
        return JsonResponse({"message": "User not found"}, status=200)

    config = {
        "configurable": {
            # The customer_id is used in our order and cart tools to
            # fetch the user's order and cart information
            "customer_id": customer_id,
            # Checkpoints are accessed by thread_id
            "thread_id": thread_id,
        }
    }

    if interrupted:
        # If the process was interrupted by sensitive tools,
        # the user will be asked to approve the actions.
        if query.strip() == "approve":
            # Approved
            graph.invoke(
                None,
                config,
            )
        else:
            tool_call_id = (
                graph.get_state(config).values["messages"][-1].tool_calls[0]["id"]
            )
            graph.invoke(
                {
                    "messages": [
                        ToolMessage(
                            tool_call_id=tool_call_id,
                            content=f"API call denied by user. Reasoning: `{query}`. Continue assisting, accounting for the user's input.",
                        )
                    ]
                },
                config,
            )

    _printed = set()

    events = graph.stream({"messages": ("user", query)}, config, stream_mode="values")
    message = ""
    for event in events:
        interrupted = False
        message = print_event(event, _printed)
        state = graph.get_state(config)
        if state.next:
            interrupted = True
            message = (
                "Do you approve of the above actions? Type 'approve' to continue;"
                " otherwise, explain your requested changed."
            )
    return JsonResponse(
        {"message": message, "threadID": thread_id, "interrupted": interrupted},
        status=200,
    )
