# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pytest_zebrunner', 'pytest_zebrunner.api']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.16.1,<0.17.0',
 'pydantic>=1.7.2,<2.0.0',
 'pytest>=6.1.1,<7.0.0',
 'python-dotenv>=0.15.0,<0.16.0']

entry_points = \
{'pytest11': ['pytest-zebrunner = pytest_zebrunner.plugin']}

setup_kwargs = {
    'name': 'pytest-zebrunner',
    'version': '0.1.1',
    'description': 'Pytest connector for Zebrunner reporting',
    'long_description': '# Zebrunner PyTest agent\n\n\nThe official Zebrunner Pytest agent provides reporting functionality. It can automatically track selenium sessions\nand send info about session details to Zebrunner backend. It can be ease integrated in project just by installing library\nand adding configuration file.\n\nTo include reporting into your project is pretty easy - just install agent and provide minimal valid configuration for reporting.\n\n\n## Installation\n\n    pip install pytest-zebrunner\n\n## Configuration\nAfter installation reporting is disabled by default. It won\'t send data to zebrunner service without valid configuration.\nTo configure app you need to specify environment variables. It also can be done by specifying variables in `.env` file in root path of your project.\nYou can configure agent **only** with environment variables. Another formats would be added in future.\nPlaned formats are `yaml`, `ini` and program arguments.\n\n<!-- groups:start -->\n### Environment variables\n```dosini\nSERVICE_URL=<zebrunner url>\nACCESS_TOKEN=<access_token>\nZEBRUNNER_PROJECT=ProjectName\nZEBRUNNER_ENABLED=true\nTEST_RUN_NAME=Testing new features\nBUILD=1.25.16\nENV=stage\nSEND_LOGS=true\n```\n\n- `SERVICE_URL` - [required] It is Zebrunner server hostname. It can be obtained in Zebrunner on the \'Account & profile\' page under the \'Service URL\' section;\n\n- `ACCESS_TOKEN` - [required] Access token must be used to perform API calls. It can be obtained in Zebrunner on the \'Account & profile\' page under the \'Token\' section;\n\n- `ZEBRUNNER_PROJECT` - [required] It is the project that the test run belongs to. The default value is `UNKNOWN`. You can manage projects in Zebrunner in the appropriate section;\n\n- `REPORTING_ENABLED` - You can disable agent if it makes side effects in you project or doesn\'t work. *Default*: `true`\n\n- `TEST_RUN_NAME` - It is the display name of the test run. *Default*: `Unnamed-%time`\n\n- `BUILD` -  It is the build number that is associated with the test run. It can depict either the test build number or the application build number;\n\n- `ENV` - It is the environment where the tests will run.\n\n- `SEND_LOGS` - Send test logs to zebrunner. *Default*: `false`\n<!-- groups:end -->\n\nIf required configurations not provided there is a warning in logs with problem description and names of options,\nwhich need to be specified. Parameter names are case insensitive and can be written in upper and lower registers.\n\n## Collecting logs\nIt is also possible to enable the log collection for your tests.  All you have to do to enable logging is to enable it in configuration.\nAgent connects to pythons root logger and collect logs from there. Possible, in future would be more options to configure logs sending.\n\n\n## Additional functionality\n\n**IMPORTANT**: All attachments to tests can be done only while some test is running.\nAll attachments to test-run can be done only while pytest test-session is active.\n---------------------------\n\n### Collecting captured screenshot\nSometimes it may be useful to have an ability to track captured screenshots in scope of zebrunner reporting. The agent comes\nwith API allowing you to send your screenshots to Zebrunner, so they will be attached to the test.\n\n```python\nfrom pytest_zebrunner.attachments import attach_test_screenshot\n\n\ndef test_something():\n    ...\n    driver.save_screenshot("path_to_screenshot.png) # Capture screenshot with selenium driver\n    attach_test_screenshot("path_to_screenshot.png")\n    ...\n```\n\n### Collecting additional artifacts\nIn case your tests or entire test run produce some artifacts, it may be useful to track them in Zebrunner.\nThe agent comes with a few convenient methods for uploading artifacts in Zebrunner and linking them to the currently running test or the test run.\nArtifacts and artifact-references can be attached using functions from `attachments` module. Together with an artifact\nor artifact reference, you must provide the display name. For the file, this name must contain the file extension that\nreflects the actual content of the file. If the file extension does not match the file content, this file will not be\nsaved in Zebrunner. Artifact reference can have an arbitrary name.\n\n#### Attach artifact to test\n```python\nfrom pytest_zebrunner.attachments import attach_test_artifact\n\n\ndef test_something():\n    ...\n    attach_test_artifact("path_to_artifact")\n    ...\n```\n\n### Attach artifact-reference to test\n```python\nfrom pytest_zebrunner.attachments import attach_test_artifact_reference\n\n\ndef test_something():\n    ...\n    attach_test_artifact_reference("name", "reference")\n    ...\n```\n\n### Attach artifact to test-run\n```python\nfrom pytest_zebrunner.attachments import attach_test_run_artifact\n\n\nattach_test_run_artifact("path_to_artifact")\n```\n\n### Attach artifact-reference to test-run\n```python\nfrom pytest_zebrunner.attachments import attach_test_run_artifact_reference\n\n\nattach_test_run_artifact_reference("name", "reference")\n```\n\nArtifact upload process is performed in the foreground now, sow it will block execution thread while sending.\nIn future release background uploading would be realized.\n\n\n### Attaching test labels\nIn some cases, it may be useful to attach some meta information related to a test. The agent comes with a concept of a label.\nLabel is a key-value pair associated with a test. The key and value are represented by a `str`. Labels can be attached to\ntests and test-runs.\n\n```python\n@pytest.mark.label("name", "value")\ndef test_something():\n    ...\n```\nor\n```python\nfrom pytest_zebrunner.attachments import attach_test_label\n\n\ndef test_something():\n    ...\n    attach_test_label("name", "value")\n    ...\n```\n**Note:** These two methods can be combined.\n\nFor test-run:\n```python\nfrom pytest_zebrunner.attachments import attach_test_run_label\n\nattach_test_run_label("name", "value")\n```\n\n\n### Tracking test maintainer\nYou may want to add transparency to the process of automation maintenance by having an engineer responsible for\nevolution of specific tests or test classes. Zebrunner comes with a concept of a maintainer - a person that can be\nassigned to maintain tests. In order to keep track of those, the agent comes with the `@pytest.mark.maintainer` annotation.\n\nSee a sample test bellow:\n\n```python\n@pytest.mark.maintainer("username_of_maintainer")\ndef test_something():\n    ...\n```\n\n### Tracking of web driver sessions\nThe Zebrunner test agent has a great ability to track tests along with remote driver sessions. You have nothing to do :)\nThe agent automatically injects tracking functionality to selenium driver if selenium library is installed. Agent sends\ndriver capabilities to zebrunner when the driver starts and finish time when the driver stops.\n',
    'author': 'Anatoliy Platonov',
    'author_email': 'p4m.dev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://zebrunner.com/documentation/agents/pytest',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
