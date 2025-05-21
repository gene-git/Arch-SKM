"""
Tests:
    - Hash
    - Moving to production
    - DNS server restart

Please set PYTHONPATH=../src/dns_tools
"""
from subprocess import CalledProcessError
import pytest


from lib import run_prog


@pytest.fixture(scope='session', autouse=True)
def setup_cleanup():
    """
    Setup before tests run
    Clean up after tests completed
    """
    pargs = ['./tools/test-init']
    (rc, _stdout, stderr) = run_prog(pargs)
    if rc != 0:
        raise CalledProcessError(-1, pargs, stderr)

    yield

    pargs = ['./tools/test-clean']
    (rc, _stdout, _stderr) = run_prog(pargs)
    if rc != 0:
        raise CalledProcessError(-1, pargs, stderr)


class TestKeys:
    """
    Hash test class
    """
    def test_01_genkeys(self):
        """
        Generate keys
        """
        pargs = ['./certs-local/genkeys.py']
        pargs += ['-c', './config']
        (rc, stdout, _stderr) = run_prog(pargs)
        assert rc == 0
        assert 'Success: all done' in stdout

    def test_02_refresh(self):
        """
        Key refresh should not be needed
        """
        pargs = ['./certs-local/genkeys.py']
        pargs += ['-c', './config', '-r', '7d', '-v']
        (rc, stdout, _stderr) = run_prog(pargs)
        assert rc == 0
        assert 'Key refresh not needed' in stdout

    def test_03_sign_modules(self):
        """
        Sign sample modules
        """
        pargs = ['./certs-local/sign_module.py']
        pargs += ['-d', './modules']
        (rc, stdout, _stderr) = run_prog(pargs)
        assert rc == 0
        assert 'Success: all done' in stdout
