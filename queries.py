from sqlalchemy import create_engine, text
import sys

connection_string = "postgresql://postgres:123456@localhost:5432/caregiver_platform"

try:
    engine = create_engine(connection_string, echo=True)
    connection = engine.connect()
    print("Connected to the database")
except Exception as e:
    print(f"Error connecting to the database: {e}")
    sys.exit(1)

def execute_query(query, fetch=True):
    try:
        result = connection.execute(text(query))
        
        if fetch and result.returns_rows:
            setAns = result.fetchall()
            if setAns:
                print(f"\nResults:")
                for ans in setAns:
                    print(ans)
                    print("\n")
            else:
                print("Nothing here.")
        else:
            connection.commit()
            print(f"Success, nice!")
        
    except Exception as e:
        print(f"Error happened: {e}")
        connection.rollback()

drop_tables = """
DROP TABLE IF EXISTS APPOINTMENT CASCADE;
DROP TABLE IF EXISTS JOB_APPLICATION CASCADE;
DROP TABLE IF EXISTS JOB CASCADE;
DROP TABLE IF EXISTS ADDRESS CASCADE;
DROP TABLE IF EXISTS MEMBER CASCADE;
DROP TABLE IF EXISTS CAREGIVER CASCADE;
DROP TABLE IF EXISTS "USER" CASCADE;
"""
execute_query(drop_tables, fetch=False)


print("\nSECTION 1: CREATE TABLE STATEMENTS")
print("1.1: Create USER table")
create_user_table = """
create table "USER" (
	user_id serial primary key, 
	email varchar(100) not null unique, 
	given_name varchar(40) not null, 
	surname varchar(40) not null, 
	city varchar(30), 
	phone_number varchar(30), 
	profile_description text, 
	password varchar(500) not null);
"""
execute_query(create_user_table, fetch=False)

print("1.2: Create CAREGIVER table")
create_caregiver_table = """
create table Caregiver (
	caregiver_user_id integer primary key, 
	photo varchar(300),
	gender varchar (10),
	caregiving_type varchar(30) not null,
	hourly_rate decimal(10, 2) not null,
	foreign key (caregiver_user_id) references "USER" (user_id) on delete cascade);
"""
execute_query(create_caregiver_table, fetch=False)

print("1.3: Create MEMBER table")
create_member_table = """
create table MEMBER(
    member_user_id integer primary key,
    house_rules text,
    dependent_description text,
    foreign key (member_user_id) references "USER"(user_id) on delete cascade);
"""
execute_query(create_member_table, fetch=False)

print("1.4: Create ADDRESS table")
create_address_table = """
create table ADDRESS (
    member_user_id integer primary key,
    house_number varchar(30),
    street varchar(50) not null,
    town varchar(30),
    foreign key (member_user_id) references MEMBER(member_user_id) on delete cascade);
"""
execute_query(create_address_table, fetch=False)

print("1.5: Create JOB table")
create_job_table = """
create table JOB (
    job_id serial primary key,
    member_user_id integer not null,
    required_caregiving_type varchar(30) not null,
    other_requirements text,
    date_posted date not null,
    foreign key (member_user_id) references MEMBER(member_user_id) on delete cascade);
"""
execute_query(create_job_table, fetch=False)

print("1.6: Create JOB_APPLICATION table")
create_job_application_table = """
create table JOB_APPLICATION (
    caregiver_user_id integer,
    job_id integer,
    date_applied date not null,
    primary key (caregiver_user_id, job_id),
    foreign key (caregiver_user_id) references CAREGIVER(caregiver_user_id) on delete cascade,
    foreign key (job_id) references JOB(job_id) on delete cascade);
"""
execute_query(create_job_application_table, fetch=False)

print("1.7: Create APPOINTMENT table")
create_appointment_table = """
create table APPOINTMENT(
    appointment_id serial primary key,
    caregiver_user_id integer not null,
    member_user_id integer not null,
    appointment_date date not null,
    appointment_time time not null,
    work_hours decimal(5, 2) not null,
    status varchar(30) not null,
    foreign key (caregiver_user_id) references CAREGIVER(caregiver_user_id) on delete cascade,
    foreign key (member_user_id) references MEMBER(member_user_id) on delete cascade);
"""
execute_query(create_appointment_table, fetch=False)


print("\nSECTION 2: INSERT STATEMENTS")
print("2.1: Insert data into USER table")
insert_users = """
INSERT INTO "USER" (email, given_name, surname, city, phone_number, profile_description, password) VALUES
('amir.amirov@mail.com', 'Amir', 'Amirov', 'Almaty', '+77713112727', 'New in babysitting', '123123Aa!aA!'),
('aza.aza@mail.com', 'Azamat', 'Azamatov', 'Atyrau', '+77777777777', 'Experienced guy', 'VictorSecret1!'),
('aisu.maisu@mail.ru', 'Aisu', 'Maisu', 'Astana', '+78787878787', 'Yes sir', 'counterstrikyes!121'),
('aina.kotegaw@yahoo.jp', 'Aina', 'Kotegaw', 'Astana', '+77712132123', 'Fun and interesting caresitter', '321123321!aa'),
('amir.uaisov@mail.ru', 'Amir', 'Uaisov', 'Atyrau', '+29923929232', 'Proffesional caresitter', 'dota24life'),
('arman.armanov@nu.edu.kz', 'Arman', 'Armanov', 'Astana', '+77778989898', 'Interesting person', 'armanarman7sui'),
('donal.duck@google.com', 'Donald', 'Duck', 'Uralsk', '+77773212342', 'Rich guy and caresitter', 'dolladolla100000$'),
('buzz.lightyy@mks.com', 'Buzz', 'Lighty', 'Shymkent', '+78881123123', 'Cosmonavt previously', 'tothestars777suisui'),
('christiano.ronaldo@real.sp', 'Chris', 'Ron', 'Aktau', '+77777717777', 'Proffesionl fottballer', '!SUI7SUI7SUI!'),
('elon.musk@dada.com', 'Elon', 'Muskovitch', 'Talgar', '+77878181811', 'Richest caresitter you can find', 'TeslaPlusNASA111!'),
('dondonm.av@mail.com', 'Don', 'Don', 'Almaty', '+772133312427', 'New', '123123Aa!aA!sa'),
('a.a@mail.com', 'A', 'A', 'Atyrau', '+77272722727', 'Father', 'VictorSecret1!'),
('amina.amina@mail.ru', 'Amina', 'Aminova', 'Astana', '+71767$72767', 'Mother of two', 'counterstrikyes!121'),
('chisa.kotegaw@yahoo.jp', 'Chisa', 'Kotegaw', 'Astana', '+71110102023', 'Fun', 'ILOVEDIVINGyes!!'),
('Omaga.three@mail.ru', 'Omega', 'Three', 'Atyrau', '+79923729732', 'Pro', 'dota4life'),
('Hrutka.cocoa@nu.edu.kz', 'Hrutka', 'Cocoa', 'Astana', '+88881211231', 'Interesting', 'armhrutka7sui'),
('xia.dia@google.com', 'Xi', 'Di', 'Uralsk', '+77754413241', 'Rich', '187800000$'),
('Calcium.Magnesium@mks.com', 'Calcium', 'Magnesium', 'Shymkent', '+7858533213', 'Cosmo', 'tisui!11!111'),
('gon.armin@manga.jp', 'Gon', 'Armin', 'Almaty', '+9292929212', 'Strongest', 'temamatetw1112'),
('ya.ustal@mail.ru', 'Ye', 'Kanye', 'Astana', '+1233211232', 'Norm Music and father', 'helloImYe98765!');
"""
execute_query(insert_users, fetch=False)

print("2.2: Insert data into CAREGIVER table")
insert_caregivers = """
insert into caregiver (caregiver_user_id, photo, gender, caregiving_type, hourly_rate) values
(1, 'amir_photo.jpg', 'Male', 'babysitter', 8.50),
(2, 'azamat_photo.jpg', 'Male', 'elderly care', 12.00),
(3, 'aisu_photo.jpg', 'Female', 'playmate', 7.00),
(4, 'aina_photo.jpg', 'Female', 'babysitter', 9.50),
(5, 'amir_u_photo.jpg', 'Male', 'elderly care', 15.00),
(6, 'arman_photo.jpg', 'Male', 'playmate', 8.00),
(7, 'donald_photo.jpg', 'Male', 'babysitter', 11.00),
(8, 'buzz_photo.jpg', 'Male', 'elderly care', 13.50),
(9, 'chris_photo.jpg', 'Male', 'playmate', 9.00),
(10, 'elon_photo.jpg', 'Male', 'elderly care', 14.00);
"""
execute_query(insert_caregivers, fetch=False)

print("2.3: Insert data into MEMBER table")
insert_members = """
insert into member (member_user_id, house_rules, dependent_description) values
(11, 'No smoking.', '24 year old son who loves video games'),
(12, 'No pets.', '80 year old father with hearing issues'),
(13, 'No pets. No smoking.', 'Two daughters, 5 and 7 years old, very active'),
(14, 'Nothing', '6 year old daughter who loves swimming'),
(15, 'No noises pls.', '75 year old mother, needs medication reminders'),
(16, 'Clean.', '5 year old boy who enjoys painting but was rejected from getting into painting school'),
(17, 'No smoking.', '3 year old twin boys, very energetic'),
(18, 'Quiet.', '82 year old grandfather with mobility issues'),
(19, 'No pets.', '12 year old son who loves manga and sports'),
(20, 'No smoking. No pets.', '4 year old daughter, enjoys music and dancing');
"""
execute_query(insert_members, fetch=False)

print("2.4: Insert data into ADDRESS table")
insert_addresses = """
insert into address (member_user_id, house_number, street, town) values
(11, '10', 'Dostyk Plaza Burgers', 'Almaty'),
(12, '11', 'Kabanbay Batyr', 'Atyrau'),
(13, '12', 'Respublika Mega', 'Astana'),
(14, '66', 'Kabanbay Batyr', 'Astana'),
(15, '67', 'Mangilik El', 'Atyrau'),
(16, '68', 'Kabanbay Batyr', 'Astana'),
(17, '33', 'Turan', 'Uralsk'),
(18, '1', 'Kazan Street', 'Shymkent'),
(19, '2', 'Abay Elon Street', 'Almaty'),
(20, '3', 'Kosmopol Street', 'Astana');
"""
execute_query(insert_addresses, fetch=False)

print("2.5: Insert data into JOB table")
insert_jobs = """
insert into job (member_user_id, required_caregiving_type, other_requirements, date_posted) values
(11, 'babysitter', 'Good with technology and games and manga, soft-spoken preferred', '2025-10-01'),
(12, 'elderly care', 'Experience with ear issues pateints', '2025-7-02'),
(13, 'babysitter', 'Must energetic with multiple children', '2025-8-03'),
(16, 'playmate', 'Creative and active', '2025-11-04'),
(13, 'babysitter', 'Swimming pools by kendrik', '2025-9-05'),
(13, 'elderly care', 'Medical knowledge', '2025-10-06'),
(16, 'playmate', 'Artistic skills and graduation from painting school', '2025-11-07'),
(17, 'babysitter', 'Experience with piloting the f1 bolid', '2025-12-08'),
(18, 'elderly care', 'Experience with gentle approach', '2025-1-09'),
(19, 'playmate', 'Sports and fun', '2025-4-10'),
(20, 'babysitter', 'Music background', '2025-5-11'),
(20, 'elderly care', 'Patient and understanding caregiver needed', '2025-6-12');
"""
execute_query(insert_jobs, fetch=False)

print("2.6: Insert data into JOB_APPLICATION table")
insert_job_applications = """
insert into job_application (caregiver_user_id, job_id, date_applied) values
(1, 1, '2025-10-02'),
(4, 1, '2025-10-03'),
(7, 1, '2025-10-03'),
(2, 2, '2025-07-03'),
(5, 2, '2025-07-04'),
(8, 2, '2025-07-04'),
(1, 3, '2025-08-04'),
(4, 3, '2025-08-05'),
(7, 3, '2025-08-05'),
(3, 4, '2025-11-05'),
(6, 4, '2025-11-06'),
(9, 4, '2025-11-06'),
(1, 5, '2025-09-06'),
(4, 5, '2025-09-07'),
(2, 6, '2025-10-07'),
(5, 6, '2025-10-08'),
(8, 6, '2025-10-08'),
(3, 7, '2025-11-08'),
(6, 7, '2025-11-09'),
(9, 7, '2025-11-09'),
(1, 8, '2025-12-09'),
(4, 8, '2025-12-10'),
(7, 8, '2025-12-10'),
(2, 9, '2025-01-10'),
(5, 9, '2025-01-11'),
(3, 10, '2025-04-11'),
(9, 10, '2025-04-12'),
(6, 11, '2025-05-12');
"""
execute_query(insert_job_applications, fetch=False)

print("2.7: Insert data into APPOINTMENT table")
insert_appointments = """
insert into appointment (caregiver_user_id, member_user_id, appointment_date, appointment_time, work_hours, status) values
(1, 11, '2025-11-22', '09:00:00', 3.0, 'accepted'),
(2, 12, '2025-11-23', '10:00:00', 4.0, 'accepted'),
(3, 16, '2025-11-24', '14:00:00', 2.0, 'accepted'),
(4, 13, '2025-11-24', '08:00:00', 5.0, 'accepted'),
(5, 15, '2025-11-24', '13:00:00', 3.5, 'accepted'),
(6, 16, '2025-11-23', '09:00:00', 4.0, 'accepted'),
(7, 17, '2025-11-25', '15:00:00', 2.5, 'pending'),
(8, 18, '2025-11-23', '10:00:00', 3.0, 'accepted'),
(9, 19, '2025-11-23', '11:00:00', 4.5, 'accepted'),
(10, 15, '2025-11-24', '14:00:00', 3.0, 'declined'),
(1, 20, '2025-11-25', '09:30:00', 2.0, 'accepted'),
(2, 18, '2025-11-26', '10:00:00', 4.0, 'pending'),
(4, 11, '2025-11-27', '08:30:00', 3.0, 'accepted');
"""
execute_query(insert_appointments, fetch=False)


print("\nSECTION 3: UPDATE STATEMENTS")
print("3.1: Arman Armanov's phone number updated to +77773414141")
query_3_1 = """
UPDATE "USER"
SET phone_number = '+77773414141'
WHERE given_name = 'Arman' AND surname = 'Armanov';
"""
execute_query(query_3_1, fetch=False)

print("3.2: Add $0.3 commission if rate < $10, or 10% if rate >= $10")
query_3_2 = """
UPDATE caregiver
SET hourly_rate = hourly_rate + 0.3
WHERE hourly_rate < 10;

UPDATE caregiver
SET hourly_rate = hourly_rate * 1.10
WHERE hourly_rate >= 10;
"""
execute_query(query_3_2, fetch=False)



print("\nSECTION 4: DELETE STATEMENTS")
print("4.1: Delete jobs posted by Amina Aminova")
query_4_1 = """
DELETE FROM job
WHERE member_user_id IN (
    SELECT user_id
    FROM "USER"
    WHERE given_name = 'Amina' AND surname = 'Aminova');
"""
execute_query(query_4_1, fetch=False)

print("4.2: Delete members who live on Kabanbay Batyr street")
query_4_2 = """
DELETE FROM member
WHERE member_user_id IN (
    SELECT member_user_id 
    FROM address 
    WHERE street = 'Kabanbay Batyr');
"""
execute_query(query_4_2, fetch=False)



print("\nVERIFICATION QUERIES")
print("Verification: Check Arman's new phone number")
verify_3_1 = """
SELECT given_name, surname, phone_number 
FROM "USER" 
WHERE given_name = 'Arman' AND surname = 'Armanov';
"""
execute_query(verify_3_1)

print("Verification: Check updated hourly rates")
verify_3_2 = """
SELECT caregiver_user_id, hourly_rate 
FROM caregiver 
ORDER BY caregiver_user_id;
"""
execute_query(verify_3_2)

print("Verification: Check if Amina's jobs are deleted")
verify_4_1 = """
SELECT j.job_id, u.given_name, u.surname 
FROM job j
JOIN member m ON j.member_user_id = m.member_user_id
JOIN "USER" u ON m.member_user_id = u.user_id
WHERE u.given_name = 'Amina' AND u.surname = 'Aminova';
"""
execute_query(verify_4_1)

print("Verification: Check if members on Kabanbay Batyr are deleted")
verify_4_2 = """
SELECT m.member_user_id, u.given_name, u.surname, a.street
FROM member m
JOIN "USER" u ON m.member_user_id = u.user_id
LEFT JOIN address a ON m.member_user_id = a.member_user_id
WHERE a.street = 'Kabanbay Batyr' OR a.street IS NULL;
"""
execute_query(verify_4_2)



print("\nSECTION 5: SIMPLE QUERIES")
print("5.1: Caregiver and member names for accepted appointments")
query_5_1 = """
SELECT 
    uCare.given_name AS caregiver_name,
    uCare.surname AS caregiver_surname,
    uMember.given_name AS member_name,
    uMember.surname AS member_surname
FROM appointment a
JOIN caregiver c ON a.caregiver_user_id = c.caregiver_user_id
JOIN "USER" uCare ON c.caregiver_user_id = uCare.user_id
JOIN member m ON a.member_user_id = m.member_user_id
JOIN "USER" uMember ON m.member_user_id = uMember.user_id
WHERE a.status = 'accepted';
"""
execute_query(query_5_1)


print("5.2: Job IDs that contain 'soft-spoken' in requirements")
query_5_2 = """
SELECT job_id
FROM job
WHERE other_requirements ILIKE '%soft-spoken%';
"""
execute_query(query_5_2)


print("5.3: Work hours of all babysitter positions")
query_5_3 = """
SELECT 
    a.appointment_id,
    c.caregiver_user_id,
    a.work_hours
FROM appointment a
JOIN caregiver c ON a.caregiver_user_id = c.caregiver_user_id
WHERE c.caregiving_type = 'babysitter';
"""
execute_query(query_5_3)


print("5.4: Members looking for Elderly Care in Astana with 'No pets' rule")
query_5_4 = """
SELECT DISTINCT
    u.user_id,
    u.given_name,
    u.surname,
    u.city,
    m.house_rules,
    j.required_caregiving_type
FROM member m
JOIN "USER" u ON m.member_user_id = u.user_id
JOIN job j ON m.member_user_id = j.member_user_id
WHERE u.city = 'Astana' 
    AND m.house_rules ILIKE '%No pets%'
    AND j.required_caregiving_type = 'elderly care';
"""
execute_query(query_5_4)

print("\nSECTION 6: COMPLEX QUERIES")
print("6.1: Count the number of applicants for each job posted by a member)")
query_6_1 = """
SELECT 
    u.given_name AS member_name,
    u.surname AS member_surname,
    j.job_id,
    j.required_caregiving_type,
    COUNT(ja.caregiver_user_id) AS applicant_count
FROM job j
JOIN member m ON j.member_user_id = m.member_user_id
JOIN "USER" u ON m.member_user_id = u.user_id
LEFT JOIN job_application ja ON j.job_id = ja.job_id
GROUP BY j.job_id, j.required_caregiving_type, u.given_name, u.surname
ORDER BY applicant_count DESC;
"""
execute_query(query_6_1)



print("6.2: Total hours spent by care givers for accepted appointments")
query_6_2 = """
SELECT 
    u.given_name,
    u.surname,
    c.caregiving_type,
    SUM(a.work_hours) AS total_hours_spent
FROM caregiver c
JOIN "USER" u ON c.caregiver_user_id = u.user_id
JOIN appointment a ON c.caregiver_user_id = a.caregiver_user_id
WHERE a.status = 'accepted'
GROUP BY c.caregiver_user_id, u.given_name, u.surname, c.caregiving_type
ORDER BY total_hours_spent DESC;
"""
execute_query(query_6_2)


print("6.3: Average pay of caregivers based on accepted appointments")
query_6_3 = """
SELECT 
    u.given_name,
    u.surname,
    c.hourly_rate,
    AVG(a.work_hours * c.hourly_rate) AS avg_payment_per_appointment
FROM caregiver c
JOIN "USER" u ON c.caregiver_user_id = u.user_id
JOIN appointment a ON c.caregiver_user_id = a.caregiver_user_id
WHERE a.status = 'accepted'
GROUP BY c.caregiver_user_id, u.given_name, u.surname, c.hourly_rate
ORDER BY avg_payment_per_appointment DESC;
"""
execute_query(query_6_3)


print("6.4: Caregivers who earn above average based on accepted appointments")
query_6_4 = """
SELECT 
    u.given_name,
    u.surname,
    c.caregiving_type,
    SUM(a.work_hours * c.hourly_rate) AS total_earnings
FROM caregiver c
JOIN "USER" u ON c.caregiver_user_id = u.user_id
JOIN appointment a ON c.caregiver_user_id = a.caregiver_user_id
WHERE a.status = 'accepted'
GROUP BY c.caregiver_user_id, u.given_name, u.surname, c.caregiving_type
HAVING SUM(a.work_hours * c.hourly_rate) > (
    SELECT AVG(total_earnings)
    FROM (
        SELECT SUM(a2.work_hours * c2.hourly_rate) AS total_earnings
        FROM caregiver c2
        JOIN appointment a2 ON c2.caregiver_user_id = a2.caregiver_user_id
        WHERE a2.status = 'accepted'
        GROUP BY c2.caregiver_user_id
    ) AS earnings_subquery
)
ORDER BY total_earnings DESC;
"""
execute_query(query_6_4)



print("\nSECTION 7: QUERY WITH DERIVED ATTRIBUTE")
print("7: Calculate total cost for all accepted appointments (derived attribute)")
query_7 = """
SELECT 
    uCare.given_name AS caregiver_name,
    uCare.surname AS caregiver_surname,
    uMember.given_name AS member_name,
    uMember.surname AS member_surname,
    (a.work_hours * c.hourly_rate) AS total_cost
FROM appointment a
JOIN caregiver c ON a.caregiver_user_id = c.caregiver_user_id
JOIN "USER" uCare ON c.caregiver_user_id = uCare.user_id
JOIN member m ON a.member_user_id = m.member_user_id
JOIN "USER" uMember ON m.member_user_id = uMember.user_id
WHERE a.status = 'accepted'
ORDER BY total_cost DESC;
"""
execute_query(query_7)



print("\nSECTION 8: VIEW OPERATION")
print("8.1: Create view for job applications")
create_view = """
CREATE OR REPLACE VIEW job_applications_view AS
SELECT 
    ja.job_id,
    j.required_caregiving_type,
    j.other_requirements,
    j.date_posted,
    uMember.given_name AS member_name,
    uMember.surname AS member_surname,
    ja.caregiver_user_id,
    uCare.given_name AS applicant_name,
    uCare.surname AS applicant_surname,
    c.caregiving_type AS applicant_caregiving_type,
    c.hourly_rate,
    ja.date_applied
FROM job_application ja
JOIN job j ON ja.job_id = j.job_id
JOIN member m ON j.member_user_id = m.member_user_id
JOIN "USER" uMember ON m.member_user_id = uMember.user_id
JOIN caregiver c ON ja.caregiver_user_id = c.caregiver_user_id
JOIN "USER" uCare ON c.caregiver_user_id = uCare.user_id
ORDER BY ja.date_applied DESC;
"""
execute_query(create_view, fetch=False)



print("8.2: Query the job_applications_view")
query_view = """
SELECT * FROM job_applications_view
LIMIT 10;
"""
execute_query(query_view)

connection.close()
print("\nDatabase connection closed")