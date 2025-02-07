import pymssql
from enum import Enum
import utils.encryption as encrypt

class Database:
    def __init__(self, server, username, password, database):
        self._conn = pymssql.connect(server, username, password, database)
        self._cursor = self._conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.rollback()
        else:
            self.close(commit=True)

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()
        self.close(commit=False)  # Close the connection without committing changes

    def close(self, commit=True):
        if commit:
            self.commit()
        self.connection.close()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchall()

    def queryone(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchone()

    def fetch_all_user_data(self, email):
        sql = "SELECT * FROM SEBN_ES.Users WHERE Email = %s"
        return self.queryone(sql, (email,))
    
    def select_user_cost_center(self, email):
        sql = "SELECT CostCenter FROM SEBN_ES.Users WHERE Email = %s"
        return self.queryone(sql, (email,))
    
    def select_user_working_hours(self, email):
        sql = "SELECT WorkingHours FROM SEBN_ES.Users WHERE Email = %s"
        return self.queryone(sql, (email,))
    
    def update_user_data(self, full_name, email, city, position, department, sub_department, cost_center, working_hours, tech_responsible, travel_responsible):
        sql = "UPDATE SEBN_ES.Users SET FullName = %s, City = %s, Position = %s, Department = %s, SubDepartment = %s, CostCenter = %s, WorkingHours = %s, TechResponsible = %s, TravelResponsible = %s WHERE Email = %s"
        self.execute(sql, (full_name, city, position, department, sub_department, cost_center, working_hours, tech_responsible, travel_responsible, email))

    def fetch_login_data_by_email(self, email):
        sql = "SELECT HashPassword, SaltPassword FROM SEBN_ES.Users WHERE Email = %s"
        return self.queryone(sql, (email,))

    def fetch_user_calendar_data_day_by_day(self, email):
        sql = "SELECT * FROM SEBN_ES.Dias_Calendar Where Email = %s"
        return self.query(sql, (email,))

    def fetch_user_calendar_data_log(self, email):
        sql = "SELECT * FROM SEBN_ES.LOG_Calendar Where Email = %s"
        return self.query(sql, (email,))

    def update_password(self, email, password):
        hashed_password, salt = encode_password(password)
        sql = "UPDATE SEBN_ES.Users SET HashPassword = %s, SaltPassword = %s WHERE Email = %s"
        self.execute(sql, (hashed_password, salt, email))

    def add_festivity(self, city, date):
        sql = "INSERT INTO SEBN_ES.BankHolidays (City,Date) VALUES (%s,%s)"
        self.execute(sql, (city, date))

    def select_festivities(self):
        sql = "SELECT * FROM SEBN_ES.BankHolidays ORDER BY Date DESC"
        return self.query(sql)

    def select_festivity_by_user(self, email):
        sql = "SELECT * FROM SEBN_ES.BankHolidays WHERE City IN ( SELECT City FROM SEBN_ES.Users WHERE Email = %s )"
        return self.query(sql, (email,))

    def delete_festivity(self, id):
        sql = "DELETE FROM SEBN_ES.BankHolidays WHERE ID = %s"
        self.execute(sql, (id))
        affected_rows = self.cursor.rowcount  # Get the number of affected rows
        return affected_rows

    def select_festivity(self, city, date):
        sql = "SELECT * FROM SEBN_ES.BankHolidays WHERE City = %s AND Date = %s"
        return self.query(sql, (city, date))

    def select_city_days(self):
        sql = "SELECT * FROM SEBN_ES.CityVacationDays"
        return self.query(sql)
    
    def add_city_days(self, year, city, days):
        sql = "INSERT INTO SEBN_ES.CityVacationDays (Year,City,VacationDays) VALUES (%s,%s,%s)"
        self.execute(sql, (year, city, days))
        
    def remove_city_days_year(self, year):
        sql = "DELETE FROM SEBN_ES.CityVacationDays WHERE Year = %s"
        self.execute(sql, year)
    
    def select_city_vacation_days_cur_year(self):
        sql = "SELECT * FROM SEBN_ES.CityVacationDays WHERE Year = YEAR(GETDATE())"
        return self.query(sql)

    def add_log_calendar_request(self, email, entry_date, start_day, finishing_day, partial_day, status, total_quantity):
        sql = "INSERT INTO SEBN_ES.LogCalendarRequest (UserEmail,EntryDate,StartingDay,FinishingDay,PartialDay,Status,TotalQuantity) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        self.execute(sql, (email, entry_date, start_day, finishing_day, partial_day, status, total_quantity))

    def select_last_user_calendar_request(self, email):
        sql = "SELECT id FROM SEBN_ES.LogCalendarRequest WHERE UserEmail = %s AND id = (SELECT MAX(id) FROM SEBN_ES.LogCalendarRequest)"
        return self.query(sql, email)

    def add_calendar_data_bulk(self, id_request, day, partial_day, bucket, quantity):
        sql = "INSERT INTO SEBN_ES.CalendarDataBulk (idRequest,Day,PartialDay,Bucket,Quantity) VALUES (%s,%s,%s,%s,%s)"
        self.execute(sql, (id_request, day, partial_day, bucket, quantity))

    def get_user_days(self, email):
        sql = "SELECT * FROM SEBN_ES.UserDays WHERE UserEmail = %s"
        return self.queryone(sql, email)

    def get_single_user_days(self, type, email):
        sql = f"SELECT {type} FROM SEBN_ES.UserDays WHERE UserEmail = %s"
        return self.query(sql, email)

    def update_user_days(self, extra_hours, holidays, liq_travel, email):
        sql = "UPDATE SEBN_ES.UserDays SET ExtraHours = %s, Holidays = %s, LiqTravel = %s WHERE UserEmail = %s"
        self.execute(sql, (extra_hours, holidays, liq_travel, email))

    def select_holiday_request_range(self, email, starting_day, finishing_day):
        sql = "SELECT COUNT(*) FROM SEBN_ES.LogCalendarRequest WHERE Status != 'DELETED' AND UserEmail = %s AND (StartingDay BETWEEN %s AND %s OR FinishingDay BETWEEN %s AND %s)"
        result = self.query(sql, (email, starting_day, finishing_day, starting_day, finishing_day))
        return result[0][0] if result else 0

    def get_user_holidays(self, email):
        sql = "SELECT * FROM SEBN_ES.LogCalendarRequest WHERE UserEmail = %s AND Status != 'DELETED'" #AND Status != 'REJECTED'"
        return self.query(sql, email)
    
    def add_travel_request(self, id, user_email, destination, address, date_from, date_to, day_amount, cost_center, added_value, advance_payment, advance_payment_amount,reason, transport, extra_documentation):        
        sql_travel = "INSERT INTO SEBN_ES.TravelRequest (Id, User_Email, Destination, Address, Date_From, Date_To, Day_Amount, Cost_Center, Added_Value, Advance_Payment, Advance_Payment_Amount, Reason, Transport, Extra_Documentation) VALUES (%s,%s,%s,%s,%s,%s, %s,%s, %s, %s, %s, %s, %s, %s)"
        self.execute(sql_travel, (id, user_email, destination, address, date_from, date_to, day_amount, cost_center, added_value, advance_payment, advance_payment_amount,reason, transport, extra_documentation))
    
    def edit_travel_request_details(self, id, destination, address, date_from, date_to, day_amount, cost_center, added_value, advance_payment, advance_payment_amount,reason, transport, extra_documentation):
        sql = "UPDATE SEBN_ES.TravelRequest SET Destination = %s, Address = %s, Date_From = %s, Date_To = %s, Day_Amount = %s, Cost_Center = %s, Added_Value = %s, Advance_Payment = %s, Advance_Payment_Amount = %s, Reason = %s, Transport = %s, Extra_Documentation = %s WHERE Id = %s"
        self.execute(sql, (destination, address, date_from, date_to, day_amount, cost_center, added_value, advance_payment, advance_payment_amount, reason, transport, extra_documentation, id))
        
    def select_travels_by_user(self, email): 
        sql = "SELECT * FROM SEBN_ES.TravelRequest WHERE User_Email = %s AND Status != 'DELETED'"
        return self.query(sql, (email,)) 
    
    def select_travel_by_id(self, travel_id): 
        sql = "SELECT * FROM SEBN_ES.TravelRequest WHERE Id = %s"
        return self.query(sql, (travel_id)) 
    
    def get_last_travel_id(self):
        sql = "SELECT MAX(Id) FROM SEBN_ES.TravelRequest"
        return self.queryone(sql) 
    
    def change_travel_status(self, status, travel_id):
        sql = "UPDATE SEBN_ES.TravelRequest SET Status = %s WHERE Id = %s"
        self.execute(sql, (status, travel_id))
    
    def change_travel_documentation(self, extra_documentation, travel_id):
        sql = "UPDATE SEBN_ES.TravelRequest SET Extra_Documentation = %s WHERE Id = %s"
        self.execute(sql, (extra_documentation, travel_id))

    def sign_travel_responsible(self, responsible, travel_id):
        sql = "UPDATE SEBN_ES.TravelRequest SET Responsible_Signature = %s WHERE Id = %s"
        self.execute(sql, (responsible, travel_id))
        
    def sign_travel_management(self, management, travel_id):
        sql = "UPDATE SEBN_ES.TravelRequest SET Management_Signature = %s WHERE Id = %s"
        self.execute(sql, (management, travel_id))

    def select_user_calendar_data_bulk(self, id):
        sql = "SELECT Bucket, Quantity FROM SEBN_ES.CalendarDataBulk WHERE idRequest = %s"
        return self.query(sql, id)
    
    def select_user_holidays_dates_bucket_status(self, email):
        sql = "SELECT cdb.Day, cdb.Bucket, lcr.Status FROM SEBN_ES.CalendarDataBulk cdb JOIN SEBN_ES.LogCalendarRequest lcr ON cdb.idRequest = lcr.id WHERE lcr.UserEmail = %s"
        return self.query(sql, email)
    
    def select_user_holidays_used_cur_year(self, email): #counts amount of CREATED and SIGNED vacations in the current year
        sql = "SELECT * FROM SEBN_ES.LogCalendarRequest WHERE UserEmail = %s AND Status != 'DELETED' AND Status != 'REJECTED' AND YEAR(StartingDay) = YEAR(GETDATE())" 
        return self.query(sql, email)

    def add_user_days_on_delete(self, extra_hours, holidays, liq_travel, email):
        sql = "UPDATE SEBN_ES.UserDays SET ExtraHours = ExtraHours + %s, Holidays = Holidays + %s, LiqTravel = LiqTravel + %s WHERE UserEmail = %s"
        self.execute(sql, (extra_hours, holidays, liq_travel, email))

    def delete_calendar_data_bulk(self, id):
        sql = "DELETE FROM SEBN_ES.CalendarDataBulk WHERE idRequest = %s"
        self.execute(sql, id)

    def change_holiday_status(self, status, id):
        sql = "UPDATE SEBN_ES.LogCalendarRequest SET Status = %s WHERE id = %s"
        self.execute(sql, (status, id))

    def get_users_below(self, email):
        sql = "SELECT * FROM SEBN_ES.Users WHERE TechResponsible = %s OR TravelResponsible = %s"
        results = self.query(sql, (email, email))
        employees = [{'FullName': row[0], 'Email': row[1], 'TechResponsible': row[5], 'TravelResponsible': row[6]} for row in results]
        return employees
    
    def get_responsible_has_unsigned(self, email):
        sql = "SELECT us.Email FROM SEBN_ES.Users us WHERE (TechResponsible = %s AND (SELECT COUNT(*) FROM SEBN_ES.LogCalendarRequest WHERE UserEmail = us.Email AND Status = 'CREATED') > 0 ) OR (TravelResponsible = %s AND (SELECT COUNT(*) FROM SEBN_ES.TravelRequest WHERE User_Email = us.Email AND Status = 'CREATED' AND Responsible_Signature is null) > 0)"
        return self.query(sql, (email, email))

    def get_current_user_rank(self, email):
        sql = "SELECT CAST(CASE WHEN Position = 'Internship' AND Currently_Working = 1 THEN 'xfapochizfrtv05ikicmqbb4y4ld5415jhwg7yk81fzbh6paw122sc06t6i70fpl' ELSE 'ac2de5774e07ee521327aff50b5a00b41b3c3d2dc8ddfa833db2ebd5a30eaff3' END AS varchar(64)) as 'isIntern',CAST(CASE WHEN ((SELECT COUNT(*) as Responsible FROM SEBN_ES.Users WHERE TechResponsible = %s OR TravelResponsible = %s) > 0) AND Currently_Working = 1 THEN 'e7698668c7a6762266de376ce96adbea6e2cc5cd203bad0adb4e1832480b784b' ELSE 'ac2de5774e07ee521327aff50b5a00b41b3c3d2dc8ddfa833db2ebd5a30eaff3' END AS varchar(64) ) as 'isResponsible', CAST(CASE WHEN (Admin = 1 AND Currently_Working = 1) OR ((Department = 'CHR' OR Department = 'PHR') AND Currently_Working = 1) THEN 'cb88dfe7c01e300d2be5b0368f2e50895dd181601a7d31e61bfd7e597f7ef127' ELSE 'ac2de5774e07ee521327aff50b5a00b41b3c3d2dc8ddfa833db2ebd5a30eaff3' END AS varchar(64) ) as 'isAdmin', CAST(CASE WHEN Position = 'Manager' AND Currently_Working = 1 THEN '38ovzt6htlz9dvkfpb6gdidjlt2zkxsue4q39wfehxlp7ykhjrp75hmk954spu0n' ELSE 'ac2de5774e07ee521327aff50b5a00b41b3c3d2dc8ddfa833db2ebd5a30eaff3' END AS varchar(64) ) as 'isManager' FROM SEBN_ES.Users WHERE Email = %s"
        return self.queryone(sql, (email, email, email))
    
    def get_user_boss(self, email):
        sql = "SELECT TechResponsible FROM SEBN_ES.Users WHERE Email = %s"
        return self.query(sql, email)
    
    def get_user_travel_responsible(self, email):
        sql = "SELECT TravelResponsible FROM SEBN_ES.Users WHERE Email = %s"
        return self.query(sql, email)
    
    #TODO: REMOVE TESTING CASE from query
    def get_user_manager(self, email):
        sql = "SELECT (SELECT CASE WHEN up.Abigail = 1 THEN 'abigail.noain@sebn.com' WHEN up.Burkhard = 1 THEN 'burkhard.gesenhues-huebenthal@sebn.com' WHEN up.Ruediger = 1 THEN 'ruediger.rensch@sebn.com' WHEN up.Testing = 1 THEN 'testing.manager@sebn.com' ELSE null END ) AS 'Manager' FROM SEBN_ES.Users us JOIN SEBN_ES.UpperManagement up ON us.Email = up.UserEmail WHERE us.Email =  %s" 
        return self.query(sql, email)
    
    #TODO: borrar lo de testing del case!!!
    def get_manager_users_below(self, email):
        sql = "SELECT * FROM (SELECT us.FullName, us.Email, us.Department, (SELECT CASE WHEN up.Abigail = 1 THEN 'abigail.noain@sebn.com' WHEN up.Burkhard = 1 THEN 'burkhard.gesenhues-huebenthal@sebn.com' WHEN up.Ruediger = 1 THEN 'ruediger.rensch@sebn.com' WHEN up.Testing = 1 THEN 'testing.manager@sebn.com' ELSE null END) AS 'Manager' FROM SEBN_ES.Users us JOIN SEBN_ES.UpperManagement up ON us.Email = up.UserEmail) user_managers WHERE user_managers.Manager = %s"
        results = self.query(sql, email)
        employees = [{'FullName': row[0], 'Email': row[1], 'Department': row[2]} for row in results]
        return employees
    
    #TODO: borrar lo de testing del case!!!
    def get_manager_has_unsigned(self, email):
        sql = "SELECT Email FROM (SELECT us.Email as Email,(SELECT CASE WHEN up.Abigail = 1 THEN 'abigail.noain@sebn.com' WHEN up.Burkhard = 1 THEN 'burkhard.gesenhues-huebenthal@sebn.com' WHEN up.Ruediger = 1 THEN 'ruediger.rensch@sebn.com' WHEN up.Testing = 1 THEN 'testing.manager@sebn.com' ELSE null END) AS 'Manager' FROM SEBN_ES.Users us JOIN SEBN_ES.UpperManagement up ON us.Email = up.UserEmail) user_managers WHERE user_managers.Manager = %s AND ((SELECT COUNT(*) FROM SEBN_ES.TravelRequest WHERE User_Email = user_managers.Email AND Status = 'CREATED' AND Management_Signature is null AND Responsible_Signature is not null) > 0)"
        return self.query(sql, email)
    
    def get_all_managers(self):
        sql = "SELECT c.name AS COLUMN_NAME FROM sys.columns c WHERE c.object_id = OBJECT_ID('SEBN_ES.UpperManagement') AND c.name NOT IN ('UserEmail', 'CurrentlyWorking', 'Testing')" #TODO: FILTER THE TESTING MANAGER! --> DELETE WHEN testing manager REMOVED
        return self.query(sql)

    def get_user_info(self, email):
        sql = "SELECT * FROM SEBN_ES.Users WHERE Email = %s"
        return self.query(sql, email)

    def get_users(self):
        sql = "SELECT * FROM SEBN_ES.Users WHERE Currently_Working = 1"
        return self.query(sql)
    
    def get_users_name_mail(self):
        sql = "SELECT FullName, Email, Department, City, CostCenter FROM SEBN_ES.Users WHERE Currently_Working = 1"
        return self.query(sql)
    
    def get_all_existing_users(self):
        sql = "SELECT FullName, Email FROM SEBN_ES.Users"
        return self.query(sql)
    
    def get_users_in_city(self, city):
        sql = "SELECT FullName, Email FROM SEBN_ES.Users WHERE City = %s AND Currently_Working = 1"
        return self.query(sql, city)

    def get_logs(self):
        sql = "SELECT * FROM SEBN_ES.LogCalendarRequest ORDER BY EntryDate DESC"
        return self.query(sql)

    def get_hr_logs(self):
        sql = "SELECT * FROM SEBN_ES.LogCalendarRRHH ORDER BY EntryDate DESC"
        return self.query(sql)

    def create_hr_logs(self, email, entry_date, bucket, quantity):
        sql = "INSERT INTO SEBN_ES.LogCalendarRRHH (UserEmail,EntryDate,Bucket,Quantity) VALUES (%s,%s,%s,%s)"
        self.execute(sql, (email, entry_date, bucket, quantity))

    def get_departments(self):
        sql = "SELECT * FROM SEBN_ES.Departments"
        return self.query(sql)
    
    def get_sub_departments(self):
        sql = "SELECT * FROM SEBN_ES.DepartmentsSub"
        return self.query(sql)

    def create_user(self, full_name, email, department, sub_department, cost_center, working_hours, position, tech_responsible, travel_responsible, city,hash_password, salt_password):
        sql = "INSERT INTO SEBN_ES.Users (FullName,Email,Department,SubDepartment,CostCenter,WorkingHours,Position,TechResponsible,TravelResponsible,City,Admin,Currently_Working, HashPassword,SaltPassword) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        self.execute(sql, (full_name, email, department, sub_department, cost_center, working_hours, position, tech_responsible, travel_responsible, city, 0, 1, hash_password, salt_password))
        
    def delete_user(self, email):
        sql = "UPDATE SEBN_ES.Users SET Currently_Working = 0 WHERE Email = %s; UPDATE SEBN_ES.UserDays SET CurrentlyWorking = 0 WHERE UserEmail = %s; UPDATE SEBN_ES.UpperManagement SET CurrentlyWorking = 0 WHERE UserEmail = %s;"
        self.execute(sql, (email, email, email)) 

    def create_user_days(self, email, holidays):
        sql = "INSERT INTO SEBN_ES.UserDays (UserEmail,ExtraHours,Holidays,LiqTravel) VALUES (%s,0,%s,0)"
        self.execute(sql, (email, holidays))

    def get_buckets(self):
        sql = "SELECT * FROM SEBN_ES.Bucket"
        return self.query(sql)

    def create_single_user_days(self, type, quantity, email):
        sql = f"UPDATE SEBN_ES.Userdays SET {type} = {type} + %s WHERE UserEmail = %s"
        self.execute(sql, (quantity, email))

    def create_home_office(self, email, date, type):
        sql = "INSERT INTO SEBN_ES.HomeOffice (UserEmail,Date,Type) VALUES (%s,%s,%s)"
        self.execute(sql, (email, date, type))

    def delete_home_office(self, email, date):
        sql = "DELETE FROM SEBN_ES.HomeOffice WHERE UserEmail = %s AND Date = %s"
        self.execute(sql, (email, date))
        return self._cursor.rowcount

    def get_home_office(self, email):
        sql = "SELECT * FROM SEBN_ES.HomeOffice WHERE UserEmail = %s"
        return self.query(sql, email)
    
    def get_home_office_cur_month(self, email): #obtain all user home office data for current month
        sql = "SELECT * FROM SEBN_ES.HomeOffice WHERE UserEmail = %s AND MONTH(Date) = MONTH(GETDATE())"
        return self.query(sql, email)
    
    def get_all_home_office_grouped(self, starting_date, finishing_date):
        sql = "SELECT u.City, u.Department, ho.* FROM SEBN_ES.Users u JOIN SEBN_ES.HomeOffice ho ON u.Email = ho.UserEmail WHERE ho.Date BETWEEN %s AND %s ORDER BY u.City, u.Department, ho.UserEmail"
        return self.query(sql, (starting_date, finishing_date))

    def get_department_home_office(self, email):
        sql = "SELECT SEBN_ES.HomeOffice.*, SEBN_ES.Users.FullName FROM SEBN_ES.HomeOffice INNER JOIN SEBN_ES.Users ON SEBN_ES.HomeOffice.UserEmail = SEBN_ES.Users.Email WHERE SEBN_ES.Users.Department = (SELECT Department FROM SEBN_ES.Users WHERE Email = %s) AND SEBN_ES.Users.City = (SELECT City FROM SEBN_ES.Users WHERE Email = %s) and SEBN_ES.Users.Currently_Working = 1"
        return self.query(sql, (email, email))

    def get_department_partners(self, email):
        sql = "SELECT u.FullName FROM SEBN_ES.Users u JOIN SEBN_ES.Users u2 ON u.Department = u2.Department AND u.City = u2.City WHERE u2.Email = %s AND u2.Currently_Working = 1"
        return self.query(sql, email)

    def add_employee_to_manager(self, email, gerency):
        sql = f"INSERT INTO SEBN_ES.UpperManagement (UserEmail, {gerency}) VALUES (%s, %s)"
        return self.execute(sql, (email, 1))
    
    def delete_user_from_database(self, email):
        sql= "DELETE FROM SEBN_ES.UserDays WHERE UserEmail = %s;DELETE FROM SEBN_ES.UpperManagement WHERE UserEmail = %s;DELETE FROM SEBN_ES.TravelRequest WHERE User_Email = %s;DELETE FROM SEBN_ES.HomeOffice WHERE UserEmail = %s; DELETE FROM SEBN_ES.LogCalendarRRHH WHERE UserEmail = %s; DELETE FROM SEBN_ES.CalendarDataBulk WHERE idRequest IN (SELECT Id FROM SEBN_ES.LogCalendarRequest WHERE UserEmail = %s); DELETE FROM SEBN_ES.LogCalendarRequest WHERE UserEmail = %s; DELETE FROM SEBN_ES.Users WHERE Email = %s;"
        return self.execute(sql, (email,email,email,email,email,email,email,email))
    
    #TODO: get_vacations_data_filtered query (for hr/Reporting)
    def get_vacations_data_filtered(self, start_date, end_date):
        sql = ""
        return self.query(sql, start_date, end_date)


def encode_password(password):
    hashed_password, salt = encrypt.encrypt_password(password)
    return hashed_password, salt


def decode_password(salt_password, password):
    hashed_password = encrypt.decrypt_password(password, salt_password)
    return hashed_password


def check_password(hash_password, salt_password, password):
    return encrypt.verify_password(hash_password, salt_password, password)

class LoginStatus(Enum):
    SUCCESS = "Success"
    INCORRECT_PASSWORD = "Incorrect Password"
    USER_NOT_FOUND = "User not found"
    UNKNOWN_ERROR = "Unknown error during login"
    INVALID_USER_DATA = "Internal error. Contact SCA"
