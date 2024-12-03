#Name: Jad Saad
#Program: 4
#Class: CS302
#File: Main.py
"""Descripton: This program is inspired by Discord, bringing a community of gamers together through discussion channels!
In this program you are able to join as either a User, Moderator, or Admin. With each type of member, you get different permissions.
Using the os import, I was able to create, modify, and read files to save the channels, chat logs, and members! Using Glass Box testing,
I was able to make sure that all my code was working as I wrote it, and outputted working, well written code, efficiently"""


from Server import Server
from Member import User, Admin, Mod

def main():
    
    # Create server, loading previous state 
    server = Server()

    print("\nHello! Welcome to the Viking Gaming Hub!")
    print("\nWould you like to be a (1)User, (2)Admin or (3) Moderator? Enter 4 to exit.")
    
    valid = False
    
    while not valid:
        try:
            choice = int(input("\nEnter here: "))
            
            if choice in [1, 2, 3, 4]:
                valid = True
            else:
                print("\nWould you like to be a (1)User, (2)Admin or (3) Moderator? Enter 4 to exit.")
        except ValueError:
            print("\nMust Choose(1)User, (2)Admin or (3)Moderator? Enter 4 to exit.")
    
    if choice == 4:
        print("Goodbye!")
        return
    

    name = input("Enter your username: ")

    # Create Player
    if choice == 1:
        member = User(name)
    elif choice == 2:
        member = Admin(name)
    else:
        member = Mod(name)
    
    server.addUserToServer(member)

    choice = 0
    channelName = None

    while choice != 5:
        displayMenu()
        try:
            choice = int(input("\nEnter your choice: "))
            
            if choice == 1:
                channelName = joinChannel(server, member)

            elif choice == 2:
                    server.displayChatLog(channelName)

            elif choice == 3:
                    message = input("Input Message: ")
                    server.postMessage(member, channelName, message)

            elif choice == 4:
                if not isinstance(member, User):
                    launchAdminMenu(member, server, channelName)
                else:
                    print("Only Admins can perform this action.")
            elif choice == 5:
                print("Exiting system...")
            else:
                print("Invalid option. Please try again.")

        except ValueError:
            print("Invalid input. Please enter a number.")

def displayMenu() -> None:
    print("""\n1. Join a Channel: Users can select a channel to join.
2. View Messages: Users can see the most recent messages posted in the channel.
3. Send a Message: Users can post a message or send a private message. (private messaging will be added in prog5)
4. Admin/Moderator Actions (if applicable): Administrators can add or remove users and channels, and delete inappropriate messages. Moderators can only remove messages.
5. Exit System: Ends the session.""")


def launchAdminMenu(member, server: Server, channelName: str) -> None:
    # Display the admin menu with options
    print("""Admin Console: 
1. Add User 
2. Remove User 
3. Delete Message.
4. Create Channel
5. Remove Channel
6. Go Back""")
    
    valid = False  # Flag to track valid input

    # Loop until the user provides a valid input for the main menu
    while not valid:
        try:
            # Prompt user for input and convert to an integer
            choice = int(input("\nEnter your choice: "))

            # Check if the choice is valid
            if choice in [1, 2, 3, 4, 5, 6]:
                valid = True

        except ValueError:
            # Handle case where input is not an integer
            print("\nInvalid Choice!")

    # Action corresponding to the user's menu choice
    if choice == 1:
        # Prompt to input the username of the user to add
        userName = input("\nInput name of user: ")
        
        # Add the user to the channel
        server.addUserToChannel(member, User(userName), channelName)

    elif choice == 2:
        # Ask whether the user wants to remove from a channel or the server
        print("\nWould you like to remove from (1) Channel or (2) Server")
        
        valid = False  # Reset valid flag for sub-menu input
        while not valid:
            try:
                # Get user's choice for removal type (channel or server)
                remChoice = int(input("\nEnter your choice: "))

                # Check if the choice is valid (1 for channel, 2 for server)
                if remChoice in [1, 2]:
                    valid = True

            except ValueError:
                # Handle case where input is not an integer
                print("\nInvalid Choice!")
        
        # Get the username of the user to remove
        userName = input("\nInput name of user: ")

        if remChoice == 1:
            # If removing from a channel, check if channelName is provided
            if channelName is not None:
                # Remove user from the specified channel
                server.deleteUserFromChannel(member, userName, channelName)
            else:
                print("\nNot in a channel!")  # Handle case when not in a channel
        else:
            # If removing from the server, remove user from the server
            server.deleteUserFromServer(member, userName)

    elif choice == 3:
        # If deleting a message from the server
        if channelName is not None:
            # Display the chat log for the given channel
            server.displayChatLog(channelName)

            # Ask for the message content to delete
            message = input("Enter the brief content of message you'd like to remove: ")

            # Delete the message from the server
            server.deleteMessageFromServer(member, message, channelName)
        else:
            print("\nNot in a channel!")  # Handle case when not in a channel
    
    elif choice == 4:
        # Get the name of the channel wanting to be created
        toCreate = input("Input the name of the channel you'd like to create: ")
        
        server.createChannel(member, toCreate)
    elif choice == 5:
        # Get the name of the channel wanting to be deleted
        toDelete = input("Input the name of the channel you'd like to delete: ")
        
        server.deleteChannel(member, toDelete)

    
def joinChannel(server: Server, member) -> str:
    success = False

    #checks if there are channels to display
    if server.displayChannels():
        channelName = input("\nEnter the name of the desired channel: ")
        success = server.joinChannel(member, channelName)
        
        #return the channel name if channel exists
        if success:
            return channelName
    
    #return None when no channels are available
    return None
    



if __name__ == "__main__":
    main()
