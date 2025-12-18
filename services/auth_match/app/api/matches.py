"""Match and invitation API routes."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from services.auth_match.app.schemas.match import (
    InvitationAction,
    InvitationCreate,
    InvitationResponse,
    MatchResponse,
)
from services.auth_match.app.services.match_service import MatchService
from shared.auth import get_current_user
from shared.database import get_db

router = APIRouter()


@router.post(
    "/invitations",
    response_model=InvitationResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_invitation(
    invitation_data: InvitationCreate,
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Create a new invitation (swipe action).

    Args:
        invitation_data: Invitation data
        current_user: Current user from token
        db: Database session

    Returns:
        Created invitation
    """
    service = MatchService(db)
    try:
        invitation = await service.create_invitation(
            current_user["sub"], invitation_data
        )
        return invitation
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e


@router.get("/invitations/received", response_model=list[InvitationResponse])
async def get_received_invitations(
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get received invitations.

    Args:
        current_user: Current user from token
        db: Database session

    Returns:
        List of received invitations
    """
    service = MatchService(db)
    return await service.get_user_invitations(current_user["sub"], sent=False)


@router.get("/invitations/sent", response_model=list[InvitationResponse])
async def get_sent_invitations(
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get sent invitations.

    Args:
        current_user: Current user from token
        db: Database session

    Returns:
        List of sent invitations
    """
    service = MatchService(db)
    return await service.get_user_invitations(current_user["sub"], sent=True)


@router.post("/invitations/{invitation_id}/respond", response_model=InvitationResponse)
async def respond_to_invitation(
    invitation_id: str,
    action: InvitationAction,
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Respond to an invitation (accept/decline).

    Args:
        invitation_id: Invitation ID
        action: Accept or decline
        current_user: Current user from token
        db: Database session

    Returns:
        Updated invitation
    """
    service = MatchService(db)
    invitation = await service.respond_to_invitation(
        invitation_id, current_user["sub"], action.action == "accept"
    )
    if not invitation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invitation not found or already responded",
        )
    return invitation


@router.get("/", response_model=list[MatchResponse])
async def get_matches(
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get all matches for current user.

    Args:
        current_user: Current user from token
        db: Database session

    Returns:
        List of matches
    """
    service = MatchService(db)
    return await service.get_user_matches(current_user["sub"])


@router.delete("/{match_id}", response_model=MatchResponse)
async def unmatch(
    match_id: str,
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Unmatch from a user.

    Args:
        match_id: Match ID
        current_user: Current user from token
        db: Database session

    Returns:
        Updated match
    """
    service = MatchService(db)
    match = await service.unmatch(match_id, current_user["sub"])
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match not found",
        )
    return match
