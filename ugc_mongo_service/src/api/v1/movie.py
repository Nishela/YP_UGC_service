import logging
from collections import namedtuple
from datetime import datetime
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer
from utils.token_decoder import get_token_payload

from models.models import (
    FilmInfo,
    FilmReview,
    FilmReviewAdd,
    FilmReviewInfo,
    FilmVote,
    FilmVoteFilter,
)
from services.movie import FilmService, get_film_service

router = APIRouter()
security = HTTPBearer()


@router.get("/{film_id}/likes", response_model=FilmInfo, summary='Show information about film rating')
async def film_likes(film_id: str, film_service: FilmService = Depends(get_film_service), ) -> FilmInfo:
    """
        ## Get detailed information about Film:
        - _movie_id_
        - _likes_
        - _dislikes_
        - _rating_

        URL params:
        - **{film_id}**
    """

    film_info = await film_service.get_film_info(film_id)
    if not film_info:
        logging.info('Cannot get film info, film_id %s does not exist', film_id)
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return film_info


@router.post("/vote", response_model=FilmVote, summary='Set movie rating')
async def upsert_film_vote(film_vote: FilmVote, film_service: FilmService = Depends(get_film_service),
                           access_token: namedtuple = Depends(security), ) -> FilmVote:
    """
            ## Set movie rating:
            - _movie_id_
            - _rating_
    """

    token_payload = get_token_payload(access_token.credentials)
    if not (user_id := token_payload.get('user_id')):
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)

    result = await film_service.upsert_film_vote(
        film_id=film_vote.movie_id,
        user_id=user_id,
        rating=film_vote.rating,
    )
    if not result:
        logging.error('vote not counted movie_id: %s, user_id %s', film_vote.movie_id, token_payload.get('user_id'))
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return result


@router.delete("/vote", response_model=FilmVote, summary='Delete movie rating')
async def remove_film_vote(film_vote: FilmVoteFilter, film_service: FilmService = Depends(get_film_service),
                           access_token: namedtuple = Depends(security), ) -> FilmVote:
    """
            ## Delete movie rating:
            - _movie_id_
            - _rating_
    """

    token_payload = get_token_payload(access_token.credentials)
    if not (user_id := token_payload.get('user_id')):
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)

    result = await film_service.remove_film_vote(film_id=film_vote.movie_id, user_id=user_id)
    if not result:
        logging.error(f'failed to delete movie_id %s, user_id %s', film_vote.movie_id, user_id)
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return result


@router.post("/review/info", response_model=FilmReviewInfo, summary='Detailed info about Film by ID')
async def get_film_review_info(film_review: FilmVoteFilter, film_service: FilmService = Depends(get_film_service),
                               access_token: namedtuple = Depends(security), ) -> FilmReview:
    """
            ## Detailed film information:
            - _movie_id_
            - _text_
            - _timestamp_
            - _rating_
    """

    token_payload = get_token_payload(access_token.credentials)
    if not (user_id := token_payload.get('user_id')):
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)

    result = await film_service.get_film_review_info(film_id=film_review.movie_id, user_id=user_id)
    if not result:
        logging.error('failed to get review movie_id %s, user_id %s', film_review.movie_id, user_id)
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return result


@router.post("/review", response_model=FilmReview, summary='Set film review')
async def upsert_film_review(film_review: FilmReviewAdd, film_service: FilmService = Depends(get_film_service),
                             access_token: namedtuple = Depends(security), ) -> FilmReview:
    """
            ## Set film review:
            - _movie_id_
            - _text_
            - _timestamp_
    """

    token_payload = get_token_payload(access_token.credentials)
    if not (user_id := token_payload.get('user_id')):
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)

    result = await film_service.upsert_film_review(
        film_id=film_review.movie_id,
        user_id=user_id,
        text=film_review.text,
        timestamp=datetime.now(),
    )
    if not result:
        logging.error('failed to add review movie_id %s, user_id %s', film_review.movie_id, user_id)
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)
    return result


@router.delete("/review", response_model=FilmReview, summary='Delete film review')
async def remove_film_review(film_review: FilmVoteFilter, film_service: FilmService = Depends(get_film_service),
                             access_token: namedtuple = Depends(security), ) -> FilmReview:
    """
            ## Delete film review:
            - _movie_id_
            - _text_
            - _timestamp_
    """

    token_payload = get_token_payload(access_token.credentials)
    if not (user_id := token_payload.get('user_id')):
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)

    result = await film_service.remove_film_review(film_id=film_review.movie_id, user_id=user_id)
    if not result:
        logging.error('failed to delete review movie_id %s, user_id %s', film_review.movie_id, user_id)
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return result
