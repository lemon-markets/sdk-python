def task_format():
    return {
        "actions": [
            "black lemon tests setup.py dodo.py",
            "isort --profile black lemon tests setup.py dodo.py",
            "autoflake --remove-all-unused-imports --in-place -r lemon tests setup.py dodo.py",
        ],
    }


def task_lint():
    return {
        "actions": [
            "pylint lemon tests dodo.py",
            "mypy --strict lemon tests",
        ],
    }
