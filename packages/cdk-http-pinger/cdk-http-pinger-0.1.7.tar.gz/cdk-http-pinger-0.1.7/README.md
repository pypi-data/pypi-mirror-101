[![NPM version](https://badge.fury.io/js/cdk-http-pinger.svg)](https://badge.fury.io/js/cdk-http-pinger)
[![PyPI version](https://badge.fury.io/py/cdk-http-pinger.svg)](https://badge.fury.io/py/cdk-http-pinger)
![Release](https://github.com/pahud/cdk-http-pinger/workflows/Release/badge.svg?branch=main)

# `cdk-http-pinger`

HTTP Pinger for AWS CDK

# Sample

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk_http_pinger import Pinger

app = App()

stack = Stack(app, "my-stack")

pinger = Pinger(stack, "Pinger", url="https://aws.amazon.com")

CfnOutput(stack, "HttpStatus", value=pinger.http_status)
CfnOutput(stack, "HtmlTitle", value=pinger.html_title)
CfnOutput(stack, "URL", value=pinger.url)
CfnOutput(stack, "Body", value=pinger.body)
```
