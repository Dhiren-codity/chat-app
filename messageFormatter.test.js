// Import the code to be tested

describe('MessageFormatter', () => {
  const MessageFormatter = require('./MessageFormatter'); // Adjust the path as necessary
  
  describe('MessageFormatter', () => {
    let messageFormatter;
  
    beforeEach(() => {
      messageFormatter = new MessageFormatter();
    });
  
    describe('formatTimestamp', () => {
      it('should return an empty string if timestamp is null', () => {
        expect(messageFormatter.formatTimestamp(null)).toBe('');
      });
  
      it('should return an empty string if timestamp is undefined', () => {
        expect(messageFormatter.formatTimestamp(undefined)).toBe('');
      });
  
      it('should return an empty string if timestamp is invalid', () => {
        expect(messageFormatter.formatTimestamp('invalid')).toBe('');
      });
  
      it('should return "Just now" if the timestamp is less than a minute ago', () => {
        const now = new Date();
        const timestamp = new Date(now.getTime() - 30000).toISOString(); // 30 seconds ago
        expect(messageFormatter.formatTimestamp(timestamp)).toBe('Just now');
      });
  
      it('should return "1 minute ago" if the timestamp is exactly one minute ago', () => {
        const now = new Date();
        const timestamp = new Date(now.getTime() - 60000).toISOString(); // 1 minute ago
        expect(messageFormatter.formatTimestamp(timestamp)).toBe('1 minute ago');
      });
  
      it('should return "5 minutes ago" if the timestamp is 5 minutes ago', () => {
        const now = new Date();
        const timestamp = new Date(now.getTime() - 300000).toISOString(); // 5 minutes ago
        expect(messageFormatter.formatTimestamp(timestamp)).toBe('5 minutes ago');
      });
  
      it('should return "1 hour ago" if the timestamp is exactly one hour ago', () => {
        const now = new Date();
        const timestamp = new Date(now.getTime() - 3600000).toISOString(); // 1 hour ago
        expect(messageFormatter.formatTimestamp(timestamp)).toBe('1 hour ago');
      });
  
      it('should return "3 hours ago" if the timestamp is 3 hours ago', () => {
        const now = new Date();
        const timestamp = new Date(now.getTime() - 10800000).toISOString(); // 3 hours ago
        expect(messageFormatter.formatTimestamp(timestamp)).toBe('3 hours ago');
      });
  
      it('should return "1 day ago" if the timestamp is exactly one day ago', () => {
        const now = new Date();
        const timestamp = new Date(now.getTime() - 86400000).toISOString(); // 1 day ago
        expect(messageFormatter.formatTimestamp(timestamp)).toBe('1 day ago');
      });
  
      it('should return "3 days ago" if the timestamp is 3 days ago', () => {
        const now = new Date();
        const timestamp = new Date(now.getTime() - 259200000).toISOString(); // 3 days ago
        expect(messageFormatter.formatTimestamp(timestamp)).toBe('3 days ago');
      });
  
      it('should return the date in locale format if the timestamp is more than 7 days ago', () => {
        const now = new Date();
        const timestamp = new Date(now.getTime() - 604800000).toISOString(); // 7 days ago
        const expectedDate = new Date(timestamp).toLocaleDateString();
        expect(messageFormatter.formatTimestamp(timestamp)).toBe(expectedDate);
      });
    });
  });

  const MessageFormatter = require('./MessageFormatter'); // Adjust the path as necessary
  
  describe('MessageFormatter', () => {
    let messageFormatter;
  
    beforeEach(() => {
      messageFormatter = new MessageFormatter();
    });
  
    describe('methodToTest', () => {
      it('should return an empty string for empty input', () => {
        const result = messageFormatter.methodToTest('');
        expect(result).toBe('');
      });
  
      it('should return an empty string for null input', () => {
        const result = messageFormatter.methodToTest(null);
        expect(result).toBe('');
      });
  
      it('should return an empty string for undefined input', () => {
        const result = messageFormatter.methodToTest(undefined);
        expect(result).toBe('');
      });
  
      it('should return an empty string for a valid string input', () => {
        const result = messageFormatter.methodToTest('Hello, World!');
        expect(result).toBe('');
      });
  
      it('should return an empty string for a number input', () => {
        const result = messageFormatter.methodToTest(12345);
        expect(result).toBe('');
      });
  
      it('should return an empty string for an object input', () => {
        const result = messageFormatter.methodToTest({ key: 'value' });
        expect(result).toBe('');
      });
  
      it('should return an empty string for an array input', () => {
        const result = messageFormatter.methodToTest(['array', 'of', 'strings']);
        expect(result).toBe('');
      });
  
      it('should return an empty string for a boolean input', () => {
        const result = messageFormatter.methodToTest(true);
        expect(result).toBe('');
      });
    });
  });

  const MessageFormatter = require('./MessageFormatter'); // Adjust the path as necessary
  
  describe('MessageFormatter', () => {
    let messageFormatter;
  
    beforeEach(() => {
      messageFormatter = new MessageFormatter();
    });
  
    describe('methodToTest', () => {
      it('should return "Just now" for the current time', () => {
        const result = messageFormatter.methodToTest(new Date());
        expect(result).toBe('Just now');
      });
  
      it('should return "Just now" for a date within a few seconds ago', () => {
        const now = new Date();
        const aFewSecondsAgo = new Date(now.getTime() - 5000); // 5 seconds ago
        const result = messageFormatter.methodToTest(aFewSecondsAgo);
        expect(result).toBe('Just now');
      });
  
      it('should return "Just now" for a date within a minute ago', () => {
        const now = new Date();
        const aMinuteAgo = new Date(now.getTime() - 60000); // 1 minute ago
        const result = messageFormatter.methodToTest(aMinuteAgo);
        expect(result).toBe('Just now');
      });
  
      it('should not return "Just now" for a date more than a minute ago', () => {
        const now = new Date();
        const moreThanAMinuteAgo = new Date(now.getTime() - 61000); // 61 seconds ago
        const result = messageFormatter.methodToTest(moreThanAMinuteAgo);
        expect(result).not.toBe('Just now');
      });
  
      it('should handle invalid date input gracefully', () => {
        const result = messageFormatter.methodToTest('invalid date');
        expect(result).not.toBe('Just now');
      });
  
      it('should handle null input gracefully', () => {
        const result = messageFormatter.methodToTest(null);
        expect(result).not.toBe('Just now');
      });
  
      it('should handle undefined input gracefully', () => {
        const result = messageFormatter.methodToTest(undefined);
        expect(result).not.toBe('Just now');
      });
    });
  });

  const MessageFormatter = require('./MessageFormatter');
  
  describe('MessageFormatter', () => {
    let messageFormatter;
  
    beforeEach(() => {
      messageFormatter = new MessageFormatter();
    });
  
    describe('formatTimeAgo', () => {
      it('should return "1 minute ago" for input 1', () => {
        const result = messageFormatter.formatTimeAgo(1);
        expect(result).toBe('1 minute ago');
      });
  
      it('should return "2 minutes ago" for input 2', () => {
        const result = messageFormatter.formatTimeAgo(2);
        expect(result).toBe('2 minutes ago');
      });
  
      it('should return "0 minutes ago" for input 0', () => {
        const result = messageFormatter.formatTimeAgo(0);
        expect(result).toBe('0 minutes ago');
      });
  
      it('should return "59 minutes ago" for input 59', () => {
        const result = messageFormatter.formatTimeAgo(59);
        expect(result).toBe('59 minutes ago');
      });
  
      it('should handle large numbers correctly', () => {
        const result = messageFormatter.formatTimeAgo(1000);
        expect(result).toBe('1000 minutes ago');
      });
    });
  });

  const MessageFormatter = require('./MessageFormatter'); // Adjust the path as necessary
  
  describe('MessageFormatter', () => {
    let messageFormatter;
  
    beforeEach(() => {
      messageFormatter = new MessageFormatter();
    });
  
    describe('formatHoursAgo', () => {
      it('should return "1 hour ago" when diffHours is 1', () => {
        const result = messageFormatter.formatHoursAgo(1);
        expect(result).toBe('1 hour ago');
      });
  
      it('should return "2 hours ago" when diffHours is 2', () => {
        const result = messageFormatter.formatHoursAgo(2);
        expect(result).toBe('2 hours ago');
      });
  
      it('should return "0 hours ago" when diffHours is 0', () => {
        const result = messageFormatter.formatHoursAgo(0);
        expect(result).toBe('0 hours ago');
      });
  
      it('should return "24 hours ago" when diffHours is 24', () => {
        const result = messageFormatter.formatHoursAgo(24);
        expect(result).toBe('24 hours ago');
      });
  
      it('should return "-1 hours ago" when diffHours is -1', () => {
        const result = messageFormatter.formatHoursAgo(-1);
        expect(result).toBe('-1 hours ago');
      });
    });
  });

  const MessageFormatter = require('./MessageFormatter'); // Adjust the path as necessary
  
  describe('MessageFormatter', () => {
    let messageFormatter;
  
    beforeEach(() => {
      messageFormatter = new MessageFormatter();
    });
  
    describe('formatDaysAgo', () => {
      it('should return "1 day ago" for 1 day', () => {
        const result = messageFormatter.formatDaysAgo(1);
        expect(result).toBe('1 day ago');
      });
  
      it('should return "2 days ago" for 2 days', () => {
        const result = messageFormatter.formatDaysAgo(2);
        expect(result).toBe('2 days ago');
      });
  
      it('should return "0 days ago" for 0 days', () => {
        const result = messageFormatter.formatDaysAgo(0);
        expect(result).toBe('0 days ago');
      });
  
      it('should return "100 days ago" for 100 days', () => {
        const result = messageFormatter.formatDaysAgo(100);
        expect(result).toBe('100 days ago');
      });
  
      it('should handle negative numbers gracefully', () => {
        const result = messageFormatter.formatDaysAgo(-5);
        expect(result).toBe('-5 days ago');
      });
    });
  });

  const MessageFormatter = require('./MessageFormatter'); // Adjust the path as necessary
  
  describe('MessageFormatter', () => {
    let messageFormatter;
  
    beforeEach(() => {
      messageFormatter = new MessageFormatter();
    });
  
    describe('truncateMessage', () => {
      it('should return an empty string if message is undefined', () => {
        const result = messageFormatter.truncateMessage(undefined, 10);
        expect(result).toBe('');
      });
  
      it('should return an empty string if message is null', () => {
        const result = messageFormatter.truncateMessage(null, 10);
        expect(result).toBe('');
      });
  
      it('should return the full message if its length is less than or equal to maxLength', () => {
        const message = 'Hello';
        const result = messageFormatter.truncateMessage(message, 10);
        expect(result).toBe(message);
      });
  
      it('should return the full message if its length is exactly maxLength', () => {
        const message = 'HelloWorld';
        const result = messageFormatter.truncateMessage(message, 10);
        expect(result).toBe(message);
      });
  
      it('should truncate the message and append "..." if its length is greater than maxLength', () => {
        const message = 'HelloWorld!';
        const result = messageFormatter.truncateMessage(message, 10);
        expect(result).toBe('HelloW...');
      });
  
      it('should handle maxLength less than 3 correctly', () => {
        const message = 'HelloWorld!';
        const result = messageFormatter.truncateMessage(message, 2);
        expect(result).toBe('...');
      });
  
      it('should handle maxLength of 0 correctly', () => {
        const message = 'HelloWorld!';
        const result = messageFormatter.truncateMessage(message, 0);
        expect(result).toBe('...');
      });
  
      it('should handle an empty message string', () => {
        const message = '';
        const result = messageFormatter.truncateMessage(message, 10);
        expect(result).toBe('');
      });
    });
  });

  const MessageFormatter = require('./MessageFormatter'); // Adjust the path as necessary
  
  describe('MessageFormatter', () => {
    let messageFormatter;
  
    beforeEach(() => {
      messageFormatter = new MessageFormatter();
    });
  
    describe('methodToTest', () => {
      it('should return an empty string for empty input', () => {
        const result = messageFormatter.methodToTest('');
        expect(result).toBe('');
      });
  
      it('should return an empty string for null input', () => {
        const result = messageFormatter.methodToTest(null);
        expect(result).toBe('');
      });
  
      it('should return an empty string for undefined input', () => {
        const result = messageFormatter.methodToTest(undefined);
        expect(result).toBe('');
      });
  
      it('should return an empty string for a valid string input', () => {
        const result = messageFormatter.methodToTest('Hello, World!');
        expect(result).toBe('');
      });
  
      it('should return an empty string for a number input', () => {
        const result = messageFormatter.methodToTest(12345);
        expect(result).toBe('');
      });
  
      it('should return an empty string for an object input', () => {
        const result = messageFormatter.methodToTest({ key: 'value' });
        expect(result).toBe('');
      });
  
      it('should return an empty string for an array input', () => {
        const result = messageFormatter.methodToTest(['array', 'of', 'strings']);
        expect(result).toBe('');
      });
  
      it('should return an empty string for a boolean input', () => {
        const result = messageFormatter.methodToTest(true);
        expect(result).toBe('');
      });
    });
  });

  const MessageFormatter = require('./MessageFormatter'); // Adjust the path as necessary
  
  describe('MessageFormatter', () => {
    let messageFormatter;
  
    beforeEach(() => {
      messageFormatter = new MessageFormatter();
    });
  
    describe('methodToTest', () => {
      it('should return the same message for a simple string', () => {
        const message = 'Hello, World!';
        const result = messageFormatter.methodToTest(message);
        expect(result).toBe(message);
      });
  
      it('should return the same message for an empty string', () => {
        const message = '';
        const result = messageFormatter.methodToTest(message);
        expect(result).toBe(message);
      });
  
      it('should return the same message for a string with special characters', () => {
        const message = '!@#$%^&*()_+';
        const result = messageFormatter.methodToTest(message);
        expect(result).toBe(message);
      });
  
      it('should return the same message for a string with numbers', () => {
        const message = '1234567890';
        const result = messageFormatter.methodToTest(message);
        expect(result).toBe(message);
      });
  
      it('should return the same message for a long string', () => {
        const message = 'a'.repeat(1000);
        const result = messageFormatter.methodToTest(message);
        expect(result).toBe(message);
      });
  
      it('should return the same message for a string with whitespace', () => {
        const message = '   ';
        const result = messageFormatter.methodToTest(message);
        expect(result).toBe(message);
      });
  
      it('should return the same message for a string with newlines', () => {
        const message = 'Hello\nWorld';
        const result = messageFormatter.methodToTest(message);
        expect(result).toBe(message);
      });
    });
  });

  const MessageFormatter = require('./MessageFormatter'); // Adjust the path as necessary
  
  describe('MessageFormatter', () => {
    let messageFormatter;
  
    beforeEach(() => {
      messageFormatter = new MessageFormatter();
    });
  
    describe('extractMentions', () => {
      it('should return an empty array when message is null', () => {
        const result = messageFormatter.extractMentions(null);
        expect(result).toEqual([]);
      });
  
      it('should return an empty array when message is undefined', () => {
        const result = messageFormatter.extractMentions(undefined);
        expect(result).toEqual([]);
      });
  
      it('should return an empty array when message is not a string', () => {
        const result = messageFormatter.extractMentions(123);
        expect(result).toEqual([]);
      });
  
      it('should return an empty array when message is an empty string', () => {
        const result = messageFormatter.extractMentions('');
        expect(result).toEqual([]);
      });
  
      it('should return an empty array when there are no mentions', () => {
        const result = messageFormatter.extractMentions('Hello world');
        expect(result).toEqual([]);
      });
  
      it('should return an array with a single mention', () => {
        const result = messageFormatter.extractMentions('Hello @user');
        expect(result).toEqual(['user']);
      });
  
      it('should return an array with multiple mentions', () => {
        const result = messageFormatter.extractMentions('Hello @user1 and @user2');
        expect(result).toEqual(['user1', 'user2']);
      });
  
      it('should handle mentions with underscores', () => {
        const result = messageFormatter.extractMentions('Hello @user_name');
        expect(result).toEqual(['user_name']);
      });
  
      it('should handle mentions at the start of the message', () => {
        const result = messageFormatter.extractMentions('@user1 hello');
        expect(result).toEqual(['user1']);
      });
  
      it('should handle mentions at the end of the message', () => {
        const result = messageFormatter.extractMentions('Hello @user1');
        expect(result).toEqual(['user1']);
      });
  
      it('should handle consecutive mentions', () => {
        const result = messageFormatter.extractMentions('Hello @user1@user2');
        expect(result).toEqual(['user1', 'user2']);
      });
    });
  });

  const MessageFormatter = require('./MessageFormatter'); // Adjust the path as necessary
  
  describe('MessageFormatter', () => {
    let messageFormatter;
  
    beforeEach(() => {
      messageFormatter = new MessageFormatter();
    });
  
    describe('methodToTest', () => {
      it('should return an empty array for empty input', () => {
        const result = messageFormatter.methodToTest('');
        expect(result).toEqual([]);
      });
  
      it('should return an empty array for null input', () => {
        const result = messageFormatter.methodToTest(null);
        expect(result).toEqual([]);
      });
  
      it('should return an empty array for undefined input', () => {
        const result = messageFormatter.methodToTest(undefined);
        expect(result).toEqual([]);
      });
  
      it('should return an empty array for a valid string input', () => {
        const result = messageFormatter.methodToTest('Hello, World!');
        expect(result).toEqual([]);
      });
  
      it('should return an empty array for a number input', () => {
        const result = messageFormatter.methodToTest(12345);
        expect(result).toEqual([]);
      });
  
      it('should return an empty array for an object input', () => {
        const result = messageFormatter.methodToTest({ key: 'value' });
        expect(result).toEqual([]);
      });
  
      it('should return an empty array for an array input', () => {
        const result = messageFormatter.methodToTest(['item1', 'item2']);
        expect(result).toEqual([]);
      });
    });
  });

  const MessageFormatter = require('./MessageFormatter'); // Adjust the path as necessary
  
  describe('MessageFormatter', () => {
    let formatter;
  
    beforeEach(() => {
      formatter = new MessageFormatter();
    });
  
    describe('highlightMentions', () => {
      it('should return an empty string if message is null', () => {
        expect(formatter.highlightMentions(null)).toBe('');
      });
  
      it('should return an empty string if message is undefined', () => {
        expect(formatter.highlightMentions(undefined)).toBe('');
      });
  
      it('should return an empty string if message is not a string', () => {
        expect(formatter.highlightMentions(123)).toBe('');
        expect(formatter.highlightMentions({})).toBe('');
        expect(formatter.highlightMentions([])).toBe('');
      });
  
      it('should return the same string if there are no mentions', () => {
        const message = 'Hello world!';
        expect(formatter.highlightMentions(message)).toBe(message);
      });
  
      it('should highlight a single mention', () => {
        const message = 'Hello @user!';
        const expected = 'Hello <span class="mention">@user</span>!';
        expect(formatter.highlightMentions(message)).toBe(expected);
      });
  
      it('should highlight multiple mentions', () => {
        const message = '@user1 and @user2 are here.';
        const expected = '<span class="mention">@user1</span> and <span class="mention">@user2</span> are here.';
        expect(formatter.highlightMentions(message)).toBe(expected);
      });
  
      it('should handle mentions at the start and end of the message', () => {
        const message = '@user1 is here and so is @user2';
        const expected = '<span class="mention">@user1</span> is here and so is <span class="mention">@user2</span>';
        expect(formatter.highlightMentions(message)).toBe(expected);
      });
  
      it('should not highlight invalid mentions', () => {
        const message = 'Hello @user!@';
        const expected = 'Hello <span class="mention">@user</span>!';
        expect(formatter.highlightMentions(message)).toBe(expected);
      });
  
      it('should handle messages with special characters', () => {
        const message = 'Hello @user! How are you?';
        const expected = 'Hello <span class="mention">@user</span>! How are you?';
        expect(formatter.highlightMentions(message)).toBe(expected);
      });
    });
  });

  const MessageFormatter = require('./MessageFormatter'); // Adjust the path as necessary
  
  describe('MessageFormatter', () => {
    let messageFormatter;
  
    beforeEach(() => {
      messageFormatter = new MessageFormatter();
    });
  
    describe('methodToTest', () => {
      it('should return an empty string for empty input', () => {
        const result = messageFormatter.methodToTest('');
        expect(result).toBe('');
      });
  
      it('should return an empty string for null input', () => {
        const result = messageFormatter.methodToTest(null);
        expect(result).toBe('');
      });
  
      it('should return an empty string for undefined input', () => {
        const result = messageFormatter.methodToTest(undefined);
        expect(result).toBe('');
      });
  
      it('should return an empty string for a valid string input', () => {
        const result = messageFormatter.methodToTest('Hello, World!');
        expect(result).toBe('');
      });
  
      it('should return an empty string for a number input', () => {
        const result = messageFormatter.methodToTest(12345);
        expect(result).toBe('');
      });
  
      it('should return an empty string for an object input', () => {
        const result = messageFormatter.methodToTest({ key: 'value' });
        expect(result).toBe('');
      });
  
      it('should return an empty string for an array input', () => {
        const result = messageFormatter.methodToTest(['array', 'of', 'strings']);
        expect(result).toBe('');
      });
    });
  });

  const MessageFormatter = require('./MessageFormatter'); // Adjust the path as necessary
  
  describe('MessageFormatter', () => {
    let messageFormatter;
  
    beforeEach(() => {
      messageFormatter = new MessageFormatter();
    });
  
    describe('extractUrls', () => {
      it('should return an empty array when message is null', () => {
        const result = messageFormatter.extractUrls(null);
        expect(result).toEqual([]);
      });
  
      it('should return an empty array when message is undefined', () => {
        const result = messageFormatter.extractUrls(undefined);
        expect(result).toEqual([]);
      });
  
      it('should return an empty array when message is not a string', () => {
        const result = messageFormatter.extractUrls(12345);
        expect(result).toEqual([]);
      });
  
      it('should return an empty array when message is an empty string', () => {
        const result = messageFormatter.extractUrls('');
        expect(result).toEqual([]);
      });
  
      it('should return an empty array when there are no URLs in the message', () => {
        const result = messageFormatter.extractUrls('This is a test message with no URLs.');
        expect(result).toEqual([]);
      });
  
      it('should return an array with a single URL when there is one URL in the message', () => {
        const result = messageFormatter.extractUrls('Check out this link: https://example.com');
        expect(result).toEqual(['https://example.com']);
      });
  
      it('should return an array with multiple URLs when there are multiple URLs in the message', () => {
        const result = messageFormatter.extractUrls('Visit https://example.com and http://test.com for more info.');
        expect(result).toEqual(['https://example.com', 'http://test.com']);
      });
  
      it('should handle URLs with different protocols', () => {
        const result = messageFormatter.extractUrls('Secure site: https://secure.com, Non-secure: http://nonsecure.com');
        expect(result).toEqual(['https://secure.com', 'http://nonsecure.com']);
      });
  
      it('should return an empty array when URLs are malformed', () => {
        const result = messageFormatter.extractUrls('Visit htp://example.com or www.example.com');
        expect(result).toEqual([]);
      });
    });
  });

  const MessageFormatter = require('./MessageFormatter'); // Adjust the path as necessary
  
  describe('MessageFormatter', () => {
    let messageFormatter;
  
    beforeEach(() => {
      messageFormatter = new MessageFormatter();
    });
  
    describe('methodToTest', () => {
      it('should return an empty array for empty input', () => {
        const result = messageFormatter.methodToTest('');
        expect(result).toEqual([]);
      });
  
      it('should return an empty array for null input', () => {
        const result = messageFormatter.methodToTest(null);
        expect(result).toEqual([]);
      });
  
      it('should return an empty array for undefined input', () => {
        const result = messageFormatter.methodToTest(undefined);
        expect(result).toEqual([]);
      });
  
      it('should return an empty array for a valid string input', () => {
        const result = messageFormatter.methodToTest('Hello, World!');
        expect(result).toEqual([]);
      });
  
      it('should return an empty array for a number input', () => {
        const result = messageFormatter.methodToTest(12345);
        expect(result).toEqual([]);
      });
  
      it('should return an empty array for an object input', () => {
        const result = messageFormatter.methodToTest({ key: 'value' });
        expect(result).toEqual([]);
      });
  
      it('should return an empty array for an array input', () => {
        const result = messageFormatter.methodToTest(['item1', 'item2']);
        expect(result).toEqual([]);
      });
    });
  });

  const MessageFormatter = require('./MessageFormatter'); // Adjust the path as necessary
  
  describe('MessageFormatter', () => {
    let formatter;
  
    beforeEach(() => {
      formatter = new MessageFormatter();
    });
  
    describe('linkifyUrls', () => {
      it('should return an empty string if message is null', () => {
        expect(formatter.linkifyUrls(null)).toBe('');
      });
  
      it('should return an empty string if message is undefined', () => {
        expect(formatter.linkifyUrls(undefined)).toBe('');
      });
  
      it('should return an empty string if message is not a string', () => {
        expect(formatter.linkifyUrls(123)).toBe('');
        expect(formatter.linkifyUrls({})).toBe('');
        expect(formatter.linkifyUrls([])).toBe('');
      });
  
      it('should return the same string if there are no URLs', () => {
        const message = 'This is a test message without URLs.';
        expect(formatter.linkifyUrls(message)).toBe(message);
      });
  
      it('should convert a single URL to a hyperlink', () => {
        const message = 'Check this out: http://example.com';
        const expected = 'Check this out: <a href="http://example.com" target="_blank" rel="noopener noreferrer">http://example.com</a>';
        expect(formatter.linkifyUrls(message)).toBe(expected);
      });
  
      it('should convert multiple URLs to hyperlinks', () => {
        const message = 'Visit http://example.com and https://another.com';
        const expected = 'Visit <a href="http://example.com" target="_blank" rel="noopener noreferrer">http://example.com</a> and <a href="https://another.com" target="_blank" rel="noopener noreferrer">https://another.com</a>';
        expect(formatter.linkifyUrls(message)).toBe(expected);
      });
  
      it('should handle URLs with query parameters', () => {
        const message = 'Check this: https://example.com?param=value';
        const expected = 'Check this: <a href="https://example.com?param=value" target="_blank" rel="noopener noreferrer">https://example.com?param=value</a>';
        expect(formatter.linkifyUrls(message)).toBe(expected);
      });
  
      it('should handle URLs with trailing slashes', () => {
        const message = 'Visit https://example.com/';
        const expected = 'Visit <a href="https://example.com/" target="_blank" rel="noopener noreferrer">https://example.com/</a>';
        expect(formatter.linkifyUrls(message)).toBe(expected);
      });
  
      it('should not alter text that looks like a URL but is not', () => {
        const message = 'This is not a URL: example.com';
        expect(formatter.linkifyUrls(message)).toBe(message);
      });
    });
  });

  const MessageFormatter = require('./MessageFormatter'); // Adjust the path as necessary
  
  describe('MessageFormatter', () => {
    let messageFormatter;
  
    beforeEach(() => {
      messageFormatter = new MessageFormatter();
    });
  
    describe('methodToTest', () => {
      it('should return an empty string for empty input', () => {
        const result = messageFormatter.methodToTest('');
        expect(result).toBe('');
      });
  
      it('should return an empty string for null input', () => {
        const result = messageFormatter.methodToTest(null);
        expect(result).toBe('');
      });
  
      it('should return an empty string for undefined input', () => {
        const result = messageFormatter.methodToTest(undefined);
        expect(result).toBe('');
      });
  
      it('should return an empty string for a valid string input', () => {
        const result = messageFormatter.methodToTest('Hello, World!');
        expect(result).toBe('');
      });
  
      it('should return an empty string for a number input', () => {
        const result = messageFormatter.methodToTest(12345);
        expect(result).toBe('');
      });
  
      it('should return an empty string for an object input', () => {
        const result = messageFormatter.methodToTest({ key: 'value' });
        expect(result).toBe('');
      });
  
      it('should return an empty string for an array input', () => {
        const result = messageFormatter.methodToTest(['item1', 'item2']);
        expect(result).toBe('');
      });
    });
  });

  const MessageFormatter = require('./MessageFormatter');
  
  describe('MessageFormatter', () => {
    describe('sanitizeMessage', () => {
      it('should return an empty string if message is null', () => {
        expect(MessageFormatter.sanitizeMessage(null)).toBe('');
      });
  
      it('should return an empty string if message is undefined', () => {
        expect(MessageFormatter.sanitizeMessage(undefined)).toBe('');
      });
  
      it('should return an empty string if message is not a string', () => {
        expect(MessageFormatter.sanitizeMessage(123)).toBe('');
        expect(MessageFormatter.sanitizeMessage({})).toBe('');
        expect(MessageFormatter.sanitizeMessage([])).toBe('');
      });
  
      it('should escape & to &amp;', () => {
        expect(MessageFormatter.sanitizeMessage('Hello & World')).toBe('Hello &amp; World');
      });
  
      it('should escape < to &lt;', () => {
        expect(MessageFormatter.sanitizeMessage('Hello < World')).toBe('Hello &lt; World');
      });
  
      it('should escape > to &gt;', () => {
        expect(MessageFormatter.sanitizeMessage('Hello > World')).toBe('Hello &gt; World');
      });
  
      it('should escape " to &quot;', () => {
        expect(MessageFormatter.sanitizeMessage('Hello "World"')).toBe('Hello &quot;World&quot;');
      });
  
      it('should escape \' to &#x27;', () => {
        expect(MessageFormatter.sanitizeMessage("Hello 'World'")).toBe('Hello &#x27;World&#x27;');
      });
  
      it('should escape multiple special characters', () => {
        expect(MessageFormatter.sanitizeMessage('Hello & < > " \' World')).toBe('Hello &amp; &lt; &gt; &quot; &#x27; World');
      });
  
      it('should return the same string if there are no special characters', () => {
        expect(MessageFormatter.sanitizeMessage('Hello World')).toBe('Hello World');
      });
    });
  });

  const MessageFormatter = require('./MessageFormatter'); // Adjust the path as necessary
  
  describe('MessageFormatter', () => {
    let messageFormatter;
  
    beforeEach(() => {
      messageFormatter = new MessageFormatter();
    });
  
    describe('methodToTest', () => {
      it('should return an empty string for an empty input', () => {
        const result = messageFormatter.methodToTest('');
        expect(result).toBe('');
      });
  
      it('should return an empty string for a null input', () => {
        const result = messageFormatter.methodToTest(null);
        expect(result).toBe('');
      });
  
      it('should return an empty string for an undefined input', () => {
        const result = messageFormatter.methodToTest(undefined);
        expect(result).toBe('');
      });
  
      it('should return an empty string for a non-empty string input', () => {
        const result = messageFormatter.methodToTest('Hello, World!');
        expect(result).toBe('');
      });
  
      it('should return an empty string for a number input', () => {
        const result = messageFormatter.methodToTest(123);
        expect(result).toBe('');
      });
  
      it('should return an empty string for an object input', () => {
        const result = messageFormatter.methodToTest({ key: 'value' });
        expect(result).toBe('');
      });
  
      it('should return an empty string for an array input', () => {
        const result = messageFormatter.methodToTest(['item1', 'item2']);
        expect(result).toBe('');
      });
    });
  });

  const MessageFormatter = require('./MessageFormatter'); // Adjust the path as necessary
  
  describe('MessageFormatter', () => {
    let messageFormatter;
  
    beforeEach(() => {
      messageFormatter = new MessageFormatter();
    });
  
    describe('Method to test', () => {
      it('should return null if messageData is null', () => {
        const result = messageFormatter.methodToTest(null);
        expect(result).toBeNull();
      });
  
      it('should return null if messageData.content is undefined', () => {
        const result = messageFormatter.methodToTest({});
        expect(result).toBeNull();
      });
  
      it('should return formatted message object for valid input', () => {
        const messageData = {
          content: 'Hello @user, check this out: http://example.com',
          timestamp: 1633072800000,
          sender: 'John Doe'
        };
        const result = messageFormatter.methodToTest(messageData);
  
        expect(result).toEqual({
          content: expect.any(String),
          originalContent: 'Hello @user, check this out: http://example.com',
          timestamp: expect.any(String),
          sender: 'John Doe',
          mentions: ['@user'],
          urls: ['http://example.com']
        });
      });
  
      it('should handle messages with no mentions or URLs', () => {
        const messageData = {
          content: 'Just a simple message',
          timestamp: 1633072800000,
          sender: 'Jane Doe'
        };
        const result = messageFormatter.methodToTest(messageData);
  
        expect(result).toEqual({
          content: 'Just a simple message',
          originalContent: 'Just a simple message',
          timestamp: expect.any(String),
          sender: 'Jane Doe',
          mentions: [],
          urls: []
        });
      });
  
      it('should default sender to "Unknown" if not provided', () => {
        const messageData = {
          content: 'Message without sender',
          timestamp: 1633072800000
        };
        const result = messageFormatter.methodToTest(messageData);
  
        expect(result.sender).toBe('Unknown');
      });
  
      it('should correctly extract multiple mentions and URLs', () => {
        const messageData = {
          content: 'Hey @user1 and @user2, visit http://example.com and https://another.com',
          timestamp: 1633072800000,
          sender: 'Alice'
        };
        const result = messageFormatter.methodToTest(messageData);
  
        expect(result.mentions).toEqual(['@user1', '@user2']);
        expect(result.urls).toEqual(['http://example.com', 'https://another.com']);
      });
    });
  });

  const MessageFormatter = require('./MessageFormatter');
  
  describe('MessageFormatter', () => {
    let messageFormatter;
  
    beforeEach(() => {
      messageFormatter = new MessageFormatter();
    });
  
    describe('methodToTest', () => {
      it('should return null for empty input', () => {
        const result = messageFormatter.methodToTest('');
        expect(result).toBeNull();
      });
  
      it('should return null for null input', () => {
        const result = messageFormatter.methodToTest(null);
        expect(result).toBeNull();
      });
  
      it('should return null for undefined input', () => {
        const result = messageFormatter.methodToTest(undefined);
        expect(result).toBeNull();
      });
  
      it('should return null for valid string input', () => {
        const result = messageFormatter.methodToTest('Hello, World!');
        expect(result).toBeNull();
      });
  
      it('should return null for numeric input', () => {
        const result = messageFormatter.methodToTest(12345);
        expect(result).toBeNull();
      });
  
      it('should return null for object input', () => {
        const result = messageFormatter.methodToTest({ key: 'value' });
        expect(result).toBeNull();
      });
  
      it('should return null for array input', () => {
        const result = messageFormatter.methodToTest(['array', 'of', 'values']);
        expect(result).toBeNull();
      });
    });
  });

  const MessageFormatter = require('./MessageFormatter'); // Adjust the path as necessary
  
  describe('MessageFormatter', () => {
    let messageFormatter;
  
    beforeEach(() => {
      messageFormatter = new MessageFormatter();
    });
  
    describe('countWords', () => {
      it('should return 0 for null input', () => {
        expect(messageFormatter.countWords(null)).toBe(0);
      });
  
      it('should return 0 for undefined input', () => {
        expect(messageFormatter.countWords(undefined)).toBe(0);
      });
  
      it('should return 0 for non-string input', () => {
        expect(messageFormatter.countWords(123)).toBe(0);
        expect(messageFormatter.countWords({})).toBe(0);
        expect(messageFormatter.countWords([])).toBe(0);
      });
  
      it('should return 0 for an empty string', () => {
        expect(messageFormatter.countWords('')).toBe(0);
      });
  
      it('should return 0 for a string with only spaces', () => {
        expect(messageFormatter.countWords('     ')).toBe(0);
      });
  
      it('should return the correct word count for a single word', () => {
        expect(messageFormatter.countWords('hello')).toBe(1);
      });
  
      it('should return the correct word count for multiple words', () => {
        expect(messageFormatter.countWords('hello world')).toBe(2);
        expect(messageFormatter.countWords('  hello   world  ')).toBe(2);
      });
  
      it('should handle strings with multiple spaces between words', () => {
        expect(messageFormatter.countWords('hello    world')).toBe(2);
      });
  
      it('should handle strings with leading and trailing spaces', () => {
        expect(messageFormatter.countWords('   hello world   ')).toBe(2);
      });
  
      it('should handle strings with special characters', () => {
        expect(messageFormatter.countWords('hello, world!')).toBe(2);
      });
    });
  });

  const MessageFormatter = require('./MessageFormatter'); // Adjust the path as necessary
  
  describe('MessageFormatter', () => {
    let messageFormatter;
  
    beforeEach(() => {
      messageFormatter = new MessageFormatter();
    });
  
    describe('methodToTest', () => {
      it('should return 0 for a typical input', () => {
        const result = messageFormatter.methodToTest('typical input');
        expect(result).toBe(0);
      });
  
      it('should return 0 for an empty string', () => {
        const result = messageFormatter.methodToTest('');
        expect(result).toBe(0);
      });
  
      it('should return 0 for a null input', () => {
        const result = messageFormatter.methodToTest(null);
        expect(result).toBe(0);
      });
  
      it('should return 0 for an undefined input', () => {
        const result = messageFormatter.methodToTest(undefined);
        expect(result).toBe(0);
      });
  
      it('should return 0 for a number input', () => {
        const result = messageFormatter.methodToTest(123);
        expect(result).toBe(0);
      });
  
      it('should return 0 for a boolean input', () => {
        const result = messageFormatter.methodToTest(true);
        expect(result).toBe(0);
      });
  
      it('should return 0 for an object input', () => {
        const result = messageFormatter.methodToTest({ key: 'value' });
        expect(result).toBe(0);
      });
  
      it('should return 0 for an array input', () => {
        const result = messageFormatter.methodToTest(['array', 'of', 'values']);
        expect(result).toBe(0);
      });
    });
  });

  const MessageFormatter = require('./MessageFormatter');
  
  describe('MessageFormatter', () => {
    let messageFormatter;
  
    beforeEach(() => {
      messageFormatter = new MessageFormatter();
    });
  
    describe('isEmpty', () => {
      it('should return true for null input', () => {
        expect(messageFormatter.isEmpty(null)).toBe(true);
      });
  
      it('should return true for undefined input', () => {
        expect(messageFormatter.isEmpty(undefined)).toBe(true);
      });
  
      it('should return true for empty string', () => {
        expect(messageFormatter.isEmpty('')).toBe(true);
      });
  
      it('should return true for string with only spaces', () => {
        expect(messageFormatter.isEmpty('   ')).toBe(true);
      });
  
      it('should return false for non-empty string', () => {
        expect(messageFormatter.isEmpty('Hello')).toBe(false);
      });
  
      it('should return false for string with spaces and characters', () => {
        expect(messageFormatter.isEmpty('  Hello  ')).toBe(false);
      });
    });
  });

  const MessageFormatter = require('./MessageFormatter');
  
  describe('MessageFormatter', () => {
    let messageFormatter;
  
    beforeEach(() => {
      messageFormatter = new MessageFormatter();
    });
  
    describe('formatMessage', () => {
      it('should format a simple message correctly', () => {
        const input = 'Hello, World!';
        const expectedOutput = 'Formatted: Hello, World!';
        expect(messageFormatter.formatMessage(input)).toBe(expectedOutput);
      });
  
      it('should handle an empty string', () => {
        const input = '';
        const expectedOutput = 'Formatted: ';
        expect(messageFormatter.formatMessage(input)).toBe(expectedOutput);
      });
  
      it('should handle a string with special characters', () => {
        const input = '!@#$%^&*()';
        const expectedOutput = 'Formatted: !@#$%^&*()';
        expect(messageFormatter.formatMessage(input)).toBe(expectedOutput);
      });
  
      it('should handle a string with numbers', () => {
        const input = '1234567890';
        const expectedOutput = 'Formatted: 1234567890';
        expect(messageFormatter.formatMessage(input)).toBe(expectedOutput);
      });
  
      it('should handle a very long string', () => {
        const input = 'a'.repeat(1000);
        const expectedOutput = 'Formatted: ' + 'a'.repeat(1000);
        expect(messageFormatter.formatMessage(input)).toBe(expectedOutput);
      });
  
      it('should handle null input gracefully', () => {
        const input = null;
        const expectedOutput = 'Formatted: null';
        expect(messageFormatter.formatMessage(input)).toBe(expectedOutput);
      });
  
      it('should handle undefined input gracefully', () => {
        const input = undefined;
        const expectedOutput = 'Formatted: undefined';
        expect(messageFormatter.formatMessage(input)).toBe(expectedOutput);
      });
    });
  });

});
