from db import get_connection
from date import parse_date
import re

def create_project(cur, conn, owner_id):
    print("Creating project...")

    while True:
        title = input('Project title: ').strip()
        if title:
            break
        print('Project title cannot be empty')

    while True:
        details = input('Project details: ').strip()
        if details:
            break
        print('Project details cannot be empty')

    while True:
        total_target = input('Target: ').strip()
        if re.match(r'^\d+(\.\d+)?$', total_target):
            break
        print('Target must be a valid number (e.g. 10000 or 10000.00)')

    while True:
        start_input = input("Start date: ").strip()
        start_date = parse_date(start_input)
        if start_date:
            break
        print("Invalid date. Try: 2025-12-31 or 31-Dec-2025")

    while True:
        end_input = input("End date: ").strip()
        end_date = parse_date(end_input)
        if end_date:
            break
        print("Invalid date. Try: 2025-12-31 or 31-Dec-2025")

    try:
        insert_query = '''
            INSERT INTO projects (title, details, total_target, start_date, end_date, owner_id) 
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING *
        '''
        cur.execute(insert_query, (title, details, total_target, start_date, end_date, owner_id))
        new_project = cur.fetchone()
        conn.commit()

        if new_project:
           print("\nProject created successfully:")
        else:
            print("\nProject created but no details returned.")
            return False

    except Exception as error:
        conn.rollback()
        print(f"Error creating project: {error}")
        return False

def view_projects(cur,owner_id):
    print("\n***Created Projects***\n")
    query = "SELECT * FROM projects WHERE owner_id = %s"
    cur.execute(query,(owner_id,))
    projects = cur.fetchall()
    for project in projects:
        print(f"ID: {project[0]}")
        print(f"Title: {project[1]}")
        print(f"Details: {project[2]}")
        print(f"Target: {project[3]}")
        print(f"Start Date: {project[4]}")
        print(f"End Date: {project[5]}")
        print("\n")

def edit_project(cur, conn):
    allowed_columns = ['title', 'details', 'total_target', 'start_date', 'end_date']
    while True:
        id = input("Enter project id you wish to edit:").strip()
        if not id.isdigit():
            print("Id must be a number")
            continue

        proper_id = int(id)

        check_query = "SELECT EXISTS(SELECT 1 FROM projects WHERE project_id = %s)"
        cur.execute(check_query, (proper_id,))
        exists = cur.fetchone()[0]
        
        if not exists:
            print(f"Project ID {proper_id} does not exist")
            continue
    
        print(f"\nEditing project with id = {proper_id}")
        fetch_query = '''
            SELECT * FROM projects WHERE project_id = %s
        '''
        cur.execute(fetch_query, (proper_id,))
        conn.commit()
        project = cur.fetchone()
        if project:
            print(f"Title: {project[1]}")
            print(f"Details: {project[2]}")
            print(f"Target: {project[3]}")
            print(f"Start Date: {project[4]}")
            print(f"End Date: {project[5]}")
        
        print("\nEditable fields:", ", ".join(allowed_columns))
        while True:
            column = input("Field:").strip().lower()
            if column not in allowed_columns:
                print("\nInvalid field. Please choose one of:", ", ".join(allowed_columns))
                continue    
            break

        fetch_column = f"SELECT {column} FROM projects WHERE project_id = %s"
        cur.execute(fetch_column, (proper_id,))
        value = cur.fetchone()
        if value is not None:
            print(f"Current value: {value[0]}")
        else:
            print("Value not found.") 
            return
        #Update the field
        while True:
            new_value = input(f"Enter new value for {column}: ").strip()
            if new_value:
                break

        update_query = f"UPDATE projects SET {column} = %s WHERE project_id = %s"
        try:
            cur.execute(update_query, (new_value, proper_id))
            conn.commit()
            print(f"\n{column} updated successfully.")
            return
        except Exception as error:
            conn.rollback()
            print(f"Error updating {column}: {error}")
    
def delete_project(cur,conn):
    while True:
        id_delete = input("Enter project id you wish to delete:").strip()
        if not id_delete.isdigit():
            print("Id must be a number")
            continue

        proper_id = int(id_delete)

        check_query = "SELECT EXISTS(SELECT 1 FROM projects WHERE project_id = %s)"
        cur.execute(check_query, (proper_id,))
        exists = cur.fetchone()[0]
        
        if not exists:
            print(f"Project ID {proper_id} does not exist")
            continue

        try:
            delete_query = "DELETE FROM projects WHERE project_id = %s"
            cur.execute(delete_query, (proper_id,))
            conn.commit()
            print(f"\nProject with ID {proper_id} deleted successfully.")
            return
        except Exception as error:
            conn.rollback()
            print(f"Error deleting project: {error}")
        

def project_menu(cur, conn, owner_id):
    while True:
        print("\n=== Project Menu ===")
        print("1. Create Project")
        print("2. View My Projects")
        print("3. Edit a project")
        print("4. Delete a project")
        print("5. Logout")
        
        choice = input("Enter your choice : ").strip()
        
        if choice == '1':
            create_project(cur,conn,owner_id)
        elif choice == '2':
            view_projects(cur,owner_id)
        elif choice == '3':
            edit_project(cur,conn)
        elif choice == '4':
            delete_project(cur,conn)
        elif choice == '5':
            print("Logging out...\n")
            break
        else:
            print("\nInvalid choice. Please try again.")