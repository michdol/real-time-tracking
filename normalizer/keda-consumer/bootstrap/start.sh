#!/bin/bash
set -euo pipefail

CLUSTER="${K3D_CLUSTER:-rtt}"
KEDA_VERSION="${KEDA_VERSION:-2.16.1}"

if [[ ! -f /work/normalizer/keda-consumer/Dockerfile ]]; then
  echo "consumer Dockerfile is not mounted at /work/normalizer/keda-consumer" >&2
  exit 1
fi

if ! docker image inspect keda-consumer:local >/dev/null 2>&1; then
  echo "keda-consumer:local is missing; run docker compose build keda-consumer" >&2
  exit 1
fi

if ! k3d cluster list | awk 'NR>1 {print $1}' | grep -qx "${CLUSTER}"; then
  echo "creating k3d cluster ${CLUSTER}"
  k3d cluster create "${CLUSTER}" --agents 0 --wait --api-port 127.0.0.1:6550
fi

k3d kubeconfig get "${CLUSTER}" > /tmp/kubeconfig.yaml
sed -i -E 's#https://(127\.0\.0\.1|0\.0\.0\.0):#https://host.docker.internal:#' /tmp/kubeconfig.yaml
export KUBECONFIG=/tmp/kubeconfig.yaml
cluster_name="$(kubectl config view -o jsonpath='{.clusters[0].name}')"
kubectl config set-cluster "${cluster_name}" --tls-server-name=localhost
mkdir -p /root/.kube
cp /tmp/kubeconfig.yaml /root/.kube/config

kubectl wait --for=condition=Ready node --all --timeout=180s

REDPANDA_NETWORK="${REDPANDA_NETWORK:-redpanda-quickstart-multi-broker_redpanda_network}"
node="k3d-${CLUSTER}-server-0"
if ! docker inspect "${node}" --format '{{json .NetworkSettings.Networks}}' | grep -q "\"${REDPANDA_NETWORK}\""; then
  echo "connecting ${node} to ${REDPANDA_NETWORK}"
  docker network connect "${REDPANDA_NETWORK}" "${node}"
fi

server="$(mktemp)"
{
  echo "redpanda-0 redpanda-1 redpanda-2 {"
  echo "  hosts {"
  found=0
  for name in redpanda-0 redpanda-1 redpanda-2; do
    ip="$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' "${name}" 2>/dev/null || true)"
    if [[ -n "${ip}" ]]; then
      echo "    ${ip} ${name}"
      found=1
    fi
  done
  echo "    fallthrough"
  echo "  }"
  echo "}"
} > "${server}"
if [[ "${found}" -ne 1 ]]; then
  echo "no redpanda brokers found" >&2
  exit 1
fi

kubectl -n kube-system create configmap coredns-custom \
  --from-file="redpanda.server=${server}" \
  --dry-run=client -o yaml | kubectl apply -f -
kubectl -n kube-system rollout restart deploy/coredns
kubectl -n kube-system rollout status deploy/coredns --timeout=180s
rm -f "${server}"

if ! kubectl get crd scaledobjects.keda.sh >/dev/null 2>&1; then
  kubectl apply --server-side -f "https://github.com/kedacore/keda/releases/download/v${KEDA_VERSION}/keda-${KEDA_VERSION}.yaml"
fi
kubectl -n keda rollout status deploy/keda-operator --timeout=180s
kubectl -n keda rollout status deploy/keda-metrics-apiserver --timeout=180s

echo "importing keda-consumer:local into ${CLUSTER}"
k3d image import keda-consumer:local -c "${CLUSTER}"

kubectl apply -f /work/normalizer/keda-consumer/k8s/secret.yaml
kubectl apply -f /work/normalizer/keda-consumer/k8s/deployment.yaml
kubectl apply -f /work/normalizer/keda-consumer/k8s/scaledobject.yaml
kubectl rollout status deploy/kafka-consumer --timeout=180s

echo "kafka-consumer is running; KEDA keeps it between 1 and 4 replicas"
sleep infinity
