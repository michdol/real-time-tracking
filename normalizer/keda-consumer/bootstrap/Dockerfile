FROM docker:27-cli

RUN apk add --no-cache bash ca-certificates curl

ARG K3D_VERSION=v5.8.3
ARG KUBECTL_VERSION=v1.31.4

RUN arch="$(uname -m)"; \
    case "$arch" in \
      x86_64) target=amd64 ;; \
      aarch64) target=arm64 ;; \
      *) echo "unsupported architecture: $arch" >&2; exit 1 ;; \
    esac; \
    curl -fsSL -o /usr/local/bin/k3d "https://github.com/k3d-io/k3d/releases/download/${K3D_VERSION}/k3d-linux-${target}"; \
    curl -fsSL -o /usr/local/bin/kubectl "https://dl.k8s.io/release/${KUBECTL_VERSION}/bin/linux/${target}/kubectl"; \
    chmod +x /usr/local/bin/k3d /usr/local/bin/kubectl

COPY start.sh /start.sh
RUN chmod +x /start.sh

ENTRYPOINT ["bash", "/start.sh"]
