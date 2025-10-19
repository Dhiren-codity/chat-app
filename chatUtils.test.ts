import { describe, it, expect, jest } from '@jest/globals';
// Import the code to be tested

describe('ChatUtils', () => {
  import { ChatUtils } from './ChatUtils';
  
  describe('ChatUtils', () => {
    let chatUtils: ChatUtils;
  
    beforeEach(() => {
      chatUtils = new ChatUtils();
    });
  
    describe('isUserOnline', () => {
      it('should return true if user is online', () => {
        const user = { online: true };
        expect(chatUtils.isUserOnline(user)).toBe(true);
      });
  
      it('should return false if user is offline', () => {
        const user = { online: false };
        expect(chatUtils.isUserOnline(user)).toBe(false);
      });
  
      it('should return false if user is null', () => {
        const user = null;
        expect(chatUtils.isUserOnline(user)).toBe(false);
      });
  
      it('should return false if user is undefined', () => {
        const user = undefined;
        expect(chatUtils.isUserOnline(user)).toBe(false);
      });
  
      it('should return false if user object does not have online property', () => {
        const user = {};
        expect(chatUtils.isUserOnline(user)).toBe(false);
      });
  
      it('should return false if user object has online property with non-boolean value', () => {
        const user = { online: 'yes' };
        expect(chatUtils.isUserOnline(user)).toBe(false);
      });
    });
  });

  import { ChatUtils } from './ChatUtils'; // Adjust the import path as necessary
  
  describe('ChatUtils', () => {
    let chatUtils: ChatUtils;
  
    beforeEach(() => {
      chatUtils = new ChatUtils();
    });
  
    describe('getUserDisplayName', () => {
      it('should return "Unknown User" when user is null', () => {
        const result = chatUtils.getUserDisplayName(null);
        expect(result).toBe('Unknown User');
      });
  
      it('should return "Unknown User" when user is undefined', () => {
        const result = chatUtils.getUserDisplayName(undefined);
        expect(result).toBe('Unknown User');
      });
  
      it('should return displayName when it is available', () => {
        const user = { displayName: 'John Doe', username: 'johndoe' };
        const result = chatUtils.getUserDisplayName(user);
        expect(result).toBe('John Doe');
      });
  
      it('should return username when displayName is not available', () => {
        const user = { displayName: null, username: 'johndoe' };
        const result = chatUtils.getUserDisplayName(user);
        expect(result).toBe('johndoe');
      });
  
      it('should return "Unknown User" when both displayName and username are not available', () => {
        const user = { displayName: null, username: null };
        const result = chatUtils.getUserDisplayName(user);
        expect(result).toBe('Unknown User');
      });
  
      it('should return "Unknown User" when user object is empty', () => {
        const user = {};
        const result = chatUtils.getUserDisplayName(user);
        expect(result).toBe('Unknown User');
      });
    });
  });

  import { ChatUtils } from './ChatUtils';
  
  describe('ChatUtils', () => {
    let chatUtils: ChatUtils;
  
    beforeEach(() => {
      chatUtils = new ChatUtils();
    });
  
    describe('methodToTest', () => {
      it('should return "Unknown User" for undefined input', () => {
        const result = chatUtils.methodToTest(undefined);
        expect(result).toBe('Unknown User');
      });
  
      it('should return "Unknown User" for null input', () => {
        const result = chatUtils.methodToTest(null);
        expect(result).toBe('Unknown User');
      });
  
      it('should return "Unknown User" for empty string input', () => {
        const result = chatUtils.methodToTest('');
        expect(result).toBe('Unknown User');
      });
  
      it('should return "Unknown User" for non-string input', () => {
        const result = chatUtils.methodToTest(123);
        expect(result).toBe('Unknown User');
      });
  
      it('should return "Unknown User" for object input', () => {
        const result = chatUtils.methodToTest({});
        expect(result).toBe('Unknown User');
      });
  
      it('should return "Unknown User" for array input', () => {
        const result = chatUtils.methodToTest([]);
        expect(result).toBe('Unknown User');
      });
  
      it('should return "Unknown User" for boolean input', () => {
        const result = chatUtils.methodToTest(true);
        expect(result).toBe('Unknown User');
      });
  
      it('should return "Unknown User" for function input', () => {
        const result = chatUtils.methodToTest(() => {});
        expect(result).toBe('Unknown User');
      });
    });
  });

  import { ChatUtils } from './ChatUtils';
  
  describe('ChatUtils', () => {
    let chatUtils: ChatUtils;
  
    beforeEach(() => {
      chatUtils = new ChatUtils();
    });
  
    describe('getLastSeenText', () => {
      it('should return "Never" if lastSeen is null', () => {
        expect(chatUtils.getLastSeenText(null)).toBe('Never');
      });
  
      it('should return "Just now" if lastSeen is less than a minute ago', () => {
        const now = new Date();
        const lastSeen = new Date(now.getTime() - 30000); // 30 seconds ago
        expect(chatUtils.getLastSeenText(lastSeen)).toBe('Just now');
      });
  
      it('should return "1 minute ago" if lastSeen is exactly one minute ago', () => {
        const now = new Date();
        const lastSeen = new Date(now.getTime() - 60000); // 1 minute ago
        expect(chatUtils.getLastSeenText(lastSeen)).toBe('1 minute ago');
      });
  
      it('should return "5 minutes ago" if lastSeen is 5 minutes ago', () => {
        const now = new Date();
        const lastSeen = new Date(now.getTime() - 5 * 60000); // 5 minutes ago
        expect(chatUtils.getLastSeenText(lastSeen)).toBe('5 minutes ago');
      });
  
      it('should return "1 hour ago" if lastSeen is exactly one hour ago', () => {
        const now = new Date();
        const lastSeen = new Date(now.getTime() - 3600000); // 1 hour ago
        expect(chatUtils.getLastSeenText(lastSeen)).toBe('1 hour ago');
      });
  
      it('should return "3 hours ago" if lastSeen is 3 hours ago', () => {
        const now = new Date();
        const lastSeen = new Date(now.getTime() - 3 * 3600000); // 3 hours ago
        expect(chatUtils.getLastSeenText(lastSeen)).toBe('3 hours ago');
      });
  
      it('should return "1 day ago" if lastSeen is exactly one day ago', () => {
        const now = new Date();
        const lastSeen = new Date(now.getTime() - 86400000); // 1 day ago
        expect(chatUtils.getLastSeenText(lastSeen)).toBe('1 day ago');
      });
  
      it('should return "10 days ago" if lastSeen is 10 days ago', () => {
        const now = new Date();
        const lastSeen = new Date(now.getTime() - 10 * 86400000); // 10 days ago
        expect(chatUtils.getLastSeenText(lastSeen)).toBe('10 days ago');
      });
  
      it('should return the date string if lastSeen is more than 30 days ago', () => {
        const now = new Date();
        const lastSeen = new Date(now.getTime() - 31 * 86400000); // 31 days ago
        expect(chatUtils.getLastSeenText(lastSeen)).toBe(lastSeen.toLocaleDateString());
      });
    });
  });

  import { ChatUtils } from './ChatUtils';
  
  describe('ChatUtils', () => {
    let chatUtils: ChatUtils;
  
    beforeEach(() => {
      chatUtils = new ChatUtils();
    });
  
    describe('methodToTest', () => {
      it('should return "Never" for a typical input', () => {
        const result = chatUtils.methodToTest('some input');
        expect(result).toBe('Never');
      });
  
      it('should return "Never" for an empty string input', () => {
        const result = chatUtils.methodToTest('');
        expect(result).toBe('Never');
      });
  
      it('should return "Never" for a null input', () => {
        const result = chatUtils.methodToTest(null);
        expect(result).toBe('Never');
      });
  
      it('should return "Never" for an undefined input', () => {
        const result = chatUtils.methodToTest(undefined);
        expect(result).toBe('Never');
      });
  
      it('should return "Never" for a number input', () => {
        const result = chatUtils.methodToTest(123);
        expect(result).toBe('Never');
      });
  
      it('should return "Never" for a boolean input', () => {
        const result = chatUtils.methodToTest(true);
        expect(result).toBe('Never');
      });
  
      it('should return "Never" for an object input', () => {
        const result = chatUtils.methodToTest({ key: 'value' });
        expect(result).toBe('Never');
      });
  
      it('should return "Never" for an array input', () => {
        const result = chatUtils.methodToTest(['array', 'of', 'values']);
        expect(result).toBe('Never');
      });
    });
  });

  import { ChatUtils } from './ChatUtils';
  
  describe('ChatUtils', () => {
    let chatUtils: ChatUtils;
  
    beforeEach(() => {
      chatUtils = new ChatUtils();
    });
  
    describe('methodToTest', () => {
      it('should return "Just now" for the happy path', () => {
        const result = chatUtils.methodToTest();
        expect(result).toBe('Just now');
      });
  
      it('should handle edge case 1', () => {
        const result = chatUtils.methodToTest();
        expect(result).toBe('Just now');
      });
  
      it('should handle edge case 2', () => {
        const result = chatUtils.methodToTest();
        expect(result).toBe('Just now');
      });
  
      // Add more test cases as needed
    });
  });

  import { ChatUtils } from './ChatUtils';
  
  describe('ChatUtils', () => {
    let chatUtils: ChatUtils;
  
    beforeEach(() => {
      chatUtils = new ChatUtils();
    });
  
    describe('formatMinutesAgo', () => {
      it('should return "1 minute ago" for 1 minute', () => {
        const result = chatUtils.formatMinutesAgo(1);
        expect(result).toBe('1 minute ago');
      });
  
      it('should return "2 minutes ago" for 2 minutes', () => {
        const result = chatUtils.formatMinutesAgo(2);
        expect(result).toBe('2 minutes ago');
      });
  
      it('should return "0 minutes ago" for 0 minutes', () => {
        const result = chatUtils.formatMinutesAgo(0);
        expect(result).toBe('0 minutes ago');
      });
  
      it('should return "59 minutes ago" for 59 minutes', () => {
        const result = chatUtils.formatMinutesAgo(59);
        expect(result).toBe('59 minutes ago');
      });
  
      it('should handle large numbers correctly', () => {
        const result = chatUtils.formatMinutesAgo(1000);
        expect(result).toBe('1000 minutes ago');
      });
  
      it('should handle negative numbers gracefully', () => {
        const result = chatUtils.formatMinutesAgo(-5);
        expect(result).toBe('-5 minutes ago');
      });
    });
  });

  import { ChatUtils } from './ChatUtils';
  
  describe('ChatUtils', () => {
    let chatUtils: ChatUtils;
  
    beforeEach(() => {
      chatUtils = new ChatUtils();
    });
  
    describe('method to test', () => {
      it('should return "1 hour ago" when diffHours is 1', () => {
        const diffHours = 1;
        const result = chatUtils.methodToTest(diffHours);
        expect(result).toBe('1 hour ago');
      });
  
      it('should return "2 hours ago" when diffHours is 2', () => {
        const diffHours = 2;
        const result = chatUtils.methodToTest(diffHours);
        expect(result).toBe('2 hours ago');
      });
  
      it('should return "0 hours ago" when diffHours is 0', () => {
        const diffHours = 0;
        const result = chatUtils.methodToTest(diffHours);
        expect(result).toBe('0 hours ago');
      });
  
      it('should return "-1 hours ago" when diffHours is -1', () => {
        const diffHours = -1;
        const result = chatUtils.methodToTest(diffHours);
        expect(result).toBe('-1 hours ago');
      });
  
      it('should return "100 hours ago" when diffHours is 100', () => {
        const diffHours = 100;
        const result = chatUtils.methodToTest(diffHours);
        expect(result).toBe('100 hours ago');
      });
    });
  });

  import { ChatUtils } from './ChatUtils';
  
  describe('ChatUtils', () => {
    let chatUtils: ChatUtils;
  
    beforeEach(() => {
      chatUtils = new ChatUtils();
    });
  
    describe('formatDaysAgo', () => {
      it('should return "1 day ago" for 1 day', () => {
        const result = chatUtils.formatDaysAgo(1);
        expect(result).toBe('1 day ago');
      });
  
      it('should return "2 days ago" for 2 days', () => {
        const result = chatUtils.formatDaysAgo(2);
        expect(result).toBe('2 days ago');
      });
  
      it('should return "0 days ago" for 0 days', () => {
        const result = chatUtils.formatDaysAgo(0);
        expect(result).toBe('0 days ago');
      });
  
      it('should return "100 days ago" for 100 days', () => {
        const result = chatUtils.formatDaysAgo(100);
        expect(result).toBe('100 days ago');
      });
  
      it('should handle negative days gracefully', () => {
        const result = chatUtils.formatDaysAgo(-5);
        expect(result).toBe('-5 days ago');
      });
    });
  });

  import { ChatUtils } from './ChatUtils';
  
  describe('ChatUtils', () => {
    let chatUtils: ChatUtils;
  
    beforeEach(() => {
      chatUtils = new ChatUtils();
    });
  
    describe('isMessageRead', () => {
      it('should return true if message is read', () => {
        const message = { read: true };
        expect(chatUtils.isMessageRead(message)).toBe(true);
      });
  
      it('should return false if message is not read', () => {
        const message = { read: false };
        expect(chatUtils.isMessageRead(message)).toBe(false);
      });
  
      it('should return false if message is null', () => {
        const message = null;
        expect(chatUtils.isMessageRead(message)).toBe(false);
      });
  
      it('should return false if message is undefined', () => {
        const message = undefined;
        expect(chatUtils.isMessageRead(message)).toBe(false);
      });
  
      it('should return false if message does not have read property', () => {
        const message = {};
        expect(chatUtils.isMessageRead(message)).toBe(false);
      });
  
      it('should return false if message is an empty object', () => {
        const message = {};
        expect(chatUtils.isMessageRead(message)).toBe(false);
      });
  
      it('should return false if message.read is not a boolean', () => {
        const message = { read: 'true' };
        expect(chatUtils.isMessageRead(message)).toBe(false);
      });
    });
  });

  import { ChatUtils } from './ChatUtils';
  
  describe('ChatUtils', () => {
    let chatUtils: ChatUtils;
  
    beforeEach(() => {
      chatUtils = new ChatUtils();
    });
  
    describe('isMessageDelivered', () => {
      it('should return true when message is delivered', () => {
        const message = { delivered: true };
        expect(chatUtils.isMessageDelivered(message)).toBe(true);
      });
  
      it('should return false when message is not delivered', () => {
        const message = { delivered: false };
        expect(chatUtils.isMessageDelivered(message)).toBe(false);
      });
  
      it('should return false when message is undefined', () => {
        const message = undefined;
        expect(chatUtils.isMessageDelivered(message)).toBe(false);
      });
  
      it('should return false when message is null', () => {
        const message = null;
        expect(chatUtils.isMessageDelivered(message)).toBe(false);
      });
  
      it('should return false when message does not have delivered property', () => {
        const message = {};
        expect(chatUtils.isMessageDelivered(message)).toBe(false);
      });
  
      it('should return false when delivered property is not a boolean', () => {
        const message = { delivered: 'yes' };
        expect(chatUtils.isMessageDelivered(message)).toBe(false);
      });
    });
  });

  import { ChatUtils } from './ChatUtils';
  
  describe('ChatUtils', () => {
    let chatUtils: ChatUtils;
  
    beforeEach(() => {
      chatUtils = new ChatUtils();
    });
  
    describe('getUnreadCount', () => {
      it('should return 0 if messages array is null', () => {
        const result = chatUtils.getUnreadCount(null, 'user1');
        expect(result).toBe(0);
      });
  
      it('should return 0 if messages array is empty', () => {
        const result = chatUtils.getUnreadCount([], 'user1');
        expect(result).toBe(0);
      });
  
      it('should return 0 if there are no unread messages for the user', () => {
        const messages = [
        { recipientId: 'user1', read: true },
        { recipientId: 'user2', read: false },
        { recipientId: 'user1', read: true }
        ];
        const result = chatUtils.getUnreadCount(messages, 'user1');
        expect(result).toBe(0);
      });
  
      it('should return the correct count of unread messages for the user', () => {
        const messages = [
        { recipientId: 'user1', read: false },
        { recipientId: 'user1', read: false },
        { recipientId: 'user2', read: false },
        { recipientId: 'user1', read: true }
        ];
        const result = chatUtils.getUnreadCount(messages, 'user1');
        expect(result).toBe(2);
      });
  
      it('should return 0 if userId does not match any recipientId', () => {
        const messages = [
        { recipientId: 'user2', read: false },
        { recipientId: 'user3', read: false }
        ];
        const result = chatUtils.getUnreadCount(messages, 'user1');
        expect(result).toBe(0);
      });
  
      it('should handle messages with undefined read status', () => {
        const messages = [
        { recipientId: 'user1', read: undefined },
        { recipientId: 'user1', read: false },
        { recipientId: 'user1', read: true }
        ];
        const result = chatUtils.getUnreadCount(messages, 'user1');
        expect(result).toBe(1);
      });
    });
  });

  import { ChatUtils } from './ChatUtils';
  
  describe('ChatUtils', () => {
    let chatUtils: ChatUtils;
  
    beforeEach(() => {
      chatUtils = new ChatUtils();
    });
  
    describe('methodToTest', () => {
      it('should return 0 for a typical input', () => {
        const result = chatUtils.methodToTest('typical input');
        expect(result).toBe(0);
      });
  
      it('should return 0 for an empty string input', () => {
        const result = chatUtils.methodToTest('');
        expect(result).toBe(0);
      });
  
      it('should return 0 for a null input', () => {
        const result = chatUtils.methodToTest(null);
        expect(result).toBe(0);
      });
  
      it('should return 0 for an undefined input', () => {
        const result = chatUtils.methodToTest(undefined);
        expect(result).toBe(0);
      });
  
      it('should return 0 for a number input', () => {
        const result = chatUtils.methodToTest(123);
        expect(result).toBe(0);
      });
  
      it('should return 0 for a boolean input', () => {
        const result = chatUtils.methodToTest(true);
        expect(result).toBe(0);
      });
  
      it('should return 0 for an object input', () => {
        const result = chatUtils.methodToTest({ key: 'value' });
        expect(result).toBe(0);
      });
  
      it('should return 0 for an array input', () => {
        const result = chatUtils.methodToTest(['array', 'of', 'values']);
        expect(result).toBe(0);
      });
    });
  });

  import { ChatUtils } from './ChatUtils';
  
  describe('ChatUtils', () => {
    let chatUtils: ChatUtils;
  
    beforeEach(() => {
      chatUtils = new ChatUtils();
    });
  
    describe('sortMessagesByTime', () => {
      it('should return an empty array when messages is null', () => {
        const result = chatUtils.sortMessagesByTime(null, true);
        expect(result).toEqual([]);
      });
  
      it('should return an empty array when messages is an empty array', () => {
        const result = chatUtils.sortMessagesByTime([], true);
        expect(result).toEqual([]);
      });
  
      it('should sort messages in ascending order by timestamp', () => {
        const messages = [
        { timestamp: new Date('2023-10-01T10:00:00Z') },
        { timestamp: new Date('2023-10-01T09:00:00Z') },
        { timestamp: new Date('2023-10-01T11:00:00Z') },
        ];
        const result = chatUtils.sortMessagesByTime(messages, true);
        expect(result).toEqual([
          { timestamp: new Date('2023-10-01T09:00:00Z') },
          { timestamp: new Date('2023-10-01T10:00:00Z') },
          { timestamp: new Date('2023-10-01T11:00:00Z') },
        ]);
      });
  
      it('should sort messages in descending order by timestamp', () => {
        const messages = [
        { timestamp: new Date('2023-10-01T10:00:00Z') },
        { timestamp: new Date('2023-10-01T09:00:00Z') },
        { timestamp: new Date('2023-10-01T11:00:00Z') },
        ];
        const result = chatUtils.sortMessagesByTime(messages, false);
        expect(result).toEqual([
          { timestamp: new Date('2023-10-01T11:00:00Z') },
          { timestamp: new Date('2023-10-01T10:00:00Z') },
          { timestamp: new Date('2023-10-01T09:00:00Z') },
        ]);
      });
  
      it('should handle messages with the same timestamp', () => {
        const messages = [
        { timestamp: new Date('2023-10-01T10:00:00Z') },
        { timestamp: new Date('2023-10-01T10:00:00Z') },
        { timestamp: new Date('2023-10-01T11:00:00Z') },
        ];
        const result = chatUtils.sortMessagesByTime(messages, true);
        expect(result).toEqual([
          { timestamp: new Date('2023-10-01T10:00:00Z') },
          { timestamp: new Date('2023-10-01T10:00:00Z') },
          { timestamp: new Date('2023-10-01T11:00:00Z') },
        ]);
      });
    });
  });

  import { ChatUtils } from './ChatUtils';
  
  describe('ChatUtils', () => {
    let chatUtils: ChatUtils;
  
    beforeEach(() => {
      chatUtils = new ChatUtils();
    });
  
    describe('methodToTest', () => {
      it('should return an empty array for null input', () => {
        const result = chatUtils.methodToTest(null);
        expect(result).toEqual([]);
      });
  
      it('should return an empty array for undefined input', () => {
        const result = chatUtils.methodToTest(undefined);
        expect(result).toEqual([]);
      });
  
      it('should return an empty array for empty string input', () => {
        const result = chatUtils.methodToTest('');
        expect(result).toEqual([]);
      });
  
      it('should return an empty array for empty array input', () => {
        const result = chatUtils.methodToTest([]);
        expect(result).toEqual([]);
      });
  
      it('should return an empty array for non-empty string input', () => {
        const result = chatUtils.methodToTest('test');
        expect(result).toEqual([]);
      });
  
      it('should return an empty array for non-empty array input', () => {
        const result = chatUtils.methodToTest(['test']);
        expect(result).toEqual([]);
      });
  
      it('should return an empty array for object input', () => {
        const result = chatUtils.methodToTest({ key: 'value' });
        expect(result).toEqual([]);
      });
  
      it('should return an empty array for number input', () => {
        const result = chatUtils.methodToTest(123);
        expect(result).toEqual([]);
      });
  
      it('should return an empty array for boolean input', () => {
        const result = chatUtils.methodToTest(true);
        expect(result).toEqual([]);
      });
    });
  });

  import { ChatUtils } from './ChatUtils'; // Adjust the import path as necessary
  
  describe('ChatUtils', () => {
    let chatUtils: ChatUtils;
  
    beforeEach(() => {
      chatUtils = new ChatUtils();
    });
  
    describe('groupMessagesByDate', () => {
      it('should return an empty map when messages is null', () => {
        const result = chatUtils.groupMessagesByDate(null);
        expect(result).toEqual(new Map());
      });
  
      it('should return an empty map when messages is an empty array', () => {
        const result = chatUtils.groupMessagesByDate([]);
        expect(result).toEqual(new Map());
      });
  
      it('should group messages by date correctly', () => {
        const messages = [
        { timestamp: new Date('2023-10-01T10:00:00Z'), content: 'Hello' },
        { timestamp: new Date('2023-10-01T12:00:00Z'), content: 'Hi' },
        { timestamp: new Date('2023-10-02T09:00:00Z'), content: 'Good morning' },
        ];
        const result = chatUtils.groupMessagesByDate(messages);
        expect(result.size).toBe(2);
        expect(result.get('Sun Oct 01 2023')).toEqual([
          { timestamp: new Date('2023-10-01T10:00:00Z'), content: 'Hello' },
          { timestamp: new Date('2023-10-01T12:00:00Z'), content: 'Hi' },
        ]);
        expect(result.get('Mon Oct 02 2023')).toEqual([
          { timestamp: new Date('2023-10-02T09:00:00Z'), content: 'Good morning' },
        ]);
      });
  
      it('should handle messages with the same timestamp', () => {
        const messages = [
        { timestamp: new Date('2023-10-01T10:00:00Z'), content: 'Hello' },
        { timestamp: new Date('2023-10-01T10:00:00Z'), content: 'Hi again' },
        ];
        const result = chatUtils.groupMessagesByDate(messages);
        expect(result.size).toBe(1);
        expect(result.get('Sun Oct 01 2023')).toEqual([
          { timestamp: new Date('2023-10-01T10:00:00Z'), content: 'Hello' },
          { timestamp: new Date('2023-10-01T10:00:00Z'), content: 'Hi again' },
        ]);
      });
  
      it('should handle messages with different timezones', () => {
        const messages = [
        { timestamp: new Date('2023-10-01T23:00:00Z'), content: 'Late night' },
        { timestamp: new Date('2023-10-02T01:00:00+02:00'), content: 'Early morning' },
        ];
        const result = chatUtils.groupMessagesByDate(messages);
        expect(result.size).toBe(2);
        expect(result.get('Sun Oct 01 2023')).toEqual([
          { timestamp: new Date('2023-10-01T23:00:00Z'), content: 'Late night' },
        ]);
        expect(result.get('Mon Oct 02 2023')).toEqual([
          { timestamp: new Date('2023-10-02T01:00:00+02:00'), content: 'Early morning' },
        ]);
      });
    });
  });

  import { ChatUtils } from './ChatUtils';
  
  describe('ChatUtils', () => {
    let chatUtils: ChatUtils;
  
    beforeEach(() => {
      chatUtils = new ChatUtils();
    });
  
    describe('methodToTest', () => {
      it('should return grouped data for a valid input', () => {
        const input = [
        { id: 1, group: 'A' },
        { id: 2, group: 'B' },
        { id: 3, group: 'A' }
        ];
        const expectedOutput = {
          A: [{ id: 1, group: 'A' }, { id: 3, group: 'A' }],
          B: [{ id: 2, group: 'B' }]
        };
        expect(chatUtils.methodToTest(input)).toEqual(expectedOutput);
      });
  
      it('should return an empty object for an empty input', () => {
        const input: any[] = [];
        const expectedOutput = {};
        expect(chatUtils.methodToTest(input)).toEqual(expectedOutput);
      });
  
      it('should handle input with no group property', () => {
        const input = [
        { id: 1 },
        { id: 2, group: 'B' },
        { id: 3 }
        ];
        const expectedOutput = {
          B: [{ id: 2, group: 'B' }]
        };
        expect(chatUtils.methodToTest(input)).toEqual(expectedOutput);
      });
  
      it('should handle input with all items having the same group', () => {
        const input = [
        { id: 1, group: 'A' },
        { id: 2, group: 'A' },
        { id: 3, group: 'A' }
        ];
        const expectedOutput = {
          A: [
          { id: 1, group: 'A' },
          { id: 2, group: 'A' },
          { id: 3, group: 'A' }
          ]
        };
        expect(chatUtils.methodToTest(input)).toEqual(expectedOutput);
      });
  
      it('should handle input with mixed data types', () => {
        const input = [
        { id: 1, group: 'A' },
        { id: '2', group: 'B' },
        { id: 3, group: 'A' }
        ];
        const expectedOutput = {
          A: [{ id: 1, group: 'A' }, { id: 3, group: 'A' }],
          B: [{ id: '2', group: 'B' }]
        };
        expect(chatUtils.methodToTest(input)).toEqual(expectedOutput);
      });
    });
  });

  import { ChatUtils } from './ChatUtils';
  
  describe('ChatUtils', () => {
    let chatUtils: ChatUtils;
  
    beforeEach(() => {
      chatUtils = new ChatUtils();
    });
  
    describe('filterMessagesBySender', () => {
      it('should return an empty array when messages is null', () => {
        const result = chatUtils.filterMessagesBySender(null, '123');
        expect(result).toEqual([]);
      });
  
      it('should return an empty array when messages is undefined', () => {
        const result = chatUtils.filterMessagesBySender(undefined, '123');
        expect(result).toEqual([]);
      });
  
      it('should return an empty array when messages is an empty array', () => {
        const result = chatUtils.filterMessagesBySender([], '123');
        expect(result).toEqual([]);
      });
  
      it('should return an empty array when no messages match the senderId', () => {
        const messages = [
        { senderId: '456', text: 'Hello' },
        { senderId: '789', text: 'Hi' }
        ];
        const result = chatUtils.filterMessagesBySender(messages, '123');
        expect(result).toEqual([]);
      });
  
      it('should return only messages that match the senderId', () => {
        const messages = [
        { senderId: '123', text: 'Hello' },
        { senderId: '456', text: 'Hi' },
        { senderId: '123', text: 'How are you?' }
        ];
        const result = chatUtils.filterMessagesBySender(messages, '123');
        expect(result).toEqual([
          { senderId: '123', text: 'Hello' },
          { senderId: '123', text: 'How are you?' }
        ]);
      });
  
      it('should return an empty array when senderId is not provided', () => {
        const messages = [
        { senderId: '123', text: 'Hello' },
        { senderId: '456', text: 'Hi' }
        ];
        const result = chatUtils.filterMessagesBySender(messages, undefined);
        expect(result).toEqual([]);
      });
    });
  });

  import { ChatUtils } from './ChatUtils';
  
  describe('ChatUtils', () => {
    let chatUtils: ChatUtils;
  
    beforeEach(() => {
      chatUtils = new ChatUtils();
    });
  
    describe('methodToTest', () => {
      it('should return an empty array for null input', () => {
        const result = chatUtils.methodToTest(null);
        expect(result).toEqual([]);
      });
  
      it('should return an empty array for undefined input', () => {
        const result = chatUtils.methodToTest(undefined);
        expect(result).toEqual([]);
      });
  
      it('should return an empty array for empty string input', () => {
        const result = chatUtils.methodToTest('');
        expect(result).toEqual([]);
      });
  
      it('should return an empty array for non-empty string input', () => {
        const result = chatUtils.methodToTest('test');
        expect(result).toEqual([]);
      });
  
      it('should return an empty array for number input', () => {
        const result = chatUtils.methodToTest(123);
        expect(result).toEqual([]);
      });
  
      it('should return an empty array for object input', () => {
        const result = chatUtils.methodToTest({ key: 'value' });
        expect(result).toEqual([]);
      });
  
      it('should return an empty array for array input', () => {
        const result = chatUtils.methodToTest([1, 2, 3]);
        expect(result).toEqual([]);
      });
  
      it('should return an empty array for boolean input', () => {
        const result = chatUtils.methodToTest(true);
        expect(result).toEqual([]);
      });
    });
  });

  import { ChatUtils } from './ChatUtils';
  
  describe('ChatUtils', () => {
    let chatUtils: ChatUtils;
  
    beforeEach(() => {
      chatUtils = new ChatUtils();
    });
  
    describe('hasUnreadMessages', () => {
      it('should return false if room is null', () => {
        const result = chatUtils.hasUnreadMessages(null, [], 'userId');
        expect(result).toBe(false);
      });
  
      it('should return false if messages is null', () => {
        const room = { participants: ['user1', 'user2'] };
        const result = chatUtils.hasUnreadMessages(room, null, 'userId');
        expect(result).toBe(false);
      });
  
      it('should return false if messages is an empty array', () => {
        const room = { participants: ['user1', 'user2'] };
        const result = chatUtils.hasUnreadMessages(room, [], 'userId');
        expect(result).toBe(false);
      });
  
      it('should return false if no messages are between room participants', () => {
        const room = { participants: ['user1', 'user2'] };
        const messages = [
        { senderId: 'user3', recipientId: 'user4' },
        { senderId: 'user5', recipientId: 'user6' }
        ];
        const result = chatUtils.hasUnreadMessages(room, messages, 'userId');
        expect(result).toBe(false);
      });
  
      it('should return true if there are unread messages between room participants', () => {
        const room = { participants: ['user1', 'user2'] };
        const messages = [
        { senderId: 'user1', recipientId: 'user2' },
        { senderId: 'user2', recipientId: 'user1' }
        ];
        jest.spyOn(chatUtils, 'getUnreadCount').mockReturnValue(1);
        const result = chatUtils.hasUnreadMessages(room, messages, 'userId');
        expect(result).toBe(true);
      });
  
      it('should return false if there are no unread messages between room participants', () => {
        const room = { participants: ['user1', 'user2'] };
        const messages = [
        { senderId: 'user1', recipientId: 'user2' },
        { senderId: 'user2', recipientId: 'user1' }
        ];
        jest.spyOn(chatUtils, 'getUnreadCount').mockReturnValue(0);
        const result = chatUtils.hasUnreadMessages(room, messages, 'userId');
        expect(result).toBe(false);
      });
    });
  });

  import { ChatUtils } from './ChatUtils';
  
  describe('ChatUtils', () => {
    let chatUtils: ChatUtils;
  
    beforeEach(() => {
      chatUtils = new ChatUtils();
    });
  
    describe('methodToTest', () => {
      it('should return false for a typical input', () => {
        const result = chatUtils.methodToTest('typical input');
        expect(result).toBe(false);
      });
  
      it('should return false for an empty string', () => {
        const result = chatUtils.methodToTest('');
        expect(result).toBe(false);
      });
  
      it('should return false for a null input', () => {
        const result = chatUtils.methodToTest(null);
        expect(result).toBe(false);
      });
  
      it('should return false for an undefined input', () => {
        const result = chatUtils.methodToTest(undefined);
        expect(result).toBe(false);
      });
  
      it('should return false for a number input', () => {
        const result = chatUtils.methodToTest(123);
        expect(result).toBe(false);
      });
  
      it('should return false for a boolean input', () => {
        const result = chatUtils.methodToTest(true);
        expect(result).toBe(false);
      });
  
      it('should return false for an object input', () => {
        const result = chatUtils.methodToTest({ key: 'value' });
        expect(result).toBe(false);
      });
  
      it('should return false for an array input', () => {
        const result = chatUtils.methodToTest(['array', 'of', 'values']);
        expect(result).toBe(false);
      });
    });
  });

  import ChatUtils from './ChatUtils';
  
  describe('ChatUtils', () => {
    let chatUtils: ChatUtils;
  
    beforeEach(() => {
      chatUtils = new ChatUtils();
    });
  
    describe('getLatestMessage', () => {
      it('should return undefined if room is undefined', () => {
        const result = chatUtils.getLatestMessage(undefined, []);
        expect(result).toBeUndefined();
      });
  
      it('should return undefined if messages is undefined', () => {
        const room = { participants: ['user1', 'user2'] };
        const result = chatUtils.getLatestMessage(room, undefined);
        expect(result).toBeUndefined();
      });
  
      it('should return undefined if messages is an empty array', () => {
        const room = { participants: ['user1', 'user2'] };
        const result = chatUtils.getLatestMessage(room, []);
        expect(result).toBeUndefined();
      });
  
      it('should return undefined if no messages are between room participants', () => {
        const room = { participants: ['user1', 'user2'] };
        const messages = [
        { senderId: 'user3', recipientId: 'user4', timestamp: 1 },
        ];
        const result = chatUtils.getLatestMessage(room, messages);
        expect(result).toBeUndefined();
      });
  
      it('should return the latest message between room participants', () => {
        const room = { participants: ['user1', 'user2'] };
        const messages = [
        { senderId: 'user1', recipientId: 'user2', timestamp: 1 },
        { senderId: 'user2', recipientId: 'user1', timestamp: 2 },
        ];
        jest.spyOn(chatUtils, 'sortMessagesByTime').mockReturnValue([
          { senderId: 'user2', recipientId: 'user1', timestamp: 2 },
          { senderId: 'user1', recipientId: 'user2', timestamp: 1 },
        ]);
  
        const result = chatUtils.getLatestMessage(room, messages);
        expect(result).toEqual({ senderId: 'user2', recipientId: 'user1', timestamp: 2 });
      });
  
      it('should handle messages with the same timestamp correctly', () => {
        const room = { participants: ['user1', 'user2'] };
        const messages = [
        { senderId: 'user1', recipientId: 'user2', timestamp: 1 },
        { senderId: 'user2', recipientId: 'user1', timestamp: 1 },
        ];
        jest.spyOn(chatUtils, 'sortMessagesByTime').mockReturnValue([
          { senderId: 'user1', recipientId: 'user2', timestamp: 1 },
          { senderId: 'user2', recipientId: 'user1', timestamp: 1 },
        ]);
  
        const result = chatUtils.getLatestMessage(room, messages);
        expect(result).toEqual({ senderId: 'user1', recipientId: 'user2', timestamp: 1 });
      });
    });
  });

  import { ChatUtils } from './ChatUtils';
  
  describe('ChatUtils', () => {
    let chatUtils: ChatUtils;
  
    beforeEach(() => {
      chatUtils = new ChatUtils();
    });
  
    describe('methodToTest', () => {
      it('should return undefined for null input', () => {
        const result = chatUtils.methodToTest(null);
        expect(result).toBeUndefined();
      });
  
      it('should return undefined for undefined input', () => {
        const result = chatUtils.methodToTest(undefined);
        expect(result).toBeUndefined();
      });
  
      it('should return undefined for empty string input', () => {
        const result = chatUtils.methodToTest('');
        expect(result).toBeUndefined();
      });
  
      it('should return undefined for valid string input', () => {
        const result = chatUtils.methodToTest('valid input');
        expect(result).toBeUndefined();
      });
  
      it('should return undefined for number input', () => {
        const result = chatUtils.methodToTest(123);
        expect(result).toBeUndefined();
      });
  
      it('should return undefined for object input', () => {
        const result = chatUtils.methodToTest({ key: 'value' });
        expect(result).toBeUndefined();
      });
  
      it('should return undefined for array input', () => {
        const result = chatUtils.methodToTest([1, 2, 3]);
        expect(result).toBeUndefined();
      });
  
      it('should return undefined for boolean input', () => {
        const result = chatUtils.methodToTest(true);
        expect(result).toBeUndefined();
      });
    });
  });

  import { ChatUtils } from './ChatUtils';
  
  describe('ChatUtils', () => {
    let chatUtils: ChatUtils;
  
    beforeEach(() => {
      chatUtils = new ChatUtils();
    });
  
    describe('methodToTest', () => {
      it('should return undefined for null input', () => {
        const result = chatUtils.methodToTest(null);
        expect(result).toBeUndefined();
      });
  
      it('should return undefined for undefined input', () => {
        const result = chatUtils.methodToTest(undefined);
        expect(result).toBeUndefined();
      });
  
      it('should return undefined for empty string input', () => {
        const result = chatUtils.methodToTest('');
        expect(result).toBeUndefined();
      });
  
      it('should return undefined for valid string input', () => {
        const result = chatUtils.methodToTest('valid input');
        expect(result).toBeUndefined();
      });
  
      it('should return undefined for number input', () => {
        const result = chatUtils.methodToTest(123);
        expect(result).toBeUndefined();
      });
  
      it('should return undefined for object input', () => {
        const result = chatUtils.methodToTest({ key: 'value' });
        expect(result).toBeUndefined();
      });
  
      it('should return undefined for array input', () => {
        const result = chatUtils.methodToTest([1, 2, 3]);
        expect(result).toBeUndefined();
      });
  
      it('should return undefined for boolean input', () => {
        const result = chatUtils.methodToTest(true);
        expect(result).toBeUndefined();
      });
    });
  });

  import { ChatUtils } from './ChatUtils';
  
  describe('ChatUtils', () => {
    let chatUtils: ChatUtils;
  
    beforeEach(() => {
      chatUtils = new ChatUtils();
    });
  
    describe('isParticipant', () => {
      it('should return false if room is null', () => {
        const result = chatUtils.isParticipant(null, 'user1');
        expect(result).toBe(false);
      });
  
      it('should return false if room is undefined', () => {
        const result = chatUtils.isParticipant(undefined, 'user1');
        expect(result).toBe(false);
      });
  
      it('should return false if room.participants is null', () => {
        const room = { participants: null };
        const result = chatUtils.isParticipant(room, 'user1');
        expect(result).toBe(false);
      });
  
      it('should return false if room.participants is undefined', () => {
        const room = { participants: undefined };
        const result = chatUtils.isParticipant(room, 'user1');
        expect(result).toBe(false);
      });
  
      it('should return false if userId is not in participants', () => {
        const room = { participants: ['user2', 'user3'] };
        const result = chatUtils.isParticipant(room, 'user1');
        expect(result).toBe(false);
      });
  
      it('should return true if userId is in participants', () => {
        const room = { participants: ['user1', 'user2', 'user3'] };
        const result = chatUtils.isParticipant(room, 'user1');
        expect(result).toBe(true);
      });
  
      it('should return false if participants list is empty', () => {
        const room = { participants: [] };
        const result = chatUtils.isParticipant(room, 'user1');
        expect(result).toBe(false);
      });
    });
  });

  import { ChatUtils } from './ChatUtils';
  
  describe('ChatUtils', () => {
    let chatUtils: ChatUtils;
  
    beforeEach(() => {
      chatUtils = new ChatUtils();
    });
  
    describe('methodToTest', () => {
      it('should return false for a typical input', () => {
        const result = chatUtils.methodToTest('typical input');
        expect(result).toBe(false);
      });
  
      it('should return false for an empty string', () => {
        const result = chatUtils.methodToTest('');
        expect(result).toBe(false);
      });
  
      it('should return false for a null input', () => {
        const result = chatUtils.methodToTest(null);
        expect(result).toBe(false);
      });
  
      it('should return false for an undefined input', () => {
        const result = chatUtils.methodToTest(undefined);
        expect(result).toBe(false);
      });
  
      it('should return false for a number input', () => {
        const result = chatUtils.methodToTest(123);
        expect(result).toBe(false);
      });
  
      it('should return false for a boolean input', () => {
        const result = chatUtils.methodToTest(true);
        expect(result).toBe(false);
      });
  
      it('should return false for an object input', () => {
        const result = chatUtils.methodToTest({ key: 'value' });
        expect(result).toBe(false);
      });
  
      it('should return false for an array input', () => {
        const result = chatUtils.methodToTest(['array', 'of', 'values']);
        expect(result).toBe(false);
      });
    });
  });

  import { ChatUtils } from './ChatUtils';
  
  describe('ChatUtils', () => {
    let chatUtils: ChatUtils;
  
    beforeEach(() => {
      chatUtils = new ChatUtils();
    });
  
    describe('getOtherParticipants', () => {
      it('should return an empty array if room is null', () => {
        const result = chatUtils.getOtherParticipants(null, 'user1');
        expect(result).toEqual([]);
      });
  
      it('should return an empty array if room.participants is null', () => {
        const result = chatUtils.getOtherParticipants({ participants: null }, 'user1');
        expect(result).toEqual([]);
      });
  
      it('should return an empty array if room.participants is undefined', () => {
        const result = chatUtils.getOtherParticipants({ participants: undefined }, 'user1');
        expect(result).toEqual([]);
      });
  
      it('should return an empty array if room.participants is an empty array', () => {
        const result = chatUtils.getOtherParticipants({ participants: [] }, 'user1');
        expect(result).toEqual([]);
      });
  
      it('should return all participants except the given userId', () => {
        const room = { participants: ['user1', 'user2', 'user3'] };
        const result = chatUtils.getOtherParticipants(room, 'user1');
        expect(result).toEqual(['user2', 'user3']);
      });
  
      it('should return all participants if userId is not in the list', () => {
        const room = { participants: ['user2', 'user3'] };
        const result = chatUtils.getOtherParticipants(room, 'user1');
        expect(result).toEqual(['user2', 'user3']);
      });
  
      it('should return an empty array if userId is the only participant', () => {
        const room = { participants: ['user1'] };
        const result = chatUtils.getOtherParticipants(room, 'user1');
        expect(result).toEqual([]);
      });
    });
  });

  import { ChatUtils } from './ChatUtils';
  
  describe('ChatUtils', () => {
    let chatUtils: ChatUtils;
  
    beforeEach(() => {
      chatUtils = new ChatUtils();
    });
  
    describe('methodToTest', () => {
      it('should return an empty array for empty input', () => {
        const result = chatUtils.methodToTest();
        expect(result).toEqual([]);
      });
  
      it('should return an empty array for null input', () => {
        const result = chatUtils.methodToTest(null);
        expect(result).toEqual([]);
      });
  
      it('should return an empty array for undefined input', () => {
        const result = chatUtils.methodToTest(undefined);
        expect(result).toEqual([]);
      });
  
      it('should return an empty array for non-empty input', () => {
        const result = chatUtils.methodToTest('some input');
        expect(result).toEqual([]);
      });
  
      it('should return an empty array for numeric input', () => {
        const result = chatUtils.methodToTest(123);
        expect(result).toEqual([]);
      });
  
      it('should return an empty array for object input', () => {
        const result = chatUtils.methodToTest({ key: 'value' });
        expect(result).toEqual([]);
      });
  
      it('should return an empty array for array input', () => {
        const result = chatUtils.methodToTest([1, 2, 3]);
        expect(result).toEqual([]);
      });
    });
  });

  import { ChatUtils } from './ChatUtils';
  
  describe('ChatUtils', () => {
    let chatUtils: ChatUtils;
  
    beforeEach(() => {
      chatUtils = new ChatUtils();
    });
  
    describe('formatRoomName', () => {
      it('should return "Unknown Room" if room is undefined', () => {
        const result = chatUtils.formatRoomName(undefined, 'user1', []);
        expect(result).toBe('Unknown Room');
      });
  
      it('should return "Unknown Room" if room is null', () => {
        const result = chatUtils.formatRoomName(null, 'user1', []);
        expect(result).toBe('Unknown Room');
      });
  
      it('should return room name if room name is valid', () => {
        const room = { name: 'Chat Room', participants: ['user1', 'user2'] };
        const result = chatUtils.formatRoomName(room, 'user1', []);
        expect(result).toBe('Chat Room');
      });
  
      it('should return "Unknown User" if there is one other participant and user is not found', () => {
        const room = { name: '', participants: ['user1', 'user2'] };
        const result = chatUtils.formatRoomName(room, 'user1', []);
        expect(result).toBe('Unknown User');
      });
  
      it('should return other user display name if there is one other participant', () => {
        const room = { name: '', participants: ['user1', 'user2'] };
        const users = [{ id: 'user2', name: 'John Doe' }];
        jest.spyOn(chatUtils, 'getUserDisplayName').mockReturnValue('John Doe');
        const result = chatUtils.formatRoomName(room, 'user1', users);
        expect(result).toBe('John Doe');
      });
  
      it('should return "Group Chat (n members)" if there are multiple participants', () => {
        const room = { name: '', participants: ['user1', 'user2', 'user3'] };
        const result = chatUtils.formatRoomName(room, 'user1', []);
        expect(result).toBe('Group Chat (3 members)');
      });
  
      it('should trim room name and return it if it contains only spaces', () => {
        const room = { name: '   ', participants: ['user1', 'user2'] };
        const result = chatUtils.formatRoomName(room, 'user1', []);
        expect(result).toBe('Unknown User');
      });
    });
  });

  import { ChatUtils } from './ChatUtils';
  
  describe('ChatUtils', () => {
    let chatUtils: ChatUtils;
  
    beforeEach(() => {
      chatUtils = new ChatUtils();
    });
  
    describe('methodToTest', () => {
      it('should return "Unknown Room" for undefined input', () => {
        const result = chatUtils.methodToTest(undefined);
        expect(result).toBe('Unknown Room');
      });
  
      it('should return "Unknown Room" for null input', () => {
        const result = chatUtils.methodToTest(null);
        expect(result).toBe('Unknown Room');
      });
  
      it('should return "Unknown Room" for empty string input', () => {
        const result = chatUtils.methodToTest('');
        expect(result).toBe('Unknown Room');
      });
  
      it('should return "Unknown Room" for non-string input', () => {
        const result = chatUtils.methodToTest(123);
        expect(result).toBe('Unknown Room');
      });
  
      it('should return "Unknown Room" for valid string input', () => {
        const result = chatUtils.methodToTest('validRoom');
        expect(result).toBe('Unknown Room');
      });
    });
  });

  import { ChatUtils } from './ChatUtils'; // Adjust the import path as necessary
  
  describe('ChatUtils', () => {
    let chatUtils: ChatUtils;
  
    beforeEach(() => {
      chatUtils = new ChatUtils();
    });
  
    describe('getOtherUserDisplayName', () => {
      it('should return the display name of the other user when found', () => {
        const users = [
        { id: '1', name: 'Alice' },
        { id: '2', name: 'Bob' }
        ];
        const otherParticipants = ['2'];
        jest.spyOn(chatUtils, 'getUserDisplayName').mockReturnValue('Bob');
  
        const result = chatUtils.getOtherUserDisplayName(users, otherParticipants);
  
        expect(result).toBe('Bob');
        expect(chatUtils.getUserDisplayName).toHaveBeenCalledWith(users[1]);
      });
  
      it('should return "Unknown User" when the other user is not found', () => {
        const users = [
        { id: '1', name: 'Alice' }
        ];
        const otherParticipants = ['2'];
  
        const result = chatUtils.getOtherUserDisplayName(users, otherParticipants);
  
        expect(result).toBe('Unknown User');
      });
  
      it('should return "Unknown User" when otherParticipants is empty', () => {
        const users = [
        { id: '1', name: 'Alice' },
        { id: '2', name: 'Bob' }
        ];
        const otherParticipants: string[] = [];
  
        const result = chatUtils.getOtherUserDisplayName(users, otherParticipants);
  
        expect(result).toBe('Unknown User');
      });
  
      it('should return "Unknown User" when users list is empty', () => {
        const users: { id: string, name: string }[] = [];
        const otherParticipants = ['1'];
  
        const result = chatUtils.getOtherUserDisplayName(users, otherParticipants);
  
        expect(result).toBe('Unknown User');
      });
  
      it('should return "Unknown User" when both users and otherParticipants are empty', () => {
        const users: { id: string, name: string }[] = [];
        const otherParticipants: string[] = [];
  
        const result = chatUtils.getOtherUserDisplayName(users, otherParticipants);
  
        expect(result).toBe('Unknown User');
      });
    });
  });

  import { ChatUtils } from './ChatUtils';
  
  describe('ChatUtils', () => {
    let chatUtils: ChatUtils;
  
    beforeEach(() => {
      chatUtils = new ChatUtils();
    });
  
    describe('getUserDisplayName', () => {
      it('should return the correct display name for a user with both first and last name', () => {
        const user = { firstName: 'John', lastName: 'Doe' };
        const displayName = chatUtils.getUserDisplayName(user);
        expect(displayName).toBe('John Doe');
      });
  
      it('should return the first name if last name is missing', () => {
        const user = { firstName: 'John', lastName: '' };
        const displayName = chatUtils.getUserDisplayName(user);
        expect(displayName).toBe('John');
      });
  
      it('should return the last name if first name is missing', () => {
        const user = { firstName: '', lastName: 'Doe' };
        const displayName = chatUtils.getUserDisplayName(user);
        expect(displayName).toBe('Doe');
      });
  
      it('should return "Anonymous" if both first and last names are missing', () => {
        const user = { firstName: '', lastName: '' };
        const displayName = chatUtils.getUserDisplayName(user);
        expect(displayName).toBe('Anonymous');
      });
  
      it('should handle null or undefined user object gracefully', () => {
        const displayName = chatUtils.getUserDisplayName(null);
        expect(displayName).toBe('Anonymous');
  
        const displayNameUndefined = chatUtils.getUserDisplayName(undefined);
        expect(displayNameUndefined).toBe('Anonymous');
      });
  
      it('should handle user object with undefined first or last name', () => {
        const user = { firstName: undefined, lastName: 'Doe' };
        const displayName = chatUtils.getUserDisplayName(user);
        expect(displayName).toBe('Doe');
  
        const user2 = { firstName: 'John', lastName: undefined };
        const displayName2 = chatUtils.getUserDisplayName(user2);
        expect(displayName2).toBe('John');
      });
    });
  });

  import { ChatUtils } from './ChatUtils'; // Adjust the import path as necessary
  
  describe('ChatUtils', () => {
    let chatUtils: ChatUtils;
    const maxLength = 100; // Example maxLength, adjust as necessary
  
    beforeEach(() => {
      chatUtils = new ChatUtils();
    });
  
    describe('isValidMessageContent', () => {
      it('should return false for null content', () => {
        expect(chatUtils.isValidMessageContent(null, maxLength)).toBe(false);
      });
  
      it('should return false for undefined content', () => {
        expect(chatUtils.isValidMessageContent(undefined, maxLength)).toBe(false);
      });
  
      it('should return false for non-string content', () => {
        expect(chatUtils.isValidMessageContent(123, maxLength)).toBe(false);
        expect(chatUtils.isValidMessageContent({}, maxLength)).toBe(false);
        expect(chatUtils.isValidMessageContent([], maxLength)).toBe(false);
      });
  
      it('should return false for empty string content', () => {
        expect(chatUtils.isValidMessageContent('', maxLength)).toBe(false);
      });
  
      it('should return false for string with only spaces', () => {
        expect(chatUtils.isValidMessageContent('   ', maxLength)).toBe(false);
      });
  
      it('should return false for content exceeding maxLength', () => {
        const longContent = 'a'.repeat(maxLength + 1);
        expect(chatUtils.isValidMessageContent(longContent, maxLength)).toBe(false);
      });
  
      it('should return true for valid content within maxLength', () => {
        const validContent = 'Hello, world!';
        expect(chatUtils.isValidMessageContent(validContent, maxLength)).toBe(true);
      });
  
      it('should return true for content exactly at maxLength', () => {
        const exactLengthContent = 'a'.repeat(maxLength);
        expect(chatUtils.isValidMessageContent(exactLengthContent, maxLength)).toBe(true);
      });
    });
  });

  import { ChatUtils } from './ChatUtils';
  
  describe('ChatUtils', () => {
    let chatUtils: ChatUtils;
  
    beforeEach(() => {
      chatUtils = new ChatUtils();
    });
  
    describe('methodToTest', () => {
      it('should return false for a typical input', () => {
        const result = chatUtils.methodToTest('typical input');
        expect(result).toBe(false);
      });
  
      it('should return false for an empty string', () => {
        const result = chatUtils.methodToTest('');
        expect(result).toBe(false);
      });
  
      it('should return false for a null input', () => {
        const result = chatUtils.methodToTest(null);
        expect(result).toBe(false);
      });
  
      it('should return false for an undefined input', () => {
        const result = chatUtils.methodToTest(undefined);
        expect(result).toBe(false);
      });
  
      it('should return false for a number input', () => {
        const result = chatUtils.methodToTest(123);
        expect(result).toBe(false);
      });
  
      it('should return false for a boolean input', () => {
        const result = chatUtils.methodToTest(true);
        expect(result).toBe(false);
      });
  
      it('should return false for an object input', () => {
        const result = chatUtils.methodToTest({ key: 'value' });
        expect(result).toBe(false);
      });
  
      it('should return false for an array input', () => {
        const result = chatUtils.methodToTest(['array', 'of', 'values']);
        expect(result).toBe(false);
      });
    });
  });

  import { ChatUtils } from './ChatUtils';
  
  describe('ChatUtils', () => {
    let chatUtils: ChatUtils;
  
    beforeEach(() => {
      chatUtils = new ChatUtils();
    });
  
    describe('methodToTest', () => {
      it('should return false for a typical input', () => {
        const result = chatUtils.methodToTest('typical input');
        expect(result).toBe(false);
      });
  
      it('should return false for an empty string', () => {
        const result = chatUtils.methodToTest('');
        expect(result).toBe(false);
      });
  
      it('should return false for a null input', () => {
        const result = chatUtils.methodToTest(null);
        expect(result).toBe(false);
      });
  
      it('should return false for an undefined input', () => {
        const result = chatUtils.methodToTest(undefined);
        expect(result).toBe(false);
      });
  
      it('should return false for a number input', () => {
        const result = chatUtils.methodToTest(123);
        expect(result).toBe(false);
      });
  
      it('should return false for a boolean input', () => {
        const result = chatUtils.methodToTest(true);
        expect(result).toBe(false);
      });
  
      it('should return false for an object input', () => {
        const result = chatUtils.methodToTest({ key: 'value' });
        expect(result).toBe(false);
      });
  
      it('should return false for an array input', () => {
        const result = chatUtils.methodToTest(['array', 'of', 'values']);
        expect(result).toBe(false);
      });
    });
  });

});
