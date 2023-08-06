# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fake_ssh', 'fake_ssh.demo']

package_data = \
{'': ['*']}

install_requires = \
['Logbook>=1.5.3,<2.0.0', 'paramiko>=2.4,<3.0']

entry_points = \
{'console_scripts': ['echo_server = fake_ssh.demo.echo_server:main']}

setup_kwargs = {
    'name': 'fake-ssh',
    'version': '0.1.0a5',
    'description': 'Fakes an SSH Server',
    'long_description': 'Mock SSH Server\n-----------------\n\n\nDo you...\n\n* have a test that SSHs into a server and don\'t want the hassle of setting one up for testing?\n\n* think monkeypatching isn\'t as good as it sounds?\n\n* want to develop an application and need a fake server to return predefined results?\n\nThis package is for you!\n\nInstallation\n-----------\n\n```\npip install fake-ssh\n```\n\nUsage\n-----\n\n## Blocking Server\n\nA blocking server is often used for development purposes.\n\nSimply write yourself a `server.py` file:\n\n```python\nfrom typing import Optional\nfrom fake_ssh import Server\n\n\ndef handler(command: str) -> Optional[str]:\n    if command.startswith("ls"):\n        return "file1\\nfile2\\n"\n    elif command.startswith("echo"):\n        return command[4:].strip() + "\\n"\n\nif __name__ == "__main__":\n    Server(command_handler=handler, port=5050).run_blocking()\n\n```\n\nAnd run it:\n\n```\n$ python3 server.py\n```\n\nIn a separate terminal, run:\n\n```\n$ ssh root@127.0.0.1 -p 5050 echo 42\n42\n                                                                         \n$ ssh root@127.0.0.1 -p 5050 ls\nfile1\nfile2\n```\n\n(if you are prompted for a password, you can leave it blank)\n\nNote how you need to specify a non standard port (5050). Using the standard port (22) would require root permissions\nand is probably unsafe.\n\n\n## Non-Blocking Server\n\nA non blocking server is often used in tests. \n\nThis server runs in a thread and allows you to run some tests in parallel.\n\n```python\nimport paramiko\nimport pytest\n\nfrom fake_ssh import Server\n\n\ndef handler(command):\n    if command == "ls":\n        return "file1\\nfile2\\n"\n\n\n@pytest.fixture\ndef server():\n    with Server(command_handler=handler) as server:\n        yield server\n\n\ndef my_ls(host, port):\n    c = paramiko.SSHClient()\n    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())\n    c.connect(hostname=host,\n              port=port,\n              username="root",\n              password="",\n              allow_agent=False,\n              look_for_keys=False)\n    return c.exec_command("ls")[1].read().decode().splitlines()\n\n\ndef test_ls(server):\n    assert my_ls(server.host, server.port) == ["file1", "file2"]\n\n```\n',
    'author': 'David Sternlicht',
    'author_email': 'dsternlicht@infinidat.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/d1618033/fake-ssh.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
