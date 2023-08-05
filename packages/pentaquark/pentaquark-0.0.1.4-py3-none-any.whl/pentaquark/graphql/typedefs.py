"""
Needed to build a graphql api:
- types
- input types
- queries
- mutations

Goal: make GraphQL customizable, while keeping the number of queries as small as possible
"""
import enum
from pentaquark.graphql.mixins import GraphQLTypeBuilder

ALL_FIELDS = "__all_fields__"
ALL_RELATIONSHIPS = "__all_relationships__"


class TypeDefsTypes(enum.Enum):
    TYPE = "type"
    INPUT = "input"
    QUERY = "query"
    MUTATION = "mutation"


def register(klass):
    # register type (?)
    return klass


class GQLType:
    field = None  # extra fields

    class Meta:
        model = None
        type = False
        include_fields = ALL_FIELDS
        include_relationships = ALL_RELATIONSHIPS
        required_fields = None
        exclude_fields = None

    def __init__(self):
        pass

    def to_graphql(self):
        gql_builder = GraphQLTypeBuilder(self.Meta.model)
        if self.Meta.type == TypeDefsTypes.INPUT:
            return gql_builder.to_graphql_input_type()
        if self.Meta.type == TypeDefsTypes.TYPE:
            return gql_builder.to_graphql_type()
        # if self.type == TypeDefsTypes.QUERY:
        #     return gql_builder.to_graphql_queries()
        # if self.type == TypeDefsTypes.MUTATION:
        #     return gql_builder.to_graphql_mutations()
        raise Exception(f"{self.Meta.type} not known, must be an instance of TypeDefsTypes")


class GQLQuery:

    class Meta:
        name = ""
        model = None
        input_type = None
        return_type = None
        return_multiple = False

    def get_name(self):
        return self.Meta.name or self.Meta.model.get_label()

    def resolve(self, obj, info, **kwargs):
        pass

    def to_graphql(self):
        gql_builder = GraphQLTypeBuilder(self.Meta.model)
        return gql_builder.to_graphql_queries()


# import enum
#
#
# class ValidationError(Exception):
#     pass
#
#
# class TypeDefsTypes(enum.Enum):
#     TYPE = "type"
#     INPUT = "input"
#     QUERY = "query"
#     MUTATION = "mutation"
#
#
# class TypeDef:
#     def __init__(self, name, properties, args=None, typ=TypeDefsTypes.TYPE, resolver=None):
#         self.type = typ
#         self.name = name
#         self.properties = properties
#         self.args = args
#         self.resolver = None
#
#     def _to_prop_list(self):
#         return "\n".join(
#             f"{k}: {v}" for k, v in self.properties.items()
#         )
#
#     def _to_arg_list(self):
#         return ",".join(
#             f"{k}: {v}" for k, v in self.args.items()
#         )
#
#     def _to_prefix(self):
#         if self.args:
#             return f"{self.type.value} ({self._to_arg_list()})"
#         return self.type.value
#
#     def to_graphql(self):
#         return f"""{self._to_prefix()} {{
#             {self._to_prop_list()}
#         }}
#         """
#
#     def bin_resolver(self, func):
#         self.resolver = func
#
#
# class QueryDef(TypeDef):
#     def __init__(self, name, args=None, properties=None, resolver=None):
#         super().__init__(name, properties, args, TypeDefsTypes.QUERY, resolver)
#
#
# class MutationDef(TypeDef):
#     def __init__(self, name, args, properties, resolver):
#         super().__init__(name, properties, args, TypeDefsTypes.MUTATION, resolver)
#
#
# class ModelTypeDef(TypeDef):
#     class Meta:
#         model = None
#
#     def __init__(self, model, name=None, args=None, properties=None, type=TypeDefsTypes.TYPE):
#         super().__init__(name, args, properties, type)
#         self.model = model
#         if self.name is None:
#             self.name = model.get_graphql_type()
#         if self.args is None:
#             self.args = model.get_property_graphql_type()
#         if self.properties is None:
#             self.properties = model.get_property_graphql_type()
#         self._validate()
#
#     def _validate(self):
#         for a in self.args:
#             if a not in self.model._properties:
#                 raise ValidationError()
#         for p in self.properties:
#             if p not in self.model._properties:
#                 raise ValidationError()
