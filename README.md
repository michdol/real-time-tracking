# Connecting Edge to Redpanda cluster
Redpanda cluster is run from a bootstrapped docker-compose and Edge FastAPI from separate docker-compose.
To allow Edge connect to the cluster it must be deployed on Redpanda's network.

```
services:
    edge:
        ...
        networks:
          - redpanda-quickstart-multi-broker_redpanda_network

networks:
  redpanda-quickstart-multi-broker_redpanda_network:
    external: true
```

To find network name run:

`docker inspect redpanda-0 --format '{{range $net, $v := .NetworkSettings.Networks}}{{$net}} {{end}}'`


# Tools

## Terraform

`https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli`


