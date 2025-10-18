import { ChatUtils, User, Message, ChatRoom } from './chatUtils';

describe('ChatUtils', () => {
  const mockUser: User = {
    id: 1,
    username: 'testuser',
    displayName: 'Test User',
    online: true,
    lastSeen: new Date(),
  };

  const mockMessage: Message = {
    id: 1,
    content: 'Test message',
    senderId: 1,
    recipientId: 2,
    timestamp: new Date(),
    read: false,
    delivered: true,
  };

  const mockRoom: ChatRoom = {
    id: 1,
    name: 'Test Room',
    participants: [1, 2, 3],
    createdAt: new Date(),
  };

  describe('isUserOnline', () => {
    it('should return true for online user', () => {
      expect(ChatUtils.isUserOnline(mockUser)).toBe(true);
    });

    it('should return false for offline user', () => {
      const offlineUser = { ...mockUser, online: false };
      expect(ChatUtils.isUserOnline(offlineUser)).toBe(false);
    });
  });

  describe('getUserDisplayName', () => {
    it('should return display name if available', () => {
      expect(ChatUtils.getUserDisplayName(mockUser)).toBe('Test User');
    });

    it('should return username if no display name', () => {
      const user = { ...mockUser, displayName: undefined };
      expect(ChatUtils.getUserDisplayName(user)).toBe('testuser');
    });

    it('should return "Unknown User" for null user', () => {
      expect(ChatUtils.getUserDisplayName(null as any)).toBe('Unknown User');
    });
  });

  describe('getLastSeenText', () => {
    it('should return "Never" for undefined lastSeen', () => {
      expect(ChatUtils.getLastSeenText(undefined)).toBe('Never');
    });

    it('should return "Just now" for very recent timestamp', () => {
      const now = new Date();
      expect(ChatUtils.getLastSeenText(now)).toBe('Just now');
    });
  });

  describe('isMessageRead', () => {
    it('should return false for unread message', () => {
      expect(ChatUtils.isMessageRead(mockMessage)).toBe(false);
    });

    it('should return true for read message', () => {
      const readMessage = { ...mockMessage, read: true };
      expect(ChatUtils.isMessageRead(readMessage)).toBe(true);
    });
  });

  describe('isMessageDelivered', () => {
    it('should return true for delivered message', () => {
      expect(ChatUtils.isMessageDelivered(mockMessage)).toBe(true);
    });

    it('should return false for undelivered message', () => {
      const undeliveredMessage = { ...mockMessage, delivered: false };
      expect(ChatUtils.isMessageDelivered(undeliveredMessage)).toBe(false);
    });
  });

  describe('getUnreadCount', () => {
    const messages: Message[] = [
      { ...mockMessage, id: 1, recipientId: 1, read: false },
      { ...mockMessage, id: 2, recipientId: 1, read: false },
      { ...mockMessage, id: 3, recipientId: 1, read: true },
      { ...mockMessage, id: 4, recipientId: 2, read: false },
    ];

    it('should count unread messages for user', () => {
      expect(ChatUtils.getUnreadCount(messages, 1)).toBe(2);
    });

    it('should return 0 for empty messages', () => {
      expect(ChatUtils.getUnreadCount([], 1)).toBe(0);
    });

    it('should return 0 when all messages are read', () => {
      expect(ChatUtils.getUnreadCount(messages, 3)).toBe(0);
    });
  });

  describe('sortMessagesByTime', () => {
    const messages: Message[] = [
      { ...mockMessage, id: 1, timestamp: new Date('2024-01-03') },
      { ...mockMessage, id: 2, timestamp: new Date('2024-01-01') },
      { ...mockMessage, id: 3, timestamp: new Date('2024-01-02') },
    ];

    it('should sort messages in ascending order by default', () => {
      const sorted = ChatUtils.sortMessagesByTime(messages);
      expect(sorted[0].id).toBe(2);
      expect(sorted[1].id).toBe(3);
      expect(sorted[2].id).toBe(1);
    });

    it('should sort messages in descending order when specified', () => {
      const sorted = ChatUtils.sortMessagesByTime(messages, false);
      expect(sorted[0].id).toBe(1);
      expect(sorted[1].id).toBe(3);
      expect(sorted[2].id).toBe(2);
    });

    it('should return empty array for empty input', () => {
      expect(ChatUtils.sortMessagesByTime([])).toEqual([]);
    });
  });

  describe('filterMessagesBySender', () => {
    const messages: Message[] = [
      { ...mockMessage, id: 1, senderId: 1 },
      { ...mockMessage, id: 2, senderId: 2 },
      { ...mockMessage, id: 3, senderId: 1 },
    ];

    it('should filter messages by sender', () => {
      const filtered = ChatUtils.filterMessagesBySender(messages, 1);
      expect(filtered).toHaveLength(2);
      expect(filtered.every(m => m.senderId === 1)).toBe(true);
    });

    it('should return empty array when no matches', () => {
      expect(ChatUtils.filterMessagesBySender(messages, 999)).toEqual([]);
    });
  });

  describe('isParticipant', () => {
    it('should return true for participant', () => {
      expect(ChatUtils.isParticipant(mockRoom, 1)).toBe(true);
    });

    it('should return false for non-participant', () => {
      expect(ChatUtils.isParticipant(mockRoom, 999)).toBe(false);
    });

    it('should return false for null room', () => {
      expect(ChatUtils.isParticipant(null as any, 1)).toBe(false);
    });
  });

  describe('getOtherParticipants', () => {
    it('should return other participants excluding current user', () => {
      const others = ChatUtils.getOtherParticipants(mockRoom, 1);
      expect(others).toEqual([2, 3]);
    });

    it('should return empty array for null room', () => {
      expect(ChatUtils.getOtherParticipants(null as any, 1)).toEqual([]);
    });
  });

  describe('isValidMessageContent', () => {
    it('should return true for valid content', () => {
      expect(ChatUtils.isValidMessageContent('Hello world')).toBe(true);
    });

    it('should return false for empty content', () => {
      expect(ChatUtils.isValidMessageContent('')).toBe(false);
    });

    it('should return false for whitespace only', () => {
      expect(ChatUtils.isValidMessageContent('   ')).toBe(false);
    });

    it('should return false for content exceeding max length', () => {
      const longContent = 'a'.repeat(6000);
      expect(ChatUtils.isValidMessageContent(longContent, 5000)).toBe(false);
    });

    it('should return false for null content', () => {
      expect(ChatUtils.isValidMessageContent(null as any)).toBe(false);
    });
  });
});
