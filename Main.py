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
    
    choice = 0
    currChannel = None

    while choice != 5:
        displayMenu()
        try:
            choice = int(input("\nEnter your choice: "))
            
            if choice == 1:
                channelName = joinChannel(server, member)


                
                while channelName is not None:
                    displayChannelMenu()
                    channelChoice = 0

                    # Validate Input
                    while not valid:
                        try:
                            choice = int(input("\nEnter here: "))
                            
                            if choice in [1, 2, 3]:
                                valid = True
                            else:
                                displayChannelMenu()
                        except ValueError:
                            displayChannelMenu()
                    
                    if choice == 1:
                        message = input("Input Message: ")

                        server.postMessage(member, channelName, message)
                    else:
                        server.displayChannelMembers()

                            


            elif choice == 2:
                # Show current interactions
                    server.displayChatLog(channelName)

            elif choice == 3:
                    message = input("Input Message: ")
                    server.postMessage(member, channelName, message)

            elif choice == 4:
                if member.hasPermission("create_channel"):
                    displayAdminMenu()

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

def displayChannelMenu():
    print("""\n1. Post a Message
2. List All Users in Current Channel
3. Go Back""")

def displayAdminMenu():
    print("""Admin Console: 
1. Add User 
2. Remove User 
3. Delete Message.""")


    
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
