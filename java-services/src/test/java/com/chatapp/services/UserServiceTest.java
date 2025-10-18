package com.chatapp.services;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import static org.junit.jupiter.api.Assertions.*;

import java.util.List;
import java.util.Optional;

public class UserServiceTest {

    private UserService userService;

    @BeforeEach
    public void setUp() {
        userService = new UserService();
    }

    @Test
    public void testCreateUser_ValidInput() {
        UserService.User user = userService.createUser("testuser", "test@example.com", "Test User");

        assertNotNull(user);
        assertEquals("testuser", user.getUsername());
        assertEquals("test@example.com", user.getEmail());
        assertEquals("Test User", user.getDisplayName());
    }

    @Test
    public void testCreateUser_InvalidUsername() {
        assertThrows(IllegalArgumentException.class, () -> {
            userService.createUser("ab", "test@example.com", "Test");
        });
    }

    @Test
    public void testCreateUser_InvalidEmail() {
        assertThrows(IllegalArgumentException.class, () -> {
            userService.createUser("testuser", "invalid-email", "Test");
        });
    }

    @Test
    public void testCreateUser_DuplicateUsername() {
        userService.createUser("testuser", "test1@example.com", "Test User 1");

        assertThrows(IllegalArgumentException.class, () -> {
            userService.createUser("testuser", "test2@example.com", "Test User 2");
        });
    }

    @Test
    public void testGetUserById_Exists() {
        UserService.User created = userService.createUser("testuser", "test@example.com", "Test User");

        Optional<UserService.User> found = userService.getUserById(created.getId());

        assertTrue(found.isPresent());
        assertEquals("testuser", found.get().getUsername());
    }

    @Test
    public void testGetUserById_NotExists() {
        Optional<UserService.User> found = userService.getUserById(999L);

        assertFalse(found.isPresent());
    }

    @Test
    public void testGetUserByUsername_Exists() {
        userService.createUser("testuser", "test@example.com", "Test User");

        Optional<UserService.User> found = userService.getUserByUsername("testuser");

        assertTrue(found.isPresent());
        assertEquals("test@example.com", found.get().getEmail());
    }

    @Test
    public void testGetUserByEmail_Exists() {
        userService.createUser("testuser", "test@example.com", "Test User");

        Optional<UserService.User> found = userService.getUserByEmail("test@example.com");

        assertTrue(found.isPresent());
        assertEquals("testuser", found.get().getUsername());
    }

    @Test
    public void testUpdateOnlineStatus() {
        UserService.User user = userService.createUser("testuser", "test@example.com", "Test User");

        boolean result = userService.updateOnlineStatus(user.getId(), true);

        assertTrue(result);
        assertTrue(user.isOnline());
    }

    @Test
    public void testUpdateDisplayName_Valid() {
        UserService.User user = userService.createUser("testuser", "test@example.com", "Test User");

        boolean result = userService.updateDisplayName(user.getId(), "New Name");

        assertTrue(result);
        assertEquals("New Name", user.getDisplayName());
    }

    @Test
    public void testUpdateDisplayName_Empty() {
        UserService.User user = userService.createUser("testuser", "test@example.com", "Test User");

        assertThrows(IllegalArgumentException.class, () -> {
            userService.updateDisplayName(user.getId(), "");
        });
    }

    @Test
    public void testUpdateBio_Valid() {
        UserService.User user = userService.createUser("testuser", "test@example.com", "Test User");

        boolean result = userService.updateBio(user.getId(), "This is my bio");

        assertTrue(result);
        assertEquals("This is my bio", user.getBio());
    }

    @Test
    public void testDeleteUser() {
        UserService.User user = userService.createUser("testuser", "test@example.com", "Test User");

        boolean result = userService.deleteUser(user.getId());

        assertTrue(result);
        assertFalse(userService.getUserById(user.getId()).isPresent());
    }

    @Test
    public void testGetAllUsers() {
        userService.createUser("user1", "user1@example.com", "User 1");
        userService.createUser("user2", "user2@example.com", "User 2");

        List<UserService.User> users = userService.getAllUsers();

        assertEquals(2, users.size());
    }

    @Test
    public void testGetOnlineUsers() {
        UserService.User user1 = userService.createUser("user1", "user1@example.com", "User 1");
        UserService.User user2 = userService.createUser("user2", "user2@example.com", "User 2");

        userService.updateOnlineStatus(user1.getId(), true);

        List<UserService.User> onlineUsers = userService.getOnlineUsers();

        assertEquals(1, onlineUsers.size());
        assertEquals("user1", onlineUsers.get(0).getUsername());
    }

    @Test
    public void testSearchUsersByUsername() {
        userService.createUser("testuser1", "test1@example.com", "Test 1");
        userService.createUser("testuser2", "test2@example.com", "Test 2");
        userService.createUser("otheruser", "other@example.com", "Other");

        List<UserService.User> results = userService.searchUsersByUsername("test");

        assertEquals(2, results.size());
    }

    @Test
    public void testIsValidUsername() {
        assertTrue(userService.isValidUsername("validuser123"));
        assertTrue(userService.isValidUsername("user_name"));
        assertFalse(userService.isValidUsername("ab")); // too short
        assertFalse(userService.isValidUsername("")); // empty
        assertFalse(userService.isValidUsername(null)); // null
    }

    @Test
    public void testIsValidEmail() {
        assertTrue(userService.isValidEmail("test@example.com"));
        assertTrue(userService.isValidEmail("user.name@domain.co.uk"));
        assertFalse(userService.isValidEmail("invalid-email"));
        assertFalse(userService.isValidEmail("@example.com"));
        assertFalse(userService.isValidEmail(null));
    }

    @Test
    public void testGetUserCount() {
        assertEquals(0, userService.getUserCount());

        userService.createUser("user1", "user1@example.com", "User 1");
        assertEquals(1, userService.getUserCount());

        userService.createUser("user2", "user2@example.com", "User 2");
        assertEquals(2, userService.getUserCount());
    }

    @Test
    public void testGetOnlineUserCount() {
        UserService.User user1 = userService.createUser("user1", "user1@example.com", "User 1");
        UserService.User user2 = userService.createUser("user2", "user2@example.com", "User 2");

        assertEquals(0, userService.getOnlineUserCount());

        userService.updateOnlineStatus(user1.getId(), true);
        assertEquals(1, userService.getOnlineUserCount());

        userService.updateOnlineStatus(user2.getId(), true);
        assertEquals(2, userService.getOnlineUserCount());
    }
}
