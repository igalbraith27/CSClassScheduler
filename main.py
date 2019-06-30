class Course:
    def __init__(self, score, unitCount, id, name):
        self.score = score
        self.unitCount = unitCount
        self.id = id
        self.name = name


class Semester:
    def __init__(self, coursesLst, id):
        self.coursesLst = coursesLst
        self.id = id

    def populate(self, courses):
        self.coursesLst += courses


class Schedule:
    def __init__(self, graph):
        self.g = graph
        # Generate schedule here
        semesters_list = []
        for x in range(8):
            s = Semester([], x)
            semesters_list += s
            self.gen_semester(s)

    def get_classes_taken(self, semester):
        classes = []
        for sem in self.semesterLst:
            if sem.id < semester.id:
                classes += sem.classes
        return classes

    def gen_courses(self):
        courses = []
        courses += [Course(6, 4, 0, 'cs61a')]
        courses += [Course(5, 4, 1, 'cs61b')]
        courses += [Course(7, 4, 2, 'cs61c')]
        courses += [Course(9, 4, 3, 'cs70')]
        courses += [Course(6, 4, 4, 'cs161')]
        courses += [Course(8, 4, 5, 'cs170')]
        courses += [Course(8, 4, 6, 'cs162')]
        courses += [Course(6, 4, 7, 'cs188')]
        courses += [Course(6, 4, 8, 'cs186')]
        courses += [Course(1, 4, 9, 'data8')]
        return courses

    def gen_semester(self, semester):
        all_courses = self.gen_courses()

        classes_taken = self.get_classes_taken(semester)

        # Get classes that have not yet been taken
        possible_classes = all_courses - classes_taken

        # Get classes that you have taken prerequisites for
        eligible_classes = []
        for course in possible_classes:
            if self.g.check_eligible(classes_taken, course):
                eligible_classes += [course]

        semester.populate(eligible_classes[:4])


class Graph:
    def __init__(self, courses, edges):
        self.courses = courses
        self.edges = edges

    def add_dependency(self, prereq, course):
        self.edges[course] += [prereq]

    def check_dependency(self, prereq, course):
        # Self.edges[course] returns the prerequisites of a course
        return prereq in self.edges[course]

    def check_eligible(self, taken, course):
        prereqs = self.edges[course]
        for takenCourse in taken:
            if takenCourse in prereqs:
                prereqs.remove(takenCourse)
        if prereqs:
            return False
        return True
