# ACM Agent

This is a multi-agent system for troubleshooting Kubernetes applications. Its initial implementation focuses on diagnosing the Open (or Advanced) Cluster Management environment, but it can be customized for other products as well.

## Environment

We set up an Open Cluster Management environment to demonstrate how it works.

- [Installation](https://open-cluster-management.io/docs/getting-started/quick-start/)

Install clusteradm CLI tool
Run the following command to download and install the latest clusteradm command-line tool:

```bash
curl -L https://raw.githubusercontent.com/open-cluster-management-io/clusteradm/main/install.sh | bash
```

Setup hub and managed cluster
Run the following command to quickly setup a hub cluster and 2 managed clusters by kind.

```bash
curl -L https://raw.githubusercontent.com/open-cluster-management-io/OCM/main/solutions/setup-dev-environment/local-up.sh | bash
```

## Organize Agents

### Task 1: Interact with the Kubernetes Environment

![agent1](./images/agent1.png)

- User: The user who ask questions and give tasks
- Executor: Execute the code written by the 'Engineer' and report the results back to them
- Engineer: Analyze the intent of the user or planner to write a sequence of shell commands or scripts

### Task 2: Add Knowledge Advisor for ACM

![agent2](./images/agent2.png)

- Planner - Kubernetes planner, responsible for making a detailed plan to accomplish a specific task within a Kubernetes environment

- Advisor - The knowledge repository where you can find solutions and ideas for addressing any multi-cluster issues

### Task3: Orchestrate all agents within the system

![agent3](./images/agent3.png)

- Manager - orchestrates the workflow between agents

#### Demo: Cluster Unknown

[![Watch the demo](https://asciinema.org/a/687993.svg)](https://asciinema.org/a/687993)

#### Addons Aren't Created

[![Watch the demo](https://asciinema.org/a/689439.svg)](https://asciinema.org/a/689439)
