"""
[![NPM version](https://badge.fury.io/js/aws-cdk-ssm-sdk-parameter.svg)](https://badge.fury.io/js/aws-cdk-ssm-sdk-parameter)
[![PyPI version](https://badge.fury.io/py/aws-cdk-ssm-sdk-parameter.svg)](https://badge.fury.io/py/aws-cdk-ssm-sdk-parameter)
![Release](https://github.com/mmuller88/aws-cdk-ssm-sdk-parameter/workflows/Release/badge.svg)

# aws-cdk-ssm-sdk-parameter

Thats an AWS CDK Construct for get and set the value of an SSM parameter. It is designed to be loose coupled and be not managed through AWS CDK / Cloudformation so that the SSM parameter can exist across different stacks and be updated without causing a drift. The looseness is reached through using CFN Custom Resources.

The implementation simply leverages [AwsCustomResource](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_custom-resources.AwsCustomResource.html) as an SDK wrapper for:

* https://awscli.amazonaws.com/v2/documentation/api/latest/reference/ssm/get-parameter.html https://docs.aws.amazon.com/systems-manager/latest/APIReference/API_GetParameter.html
* https://awscli.amazonaws.com/v2/documentation/api/latest/reference/ssm/put-parameter.html https://docs.aws.amazon.com/systems-manager/latest/APIReference/API_PutParameter.html
* https://awscli.amazonaws.com/v2/documentation/api/latest/reference/ssm/delete-parameter.html https://docs.aws.amazon.com/systems-manager/latest/APIReference/API_DeleteParameter.html

# Features

* If the parameter doesn't exist, it will be created. Otherwise it pulls the current value of the parameter.
* optional delete when destroying the stack

# Use Case

Initialize a parameter to some value upon creation, but allow it to diverge during future CDK deployments.

SSM StringParameter APP_VERSION of an image is used across ECS deployments. New ECS deployments use that latest version value in it. APP_VERSION isn't managed / editable with CDK but if APP_VERSION wouldn't exist you can specify kind of default.

# Example

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
stack = cdk.Stack(app, "ssm-demo-stack", env=env)

# Create a loose coupled SSM Parameter from type String
SSMParameter(stack, "SSMParameter",
    parameter_name="fooString",
    default_value="fooValue"
)

# Create a loose coupled SSM Parameter from type StringList
SSMParameter(stack, "SSMParameterStringList",
    parameter_name="fooStringList",
    default_value="fooValue1,fooValue2,fooValue3",
    type=SSMParameterType.StringList
)

# Delete the SSM Parameter if the stack gets deleted
SSMParameter(stack, "SSMParameterWithDelete",
    parameter_name="fooWithDelete",
    default_value="fooValue",
    delete=True
)
```

# Local Testing

For local testing simply run

```
yarn deploy --profile X
```

For destroying use

```
yarn destroy --profile X
```

# Limitation

* SSM SecureString Parameter are not supported
* default description are not supported
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.core


class SSMParameter(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-ssm-sdk-parameter.SSMParameter",
):
    def __init__(
        self,
        parent: aws_cdk.core.Stack,
        name: builtins.str,
        *,
        parameter_name: builtins.str,
        default_value: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.bool] = None,
        type: typing.Optional["SSMParameterType"] = None,
    ) -> None:
        """
        :param parent: -
        :param name: -
        :param parameter_name: 
        :param default_value: if the parameter couldn't be found that will be the default value.
        :param delete: Optional parameter for deleting the SSM Parameter if the stack gets deleted. Default: false
        :param type: The SSM Parameter type. SecureString is atm not supported
        """
        props = SSMParameterProps(
            parameter_name=parameter_name,
            default_value=default_value,
            delete=delete,
            type=type,
        )

        jsii.create(SSMParameter, self, [parent, name, props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="parameterName")
    def parameter_name(self) -> builtins.str:
        return jsii.get(self, "parameterName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="parameterValue")
    def parameter_value(self) -> builtins.str:
        """the returned parameter for the SSM Parameter."""
        return jsii.get(self, "parameterValue")


@jsii.data_type(
    jsii_type="aws-cdk-ssm-sdk-parameter.SSMParameterProps",
    jsii_struct_bases=[],
    name_mapping={
        "parameter_name": "parameterName",
        "default_value": "defaultValue",
        "delete": "delete",
        "type": "type",
    },
)
class SSMParameterProps:
    def __init__(
        self,
        *,
        parameter_name: builtins.str,
        default_value: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.bool] = None,
        type: typing.Optional["SSMParameterType"] = None,
    ) -> None:
        """
        :param parameter_name: 
        :param default_value: if the parameter couldn't be found that will be the default value.
        :param delete: Optional parameter for deleting the SSM Parameter if the stack gets deleted. Default: false
        :param type: The SSM Parameter type. SecureString is atm not supported
        """
        self._values: typing.Dict[str, typing.Any] = {
            "parameter_name": parameter_name,
        }
        if default_value is not None:
            self._values["default_value"] = default_value
        if delete is not None:
            self._values["delete"] = delete
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def parameter_name(self) -> builtins.str:
        result = self._values.get("parameter_name")
        assert result is not None, "Required property 'parameter_name' is missing"
        return result

    @builtins.property
    def default_value(self) -> typing.Optional[builtins.str]:
        """if the parameter couldn't be found that will be the default value."""
        result = self._values.get("default_value")
        return result

    @builtins.property
    def delete(self) -> typing.Optional[builtins.bool]:
        """Optional parameter for deleting the SSM Parameter if the stack gets deleted.

        :default: false
        """
        result = self._values.get("delete")
        return result

    @builtins.property
    def type(self) -> typing.Optional["SSMParameterType"]:
        """The SSM Parameter type.

        SecureString is atm not supported
        """
        result = self._values.get("type")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SSMParameterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="aws-cdk-ssm-sdk-parameter.SSMParameterType")
class SSMParameterType(enum.Enum):
    """The SSM Parameter type.

    SecureString is atm not supported
    """

    STRING = "STRING"
    STRING_LIST = "STRING_LIST"


__all__ = [
    "SSMParameter",
    "SSMParameterProps",
    "SSMParameterType",
]

publication.publish()
