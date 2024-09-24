import autogen
import os

from tools import *

current_dir = os.path.dirname(os.path.realpath(__file__))


def kube_planner(llm_config: dict):
    prompt_dir = os.path.join(current_dir, "..", "prompts")
    with open(os.path.join(prompt_dir, "basic_knowledge.txt"), "r") as f:
        basic_knowledge = f.read()
    with open(os.path.join(prompt_dir, "cluster_access.txt"), "r") as f:
        cluster_access = f.read()

    planner = autogen.AssistantAgent(
        name="Planner",
        is_termination_msg=termination_message,
        human_input_mode="ALWAYS",
        llm_config=llm_config.copy(),
        description="Kubernetes planner, responsible for making a detailed plan to accomplish a specific task within a Kubernetes environment",
        system_message=f"""
You are a Kubernetes Planner

**Objective:**

Your task is to create a comprehensive checklist or action plan to address issues or complete tasks related to Kubernetes multi-cluster environments.

Before drafting the plan, consult the Advisor for additional details. Use this prompt to request insights:
"Advisor, can you please provide more insights on this issue?" without any additional message.

Based on the information provided by the Advisor, develop a plan consisting of several steps. Each step should represent a potential solution and may involve running a series of kubectl operations on resources in the hub or managed clusters. After executing each step, verify whether the issue is resolved:

- If resolved, report the outcome and mark the step as complete.
- If unresolved, review progress, update the checklist if necessary, and move on to the next step.
- If you are founding an issue, you can try adding potential fix steps or strategies.

{basic_knowledge}

Note: This above knowledge will help you understand the background when drafting the plan.

{cluster_access}

Note: Use the method outlined above to specify cluster access in the plan.


Reply "TERMINATE" in the end when everything is done.
""",
    )
    return planner
