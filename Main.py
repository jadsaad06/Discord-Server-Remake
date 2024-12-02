from Server import Server
from Member import Member, User, Admin

def main():
    print("\nHello! Welcome to the Viking Gaming Hub!")
    print("\nWould you like to be a (1)User or (2)Admin? Enter 3 to exit.")
    
    valid = False
    
    while not valid:
        try:
            choice = int(input("\nEnter here: "))
            
            if choice in [1, 2, 3]:
                valid = True
            else:
                print("\nMust choose (1)User, (2)Admin, or (3) to Exit.")
        except ValueError:
            print("\nMust choose (1)User, (2)Admin, or (3) to Exit.")
    
    if choice == 3:
        print("Goodbye!")
        return
    
    # Create server if not exiting
    server = Server()

    name = input("Enter your username: ")

    # Create Player
    if choice == 1:
        member = User(name)
    else:
        member = Admin(name)
    
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
                # Show current interactions
                    server.displayChatLog(channelName)

            elif choice == 3:
                    message = input("Input Message: ")
                    server.postMessage(member, channelName, message)

            elif choice == 4:
                if member.hasPermission("create_channel"):
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
4. Admin Actions (if applicable): Administrators can add or remove users, and delete inappropriate messages.
5. Exit System: Ends the session.""")

def displayChannelMenu() -> None:
    print("""\n1. Post a Message
2. List All Users in Current Channel
3. Go Back""")

def launchAdminMenu(member: Member, server: Server, channelName: str) -> None:
    # Display the admin menu with options
    print("""Admin Console: 
1. Add User 
2. Remove User 
3. Delete Message.
4. Go Back""")
    
    valid = False  # Flag to track valid input

    # Loop until the user provides a valid input for the main menu
    while not valid:
        try:
            # Prompt user for input and convert to an integer
            choice = int(input("\nEnter your choice: "))

            # Check if the choice is valid (1, 2, or 3 for actions)
            if choice in [1, 2, 3]:
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

    
def joinChannel(server: Server, member: Member) -> str:
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
