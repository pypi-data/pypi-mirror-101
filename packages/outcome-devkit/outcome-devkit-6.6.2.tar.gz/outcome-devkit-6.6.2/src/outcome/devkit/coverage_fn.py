"""These functions only exist to test the dynamic coverage."""


def fn_only_covered_in_unit():  # pragma: only-covered-in-unit-tests
    return True


def fn_only_covered_in_integration():  # pragma: only-covered-in-integration-tests
    return True


# This line is here to ensure that there is always 1 line of coverage for the file
marker = True
