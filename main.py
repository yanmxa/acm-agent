import os
import sys
import autogen

from agents import *
from tools import *

from dotenv import load_dotenv

load_dotenv()

llm_config = {
    "config_list": [
        {
            "model": "llama-3.1-70b-versatile",
            "base_url": "https://api.groq.com/openai/v1",
            "api_key": os.getenv("GROQ_API_KEY"),
            "temperature": 0.0,
            "price": [0, 0],
        }
    ]
}

# llm_config = {
#     "config_list": [{"model": "gpt-4o", "api_key": os.environ.get("OPENAI_API_KEY")}]
# }


def main(prompt):
    user = user_proxy()
    executor = kubectl_executor()
    engineer = kube_engineer(llm_config)
    planner = kube_planner(llm_config)
    ocmer = ocm_agent(llm_config)

    user.reset()
    executor.reset()
    engineer.reset()
    planner.reset()
    ocmer.reset()

    # Engineer
    # group_chat = autogen.GroupChat(
    #     agents=[user, engineer, executor],
    #     max_round=20,
    #     messages=[],
    #     speaker_selection_method=engineer_selection(engineer, executor, user),
    #     send_introductions=True,
    # )
    # manager = autogen.GroupChatManager(groupchat=group_chat, llm_config=llm_config)
    # group_chat_result = user.initiate_chat(
    #     manager,
    #     message=react_prompt_message,
    #     question=prompt,
    # )

    # Planner + Engineer
    # group_chat = autogen.GroupChat(
    #     agents=[user, engineer, planner, executor],
    #     max_round=20,
    #     messages=[],
    #     speaker_selection_method=planner_selection(planner, engineer, executor, user),
    #     send_introductions=True,
    # )
    # manager = autogen.GroupChatManager(groupchat=group_chat, llm_config=llm_config)
    # group_chat_result = user.initiate_chat(
    #     manager,
    #     message=prompt,
    # )

    # Planner + Engineer + OCMer
    group_chat = autogen.GroupChat(
        agents=[user, engineer, planner, executor, ocmer],
        max_round=50,
        messages=[],
        speaker_selection_method=ocm_selection(
            ocmer, planner, engineer, executor, user
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
        main(sys.argv[1])
    else:
        print("No parameters were provided.")
