package services

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

func TestNewMessageValidator(t *testing.T) {
	tests := []struct {
		name     string
		expected *MessageValidator
	}{
		{
			name: "default validator",
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


func TestValidateContent(t *testing.T) {
	mv := MessageValidator{
		MinLength:   5,
		MaxLength:   100,
		BannedWords: []string{"banned", "prohibited"},
	}

	tests := []struct {
		name     string
		content  string
		expected error
		wantErr  bool
	}{
		{"valid content", "This is a valid message", nil, false},
		{"empty content", "   ", errors.New("message content cannot be empty"), true},
		{"too short content", "Hi", errors.New("message content is too short"), true},
		{"exceeds max length", strings.Repeat("a", 101), errors.New("message content exceeds maximum length"), true},
		{"contains banned word", "This message is banned", errors.New("message contains banned words"), true},
		{"exact min length", "Hello", nil, false},
		{"exact max length", strings.Repeat("a", 100), nil, false},
		{"content with spaces", "   Valid content   ", nil, false},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			err := ValidateContent(tt.content, mv)
			if tt.wantErr {
				assert.Error(t, err)
				assert.Equal(t, tt.expected.Error(), err.Error())
			} else {
				assert.NoError(t, err)
			}
		})
	}
}


# TODO: Test ValidateContent with None content

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
		{"exceed max mentions", "Hello @user1 @user2 @user3", MentionValidator{MaxMentions: 2}, nil, true},
		{"empty content", "", MentionValidator{MaxMentions: 5}, []string{}, false},
		{"only mentions", "@user1 @user2", MentionValidator{MaxMentions: 5}, []string{"user1", "user2"}, false},
		{"mentions with special characters", "Hello @user_1 and @user-2", MentionValidator{MaxMentions: 5}, []string{"user_1", "user-2"}, false},
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

func TestExtractURLs(t *testing.T) {
	tests := []struct {
		name     string
		content  string
		maxURLs  int
		expected []string
		wantErr  bool
	}{
		{
			name:     "valid input with one URL",
			content:  "Check this out: http://example.com",
			maxURLs:  1,
			expected: []string{"http://example.com"},
			wantErr:  false,
		},
		{
			name:     "valid input with multiple URLs",
			content:  "Visit http://example.com and https://example.org",
			maxURLs:  2,
			expected: []string{"http://example.com", "https://example.org"},
			wantErr:  false,
		},
		{
			name:     "too many URLs",
			content:  "Visit http://example.com and https://example.org",
			maxURLs:  1,
			expected: nil,
			wantErr:  true,
		},
		{
			name:     "no URLs",
			content:  "No URLs here!",
			maxURLs:  1,
			expected: []string{},
			wantErr:  false,
		},
		{
			name:     "empty content",
			content:  "",
			maxURLs:  1,
			expected: []string{},
			wantErr:  false,
		},
		{
			name:     "content with non-URL text",
			content:  "This is a test string with no URLs.",
			maxURLs:  1,
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
		{"complex case", "\x00Hello\n\n\n\n  World\x00", "Hello\n\nWorld"},
		{"empty input", "", ""},
		{"only null bytes", "\x00\x00\x00", ""},
		{"only spaces", "   ", ""},
		{"only newlines", "\n\n\n\n", "\n\n"},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := SanitizeContent(tt.input)
			assert.Equal(t, tt.expected, result)
		})
	}
}


# TODO: Test SanitizeContent with None content

func TestCheckSpam(t *testing.T) {
	tests := []struct {
		name     string
		input    string
		expected bool
		wantErr  bool
		errMsg   string
	}{
		{"no spam", "This is a normal message.", false, false, ""},
		{"excessive repetition", "spam spam spam spam spam spam spam spam spam spam spam", true, true, "message appears to be spam (excessive repetition)"},
		{"excessive caps", "THIS IS A SPAM MESSAGE", true, true, "message appears to be spam (excessive caps)"},
		{"mixed case, not spam", "This is NOT a spam message", false, false, ""},
		{"empty string", "", false, false, ""},
		{"just below repetition threshold", "word word word word word word word word word word", false, false, ""},
		{"just below caps threshold", "THIS IS NOT SPAM", false, false, ""},
		{"exactly at caps threshold", "THIS IS SPAM", false, false, ""},
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

func TestSetBannedWords(t *testing.T) {
	tests := []struct {
		name     string
		input    []string
		expected []string
	}{
		{"valid input", []string{"badword1", "badword2"}, []string{"badword1", "badword2"}},
		{"empty input", []string{}, []string{}},
		{"nil input", nil, nil},
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

func TestAddBannedWord(t *testing.T) {
	tests := []struct {
		name     string
		input    string
		expected []string
	}{
		{"add single word", "test", []string{"test"}},
		{"add another word", "example", []string{"example"}},
		{"add empty string", "", []string{""}},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			mv := &MockValidator{}
			mv.AddBannedWord(tt.input)
			assert.Equal(t, tt.expected, mv.BannedWords)
		})
	}
}


# TODO: Test AddBannedWord with None word

func TestCountWords(t *testing.T) {
	tests := []struct {
		name     string
		input    string
		expected int
	}{
		{"valid input with words", "hello world", 2},
		{"valid input with multiple spaces", "  hello   world  ", 2},
		{"empty input", "", 0},
		{"input with only spaces", "     ", 0},
		{"input with newlines", "\nhello\nworld\n", 2},
		{"input with tabs", "\thello\tworld\t", 2},
		{"input with mixed whitespace", " \t\nhello \n\tworld\t\n ", 2},
		{"single word", "hello", 1},
		{"input with punctuation", "hello, world!", 2},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := CountWords(tt.input)
			assert.Equal(t, tt.expected, result)
		})
	}
}


# TODO: Test CountWords with None content

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

