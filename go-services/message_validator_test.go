package main

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

package services

import (
	"regexp"
	"testing"

	"github.com/stretchr/testify/assert"
)

type MessageValidator struct {
	MaxLength    int
	MinLength    int
	AllowedChars *regexp.Regexp
	BannedWords  []string
	MaxMentions  int
	MaxURLs      int
}

func NewMessageValidator() *MessageValidator {
	return &MessageValidator{
		MaxLength:    5000,
		MinLength:    1,
		AllowedChars: regexp.MustCompile(`^[\p{L}\p{N}\p{P}\p{Z}\p{S}\n\r\t]+$`),
		BannedWords:  []string{},
		MaxMentions:  10,
		MaxURLs:      5,
	}
}

func TestNewMessageValidator(t *testing.T) {
	tests := []struct {
		name     string
		expected *MessageValidator
	}{
		{
			name: "default configuration",
			expected: &MessageValidator{
				MaxLength:    5000,
				MinLength:    1,
				AllowedChars: regexp.MustCompile(`^[\p{L}\p{N}\p{P}\p{Z}\p{S}\n\r\t]+$`),
				BannedWords:  []string{},
				MaxMentions:  10,
				MaxURLs:      5,
			},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := NewMessageValidator()
			assert.Equal(t, tt.expected.MaxLength, result.MaxLength)
			assert.Equal(t, tt.expected.MinLength, result.MinLength)
			assert.Equal(t, tt.expected.AllowedChars.String(), result.AllowedChars.String())
			assert.Equal(t, tt.expected.BannedWords, result.BannedWords)
			assert.Equal(t, tt.expected.MaxMentions, result.MaxMentions)
			assert.Equal(t, tt.expected.MaxURLs, result.MaxURLs)
		})
	}
}

package services

import (
	"errors"
	"strings"
	"testing"
	"unicode/utf8"

	"github.com/stretchr/testify/assert"
)

type MessageValidator struct {
	MinLength   int
	MaxLength   int
	BannedWords []string
}

func ValidateContent(content string, mv MessageValidator) error {
	trimmed := strings.TrimSpace(content)
	if len(trimmed) == 0 {
		return errors.New("message content cannot be empty")
	}

	if utf8.RuneCountInString(trimmed) < mv.MinLength {
		return errors.New("message content is too short")
	}

	if utf8.RuneCountInString(content) > mv.MaxLength {
		return errors.New("message content exceeds maximum length")
	}

	for _, word := range mv.BannedWords {
		if strings.Contains(strings.ToLower(content), strings.ToLower(word)) {
			return errors.New("message contains banned words")
		}
	}

	return nil
}

func TestValidateContent(t *testing.T) {
	mv := MessageValidator{
		MinLength:   5,
		MaxLength:   100,
		BannedWords: []string{"banned", "prohibited"},
	}

	tests := []struct {
		name     string
		content  string
		mv       MessageValidator
		wantErr  bool
		errMsg   string
	}{
		{"valid content", "This is a valid message", mv, false, ""},
		{"empty content", "   ", mv, true, "message content cannot be empty"},
		{"too short content", "Hi", mv, true, "message content is too short"},
		{"exceeds max length", strings.Repeat("a", 101), mv, true, "message content exceeds maximum length"},
		{"contains banned word", "This message is banned", mv, true, "message contains banned words"},
		{"exact min length", "Hello", mv, false, ""},
		{"exact max length", strings.Repeat("a", 100), mv, false, ""},
		{"content with spaces", "   Valid content   ", mv, false, ""},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			err := ValidateContent(tt.content, tt.mv)
			if tt.wantErr {
				assert.Error(t, err)
				assert.Equal(t, tt.errMsg, err.Error())
			} else {
				assert.NoError(t, err)
			}
		})
	}
}

# TODO: Test ValidateContent with None content

package services

import (
	"errors"
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
)

type Message struct {
	Content   string
	SenderID  int
	RoomID    int
	Timestamp time.Time
}

type MessageValidator struct{}

func (mv *MessageValidator) ValidateContent(content string) error {
	if content == "" {
		return errors.New("content cannot be empty")
	}
	return nil
}

func ValidateMessage(msg *Message) error {
	mv := &MessageValidator{}
	if msg == nil {
		return errors.New("message cannot be nil")
	}

	if err := mv.ValidateContent(msg.Content); err != nil {
		return err
	}

	if msg.SenderID <= 0 {
		return errors.New("invalid sender ID")
	}

	if msg.RoomID <= 0 {
		return errors.New("invalid room ID")
	}

	if msg.Timestamp.IsZero() {
		return errors.New("message timestamp is required")
	}

	if msg.Timestamp.After(time.Now()) {
		return errors.New("message timestamp cannot be in the future")
	}

	return nil
}

func TestValidateMessage(t *testing.T) {
	tests := []struct {
		name    string
		input   *Message
		wantErr bool
		errMsg  string
	}{
		{
			name: "valid message",
			input: &Message{
				Content:   "Hello",
				SenderID:  1,
				RoomID:    1,
				Timestamp: time.Now(),
			},
			wantErr: false,
		},
		{
			name:    "nil message",
			input:   nil,
			wantErr: true,
			errMsg:  "message cannot be nil",
		},
		{
			name: "empty content",
			input: &Message{
				Content:   "",
				SenderID:  1,
				RoomID:    1,
				Timestamp: time.Now(),
			},
			wantErr: true,
			errMsg:  "content cannot be empty",
		},
		{
			name: "invalid sender ID",
			input: &Message{
				Content:   "Hello",
				SenderID:  0,
				RoomID:    1,
				Timestamp: time.Now(),
			},
			wantErr: true,
			errMsg:  "invalid sender ID",
		},
		{
			name: "invalid room ID",
			input: &Message{
				Content:   "Hello",
				SenderID:  1,
				RoomID:    0,
				Timestamp: time.Now(),
			},
			wantErr: true,
			errMsg:  "invalid room ID",
		},
		{
			name: "zero timestamp",
			input: &Message{
				Content:   "Hello",
				SenderID:  1,
				RoomID:    1,
				Timestamp: time.Time{},
			},
			wantErr: true,
			errMsg:  "message timestamp is required",
		},
		{
			name: "future timestamp",
			input: &Message{
				Content:   "Hello",
				SenderID:  1,
				RoomID:    1,
				Timestamp: time.Now().Add(24 * time.Hour),
			},
			wantErr: true,
			errMsg:  "message timestamp cannot be in the future",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			err := ValidateMessage(tt.input)
			if tt.wantErr {
				assert.Error(t, err)
				assert.EqualError(t, err, tt.errMsg)
			} else {
				assert.NoError(t, err)
			}
		})
	}
}

# TODO: Test ValidateMessage with None msg

package services

import (
	"errors"
	"regexp"
	"testing"

	"github.com/stretchr/testify/assert"
)

type MentionValidator struct {
	MaxMentions int
}

func ExtractMentions(content string, mv MentionValidator) ([]string, error) {
	mentionPattern := regexp.MustCompile(`@(\w+)`)
	matches := mentionPattern.FindAllStringSubmatch(content, -1)

	mentions := make([]string, 0)
	for _, match := range matches {
		if len(match) > 1 {
			mentions = append(mentions, match[1])
		}
	}

	if len(mentions) > mv.MaxMentions {
		return nil, errors.New("too many mentions in message")
	}

	return mentions, nil
}

func TestExtractMentions(t *testing.T) {
	tests := []struct {
		name     string
		content  string
		mv       MentionValidator
		expected []string
		wantErr  bool
	}{
		{"no mentions", "Hello world", MentionValidator{MaxMentions: 5}, []string{}, false},
		{"single mention", "Hello @user", MentionValidator{MaxMentions: 5}, []string{"user"}, false},
		{"multiple mentions", "Hello @user1 and @user2", MentionValidator{MaxMentions: 5}, []string{"user1", "user2"}, false},
		{"exceed max mentions", "@user1 @user2 @user3", MentionValidator{MaxMentions: 2}, nil, true},
		{"empty content", "", MentionValidator{MaxMentions: 5}, []string{}, false},
		{"no valid mentions", "Hello @123", MentionValidator{MaxMentions: 5}, []string{}, false},
		{"exact max mentions", "@user1 @user2", MentionValidator{MaxMentions: 2}, []string{"user1", "user2"}, false},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := ExtractMentions(tt.content, tt.mv)
			if (err != nil) != tt.wantErr {
				t.Errorf("error = %v, wantErr %v", err, tt.wantErr)
				return
			}
			assert.Equal(t, tt.expected, result)
		})
	}
}

# TODO: Test ExtractMentions with None content

package services

import (
	"errors"
	"regexp"
	"testing"

	"github.com/stretchr/testify/assert"
)

func ExtractURLs(content string, maxURLs int) ([]string, error) {
	urlPattern := regexp.MustCompile(`https?://[^\s]+`)
	urls := urlPattern.FindAllString(content, -1)

	if len(urls) > maxURLs {
		return nil, errors.New("too many URLs in message")
	}

	return urls, nil
}

func TestExtractURLs(t *testing.T) {
	tests := []struct {
		name     string
		content  string
		maxURLs  int
		expected []string
		wantErr  bool
	}{
		{
			name:     "valid input with no URLs",
			content:  "This is a test message with no URLs.",
			maxURLs:  5,
			expected: []string{},
			wantErr:  false,
		},
		{
			name:     "valid input with URLs within limit",
			content:  "Check this out: http://example.com and https://example.org",
			maxURLs:  5,
			expected: []string{"http://example.com", "https://example.org"},
			wantErr:  false,
		},
		{
			name:     "valid input with URLs exceeding limit",
			content:  "Visit http://example.com, https://example.org, and http://example.net",
			maxURLs:  2,
			expected: nil,
			wantErr:  true,
		},
		{
			name:     "empty content",
			content:  "",
			maxURLs:  5,
			expected: []string{},
			wantErr:  false,
		},
		{
			name:     "content with only URLs",
			content:  "http://example.com https://example.org",
			maxURLs:  1,
			expected: nil,
			wantErr:  true,
		},
		{
			name:     "content with no URLs and zero maxURLs",
			content:  "No URLs here.",
			maxURLs:  0,
			expected: []string{},
			wantErr:  false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := ExtractURLs(tt.content, tt.maxURLs)
			if tt.wantErr {
				assert.Error(t, err)
			} else {
				assert.NoError(t, err)
			}
			assert.Equal(t, tt.expected, result)
		})
	}
}

# TODO: Test ExtractURLs with None content

package services

import (
	"regexp"
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
)

func SanitizeContent(content string) string {
	// Remove null bytes
	sanitized := strings.ReplaceAll(content, "\x00", "")

	// Trim excessive whitespace
	sanitized = strings.TrimSpace(sanitized)

	// Replace multiple newlines with maximum of 2
	multiNewline := regexp.MustCompile(`\n{3,}`)
	sanitized = multiNewline.ReplaceAllString(sanitized, "\n\n")

	return sanitized
}

func TestSanitizeContent(t *testing.T) {
	tests := []struct {
		name     string
		input    string
		expected string
	}{
		{"no changes", "Hello World", "Hello World"},
		{"remove null bytes", "Hello\x00World", "HelloWorld"},
		{"trim spaces", "   Hello World   ", "Hello World"},
		{"multiple newlines", "Hello\n\n\nWorld", "Hello\n\nWorld"},
		{"mixed changes", "\x00Hello\n\n\n\nWorld   ", "Hello\n\nWorld"},
		{"empty input", "", ""},
		{"only null bytes", "\x00\x00\x00", ""},
		{"only spaces", "     ", ""},
		{"only newlines", "\n\n\n\n\n", "\n\n"},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := SanitizeContent(tt.input)
			assert.Equal(t, tt.expected, result)
		})
	}
}

# TODO: Test SanitizeContent with None content

package services

import (
	"errors"
	"strings"
	"testing"
	"unicode/utf8"

	"github.com/stretchr/testify/assert"
)

func CheckSpam(content string) (bool, error) {
	words := strings.Fields(content)
	if len(words) > 0 {
		wordCount := make(map[string]int)
		for _, word := range words {
			wordCount[strings.ToLower(word)]++
		}

		for _, count := range wordCount {
			if count > 10 {
				return true, errors.New("message appears to be spam (excessive repetition)")
			}
		}
	}

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

func TestCheckSpam(t *testing.T) {
	tests := []struct {
		name     string
		input    string
		expected bool
		wantErr  bool
		errMsg   string
	}{
		{"no spam", "This is a normal message", false, false, ""},
		{"excessive repetition", "spam spam spam spam spam spam spam spam spam spam spam", true, true, "message appears to be spam (excessive repetition)"},
		{"excessive caps", "THIS IS A SPAM MESSAGE", true, true, "message appears to be spam (excessive caps)"},
		{"mixed case, no spam", "This is NOT a spam message", false, false, ""},
		{"empty string", "", false, false, ""},
		{"just below repetition threshold", "word word word word word word word word word word", false, false, ""},
		{"just below caps threshold", "THIS IS a test", false, false, ""},
		{"exactly at caps threshold", "THIS IS A TEST", true, true, "message appears to be spam (excessive caps)"},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := CheckSpam(tt.input)
			if (err != nil) != tt.wantErr {
				t.Errorf("error = %v, wantErr %v", err, tt.wantErr)
				return
			}
			if err != nil && err.Error() != tt.errMsg {
				t.Errorf("error message = %v, want %v", err.Error(), tt.errMsg)
			}
			assert.Equal(t, tt.expected, result)
		})
	}
}

# TODO: Test CheckSpam with None content

package services

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type Message struct {
	Content string
}

type MessageValidator struct{}

func (mv *MessageValidator) SanitizeContent(content string) string {
	// Mock implementation
	return content
}

func (mv *MessageValidator) ValidateMessage(msg *Message) error {
	// Mock implementation
	return nil
}

func (mv *MessageValidator) CheckSpam(content string) (bool, error) {
	// Mock implementation
	return false, nil
}

func ValidateAndSanitize(msg *Message) (*Message, error) {
	mv := &MessageValidator{}
	msg.Content = mv.SanitizeContent(msg.Content)

	if err := mv.ValidateMessage(msg); err != nil {
		return nil, err
	}

	isSpam, err := mv.CheckSpam(msg.Content)
	if isSpam {
		return nil, err
	}

	return msg, nil
}

func TestValidateAndSanitize(t *testing.T) {
	tests := []struct {
		name     string
		input    *Message
		expected *Message
		wantErr  bool
	}{
		{
			name:     "valid input",
			input:    &Message{Content: "Hello, World!"},
			expected: &Message{Content: "Hello, World!"},
			wantErr:  false,
		},
		{
			name:     "nil input",
			input:    nil,
			expected: nil,
			wantErr:  true,
		},
		{
			name:     "empty content",
			input:    &Message{Content: ""},
			expected: &Message{Content: ""},
			wantErr:  false,
		},
		{
			name:     "spam content",
			input:    &Message{Content: "spam"},
			expected: nil,
			wantErr:  true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := ValidateAndSanitize(tt.input)
			if (err != nil) != tt.wantErr {
				t.Errorf("error = %v, wantErr %v", err, tt.wantErr)
				return
			}
			assert.Equal(t, tt.expected, result)
		})
	}
}

# TODO: Test ValidateAndSanitize with None msg

package services

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type MockValidator struct {
	BannedWords []string
}

func (mv *MockValidator) SetBannedWords(words []string) {
	mv.BannedWords = words
}

func TestSetBannedWords(t *testing.T) {
	tests := []struct {
		name     string
		input    []string
		expected []string
	}{
		{"valid input", []string{"badword1", "badword2"}, []string{"badword1", "badword2"}},
		{"nil input", nil, nil},
		{"empty input", []string{}, []string{}},
		{"single word", []string{"badword"}, []string{"badword"}},
		{"duplicate words", []string{"badword", "badword"}, []string{"badword", "badword"}},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			mv := &MockValidator{}
			mv.SetBannedWords(tt.input)
			assert.Equal(t, tt.expected, mv.BannedWords)
		})
	}
}

# TODO: Test SetBannedWords with None words

package services

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

type MockValidator struct {
	BannedWords []string
}

func (mv *MockValidator) AddBannedWord(word string) {
	mv.BannedWords = append(mv.BannedWords, word)
}

func TestAddBannedWord(t *testing.T) {
	tests := []struct {
		name     string
		input    string
		expected []string
	}{
		{"add valid word", "test", []string{"test"}},
		{"add empty word", "", []string{""}},
		{"add duplicate word", "duplicate", []string{"duplicate", "duplicate"}},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			mv := &MockValidator{}
			mv.AddBannedWord(tt.input)
			if tt.name == "add duplicate word" {
				mv.AddBannedWord(tt.input)
			}
			assert.Equal(t, tt.expected, mv.BannedWords)
		})
	}
}

# TODO: Test AddBannedWord with None word

package services

import (
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
)

func CountWords(content string) int {
	words := strings.Fields(content)
	return len(words)
}

func TestCountWords(t *testing.T) {
	tests := []struct {
		name     string
		input    string
		expected int
	}{
		{"valid input with words", "hello world", 2},
		{"valid input with multiple spaces", "  hello   world  ", 2},
		{"empty input", "", 0},
		{"input with only spaces", "   ", 0},
		{"input with newline characters", "\nhello\nworld\n", 2},
		{"input with tabs", "\thello\tworld\t", 2},
		{"input with mixed whitespace", " \t\nhello \t\nworld \t\n", 2},
		{"input with punctuation", "hello, world!", 2},
		{"input with numbers", "123 456", 2},
		{"input with special characters", "@#$ %^&", 2},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := CountWords(tt.input)
			assert.Equal(t, tt.expected, result)
		})
	}
}

# TODO: Test CountWords with None content

package services

import (
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
)

func IsEmpty(content string) bool {
	return len(strings.TrimSpace(content)) == 0
}

func TestIsEmpty(t *testing.T) {
	tests := []struct {
		name     string
		input    string
		expected bool
	}{
		{"empty string", "", true},
		{"spaces only", "   ", true},
		{"non-empty string", "test", false},
		{"string with spaces", "  test  ", false},
		{"newline characters", "\n", true},
		{"tab characters", "\t", true},
		{"mixed whitespace", " \t\n ", true},
		{"non-whitespace characters", " \t\n a", false},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := IsEmpty(tt.input)
			assert.Equal(t, tt.expected, result)
		})
	}
}

# TODO: Test IsEmpty with None content

func TestMessageValidator_ValidateContent(t *testing.T) {
	// Test MessageValidator.ValidateContent

	// Arrange
	instance := &MessageValidator{}
	content := "test_string"

	// Act
	got := instance.ValidateContent(content)

	// Assert
	if got == nil {
		t.Errorf("Expected non-nil result")
	}
}

func TestMessageValidator_ValidateMessage(t *testing.T) {
	// Test MessageValidator.ValidateMessage

	// Arrange
	instance := &MessageValidator{}
	msg := nil // TODO: Provide appropriate test value

	// Act
	got := instance.ValidateMessage(msg)

	// Assert
	if got == nil {
		t.Errorf("Expected non-nil result")
	}
}

func TestMessageValidator_ExtractMentions(t *testing.T) {
	// Test MessageValidator.ExtractMentions

	// Arrange
	instance := &MessageValidator{}
	content := "test_string"

	// Act
	got := instance.ExtractMentions(content)

	// Assert
	if got == nil {
		t.Errorf("Expected non-nil result")
	}
}

func TestMessageValidator_ExtractURLs(t *testing.T) {
	// Test MessageValidator.ExtractURLs

	// Arrange
	instance := &MessageValidator{}
	content := "test_string"

	// Act
	got := instance.ExtractURLs(content)

	// Assert
	if got == nil {
		t.Errorf("Expected non-nil result")
	}
}

func TestMessageValidator_SanitizeContent(t *testing.T) {
	// Test MessageValidator.SanitizeContent

	// Arrange
	instance := &MessageValidator{}
	content := "test_string"

	// Act
	got := instance.SanitizeContent(content)

	// Assert
	if got == nil {
		t.Errorf("Expected non-nil result")
	}
}

func TestMessageValidator_CheckSpam(t *testing.T) {
	// Test MessageValidator.CheckSpam

	// Arrange
	instance := &MessageValidator{}
	content := "test_string"

	// Act
	got := instance.CheckSpam(content)

	// Assert
	if got == nil {
		t.Errorf("Expected non-nil result")
	}
}

func TestMessageValidator_ValidateAndSanitize(t *testing.T) {
	// Test MessageValidator.ValidateAndSanitize

	// Arrange
	instance := &MessageValidator{}
	msg := nil // TODO: Provide appropriate test value

	// Act
	got := instance.ValidateAndSanitize(msg)

	// Assert
	if got == nil {
		t.Errorf("Expected non-nil result")
	}
}

func TestMessageValidator_SetBannedWords(t *testing.T) {
	// Test MessageValidator.SetBannedWords

	// Arrange
	instance := &MessageValidator{}
	words := "test_string"

	// Act
	instance.SetBannedWords(words)

	// Assert
	// Method has no return value
}

func TestMessageValidator_AddBannedWord(t *testing.T) {
	// Test MessageValidator.AddBannedWord

	// Arrange
	instance := &MessageValidator{}
	word := "test_string"

	// Act
	instance.AddBannedWord(word)

	// Assert
	// Method has no return value
}

func TestMessageValidator_CountWords(t *testing.T) {
	// Test MessageValidator.CountWords

	// Arrange
	instance := &MessageValidator{}
	content := "test_string"

	// Act
	got := instance.CountWords(content)

	// Assert
	if got == nil {
		t.Errorf("Expected non-nil result")
	}
}

func TestMessageValidator_IsEmpty(t *testing.T) {
	// Test MessageValidator.IsEmpty

	// Arrange
	instance := &MessageValidator{}
	content := "test_string"

	// Act
	got := instance.IsEmpty(content)

	// Assert
	if got == nil {
		t.Errorf("Expected non-nil result")
	}
}
