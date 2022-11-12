import logging
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from models.models import Bookmark, Bookmarks
from services.user import UserService, get_user_service
from utils.http_bearer_security import security
from utils.token_decoder import get_token_payload

router = APIRouter()


@router.get("/{user_id}/bookmarks", response_model=Bookmarks, summary='Get user bookmarks')
async def user_bookmarks(user_id: str, user_service: UserService = Depends(get_user_service)) -> Bookmarks:
    """
        ## Get detailed information about user bookmarks:
        - _user_id_
        - _movie_ids_

        URL params:
        - **{user_id}**
    """

    bookmarks = await user_service.get_user_bookmarks(user_id)
    if not bookmarks:
        logging.info('Cannot get user_bookmarks for user %s', user_id)
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return bookmarks


@router.post("/bookmark", response_model=Bookmark, summary='Add movie to bookmarks')
async def add_bookmark(movie_id: str, user_service: UserService = Depends(get_user_service),
                       access_token=Depends(security), ) -> Bookmark:
    """
            ## Add movie to bookmarks:
            - _user_id_
            - _movie_id_
    """

    token_payload = get_token_payload(access_token.credentials)
    if not (user_id := token_payload.get('user_id')):
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)

    result = await user_service.add_user_bookmark(film_id=movie_id, user_id=user_id)
    if not result:
        logging.error('Cannot add bookmark for movie %s, bookmark %s', movie_id, user_id)
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)
    return result


@router.delete("/bookmark", response_model=Bookmark, summary='Delete movie from bookmarks')
async def remove_bookmark(movie_id: str, user_service: UserService = Depends(get_user_service),
                          access_token=Depends(security), ) -> Bookmark:
    """
            ## Delete movie from bookmarks:
            - _user_id_
            - _movie_id_
    """

    token_payload = get_token_payload(access_token.credentials)
    if not (user_id := token_payload.get('user_id')):
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)

    result = await user_service.remove_user_bookmark(film_id=movie_id, user_id=user_id)
    if not result:
        logging.error('Cannot delete bookmark for movie %s, bookmark %s', movie_id, user_id)
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return result
