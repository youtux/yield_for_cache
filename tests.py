import functools

import mock
import pytest

import yield_for_cache


@pytest.fixture
def cache_type():
    return 'dict'


@pytest.fixture
def cache(cache_type):
    if cache_type == 'dict':
        return {}
    else:
        raise NotImplementedError


@pytest.fixture
def get_or_create(cache_type, cache):
    if cache_type == 'dict':
        return functools.partial(yield_for_cache.dict_get_or_create, dict=cache)
    else:
        raise NotImplementedError


def test_refuse_to_decorate_normal_function():
    get_or_create = mock.NonCallableMock()
    decorator = yield_for_cache.yield_for_cache(get_or_create)

    with pytest.raises(TypeError):
        @decorator
        def under_test():
            return 'ok'


def test_key_in_cache(get_or_create, cache):
    cache['a cache key'] = 'value'

    @yield_for_cache.yield_for_cache(get_or_create)
    def under_test():
        yield 'a cache key'
        raise ValueError('This should not be reached')

    assert under_test() == 'value'
    assert cache.get('a cache key') == 'value'


def test_key_not_in_cache(get_or_create, cache):
    @yield_for_cache.yield_for_cache(get_or_create)
    def under_test():
        yield 'a cache key'
        yield 'ok'

    assert under_test() == 'ok'
    assert cache.get('a cache key') == 'ok'


def test_yield_no_key():
    get_or_create = mock.NonCallableMock()

    @yield_for_cache.yield_for_cache(get_or_create)
    def under_test():
        yield
        yield 'ok'

    assert under_test() == 'ok'


def test_yield_key_none():
    get_or_create = mock.NonCallableMock()

    @yield_for_cache.yield_for_cache(get_or_create)
    def under_test():
        yield None
        yield 'ok'

    assert under_test() == 'ok'


def test_propagates_exception_before_key():
    get_or_create = mock.NonCallableMock()

    exception = ValueError('an exception')

    @yield_for_cache.yield_for_cache(get_or_create)
    def under_test():
        raise exception

    with pytest.raises(ValueError) as e:
        under_test()

    assert e.value == exception


def test_propagates_exception_after_key(cache, get_or_create):
    exception = ValueError('an exception')

    @yield_for_cache.yield_for_cache(get_or_create)
    def under_test():
        yield 'a cache key'
        raise exception

    with pytest.raises(ValueError) as e:
        under_test()

    assert e.value == exception
    assert cache.get('a cache key') is None


def test_execution_stops_after_second_yield(cache, get_or_create):
    empty_list = []

    @yield_for_cache.yield_for_cache(get_or_create)
    def under_test():
        yield 'a cache key'
        yield 'ok'
        empty_list.append(42)
        raise ValueError('This should not be reached')

    assert under_test() == 'ok'

    assert cache.get('a cache key') == 'ok'
    assert not empty_list
