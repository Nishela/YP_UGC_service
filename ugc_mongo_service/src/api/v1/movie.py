import datetime
import logging
from collections import namedtuple
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from models.models import (
    FilmInfo,
    FilmReview,
    FilmReviewAdd,
    FilmReviewInfo,
    FilmVote,
    FilmVoteFilter,
)
from services.movie import FilmService, get_film_service
from ugc_mongo_service.src.main import security
from ugc_mongo_service.src.utils.token_decoder import get_token_payload

router = APIRouter()


@router.get("/{film_id}/likes", response_model=FilmInfo, response_model_exclude_unset=True)
async def film_likes(
        film_id: str,
        film_service: FilmService = Depends(get_film_service)
) -> FilmInfo:
    film_info = await film_service.get_film_info(film_id)
    if not film_info:
        logging.info('Cannot get film info, film_id %s does not exist', film_id)
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return film_info


@router.post("/vote", response_model=FilmVote, response_model_exclude_unset=True)
async def upsert_film_vote(
        film_vote: FilmVote,
        film_service: FilmService = Depends(get_film_service),
        access_token: namedtuple = Depends(security),
) -> FilmVote:
    token_payload = get_token_payload(access_token.credentials)
    result = await film_service.upsert_film_vote(
        film_id=film_vote.movie_id,
        user_id=token_payload.get('user_id'),
        rating=film_vote.rating
    )
    if not result:
        logging.error(
            'vote not counted movie_id: %s, user_id %s',
            film_vote.movie_id,
            token_payload.get('user_id')
        )
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return result


@router.delete("/vote", response_model=FilmVote, response_model_exclude_unset=True)
async def remove_film_vote(
        film_vote: FilmVoteFilter,
        film_service: FilmService = Depends(get_film_service),
        access_token: namedtuple = Depends(security),
) -> FilmVote:
    token_payload = get_token_payload(access_token.credentials)
    result = await film_service.remove_film_vote(film_id=film_vote.movie_id, user_id=token_payload.get('user_id'))
    if not result:
        logging.error(
            f'failed to delete movie_id %s, user_id %s',
            film_vote.movie_id,
            token_payload.get('user_id')
        )
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return result


@router.post("/review/info", response_model=FilmReviewInfo, response_model_exclude_unset=True)
async def get_film_review_info(
        film_review: FilmVoteFilter,
        film_service: FilmService = Depends(get_film_service),
        access_token: namedtuple = Depends(security),
) -> FilmReview:
    token_payload = get_token_payload(access_token.credentials)
    result = await film_service.get_film_review_info(film_id=film_review.movie_id, user_id=token_payload.get('user_id'))
    if not result:
        logging.error('failed to get review movie_id %s, user_id %s', film_review.movie_id,
                      token_payload.get('user_id'))
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return result


@router.post("/review", response_model=FilmReview, response_model_exclude_unset=True)
async def upsert_film_review(
        film_review: FilmReviewAdd,
        film_service: FilmService = Depends(get_film_service),
        access_token: namedtuple = Depends(security),
) -> FilmReview:
    token_payload = get_token_payload(access_token.credentials)
    result = await film_service.upsert_film_review(
        film_id=film_review.movie_id,
        user_id=token_payload.get('user_id'),
        text=film_review.text,
        timestamp=datetime.datetime.now(),
    )
    if not result:
        logging.error(
            'failed to add review movie_id %s, user_id %s',
            film_review.movie_id,
            token_payload.get('user_id')
        )
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)
    return result


@router.delete("/review", response_model=FilmReview, response_model_exclude_unset=True)
async def remove_film_review(
        film_review: FilmVoteFilter,
        film_service: FilmService = Depends(get_film_service),
        access_token: namedtuple = Depends(security),
) -> FilmReview:
    token_payload = get_token_payload(access_token.credentials)
    result = await film_service.remove_film_review(film_id=film_review.movie_id, user_id=token_payload.get('user_id'))
    if not result:
        logging.error(
            'failed to delete review movie_id %s, user_id %s',
            film_review.movie_id, token_payload.get('user_id')
        )
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return result
