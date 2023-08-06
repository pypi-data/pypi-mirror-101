.. meta::
    :description: Kafka admin via AWS CloudFormation
    :keywords: AWS, CloudFormation, Kafka, Confluent

=====
Usage
=====

As CLI
-------

.. code-block:: bash


    aws-cfn-kafka-admin-provider --help
    usage: aws-cfn-kafka-admin-provider [-h] -f FILE_PATH [-o OUTPUT_FILE] [--format {json,yaml}] [_ ...]

    positional arguments:
      _

    optional arguments:
      -h, --help            show this help message and exit
      -f FILE_PATH, --file-path FILE_PATH
                            Path to the kafka definition file
      -o OUTPUT_FILE, --output-file OUTPUT_FILE
                            Path to file output
      --format {json,yaml}  Template format


As lib
-------

.. code-block:: python

    from aws_cfn_kafka_admin_provider.aws_cfn_kafka_admin_provider import KafkaStack

    stack = KafkaStack("/path/to/input/file.yaml")
    stack.render_topics()

