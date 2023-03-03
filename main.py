from functools import total_ordering


@total_ordering
class Student:

    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_lecturer(self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer) and course in lecturer.courses_attached and \
                (course in self.finished_courses or course in self.courses_in_progress) and \
                type(grade) is int and 0 <= grade <= 10:
            if course in lecturer.grades.keys():
                lecturer.grades[course].append(grade)
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'error'

    def grades_average(self):
        if self.grades:
            return sum(sum(i) for i in self.grades.values()) / sum(len(i) for i in self.grades.values())
        return 'no current grades'

    def __str__(self):
        return f'name - {self.name}\n' \
               f'surname - {self.surname}\n' \
               f'average grade - {self.grades_average()}\n' \
               f'courses in progress - ' \
               f'{", ".join(self.courses_in_progress) if self.courses_in_progress else "no courses"}\n' \
               f'finished courses - ' \
               f'{", ".join(self.finished_courses) if self.finished_courses else "no courses"}'

    def __lt__(self, other):
        if isinstance(other, Student):
            return self.grades_average() < other.grades_average()
        print('error')
        return


class Mentor:

    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


@total_ordering
class Lecturer(Mentor):

    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def grades_average(self):
        if self.grades:
            return sum(sum(i) for i in self.grades.values()) / sum(len(i) for i in self.grades.values())
        return 'no current grades'

    def __str__(self):
        return f'name - {self.name}\n' \
               f'surname - {self.surname}\n' \
               f'average grade - {self.grades_average()}'

    def __lt__(self, other):
        if isinstance(other, Lecturer):
            return self.grades_average() < other.grades_average()
        print('error')
        return


class Reviewer(Mentor):

    def __init__(self, name, surname):
        super().__init__(name, surname)

    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'error'

    def __str__(self):
        return f'name = {self.name}\n' \
               f'surname = {self.surname}'


def average_by_course_students(students, course):
    res = 0
    total_grades = 0
    for student in students:
        if isinstance(student, Student) and course in student.grades.keys():
            res += sum(student.grades[course])
            total_grades += len(student.grades[course])
        else:
            print('error')
            return
    return res / total_grades


def average_by_course_lecturers(lecturers, course):
    res = 0
    total_grades = 0
    for lecturer in lecturers:
        if isinstance(lecturer, Lecturer) and course in lecturer.grades.keys():
            res += sum(lecturer.grades[course])
            total_grades += len(lecturer.grades[course])
        else:
            print('error')
            return
    return res / total_grades


stud1 = Student('Маша', 'Иванова', 'f')
stud2 = Student('Олег', 'Петров', 'm')
lec1 = Lecturer('Иван', 'Ласточкин')
lec2 = Lecturer('Потап', 'Никитин')
rev1 = Reviewer('Федор', 'Кривозуб')
rev2 = Reviewer('Михаил', 'Бондарев')

stud1.courses_in_progress.append('python')
stud2.courses_in_progress.append('python')
rev1.courses_attached.append('python')
rev2.courses_attached.append('python')
lec1.courses_attached.append('python')
lec2.courses_attached.append('python')

rev1.rate_hw(stud1, 'python', 5)
rev2.rate_hw(stud2, 'python', 7)
stud1.rate_lecturer(lec1, 'python', 9)
stud2.rate_lecturer(lec2, 'python', 8)

print(stud1, stud2, lec1, lec2, rev1, rev2, sep='\n\n')

print(stud1 > stud2)
print(stud1 <= stud2)
print(stud1 == stud2)
print(stud1 != stud2)
print(lec1 < lec2)
print(lec1 <= lec2)
print(lec1 == lec2)
print(lec1 != lec2)

print(average_by_course_students([stud1, stud2], 'python'))
print(average_by_course_lecturers([lec1, lec2], 'python'))
