from django.db.models import Field, Lookup
from django.db.models.lookups import In


@Field.register_lookup
class NotEqual(Lookup):
    lookup_name = "ne"

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        return "%s <> %s" % (lhs, rhs), params


@Field.register_lookup
class NotIn(In):
    lookup_name = "notin"

    def get_rhs_op(self, connection, rhs):
        return "NOT IN %s" % rhs
