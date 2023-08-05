======================================
AWS CFN Custom resource Resolve parser
======================================


.. image:: https://img.shields.io/pypi/v/aws_cfn_custom_resource_resolve_parser.svg
        :target: https://pypi.python.org/pypi/aws_cfn_custom_resource_resolve_parser

.. image:: https://readthedocs.org/projects/aws-cfn-custom-resource-resolve-parser/badge/?version=latest
        :target: https://aws-cfn-custom-resource-resolve-parser.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status


----------------------------------------------------------------------------------------------------
Small lib to parse and retrieve secret from AWS Secrets manager using the CFN resolve format string
----------------------------------------------------------------------------------------------------

Intent
=======

Currently in AWS CloudFormation, using **{{resolve}}** does not work for custom resources. Pending the feature being
released, when the use of private resource types is not possible for the use-case, this small lib aims to allow
parsing secrets so that you can today write your CFN templates with resolve.

Requirements
=============

Sadly, this means the lambda function using this library will still need IAM access directly, and cannot use the role
used by CloudFormation on create/update currently.

Usage
=======

.. code-block:: python

    from aws_cfn_custom_resource_resolve_parser import handle
    secret_string = r"{{resolve:secretsmanager:mysecret:SecretString:password}}"
    secret_value = handle(secret_string)


* Documentation: https://aws-cfn-custom-resource-resolve-parser.readthedocs.io.

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
