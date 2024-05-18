Allow CI tests for a cookiecutter repo with some basic tests. Uses `pytest-cookies` so install that first:

```bash
pip install pytest-cookies
```

Tests below are for a Java project template (using Gradle). Adjust as desired.

```python
import os
import shlex
import subprocess
from contextlib import contextmanager
from cookiecutter.utils import rmtree


@contextmanager
def run_cookiecutter(cookies, *args, **kwargs):
	"""
	Runs cookiecutter on entering `with` block.
	Deletes files when leaving `with` context
	"""
	result = cookies.bake(*args, **kwargs)
	try:
		yield result
	finally:
		if result.project:
			rmtree(str(result.project))


@contextmanager
def inside_dir(dirpath):
	"""
	Changes to given directory temporarily.
	"""
	old_path = os.getcwd()
	try:
		os.chdir(dirpath)
		yield
	finally:
		os.chdir(old_path)


def run_inside_dir(command, dirpath):
	with inside_dir(dirpath):
		return subprocess.check_call(shlex.split(command))


def test_bake_with_defaults(cookies):
	with run_cookiecutter(cookies) as result:
		assert result.exception is None
		assert result.project.isdir()
		assert result.exit_code == 0

		found_toplevel_files = [
			f.basename
			for f in result.project.listdir()
		]
		assert "build.gradle.kts" in found_toplevel_files


def test_bake_and_run_build(cookies):
	with run_cookiecutter(cookies) as result:
		assert result.exception is None
		assert result.project.isdir()
		assert run_inside_dir("gradle build", str(result.project)) == 0


def test_setting_project_name(cookies):
	properties = {"repo_name": "foo-service"}
	with run_cookiecutter(cookies, extra_context=properties) as result:
		assert result.exception is None
		assert result.exit_code == 0

		assert "foo-service" == result.project.basename

		with open(str(result.project.join("settings.gradle.kts"))) as manifest_file:
			assert "foo-service" in manifest_file.read()
```
