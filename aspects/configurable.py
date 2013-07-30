# Copyright (c) 2013 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""
Configurable: A base class. Provides methods to read, and verify configuration.

read_config_from_file: Reads a config text file and returns a config object

get_section_of_config: Returns a subsection of the configspec

get_section_of_configspec: Returns a subsection of the config

ConfigurationError: The exception type thrown by the Configurable functions
"""

import collections
import pprint
import re
from wireless_automation.aspects import configobj
from wireless_automation.aspects import wireless_automation_error
from wireless_automation.aspects import wireless_automation_logging
from wireless_automation.aspects import validate

log = wireless_automation_logging.setup_logging('configurable')


class ConfigurationError(wireless_automation_error.WirelessAutomationError):
    pass


def read_config_from_file(file_name):
    """
    Read a config from a file.

    @param file_name: The file to read.

    @return: a ConfigObj containing the data.
        This will have no configspec, only the data.

    """
    return configobj.ConfigObj(file_name)


def get_section_of_configspec(configspec, section_name):
    """
    Returns the specified subsection of the configspec.

    @param configspec: The configspec

    @param section_name:  The name of the section to return

    @return: A subsection of the passed in configspec.

    """
    if isinstance(configspec, configobj.ConfigObj):
        pass
    elif isinstance(configspec, list):
        configspec = configobj.ConfigObj(configspec=configspec).configspec
    else:
        raise ConfigurationError('get_section_of_configspec needs ConfigObj'
                                 ' or list, not %s ' % type(configspec))

    if section_name not in configspec.sections:
        raise ConfigurationError('Subsection %s not found in configspec %s' %
                                 (section_name, configspec))
    # A bit of a hack. To retain comments in the configspec, we
    # cast it to a ConfigObj, and write it.
    strings = configobj.ConfigObj(configspec[section_name]).write()
    # It produces a correct output, except for not removing the []
    # of child sections. So we do that here, along with removing quotes.
    strings = [re.sub('\"(.*)\"', '\\1', x) for x in strings]
    strings = [re.sub('\[(.*)\]', '\\1', x) for x in strings]
    return strings


def get_section_of_config(config, section_name):
    """
    Returns one section of the config, by name.

    Used for reading in the config file for the app, which contains config
    for many objects. Pull out the config for each object by section name.

    Output:
        [Class1Section]
        power=33
        channel=3
        [Class2Section]
        power=33
        freq=1889.8

    @param config: The config to copy the section from

    @param section_name: the top level section name

    @return: The section as a ConfigObj

    """
    x = config[section_name]
    config = configobj.ConfigObj(x).write()
    config = [re.sub('\[(.*)\]', '\\1', x) for x in config]
    return config


def combine_configs(tuple_list):
    """
    Combines configs. Used when asking many objects for their config, then
    saving the combined config in one file that is now the config for the app.
    Duplicate section names are bad.

    Example:
    c1 = class1.get_default_config()
    c2 = class2.get_default_config()
    combined_config = [('Class1Section',c1),('Class2Section',c2)]
    combined_config.print()

    Output:
        [Class1Section]
        power=33
        channel=3
        [Class2Section]
        power=33
        freq=1889.8

    @param tuple_list: list of ('name',ConfigObj)

    @return: a ConfigObj composed of the sub sections, while maintaining order.

    """
    # Check the input
    sections = [x[0] for x in tuple_list]
    counter = collections.Counter(sections)
    if counter.most_common()[0][1] > 1:
        log.error('conbine_configs requires unique names. These are duplicates')
        for name in counter.most_common():
            if name[1] > 1:
                log.error("'%s' was used %s times" % (name[0], name[1]))
        raise ConfigurationError('combine_configs called with duplicate names')
    # do the merge
    merged = configobj.ConfigObj()
    for item in tuple_list:
        assert isinstance(item[0], str)
        assert isinstance(item[1], configobj.ConfigObj)
        merged.merge({item[0]: item[1].dict()})
    return merged


class Configurable(object):
    """
    Provides an interface for configuring complex objects. The specification
    for the config is specified in self.configspec, and incoming config
    is checked against this. This provides a single location to specify what
    input an object needs, and a way to verify the incoming config.

    Public API:
    get_default_config()
    is_this_config_valid()

    The derived class must:
        Specify a self.configspec as a class variable.
        Take in a  config object as a parameter to __init__, and
        Call the super constructor: Configurable.__init__()

    Configspec Examples:

        class MyNewClass(Configurable):
            configspec = [
            'channel=integer(min=0, max=9999, default=1)',
            'scpi_hostname=string(default=lookup_in_labconfig)',
            'port=integer(default=1234)',
            'gpib_address=integer(min=0, max=999, default=14)',
            'read_timeout_seconds=integer(min=0, max=100, default=3)',
            'connect_timeout_seconds=integer(min=0, max=100, default=10)'
            ]

        class ClassWithAllTheConfigTypes(Configurable):
            configspec = [
                "Number = integer(min=0, max=10, default=9)",
                "Float = float (min='0', max='1.111', default = '1.1')",
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
                # not useful for Configurable, which uses default extensively.
                #"MixedList = Do not use.
                "AlwaysOK = pass(default = None) ",
                "OptionList  = option('red', 'blue', 'green',default='red' )",
            ]

    Usage Example:
    config = complex_object_class.get_default_config()
    config['only param I want to change'] = 'new and better value'
    if complex_object_class.is_this_config_valid(config):
        co = complex_obj(config)

    A list of the available types from the configobj docs.

    * 'integer': matches integer values (including negative)
                 Takes optional 'min' and 'max' arguments : ::

                   integer()
                   integer(3, 9)  # any value from 3 to 9
                   integer(min=0) # any positive value
                   integer(max=9)

    * 'float': matches float values
               Has the same parameters as the integer check.

    * 'boolean': matches boolean values - ``True`` or ``False``
                 Acceptable string values for True are :
                   true, on, yes, 1
                 Acceptable string values for False are :
                   false, off, no, 0

                 Any other value raises an error.

    * 'ip_addr': matches an Internet Protocol address, v.4, represented
                 by a dotted-quad string, i.e. '1.2.3.4'.

    * 'string': matches any string.
                Takes optional keyword args 'min' and 'max'
                to specify min and max lengths of the string.

    * 'list': matches any list.
              Takes optional keyword args 'min', and 'max' to specify min and
              max sizes of the list. (Always returns a list.)

    * 'tuple': matches any tuple.
              Takes optional keyword args 'min', and 'max' to specify min and
              max sizes of the tuple. (Always returns a tuple.)

    * 'int_list': Matches a list of integers.
                  Takes the same arguments as list.

    * 'float_list': Matches a list of floats.
                    Takes the same arguments as list.

    * 'bool_list': Matches a list of boolean values.
                   Takes the same arguments as list.

    * 'ip_addr_list': Matches a list of IP addresses.
                     Takes the same arguments as list.

    * 'string_list': Matches a list of strings.
                     Takes the same arguments as list.

    #Mixed list does not have the default keyword, making this
    # not useful for Configurable, which uses defaults extensively.
    * 'mixed_list':  Not usable in Configurable.

    * 'pass': This check matches everything ! It never fails
              and the value is unchanged.

              It is also the default if no check is specified.

    * 'option': This check matches any from a list of options.
                You specify this check with : ::

                  option('option 1', 'option 2', 'option 3')

    """
    # The config spec(a ConfigObject term for the definition of the
    #  configuration)

    def __init__(self, input_config_data=None):
        """
        The configurable class defines an interface, but cannot
        be instantiated.

        Require the derived class to have self.configspec defined

        @param: input_config_data: Either a string or a list of string
                containing the configuration options and data.

        """
        try:
            # Explicitly require a self.configspec
            len(self.CONFIGSPEC) > 0
        except AttributeError:
            error_message = \
                    'This class needs but does not have a self.configspec'
            log.critical(error_message)
            raise ConfigurationError(error_message)

        # Check the configspec for sanity.
        self.CONFIGSPEC = self._convert_configspec_to_str_list(self.CONFIGSPEC)

        # Run get_default_config to verify the configspec is valid
        # We do this at construction to announce problems as early as possible
        default_config = self.get_default_config()

        # To allow for the config to be a subset of all the options,
        # combine the passed in config with the default values.
        # This way the incoming config could be empty, or have a single value.
        input_config_obj = configobj.ConfigObj(input_config_data)
        config = self._merge_two_configs(default_config, input_config_obj)

        if self.is_this_config_valid(config):
            # Convert the string values to ints and floats
            self.config = self._convert_strings_to_types(config)
        else:
            raise ConfigurationError(
                    'config data does not match the configspec of the object')

    @classmethod
    def _merge_two_configs(cls, base_config, extension_config):
        """
        Merges two configs.

        Example:
        base_config = {'temperature': 43, 'day': 'monday'}
        extension_config = {'temperature': 99, 'color': 'red'}
        returns :  {'temperature': 99, 'day': 'monday', 'color': 'red'}

        @param base_config:  ConfigObj

        @param extension_config:  ConfigObj

        @return: base_config filled in with data from extension_config.


        """
        assert isinstance(base_config, configobj.ConfigObj)
        assert isinstance(extension_config, configobj.ConfigObj)
        base_config.merge(extension_config)
        return base_config

    @classmethod
    def _get_items_in_config_not_in_configspec(cls, config):
        """
        @param config: ConfigObj

        @return: a list of items in config, but not in self.configspec.

        This happens when a config value is misspelled.

        """
        # Make a new ConfigObj of our configspec and the incoming config
        new_config = configobj.ConfigObj(
            dict(config), configspec=cls.CONFIGSPEC)
        validator = validate.Validator()
        new_config.validate(
            validator,
            preserve_errors=True, copy=True)
        extra_items = configobj.get_extra_values(new_config)
        return extra_items

    def _convert_strings_to_types(self, config):
        """
        @param config: ConfigObj

        @return: ConfigObj with values converted to the correct types

        """
        assert isinstance(config, configobj.ConfigObj)
        validator = validate.Validator()
        config.validate(validator, preserve_errors=True, copy=True)
        return config

    @classmethod
    def is_this_config_valid(cls, config):
        """
        Verify that config passes validation against self.configspec

        Raises an exception on bad configs.

        @param config: The config to check

        @return: True or False

        """
        if not isinstance(config, configobj.ConfigObj):
            raise ConfigurationError(
                    'Object passed into _is_this_config_valid is not a '
                    'ConfigObj')
        new_config = configobj.ConfigObj(
            dict(config),
            configspec=cls.CONFIGSPEC)
        validator = validate.Validator()
        validate_results = new_config.validate(validator,
                                               preserve_errors=True, copy=True)
        extra_items = configobj.get_extra_values(new_config)
        flattend_errors = configobj.flatten_errors(new_config, validate_results)

        if (validate_results is True) and not extra_items:
            return True

        # An invalid config may have bad keys, which means we can't convert
        # it to a string. If that happens, just print the keys.
        try:
            log.critical('This config is bad: %s ' % config)
        except KeyError:
            log.critical('This config with theses keys is bad: %s ' %
                         config.keys())

        log.critical('Above config must conform to this configspec: ')
        pretty_str = pprint.pformat(cls.CONFIGSPEC)
        log.critical('\n' + pretty_str)
        if len(extra_items) > 0:
            log.critical('Extra (mispelled?) items: ')
            for item in extra_items:
                log.critical(item)
        if len(flattend_errors) > 0:
            log.critical('Bad Values: ')
            for err in flattend_errors:
                    log.critical(err)
        return False

    @classmethod
    def _convert_configspec_to_str_list(cls, configspec):
        """
        Check the configspec for sanity.

        @param configspec: config spec of type str or list or Section

        @return: config spec of type list

        """
        if isinstance(configspec, list):
            return configspec
        if isinstance(configspec, configobj.ConfigObj):
            return configspec.write()
        else:
            raise ConfigurationError(
                'Configuration objects require ' +
                'self.configspec to be of type str or list, not %s' %
                type(configspec))

    @classmethod
    def get_default_config(cls):
        """
        @return: a ConfigObj with the default values filled in.

        """
        configspec = cls._convert_configspec_to_str_list(cls.CONFIGSPEC)
        try:
            config = configobj.ConfigObj(configspec=configspec)
            validator = validate.Validator()
            config.validate(validator, copy=True)
            # Other parts of the class expect this to return a ConfigObj
            assert isinstance(config, configobj.ConfigObj)
        except Exception as e:
            # Explicitly catch all types of errors. Any error raised
            # by the above code means the config was bad, and we should
            # stop and print out useful debugging info.
            pretty_str = pprint.pformat(configspec)
            log.critical('This configspec failed: \n%s ' % pretty_str)
            log.exception(e)
            raise ConfigurationError(e.message)
        return config
