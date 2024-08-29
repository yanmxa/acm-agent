import autogen


# https://microsoft.github.io/autogen/docs/notebooks/agentchat_groupchat_customized
def engineer_selection(
    engineer: autogen.Agent, executor: autogen.Agent, user: autogen.Agent
):
    def custom_speaker_selection_func(
        last_speaker: autogen.Agent, groupchat: autogen.GroupChat
    ):
        """Define a customized speaker selection function.
        A recommended way is to define a transition for each speaker in the groupchat.

        Returns:
            Return an `Agent` class or a string from ['auto', 'manual', 'random', 'round_robin'] to select a default method to use.
        """
        messages = groupchat.messages

        if last_speaker == engineer:
            if "```" in messages[-1]["content"]:
                return executor
            else:
                return engineer
        elif last_speaker == executor:
            return engineer
        elif last_speaker == user:
            return engineer
        else:
            return "auto"

    return custom_speaker_selection_func


def planner_selection(
    planner: autogen.Agent,
    engineer: autogen.Agent,
    executor: autogen.Agent,
    user: autogen.Agent,
):
    def custom_speaker_selection_func(last_speaker, groupchat):
        content = groupchat.messages[-1]["content"]

        if last_speaker == planner:
            return user if "TERMINATE" in content else engineer
        elif last_speaker == engineer:
            return executor if "```" in content else planner
        elif last_speaker == executor:
            return engineer
        elif last_speaker == user:
            return planner
        return "auto"

    return custom_speaker_selection_func


def ocm_selection(
    ocmer: autogen.Agent,
    planner: autogen.Agent,
    engineer: autogen.Agent,
    executor: autogen.Agent,
    user: autogen.Agent,
):
    def custom_speaker_selection_func(last_speaker, groupchat):
        content = groupchat.messages[-1]["content"]

        if last_speaker == planner:
            if "TERMINATE" in content:
                return user
            elif "OCMer" in content:
                return ocmer
            else:
                return engineer
        elif last_speaker == engineer:
            return executor if "```" in content else planner
        elif last_speaker == executor:
            return engineer
        elif last_speaker == user:
            return planner
        return "auto"

    return custom_speaker_selection_func
