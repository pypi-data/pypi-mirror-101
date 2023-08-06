Getting started
===============

AWS simple pipeline package is implemented for deploying a Continuous Deployment or Delivery system (CD) by AWS CodePipeline service.

You can use this simple pipeline for deploying your personal solution in 2 environments: staging and production.

It is part of the `educational repositories <https://github.com/pandle/materials>`_ to learn how to write stardard code and common uses of the TDD, CI and CD.

Prerequisites
#############

You have to install the `AWS Cloud Development Kit <https://docs.aws.amazon.com/cdk/latest/guide/>`_ (AWS CDK) for deploying the AWS simple pipeline:

.. code-block:: bash

    npm install -g aws-cdk # for installing AWS CDK
    cdk --help # for printing its commands

And you need an AWS account, in this repository called **your-account**.

Installation
############

The package is not self-consistent. So you have to download the package by github and to install the requirements before to deploy on AWS:

.. code-block:: bash

    git clone https://github.com/bilardi/aws-simple-pipeline
    cd aws-simple-pipeline/
    pip3 install --upgrade -r requirements.txt
    export AWS_PROFILE=your-account
    cdk deploy

Or if you want to use this package into your code, you can install by python3-pip:

.. code-block:: bash

    pip3 install aws_simple_pipeline
    python3
    >>> import aws_simple_pipeline
    >>> help(aws_simple_pipeline)

Read the documentation on `readthedocs <https://aws-simple-pipeline.readthedocs.io/en/latest/>`_ for

* Usage
* Development

Change Log
##########

See `CHANGELOG.md <https://github.com/bilardi/aws-simple-pipeline/blob/master/CHANGELOG.md>`_ for details.

License
#######

This package is released under the MIT license.  See `LICENSE <https://github.com/bilardi/aws-simple-pipeline/blob/master/LICENSE>`_ for details.
