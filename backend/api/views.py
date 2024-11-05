import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from langchain_core.messages import ToolMessage

from .core.langchaingraph import graph
from .services.customers import get_user_info
from .utilities import _print_event


@csrf_exempt
def query_view(request):
    data = json.loads(request.body.decode("utf-8"))
    customer_id = data.get("customerID", 0)
    thread_id = data.get("threadID", 0)
    query = data.get("query", "")
    user_info = get_user_info(customer_id, thread_id)
    thread_id = user_info["thread_id"]
    if thread_id is None:
        return JsonResponse({"message": "User not found"}, status=404)

    config = {
        "configurable": {
            # The customer_id is used in our order and cart tools to
            # fetch the user's order and cart information
            "customer_id": customer_id,
            # Checkpoints are accessed by thread_id
            "thread_id": thread_id,
        }
    }

    tutorial_questions = [
        "How much available balance do I have?",
        "Do I have any pending orders?",
        "What are my current orders?",
        "What's in my cart?",
    ]

    _printed = set()
    # We can reuse the tutorial questions from part 1 to see how it does.

    events = graph.stream({"messages": ("user", query)}, config, stream_mode="values")
    message = ""
    for event in events:
        message = _print_event(event, _printed)
    # snapshot = graph.get_state(config)
    # while snapshot.next:
    #     # We have an interrupt! The agent is trying to use a tool, and the user can approve or deny it
    #     # Note: This code is all outside of your graph. Typically, you would stream the output to a UI.
    #     # Then, you would have the frontend trigger a new run via an API call when the user has provided input.
    #     try:
    #         user_input = input(
    #             "Do you approve of the above actions? Type 'y' to continue;"
    #             " otherwise, explain your requested changed.\n\n"
    #         )
    #     except:
    #         user_input = "y"
    #     if user_input.strip() == "y":
    #         # Just continue
    #         result = graph.invoke(
    #             None,
    #             config,
    #         )
    #     else:
    #         # Satisfy the tool invocation by
    #         # providing instructions on the requested changes / change of mind
    #         result = graph.invoke(
    #             {
    #                 "messages": [
    #                     ToolMessage(
    #                         tool_call_id=event["messages"][-1].tool_calls[0]["id"],
    #                         content=f"API call denied by user. Reasoning: '{user_input}'. Continue assisting, accounting for the user's input.",
    #                     )
    #                 ]
    #             },
    #             config,
    #         )
    #     snapshot = graph.get_state(config)
    return JsonResponse({"message": message, "threadID": thread_id}, status=200)
