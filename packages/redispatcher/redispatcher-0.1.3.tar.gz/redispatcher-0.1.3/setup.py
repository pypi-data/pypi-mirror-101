# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['redispatcher']

package_data = \
{'': ['*']}

install_requires = \
['aioredis>=1.3.1,<2.0.0', 'isort>=5.8.0,<6.0.0', 'pydantic>=1.8.1,<2.0.0']

setup_kwargs = {
    'name': 'redispatcher',
    'version': '0.1.3',
    'description': 'Toolset for asynchronous message processing backed by Redis as the message broker',
    'long_description': '# redispatcher\n\nredispatcher is a small library that allows you to specify a pool of workers that listen to messages added to queues in Redis. This allows you to execute long running background tasks asynchronously, like sending a welcome email after a user registers.\n\nredispatcher relies on\n* `aioredis` to publish to Redis queues and for your consumers to read from Redis\n* `pydantic` to validate all messages and make sure they conform to the shape you specify\n\n### You should try redispatcher if you\n* Have a redis instance\n* Have a web service that needs to process long running tasks in the background\n* Don\'t want to deal with setting up Rabbit and cumbersome libraries like Celery\n\n\n## Overview\n\nredispatcher can be broken down into three (ish) parts.\n\n#### Consumer\nIt all begins with a consumer. A consumer is just a class that defines the structure of the mssages it will be listening for and a function that implements the logic for processing that message.\n\n#### Publishing\nEvery consumer you define will provide you with an easy `publish` method that you can use to queue up messages. Because we use Pydantic, it will validate and ensure that any messages you send/receive have to be formatted correctly. \n\n#### Consumer Pool\nA consumer pool is a separate process that listens for all relevant messages queued up in Redis and dispatches them to the designated consumers to be processed.\n\n\n## Install\n```bash\n$ pip install redispatcher\n```\n\n### Basic Consumer\n```python\n# my_consumer.py\nfrom redispatcher import BaseConsumer\n\nclass MyConsumer(BaseConsumer):\n\n    QUEUE = "my-queue-key"\n\n    class Message(BaseConsumer.Message):\n        email: str\n        name: str\n        registered: bool\n    \n    async def process_message(self, message: Message):\n        print(f"processing message {message}")\n        ...\n\n```\n\n### Running your consumers in a pool\n\n#### Defining your pool\n```python\n# pool.py\nfrom redispatcher import ConsumerPool, RedispatcherConfig, ConsumerConfig\n\nfrom my_consumer import MyConsumer\n\nconfig = RedispatcherConfig(\n    redis_dsn="rediss://", # if not provided, will read from env\n    consumers=[\n        ConsumerConfig(\n            consumer_class=MyConsumer\n        )\n    ]\n)\n\nif __name__ == "__main__":\n    consumer_pool = ConsumerPool(config)\n    consumer_pool.start() \n```\n\n```bash\n$ python pool.py\n```\n\n### Publishing messages to your pool\n```python\n# endpoint.py\n\nfrom my_consumer import MyConsumer\nfrom clients import my_aioredis_client\n\n@app.post("/signup")\nasync def signup()\n    # queue up work to send a welcome email while we continue with the rest of our endpoint logic\n    await MyConsumer.publish(MyConsumer.Message(email=..., name=..., registered=True), my_aioredis_client)\n```\n\n\n### Advanced usage\n\nWe built redispatcher with a couple of handy utilities, but kept it as minimal as possible for your own consumers to be subclassed and implement any logging/tracing/etc logic yourself. \n\nTake a look at `examples/nicer_consumer.py` and `examples/example_publisher.py` for some examples of what\'s possible.\n\n\n### Contributing\n\nIf you have a suggestion on how to improve redispatcher or experience a bug file an issue at <https://github.com/rafalstapinski/redispatcher/issues>.\n\nIf you want to contribute, open a PR at <https://github.com/rafalstapinski/redispatcher>.\n\nPyPi: <https://pypi.org/project/redispatcher/>\n',
    'author': 'Rafal Stapinski',
    'author_email': 'stapinskirafal@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rafalstapinski/redispatcher',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
