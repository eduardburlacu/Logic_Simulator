import pytest
from names import Names


@pytest.fixture
def new_names():
    """Return a new names instance."""
    return Names()


@pytest.fixture
def name_string_list():
    """Return a list of example names."""
    return ["Leah", "Jack", "Bob"]


@pytest.fixture
def used_names(name_string_list):
    """Return a names instance, after three names have been added."""
    my_name = Names()
    for name in name_string_list:
        my_name.lookup([name])
    return my_name


def test_get_name_string_raises_exceptions(used_names):
    """Test if get_string raises expected exceptions."""
    with pytest.raises(TypeError):
        used_names.get_name_string(1.4)
    with pytest.raises(TypeError):
        used_names.get_name_string("hello")


@pytest.mark.parametrize("name_id, expected_string", [
    (0, "Leah"),
    (1, "Jack"),
    (2, "Bob"),
])
def test_get_name_string(new_names, name_string_list,
                         used_names, name_id, expected_string):
    """Test if get_string returns the expected string."""
    assert used_names.get_name_string(name_id) == expected_string
    assert new_names.get_name_string(name_id) is None


@pytest.mark.parametrize("query_name, expected_id", [
    ("Leah", 0),
    ("Jack", 1),
    ("Bob", 2),
])
def test_query(new_names, name_string_list, used_names,
               query_name, expected_id):
    assert used_names.query(query_name) == expected_id
    assert new_names.query(query_name) is None


def test_lookup_add(used_names):
    """Checks that lookup adds a name if it is not already in the class"""
    original_length = len(used_names.names_list)
    used_names.lookup(["Edi"])
    new_length = len(used_names.names_list)
    assert new_length == original_length + 1


def test_unique_error_codes_raises_exceptions(new_names):
    """Test if unique_error_codes raises expected exceptions."""
    with pytest.raises(TypeError):
        new_names.unique_error_codes(1.4)


@pytest.mark.parametrize(
    "num_error_codes, error_codes", [(0, []), (1, [0]), (2, [0, 1])]
)
def test_unique_error_codes(
    new_names, used_names, num_error_codes, error_codes
):
    """Test if unique_error_codes behaves as expected."""
    assert list(new_names.unique_error_codes(num_error_codes)) == error_codes
    assert list(used_names.unique_error_codes(num_error_codes)) == [
        c for c in error_codes
    ]
