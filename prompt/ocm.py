OCM_KIND_CLUSTER_ACCESS = """
You can interact with all clusters (hub and managed) using the `KUBECONFIG` environment variable by switching contexts to access different clusters.

Each of these clusters is created using KinD. To access the hub cluster, use the `kind-hub` context.

For managed clusters, switch to the corresponding context in the format `kind-<ManagedCluster>`. For example, to retrieve all pods on `cluster1`, use the following command:

```bash
kubectl get pods -A --context kind-cluster1
```
"""

OCM_BASIC_KNOWLEDGE = """
1. The cluster that manages other clusters is referred to as the hub cluster. It includes the following customized resources and controllers:

  - `ClusterManager` (Global Resource): This resource configures the hub and is reconciled by the `cluster-manager` controller in the `open-cluster-management` namespace by default. The `cluster-manager` watches the `ClusterManager` resource and installs other components in the `open-cluster-management-hub` namespace, including the `addon-manager`, `placement`, `registration`, and `work` controllers.
  
  - `registration`: This component is responsible for registering managed clusters with the hub. It consists of the `cluster-manager-registration-controller` and the `cluster-manager-registration-webhook`, which watches the `CSR` and `ManagedCluster` resources for the managed cluster.
  
  - `addon-manager`: The `cluster-manager-addon-manager-controller` watches the global `ClusterManagementAddon` resource and the namespaced `ManagedClusterAddon` resource. The `ClusterManagementAddon` represents an addon application for the multi-cluster system. The `ManagedClusterAddon` is associated with a specific managed cluster and exists in the cluster namespace, indicating that the addon has been scheduled to that cluster. A single `ClusterManagementAddon` can correspond to multiple `ManagedClusterAddon` instances.
  
  - Placement: This component schedules workloads to target managed clusters. The `cluster-manager-placement-controller` monitors the namespaced `Placement` resource and produces scheduling decisions in the `PlacementDecision` resource.
  
  - Work: The `cluster-manager-work-webhook` controller/webhook manages the `ManifestWork` resource, which encapsulates Kubernetes resources.
  
2. The clusters managed by the hub are represented by the custom resource `ManagedCluster` (abbreviated as mcl and global in scope) within the hub cluster. You can list the clusters currently managed by the hub using `kubectl get mcl` in the hub cluster. The following components are present in the managed cluster:

  - Klusterlet: The `klusterlet` controller in the `open-cluster-management` namespace monitors the global `Klusterlet` resource and installs other controllers such as the `klusterlet-registration-agent` and `klusterlet-work-agent`.
  
  - `klusterlet-registration-agent`: Located in the managed cluster, this agent creates the `CSR` in the hub cluster and monitors/updates the heartbeat(lease) of the `ManagedCluster` in the hub cluster.
  
  - `klusterlet-work-agent`: Also located in the managed cluster, this agent monitors the `ManifestWork` of its namespace in the hub cluster and applies it to the local cluster (the managed cluster). It also updates the `ManifestWork` status in the hub cluster.
"""
