import graphene
from graphene_django import DjangoObjectType

from books.models import Book


class BookType(DjangoObjectType):
    class Meta:
        model = Book
        fields = ("id", "title", "description", "created_at", "updated_at")


class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hello")
    books = graphene.List(BookType)
    book = graphene.Field(BookType, id=graphene.ID())  # Pourquoi ID() et non Int()

    # def resolve_hello(self, info):
    #  return "World"

    def resolve_books(self, info):
        return Book.objects.all()

    def resolve_book(self, info, id):
        return Book.objects.get(pk=id) # Pourquoi  (pk=id) et non (id=id)


schema = graphene.Schema(query=Query)

# ================= Graph QL Query ================= #

# {
#   books {
#     id
#     title
#     description
#     createdAt
#     updatedAt
#   }
# }

# {
#     book(id:5){
#     id
# title
# }
# }
