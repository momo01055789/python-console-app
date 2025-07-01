from db import get_connection
from auth import register, login
from projects import project_menu

def main():
    with get_connection() as (conn, cur):  
        print("Your database is ready")
        
        while True:
            print("Select an option:")
            print("1. Register")
            print("2. Login")
            print("3. Exit")
            choice = input("Enter your choice: ")
            
            if choice == "1":
                register(cur, conn) 
            elif choice == "2":
                user_id = login()
                if user_id:
                    print("Login successful!")
                    project_menu(cur, conn, user_id)
            elif choice == "3":
                print("Goodbye, come back soon :)")
                break
            else:
                print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main()
   

   
    