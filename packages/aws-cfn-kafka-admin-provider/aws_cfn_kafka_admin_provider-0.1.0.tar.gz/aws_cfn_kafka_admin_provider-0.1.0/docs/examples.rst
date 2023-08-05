
============
Examples
============

Command line
============

To convert to a CloudFormation template

.. code-block:: bash

    aws-cfn-kafka-admin-provider -f <input_file>


Sample files
=============

Sample file for AWS MSK
------------------------

.. literalinclude:: ../examples/valid_input_custom_msk.yaml
    :language: yaml

Renders, in YAML, into

.. code-block:: yaml

    Description: Kafka topics-acls-schemas root
    Resources:
      newtopic01:
        Properties:
          BootstrapServers: b-1.cluster-demo-01.g02u6o.c1.kafka.eu-west-1.amazonaws.com:9096,b-3.cluster-demo-01.g02u6o.c1.kafka.eu-west-1.amazonaws.com:9096,b-2.cluster-demo-01.g02u6o.c1.kafka.eu-west-1.amazonaws.com:9096
          Name: new-topic-01
          PartitionsCount: 4
          ReplicationFactor: 3
          SASLMechanism: SCRAM-SHA-512
          SASLPassword: '{{resolve:secretsmanager:arn:aws:secretsmanager:eu-west-1:012345678912:secret:AmazonMSK_dummy001-bd9iT7:SecretString:password}}'
          SASLUsername: '{{resolve:secretsmanager:arn:aws:secretsmanager:eu-west-1:012345678912:secret:AmazonMSK_dummy001-bd9iT7:SecretString:username}}'
          SecurityProtocol: SASL_SSL
          ServiceToken: !Sub 'arn:${AWS::Partition}:lambda:${AWS::Region}:${AWS::AccountId}:function:cfn-msk-topic-provider-CustomProviderFunction-JWZXFH0AYOX5'
        Type: Custom::KafkaTopic
      newtopic02:
        Properties:
          BootstrapServers: b-1.cluster-demo-01.g02u6o.c1.kafka.eu-west-1.amazonaws.com:9096,b-3.cluster-demo-01.g02u6o.c1.kafka.eu-west-1.amazonaws.com:9096,b-2.cluster-demo-01.g02u6o.c1.kafka.eu-west-1.amazonaws.com:9096
          Name: new-topic-02
          PartitionsCount: 2
          ReplicationFactor: 3
          SASLMechanism: SCRAM-SHA-512
          SASLPassword: '{{resolve:secretsmanager:arn:aws:secretsmanager:eu-west-1:012345678912:secret:AmazonMSK_dummy001-bd9iT7:SecretString:password}}'
          SASLUsername: '{{resolve:secretsmanager:arn:aws:secretsmanager:eu-west-1:012345678912:secret:AmazonMSK_dummy001-bd9iT7:SecretString:username}}'
          SecurityProtocol: SASL_SSL
          ServiceToken: !Sub 'arn:${AWS::Partition}:lambda:${AWS::Region}:${AWS::AccountId}:function:cfn-msk-topic-provider-CustomProviderFunction-JWZXFH0AYOX5'
        Type: Custom::KafkaTopic

