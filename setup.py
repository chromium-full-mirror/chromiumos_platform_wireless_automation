from distutils.core import setup

# todo: regenerate this.
setup(
    name='wireless_automation',
    version='0.8',
    packages=['build.lib.linux-x86_64-2.7.wireless_automation', 'unit_tests',
              'unit_tests.unittests', 'wireless_automation', 'wireless_automation.racks',
              'wireless_automation.aspects', 'wireless_automation.instruments',
              'wireless_automation.instruments.call_box',
              'wireless_automation.instruments.call_box.agilent_pxt',
              'wireless_automation.instruments.prologix',
              'wireless_automation.instruments.network_data_source',
              'wireless_automation.chrome_device', 'wireless_automation.chrome_device.wifi',
              'wireless_automation.chrome_device.modems'],
    url='',
    license='',
    author='byronk',
    author_email='byronk@google.com',
    description='Library for automation wireless tests'
)
