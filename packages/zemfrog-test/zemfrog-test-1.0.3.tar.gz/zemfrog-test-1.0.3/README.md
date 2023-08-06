# zemfrog-test
Zemfrog unit testing tools

# Features

* Support automatically create unit tests for API / blueprints
* Available fixtures:
    - client
        > This is to access the Client class to interact with the API
    - app_ctx
        > This is to enable the flask context application
    - req_ctx
        > This is to activate the flask request context application
    - user
        > This is to generate confirmed random users


# Warning

zemfrog test is available a finalizer to delete all users when the test session ends. so you need to create a special database for testing.


# Usage

Install this

```sh
pip install zemfrog-test
```

And add it to the `COMMANDS` configuration in the zemfrog application.

```python
COMMANDS = ["zemfrog_test"]
```

Now that you have the `test` command, here is a list of supported commands:

* `init` - Initialize the tests directory in the project directory.
* `new` - Create unit tests for the API or blueprint. (The names entered must match `APIS` and `BLUEPRINTS` configurations. For example `zemfrog_auth.jwt`)
* `run` - To run unit tests. **It doesn't work with the `pytest` command, don't know why. :/**
