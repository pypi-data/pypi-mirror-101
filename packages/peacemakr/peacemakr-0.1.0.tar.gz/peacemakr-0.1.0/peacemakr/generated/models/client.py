# coding: utf-8

"""
    Peacemakr

    This API describes the Peacemakr services, which enable seamless application layer encryption and verification.  # noqa: E501

    OpenAPI spec version: 1.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from peacemakr.generated.models.public_key import PublicKey  # noqa: F401,E501


class Client(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'id': 'str',
        'sdk': 'str',
        'preferred_public_key_id': 'str',
        'public_keys': 'list[PublicKey]'
    }

    attribute_map = {
        'id': 'id',
        'sdk': 'sdk',
        'preferred_public_key_id': 'preferredPublicKeyId',
        'public_keys': 'publicKeys'
    }

    def __init__(self, id=None, sdk=None, preferred_public_key_id=None, public_keys=None):  # noqa: E501
        """Client - a model defined in Swagger"""  # noqa: E501

        self._id = None
        self._sdk = None
        self._preferred_public_key_id = None
        self._public_keys = None
        self.discriminator = None

        self.id = id
        if sdk is not None:
            self.sdk = sdk
        if preferred_public_key_id is not None:
            self.preferred_public_key_id = preferred_public_key_id
        self.public_keys = public_keys

    @property
    def id(self):
        """Gets the id of this Client.  # noqa: E501


        :return: The id of this Client.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Client.


        :param id: The id of this Client.  # noqa: E501
        :type: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def sdk(self):
        """Gets the sdk of this Client.  # noqa: E501


        :return: The sdk of this Client.  # noqa: E501
        :rtype: str
        """
        return self._sdk

    @sdk.setter
    def sdk(self, sdk):
        """Sets the sdk of this Client.


        :param sdk: The sdk of this Client.  # noqa: E501
        :type: str
        """

        self._sdk = sdk

    @property
    def preferred_public_key_id(self):
        """Gets the preferred_public_key_id of this Client.  # noqa: E501

        of all the public keys KeyDeriver's should deliver to this public key - it is also the most recently added public key  # noqa: E501

        :return: The preferred_public_key_id of this Client.  # noqa: E501
        :rtype: str
        """
        return self._preferred_public_key_id

    @preferred_public_key_id.setter
    def preferred_public_key_id(self, preferred_public_key_id):
        """Sets the preferred_public_key_id of this Client.

        of all the public keys KeyDeriver's should deliver to this public key - it is also the most recently added public key  # noqa: E501

        :param preferred_public_key_id: The preferred_public_key_id of this Client.  # noqa: E501
        :type: str
        """

        self._preferred_public_key_id = preferred_public_key_id

    @property
    def public_keys(self):
        """Gets the public_keys of this Client.  # noqa: E501


        :return: The public_keys of this Client.  # noqa: E501
        :rtype: list[PublicKey]
        """
        return self._public_keys

    @public_keys.setter
    def public_keys(self, public_keys):
        """Sets the public_keys of this Client.


        :param public_keys: The public_keys of this Client.  # noqa: E501
        :type: list[PublicKey]
        """
        if public_keys is None:
            raise ValueError("Invalid value for `public_keys`, must not be `None`")  # noqa: E501

        self._public_keys = public_keys

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(Client, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, Client):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
