/**
 * Message Formatter
 * Formats and processes chat messages for display
 */

class MessageFormatter {
  /**
   * Format a timestamp to a human-readable string
   * @param {Date|string|number} timestamp - The timestamp to format
   * @returns {string} Formatted timestamp string
   */
  static formatTimestamp(timestamp) {
    if (!timestamp) {
      return '';
    }

    const date = new Date(timestamp);
    if (isNaN(date.getTime())) {
      return '';
    }

    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) {
      return 'Just now';
    } else if (diffMins < 60) {
      return `${diffMins} minute${diffMins > 1 ? 's' : ''} ago`;
    } else if (diffHours < 24) {
      return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
    } else if (diffDays < 7) {
      return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`;
    } else {
      return date.toLocaleDateString();
    }
  }

  /**
   * Truncate a message to a specified length
   * @param {string} message - The message to truncate
   * @param {number} maxLength - Maximum length (default: 100)
   * @returns {string} Truncated message
   */
  static truncateMessage(message, maxLength = 100) {
    if (!message) {
      return '';
    }

    if (message.length <= maxLength) {
      return message;
    }

    return message.substring(0, maxLength - 3) + '...';
  }

  /**
   * Extract mentions from a message
   * @param {string} message - The message to parse
   * @returns {string[]} Array of mentioned usernames
   */
  static extractMentions(message) {
    if (!message || typeof message !== 'string') {
      return [];
    }

    const mentionPattern = /@(\w+)/g;
    const mentions = [];
    let match;

    while ((match = mentionPattern.exec(message)) !== null) {
      mentions.push(match[1]);
    }

    return mentions;
  }

  /**
   * Highlight mentions in a message
   * @param {string} message - The message to process
   * @returns {string} Message with highlighted mentions
   */
  static highlightMentions(message) {
    if (!message || typeof message !== 'string') {
      return '';
    }

    return message.replace(/@(\w+)/g, '<span class="mention">@$1</span>');
  }

  /**
   * Extract URLs from a message
   * @param {string} message - The message to parse
   * @returns {string[]} Array of URLs found in the message
   */
  static extractUrls(message) {
    if (!message || typeof message !== 'string') {
      return [];
    }

    const urlPattern = /(https?:\/\/[^\s]+)/g;
    return message.match(urlPattern) || [];
  }

  /**
   * Convert URLs in a message to clickable links
   * @param {string} message - The message to process
   * @returns {string} Message with clickable links
   */
  static linkifyUrls(message) {
    if (!message || typeof message !== 'string') {
      return '';
    }

    return message.replace(
      /(https?:\/\/[^\s]+)/g,
      '<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>'
    );
  }

  /**
   * Sanitize a message to prevent XSS attacks
   * @param {string} message - The message to sanitize
   * @returns {string} Sanitized message
   */
  static sanitizeMessage(message) {
    if (!message || typeof message !== 'string') {
      return '';
    }

    return message
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#x27;')
      .replace(/\//g, '&#x2F;');
  }

  /**
   * Format a complete message with all formatting applied
   * @param {Object} messageData - Message data object
   * @param {string} messageData.content - Message content
   * @param {Date|string|number} messageData.timestamp - Message timestamp
   * @param {string} messageData.sender - Sender username
   * @returns {Object} Formatted message object
   */
  static formatMessage(messageData) {
    if (!messageData || !messageData.content) {
      return null;
    }

    const sanitized = this.sanitizeMessage(messageData.content);
    const withLinks = this.linkifyUrls(sanitized);
    const withMentions = this.highlightMentions(withLinks);

    return {
      content: withMentions,
      originalContent: messageData.content,
      timestamp: this.formatTimestamp(messageData.timestamp),
      sender: messageData.sender || 'Unknown',
      mentions: this.extractMentions(messageData.content),
      urls: this.extractUrls(messageData.content)
    };
  }

  /**
   * Count words in a message
   * @param {string} message - The message to analyze
   * @returns {number} Word count
   */
  static countWords(message) {
    if (!message || typeof message !== 'string') {
      return 0;
    }

    return message.trim().split(/\s+/).filter(word => word.length > 0).length;
  }

  /**
   * Check if a message is empty or whitespace only
   * @param {string} message - The message to check
   * @returns {boolean} True if message is empty
   */
  static isEmpty(message) {
    return !message || message.trim().length === 0;
  }
}

// Export for Node.js environments
if (typeof module !== 'undefined' && module.exports) {
  module.exports = MessageFormatter;
}
// test bot update
