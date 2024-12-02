from Member import Admin, User, Bot, Permission
import numpy as np

# ServerSystem class for managing channels and members
class Server:
    def __init__(self):
        # Dictionary to store chat logs for each channel
        self.__chatLogs = {}
        
        # Dictionary to store channels and their members
        self.__channels = {}
        
        # Array to store all members in the server, initially empty
        self.__members = np.empty(10, dtype=str)

    # Method to create a new channel
    def createChannel(self, member, channelName) -> bool:
        # Check if the member has the required permission
        if not member.hasPermission(Permission.CREATE_CHANNEL):
            print(f"Error: {member.name} does not have permission to create a channel.")
            return False
        
        # Check if the channel already exists
        if channelName in self.__channels:
            print(f"Error: Channel '{channelName}' already exists.")
            return False
        
        # Create the channel and initialize its member list
        self.__channels[channelName] = []
        print(f"Channel '{channelName}' created successfully by {member.name}.")
        return True

    # Method to allow a member to join an existing channel
    def joinChannel(self, member, channelName) -> bool:
        # Check if the channel exists
        if channelName not in self.__channels:
            print(f"Error: Channel '{channelName}' does not exist.")
            return False
        
        # Add the member to the channel's member list
        self.__channels[channelName].append(member)
        print(f"{member.name} joined the channel '{channelName}'.")
        return True

    # Method to add a new user to the server
    def addUserToServer(self, user) -> bool:
        # Check if the server's member array is full
        if self.__members.size >= 10 and all(self.__members):
            print("Error: Server member limit reached.")
            return False
        
        # Find an empty slot in the array and add the user
        for i in range(len(self.__members)):
            if self.__members[i] is None or self.__members[i] == '':
                self.__members[i] = user
                print(f"{user.name} added to the server.")
                return True
        
        return False

    # Method to add a user to a specific channel
    def addUserToChannel(self, member, user, channelName) -> bool:
        # Check if the member has the required permission
        if not member.hasPermission(Permission.ADD_USER):
            print(f"Error: {member.name} does not have permission to add users.")
            return False
        
        # Check if the channel exists
        if channelName not in self.__channels:
            print(f"Error: Channel '{channelName}' does not exist.")
            return False
        
        # Add the user to the channel's member list
        self.__channels[channelName].append(user)
        print(f"{user.name} added to '{channelName}' by {member.name}.")
        return True

    # Method to post a message in a specific channel
    def postMessage(self, member, channelName, message) -> bool:
        # Check if the member has the required permission
        if not member.hasPermission(Permission.POST_MESSAGE):
            print(f"Error: {member.name} does not have permission to post a message.")
            return False
        
        # Check if the channel exists and the member is part of the channel
        if channelName not in self.__channels or member not in self.__channels[channelName]:
            print(f"Error: {member.name} is not part of the channel '{channelName}'.")
            return False
        
        # Check if the message is not empty
        if not message.strip():
            print("Error: Message cannot be empty.")
            return False
        
        # Add the message to the channel's chat logs
        if channelName not in self.__chatLogs:
            self.__chatLogs[channelName] = []
        self.__chatLogs[channelName].append(message)
        print(f"Message from {member.name} posted successfully in '{channelName}'.")
        return True

    # Method to delete a specific channel
    def deleteChannel(self, member, channelName) -> bool:
        # Check if the member has the required permission
        if not member.hasPermission(Permission.DELETE_CHANNEL):
            print(f"Error: {member.name} does not have permission to delete a channel.")
            return False
        
        # Check if the channel exists
        if channelName not in self.__channels:
            print(f"Error: Channel '{channelName}' does not exist.")
            return False
        
        # Delete the channel
        del self.__channels[channelName]
        print(f"Channel '{channelName}' deleted successfully by {member.name}.")
        return True

    # Method to display all members in the server
    def displayMembers(self) -> bool:
        # Check if the member list is empty
        if self.__members.size == 0:
            print("Error! No Members Added!")
            return False
        
        # Print each member
        for x in self.__members:
            if x:
                print(x)
        return True

    # Method to display all existing channels
    def displayChannels(self) -> bool:
        # Check if there are no channels
        if not self.__channels:
            print("Error! No Channels Found!")
            return False
        
        # Print each channel name
        for x in self.__channels:
            print(x)
        return True

