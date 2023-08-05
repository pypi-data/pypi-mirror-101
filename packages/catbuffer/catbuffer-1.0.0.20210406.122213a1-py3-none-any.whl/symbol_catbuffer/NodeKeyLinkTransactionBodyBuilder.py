#!/usr/bin/python
"""
    Copyright (c) 2016-2019, Jaguar0625, gimre, BloodyRookie, Tech Bureau, Corp.
    Copyright (c) 2020-present, Jaguar0625, gimre, BloodyRookie.

    This file is part of Catapult.

    Catapult is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Catapult is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with Catapult. If not, see <http://www.gnu.org/licenses/>.
"""

# pylint: disable=W0622,W0612,C0301,R0904

from __future__ import annotations

# pylint: disable=unused-import

from binascii import hexlify
import re
from .GeneratorUtils import GeneratorUtils
from .KeyDto import KeyDto
from .LinkActionDto import LinkActionDto

def to_hex_string(bin):
    return hexlify(bin).decode('utf-8')

class NodeKeyLinkTransactionBodyBuilder:
    """Binary layout for a node key link transaction.

    Attributes:
        linked_public_key: Linked public key.
        link_action: Link action.
    """
    def __init__(self):
        """ Constructor."""
        self.linked_public_key = bytes(32)
        self.link_action = LinkActionDto(0).value

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> NodeKeyLinkTransactionBodyBuilder:
        """Creates an instance of NodeKeyLinkTransactionBodyBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of NodeKeyLinkTransactionBodyBuilder.
        """
        bytes_ = bytes(payload)

        linked_public_key_ = KeyDto.loadFromBinary(bytes_)  # kind:CUSTOM1_byte
        linked_public_key = linked_public_key_.key
        bytes_ = bytes_[linked_public_key_.getSize():]
        link_action_ = LinkActionDto.loadFromBinary(bytes_)  # kind:CUSTOM2
        link_action = link_action_.value
        bytes_ = bytes_[link_action_.getSize():]

        # create object and call
        result = NodeKeyLinkTransactionBodyBuilder()
        result.linked_public_key = linked_public_key
        result.link_action = link_action
        return result

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = 0
        size += KeyDto(self.linked_public_key).getSize()
        size += LinkActionDto(self.link_action).getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, KeyDto(self.linked_public_key).serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, LinkActionDto(self.link_action).serialize())  # kind:CUSTOM
        return bytes_

    def __str__(self):
        """Returns nice representation.
        Returns:
            Printable string
        """
        result = ''
        result += '{:24s} : {}\n'.format('linkedPublicKey', to_hex_string(KeyDto(self.linked_public_key).serialize()))
        result += '{:24s} : {}\n'.format('linkAction', to_hex_string(LinkActionDto(self.link_action).serialize()))
        return result
