import os
from typing import Dict, List, Optional, Tuple, Union
import warnings

import autogen
from autogen.agentchat import Agent, ConversableAgent
from autogen import OpenAIWrapper
from txtai.embeddings import Embeddings

from tools import *

warnings.filterwarnings("ignore")

current_dir = os.path.dirname(os.path.realpath(__file__))


class AdvisorAgent(ConversableAgent):

    def __init__(
        self,
        name: str,
        description: Optional[str] = None,
        **kwargs,
    ):
        """
        Args:
            name (str): agent name.
            description (str): a short description of the agent. This description is used by other agents
                (e.g. the GroupChatManager) to decide when to call upon this agent.
            **kwargs (dict): Please refer to other kwargs in
                [ConversableAgent](../conversable_agent#__init__).
        """

        super().__init__(
            name,
            description=description,
            **kwargs,
        )

        self.embeddings = Embeddings(
            path="sentence-transformers/all-MiniLM-L6-v2",
        )

        self.documents = self._get_documents(
            os.path.join(current_dir, "..", "runbooks")
        )

        # export OMP_NUM_THREADS=1
        self.embeddings.index(self.documents)

        # Override the `generate_oai_reply`
        self.replace_reply_func(
            ConversableAgent.generate_oai_reply,
            AdvisorAgent._generate_oai_reply,
        )

        self.replace_reply_func(
            ConversableAgent.a_generate_oai_reply,
            AdvisorAgent._a_generate_oai_reply,
        )

    def _generate_oai_reply(
        self,
        messages: Optional[List[Dict]] = None,
        sender: Optional[Agent] = None,
        config: Optional[OpenAIWrapper] = None,
    ) -> Tuple[bool, Union[str, Dict, None]]:
        """Generate a reply using autogen.oai."""

        if not messages:
            return (True, "")

        user_msgs = [msg for msg in messages if msg.get("name") == "User"]
        message = user_msgs[-1].get("content", "")  # get the last user message content
        # history = messages[:-1]

        return (True, self._search(message))

    async def _a_generate_oai_reply(
        self,
        messages: Optional[List[Dict]] = None,
        sender: Optional[Agent] = None,
        config: Optional[OpenAIWrapper] = None,
    ) -> Tuple[bool, Union[str, Dict, None]]:
        """Generate a reply using autogen.oai."""

        if not messages:
            return (True, "")

        user_msgs = [msg for msg in messages if msg.get("name") == "User"]
        message = user_msgs[-1].get("content", "")

        return (True, self._search(message))

    def _get_documents(self, run_book_dir):
        all_files = list_files(run_book_dir, "md")
        documents = []
        i = 0
        for file in all_files:
            with open(file, "r") as f:
                content = f.read()
                title, desc = extract_title_and_description(content)
                documents.append((i, f"""Title: {title}\n Description: {desc}""", file))
                # documents.append((i, title, file))
                i = i + 1
        return documents

    def _search(self, message):
        results = self.embeddings.search(message, 2)
        for item in results:
            file = self.documents[item[0]][2]
            print(f"Knowledge found with a score of: {item}\nFile: {file} \n")
            raw_content = ""
            with open(file, "r") as f:
                raw_content = f.read()
        return raw_content


def advisor_agent():
    advisor = AdvisorAgent(
        name="Advisor",
        is_termination_msg=termination_message,
        human_input_mode="ALWAYS",
        description="The knowledge repository where you can find run-books and ideas for addressing any multi-cluster issues",
    )
    return advisor
