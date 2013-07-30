#!/usr/bin/python
# Copyright (c) 2013 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import copy
import StringIO
import unittest
import sys
from wireless_automation.aspects import wireless_automation_logging
from wireless_automation.aspects import configurable
from wireless_automation.aspects.configurable import configobj


class ConfigurableTestClass1(configurable.Configurable):
    """
    a test class with a configspec for testing, used below.
    """
    CONFIGSPEC = [
        '#comment here',
        'topnumber=integer(min=1,max=50,default=21)',
        '[level_1]',
        '#meaningful level_1 comment here.',
        'midnumber=integer(min=1,max=50,default=22)',
        'midnumber2=integer(min=1,max=50,default=23)',
        '[[level_2]]',
        '#meaningful level_2 comment here.',
        'number=integer(min=1,max=50,default=24)',
        'number1=integer(min=1,max=50,default=25)',
        'number2=integer(min=1,max=50,default=26)',
        'flavor=string(default=berrydefault)'
    ]

    def __init__(self, input_config_data=None):
        """
        @param input_config_data : the input config data
        @return: a new object
        """
        configurable.Configurable.__init__(self, input_config_data)


class BrokenConfigurableTestClass1(ConfigurableTestClass1):
    """
    BrokenConfigurableTestClass1
    """
    CONFIGSPEC = 'this should break the configspec reader'


class BrokenConfigurableTestClass1List(ConfigurableTestClass1):
    """
    BrokenConfigurableTestClass1List
    """
    CONFIGSPEC = ['this should break the configspec reader']


class ConfigurableTestClassNoConfigspec(configurable.Configurable):
    """
    no configspec should raise an error
    """
    def __init__(self, input_config_data=None):
        configurable.Configurable.__init__(self, input_config_data)


class ConfigurableWithConfigspecDict(ConfigurableTestClass1):
    """
    ConfigurableWithConfigspecDict
    """
    CONFIGSPEC = {'should not work '}


class ConfigurableOnlyNeedsLevel1(ConfigurableTestClass1):
    """
    Take a subsection of the config
    """
    CONFIGSPEC = 'set this later '


class ConfigurableClassWithConfigobjAsConfigspec(configurable.Configurable):
    """
    ConfigurableClassWithConfigobjAsConfigspec
    """
    CONFIGSPEC = configobj.ConfigObj(configspec=['x:integer(default=11)'])


class ClassWithAllTheConfigTypes(configurable.Configurable):
    CONFIGSPEC = [
        "Number = integer(min=0, max=10, default=9)",
        #"Float = float (min='0', max='1.111', default = '1.1')",
        "Float = float(default=1)",
        "TrueFalse = boolean(default=False)",
        "IpAddress = ip_addr(default='10.0.0.1')",
        "String = string(min=0,max=100, default='100 chars max')",
        "Tuple = tuple(min=1, max=2, default=list('a','b'))",
        "IntList = int_list(min=1, max=10, default =list(1,2))",
        "FloatList = float_list(min=1, max=10, default =list('1.1',2))",
        "BoolList = bool_list(min=1, max=10, "
                               "default =list(True,False,0,'yes',no))",
        "IpAddrList = ip_addr_list(min=1, max=10, "
                       "default =list(10.10.10.1,1.1.1.1))",
        "StringList = string_list(min=1, max=10, "
                       "default =list('string1', 'string2'))",
        #Mixed list does not have the default keyword, making this
        # not useful for Configurable, which uses defaults extensively.
        #"MixedList = Do not use.
        "AlwaysOK = pass(default = None) ",
        "OptionList  = option('red', 'blue', 'green',default='red' )",
    ]

    def __init__(self, config):
        super(ClassWithAllTheConfigTypes, self).__init__(config)


class TestConfigurableWithManyClasses(unittest.TestCase):
    """
    How does reading a config file and splitting the sections work
    """
    def test_write_and_read_config_file(self):
        """
        test_write_and_read_config_file
        """
        tt = ConfigurableTestClass1()
        default_config = tt.get_default_config()
        fh = StringIO.StringIO()
        default_config.write(fh)
        fh.seek(0)
        read_config = configurable.read_config_from_file(fh)
        self.assertEqual(read_config.write(),
                         default_config.write(),
                         'Reading the config file failed')

    def test_pass_part_of_config_to_object(self):
        """
        test_pass_part_of_config_to_object
        """
        tt = ConfigurableTestClass1()
        sub_configspec = configurable.get_section_of_configspec(
            tt.config.configspec, 'level_1')
        ConfigurableOnlyNeedsLevel1.CONFIGSPEC = sub_configspec
        config = tt.get_default_config()
        section = configurable.get_section_of_config(config, 'level_1')
        tt1 = ConfigurableOnlyNeedsLevel1(section)

    def test_get_section_of_configspec_should_raise_on_dict_input(self):
        """
        test_get_section_of_configspec_should_raise_on_dict_input
        """
        tt = ConfigurableTestClass1()
        with self.assertRaises(configurable.ConfigurationError):
            sub_configspec = configurable.get_section_of_configspec(
                {'spec': '=integer'}, {'level_1'})

    def test_build_config_from_two_classes_and_get_subsections(self):
        """
        test_build_config_from_two_classes_and_get_subsections
        """
        tt = ConfigurableTestClass1()
        combined = configurable.combine_configs([
            ('first', tt.config),
            ('second', tt.config)
        ])
        combined_list_str = combined.write()
        self.assertEqual(combined_list_str[0], '[first]', 'combineding lists')
        self.assertEqual(combined['first'], tt.config, '[first] missing')
        self.assertEqual(combined['second'], tt.config, '[second] missing')

    def test_combine_configs_should_raise_on_duplicate_names(self):
        """
        test_combine_configs_should_raise_on_duplicate_names
        """
        tt = ConfigurableTestClass1()
        with self.assertRaises(configurable.ConfigurationError):
            combined = configurable.combine_configs([
                ('first', tt.config),
                ('first', tt.config)
            ])

    def test_get_section_of_configspec_should_raise_on_missing_section(self):
        """
        test_get_section_of_configspec_should_raise_on_missing_section
        """
        configspec = ConfigurableTestClass1.CONFIGSPEC
        section = 'non_existant_section_name'
        with self.assertRaises(configurable.ConfigurationError):
            configspec_section = configurable.get_section_of_configspec(
                    configspec, section)

    def test_get_section_of_configspec(self):
        """
        test_get_section_of_configspec
        """
        configspec = ConfigurableTestClass1.CONFIGSPEC
        section = 'level_1'
        configspec_section = configurable.get_section_of_configspec(
            configspec, section)
        self.assertEqual(
            configspec_section[0],
            'midnumber = integer(min=1,max=50,default=22)',
            'get_section of configspec failed')

    def test_get_section_of_config(self):
        """
        test_get_section_of_config
        """
        tt = ConfigurableTestClass1()
        config = tt.get_default_config()
        sub_section = configurable.get_section_of_config(config, 'level_1')
        self.assertEqual(sub_section[0], 'midnumber = 22')


class test_configurable(unittest.TestCase):
    """
    Make a derived class of configurable
    """
    def test_make_config_with_many_types_works(self):
        """
        test_make_config_with_many_types_works
        """
        config = ClassWithAllTheConfigTypes.get_default_config()
        a = ClassWithAllTheConfigTypes(config)


    def test_configspec_creates_valid_default_config(self):
        """
        test_configspec_creates_valid_default_config
        """
        tt = ConfigurableTestClass1()
        default_config = tt.get_default_config()
        self.assertTrue(tt.is_this_config_valid(default_config))

        def add_bad_data_and_check(key, value):
            """
            add_bad_data_and_check
            @param value: the value
            @param key: the key
            """
            bad_config = copy.copy(default_config)
            bad_config[key] = value
            self.assertFalse(tt.is_this_config_valid(bad_config))

        add_bad_data_and_check('topnumber', '111')  # Too large
        add_bad_data_and_check('flavors', 'not_in_spec')
        add_bad_data_and_check('number', 'string_not_int')

    def test_many_different_invalid_config_parts(self):
        """
        test_many_different_invalid_config_parts
        """
        tt = ConfigurableTestClass1()
        default_config = tt.get_default_config()

        bad_config = copy.copy(default_config)
        bad_config['level_1']['not_there'] = 1212
        self.assertFalse(tt.is_this_config_valid(bad_config))

        bad_config = copy.copy(default_config)
        bad_config['level_1']['midnumber'] = 1212
        self.assertFalse(tt.is_this_config_valid(bad_config))

        bad_config = copy.copy(default_config)
        bad_config['level_1']['midnumber2'] = 121232
        self.assertFalse(tt.is_this_config_valid(bad_config))

        bad_config = copy.copy(default_config)
        bad_config['level_1']['level_22'] = 121232
        self.assertFalse(tt.is_this_config_valid(bad_config))

        bad_config = copy.copy(default_config)
        bad_config['level_1']['level_2']['number2'] = 121232
        self.assertFalse(tt.is_this_config_valid(bad_config))

    def test_many_invalid_config_parts_at_once(self):
        """
        test_many_invalid_config_parts_at_once
        """
        tt = ConfigurableTestClass1()
        default_config = tt.get_default_config()
        bad_config = copy.copy(default_config)
        bad_config['level_1']['not_there'] = 1212
        bad_config['level_1']['midnumber'] = 1212
        bad_config['level_1']['midnumber2'] = 121232
        bad_config['level_1']['level_22'] = 121232
        bad_config['level_1']['level_2']['number2'] = 121232
        self.assertFalse(tt.is_this_config_valid(bad_config))

    def test_is_this_config_valid_should_raise_on_bad_input(self):
        with self.assertRaises(configurable.ConfigurationError):
            ConfigurableTestClass1.is_this_config_valid(['bad_type'])

    def test_missing_configspec_raises_error(self):
        """
        test_missing_configspec_raises_error
        """
        with self.assertRaises(configurable.ConfigurationError):
            tt = ConfigurableTestClassNoConfigspec()

    def test_configspec_must_not_be_dict(self):
        """
        test_configspec_must_not_be_dict
        """
        with self.assertRaises(configurable.ConfigurationError):
            tt = ConfigurableWithConfigspecDict()

    def test_subset_of_config_options_add_to_defaults(self):
        """
        test_subset_of_config_options_add_to_defaults
        """
        tt = ConfigurableTestClass1(['topnumber=33'])
        self.assertEqual(tt.config['topnumber'], 33)
        self.assertEqual(tt.config['level_1']['midnumber'], 22)
        tt.is_this_config_valid(tt.config)

    def test_get_items_in_config_not_in_configspec(self):
        """
        test_get_items_in_config_not_in_configspec
        """
        config = ConfigurableTestClass1.get_default_config()
        config['extra_junk'] = 33
        extras = ConfigurableTestClass1.\
            _get_items_in_config_not_in_configspec(config)
        self.assertEqual(extras[0][1], 'extra_junk')

    def test_invalid_config_list_raises_error(self):
        """
        test_extra_values_raise_error
        """
        with self.assertRaises(configurable.ConfigurationError):
            tt = ConfigurableTestClass1(['extra_thing=33'])

    def test_invalid_config_dict_raises_error(self):
        """
        test_invalid_config_raises_error
        """
        with self.assertRaises(configurable.ConfigurationError):
            tt = ConfigurableTestClass1({'bad_config_data': 333})

    def test_init_with_configobj_as_confgspec(self):
        """
        test_init_with_configobj_as_confgspec
        """
        tt = ConfigurableClassWithConfigobjAsConfigspec()

    def test_valid_config(self):
        """
        test_valid_config
        """
        tt = ConfigurableTestClass1()
        default_config = tt.get_default_config()
        tt2 = ConfigurableTestClass1(default_config)

    def test_check_config_raises_error(self):
        """
        test_get_default_config_raises_error
        """
        with self.assertRaises(configurable.ConfigurationError):
            tt = BrokenConfigurableTestClass1()

    def test_get_default_config_raises_error(self):
        """
        test_get_default_config_raises_error
        """
        with self.assertRaises(configurable.ConfigurationError):
            tt = BrokenConfigurableTestClass1List.get_default_config()

if __name__ == '__main__':
    log = wireless_automation_logging.setup_logging(
        'configurable', output_stream=sys.stdout)
    unittest.main(verbosity=2)
