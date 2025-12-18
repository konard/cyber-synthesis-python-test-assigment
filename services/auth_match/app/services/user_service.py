"""User service for authentication and user management."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.auth_match.app.models.profile import UserProfile
from services.auth_match.app.models.user import User
from services.auth_match.app.schemas.profile import ProfileCreate, ProfileUpdate
from services.auth_match.app.schemas.user import UserCreate, UserUpdate
from shared.auth import create_access_token, get_password_hash, verify_password


class UserService:
    """Service for user-related operations."""

    def __init__(self, db: AsyncSession) -> None:
        """Initialize user service.

        Args:
            db: Database session
        """
        self.db = db

    async def create_user(self, user_data: UserCreate) -> User:
        """Create a new user.

        Args:
            user_data: User creation data

        Returns:
            Created user

        Raises:
            ValueError: If user with email or username already exists
        """
        # Check for existing user
        existing = await self.db.execute(
            select(User).where(
                (User.email == user_data.email) | (User.username == user_data.username)
            )
        )
        if existing.scalar_one_or_none():
            msg = "User with this email or username already exists"
            raise ValueError(msg)

        # Create user
        user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=get_password_hash(user_data.password),
        )
        self.db.add(user)
        await self.db.flush()

        # Create empty profile
        profile = UserProfile(user_id=user.id)
        self.db.add(profile)

        return user

    async def authenticate_user(
        self, username: str, password: str
    ) -> tuple[User, str] | None:
        """Authenticate user and return token.

        Args:
            username: Username
            password: Password

        Returns:
            Tuple of (user, token) if successful, None otherwise
        """
        result = await self.db.execute(select(User).where(User.username == username))
        user = result.scalar_one_or_none()

        if not user or not verify_password(password, user.hashed_password):
            return None

        if not user.is_active:
            return None

        token = create_access_token(
            data={"sub": user.id, "username": user.username, "email": user.email}
        )
        return user, token

    async def get_user_by_id(self, user_id: str) -> User | None:
        """Get user by ID.

        Args:
            user_id: User ID

        Returns:
            User if found, None otherwise
        """
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def update_user(self, user_id: str, user_data: UserUpdate) -> User | None:
        """Update user.

        Args:
            user_id: User ID
            user_data: Update data

        Returns:
            Updated user if found, None otherwise
        """
        user = await self.get_user_by_id(user_id)
        if not user:
            return None

        update_data = user_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)

        return user

    async def get_profile(self, user_id: str) -> UserProfile | None:
        """Get user profile.

        Args:
            user_id: User ID

        Returns:
            Profile if found, None otherwise
        """
        result = await self.db.execute(
            select(UserProfile).where(UserProfile.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def create_profile(
        self, user_id: str, profile_data: ProfileCreate
    ) -> UserProfile:
        """Create or update user profile.

        Args:
            user_id: User ID
            profile_data: Profile data

        Returns:
            Created or updated profile
        """
        profile = await self.get_profile(user_id)
        if profile:
            # Update existing profile
            update_data = profile_data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(profile, field, value)
        else:
            # Create new profile
            profile = UserProfile(
                user_id=user_id, **profile_data.model_dump(exclude_unset=True)
            )
            self.db.add(profile)

        return profile

    async def update_profile(
        self, user_id: str, profile_data: ProfileUpdate
    ) -> UserProfile | None:
        """Update user profile.

        Args:
            user_id: User ID
            profile_data: Profile update data

        Returns:
            Updated profile if found, None otherwise
        """
        profile = await self.get_profile(user_id)
        if not profile:
            return None

        update_data = profile_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(profile, field, value)

        return profile

    async def get_users_in_radius(
        self, latitude: float, longitude: float, radius_km: float, exclude_user_id: str
    ) -> list[User]:
        """Get users within a radius.

        Args:
            latitude: Center latitude
            longitude: Center longitude
            radius_km: Radius in kilometers
            exclude_user_id: User ID to exclude

        Returns:
            List of users within radius
        """
        # Simple distance calculation (for production, use PostGIS)
        # This is a placeholder - real implementation would use ST_DWithin
        result = await self.db.execute(
            select(User)
            .join(UserProfile)
            .where(
                User.id != exclude_user_id,
                User.is_active.is_(True),
                User.is_invisible.is_(False),
                UserProfile.last_known_latitude.isnot(None),
                UserProfile.last_known_longitude.isnot(None),
            )
        )
        return list(result.scalars().all())
