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
from .BlockDurationDto import BlockDurationDto
from .NamespaceIdDto import NamespaceIdDto
from .NamespaceRegistrationTypeDto import NamespaceRegistrationTypeDto

def to_hex_string(bin):
    return hexlify(bin).decode('utf-8')

class NamespaceRegistrationTransactionBodyBuilder:
    """Binary layout for a namespace registration transaction.

    Attributes:
        duration: Namespace duration.
        parent_id: Parent namespace identifier.
        id: Namespace identifier.
        registration_type: Namespace registration type.
        name: Namespace name.
    """
    def __init__(self):
        """ Constructor."""
        self.duration = BlockDurationDto().blockDuration
        self.parent_id = NamespaceIdDto().namespaceId
        self.id = NamespaceIdDto().namespaceId
        self.registration_type = NamespaceRegistrationTypeDto(0).value
        self.name = bytes()

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> NamespaceRegistrationTransactionBodyBuilder:
        """Creates an instance of NamespaceRegistrationTransactionBodyBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of NamespaceRegistrationTransactionBodyBuilder.
        """
        bytes_ = bytes(payload)
        registrationTypeCondition = bytes_[0:8]
        bytes_ = bytes_[8:]

        id_ = NamespaceIdDto.loadFromBinary(bytes_)  # kind:CUSTOM1_byte
        id = id_.namespaceId
        bytes_ = bytes_[id_.getSize():]
        registration_type_ = NamespaceRegistrationTypeDto.loadFromBinary(bytes_)  # kind:CUSTOM2
        registration_type = registration_type_.value
        bytes_ = bytes_[registration_type_.getSize():]
        name_size = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 1))  # kind:SIZE_FIELD
        bytes_ = bytes_[1:]
        name = GeneratorUtils.getBytes(bytes_, name_size)  # kind:BUFFER
        bytes_ = bytes_[name_size:]
        duration = None
        if registration_type == NamespaceRegistrationTypeDto.ROOT.value:
            duration = BlockDurationDto.loadFromBinary(registrationTypeCondition).blockDuration  # kind:CUSTOM3
        parent_id = None
        if registration_type == NamespaceRegistrationTypeDto.CHILD.value:
            parent_id = NamespaceIdDto.loadFromBinary(registrationTypeCondition).namespaceId  # kind:CUSTOM3

        # create object and call
        result = NamespaceRegistrationTransactionBodyBuilder()
        result.duration = duration
        result.parent_id = parent_id
        result.id = id
        result.registration_type = registration_type
        result.name = name
        return result

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = 0
        if self.registration_type == NamespaceRegistrationTypeDto.ROOT.value:
            size += BlockDurationDto(self.duration).getSize()
        if self.registration_type == NamespaceRegistrationTypeDto.CHILD.value:
            size += NamespaceIdDto(self.parent_id).getSize()
        size += NamespaceIdDto(self.id).getSize()
        size += NamespaceRegistrationTypeDto(self.registration_type).getSize()
        size += 1  # name_size
        size += len(self.name)
        return size

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        if self.registration_type == NamespaceRegistrationTypeDto.ROOT.value:
            bytes_ = GeneratorUtils.concatTypedArrays(bytes_, BlockDurationDto(self.duration).serialize())  # kind:CUSTOM
        if self.registration_type == NamespaceRegistrationTypeDto.CHILD.value:
            bytes_ = GeneratorUtils.concatTypedArrays(bytes_, NamespaceIdDto(self.parent_id).serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, NamespaceIdDto(self.id).serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, NamespaceRegistrationTypeDto(self.registration_type).serialize())  # kind:CUSTOM
        size_value = len(self.name)
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(size_value, 1))  # kind:SIZE_FIELD
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.name)  # kind:BUFFER
        return bytes_

    def __str__(self):
        """Returns nice representation.
        Returns:
            Printable string
        """
        result = ''
        if self.registration_type == NamespaceRegistrationTypeDto.ROOT.value:
            result += '{:24s} : {}\n'.format('duration', to_hex_string(BlockDurationDto(self.duration).serialize()))
        if self.registration_type == NamespaceRegistrationTypeDto.CHILD.value:
            result += '{:24s} : {}\n'.format('parentId', to_hex_string(NamespaceIdDto(self.parent_id).serialize()))
        result += '{:24s} : {}\n'.format('id', to_hex_string(NamespaceIdDto(self.id).serialize()))
        result += '{:24s} : {}\n'.format('registrationType', to_hex_string(NamespaceRegistrationTypeDto(self.registration_type).serialize()))
        size_value = len(self.name)
        result += '{:24s} : {}\n'.format('nameSize', to_hex_string(GeneratorUtils.uintToBuffer(size_value, 1)))
        result += '{:24s} : {}\n'.format('name', to_hex_string(self.name))
        return result
