__all__ = ("is_jnull", "QueryDict")

from jnius import autoclass


def is_jnull(obj):
    Objects = autoclass("java.util.Objects")
    return Objects.isNull(obj)


class QueryDict(dict):
    '''QueryDict is a dict() that can be queried with dot.

    ::

        d = QueryDict()
        # create a key named toto, with the value 1
        d.toto = 1
        # it's the same as
        d['toto'] = 1

    .. versionadded:: 1.0.4
    '''

    def __getattr__(self, attr):
        try:
            return self.__getitem__(attr)
        except KeyError:
            raise AttributeError("%r object has no attribute %r" % (
                self.__class__.__name__, attr))

    def __setattr__(self, attr, value):
        self.__setitem__(attr, value)
