from doit import task_params


@task_params([{"name": "check", "default": False, "type": bool, "long": "check"}])
def task_format(check: bool):
    return {
        "actions": [
            f"black {'--check' if check else ''} lemon tests setup.py dodo.py",
            f"isort {'--check' if check else ''} --profile black lemon tests setup.py dodo.py",
            f"autoflake --remove-all-unused-imports {'--check' if check else '--in-place'}"
            " -r lemon tests setup.py dodo.py",
        ],
    }


def task_lint():
    return {
        "actions": [
            "pylint lemon tests dodo.py",
            "mypy --strict lemon tests",
        ],
    }
