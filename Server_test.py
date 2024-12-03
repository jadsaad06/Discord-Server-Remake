#Name: Jad Saad
#File: Server_test.py

import pytest
import numpy as np
from Server import Server
from Member import User, Admin, Mod, Permission

# Create new server
@pytest.fixture
def server():
    return Server()

# Create Admin user
@pytest.fixture
def admin():
    return Admin("AdminUser")

# Create Regular User
@pytest.fixture
def regularUser():
    return User("RegularUser")

# Create Moderator User
@pytest.fixture
def modUser():
    return Mod("ModUser")

# Verify that a user can be successfully added to the server
def test_addUserToServer(server, regularUser):
    initial_count = server._Server__memberCount
    assert server.addUserToServer(regularUser) == True
    assert server._Server__memberCount == initial_count + 1
    assert regularUser in server._Server__members

# Ensure server cannot add users beyond its capacity limit
def test_addUserToServerFull(server):
    # Fill the server to capacity
    for i in range(15):
        server.addUserToServer(User(f"User{i}"))
    
    # Try to add one more user
    assert server.addUserToServer(User("ExtraUser")) == False

# Test creating a new channel successfully
def test_createChannel(server, admin):
    channel_name = "TestChannel"
    assert server.createChannel(admin, channel_name) == True
    assert channel_name in server._Server__channels
    assert server._Server__channels[channel_name] == []

# Verify that duplicate channel creation is not allowed
def test_createChannelDuplicate(server, admin):
    channel_name = "TestChannel"
    server.createChannel(admin, channel_name)
    assert server.createChannel(admin, channel_name) == False

# Ensure users without channel creation permission cannot create channels
def test_createChannelWithoutPermission(server, regularUser):
    assert server.createChannel(regularUser, "TestChannel") == False

# Test joining an existing channel
def test_joinChannel(server, admin, regularUser):
    channel_name = "TestChannel"
    server.createChannel(admin, channel_name)
    assert server.joinChannel(regularUser, channel_name) == True
    assert regularUser in server._Server__channels[channel_name]

# Verify that joining a nonexistent channel fails
def test_joinNonexistentChannel(server, regularUser):
    assert server.joinChannel(regularUser, "NonexistentChannel") == False

# Test adding a user to a channel
def test_addUserToChannel(server, admin, regularUser):
    channel_name = "TestChannel"
    server.createChannel(admin, channel_name)
    assert server.addUserToChannel(admin, regularUser, channel_name) == True
    assert regularUser in server._Server__channels[channel_name]

# Ensure users without permission cannot add other users to a channel
def test_addUserToChannelWithoutPermission(server, regularUser, modUser):
    channel_name = "TestChannel"
    server.createChannel(regularUser, channel_name)
    assert server.addUserToChannel(regularUser, modUser, channel_name) == False

# Test posting a message in a channel
def test_postMessage(server, admin, regularUser):
    channel_name = "TestChannel"
    server.createChannel(admin, channel_name)
    server.joinChannel(regularUser, channel_name)
    
    message = "Hello, world!"
    assert server.postMessage(regularUser, channel_name, message) == True
    assert f"{regularUser}: {message}" in server._Server__chatLogs[channel_name]

# Verify that posting a message without channel membership fails
def test_postMessageWithoutChannelMembership(server, admin, regularUser):
    channel_name = "TestChannel"
    server.createChannel(admin, channel_name)
    
    message = "Hello, world!"
    assert server.postMessage(regularUser, channel_name, message) == False

# Test deleting a channel
def test_deleteChannel(server, admin):
    channel_name = "TestChannel"
    server.createChannel(admin, channel_name)
    assert server.deleteChannel(admin, channel_name) == True
    assert channel_name not in server._Server__channels

# Ensure users without permission cannot delete channels
def test_deleteChannelWithoutPermission(server, regularUser):
    channel_name = "TestChannel"
    server.createChannel(regularUser, channel_name)
    assert server.deleteChannel(regularUser, channel_name) == False

# Test removing a user from a channel
def test_deleteUserFromChannel(server, admin, regularUser):
    channel_name = "TestChannel"
    server.createChannel(admin, channel_name)
    server.addUserToChannel(admin, regularUser, channel_name)
    
    assert server.deleteUserFromChannel(admin, regularUser._name, channel_name) == True
    assert regularUser not in server._Server__channels[channel_name]

# Test to check deletion of messages
def test_deleteMessageFromServer(server, admin, regularUser):
    channel_name = "TestChannel"
    server.createChannel(admin, channel_name)
    server.joinChannel(regularUser, channel_name)
    
    message = "Test message to delete"
    server.postMessage(regularUser, channel_name, message)

    assert server.deleteMessageFromChannel(admin, message, channel_name) == True
    assert all(message not in msg for msg in server._Server__chatLogs[channel_name])
    assert server.deleteMessageFromChannel(regularUser, message, channel_name) == False
