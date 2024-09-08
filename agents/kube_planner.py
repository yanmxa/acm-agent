import autogen

from tools import *
from prompt import *


def kube_planner(llm_config: dict):
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

Before drafting the plan, consult the OCM expert (Advisor) for additional details. Use this prompt to request insights:
"Advisor, can you please provide more insights on this issue?" without any additional message.

Based on the information provided by the Advisor, develop a plan consisting of several steps. Each step should represent a potential solution and may involve running a series of kubectl operations on resources in the hub or managed clusters. After executing each step, verify whether the issue is resolved:

- If resolved, report the outcome and mark the step as complete.
- If unresolved, review progress, update the checklist if necessary, and move on to the next step.

**Access Clusters:**

{OCM_KIND_CLUSTER_ACCESS}

Note: Use the method outlined above to specify cluster access in the plan.

**Knowledge of the Multi-cluster(Open Cluster Management)**

{OCM_BASIC_KNOWLEDGE}

Note: This knowledge will help you understand the background when drafting the plan.

Reply "TERMINATE" in the end when everything is done.
""",
    )
    return planner
