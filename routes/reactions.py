"""
API routes for message reactions.
"""

from flask import Blueprint, request, jsonify
from reaction_manager import ReactionManager, MessageReaction
from models import db
from functools import wraps

reactions_bp = Blueprint('reactions', __name__, url_prefix='/api/reactions')
reaction_manager = ReactionManager()


def require_auth(f):
    """Decorator to require authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Simple auth check - assumes user_id is passed in request
        user_id = request.headers.get('X-User-ID') or request.args.get('user_id')
        if not user_id:
            return jsonify({"error": "Authentication required"}), 401
        return f(*args, user_id=int(user_id), **kwargs)
    return decorated_function


@reactions_bp.route('/add', methods=['POST'])
@require_auth
def add_reaction(user_id):
    """
    Add a reaction to a message.

    Request body:
        {
            "message_id": int,
            "emoji": str
        }
    """
    data = request.get_json()

    if not data or 'message_id' not in data or 'emoji' not in data:
        return jsonify({"error": "message_id and emoji are required"}), 400

    try:
        result = reaction_manager.add_reaction(
            message_id=data['message_id'],
            user_id=user_id,
            emoji=data['emoji']
        )
        return jsonify(result), 200 if result['success'] else 400

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Failed to add reaction: {str(e)}"}), 500


@reactions_bp.route('/remove', methods=['POST'])
@require_auth
def remove_reaction(user_id):
    """
    Remove a reaction from a message.

    Request body:
        {
            "message_id": int,
            "emoji": str
        }
    """
    data = request.get_json()

    if not data or 'message_id' not in data or 'emoji' not in data:
        return jsonify({"error": "message_id and emoji are required"}), 400

    try:
        result = reaction_manager.remove_reaction(
            message_id=data['message_id'],
            user_id=user_id,
            emoji=data['emoji']
        )
        return jsonify(result), 200 if result['success'] else 404

    except Exception as e:
        return jsonify({"error": f"Failed to remove reaction: {str(e)}"}), 500


@reactions_bp.route('/toggle', methods=['POST'])
@require_auth
def toggle_reaction(user_id):
    """
    Toggle a reaction (add if doesn't exist, remove if exists).

    Request body:
        {
            "message_id": int,
            "emoji": str
        }
    """
    data = request.get_json()

    if not data or 'message_id' not in data or 'emoji' not in data:
        return jsonify({"error": "message_id and emoji are required"}), 400

    try:
        result = reaction_manager.toggle_reaction(
            message_id=data['message_id'],
            user_id=user_id,
            emoji=data['emoji']
        )
        return jsonify(result), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Failed to toggle reaction: {str(e)}"}), 500


@reactions_bp.route('/message/<int:message_id>', methods=['GET'])
def get_message_reactions(message_id):
    """Get all reactions for a message, grouped by emoji."""
    try:
        reactions = reaction_manager.get_message_reactions(message_id)
        return jsonify({
            "success": True,
            "message_id": message_id,
            "reactions": reactions
        }), 200

    except Exception as e:
        return jsonify({"error": f"Failed to get reactions: {str(e)}"}), 500


@reactions_bp.route('/user', methods=['GET'])
@require_auth
def get_user_reactions(user_id):
    """
    Get all reactions by a user, optionally filtered by message.

    Query params:
        message_id (optional): Filter by specific message
    """
    message_id = request.args.get('message_id', type=int)

    try:
        reactions = reaction_manager.get_user_reactions(user_id, message_id)
        return jsonify({
            "success": True,
            "user_id": user_id,
            "reactions": reactions
        }), 200

    except Exception as e:
        return jsonify({"error": f"Failed to get user reactions: {str(e)}"}), 500


@reactions_bp.route('/count/<int:message_id>', methods=['GET'])
def get_reaction_count(message_id):
    """Get total reaction count for a message."""
    try:
        count = reaction_manager.get_reaction_count(message_id)
        return jsonify({
            "success": True,
            "message_id": message_id,
            "count": count
        }), 200

    except Exception as e:
        return jsonify({"error": f"Failed to get reaction count: {str(e)}"}), 500


@reactions_bp.route('/popular/<int:message_id>', methods=['GET'])
def get_most_popular(message_id):
    """Get the most popular emoji for a message."""
    try:
        emoji = reaction_manager.get_most_popular_emoji(message_id)
        return jsonify({
            "success": True,
            "message_id": message_id,
            "most_popular_emoji": emoji
        }), 200

    except Exception as e:
        return jsonify({"error": f"Failed to get popular emoji: {str(e)}"}), 500


@reactions_bp.route('/allowed-emojis', methods=['GET'])
def get_allowed_emojis():
    """Get list of allowed reaction emojis."""
    return jsonify({
        "success": True,
        "emojis": ReactionManager.get_allowed_emojis()
    }), 200


@reactions_bp.route('/bulk', methods=['POST'])
@require_auth
def bulk_add_reactions(user_id):
    """
    Add multiple reactions in bulk.

    Request body:
        {
            "reactions": [
                {"message_id": int, "user_id": int, "emoji": str},
                ...
            ]
        }
    """
    data = request.get_json()

    if not data or 'reactions' not in data:
        return jsonify({"error": "reactions array is required"}), 400

    try:
        result = reaction_manager.bulk_add_reactions(data['reactions'])
        return jsonify({
            "success": True,
            "result": result
        }), 200

    except Exception as e:
        return jsonify({"error": f"Failed to bulk add reactions: {str(e)}"}), 500
