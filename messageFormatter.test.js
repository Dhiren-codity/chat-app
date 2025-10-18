const MessageFormatter = require('./messageFormatter');

describe('MessageFormatter', () => {
  describe('formatTimestamp', () => {
    it('should return empty string for null timestamp', () => {
      expect(MessageFormatter.formatTimestamp(null)).toBe('');
    });

    it('should return "Just now" for very recent timestamp', () => {
      const now = new Date();
      expect(MessageFormatter.formatTimestamp(now)).toBe('Just now');
    });

    it('should format minutes ago correctly', () => {
      const fiveMinutesAgo = new Date(Date.now() - 5 * 60 * 1000);
      expect(MessageFormatter.formatTimestamp(fiveMinutesAgo)).toBe('5 minutes ago');
    });
  });

  describe('truncateMessage', () => {
    it('should return empty string for null message', () => {
      expect(MessageFormatter.truncateMessage(null)).toBe('');
    });

    it('should not truncate short messages', () => {
      expect(MessageFormatter.truncateMessage('Hello')).toBe('Hello');
    });

    it('should truncate long messages', () => {
      const longMessage = 'a'.repeat(150);
      const result = MessageFormatter.truncateMessage(longMessage, 100);
      expect(result.length).toBe(100);
      expect(result.endsWith('...')).toBe(true);
    });
  });

  describe('extractMentions', () => {
    it('should return empty array for null message', () => {
      expect(MessageFormatter.extractMentions(null)).toEqual([]);
    });

    it('should extract single mention', () => {
      expect(MessageFormatter.extractMentions('Hello @user')).toEqual(['user']);
    });

    it('should extract multiple mentions', () => {
      expect(MessageFormatter.extractMentions('Hello @user1 and @user2')).toEqual(['user1', 'user2']);
    });

    it('should return empty array for no mentions', () => {
      expect(MessageFormatter.extractMentions('Hello world')).toEqual([]);
    });
  });

  describe('highlightMentions', () => {
    it('should return empty string for null message', () => {
      expect(MessageFormatter.highlightMentions(null)).toBe('');
    });

    it('should highlight mentions with span tags', () => {
      const result = MessageFormatter.highlightMentions('Hello @user');
      expect(result).toContain('<span class="mention">@user</span>');
    });
  });

  describe('extractUrls', () => {
    it('should return empty array for null message', () => {
      expect(MessageFormatter.extractUrls(null)).toEqual([]);
    });

    it('should extract single URL', () => {
      expect(MessageFormatter.extractUrls('Check http://example.com')).toEqual(['http://example.com']);
    });

    it('should extract multiple URLs', () => {
      const urls = MessageFormatter.extractUrls('Visit http://example.com and https://test.com');
      expect(urls).toHaveLength(2);
    });
  });

  describe('sanitizeMessage', () => {
    it('should return empty string for null message', () => {
      expect(MessageFormatter.sanitizeMessage(null)).toBe('');
    });

    it('should escape HTML characters', () => {
      expect(MessageFormatter.sanitizeMessage('<script>alert("xss")</script>'))
        .toBe('&lt;script&gt;alert(&quot;xss&quot;)&lt;&#x2F;script&gt;');
    });
  });

  describe('countWords', () => {
    it('should return 0 for null message', () => {
      expect(MessageFormatter.countWords(null)).toBe(0);
    });

    it('should count words correctly', () => {
      expect(MessageFormatter.countWords('hello world')).toBe(2);
      expect(MessageFormatter.countWords('  hello   world  ')).toBe(2);
    });

    it('should return 0 for empty message', () => {
      expect(MessageFormatter.countWords('')).toBe(0);
    });
  });

  describe('isEmpty', () => {
    it('should return true for null', () => {
      expect(MessageFormatter.isEmpty(null)).toBe(true);
    });

    it('should return true for empty string', () => {
      expect(MessageFormatter.isEmpty('')).toBe(true);
    });

    it('should return true for whitespace only', () => {
      expect(MessageFormatter.isEmpty('   ')).toBe(true);
    });

    it('should return false for non-empty string', () => {
      expect(MessageFormatter.isEmpty('Hello')).toBe(false);
    });
  });
});
