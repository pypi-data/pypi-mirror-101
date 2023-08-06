[![NPM version](https://badge.fury.io/js/cdk-apisix.svg)](https://badge.fury.io/js/cdk-apisix)
[![PyPI version](https://badge.fury.io/py/cdk-apisix.svg)](https://badge.fury.io/py/cdk-apisix)
![Release](https://github.com/pahud/cdk-apisix/workflows/Release/badge.svg)

# cdk-apisix

CDK construct library to generate serverless [Apache APISIX](https://github.com/apache/apisix) workload on AWS Fargate

![](images/apisix-fargate-cdk.png)

# sample

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk_apisix import Apisix

# create a standard apisix service
apisix = Apisix(stack, "apisix-demo")

# create a sample webservice with apisix in the same Amazon ECS cluster
apisix.create_web_service("flask",
    environment={
        "PLATFORM": "Apache APISIX on AWS Fargate"
    },
    image=ContainerImage.from_registry("public.ecr.aws/pahudnet/flask-docker-sample")
)
```

## deploy with required context variables

```sh
cdk deploy \
-c ADMIN_KEY_ADMIN=*********** \
-c ADMIN_KEY_VIEWER=*********** \
-c DASHBOARD_ADMIN_PASSWORD=*********** \
-c DASHBOARD_USER_PASSWORD=***********
```

## custom container image from local assets

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
Apisix(stack, "apisix-demo",
    apisix_container=ContainerImage.from_asset(path.join(__dirname, "../apisix_container")),
    dashboard_container=ContainerImage.from_asset(path.join(__dirname, "../apisix_dashboard"))
)
```
