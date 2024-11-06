import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from langchain_core.messages import ToolMessage

from .core.langchaingraph import graph
from .services.customers import get_user_info
from .helpers.utilities import print_event


@csrf_exempt
def query_view(request):
    data = json.loads(request.body.decode("utf-8"))
    customer_id = data.get("customerID", 0)
    thread_id = data.get("threadID", 0)
    interrupted = data.get("interrupted", False)
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
    if interrupted:
        tool_call_id = (
            graph.get_state(config).values["messages"][-1].tool_calls[0]["id"]
        )
        if query.strip() == "y":
            tool_message = [
                ToolMessage(
                    tool_call_id=tool_call_id, content="Client approved to proceed."
                )
            ]

            # We now update the state
            # Notice that we are also specifying `as_node="ask_human"`
            # This will apply this update as this node,
            # which will make it so that afterwards it continues as normal
            # graph.update_state(
            #     config, {"messages": tool_message}, as_node="sensitive_tools"
            # )
            graph.invoke(
                None,
                config,
            )
        else:
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

        # We can check the state
        # We can see that the state currently has the `agent` node next
        # This is based on how we define our graph,
        # where after the `ask_human` node goes (which we just triggered)
        # there is an edge to the `agent` node
        # graph.get_state(config).next

    _printed = set()
    # We can reuse the tutorial questions from part 1 to see how it does.

    events = graph.stream({"messages": ("user", query)}, config, stream_mode="values")
    message = ""
    for event in events:
        interrupted = False
        message = print_event(event, _printed)
        state = graph.get_state(config)
        if state.next:
            print("Interrupted!")
            interrupted = True
            message = (
                "Do you approve of the above actions? Type 'y' to continue;"
                " otherwise, explain your requested changed."
            )
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
    return JsonResponse(
        {"message": message, "threadID": thread_id, "interrupted": interrupted},
        status=200,
    )
