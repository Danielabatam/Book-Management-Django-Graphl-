import graphene


class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hello")

    def resolve_hello(self, info):
        return "World"


schema = graphene.Schema(query=Query)
