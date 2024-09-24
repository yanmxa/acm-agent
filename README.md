# ACM Agents

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
curl -L https://raw.githubusercontent.com/open-cluster-management-io/OCM/main/solutions/s
```

## Organize Agents

### Task 1: Interact with the Kubernetes Environment

![agent1](./images/agent1.png)

- User: The user who ask questions and give tasks
- Executor: Execute the code written by the 'Engineer' and report the results back to them
- Engineer: Analyze the intent of the user or planner to write a sequence of shell commands or scripts

#### Demos

- Check the status of `managedclusters`

- Retrieve the resource usage of `kafka` cluster

  <div style="display: flex; gap: 5px;">
    <a href="https://asciinema.org/a/677362" target="_blank">
      <img src="https://asciinema.org/a/677362.svg" style="width: 80%; height: auto;" />
    </a>
  </div>

### Task 2: Add Knowledge Advisor for ACM

![agent2](./images/agent2.png)

- Planner - Kubernetes planner, responsible for making a detailed plan to accomplish a specific task within a Kubernetes environment

- Advisor - The knowledge repository where you can find solutions and ideas for addressing any multi-cluster issues

### Task3: Orchestrate all agents within the system

![agent3](./images/agent3.png)

- Manager - orchestrates the workflow between agents

#### Demo: The Status of Cluster Unknown

- Scenario 1: Cluster1 - Make the bootstrap hub kubeconfig invalid

  ```bash
  # kubectl edit secret bootstrap-hub-kubeconfig -n open-cluster-management-agent --context kind-cluster1
  # kubectl edit secret hub-kubeconfig-secret  -n open-cluster-management-agent --context kind-cluster1

  kubectl delete secret bootstrap-hub-kubeconfig -n open-cluster-management-agent --context kind-cluster1
  kubectl delete secret hub-kubeconfig-secret  -n open-cluster-management-agent --context kind-cluster1
  ```

  ```python
  kubectl get mcl cluster1 --context kind-hub
  python main.py "why the status of cluster1 is unknown?"
  ```

  [![asciicast](https://asciinema.org/a/674162.svg)](https://asciinema.org/a/674162)


- Scenario 2: Disable the `Klusterlet` agent and the `registration` agent

  - Scale these 2 agents to 0

  ```bash
  kubectl scale deployment klusterlet -n open-cluster-management --replicas=0 --context kind-cluster2
  kubectl scale deployment klusterlet-registration-agent -n open-cluster-management-agent --replicas=0 --context kind-cluster2
  ```

  - Troubleshooting the unknown issue

  ```shell
  kubectl get mcl cluster2 --context kind-hub
  python main.py "why the status of cluster2 is unknown"
  ```

  [![asciicast](https://asciinema.org/a/674155.svg)](https://asciinema.org/a/674155)
