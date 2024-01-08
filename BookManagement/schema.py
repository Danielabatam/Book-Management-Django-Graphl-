import graphene
from graphene_django import DjangoObjectType

from books.models import Book


class BookType(DjangoObjectType):
    """
    This class represents a Book in the Graphene API.

    Args:
        model (Model): The Django model that this type represents.
        fields (list): A list of field names that should be included in the GraphQL type.

    Returns:
        GraphQL type: A GraphQL type that represents a Book.
    """

    class Meta:
        model = Book
        fields = ("id", "title", "description", "created_at", "updated_at")


class CreateBookMutation(graphene.Mutation):
    """
    This class represents a CreateBookMutation in the Graphene API.

    Args:
        title (str): The title of the book.
        description (str): The description of the book.

    Returns:
        Book: The created book.
    """

    class Arguments:
        """
        This class represents the arguments of the CreateBookMutation.

        Args:
            title (str): The title of the book.
            description (str): The description of the book.
        """
        title = graphene.String(required=True)
        description = graphene.String()

    def mutate(self, info, title, description):
        """
        This method creates a new book.

        Args:
            info (object): The context of the mutation.
            title (str): The title of the book.
            description (str): The description of the book.

        Returns:
            Book: The created book.
        """
        book = Book(title=title, description=description)
        book.save()
        return CreateBookMutation(book=book)


class CreateBookMutation(graphene.Mutation):
    class Arguments:
        """
    This class represents a CreateBookMutation in the Graphene API.

    Args:
        title (str): The title of the book.
        description (str): The description of the book.

    Returns:
        Book: The created book.
    """

    class Arguments:
        """
        This class represents the arguments of the CreateBookMutation.

        Args:
            title (str): The title of the book.
            description (str): The description of the book.
        """
        title = graphene.String(required=True)
        description = graphene.String()

    def mutate(self, info, title, description):
        """
        This method creates a new book.

        Args:
            info (object): The context of the mutation.
            title (str): The title of the book.
            description (str): The description of the book.

        Returns:
            Book: The created book.
        """
        book = Book(title=title, description=description)
        book.save()
        return CreateBookMutation(book=book)
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
    """
    This class represents an UpdateMutation in the Graphene API.

    Args:
        id (str): The ID of the book to update.
        title (str): The new title of the book.
        description (str): The new description of the book.

    Returns:
        Book: The updated book.
    """

    class Arguments:
        """
        This class represents the arguments of the UpdateMutation.

        Args:
            id (str): The ID of the book to update.
            title (str): The new title of the book.
            description (str): The new description of the book.
        """
        id = graphene.ID(required=True)
        title = graphene.String()
        description = graphene.String()

    book = graphene.Field(BookType)

    def mutate(self, info, id, title, description):
        """
        This method updates an existing book.

        Args:
            info (object): The context of the mutation.
            id (str): The ID of the book to update.
            title (str): The new title of the book.
            description (str): The new description of the book.

        Returns:
            Book: The updated book.
        """
        book = Book.objects.get(pk=id)
        book.title = title
        book.description = description
        book.save()
        return UpdateMutation(book=book)


class Query(graphene.ObjectType):
    """A Graphene Object Type that represents the root of the query tree.

    This class defines the fields that can be accessed at the root of the query tree.
    These fields correspond to the various queries that can be made against the database.

    Args:
        graphene.ObjectType: A Graphene Object Type that represents a collection of fields.

    Attributes:
        hello (graphene.String): A field that returns a string containing the text "Hello".
        books (graphene.List): A field that returns a list of books.
        book (graphene.Field): A field that returns a single book.
    """


    # hello = graphene.String(default_value="Hello")
    # books = graphene.List(BookType)
    # book = graphene.Field(BookType, id=graphene.ID())

    hello = graphene.String(
        """A field that returns a string containing the text "Hello".""",
        default_value="Hello"
    )

    books = graphene.List(
        """A field that returns a list of books.""",
        of=graphene.Field(BookType)
    )

    book = graphene.Field(
        """A field that returns a single book.""",
        BookType,
        id=graphene.ID(
            """The ID of the book to retrieve."""
        )
    )

    def resolve_hello(self, info):
        """A method that returns a string containing the text "Hello"."""
        return "Hello"

    def resolve_books(self, info):
        """A method that returns a list of books."""
        return Book.objects.all()

    def resolve_book(self, info, id):
        """A method that returns a single book."""
        return Book.objects.get(pk=id)


class Mutation(graphene.ObjectType):
    """
    This class represents the Mutation type in the Graphene API.

    This class defines the fields that can be accessed at the root of the mutation tree.
    These fields correspond to the various mutations that can be made against the database.

    Args:
        graphene.ObjectType: A Graphene Object Type that represents a collection of fields.

    Attributes:
        create_book (graphene.Field): A field that creates a new book.
        delete_book (graphene.Field): A field that deletes an existing book.
        update_book (graphene.Field): A field that updates an existing book.
    """

    create_book = CreateBookMutation.Field()
    """
    This class represents a CreateBookMutation in the Graphene API.

    Args:
        title (str): The title of the book.
        description (str): The description of the book.

    Returns:
        Book: The created book.
    """

    delete_book = DeleteBookMutation.Field()
    """
    This class represents a DeleteBookMutation in the Graphene API.

    Args:
        id (str): The ID of the book to delete.

    Returns:
        message (str): A message indicating that the book was deleted.
    """

    update_book = UpdateMutation.Field()
    """
    This class represents an UpdateMutation in the Graphene API.

    Args:
        id (str): The ID of the book to update.
        title (str): The new title of the book.
        description (str): The new description of the book.

    Returns:
        Book: The updated book.
    """


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
