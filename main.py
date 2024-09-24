import sys
import argparse

import autogen
from agents import *

from tools import *


# Engineer + Executor
def engineer(prompt):
    user = user_proxy()
    executor = kubectl_executor()
    engineer = kube_engineer(llm_config)

    user.reset()
    executor.reset()
    engineer.reset()

    group_chat = autogen.GroupChat(
        agents=[user, engineer, executor],
        max_round=20,
        messages=[],
        speaker_selection_method=engineer_selection(engineer, executor, user),
        send_introductions=True,
    )

    manager = autogen.GroupChatManager(groupchat=group_chat, llm_config=llm_config)
    group_chat_result = user.initiate_chat(
        manager,
        message=react_prompt_message,
        question=prompt,
    )


# Planner + Advisor
def advisor(prompt):
    user = user_proxy()
    planner = kube_planner(llm_config)
    advisor = advisor_agent()

    user.reset()
    planner.reset()
    advisor.reset()

    group_chat = autogen.GroupChat(
        agents=[user, planner, advisor],
        max_round=50,
        messages=[],
        speaker_selection_method=planner_selection(user, planner, advisor),
        send_introductions=True,
    )
    group_chat_result = user.initiate_chat(
        autogen.GroupChatManager(groupchat=group_chat, llm_config=llm_config),
        message=prompt,
    )


# Planner + Advisor + Engineer
def PAE(prompt):
    user = user_proxy()
    executor = kubectl_executor()
    engineer = kube_engineer(llm_config)
    planner = kube_planner(llm_config)
    advisor = advisor_agent()

    user.reset()
    executor.reset()
    engineer.reset()
    planner.reset()
    advisor.reset()

    group_chat = autogen.GroupChat(
        agents=[user, engineer, planner, executor, advisor],
        max_round=50,
        messages=[],
        speaker_selection_method=ocm_selection(
            advisor, planner, engineer, executor, user
        ),
        send_introductions=True,
    )
    manager = autogen.GroupChatManager(groupchat=group_chat, llm_config=llm_config)
    group_chat_result = user.initiate_chat(
        manager,
        message=prompt,
    )

    print(">> END =================================================================")
    # print(group_chat_result.summary)


def perform_task(runner, message):
    runners = {"engineer": engineer, "advisor": advisor, "all": PAE}
    task = runners.get(runner)
    if task:
        task(message)
    else:
        print(f"No valid runner '{runner}' was provided for task: {message}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a task based on the runner type.")
    parser.add_argument("message", type=str, help="The message to indicate the task.")
    parser.add_argument(
        "--runner",
        type=str,
        default="all",
        choices=["engineer", "advisor", "all"],
        help="Specify the type of runner engineer, advisor or 'all' to execute the task.",
    )
    args = parser.parse_args()
    if not args.message:
        print("No valid message!")
    perform_task(args.runner, args.message)
