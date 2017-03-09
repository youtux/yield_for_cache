import functools
import inspect


def dict_get_or_create(dict, key, creator):
    if key in dict:
        return dict[key]

    value = creator()
    dict[key] = value

    return value


def yield_for_cache(get_or_create_function):
    def cache_yield(function):
        if not inspect.isgeneratorfunction(function):
            raise TypeError('The decorated function should be a generator function.')

        @functools.wraps(function)
        def impl(*args, **kwargs):
            gen = function(*args, **kwargs)

            cache_key = next(gen)

            if cache_key is None:
                return next(gen)

            return get_or_create_function(key=cache_key, creator=lambda: next(gen))

        return impl
    return cache_yield
