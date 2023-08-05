# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyspark_spy']

package_data = \
{'': ['*']}

install_requires = \
['pyspark>=2.0.0']

setup_kwargs = {
    'name': 'pyspark-spy',
    'version': '1.0.1',
    'description': 'Collect and aggregate on spark events for profitz. In 🐍 way!',
    'long_description': "pyspark-spy\n===========\n\n![pyspark version](https://img.shields.io/badge/pyspark-2.3%2C%202.4%2C%203.0-success)\n![python version](https://img.shields.io/badge/python-3.5%2C%203.6%2C%203.7-informational)\n[![Build Status](https://travis-ci.org/sashgorokhov/pyspark-spy.svg?branch=master)](https://travis-ci.org/sashgorokhov/pyspark-spy)\n\nCollect and aggregate on spark events for profitz. In 🐍 way!\n\n## How to\nYou register a listener\n```python\nimport pyspark_spy\nlistener = pyspark_spy.PersistingSparkListener()\npyspark_spy.register_listener(spark_context, listener)\n```\n\nExecute your spark job as usual\n```python\nspark_context.range(1, 100).count()\n```\n\nAnd you have all metrics collected!\n\n```python\nprint(listener.stage_output_metrics_aggregate())\nOutputMetrics(bytesWritten=12861, recordsWritten=2426)\n```\n\nLook Ma, no actions!\n\nTested on python 3.5 - 3.7 and pyspark 2.3 - 3.0\n\n## Available listeners\n\n- `pyspark_spy.interface.SparkListener` - Base listener class. \n  It defines `on_spark_event(event_name, java_event)` method that you can implement yourself \n  for custom logic when any event is received.\n  \n- `LoggingSparkListener` - just logs event names received into supplied or automatically created logger.\n- `StdoutSparkListener` - writes event names into stdout\n- `PersistingSparkListener` - saves spark events into internal buffer\n- `ContextSparkListener` - same as PersistingSparkListener but also allows you to record only events \n  occured within python context manager scope. More on that later\n\n### PersistingSparkListener\n\nSpark events collected (as java objects):\n- applicationEnd\n- applicationStart\n- blockManagerRemoved\n- blockUpdated\n- environmentUpdate\n- executorAdded\n- executorMetricsUpdate\n- executorRemoved\n- jobEnd\n- jobStart\n- otherEvent\n- stageCompleted\n- stageSubmitted\n- taskEnd\n- taskGettingResult\n- taskStart\n- unpersistRDD\n\n```python\nlistener.java_events['executorMetricsUpdate'] # -> List of py4j java objects\n```\n\n> View all possible spark events and their fields https://spark.apache.org/docs/2.3.1/api/java/org/apache/spark/scheduler/SparkListener.html\n\nEvents converted to python objects:\n- jobEnd\n- stageCompleted\n\n```python\nlistener.python_events['jobEnd']  # -> List of java events converted to typed namedtuples.\nlistener.jobEnd  # same\n```\n\n### Available aggregations\nOnly in `PersistingSparkListener` and `ContextSparkListener`\n\n- `stage_input_metrics_aggregate` - sums up all `stageCompleted` event inputMetrics into one\n```python\nprint(listener.stage_input_metrics_aggregate())\nInputMetrics(bytesRead=21574, recordsRead=584)\n```\n- `stage_output_metrics_aggregate` - sums up all `stageCompleted` event outputMetrics into one\n```python\nprint(listener.stage_output_metrics_aggregate())\nOutputMetrics(bytesWritten=12861, recordsWritten=2426)\n```\n\n### ContextSparkListener\n\nTo collect events from different actions and to build separate aggregations, use `ContextSparkListener`.\n```python\nlistener = ContextSparkListener()\nregister_listener(sc, listener)\n\nwith listener as events: # events is basically another listener\n    run_spark_job()\nevents.stage_output_metrics_aggregate()  # events collected only within context manager\n\nwith listener as events_2:\n    run_other_spark_job()\nevents_2.stage_output_metrics_aggregate()  # metrics collected during second job\n\nlistener.stage_output_metrics_aggregate() # metrics collected for all jobs\n```",
    'author': 'Alexander Gorokhov',
    'author_email': 'sashgorokhov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sashgorokhov/pyspark-spy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5',
}


setup(**setup_kwargs)
