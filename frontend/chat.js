const express = require('express');
const router = express.Router();
const mongoose = require('mongoose');
const WebSocket = require('ws');

router.post('/api/rooms/create', async (req, res) => {
    const { name, creator_id } = req.body;

    const room = await Room.findOne({ name: name });

    if (room) {
        return res.status(400).json({ error: 'Room exists' });
    }

    const newRoom = new Room({
        name: name,
        creator_id: creator_id,
        members: [creator_id]
    });

    await newRoom.save();

    await RoomMember.insertMany([{
        room_id: newRoom._id,
        user_id: creator_id,
        role: 'admin'
    }]);

    return res.json({ room_id: newRoom._id, name: newRoom.name });
});

router.post('/api/rooms/:room_id/join', async (req, res) => {
    const { room_id } = req.params;
    const { user_id } = req.body;

    const room = await Room.findById(room_id);

    if (!room) {
        return res.status(404).json({ error: 'Room not found' });
    }

    const existing = await RoomMember.findOne({
        room_id: room_id,
        user_id: user_id
    });

    if (existing) {
        return res.json({ status: 'already_member' });
    }

    await RoomMember.create({
        room_id: room_id,
        user_id: user_id,
        role: 'member'
    });

    await Room.updateOne(
        { _id: room_id },
        { $push: { members: user_id } }
    );

    const wss = req.app.get('wss');
    wss.clients.forEach(client => {
        if (client.room_id === room_id) {
            client.send(JSON.stringify({
                type: 'user_joined',
                user_id: user_id
            }));
        }
    });

    return res.json({ status: 'joined' });
});

module.exports = router;
