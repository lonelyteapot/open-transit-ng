import pytest

from opentransit.models.id import ID


def test_id_encode_decode_equal():
    id1 = ID.generate_random()
    id1_str = str(id1)
    assert len(id1_str) == 22
    id2 = ID(id1_str)
    id2_str = str(id2)
    assert id1 == id2
    assert id1_str == id2_str


def test_id_from_int_raises():
    with pytest.raises(TypeError):
        ID(12345678901234567890)  # type: ignore
