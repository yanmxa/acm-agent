import os

import autogen
from autogen.coding import LocalCommandLineCodeExecutor

current_working_directory = os.path.dirname(os.path.realpath(__file__))

def kubectl_executor() -> autogen.UserProxyAgent:
    return autogen.UserProxyAgent(
        "Executor",
        description="Execute the code written by the 'Kubernetes Engineer' and report the result to it. Invoke me only when you have code block to run",
        llm_config=False,
        code_execution_config={
            "executor": LocalCommandLineCodeExecutor(
                timeout=10,
                work_dir=os.path.join(current_working_directory, "__kubecache__"),
            )
        },
        max_consecutive_auto_reply=12,  # terminate without auto-reply
        human_input_mode="ALWAYS",
    )
