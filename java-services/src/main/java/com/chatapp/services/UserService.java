package com.chatapp.services;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.regex.Pattern;

/**
 * User Service
 * Manages user operations for the chat application
 */
public class UserService {

    private static final Pattern EMAIL_PATTERN =
        Pattern.compile("^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$");

    private static final Pattern USERNAME_PATTERN =
        Pattern.compile("^[a-zA-Z0-9_]{3,30}$");

    private Map<Long, User> users;
    private long nextId;

    public UserService() {
        this.users = new HashMap<>();
        this.nextId = 1L;
    }

    /**
     * Create a new user
     *
     * @param username Username
     * @param email Email address
     * @param displayName Display name
     * @return Created user
     * @throws IllegalArgumentException if validation fails
     */
    public User createUser(String username, String email, String displayName) {
        // Validate username
        if (!isValidUsername(username)) {
            throw new IllegalArgumentException("Invalid username format");
        }

        // Validate email
        if (!isValidEmail(email)) {
            throw new IllegalArgumentException("Invalid email format");
        }

        // Check if username already exists
        if (usernameExists(username)) {
            throw new IllegalArgumentException("Username already exists");
        }

        // Check if email already exists
        if (emailExists(email)) {
            throw new IllegalArgumentException("Email already exists");
        }

        User user = new User(nextId++, username, email, displayName);
        users.put(user.getId(), user);

        return user;
    }

    /**
     * Get user by ID
     *
     * @param userId User ID
     * @return Optional containing user if found
     */
    public Optional<User> getUserById(Long userId) {
        return Optional.ofNullable(users.get(userId));
    }

    /**
     * Get user by username
     *
     * @param username Username to search for
     * @return Optional containing user if found
     */
    public Optional<User> getUserByUsername(String username) {
        return users.values().stream()
            .filter(u -> u.getUsername().equals(username))
            .findFirst();
    }

    /**
     * Get user by email
     *
     * @param email Email to search for
     * @return Optional containing user if found
     */
    public Optional<User> getUserByEmail(String email) {
        return users.values().stream()
            .filter(u -> u.getEmail().equals(email))
            .findFirst();
    }

    /**
     * Update user's online status
     *
     * @param userId User ID
     * @param online Online status
     * @return true if updated successfully
     */
    public boolean updateOnlineStatus(Long userId, boolean online) {
        User user = users.get(userId);
        if (user == null) {
            return false;
        }

        user.setOnline(online);
        if (!online) {
            user.setLastSeen(LocalDateTime.now());
        }

        return true;
    }

    /**
     * Update user's display name
     *
     * @param userId User ID
     * @param displayName New display name
     * @return true if updated successfully
     */
    public boolean updateDisplayName(Long userId, String displayName) {
        User user = users.get(userId);
        if (user == null) {
            return false;
        }

        if (displayName == null || displayName.trim().isEmpty()) {
            throw new IllegalArgumentException("Display name cannot be empty");
        }

        if (displayName.length() > 50) {
            throw new IllegalArgumentException("Display name too long");
        }

        user.setDisplayName(displayName);
        return true;
    }

    /**
     * Update user's bio
     *
     * @param userId User ID
     * @param bio New bio text
     * @return true if updated successfully
     */
    public boolean updateBio(Long userId, String bio) {
        User user = users.get(userId);
        if (user == null) {
            return false;
        }

        if (bio != null && bio.length() > 500) {
            throw new IllegalArgumentException("Bio too long (max 500 characters)");
        }

        user.setBio(bio);
        return true;
    }

    /**
     * Delete a user
     *
     * @param userId User ID to delete
     * @return true if deleted successfully
     */
    public boolean deleteUser(Long userId) {
        return users.remove(userId) != null;
    }

    /**
     * Get all online users
     *
     * @return List of online users
     */
    public List<User> getOnlineUsers() {
        List<User> onlineUsers = new ArrayList<>();
        for (User user : users.values()) {
            if (user.isOnline()) {
                onlineUsers.add(user);
            }
        }
        return onlineUsers;
    }

    /**
     * Get all users
     *
     * @return List of all users
     */
    public List<User> getAllUsers() {
        return new ArrayList<>(users.values());
    }

    /**
     * Search users by username prefix
     *
     * @param prefix Username prefix to search for
     * @return List of matching users
     */
    public List<User> searchUsersByUsername(String prefix) {
        if (prefix == null || prefix.isEmpty()) {
            return new ArrayList<>();
        }

        List<User> results = new ArrayList<>();
        String lowerPrefix = prefix.toLowerCase();

        for (User user : users.values()) {
            if (user.getUsername().toLowerCase().startsWith(lowerPrefix)) {
                results.add(user);
            }
        }

        return results;
    }

    /**
     * Validate username format
     *
     * @param username Username to validate
     * @return true if valid
     */
    public boolean isValidUsername(String username) {
        if (username == null) {
            return false;
        }
        return USERNAME_PATTERN.matcher(username).matches();
    }

    /**
     * Validate email format
     *
     * @param email Email to validate
     * @return true if valid
     */
    public boolean isValidEmail(String email) {
        if (email == null) {
            return false;
        }
        return EMAIL_PATTERN.matcher(email).matches();
    }

    /**
     * Check if username exists
     *
     * @param username Username to check
     * @return true if exists
     */
    public boolean usernameExists(String username) {
        return getUserByUsername(username).isPresent();
    }

    /**
     * Check if email exists
     *
     * @param email Email to check
     * @return true if exists
     */
    public boolean emailExists(String email) {
        return getUserByEmail(email).isPresent();
    }

    /**
     * Get total user count
     *
     * @return Number of users
     */
    public int getUserCount() {
        return users.size();
    }

    /**
     * Get online user count
     *
     * @return Number of online users
     */
    public int getOnlineUserCount() {
        return (int) users.values().stream()
            .filter(User::isOnline)
            .count();
    }

    /**
     * User class representing a chat user
     */
    public static class User {
        private Long id;
        private String username;
        private String email;
        private String displayName;
        private boolean online;
        private LocalDateTime lastSeen;
        private LocalDateTime createdAt;
        private String bio;

        public User(Long id, String username, String email, String displayName) {
            this.id = id;
            this.username = username;
            this.email = email;
            this.displayName = displayName;
            this.online = false;
            this.createdAt = LocalDateTime.now();
            this.lastSeen = LocalDateTime.now();
            this.bio = "";
        }

        // Getters
        public Long getId() { return id; }
        public String getUsername() { return username; }
        public String getEmail() { return email; }
        public String getDisplayName() { return displayName; }
        public boolean isOnline() { return online; }
        public LocalDateTime getLastSeen() { return lastSeen; }
        public LocalDateTime getCreatedAt() { return createdAt; }
        public String getBio() { return bio; }

        // Setters
        public void setDisplayName(String displayName) { this.displayName = displayName; }
        public void setOnline(boolean online) { this.online = online; }
        public void setLastSeen(LocalDateTime lastSeen) { this.lastSeen = lastSeen; }
        public void setBio(String bio) { this.bio = bio; }

        @Override
        public String toString() {
            return "User{" +
                    "id=" + id +
                    ", username='" + username + '\'' +
                    ", email='" + email + '\'' +
                    ", displayName='" + displayName + '\'' +
                    ", online=" + online +
                    '}';
        }
    }
}
