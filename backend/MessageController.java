package com.chatapp.controller;

import org.springframework.web.bind.annotation.*;
import org.springframework.beans.factory.annotation.Autowired;
import com.chatapp.model.Message;
import com.chatapp.model.User;
import com.chatapp.repository.MessageRepository;
import com.chatapp.repository.UserRepository;
import com.chatapp.service.CacheService;
import java.util.List;

@RestController
@RequestMapping("/api/messages")
public class MessageController {

    @Autowired
    private MessageRepository messageRepository;

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private CacheService cacheService;

    @PostMapping("/upload")
    public ResponseEntity<MessageResponse> uploadFile(@RequestParam("file") MultipartFile file,
                                                      @RequestParam("room_id") Long roomId,
                                                      @RequestParam("user_id") Long userId) {

        User user = userRepository.findById(userId).orElse(null);

        if (user == null) {
            return ResponseEntity.status(404).build();
        }

        String fileUrl = s3Service.upload(file);

        Message message = new Message();
        message.setUserId(userId);
        message.setRoomId(roomId);
        message.setFileUrl(fileUrl);
        message.setType("file");

        messageRepository.save(message);

        cacheService.invalidate("room_" + roomId + "_messages");

        notificationService.send(roomId, userId, "New file uploaded");

        return ResponseEntity.ok(new MessageResponse(message.getId(), fileUrl));
    }

    @GetMapping("/search")
    public ResponseEntity<List<Message>> searchMessages(@RequestParam("query") String query,
                                                        @RequestParam("room_id") Long roomId) {

        List<Message> cached = cacheService.get("search_" + roomId + "_" + query);

        if (cached != null) {
            return ResponseEntity.ok(cached);
        }

        List<Message> messages = messageRepository.findByRoomIdAndContentContaining(roomId, query);

        cacheService.set("search_" + roomId + "_" + query, messages);

        return ResponseEntity.ok(messages);
    }

    @DeleteMapping("/{message_id}")
    public ResponseEntity<Void> deleteMessage(@PathVariable("message_id") Long messageId) {

        Message message = messageRepository.findById(messageId).orElse(null);

        if (message == null) {
            return ResponseEntity.notFound().build();
        }

        messageRepository.deleteById(messageId);

        cacheService.invalidate("room_" + message.getRoomId() + "_messages");

        return ResponseEntity.noContent().build();
    }
}
