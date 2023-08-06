# Documentation

https://databricks-clay.readthedocs.io/en/latest/

# Development Setup

Create virual environment and install dependencies for local development:

```
python3.7 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -r dev_requirements.txt
```

Exporting variables doesn't make for a great development experience so I recommend using the enviroment manager tools of your editor and for testing create a ./pytest.ini that looks like this:

```
[pytest]
env =
    VARIABLE=value
    VARIABLE2=value2
```

**REMINDER: do NOT commit any files that contain security tokens**

Git ignore already contains an exclusion for pytest.ini


# Build

Build python wheel:
```
python setup.py sdist bdist_wheel
```

There is a CI build configured for this repo that builds on main origin on a private Azure DevOps service.

# Test

Dependencies for testing:
```
pip install --editable .
```

Run tests:
```
pytest
```

Test Coverage:
```
pytest --cov=databricks-clay --cov-report=html
```

View the report in a browser:
```
./htmlcov/index.html
```


