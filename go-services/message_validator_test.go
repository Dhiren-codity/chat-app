package services

import (
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
)

func TestNewMessageValidator(t *testing.T) {
	mv := NewMessageValidator()

	assert.NotNil(t, mv)
	assert.Equal(t, 5000, mv.MaxLength)
	assert.Equal(t, 1, mv.MinLength)
	assert.Equal(t, 10, mv.MaxMentions)
	assert.Equal(t, 5, mv.MaxURLs)
	assert.NotNil(t, mv.AllowedChars)
	assert.NotNil(t, mv.BannedWords)
}

func TestValidateContent(t *testing.T) {
	mv := NewMessageValidator()

	tests := []struct {
		name    string
		content string
		wantErr bool
	}{
		{"valid content", "Hello, world!", false},
		{"empty content", "", true},
		{"whitespace only", "   ", true},
		{"too long", string(make([]byte, 5001)), true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			err := mv.ValidateContent(tt.content)
			if tt.wantErr {
				assert.Error(t, err)
			} else {
				assert.NoError(t, err)
			}
		})
	}
}

func TestValidateMessage(t *testing.T) {
	mv := NewMessageValidator()

	tests := []struct {
		name    string
		msg     *Message
		wantErr bool
	}{
		{
			name: "valid message",
			msg: &Message{
				ID:        1,
				Content:   "Hello",
				SenderID:  1,
				RoomID:    1,
				Timestamp: time.Now(),
			},
			wantErr: false,
		},
		{
			name:    "nil message",
			msg:     nil,
			wantErr: true,
		},
		{
			name: "invalid sender ID",
			msg: &Message{
				Content:   "Hello",
				SenderID:  0,
				RoomID:    1,
				Timestamp: time.Now(),
			},
			wantErr: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			err := mv.ValidateMessage(tt.msg)
			if tt.wantErr {
				assert.Error(t, err)
			} else {
				assert.NoError(t, err)
			}
		})
	}
}

func TestExtractMentions(t *testing.T) {
	mv := NewMessageValidator()

	tests := []struct {
		name     string
		content  string
		expected []string
		wantErr  bool
	}{
		{"no mentions", "Hello world", []string{}, false},
		{"single mention", "Hello @user", []string{"user"}, false},
		{"multiple mentions", "Hello @user1 and @user2", []string{"user1", "user2"}, false},
		{"empty content", "", []string{}, false},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := mv.ExtractMentions(tt.content)
			if tt.wantErr {
				assert.Error(t, err)
			} else {
				assert.NoError(t, err)
				assert.Equal(t, tt.expected, result)
			}
		})
	}
}

func TestExtractURLs(t *testing.T) {
	mv := NewMessageValidator()

	tests := []struct {
		name     string
		content  string
		expected []string
		wantErr  bool
	}{
		{"no URLs", "Hello world", nil, false},
		{"single URL", "Check http://example.com", []string{"http://example.com"}, false},
		{"empty content", "", nil, false},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := mv.ExtractURLs(tt.content)
			if tt.wantErr {
				assert.Error(t, err)
			} else {
				assert.NoError(t, err)
				if tt.expected == nil {
					assert.Nil(t, result)
				} else {
					assert.Equal(t, tt.expected, result)
				}
			}
		})
	}
}

func TestSanitizeContent(t *testing.T) {
	mv := NewMessageValidator()

	tests := []struct {
		name     string
		content  string
		expected string
	}{
		{"no changes", "Hello", "Hello"},
		{"remove null bytes", "Hello\x00World", "HelloWorld"},
		{"trim spaces", "  Hello  ", "Hello"},
		{"multiple newlines", "Hello\n\n\nWorld", "Hello\n\nWorld"},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := mv.SanitizeContent(tt.content)
			assert.Equal(t, tt.expected, result)
		})
	}
}

func TestCheckSpam(t *testing.T) {
	mv := NewMessageValidator()

	tests := []struct {
		name    string
		content string
		isSpam  bool
		wantErr bool
	}{
		{"normal message", "Hello world", false, false},
		{"empty content", "", false, false},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			isSpam, err := mv.CheckSpam(tt.content)
			assert.Equal(t, tt.isSpam, isSpam)
			if tt.wantErr {
				assert.Error(t, err)
			} else {
				assert.NoError(t, err)
			}
		})
	}
}

func TestCountWords(t *testing.T) {
	mv := NewMessageValidator()

	tests := []struct {
		name     string
		content  string
		expected int
	}{
		{"empty string", "", 0},
		{"single word", "hello", 1},
		{"multiple words", "hello world", 2},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := mv.CountWords(tt.content)
			assert.Equal(t, tt.expected, result)
		})
	}
}

func TestIsEmpty(t *testing.T) {
	mv := NewMessageValidator()

	tests := []struct {
		name     string
		content  string
		expected bool
	}{
		{"empty string", "", true},
		{"whitespace only", "   ", true},
		{"non-empty", "Hello", false},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := mv.IsEmpty(tt.content)
			assert.Equal(t, tt.expected, result)
		})
	}
}
