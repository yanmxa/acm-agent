import os

import autogen

def user_proxy() -> autogen.UserProxyAgent:
    return autogen.UserProxyAgent(
        name="User",
        human_input_mode="ALWAYS",
        is_termination_msg=lambda x: x.get("content", "")
        and x.get("content", "").rstrip().endswith("TERMINATE"),
        code_execution_config=False,  # we don't want to execute code in this case.
        default_auto_reply="Reply `TERMINATE` if the task is done.",
        description="The user who ask questions and give tasks.",
    )
    