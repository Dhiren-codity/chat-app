package services

import (
	"errors"
	"regexp"
	"strings"
	"time"
	"unicode/utf8"
)

// Message represents a chat message
type Message struct {
	ID        int64     `json:"id"`
	Content   string    `json:"content"`
	SenderID  int64     `json:"sender_id"`
	RoomID    int64     `json:"room_id"`
	Timestamp time.Time `json:"timestamp"`
}

// MessageValidator validates chat messages
type MessageValidator struct {
	MaxLength     int
	MinLength     int
	AllowedChars  *regexp.Regexp
	BannedWords   []string
	MaxMentions   int
	MaxURLs       int
}

// NewMessageValidator creates a new message validator with default settings
func NewMessageValidator() *MessageValidator {
	return &MessageValidator{
		MaxLength:   5000,
		MinLength:   1,
		AllowedChars: regexp.MustCompile(`^[\p{L}\p{N}\p{P}\p{Z}\p{S}\n\r\t]+$`),
		BannedWords: []string{},
		MaxMentions: 10,
		MaxURLs:     5,
	}
}

// ValidateContent checks if message content is valid
func (mv *MessageValidator) ValidateContent(content string) error {
	// Check if content is empty
	trimmed := strings.TrimSpace(content)
	if len(trimmed) == 0 {
		return errors.New("message content cannot be empty")
	}

	// Check minimum length
	if utf8.RuneCountInString(trimmed) < mv.MinLength {
		return errors.New("message content is too short")
	}

	// Check maximum length
	if utf8.RuneCountInString(content) > mv.MaxLength {
		return errors.New("message content exceeds maximum length")
	}

	// Check for banned words
	for _, word := range mv.BannedWords {
		if strings.Contains(strings.ToLower(content), strings.ToLower(word)) {
			return errors.New("message contains banned words")
		}
	}

	return nil
}

// ValidateMessage validates a complete message object
func (mv *MessageValidator) ValidateMessage(msg *Message) error {
	if msg == nil {
		return errors.New("message cannot be nil")
	}

	// Validate content
	if err := mv.ValidateContent(msg.Content); err != nil {
		return err
	}

	// Validate sender ID
	if msg.SenderID <= 0 {
		return errors.New("invalid sender ID")
	}

	// Validate room ID
	if msg.RoomID <= 0 {
		return errors.New("invalid room ID")
	}

	// Validate timestamp
	if msg.Timestamp.IsZero() {
		return errors.New("message timestamp is required")
	}

	// Check if timestamp is not in the future
	if msg.Timestamp.After(time.Now()) {
		return errors.New("message timestamp cannot be in the future")
	}

	return nil
}

// ExtractMentions extracts @username mentions from message content
func (mv *MessageValidator) ExtractMentions(content string) ([]string, error) {
	mentionPattern := regexp.MustCompile(`@(\w+)`)
	matches := mentionPattern.FindAllStringSubmatch(content, -1)

	mentions := make([]string, 0)
	for _, match := range matches {
		if len(match) > 1 {
			mentions = append(mentions, match[1])
		}
	}

	// Check if too many mentions
	if len(mentions) > mv.MaxMentions {
		return nil, errors.New("too many mentions in message")
	}

	return mentions, nil
}

// ExtractURLs extracts URLs from message content
func (mv *MessageValidator) ExtractURLs(content string) ([]string, error) {
	urlPattern := regexp.MustCompile(`https?://[^\s]+`)
	urls := urlPattern.FindAllString(content, -1)

	// Check if too many URLs
	if len(urls) > mv.MaxURLs {
		return nil, errors.New("too many URLs in message")
	}

	return urls, nil
}

// SanitizeContent removes or replaces potentially harmful content
func (mv *MessageValidator) SanitizeContent(content string) string {
	// Remove null bytes
	sanitized := strings.ReplaceAll(content, "\x00", "")

	// Trim excessive whitespace
	sanitized = strings.TrimSpace(sanitized)

	// Replace multiple newlines with maximum of 2
	multiNewline := regexp.MustCompile(`\n{3,}`)
	sanitized = multiNewline.ReplaceAllString(sanitized, "\n\n")

	return sanitized
}

// CheckSpam performs basic spam detection
func (mv *MessageValidator) CheckSpam(content string) (bool, error) {
	// Check for excessive repetition
	words := strings.Fields(content)
	if len(words) > 0 {
		wordCount := make(map[string]int)
		for _, word := range words {
			wordCount[strings.ToLower(word)]++
		}

		// If any word appears more than 10 times, consider it spam
		for _, count := range wordCount {
			if count > 10 {
				return true, errors.New("message appears to be spam (excessive repetition)")
			}
		}
	}

	// Check for excessive caps
	upperCount := 0
	for _, char := range content {
		if char >= 'A' && char <= 'Z' {
			upperCount++
		}
	}

	totalLetters := utf8.RuneCountInString(content)
	if totalLetters > 10 && float64(upperCount)/float64(totalLetters) > 0.7 {
		return true, errors.New("message appears to be spam (excessive caps)")
	}

	return false, nil
}

// ValidateAndSanitize performs both validation and sanitization
func (mv *MessageValidator) ValidateAndSanitize(msg *Message) (*Message, error) {
	// Sanitize content first
	msg.Content = mv.SanitizeContent(msg.Content)

	// Then validate
	if err := mv.ValidateMessage(msg); err != nil {
		return nil, err
	}

	// Check for spam
	isSpam, err := mv.CheckSpam(msg.Content)
	if isSpam {
		return nil, err
	}

	return msg, nil
}

// SetBannedWords sets the list of banned words
func (mv *MessageValidator) SetBannedWords(words []string) {
	mv.BannedWords = words
}

// AddBannedWord adds a word to the banned list
func (mv *MessageValidator) AddBannedWord(word string) {
	mv.BannedWords = append(mv.BannedWords, word)
}

// CountWords counts the number of words in content
func (mv *MessageValidator) CountWords(content string) int {
	words := strings.Fields(content)
	return len(words)
}

// IsEmpty checks if message content is empty or whitespace only
func (mv *MessageValidator) IsEmpty(content string) bool {
	return len(strings.TrimSpace(content)) == 0
}
