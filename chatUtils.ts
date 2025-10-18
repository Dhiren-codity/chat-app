/**
 * Chat Utilities
 * TypeScript utility functions for chat operations
 */

interface User {
  id: number;
  username: string;
  displayName?: string;
  online: boolean;
  lastSeen?: Date;
}

interface Message {
  id: number;
  content: string;
  senderId: number;
  recipientId: number;
  timestamp: Date;
  read: boolean;
  delivered: boolean;
}

interface ChatRoom {
  id: number;
  name: string;
  participants: number[];
  createdAt: Date;
  lastMessage?: Message;
}

export class ChatUtils {
  /**
   * Check if a user is online
   * @param user User object to check
   * @returns True if user is online
   */
  static isUserOnline(user: User): boolean {
    return user && user.online === true;
  }

  /**
   * Get user display name or fallback to username
   * @param user User object
   * @returns Display name or username
   */
  static getUserDisplayName(user: User): string {
    if (!user) {
      return 'Unknown User';
    }
    return user.displayName || user.username || 'Unknown User';
  }

  /**
   * Calculate time since last seen
   * @param lastSeen Last seen date
   * @returns Human-readable time difference
   */
  static getLastSeenText(lastSeen: Date | undefined): string {
    if (!lastSeen) {
      return 'Never';
    }

    const now = new Date();
    const diffMs = now.getTime() - lastSeen.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) {
      return 'Just now';
    } else if (diffMins < 60) {
      return `${diffMins} minute${diffMins > 1 ? 's' : ''} ago`;
    } else if (diffHours < 24) {
      return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
    } else if (diffDays < 30) {
      return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`;
    } else {
      return lastSeen.toLocaleDateString();
    }
  }

  /**
   * Check if a message is read
   * @param message Message object
   * @returns True if message is read
   */
  static isMessageRead(message: Message): boolean {
    return message && message.read === true;
  }

  /**
   * Check if a message is delivered
   * @param message Message object
   * @returns True if message is delivered
   */
  static isMessageDelivered(message: Message): boolean {
    return message && message.delivered === true;
  }

  /**
   * Get unread message count for a user
   * @param messages Array of messages
   * @param userId User ID to check for
   * @returns Count of unread messages
   */
  static getUnreadCount(messages: Message[], userId: number): number {
    if (!messages || messages.length === 0) {
      return 0;
    }

    return messages.filter(
      msg => msg.recipientId === userId && !msg.read
    ).length;
  }

  /**
   * Sort messages by timestamp
   * @param messages Array of messages
   * @param ascending Sort in ascending order (default: true)
   * @returns Sorted array of messages
   */
  static sortMessagesByTime(messages: Message[], ascending: boolean = true): Message[] {
    if (!messages || messages.length === 0) {
      return [];
    }

    return [...messages].sort((a, b) => {
      const timeA = a.timestamp.getTime();
      const timeB = b.timestamp.getTime();
      return ascending ? timeA - timeB : timeB - timeA;
    });
  }

  /**
   * Group messages by date
   * @param messages Array of messages
   * @returns Map of date strings to message arrays
   */
  static groupMessagesByDate(messages: Message[]): Map<string, Message[]> {
    const grouped = new Map<string, Message[]>();

    if (!messages || messages.length === 0) {
      return grouped;
    }

    messages.forEach(message => {
      const dateKey = message.timestamp.toDateString();
      if (!grouped.has(dateKey)) {
        grouped.set(dateKey, []);
      }
      grouped.get(dateKey)!.push(message);
    });

    return grouped;
  }

  /**
   * Filter messages by sender
   * @param messages Array of messages
   * @param senderId Sender user ID
   * @returns Filtered array of messages
   */
  static filterMessagesBySender(messages: Message[], senderId: number): Message[] {
    if (!messages || messages.length === 0) {
      return [];
    }

    return messages.filter(msg => msg.senderId === senderId);
  }

  /**
   * Check if a chat room has unread messages for a user
   * @param room Chat room object
   * @param userId User ID to check for
   * @param messages Array of all messages
   * @returns True if room has unread messages
   */
  static hasUnreadMessages(room: ChatRoom, userId: number, messages: Message[]): boolean {
    if (!room || !messages || messages.length === 0) {
      return false;
    }

    const roomMessages = messages.filter(
      msg => room.participants.includes(msg.senderId) &&
             room.participants.includes(msg.recipientId)
    );

    return this.getUnreadCount(roomMessages, userId) > 0;
  }

  /**
   * Get the latest message in a chat room
   * @param room Chat room object
   * @param messages Array of all messages
   * @returns Latest message or undefined
   */
  static getLatestMessage(room: ChatRoom, messages: Message[]): Message | undefined {
    if (!room || !messages || messages.length === 0) {
      return undefined;
    }

    const roomMessages = messages.filter(
      msg => room.participants.includes(msg.senderId) &&
             room.participants.includes(msg.recipientId)
    );

    if (roomMessages.length === 0) {
      return undefined;
    }

    return this.sortMessagesByTime(roomMessages, false)[0];
  }

  /**
   * Check if user is participant in a room
   * @param room Chat room object
   * @param userId User ID to check
   * @returns True if user is participant
   */
  static isParticipant(room: ChatRoom, userId: number): boolean {
    if (!room || !room.participants) {
      return false;
    }

    return room.participants.includes(userId);
  }

  /**
   * Get other participants in a room (excluding specified user)
   * @param room Chat room object
   * @param userId User ID to exclude
   * @returns Array of participant IDs
   */
  static getOtherParticipants(room: ChatRoom, userId: number): number[] {
    if (!room || !room.participants) {
      return [];
    }

    return room.participants.filter(id => id !== userId);
  }

  /**
   * Format room name for display
   * @param room Chat room object
   * @param users Array of all users
   * @param currentUserId Current user's ID
   * @returns Formatted room name
   */
  static formatRoomName(room: ChatRoom, users: User[], currentUserId: number): string {
    if (!room) {
      return 'Unknown Room';
    }

    // If room has a custom name, use it
    if (room.name && room.name.trim().length > 0) {
      return room.name;
    }

    // For direct messages, show other participant's name
    const otherParticipants = this.getOtherParticipants(room, currentUserId);
    if (otherParticipants.length === 1) {
      const otherUser = users.find(u => u.id === otherParticipants[0]);
      return otherUser ? this.getUserDisplayName(otherUser) : 'Unknown User';
    }

    // For group chats, show participant count
    return `Group Chat (${room.participants.length} members)`;
  }

  /**
   * Validate message content
   * @param content Message content to validate
   * @param maxLength Maximum allowed length (default: 5000)
   * @returns True if valid
   */
  static isValidMessageContent(content: string, maxLength: number = 5000): boolean {
    if (!content || typeof content !== 'string') {
      return false;
    }

    if (content.trim().length === 0) {
      return false;
    }

    if (content.length > maxLength) {
      return false;
    }

    return true;
  }
}

export { User, Message, ChatRoom };
