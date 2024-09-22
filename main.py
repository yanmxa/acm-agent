import sys
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


if __name__ == "__main__":
    if len(sys.argv) > 1:
        advisor(sys.argv[1])
    else:
        print("No parameters were provided.")
