CREATE TABLE Course(
id INTEGER PRIMARY KEY NOT NULL,
name TEXT NOT NULL,
start_date date NOT NULL,
end_date date NOT NULL,
lectures_number integer);

INSERT INTO Course(name, start_date, end_date, lectures_number) VALUES
('Python Course', '2021-04-30', '2021-07-30', 30),
('Java Course', '2021-05-05', '2021-07-25', 28),
('DevOps Course', '2021-06-05', '2021-08-25', 32),
('Big Data Course', '2021-06-05', '2021-09-25', 30),
('C# Course', '2021-05-05', '2021-07-25', 28)