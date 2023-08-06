[![cloudcomponents Logo](https://raw.githubusercontent.com/cloudcomponents/cdk-constructs/master/logo.png)](https://github.com/cloudcomponents/cdk-constructs)

# @cloudcomponents/cdk-stripe-webhook

[![Build Status](https://github.com/cloudcomponents/cdk-constructs/workflows/Build/badge.svg)](https://github.com/cloudcomponents/cdk-constructs/actions?query=workflow=Build)
[![cdkdx](https://img.shields.io/badge/buildtool-cdkdx-blue.svg)](https://github.com/hupe1980/cdkdx)
[![typescript](https://img.shields.io/badge/jsii-typescript-blueviolet.svg)](https://www.npmjs.com/package/@cloudcomponents/cdk-stripe-webhook)
[![python](https://img.shields.io/badge/jsii-python-blueviolet.svg)](https://pypi.org/project/cloudcomponents.cdk-stripe-webhook/)

> Create, update and delete stripe webhooks with your app deployment

## Install

TypeScript/JavaScript:

```bash
npm i @cloudcomponents/cdk-stripe-webhook
```

Python:

```bash
pip install cloudcomponents.cdk-stripe-webhook
```

## How to use

### EventBus Producer

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_cdk.aws_ssm import StringParameter
from aws_cdk.core import Construct, Stack, StackProps
from cloudcomponents.cdk_secret_key import SecretKey, SecretKeyStore
from cloudcomponents.cdk_stripe_webhook import StripeWebhook, StripeEventBusProducer

class StripeWebhookStack(Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)

        secret_key = SecretKey.from_plain_text(process.env.SECRET_KEY)

        endpoint_secret_parameter = StringParameter.from_secure_string_parameter_attributes(self, "Param",
            parameter_name="stripe",
            version=1
        )

        producer = StripeEventBusProducer(self, "Producer",
            secret_key=secret_key,
            endpoint_secret=SecretKey.from_sSMParameter(endpoint_secret_parameter)
        )

        events = ["charge.failed", "charge.succeeded"]

        endpoint_secret_store = SecretKeyStore.from_sSMParameter(endpoint_secret_parameter)

        StripeWebhook(self, "StripeWebhook",
            secret_key=secret_key,
            url=producer.url,
            events=events,
            log_level="debug",
            endpoint_secret_store=endpoint_secret_store
        )
```

### Custom Handler

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_cdk.aws_apigateway import RestApi
from aws_cdk.core import Construct, Stack, StackProps
from cloudcomponents.cdk_secret_key import SecretKey
from cloudcomponents.cdk_stripe_webhook import StripeWebhook
class StripeWebhookStack(Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)

        api = RestApi(self, "Endpoint")
        api.root.add_method("POST")

        secret_key = SecretKey.from_plain_text(process.env.SECRET_KEY)

        events = ["charge.failed", "charge.succeeded"]

        StripeWebhook(self, "StripeWebhook",
            secret_key=secret_key,
            url=api.url,
            events=events,
            log_level="debug"
        )
```

## API Reference

See [API.md](https://github.com/cloudcomponents/cdk-constructs/tree/master/packages/cdk-stripe-webhook/API.md).

## Example

See more complete [examples](https://github.com/cloudcomponents/cdk-constructs/tree/master/examples).

## License

[MIT](https://github.com/cloudcomponents/cdk-constructs/tree/master/packages/cdk-stripe-webhook/LICENSE)
