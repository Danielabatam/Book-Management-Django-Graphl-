import graphene
from graphene_django import DjangoObjectType

from books.models import Book


class BookType(DjangoObjectType):
    class Meta:
        model = Book
        fields = ("id", "title", "description", "created_at", "updated_at")


class CreateBookMutation(graphene.Mutation):
    class Arguments:
        # title = graphene.String()
        title = graphene.String(required=True)
        description = graphene.String()

    book = graphene.Field(BookType)

    def mutate(self, info, title, description):
        book = Book(title=title, description=description)
        book.save()
        return CreateBookMutation(book=book)


class DeleteBookMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    message = graphene.String()

    def mutate(self, info, id):
        book = Book.objects.get(pk=id)
        book.delete()
        return DeleteBookMutation(message="Book deleted")


class UpdateMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String()
        description = graphene.String()

    book = graphene.Field(BookType)

    # message = graphene.String()

    def mutate(self, info, id, title, description):
        book = Book.objects.get(pk=id)
        book.title = title
        book.description = description
        book.save()
        return UpdateMutation(book=book)


class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hello")
    books = graphene.List(BookType)
    book = graphene.Field(BookType, id=graphene.ID())

    # def resolve_hello(self, info):
    #  return "World"

    def resolve_books(self, info):
        return Book.objects.all()

    def resolve_book(self, info, id):
        return Book.objects.get(pk=id)


class Mutation(graphene.ObjectType):
    # create_book = graphene.Field(BookType, title=graphene.String(), description=graphene.String())
    create_book = CreateBookMutation.Field()
    delete_book = DeleteBookMutation.Field()
    update_book = UpdateMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)

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

# ================= Graph QL Mutation ================= #
# mutation {
#     createBook (
#         title: "Mon premier livre",
#     description: "Il s'agit de la description de mon premier livre"
# ){
#     book {
#     id
# title
# description
# createdAt
# updatedAt
# }
# }
# }


# mutation{
#     deleteBook(id:5){
#     message
# }
# }


# mutation{
#     updateBook(
#       id:5,
#         title: "Titre (updated)"
#         description: "Description (updated)"
#     ){
#       book {
#           id
#           title
#           description
#       }
# }

# ================= Mutation Test ================= #

# python manage.py shell


# import graphene
# from BookManagement.schema import CreateBookMutation
#
# # Créez une instance de la mutation
# mutation = CreateBookMutation()
#
# # Définissez les informations et les arguments nécessaires pour la mutation
# info = None  # Remplacez ceci par les informations nécessaires pour la mutation
# title = "Mon premier livre"
# description = "Il s'agit de la description de mon premier livre"
#
# # Exécutez la mutation
# result = mutation.mutate(info, title, description)
#
# # Imprimez le résultat pour voir le livre créé
# print(result.book)
