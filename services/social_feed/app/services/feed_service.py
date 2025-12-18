"""Feed service for posts and stories."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.social_feed.app.core.config import settings
from services.social_feed.app.models.comment import Comment
from services.social_feed.app.models.like import Like
from services.social_feed.app.models.post import Post, PostStatus
from services.social_feed.app.models.story import Story
from services.social_feed.app.schemas.comment import CommentCreate
from services.social_feed.app.schemas.post import PostCreate, PostUpdate
from services.social_feed.app.schemas.story import StoryCreate
from shared.messaging.events import EventType, ServiceEvent, event_bus


class FeedService:
    """Service for feed operations."""

    def __init__(self, db: AsyncSession) -> None:
        """Initialize feed service."""
        self.db = db

    async def create_post(self, author_id: str, post_data: PostCreate) -> Post:
        """Create a new post."""
        post = Post(
            author_id=author_id,
            post_type=post_data.post_type.value,
            status=PostStatus.PUBLISHED,
            title=post_data.title,
            content=post_data.content,
            media_urls=post_data.media_urls,
            tags=post_data.tags,
            latitude=post_data.latitude,
            longitude=post_data.longitude,
            location_name=post_data.location_name,
            metadata=post_data.metadata,
            price=post_data.price,
            currency=post_data.currency,
            event_id=post_data.event_id,
            published_at=datetime.now(timezone.utc),
        )
        self.db.add(post)
        await self.db.flush()

        event = ServiceEvent(
            event_type=EventType.POST_CREATED,
            data={
                "post_id": post.id,
                "author_id": author_id,
                "post_type": post_data.post_type.value,
                "has_geo": post_data.latitude is not None,
            },
            source_service="social-feed",
        )
        await event_bus.publish(event)

        return post

    async def get_post(self, post_id: str) -> Post | None:
        """Get post by ID."""
        result = await self.db.execute(select(Post).where(Post.id == post_id))
        return result.scalar_one_or_none()

    async def get_feed(
        self, user_id: str, limit: int = 20, offset: int = 0
    ) -> list[Post]:
        """Get feed for user."""
        result = await self.db.execute(
            select(Post)
            .where(Post.status == PostStatus.PUBLISHED)
            .order_by(Post.published_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())

    async def update_post(
        self, post_id: str, user_id: str, post_data: PostUpdate
    ) -> Post | None:
        """Update a post."""
        result = await self.db.execute(
            select(Post).where(Post.id == post_id, Post.author_id == user_id)
        )
        post = result.scalar_one_or_none()
        if not post:
            return None

        update_data = post_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(post, field, value)

        return post

    async def delete_post(self, post_id: str, user_id: str) -> bool:
        """Delete a post (archive)."""
        result = await self.db.execute(
            select(Post).where(Post.id == post_id, Post.author_id == user_id)
        )
        post = result.scalar_one_or_none()
        if not post:
            return False

        post.status = PostStatus.ARCHIVED
        return True

    async def like_post(self, post_id: str, user_id: str) -> bool:
        """Like a post."""
        # Check if already liked
        existing = await self.db.execute(
            select(Like).where(
                Like.user_id == user_id,
                Like.target_id == post_id,
                Like.target_type == "post",
            )
        )
        if existing.scalar_one_or_none():
            return False

        like = Like(user_id=user_id, target_id=post_id, target_type="post")
        self.db.add(like)

        # Update counter
        post = await self.get_post(post_id)
        if post:
            post.likes_count += 1

        event = ServiceEvent(
            event_type=EventType.POST_LIKED,
            data={"post_id": post_id, "user_id": user_id},
            source_service="social-feed",
        )
        await event_bus.publish(event)

        return True

    async def unlike_post(self, post_id: str, user_id: str) -> bool:
        """Unlike a post."""
        result = await self.db.execute(
            select(Like).where(
                Like.user_id == user_id,
                Like.target_id == post_id,
                Like.target_type == "post",
            )
        )
        like = result.scalar_one_or_none()
        if not like:
            return False

        await self.db.delete(like)

        post = await self.get_post(post_id)
        if post and post.likes_count > 0:
            post.likes_count -= 1

        return True

    async def add_comment(
        self, user_id: str, comment_data: CommentCreate
    ) -> Comment | None:
        """Add a comment to a post."""
        post = await self.get_post(comment_data.post_id)
        if not post:
            return None

        comment = Comment(
            post_id=comment_data.post_id,
            author_id=user_id,
            content=comment_data.content,
            parent_id=comment_data.parent_id,
        )
        self.db.add(comment)
        post.comments_count += 1
        await self.db.flush()

        event = ServiceEvent(
            event_type=EventType.COMMENT_ADDED,
            data={
                "comment_id": comment.id,
                "post_id": comment_data.post_id,
                "author_id": user_id,
            },
            source_service="social-feed",
        )
        await event_bus.publish(event)

        return comment

    async def get_comments(
        self, post_id: str, limit: int = 50, offset: int = 0
    ) -> list[Comment]:
        """Get comments for a post."""
        result = await self.db.execute(
            select(Comment)
            .where(Comment.post_id == post_id, Comment.is_deleted.is_(False))
            .order_by(Comment.created_at.asc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())

    async def create_story(self, author_id: str, story_data: StoryCreate) -> Story:
        """Create a new story."""
        story = Story(
            author_id=author_id,
            media_url=story_data.media_url,
            media_type=story_data.media_type,
            thumbnail_url=story_data.thumbnail_url,
            text_overlay=story_data.text_overlay,
            text_style=story_data.text_style,
            latitude=story_data.latitude,
            longitude=story_data.longitude,
            location_name=story_data.location_name,
            expires_at=datetime.now(timezone.utc)
            + timedelta(hours=settings.story_expiration_hours),
        )
        self.db.add(story)
        await self.db.flush()
        return story

    async def get_active_stories(self, user_id: str | None = None) -> list[Story]:
        """Get active stories."""
        now = datetime.now(timezone.utc)
        query = select(Story).where(Story.is_active.is_(True), Story.expires_at > now)
        if user_id:
            query = query.where(Story.author_id == user_id)

        result = await self.db.execute(query.order_by(Story.created_at.desc()))
        return list(result.scalars().all())

    async def get_geo_posts(
        self, latitude: float, longitude: float, radius_km: float
    ) -> list[Post]:
        """Get posts with geolocation (for map display)."""
        # Placeholder - in production use PostGIS ST_DWithin
        result = await self.db.execute(
            select(Post).where(
                Post.status == PostStatus.PUBLISHED,
                Post.latitude.isnot(None),
                Post.longitude.isnot(None),
            )
        )
        return list(result.scalars().all())
