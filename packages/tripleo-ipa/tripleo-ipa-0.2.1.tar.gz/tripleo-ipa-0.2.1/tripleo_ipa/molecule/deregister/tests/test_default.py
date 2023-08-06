import os

import pytest
import testinfra
import testinfra.utils.ansible_runner

inventory = os.environ['MOLECULE_INVENTORY_FILE']
testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    inventory).get_hosts('all')


def setup_module(module):
    for host in testinfra_hosts:
        testinfra.get_host('ansible://' + host,
                           ansible_inventory=inventory
        ).check_output('echo password123 | kinit admin')


def teardown_module(module):
    for host in testinfra_hosts:
        testinfra.get_host('ansible://' + host,
                           ansible_inventory=inventory
        ).check_output('kdestroy')


@pytest.mark.parametrize('name', [
    'overcloud.example.test',
    'overcloud.ctlplane.example.test',
    'overcloud.internalapi.example.test',
    'overcloud.storage.example.test',
    'overcloud.storagemgmt.example.test',
])
def test_hosts_created(host, name):
    result = host.check_output('ipa host-find {}'.format(name))
    assert '1 host matched' in result


@pytest.mark.parametrize('name', [
    'test-1.example.test',
    'test-1.ctlplane.example.test',
    'test-1.external.example.test',
    'test-1.internalapi.example.test',
    'test-1.storage.example.test',
    'test-1.storagemgmt.example.test',
])
def test_hosts_deleted(host, name):
    host.run_expect([1], 'ipa host-find {}'.format(name))


@pytest.mark.parametrize('service, subhost', [
    ('HTTP', 'ctlplane'),
    ('HTTP', 'external'),
    ('HTTP', 'internalapi'),
    ('HTTP', 'storage'),
    ('HTTP', 'storagemgmt'),
    ('haproxy', 'ctlplane'),
    ('haproxy', 'internalapi'),
    ('haproxy', 'storage'),
    ('haproxy', 'storagemgmt'),
    ('libvirt-vnc', 'internalapi'),
    ('mysql', 'internalapi'),
    ('neutron_ovn', 'internalapi'),
    ('novnc-proxy', 'internalapi'),
    ('ovn_controller', 'internalapi'),
    ('ovn_dbs', 'internalapi'),
    ('rabbitmq', 'internalapi'),
    ('redis', 'internalapi'),
])
def test_services1(host, service, subhost):
    host.run_expect(
        [2],
        'ipa service-show {}/test-1.{}.example.test@EXAMPLE.TEST'.format(
            service, subhost))


@pytest.mark.parametrize('service, subhost', [
    ('HTTP', 'ctlplane'),
    ('HTTP', 'external'),
    ('HTTP', 'internalapi'),
    ('HTTP', 'storage'),
    ('HTTP', 'storagemgmt'),
    ('haproxy', 'ctlplane'),
    ('haproxy', 'internalapi'),
    ('haproxy', 'storage'),
    ('haproxy', 'storagemgmt'),
    ('libvirt-vnc', 'internalapi'),
    ('mysql', 'internalapi'),
    ('neutron_ovn', 'internalapi'),
    ('novnc-proxy', 'internalapi'),
    ('ovn_controller', 'internalapi'),
    ('ovn_dbs', 'internalapi'),
    ('rabbitmq', 'internalapi'),
    ('redis', 'internalapi'),
])
def test_services2(host, service, subhost):
    result = host.check_output(
        'ipa service-show {}/test-2.{}.example.test@EXAMPLE.TEST'.format(
            service, subhost))
    assert 'Principal name: {}/test-2.{}.example.test@EXAMPLE.TEST'.format(
        service, subhost) in result
    assert 'Principal alias: {}/test-2.{}.example.test@EXAMPLE.TEST'.format(
        service, subhost) in result
    'Roles: Nova Host Manager' in result
    assert 'Managed by: test-2.{}.example.test, test-2.example.test'.format(
        subhost) in result


@pytest.mark.parametrize('service, subhost', [
    ('libvirt', 'internalapi'),
    ('libvirt-vnc', 'internalapi'),
    ('ovn_controller', 'internalapi'),
    ('ovn_metadata', 'internalapi'),
    ('qemu', 'internalapi'),
])
def test_services3(host, service, subhost):
    result = host.check_output(
        'ipa service-show {}/test-3.{}.example.test@EXAMPLE.TEST'.format(
            service, subhost))
    assert 'Principal name: {}/test-3.{}.example.test@EXAMPLE.TEST'.format(
        service, subhost) in result
    assert 'Principal alias: {}/test-3.{}.example.test@EXAMPLE.TEST'.format(
        service, subhost) in result
    'Roles: Nova Host Manager' in result
    assert 'Managed by: test-3.{}.example.test, test-3.example.test'.format(
        subhost) in result
