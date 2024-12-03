#Name: Jad Saad
#File: Server.py

from Member import Admin, User, Mod, Permission
import numpy as np
import os

# ServerSystem class for managing channels and members
class Server:
    def __init__(self):
        # Dictionary to store chat logs for each channel
        self.__chatLogs = {}
        
        # Dictionary to store channels and their members
        self.__channels = {}
        
        # Array to store all members in the server
        self.__members = np.empty(15, dtype=object)

        # np array current size
        self.__memberCount = 0

        # Load From Files
        self.loadServerState()

    # Save the data to the channels, chatLogs, and member text files
    def saveServerState(self):
        try:
            # Save Members
            with open('members.txt', 'w') as f:
                for member in self.__members:
                    if member is not None and member != '':
                        f.write(f"{member}\n")

            # Save Channels
            with open('channels.txt', 'w') as f:
                for channel in self.__channels.keys():
                    f.write(f"{channel}\n")

            # Save Chat Logs
            with open('chatLogs.txt', 'w') as f:
                valid_channels = set(self.__channels.keys())
                for channel, logs in self.__chatLogs.items():
                    # Check if the channel is valid
                    if channel in valid_channels:
                        f.write(f"Channel: {channel}\n")
                        for log in logs:
                            f.write(f"{log}\n")
                        f.write("---END_OF_CHANNEL---\n")

            print("Server state saved successfully.")
            return True
        except Exception as e:
            print(f"Error saving server state: {e}")
            return False

    # Load the data from each of the three text files
    def loadServerState(self):

        try:
            # Load Members
            if os.path.exists('members.txt'):
                with open('members.txt', 'r') as f:
                    members = [line.strip() for line in f.readlines()]

                    for i, memberName in enumerate(members):
                        if i < 15:  
                            self.__members[i] = User(memberName)
                            self.__memberCount += 1

            # Load Channels
            if os.path.exists('channels.txt'):
                with open('channels.txt', 'r') as f:
                    channels = [line.strip() for line in f.readlines()]
                    for channel in channels:
                        self.__channels[channel] = []

            # Load Chat Logs
            if os.path.exists('chatLogs.txt'):
                with open('chatLogs.txt', 'r') as f:
                    current_channel = None
                    for line in f:
                        line = line.strip()
                        if line.startswith('Channel:'):
                            current_channel = line.split(': ')[1]
                            self.__chatLogs[current_channel] = []
                        elif line == '---END_OF_CHANNEL---':
                            current_channel = None
                        elif current_channel and line:
                            self.__chatLogs[current_channel].append(line)

            print("Server state loaded successfully.")
            return True
        except Exception as e:
            print(f"Error loading server state: {e}")
            return False

    def createChannel(self, member, channelName) -> bool:
        # Check if the member has the required permission
        if not member.hasPermission(Permission.CREATE_CHANNEL):
            print(f"Error: {member} does not have permission to create a channel.")
            return False
        
        # Check if the channel already exists
        if channelName in self.__channels:
            print(f"Error: Channel '{channelName}' already exists.")
            return False
        
        # Create the channel and initialize its member list
        self.__channels[channelName] = []
        print(f"Channel '{channelName}' created successfully by {member}.")
        
        # Save state after modification
        self.saveServerState()
        return True

    # Method to allow a member to join an existing channel
    def joinChannel(self, member, channelName) -> bool:
        # Check if the channel exists
        if channelName not in self.__channels:
            print(f"Error: Channel '{channelName}' does not exist.")
            return False
        
        # Add the member to the channel's member list
        self.__channels[channelName].append(member)
        print(f"{member} joined the channel '{channelName}'.")
        return True

    # Method to add a new user to the server
    def addUserToServer(self, user) -> bool:
        # Check if the server's member array is full
        if self.__memberCount >= 15:
            print("Error: Server member limit reached.")
            return False
        
        # Find an empty slot in the array and add the user
        if user not in self.__members:
            self.__members[self.__memberCount] = user
            self.__memberCount += 1
            print(f"{user} added to the server.")
        else:
            print(f"Welcome Back {user}!")
        self.saveServerState()
        return True
        
        return False

    # Method to add a user to a specific channel
    def addUserToChannel(self, member, user, channelName) -> bool:
        # Check if the member has the required permission
        if not member.hasPermission(Permission.ADD_USER):
            print(f"Error: {member} does not have permission to add users.")
            return False
        
        # Check if the channel exists
        if channelName not in self.__channels:
            print(f"Error: Channel '{channelName}' does not exist.")
            return False
        
        # Add the user to the channel's member list
        self.__channels[channelName].append(user)

        # Add the user to the server's member list
        if user not in self.__members:
            self.__members[self.__memberCount] = user
            self.__memberCount += 1

        print(f"{user} added to '{channelName}' by {member}.")
        self.saveServerState()
        return True

    # Method to post a message in a specific channel
    def postMessage(self, member, channelName, message) -> bool:
        # Check if the member has the required permission
        if not member.hasPermission(Permission.POST_MESSAGE):
            print(f"Error: {member} does not have permission to post a message.")
            return False
        
        # Check if the channel exists and the member is part of the channel
        if channelName not in self.__channels or member not in self.__channels[channelName]:
            print(f"Error: {member} is not part of a channel")
            return False
        
        # Check if the message is not empty
        if not message.strip():
            print("Error: Message cannot be empty.")
            return False
        
        # Add the message to the channel's chat logs
        if channelName not in self.__chatLogs:
            self.__chatLogs[channelName] = []
        self.__chatLogs[channelName].append(f"{member}: {message}")
        print(f"Message from {member} posted successfully in '{channelName}'.")
        self.saveServerState()
        return True

    # Method to delete a specific channel
    def deleteChannel(self, member, channelName) -> bool:
        # Check if the member has the required permission
        if not member.hasPermission(Permission.DELETE_CHANNEL):
            print(f"Error: {member} does not have permission to delete a channel.")
            return False
        
        # Check if the channel exists
        if channelName not in self.__channels:
            print(f"Error: Channel '{channelName}' does not exist.")
            return False
        
        # Delete the channel
        del self.__channels[channelName]
        print(f"Channel '{channelName}' deleted successfully by {member}.")
        self.saveServerState()
        return True

    # Method to delete a user from a specific channel
    def deleteUserFromChannel(self, member, userName, channelName) -> bool:
        # Check if member has the required permission
        if not member.hasPermission(Permission.REMOVE_USER):
            print(f"Error: {member} does not have permission to delete a user.")
            return False            
        
        # Check if the channel exists
        if channelName not in self.__channels:
            print(f"Error: Channel '{channelName}' does not exist.")
            return False
            
        # Check if the user exists
        if userName not in self.__channels[channelName]:
            print(f"Error: {userName} not in {channelName}")
            return False

        # Delete User
        self.__channels[channelName].remove(userName)
        print(f"Channel '{channelName}' deleted successfully by {member}.")
        return True 

    # Method to delete a user from the server
    def deleteUserFromServer(self, member, userName):
        # Check if member has the required permission
        if not member.hasPermission(Permission.REMOVE_USER):
            print(f"Error: {member} does not have permission to delete a user.")
            return False
        
        # Check if user is a member
        if userName not in self.__members:
            print(f"Error: {userName} does not exist.")
            return False

        self.__members = self.__members.delete(userName)

        for channelName in self.__channels:
            if userName in self.__channels[channelName]:
                self.deleteUserFromChannel(Admin(None), userName, channelName) 
        
        self.saveServerState()

    # Method to delete a message from a channel
    def deleteMessageFromServer(self, member, message, channelName):
        # Check if member has the required permission
        if not member.hasPermission(Permission.REMOVE_MESSAGE):
            print(f"Error: {member} does not have permission to delete a message.")
            return False

        # Check if the channel exists
        if channelName not in self.__channels:
            print(f"Error: Channel '{channelName}' does not exist.")
            return False
        
        # Look for message using substring
        for currMessage in self.__chatLogs[channelName]:
            if message in currMessage:
                self.__chatLogs[channelName].remove(currMessage)
                print("\nMessage Removed")
                return True
        
        # Returns False if message is not found
        print("\nMessage not found")
        return False
    
    



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

    # Method to display chat log in current channel
    def displayChatLog(self, channelName):
        if channelName is None:
            print("\nError! Not in a channel!")
        elif not self.__chatLogs[channelName]:
            print("\nNothing here yet!")
        else:
            for x in self.__chatLogs[channelName]:
                print(x)
    
    # Method to disploay all members in current channel
    def displayChannelMembers(self, channelName):
        if channelName not in self.__channels:
            print("\nChannel doesn't exist!")
        else:
            for x in self.__channels[channelName]:
                print(x)
