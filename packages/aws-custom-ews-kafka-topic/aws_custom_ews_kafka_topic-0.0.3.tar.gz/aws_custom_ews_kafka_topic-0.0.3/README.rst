=================================
Kafka Topic class for Troposphere
=================================

Lib to represent kafka topic that can then be used with Troposphere

How to use
==========

Install
-------

.. code-block:: bash

    pip install aws_custom_ews_kafka_topic

Deploy via Custom resource (self-managed Lambda)
-------------------------------------------------

.. code-block:: yaml

    from aws_custom_ews_kafka_topic.custom import KafkaTopic

    topic = KafkaTopic(
      ServiceToken=Ref(FunctionArn),
      Name="new-kafka-topic",
      PartitionsCount=6
    )

Deploy via Private Registry resource type
------------------------------------------

.. code-block:: yaml

    from aws_custom_ews_kafka_topic.resource import KafkaTopic

    topic = KafkaTopic(
      Name="new-kafka-topic",
      PartitionsCount=6
    )

Example from CLI
------------------

.. code-block:: bash

    >>> from troposphere import Template
    >>> from aws_custom_ews_kafka_topic.resource import KafkaTopic
    >>> t = KafkaTopic("newtopic", Name="toto", PartitionsCount=6, BootstrapServers="toto.net")
    >>> c = Template()
    >>> c.add_resource(t)
    >>> print(c.to_yaml())
    Resources:
      newtopic:
        Properties:
          BootstrapServers: toto.net
          Name: toto
          PartitionsCount: 6
        Type: EWS::Kafka::Topic


Credits
=======

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
