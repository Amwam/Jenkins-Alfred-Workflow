from paver.easy import *
from paver.setuputils import setup

setup(
    name="Jenkins-Alfred-Workflow",
    packages=['jenkins'],
    version="1.0",
    url="http://www.amwam.me/",
    author="Amit Shah",
    author_email="amitshah@oneuk.com"
)


@task
@needs(["distutils.command.sdist"])
def sdist():
    """Generate docs and source distribution."""
    pass


@task
@needs('unit_tests')
def default():
    """Default tasks to execute when running paver from the command line."""


@task
def unit_tests():
    """Runs all unit tests under the test/unit folder structure."""
    sh('pytest --cov ./')

