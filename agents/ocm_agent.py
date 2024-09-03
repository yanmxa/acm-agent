import autogen

from tools.termination import termination_message
from tools.loader import load_markdowns
from tools.prompt import to_prompt
from prompts.templates import OCM_AGENT_PROMPT


def ocm_agent(llm_config: dict):
    docs = load_markdowns("")
    msg = to_prompt(OCM_AGENT_PROMPT, {"context": docs})

    ocmer = autogen.AssistantAgent(
        name="OCMer",
        is_termination_msg=termination_message,
        human_input_mode="ALWAYS",
        llm_config=llm_config.copy(),
        description="The knowledge repository of OCM(Open Cluster Management) is a valuable resource where you can find solutions and ideas for addressing any multi-cluster issues",
        system_message=msg,
    )
    return ocmer


if __name__ == "__main__":
    docs = load_markdowns("")
    print(to_prompt(OCM_AGENT_PROMPT, {"context": docs}))