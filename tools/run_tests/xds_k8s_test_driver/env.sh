export PROJECT_ID="ginayeh-testing"
export PROJECT_NUMBER=$(gcloud projects describe "${PROJECT_ID}" --format="value(projectNumber)")
# Compute Engine default service account
export GCE_SA="${PROJECT_NUMBER}-compute@developer.gserviceaccount.com"
# The prefix to name GCP resources used by the framework
export RESOURCE_PREFIX="xds-k8s-interop-tests"

# The zone name your cluster, f.e. xds-k8s-test-cluster
export CLUSTER_NAME="${RESOURCE_PREFIX}-cluster"
# The zone of your cluster, f.e. us-central1-a
export ZONE="us-central1-b" 
# Dedicated GCP Service Account to use with workload identity.
export WORKLOAD_SA_NAME="${RESOURCE_PREFIX}"
export WORKLOAD_SA_EMAIL="${WORKLOAD_SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"
