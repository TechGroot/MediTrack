import matplotlib.pyplot as plt
import mysql.connector as ms
import pandas as pd

def init():
    # Establising the database connection
    db = ms.connect(host = "localhost", user = "root", passwd = "root", database = "hospital_management_system")
    db_cursor = db.cursor()

    # Booting the application
    boot_app(db, db_cursor)

def boot_app(db, db_cursor):
    print("\n")
    print("********************************************************************")
    print("******                                                        ******")
    print("*****                                                          *****")
    print("****                                                            ****")
    print("***                                                              ***")
    print("**                                                                **")
    print("**                   WELCOME TO CITY HOSPITAL                     **")
    print("**                                                                **")
    print("***                                                              ***")
    print("****                                                            ****")
    print("*****                                                          *****")
    print("******                                                        ******")
    print("********************************************************************")

    while True:
        print("\nManage:")
        print("1.Doctor")
        print("2.Patient")
        print("3.Staff")
        print("\nView:")
        print("4.Statistics")
        print("\n[Enter -1 to Exit Application]")

        # Inputting one of the above choices
        while True:
            choice = input("\nPlease enter your choice: ")
            
            if choice != "":
                break

        if choice == "-1":
            break

        elif choice == "1":
            manage_doctor(db, db_cursor)

        elif choice == "2":
            manage_patient(db, db_cursor)
            
        elif choice == "3":
            manage_staff(db, db_cursor)

        elif choice == "4":
            view_statistics(db, db_cursor)
            
        else:
            print("\n| Error: There is no such option. |")

    print("\nSuccessfully Exited!\n")

def manage_doctor(db, db_cursor):
    
    while True:
        print("\n")
        print(" ------------------------------------------------")
        print("|                                                |")
        print("|\tWELCOME TO DOCTOR MANAGEMENT PANEL       |")
        print("|                                                |")
        print(" ------------------------------------------------")
        print("\nSelect an option")
        print("\n1.Add a new doctor's detail")
        print("2.Delete a doctor's detail")
        print("3.Update a doctor's detail")
        print("4.View a doctor's detail")
        print("5.View all doctors' detail")

        print("\n[Enter -2 to Go Back]")

        # Inputting one of the above choice
        while True:
            choice = input("\nPlease enter your choice: ")

            if choice != "":
                break

        if choice == "-2":
            break

        # Adding a doctor   
        elif choice == "1":
            print("\n ------------------")
            print("| Add A New Doctor |")
            print(" ------------------")
            # Inputting new doctor's details
            name = input("\nPlease enter doctor's name: ")
            specialist = input("Please enter the field in which doctor specialises: ")
            phone_number = input("Please enter doctor's number: ")

            # Adding doctor to the database
            query = """insert into doctor_record(Name, Specialist, Phone_Number) values(%s, %s, %s)"""

            db_cursor.execute(query, (name, specialist, phone_number))
            db.commit()

            # Checking if adding the doctor was successful
            if db_cursor.rowcount == 0:
                print("\n| Status: Failed to add doctor " + name + " details. |")
                
            else:
                print("\n| Status: Doctor " + name + " details were successfully added. |")

            # Giving id to the user
            id_query = """select max(id) from doctor_record"""
            db_cursor.execute(id_query,)
            results = db_cursor.fetchall()
            
            print("\nDoctor " + name + "'s Id is: ", results[0][0])

        # Deleting a doctor       
        elif choice == "2":
            
            print("\n -----------------")
            print("| Delete A Doctor |")
            print(" -----------------")
            
            # Input doctor's id
            delete_id = int(input("\nPlease enter the id of the doctor to be removed: "))

            # Fetching all the details of the entered id
            query = """select * from doctor_record where id = %s"""

            db_cursor.execute(query, (delete_id, ))
            results = db_cursor.fetchall()
            
            # Checking if id exixts
            if len(results) == 0:
                print("\n| Error: There is no such id. |")
                 
            else:
                # Printing details of the doctor for the above id
                print("\nDetails for the above id are: ")
                for result in results:
                    print("\nId: " + str(result[0]) + "\nName: " + result[1] + "\nSpecialised in: " + result[2] + "\nPhone_Number: " + result[3] + "\n")

                # Asking for confirmation
                confirmation = input("Are you sure you want to delete this data from database (y/n): ")

                # Deleting the data for the doctor
                if confirmation == "y" or confirmation == "Y":
                    query = """delete from doctor_record where id = %s"""

                    db_cursor.execute(query, (delete_id, ))
                    db.commit()
                
                    # Checking if deleting the record was successful
                    if db_cursor.rowcount == 0:
                        print("\n| Status: Deleting doctor " + result[1] + " details failed. |")
                        
                    else:
                        print("\n| Status: Doctor " + result[1] + " was removed from the records successfully. |")

                elif confirmation == "N" or confirmation == "n":
                    print("\n| Status: Deletion for the doctor " + result[1] + " cancelled. |")
                    
                # If user enters invalid choice
                else:
                    print("\n| Error: There is no such option. |")        

        # Updating records for a doctor       
        elif choice == "3":
            
            print("\n -------------------------")
            print("|Update A Doctor's Record |")
            print(" -------------------------")

            # Inputting the id of the doctor 
            update_id = int(input("\nPlease enter the id of the doctor whose record is to be updated: "))
            
            # Fetching details for the above id
            query = """select * from doctor_record where id = %s"""

            db_cursor.execute(query, (update_id, ))
            results = db_cursor.fetchall()

            # Checking if the id exists in the database
            if len(results) == 0:
                print("\n| Error: No such Id exists. |")
            
            else:
                print("\nDetails for the above id are: ")
                for result in results:
                    print("\nId: " + str(result[0]) + "\nName: " + result[1] + "\nSpecialised in: " + result[2] + "\nPhone_Number: " + result[3] + "\n")
                    
                print("\nSelect the criteria to be updated:")
                print("\n1.Name")
                print("2.Specialisation")
                print("3.Phone Number")

                # Inputting the criteria to be updated
                update_choice = int(input("\nPlease enter your choice: "))

                # Updating value of name
                if update_choice == 1:

                    # Inputting updated name
                    name = input("\nPlease enter the updated name: ")

                    # Updating the value in the database
                    query = """update doctor_record
                                set Name = %s
                                where id = %s"""
                    
                    db_cursor.execute(query, (name, update_id))
                    db.commit()

                    # Checking if updation was successful
                    if db_cursor.rowcount == 0:
                        print("\n| Status: Updating the doctor name " + name + " failed. |")

                    else:
                        print("\n| Status: Doctor's name " + name + " successfully updated. |")
                        
                # Updating value of specialisation
                elif update_choice == 2:

                    # Inputting updated field specialisation
                    specialist = input("\nPlease enter the updated specialisation field: ")

                    # Updating record in database 
                    query = """update doctor_record
                                set Specialist = %s
                                where id = %s"""
                    db_cursor.execute(query, (specialist, update_id))
                    db.commit()

                    # Checking if updation was successful
                    if db_cursor.rowcount == 0:
                        print("\n| Status: Updating the doctor " + result[1] + "'s specialisation " + specialist + " failed. |")

                    else:
                        print("\n| Status: Doctor " + result[1] + "'s specialisation " + specialist + " has been updated. |")
                        
                # Updating value of phone number
                elif update_choice == 3:

                    # Inputting phone number
                    phone_number = input("\nPlease enter the updated phone number: ")

                    # Updating value in the database record
                    query = """update doctor_record
                                set Phone_Number = %s
                                where id = %s"""
                    
                    db_cursor.execute(query, (phone_number, update_id))
                    db.commit()

                    # Checking if update was successful
                    if db_cursor.rowcount == 0:
                        print("\n|Status: Updating the doctor " + result[1] + "'s phone number " + phone_number + " failed. |")
                       
                    else:
                        print("\n| Status: Updating the doctor " + result[1] + "'s phone number " + phone_number + " was successful. |")
                        
                # If user enters invalid choice
                else:
                    print("\n| Error: There is no such option. |")

        # Viewing a doctor
        elif choice == "4":
            
            print("\n ---------------")
            print("| View A Doctor |")
            print(" ---------------")
            
            # Inputting the id of the doctor to be viewed
            view_id = int(input("\nPlease enter the id of the doctor to be viewed: "))
            
            # Fetching data from the database
            query = """select * from doctor_record where id = %s"""
            
            db_cursor.execute(query, (view_id, ))
            results = db_cursor.fetchall()
            
            # Checking if id is correct
            if len(results) == 0:
                print("\n| Error: No doctor found with given id. |")
                
            else:
                for result in results:
                    print("\nId: " + str(result[0]) + "\nName: " + result[1] + "\nSpecialisation: " + result[2] + "\nPhone number: " + result[3])

        #Viewing all records
        elif choice == "5":

            print("\n ------------------")
            print("| View All Records |")
            print(" ------------------")

            # Fetching data
            query = pd.read_sql('select * from doctor_record',db)
            print(query)
            

        # If user enter invalid choice
        else:
            print("\n| Error: There is no such option. |")

def manage_patient(db, db_cursor):
    
    while True:
        print("\n")
        print(" ------------------------------------------------")
        print("|                                                |")
        print("|\tWELCOME TO PATIENT MANAGEMENT PANEL      |")
        print("|                                                |")
        print(" ------------------------------------------------")
        print("\nSelect an option")
        print("\n1.Add a new patient's detail")
        print("2.Delete a patient's detail")
        print("3.Update a patient's detail")
        print("4.View a patient's detail")
        print("5.View all patients' detail")
        print("\n[Enter -2 to go back]")

        # Inputting one of the above choices
        while True:
            choice = input("\nPlease enter your choice: ")

            if choice != "":
                break
            
        if choice == "-2":
            break

        # Adding a patient
        if choice == "1":
            
            print("\n -------------------")
            print("| Add A New Patient |")
            print(" -------------------")

            # Inputting new patient's details
            name = input("\nPlease enter patient's name: ")
            disease = input("Please enter patient's disease: ")
            gender = input("Please enter the gender of the paient: ")
            age = int(input("Please enter the age of the patient: "))
            phone_number = input("Please enter patient's phone number: ")

            # Adding data to the database
            query = """Insert into patient_record(Name, Disease, Phone_Number, Gender, Age) values(%s, %s, %s, %s, %s)"""

            db_cursor.execute(query, (name, disease, phone_number, gender, age))
            db.commit()

            # Checking if data was successfully added
            if db_cursor.rowcount == 0:
                print("\n| Status: Adding patient " + name + " to the database failed. |")

            else:
                print("\n| Status: Adding patient " + name + " to the database was successful. |")

            # Giving id to the user
            id_query = """select max(id) from patient_record"""
            db_cursor.execute(id_query,)
            results = db_cursor.fetchall()
            
            print("\nPatient " + name + "'s Id is: ", results[0][0])


        # Deleting a patient    
        elif choice == "2":
            
            print("\n ------------------")
            print("| Delete A Patient |")
            print(" ------------------")

            # Inputting id to delete from records
            delete_id = input("\nPlease enter the id of the patient to be removed: ")

             # Fetching all the details of the entered id
            query = """select * from patient_record where id = %s"""

            db_cursor.execute(query, (delete_id, ))
            results = db_cursor.fetchall()
            
            # Checking if id exixts
            if len(results) == 0:
                print("\n| Error: There is no such id. |")
                
            else:
                print("\nDetails for the above id are: ")
                for result in results:
                    print("\nId: " + str(result[0]) + "\nName: " + result[1] + "\nDisease: " + result[2] + "\nPhone_Number: " + result[3] + "\nGender: " + result[4]
                          + "\nAge: " + str(result[5]) + "\n")

                # Asking for confirmation
                confirmation = input("Are you sure you want to delete this data from database (y/n): ")

                # Deleting the data for the patient
                if confirmation == "y" or confirmation == "Y":
                    query = """delete from patient_record where id = %s"""

                    db_cursor.execute(query, (delete_id, ))
                    db.commit()
                    
                    # Checking if deleting the record was successful
                    if db_cursor.rowcount == 0:
                        print("\n| Status: Deleting patient " + result[1] + " details failed. |\n")
                        
                    else:
                        print("\n| Status: Patient " + result[1] + " was removed from the records successfully. |")

                elif confirmation == "N" or confirmation == "n":
                    print("\n| Status: Deletion for the patient " + result[1] + " cancelled. |")
                    
                # If user enters invalid choice 
                else:
                    print("\n| Error: There is no such option. |")        

        # Updating records for a patient
        elif choice == "3":
            
            print("\n ---------------------------")
            print("| Update A Patient's Record |")
            print(" ---------------------------")

            # Inputting the id of the patient
            update_id = int(input("\nPlease enter the id of the patient whose record is to be updated: "))
            
            # Fetching details for the above id
            query = """select * from patient_record where id = %s"""

            db_cursor.execute(query, (update_id, ))
            results = db_cursor.fetchall()

            # Checking if the id exists in the database
            if len(results) == 0:
                print("\n| Error: No such Id exists. |")
                  
            else:
                print("\nDetails for the above id are: ")
                for result in results:
                    print("\nId: " + str(result[0]) + "\nName: " + result[1] + "\nDisease: " + result[2] + "\nPhone_Number: " + result[3] + "\nGender: " + result[4]
                          + "\nAge: " + str(result[5]) + "\n")
                    
                print("\nSelect the criteria to be updated:")
                print("\n1.Name")
                print("2.Disease")
                print("3.Phone_Number")
                print("4.Gender")
                print("5.Age")

                # Inputting the criteria to be updated
                update_choice = int(input("\nPlease enter your choice: "))

                # Updating value of name
                if update_choice == 1:

                    # Inputting updated name
                    name = input("\nPlease enter the updated name: ")

                    # Updating the value in the database
                    query = """update patient_record
                                set Name = %s
                                where id = %s"""
                    
                    db_cursor.execute(query, (name, update_id))
                    db.commit()

                    # Checking if updation was successful
                    if db_cursor.rowcount == 0:
                        print("\n| Status: Updating the patient's name " + name + " failed. |")

                    else:
                        print("\n| Status: Patient's name " + name + " successfully updated. |")

                # Updating value of disease
                elif update_choice == 2:

                    # Inputting updated disease
                    disease = input("\nPlease enter the updated disease: ")

                    # Updating record in database 
                    query = """update patient_record
                                set Disease = %s
                                where id = %s"""
                    db_cursor.execute(query, (disease, update_id))
                    db.commit()

                    # Checking if updation was successful
                    if db_cursor.rowcount == 0:
                        print("\n| Status: Updating the patient " + result[1] + "'s disease " + disease + " failed. |")
                        
                    else:
                        print("\n| Status: Patient " + result[1] + "'s disease " + disease + " has been updated. |")
                        
                # Updating value of phone number
                elif update_choice == 3:

                    # Inputting updated phone number
                    phone_number = input("\nPlease enter the updated phone number: ")

                    # Updating value in the database record
                    query = """update patient_record
                                set Phone_Number = %s
                                where id = %s"""
                    
                    db_cursor.execute(query, (phone_number, update_id))
                    db.commit()

                    # Checking if update was successful
                    if db_cursor.rowcount == 0:
                        print("\n|Status: Updating the patient " + result[1] + "'s phone number " + phone_number + " failed. |")

                    else:
                        print("\n| Status: Updating the patient " + result[1] + "'s phone number " + phone_number + " was successful. |")
                        

                # Updating value of gender
                elif update_choice == 4:

                    # Inputting updated gender
                    gender = input("\nPlease enter the updated gender: ")

                    # Updating value in the database
                    query = """update patient_record
                                set Gender = %s
                                where id = %s"""

                    db_cursor.execute(query, (gender, update_id))
                    db.commit()

                    # Checking if update was successful
                    if db_cursor.rowcount == 0:
                          print("\n|Status: Updating the patient " + result[1] + "'s gender " + gender + " failed |")

                    else:
                        print("\n| Status: Updating the patient " + result[1] + "'s gender " + gender + " was successful. |")

                # Updating value of age
                elif update_choice == 5:

                    # Inputting updated age
                    age = int(input("\nPlease enter the updated age: "))

                    # Updating value in the database
                    query = """update patient_record
                                set Age = %s
                                where id = %s"""

                    db_cursor.execute(query, (age, update_id))
                    db.commit()

                    # Checking if update was successful
                    if db_cursor.rowcount == 0:
                        print("\n|Status: Updating the patient " + result[1] + "'s age " + str(age) + " failed. |")
                        
                    else:
                        print("\n| Status: Updating the patient " + result[1] + "'s age " + str(age) + " was successful. |")


                # If user enters invalid choice
                else:
                    print("\n| Error: There is no such option. |")

        # Viewing a patient's record
        elif choice == "4":
            
            print("\n ----------------")
            print("| View A Patient |")
            print(" ----------------")
            
            # Inputting the id of the patient to be viewed
            view_id = int(input("\nPlease enter the id of the patient to be viewed: "))
            
            # Fetching data from the database
            query = """select * from patient_record where id = %s"""
            
            db_cursor.execute(query, (view_id, ))
            results = db_cursor.fetchall()
            
            # Checking if id is correct
            if len(results) == 0:
                print("\n| Error: No patient found with given id. |")
                
            else:
                for result in results:
                    print("\nId: " + str(result[0]) + "\nName: " + result[1] + "\nDisease: " + result[2] + "\nPhone_Number: " + result[3] + "\nGender: " + result[4]
                          + "\nAge: " + str(result[5]) + "\n")

        # Viewing all records
        elif choice == "5":

            print("\n ------------------")
            print("| View All Records |")
            print(" ------------------")

            # Fetching the data
            query = pd.read_sql('select * from patient_record',db)
            print(query)
                    
        # If user enter invalid choice
        else:
            print("\n| Error: There is no such option |\n")

def manage_staff(db, db_cursor):

    while True:
        print("\n")
        print(" ------------------------------------------------")
        print("|                                                |")
        print("|\tWELCOME TO STAFF MANAGEMENT PANEL        |")
        print("|                                                |")
        print(" ------------------------------------------------")
        print("\nSelect an option")
        print("\n1.Add a new staff member's detail")
        print("2.Delete a staff member's detail")
        print("3.Update a staff member's detail")
        print("4.View a staff member's detail")
        print("5.View all staff members' detail")
        print("\n[Enter -2 to go back]")

        # Inputting one of the above choices
        while True:
            choice = input("\nPlease enter your choice: ")

            if choice != "":
                break

        if choice == "-2":
            break

        # Adding a staff member
        if choice == "1":
            
            print("\n ------------------------")
            print("| Add A New Staff Member |")
            print(" ------------------------")

            # Inputting new staff member's details
            name = input("\nPlease enter staff member's name: ")
            role = input("Please enter staff member's role: ")
            phone_number = input("Please enter staff member's phone number: ")

            # Adding data to the database
            query = """Insert into staff_record(Name, Role, Phone_Number) values(%s, %s, %s)"""

            db_cursor.execute(query, (name, role, phone_number))
            db.commit()

            # Checking if data was successfully added
            if db_cursor.rowcount == 0:
                print("\n| Status: Adding staff memeber " + name + " to the database failed. |")

            else:
                print("\n| Status: Adding staff member " + name + " to the database was successful. |")

            # Giving id to the user
            id_query = """select max(id) from staff_record"""
            db_cursor.execute(id_query,)
            results = db_cursor.fetchall()
            
            print("\nStaff member " + name + "'s Id is: ", results[0][0])

        # Deleting a staff member
        elif choice == "2":
            
            print("\n -----------------------")
            print("| Delete A Staff Member |")
            print(" -----------------------")
            
            # Input staff member's id
            delete_id = int(input("\nPlease enter the id of the staff member to be removed: "))

            # Fetching all the details of the entered id
            query = """select * from staff_record where id = %s"""

            # Printing details of the staff member for the above id
            db_cursor.execute(query, (delete_id, ))
            results = db_cursor.fetchall()
            
            # Checking if id exixts
            if len(results) == 0:
                print("\n| Error: There is no such id. |")
                
            else:
                print("\nDetails for the above id are: ")
                for result in results:
                    print("\nId: " + str(result[0]) + "\nName: " + result[1] + "\nRole: " + result[2] + "\nPhone_Number: " + result[3] + "\n")

                # Asking for confirmation
                confirmation = input("Are you sure you want to delete this data from database (y/n): ")

                # Deleting the data for the doctor
                if confirmation == "y" or confirmation == "Y":
                    query = """delete from staff_record where id = %s"""

                    db_cursor.execute(query, (delete_id, ))
                    db.commit()
                        
                    # Checking if deleting the record was successful
                    if db_cursor.rowcount == 0:
                        print("\n| Status: Deleting staff member " + result[1] + " details failed. |")
                        
                    else:
                        print("\n| Status: Staff member " + result[1] + " was removed from the records successfully. |")

                elif confirmation == "N" or confirmation == "n":
                    print("\n| Status: Deletion for the staff member " + result[1] + " cancelled. |")
                    
                # If user enters choice other than y or n
                else:
                    print("\n| Error: There is no such option. |")

        # Updating value of a staff member
        elif choice == "3":
            
            print("\n --------------------------------")
            print("| Update A Staff Member's Record |")
            print(" --------------------------------")

            # Inputting the id of the staff member 
            update_id = int(input("\nPlease enter the id of the staff member whose record is to be updated: "))
            
            # Fetching details for the above id
            query = """select * from staff_record where id = %s"""

            db_cursor.execute(query, (update_id, ))
            results = db_cursor.fetchall()

            # Checking if the id exists in the database
            if len(results) == 0:
                print("\n| Error: No such Id exists. |")
                   
            else:
                print("\nDetails for the above id are: ")
                for result in results:
                    print("\nId: " + str(result[0]) + "\nName: " + result[1] + "\nRole: " + result[2] + "\nPhone_Number: " + result[3] + "\n")
                    
                print("\nSelect the criteria to be updated:")
                print("\n1.Name")
                print("2.Role")
                print("3.Phone Number")

                # Inputting the criteria to be updated
                update_choice = int(input("\nPlease enter your choice: "))

                # Updating value of name
                if update_choice == 1:

                    # Inputting updated name
                    name = input("\nPlease enter the updated name: ")

                    # Updating the value in the database
                    query = """update patient_record
                                set Name = %s
                                where id = %s"""
                    
                    db_cursor.execute(query, (name, update_id))
                    db.commit()

                    # Checking if updation was successful
                    if db_cursor.rowcount == 0:
                        print("\n| Status: Updating the staff member name " + name + " failed. |")

                    else:
                        print("\n| Status: Staff member's name " + name + " successfully updated. |")
                        
                # Updating value of role
                elif update_choice == 2:

                    # Inputting updated role
                    role = input("\nPlease enter the updated role: ")

                    # Updating record in database 
                    query = """update staff_record
                                set Role = %s
                                where id = %s"""
                    
                    db_cursor.execute(query, (role, update_id))
                    db.commit()

                    # Checking if updation was successful
                    if db_cursor.rowcount == 0:
                        print("\n| Status: Updating the staff member " + result[1] + "'s role " + role + " failed. |")

                    else:
                        print("\n| Status: Staff member " + result[1] + "'s role " + role + " has been updated. |")
                        
                # Updating value of phone number
                elif update_choice == 3:

                    # Inputting phone number
                    phone_number = input("\nPlease enter the updated phone number: ")

                    # Updating value in the database record
                    query = """update staff_record
                                set Phone_Number = %s
                                where id = %s"""
                    
                    db_cursor.execute(query, (phone_number, update_id))
                    db.commit()

                    # Checking if update was successful
                    if db_cursor.rowcount == 0:
                        print("\n|Status: Updating the staff member " + result[1] + "'s phone number " + phone_number + " failed. |")
                       
                    else:
                        print("\n| Status: Updating the staff member " + result[1] + "'s phone number " + phone_number + " was successful. |")
                        
                # If user enters choice other than 1, 2, 3
                else:
                    print("\n| Error: There is no such option. |")

        # Viewing a staff member
        elif choice == "4":
            
            print("\n ---------------------")
            print("| View A Staff Member |")
            print(" ---------------------")
            
            # Inputting the id of the staff member to be viewed
            view_id = int(input("\nPlease enter the id of the staff member to be viewed: "))
            
            # Fetching data from the database
            query = """select * from staff_record where id = %s"""
            
            db_cursor.execute(query, (view_id, ))
            results = db_cursor.fetchall()
            
            # Checking if id is correct
            if len(results) == 0:
                print("\n| Error: No staff member found with given id. |")
            
            else:
                for result in results:
                    print("\nId: " + str(result[0]) + "\nName: " + result[1] + "\nRole: " + result[2] + "\nPhone number: " + result[3])

        # Viewing all records
        elif choice == "5":

            print("\n ------------------")
            print("| View All Records |")
            print(" ------------------")

            # Fetching data
            query = pd.read_sql('select * from staff_record',db)
            print(query)

        # If user enter invalid choice
        else:
            print("\n| Error: There is no such option |\n")

def view_statistics(db, db_cursor):

    while True:
        print("\n")
        print(" ------------------------------------------------")
        print("|                                                |")
        print("|\tWELCOME TO VIEW STATISTICS PANEL         |")
        print("|                                                |")
        print(" ------------------------------------------------")
        print("\nSelect an option")
        print("\n1.Number of female patients in each disease")
        print("2.Number of male patients in each diasease")
        print("3.Number of specialists in different fields")
        print("4.Number of staff members from different categories")
        print("\n[Enter -2 to go back]")

        # Inputting one of the above choices
        while True:
            choice = input("\nPlease enter your choice: ")

            if choice != "":
                break

        if choice == "-2":
            break

        # Graph for female patients
        elif choice == "1":

            # Fetching data for graph
            query = """select disease, count(*) from patient_record where gender = "Female" group by disease"""

            db_cursor.execute(query,)
            results = db_cursor.fetchall()
            
            # Creating empty list to store data
            disease = []
            female_patient = []
            
            for result in results:             
                disease.append(result[0])
                female_patient.append(result[1])

            # Plotting the graph
            plt.bar(disease, female_patient, width = .3)
            plt.xlabel("Diseases")
            plt.ylabel("Female Patients")            
            plt.title("Number Of Female Patients In Each Disease")
            plt.show()

        # Graph for male patients
        elif choice == "2":

            # Fetching data for graph
            query = """select disease, count(*) from patient_record where gender = "Male" group by disease"""

            db_cursor.execute(query,)
            results = db_cursor.fetchall()
            
            # Creating empty list to store data
            disease = []
            male_patient = []
            
            for result in results:
                disease.append(result[0])
                male_patient.append(result[1])

            # Plotting the graph
            plt.bar(disease, male_patient, width = .3)
            plt.ylabel("Male Patients")
            plt.xlabel("Diseases")
            plt.title("Number Of Male Patients In Each Disease")
            plt.show()

        # Graph for spcialists
        elif choice == "3":

            # Fetching data for graph
            query = """select specialist,count(specialist) from doctor_record group by specialist"""

            db_cursor.execute(query,)
            results = db_cursor.fetchall()
            
            # Creating empty list to store data
            field = []
            number = []
            
            for result in results:
                field.append(result[0])
                number.append(result[1])

            # Plotting the graph
            plt.bar(field, number, width = .3)
            plt.xlabel("Various Fields of Specialisation")
            plt.ylabel("Number of Doctors")            
            plt.title("Number Of Specialists In Different Fields")
            plt.show()

        # Graph for staff members in various roles
        elif choice == "4":

            # Fetching data for graph
            query = """select role, count(role) from staff_record group by role"""

            db_cursor.execute(query,)
            results = db_cursor.fetchall()
            
            # Creating empty list to store data
            role = []
            number = []
            
            for result in results:
                role.append(result[0])
                number.append(result[1])

            # Plotting the graph
            plt.bar(role, number, width = .3)
            plt.xlabel("Various Roles")
            plt.ylabel("Number of Staff members")            
            plt.title("Number Of Staff Members In Different Categories")
            plt.show()

        # If user enters invalid choice
        else:
            print("\n| Error: There is no such option. |")
    
# Initialise the application
init()
