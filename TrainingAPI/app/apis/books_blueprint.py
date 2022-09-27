import uuid
from crypt import methods
import json

from sanic import Blueprint
from sanic.response import json, text, raw

# from app.constants.cache_constants import CacheConstants
from sanic_openapi.openapi2.doc import UUID

from app.constants.cache_constants import CacheConstants
from app.databases.mongodb import MongoDB
# from app.databases.redis_cached import get_cache, set_cache
from app.databases.redis_cached import get_cache, set_cache
from app.decorators.json_validator import validate_with_jsonschema
# from app.hooks.error import ApiInternalError
from app.hooks.error import ApiInternalError, ApiNotFound
from app.models.book import create_book_json_schema, Book, update_book_json_schema

books_bp = Blueprint('books_blueprint', url_prefix='/books')

_db = MongoDB()


@books_bp.route('/')
async def get_all_books(request):
    # TODO: use cache to optimize api
    async with request.app.ctx.redis as r:
        books = await get_cache(r, CacheConstants.all_books)
        if books is None:
            book_objs = _db.get_books()
            books = [book.to_dict() for book in book_objs]
            await set_cache(r, CacheConstants.all_books, books)

    book_objs = _db.get_books()
    books = [book.to_dict() for book in book_objs]
    number_of_books = len(books)
    return json({
        'n_books': number_of_books,
        'books': books
    })


@books_bp.route('/', methods={'POST'})
# @protected  # TODO: Authenticate
@validate_with_jsonschema(create_book_json_schema)  # To validate request body
async def create_book(request, username=None):
    body = request.json

    book_id = str(uuid.uuid4())
    book = Book(book_id).from_dict(body)
    book.owner = username

    # # TODO: Save book to database
    inserted = _db.add_book(book)
    if not inserted:
        raise ApiInternalError('Fail to create book')

    query = {"_id": "{}".format(book_id)}
    inserted = _db.get_book(query)

    # TODO: Update cache
    async with request.app.ctx.redis as r:
        book_objs = _db.get_books()
        books = [book.to_dict() for book in book_objs]
        await set_cache(r, CacheConstants.all_books, books)

    return json({'status': 'success'})


# TODO: write api get, update, delete book
@books_bp.route("/<_id:uuid>", methods={'GET'})
async def get_book(request, _id: UUID):
    query = {"_id": "{}".format(_id)}
    book_obj = _db.get_book(query)

    if not book_obj:
        raise ApiNotFound('id {}'.format(_id))

    return json({'book': book_obj})


@books_bp.route('/<_id:uuid>', methods={'PUT'})
# @protected  # TODO: Authenticate
@validate_with_jsonschema(update_book_json_schema)  # To validate request body
async def update_book(request, _id: UUID):
    query = {"_id": "{}".format(_id)}
    book_obj = _db.get_book(query)
    if not book_obj:
        raise ApiNotFound('id {}'.format(_id))

    body = request.json

    # TODO: Update book to database
    book_obj = _db.update_book(query, body)
    if not book_obj:
        raise ApiInternalError('Fail to update book')
    book_obj = _db.get_book(query)

    # TODO: Update cache
    async with request.app.ctx.redis as r:
        book_objs = _db.get_books()
        books = [book.to_dict() for book in book_objs]
        await set_cache(r, CacheConstants.all_books, books)

    return json({'book': book_obj})


@books_bp.route('/<_id:uuid>', methods={'DELETE'})
async def delete_book(request, _id: UUID):
    query = {"_id": "{}".format(_id)}
    book_obj = _db.get_book(query)

    if not book_obj:
        raise ApiNotFound('id {}'.format(_id))

    book_obj = _db.delete_book(query)

    # TODO: Update cache
    async with request.app.ctx.redis as r:
        book_objs = _db.get_books()
        books = [book.to_dict() for book in book_objs]
        await set_cache(r, CacheConstants.all_books, books)

    return json({'status': 'success'})
