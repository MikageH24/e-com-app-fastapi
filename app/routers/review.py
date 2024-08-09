from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.backend.db_depends import get_db
from typing import Annotated

from app.models import *
from sqlalchemy import insert, select, update
from app.schemas import CreateReview, CreateRating

from app.routers.auth import get_current_user

from statistics import mean

router = APIRouter(prefix='/review', tags=['review'])


@router.get('/all_reviews')
async def get_all_reviews(db: Annotated[AsyncSession, Depends(get_db)]):
    reviews = await db.scalars(select(Review).where(Review.is_active == True))
    return reviews.all()


@router.get('/product_reviews/{product_slug}')
async def get_reviews_by_product(db: Annotated[AsyncSession, Depends(get_db)], product_slug: str):
    product = await db.scalar(select(Product.id).where(Product.slug == product_slug))
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Product not found'
        )
    reviews = await db.scalars(select(Review).where(Review.product_id == product, Review.is_active == True))
    return reviews.all()


@router.post('/create')
async def add_review(db: Annotated[AsyncSession, Depends(get_db)], create_review: CreateReview, create_rating: CreateRating,
                     get_user: Annotated[dict, Depends(get_current_user)], product_id: int):
    product = await db.scalar(select(Product).where(Product.id == product_id))
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Product not found'
        )
    if get_user.get('is_customer'):
        result = await db.execute(insert(Rating).values(
            grade=create_rating.grade,
            user_id=get_user.get('id'),
            product_id=product_id)
        )
        rating_id = result.inserted_primary_key[0]
        await db.execute(insert(Review).values(
            comment=create_review.comment,
            comment_date=create_review.comment_date,
            user_id=get_user.get('id'),
            product_id=product_id,
            rating_id=rating_id)
        )
        grades = await db.scalars(select(Rating.grade).where(Rating.product_id == product_id, Rating.is_active == True))
        updated_rating = mean(grades.all()) if grades else 0
        await db.execute(update(Product).where(Product.id == product_id).values(rating=updated_rating))
        await db.commit()
        return {
            'status_code': status.HTTP_201_CREATED,
            'transaction': 'Review is added'
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='You must be a customer to add a review'
        )


@router.put('/delete')
async def delete_review(db: Annotated[AsyncSession, Depends(get_db)], review_id: int,
                        get_user: Annotated[dict, Depends(get_current_user)]):
    review = await db.scalar(select(Review).where(Review.id == review_id))
    if review is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Review not found'
        )
    if get_user.get('is_admin'):
        await db.execute(update(Review).where(Review.id == review_id).values(is_active=False))
        await db.execute(update(Rating).where(Rating.id == review.rating_id).values(is_active=False))

        grades = await db.scalars(select(Rating.grade).where(Rating.product_id == review.product_id, Rating.is_active == True))
        updated_rating = mean(grades.all()) if grades else 0
        await db.execute(update(Product).where(Product.id == review.product_id).values(rating=updated_rating))

        await db.commit()
        return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'Review is deleted'
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='You are not authorized to use this method'
        )