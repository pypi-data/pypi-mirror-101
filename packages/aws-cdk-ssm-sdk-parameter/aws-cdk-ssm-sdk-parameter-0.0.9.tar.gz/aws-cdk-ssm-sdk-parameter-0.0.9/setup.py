import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "aws-cdk-ssm-sdk-parameter",
    "version": "0.0.9",
    "description": "aws-cdk-ssm-sdk-parameter",
    "license": "Apache-2.0",
    "url": "https://github.com/mmuller88/aws-cdk-ssm-sdk-parameter",
    "long_description_content_type": "text/markdown",
    "author": "martin.mueller<damadden88@googlemail.de>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/mmuller88/aws-cdk-ssm-sdk-parameter"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "aws_cdk_ssm_sdk_parameter",
        "aws_cdk_ssm_sdk_parameter._jsii"
    ],
    "package_data": {
        "aws_cdk_ssm_sdk_parameter._jsii": [
            "aws-cdk-ssm-sdk-parameter@0.0.9.jsii.tgz"
        ],
        "aws_cdk_ssm_sdk_parameter": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.aws-cloudformation==1.80.0",
        "aws-cdk.aws-iam==1.80.0",
        "aws-cdk.aws-lambda==1.80.0",
        "aws-cdk.cloud-assembly-schema==1.80.0",
        "aws-cdk.core==1.80.0",
        "aws-cdk.custom-resources==1.80.0",
        "constructs>=3.2.27, <4.0.0",
        "jsii>=1.16.0, <2.0.0",
        "publication>=0.0.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ]
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
