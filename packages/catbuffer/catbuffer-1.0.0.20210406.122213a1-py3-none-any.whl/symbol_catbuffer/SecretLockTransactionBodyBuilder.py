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
from .Hash256Dto import Hash256Dto
from .LockHashAlgorithmDto import LockHashAlgorithmDto
from .UnresolvedAddressDto import UnresolvedAddressDto
from .UnresolvedMosaicBuilder import UnresolvedMosaicBuilder

def to_hex_string(bin):
    return hexlify(bin).decode('utf-8')

class SecretLockTransactionBodyBuilder:
    """Binary layout for a secret lock transaction.

    Attributes:
        recipient_address: Locked mosaic recipient address.
        secret: Secret.
        mosaic: Locked mosaic.
        duration: Number of blocks for which a lock should be valid.
        hash_algorithm: Hash algorithm.
    """
    def __init__(self):
        """ Constructor."""
        self.recipient_address = bytes(24)
        self.secret = bytes(32)
        self.mosaic = None # UnresolvedMosaicBuilder
        self.duration = BlockDurationDto().blockDuration
        self.hash_algorithm = LockHashAlgorithmDto(0).value

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> SecretLockTransactionBodyBuilder:
        """Creates an instance of SecretLockTransactionBodyBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of SecretLockTransactionBodyBuilder.
        """
        bytes_ = bytes(payload)

        recipient_address_ = UnresolvedAddressDto.loadFromBinary(bytes_)  # kind:CUSTOM1_byte
        recipient_address = recipient_address_.unresolvedAddress
        bytes_ = bytes_[recipient_address_.getSize():]
        secret_ = Hash256Dto.loadFromBinary(bytes_)  # kind:CUSTOM1_byte
        secret = secret_.hash256
        bytes_ = bytes_[secret_.getSize():]
        mosaic = UnresolvedMosaicBuilder.loadFromBinary(bytes_)  # kind:CUSTOM1_nonbyte
        bytes_ = bytes_[mosaic.getSize():]
        mosaic = mosaic.as_tuple()
        duration_ = BlockDurationDto.loadFromBinary(bytes_)  # kind:CUSTOM1_byte
        duration = duration_.blockDuration
        bytes_ = bytes_[duration_.getSize():]
        hash_algorithm_ = LockHashAlgorithmDto.loadFromBinary(bytes_)  # kind:CUSTOM2
        hash_algorithm = hash_algorithm_.value
        bytes_ = bytes_[hash_algorithm_.getSize():]

        # create object and call
        result = SecretLockTransactionBodyBuilder()
        result.recipient_address = recipient_address
        result.secret = secret
        result.mosaic = mosaic
        result.duration = duration
        result.hash_algorithm = hash_algorithm
        return result

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = 0
        size += UnresolvedAddressDto(self.recipient_address).getSize()
        size += Hash256Dto(self.secret).getSize()
        size += UnresolvedMosaicBuilder.from_tuple(self.mosaic).getSize()
        size += BlockDurationDto(self.duration).getSize()
        size += LockHashAlgorithmDto(self.hash_algorithm).getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, UnresolvedAddressDto(self.recipient_address).serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, Hash256Dto(self.secret).serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, UnresolvedMosaicBuilder.from_tuple(self.mosaic).serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, BlockDurationDto(self.duration).serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, LockHashAlgorithmDto(self.hash_algorithm).serialize())  # kind:CUSTOM
        return bytes_

    def __str__(self):
        """Returns nice representation.
        Returns:
            Printable string
        """
        result = ''
        result += '{:24s} : {}\n'.format('recipientAddress', to_hex_string(UnresolvedAddressDto(self.recipient_address).serialize()))
        result += '{:24s} : {}\n'.format('secret', to_hex_string(Hash256Dto(self.secret).serialize()))
        result += '{:24s} : {}\n'.format('mosaic', to_hex_string(UnresolvedMosaicBuilder.from_tuple(self.mosaic).serialize()))
        result += '{:24s} : {}\n'.format('duration', to_hex_string(BlockDurationDto(self.duration).serialize()))
        result += '{:24s} : {}\n'.format('hashAlgorithm', to_hex_string(LockHashAlgorithmDto(self.hash_algorithm).serialize()))
        return result
