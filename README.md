# ocm-agents

## Install a Local OCM

```bash
# install clusteradm
curl -L https://raw.githubusercontent.com/open-cluster-management-io/clusteradm/main/install.sh | bash
# create OCM
curl -L https://raw.githubusercontent.com/open-cluster-management-io/OCM/main/solutions/setup-dev-environment/local-up.sh | bash
```

## Multi-Agents for OCM

- Kubernetes Engineer

  ```mermaid
  ---
  title: Standalone Kubernetes Engineer
  ---
  stateDiagram-v2
      Manager --> User
      Manager --> Engineer
      Manager --> Executor
  ```

  Operations on Global Hub and OCM

  <div style="display: flex; gap: 10px;">
  <a href="https://asciinema.org/a/673721" target="_blank">
    <img src="https://asciinema.org/a/673721.svg" alt="asciicast 673721"/>
  </a>
  <a href="https://asciinema.org/a/673715" target="_blank">
    <img src="https://asciinema.org/a/673715.svg" alt="asciicast 673715"/>
  </a>
  </div>

- Multi-Agents for Open Cluster Management

  ```mermaid
  ---
  title: Multi-Agents for Open Cluster Management
  ---
  stateDiagram-v2
      Manager --> User
      Manager --> Engineer
      Manager --> Executor
      Manager --> Planner
      Manager --> OCMer
  ```