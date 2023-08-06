# jenkins_py_scripts (AKA buildtools)

This is a collection of scripts that are used by NTS Jenkins Pipelines to enable integrations with various external tools.

## Running buildtool from source code

This is simple to do using the `--editable` flag to a pip  -- any changes you make in your local development environment will be reflected in the `buildtools` CLI tool installed with '--editable' specified.

    # run this from the directory where setup.py lives
    pip install --editable .

> NOTE: If dependency updates are part of your changes, now it is a good idea to ignore the 'buildtools' package, e.g. via grep --invert-match: `pip freeze | grep -v "buildtools" > requirements.txt`

## (CICD) How to make a new release of buildtools

> TODO: Document how to use the Jenkins CICD pipeline. (press 'approve' button when it shows up in the ConsoleText)

## (Manual, OUTDATED) How to make a new 'release' of buildtools

Currently, the 'release' process requires manually incrementing the version and creating a git tag for the version. 
Additionally, **it is a good idea to run all the automated tests before creating a new release**.

1. Update the `__version__` variable in `buildtools/__init__.py` (per [semantic versioning convention](https://semver.org/)).
    * If you add any 'required arguments' to an existing CLI, increment the `MAJOR` version.
    * If you add only 'optional arguments' to an existing CLI, increment the `MINOR` version.
    * If you don't change the CLI in any way, increment the `PATCH` version (or 'minor' version if that is more appropriate in your opinion).
2. Create a git tag that corresponds to the new version, and push it to bitbucket:
    
    git tag 1.1.1
    git push --tags

> Once the git tag is pushed, you can ["'pip install' from a git repository" (external article).](https://adamj.eu/tech/2019/03/11/pip-install-from-a-git-repository/) 
>  E.g. the following command will install v1.0.0 of buildtools: `pip3 install git+ssh://github.com/terminalstderr/buildtools.git@1.0.0#egg=buildtools`


## Tab Completion? Yes, please!

`buildtools` CLI interface supports tab completion via the [`argcomplete` module](https://kislyuk.github.io/argcomplete/).
Unfortunately, this does not work 'out of the box' without doing some 'bash configuration' -- run the following commands (or add it to your ~/.bashrc):
        
    eval "$(register-python-argcomplete buildtools)"

## Automated Testing

pytest is used for unit testing and integration testing of this solution. 
Run the pytest suite by installing 'buildtools' in editable mode and simply running 'pytest' from the CLI.

    pip install --editable .
    pytest

> NOTICE: All of the test_e2e modules require environment variables to be established -- see the test `@pytest.fixture` function definitions.

> WARNING: We did not take care to set up a 'test environment' for the e2e tests -- they are hitting the live/production resources.
> As such, some of test cases are fragile and will need refactoring if a certain pull request gets deleted.