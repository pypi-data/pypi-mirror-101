from slugify import slugify

from .scalars import Property
from ..exceptions import PentaQuarkValidationError


class ComputedProperty(Property):
    def __init__(self, func, graphql_type="String", **kwargs):
        super().__init__(**kwargs)
        self.func = func
        self.graphql_type = graphql_type

    def _validate(self, *args, **kwargs):
        try:
            __value = self.func(**kwargs)
        except Exception as e:
            raise PentaQuarkValidationError(e)
        return super()._validate(__value, **kwargs)


class SlugProperty(ComputedProperty):
    def __init__(self, source, **kwargs):
        def func(**kws):
            v = kws.get(source)
            if v is None:
                return v
            return slugify(kws.get(source))
        super().__init__(func, **kwargs)
