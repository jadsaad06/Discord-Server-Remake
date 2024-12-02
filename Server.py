from Member import Admin, User, Bot, Permission
import numpy as np

# ServerSystem class for managing channels and members
class Server:
    def __init__(self):
        self.__chatLogs = {} #Dictionary to store channels and corresponding chat logs
        self.__channels = {}  # Dictionary to store channels and their members
        self.__members = np.empty(10, dtype=str) #array of all members in server

    def createChannel(self, member, channelName):
        if not member.hasPermission(Permission.CREATE_CHANNEL):
            return f"Error: {member.name} does not have permission to create a channel."
        if channelName in self.channels:
            return f"Error: Channel '{channelName}' already exists."
        
        self.channels[channelName] = []
        return f"Channel '{channelName}' created successfully by {member.name}."
    
    def joinChannel(self, member, channelName):
        if channelName not in self.channels:
            return f"Error: Channel '{channelName}' does not exist"
        
        self.channels[channelName].append(member)

    def addUserToServer(self, user, channelName):
        self.__members.append(user)
        
    def addUserToChannel(self, member, user, channelName):
        if not member.hasPermission(Permission.ADD_USER):
            return f"Error: {member.name} does not have permission to add users."
        
        if channelName not in self.channels:
            return f"Error: Channel '{channelName}' does not exist."
        
        self.channels[channelName].append(user)
        return f"{user.name} added to '{channelName}' by {member.name}."

    def postMessage(self, member, channelName, message):
        if not member.hasPermission(Permission.POST_MESSAGE):
            return f"Error: {member.name} does not have permission to post a message."
        
        if channelName not in self.channels or member not in self.channels[channelName]:
            return f"Error: {member.name} is not part of the channel '{channelName}'."
        
        if not message.strip():
            return "Error: Message cannot be empty."
        
        self.__chatLogs[channelName].append(message)

        return f"Message from {member.name} posted successfully in '{channelName}'."

    def deleteChannel(self, member, channelName):
        if not member.hasPermission(Permission.DELETE_CHANNEL):
            return f"Error: {member.name} does not have permission to delete a channel."
        if channelName not in self.channels:
            return f"Error: Channel '{channelName}' does not exist."
        
        del self.channels[channelName]

        return f"Channel '{channelName}' deleted successfully by {member.name}."
    
    def displayMembers(self):
        if self.__members.size == 0:
            return f"Error! No Members Added!"
        
        for x in self.__members:
            print(x)
    
    def displayChannels(self):
        if not self.__channels:
            return f"Error! No Channels Found!"
           
        for x in self.__channels:
            print(x)
    