from dataclasses import dataclass, field
from typing import Mapping, Self, Sequence
from uuid import RFC_4122, UUID, uuid4

BASE57_ALPHABET = "23456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
BASE57_UUID_LENGTH = 22  # ceil(128 / log2(57))


class ID:
    uuid: UUID

    def __init__(self, string_or_uuid: str | UUID):
        if isinstance(string_or_uuid, UUID):
            object.__setattr__(self, "uuid", string_or_uuid)
        elif isinstance(string_or_uuid, str):
            return self.__init_from_string__(string_or_uuid)
        else:
            msg = f"ID cannot be constructed from type {type(string_or_uuid)}"
            raise TypeError(msg)

    def __init_from_string__(self, string: str):
        int_ = base57_encoder.decode(string)
        try:
            uuid = UUID(int=int_)
        except ValueError:
            msg = f"Invalid UUID value {int_}"
            raise IDDecodeException(msg)
        if uuid.variant != RFC_4122:
            msg = f"UUID is not RFC4122-compliant (variant={uuid.variant})"
            raise IDDecodeException(msg)
        if uuid.version != 4:
            msg = f"UUID is not version 4 (version={uuid.version})"
            raise IDDecodeException(msg)
        object.__setattr__(self, "uuid", uuid)

    @classmethod
    def generate_random(cls) -> Self:
        return cls(uuid4())

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, ID):
            return NotImplemented
        return self.uuid == value.uuid

    def __hash__(self) -> int:
        return hash(self.uuid)

    def __int__(self):
        return int(self.uuid)

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, str(self))

    def __setattr__(self, name, value) -> None:
        raise AttributeError("ID objects are immutable")

    def __str__(self) -> str:
        return base57_encoder.encode(self.uuid.int)


@dataclass(frozen=True)
class _Encoder:
    alphabet: Sequence[str]
    fixed_length: int
    digit_lookup_map: Mapping[str, int] = field(
        init=False, repr=False, compare=False, hash=False
    )

    def __post_init__(self):
        assert self.alphabet
        assert self.fixed_length > 0
        digit_lookup_map = {ch: i for i, ch in enumerate(self.alphabet)}
        object.__setattr__(self, "digit_lookup_map", digit_lookup_map)

    def encode(self, number: int) -> str:
        buffer = [self.alphabet[0]] * self.fixed_length
        for i in reversed(range(self.fixed_length)):
            if not number:
                break
            number, digit = divmod(number, len(self.alphabet))
            buffer[i] = self.alphabet[digit]
        return "".join(buffer)

    def decode(self, string: str) -> int:
        number = 0
        for ch in string:
            try:
                digit = self.digit_lookup_map[ch]
            except ValueError:
                raise IDDecodeException("Invalid digit for alphabet", ch, self.alphabet)
            number = number * len(self.alphabet) + digit
        return number


class IDDecodeException(ValueError):
    """Raised when an ID cannot be decoded."""


base57_encoder = _Encoder(BASE57_ALPHABET, BASE57_UUID_LENGTH)
