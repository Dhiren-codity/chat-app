"""
Message Reaction Manager
Handles adding, removing, and querying reactions to messages.
"""

from datetime import datetime
from typing import List, Dict, Optional
from models import db, Message


class MessageReaction(db.Model):
    """Model for storing message reactions."""
    id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(db.Integer, db.ForeignKey('message.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    emoji = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Composite unique constraint to prevent duplicate reactions
    __table_args__ = (
        db.UniqueConstraint('message_id', 'user_id', 'emoji', name='unique_reaction'),
    )


class ReactionManager:
    """Manages message reactions functionality."""

    ALLOWED_EMOJIS = ['👍', '❤️', '😂', '😮', '😢', '🎉', '🔥', '👏']

    def __init__(self, db_session=None):
        """
        Initialize reaction manager.

        Args:
            db_session: Database session (optional, uses default db if not provided)
        """
        self.db = db_session or db

    def add_reaction(self, message_id: int, user_id: int, emoji: str) -> Dict[str, any]:
        """
        Add a reaction to a message.

        Args:
            message_id: ID of the message to react to
            user_id: ID of the user adding the reaction
            emoji: Emoji to add (must be in ALLOWED_EMOJIS)

        Returns:
            Dictionary with success status and reaction data

        Raises:
            ValueError: If emoji is not allowed or message doesn't exist
        """
        if emoji not in self.ALLOWED_EMOJIS:
            raise ValueError(f"Emoji '{emoji}' not allowed. Allowed: {', '.join(self.ALLOWED_EMOJIS)}")

        # Verify message exists
        message = Message.query.get(message_id)
        if not message:
            raise ValueError(f"Message {message_id} not found")

        # Check if reaction already exists
        existing = MessageReaction.query.filter_by(
            message_id=message_id,
            user_id=user_id,
            emoji=emoji
        ).first()

        if existing:
            return {
                "success": False,
                "message": "Reaction already exists",
                "reaction_id": existing.id
            }

        # Create new reaction
        reaction = MessageReaction(
            message_id=message_id,
            user_id=user_id,
            emoji=emoji
        )

        try:
            self.db.session.add(reaction)
            self.db.session.commit()

            return {
                "success": True,
                "message": "Reaction added",
                "reaction_id": reaction.id,
                "emoji": emoji,
                "created_at": reaction.created_at.isoformat()
            }

        except Exception as e:
            self.db.session.rollback()
            raise Exception(f"Failed to add reaction: {str(e)}")

    def remove_reaction(self, message_id: int, user_id: int, emoji: str) -> Dict[str, any]:
        """
        Remove a reaction from a message.

        Args:
            message_id: ID of the message
            user_id: ID of the user removing the reaction
            emoji: Emoji to remove

        Returns:
            Dictionary with success status
        """
        reaction = MessageReaction.query.filter_by(
            message_id=message_id,
            user_id=user_id,
            emoji=emoji
        ).first()

        if not reaction:
            return {
                "success": False,
                "message": "Reaction not found"
            }

        try:
            self.db.session.delete(reaction)
            self.db.session.commit()

            return {
                "success": True,
                "message": "Reaction removed"
            }

        except Exception as e:
            self.db.session.rollback()
            raise Exception(f"Failed to remove reaction: {str(e)}")

    def get_message_reactions(self, message_id: int) -> List[Dict[str, any]]:
        """
        Get all reactions for a message, grouped by emoji.

        Args:
            message_id: ID of the message

        Returns:
            List of reaction summaries with counts
        """
        reactions = MessageReaction.query.filter_by(message_id=message_id).all()

        # Group by emoji
        grouped = {}
        for reaction in reactions:
            if reaction.emoji not in grouped:
                grouped[reaction.emoji] = {
                    "emoji": reaction.emoji,
                    "count": 0,
                    "users": []
                }

            grouped[reaction.emoji]["count"] += 1
            grouped[reaction.emoji]["users"].append(reaction.user_id)

        return list(grouped.values())

    def get_user_reactions(self, user_id: int, message_id: Optional[int] = None) -> List[Dict[str, any]]:
        """
        Get reactions by a specific user.

        Args:
            user_id: ID of the user
            message_id: Optional message ID to filter by

        Returns:
            List of user's reactions
        """
        query = MessageReaction.query.filter_by(user_id=user_id)

        if message_id:
            query = query.filter_by(message_id=message_id)

        reactions = query.all()

        return [
            {
                "reaction_id": r.id,
                "message_id": r.message_id,
                "emoji": r.emoji,
                "created_at": r.created_at.isoformat()
            }
            for r in reactions
        ]

    def toggle_reaction(self, message_id: int, user_id: int, emoji: str) -> Dict[str, any]:
        """
        Toggle a reaction (add if doesn't exist, remove if exists).

        Args:
            message_id: ID of the message
            user_id: ID of the user
            emoji: Emoji to toggle

        Returns:
            Dictionary with action taken and status
        """
        existing = MessageReaction.query.filter_by(
            message_id=message_id,
            user_id=user_id,
            emoji=emoji
        ).first()

        if existing:
            result = self.remove_reaction(message_id, user_id, emoji)
            result["action"] = "removed"
            return result
        else:
            result = self.add_reaction(message_id, user_id, emoji)
            result["action"] = "added"
            return result

    def get_reaction_count(self, message_id: int) -> int:
        """
        Get total reaction count for a message.

        Args:
            message_id: ID of the message

        Returns:
            Total number of reactions
        """
        return MessageReaction.query.filter_by(message_id=message_id).count()

    def get_most_popular_emoji(self, message_id: int) -> Optional[str]:
        """
        Get the most used emoji for a message.

        Args:
            message_id: ID of the message

        Returns:
            Most popular emoji or None if no reactions
        """
        reactions = self.get_message_reactions(message_id)

        if not reactions:
            return None

        most_popular = max(reactions, key=lambda x: x['count'])
        return most_popular['emoji']

    def has_user_reacted(self, message_id: int, user_id: int, emoji: Optional[str] = None) -> bool:
        """
        Check if a user has reacted to a message.

        Args:
            message_id: ID of the message
            user_id: ID of the user
            emoji: Optional specific emoji to check

        Returns:
            True if user has reacted (with specified emoji if provided)
        """
        query = MessageReaction.query.filter_by(
            message_id=message_id,
            user_id=user_id
        )

        if emoji:
            query = query.filter_by(emoji=emoji)

        return query.first() is not None

    def bulk_add_reactions(self, reactions: List[Dict[str, any]]) -> Dict[str, any]:
        """
        Add multiple reactions in bulk.

        Args:
            reactions: List of reaction dictionaries with message_id, user_id, emoji

        Returns:
            Summary of bulk operation
        """
        added = 0
        failed = 0
        errors = []

        for reaction_data in reactions:
            try:
                result = self.add_reaction(
                    reaction_data['message_id'],
                    reaction_data['user_id'],
                    reaction_data['emoji']
                )

                if result['success']:
                    added += 1
                else:
                    failed += 1

            except Exception as e:
                failed += 1
                errors.append(str(e))

        return {
            "total": len(reactions),
            "added": added,
            "failed": failed,
            "errors": errors
        }

    @staticmethod
    def get_allowed_emojis() -> List[str]:
        """
        Get list of allowed reaction emojis.

        Returns:
            List of allowed emojis
        """
        return ReactionManager.ALLOWED_EMOJIS.copy()
