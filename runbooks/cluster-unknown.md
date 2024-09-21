# The Status of Cluster(ManagedCluster) Is Unknown

## Description

The ManagedCluster on the hub cluster has a condition of type `ManagedClusterConditionAvailable` with a `status` of `Unknown`.
You are able to check the status of this condition with command line below,

```bash
oc get managedcluster <cluster-name> -o jsonpath='{.status.conditions[?(@.type=="ManagedClusterConditionAvailable")]}' --context <hub-cluster-context>
```

## Meaning

When the klusterlet registration agent starts running on the managed cluster, it updates a Lease resource in the cluster namespace on the hub cluster every `N` seconds, where `N` is configured in the `spec.leaseDurationSeconds` of the `ManagedCluster`. If the Lease resource is not updated in the past `5 * N` seconds, the `status` of the `ManagedClusterConditionAvailable` condition for this managed cluster will be set to `Unknown`. Once the klusterlet registration agent connects back to the hub cluster and continues to update the Lease resource, the `ManagedCluster` will become available automatically.

## Impact

Once this issue happens,

- Usually both the `klusterlet` agent and add-on agents cannot connect to the hub cluster. Changes on `ManifestWorks` and other add-on specific resources on the hub cluster can not be pulled to the managed cluster;

- The status of the `Available` condition of all ManagedClusterAddOns for this managed cluster will be set to `Unknown` as well;

## Diagnosis 

The diagnostic instructions may follow two paths: klusterlet resources and controllers

### klusterlet resources

(1) check the resource on the managed cluster

```bash
# Klusterlet CR
oc get klusterlet klusterlet --context <managed-cluster-context>

# Klusterlet operator
oc -n open-cluster-management get deploy klusterlet --context <managed-cluster-context>
```

If any of the above resources is missing, that means the cluster isn't joining to hub cluster. And you can try to join the cluster to hub.

If they all exists, check the status of the klusterlet

(2) check the status of klusterlet on the managed cluster

```bash
oc get klusterlet klusterlet --context <managed-cluster-context>  -oyaml
```

The status maybe contain the information why the klusterlet registration agent (`deploy/klusterlet-registration-agent -n open-cluster-management-agent`) cann't update the cluster lease in the hub. 

A common issue is an invalid `hub-kubeconfig-secret` used to connect to the hub cluster. However, it's essential to first identify the root cause when the Klusterlet registration and Klusterlet agent are not functioning as expected.

If there are no obvious error in the klusterlet status, consider other potential causes for the unknown status.

### klusterlet controllers

The klusterlet agent (`deploy/klusterlet -n open-cluster-management`), reconciles the Klusterlet CR(klusterlet), and is responsible for creating the klusterlet registration agent (`deploy/klusterlet-registration-agent -n open-cluster-management-agent`), which updates the cluster lease on the hub cluster.

(1) Check if the existence of the klusterlet registration agent below on the managed cluster.

```bash
# get the deployment
oc -n open-cluster-management-agent get deploy/klusterlet-registration-agent --context <managed-cluster-context>
# get the pods instance
oc -n open-cluster-management-agent get pods -l app=klusterlet-registration-agent --context <managed-cluster-context>
```

If the pod instance is present, review its logs to see if any errors are preventing the creation of the klusterlet registration agent.

(2) Check the log of the klusterlet registration agent if it exists

```bash
oc -n open-cluster-management-agent logs -l app=klusterlet-registration-agent --context <managed-cluster-context>
```

If the `klusterlet-registration-agent` deployment is not found, then go to the next step to check the klusterlet agent instance. Which is responsible to create the klusterlet registration agent!

(3) Check the klusterlet agent instance

```bash
# the deployment
oc -n open-cluster-management get deploy/klusterlet --context <managed-cluster-context>

# the pods 
oc -n open-cluster-management get pod -l app=klusterlet --context <managed-cluster-context>
```

If the klusterlet agent pod isn't running, then you can check the deployment detail to summarize why it isn't running and return the reason caused unknown status. 

If the klusterlet agent pod is running, check the logs of the klusterlet agent

(4) Check the klusterlet agent log on the managed cluster.

```bash
oc -n open-cluster-management logs -l app=klusterlet --context <managed-cluster-context>
```

If the klusterlet agent is running and no errors are found in the klusterlet agent log, consider other potential causes for the unknown status.