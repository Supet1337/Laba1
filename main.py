# -*- coding: cp1251 -*-

import json
import os
import re
import xml.etree.ElementTree as ET
from xml.dom import minidom


class Student:
    _name = ''
    _surname = ''
    _studentID = 0

    def name(self):
        return "student"

    def setName(self, name):
        self._name = name

    def setSurname(self, surname):
        self._surname = surname

    def setID(self, id : int):
        self._studentID = id

    def getName(self):
        return self._name

    def getSurname(self):
        return self._surname

    def getID(self):
        return self._studentID

class Tutor:
    _name = ''
    _surname = ''
    _patronymic = ''
    _tutorID = 0

    def name (self):
        return "tutor"

    def setName(self, name):
        self._name = name

    def setSurname(self, surname):
        self._surname = surname

    def setPatronymic(self, patronymic):
        self._patronymic = patronymic

    def setID(self, id):
        self._tutorID = id

    def getName(self):
        return self._name

    def getSurname(self):
        return self._surname

    def getPatronymic(self):
        return self._patronymic

    def getID(self):
        return self._tutorID

class Cathedra:
    _studentList = []
    _tutorList = []
    _studTutorMap = {}

    def addStudent(self, student):
        if student.name() == "student":
            self._studentList.append(student)
        else:
            print("Не тот класс")

    def addTutor(self, tutor):
        if tutor.name() == "tutor":
            self._tutorList.append(tutor)
        else:
            print("Не тот класс")

    def gettutorbyID(self, id):
        for tutor in self._tutorList:
            if int(tutor.getID()) == int(id):
                return tutor

    def getstudentbyID(self, id):
        for student in self._studentList:
            if int(student.getID()) == int(id):
                return student

    def getstudentsbyID(self, id):
        # for student in self._studTutorMap:
        #     if int(student.getID()) == int(id):
        #         return student
        students = self._studTutorMap.get(id)
        return students

    def getListStudent(self):
        listX = []
        for i in self._studentList:
            listX.append([i.getName(), i.getSurname(), i.getID()])
        return listX

    def getListTutor(self):
        listZ = []
        for i in self._tutorList:
            listZ.append([i.getName(), i.getSurname(), i.getPatronymic(), i.getID()])
        return listZ

    def parseInJSONStudent(self) -> None:
        jsn = []
        for student in self._studentList:

            jsn.append({
                "ID": student.getID(),
                "name": student.getName(),
                "surname": student.getSurname()
            })

            with open('students.json', 'w', encoding='UTF-8') as f:
                json.dump(jsn, f, indent=4)

    def parseInJSONTutor(self) -> None:
        jsn = []
        for tutor in self._tutorList:

            jsn.append({
                "ID": tutor.getID(),
                "name": tutor.getName(),
                "surname": tutor.getSurname(),
                "patronymic": tutor.getPatronymic()
            })

            with open('tutors.json', 'w', encoding='UTF-8') as f:
                json.dump(jsn, f, indent=4)


    def parseInJSONAll(self) -> None:
        jsn = []
        for key in self._studTutorMap:
            jsn.append({
                "TutorID": key,
                "FIO Tutor": self.gettutorbyID(key).getName() + " " + self.gettutorbyID(key).getSurname() + " " + self.gettutorbyID(key).getPatronymic(),
                "Data Students": [str(self.getstudentbyID(i).getID()) + " " + self.getstudentbyID(i).getName() + " " + self.getstudentbyID(i).getSurname()  for i in self.getstudentsbyID(key)],
            })

            with open('all.json', 'w', encoding='UTF-8') as f:
                json.dump(jsn, f, indent=4)

    def parseInXMLAll(self) -> None:
        data = ET.Element('Cathedra')
        for key in self._studTutorMap:
            tutor = ET.SubElement(data, 'Tutor')
            tutor.set('ID', key)
            tutor.set('Name', self.gettutorbyID(key).getName())
            tutor.set('Surname',  self.gettutorbyID(key).getSurname())
            tutor.set('Patronymic', self.gettutorbyID(key).getPatronymic())
            students = ET.SubElement(tutor, 'Students')

            for i in self.getstudentsbyID(key):
                student = ET.SubElement(students, 'StudentsData')
                student.set('ID', str(self.getstudentbyID(i).getID()))
                student.set('Name', self.getstudentbyID(i).getName())
                student.set('Surname',self.getstudentbyID(i).getSurname())

        mydata = minidom.parseString(ET.tostring(data, encoding='utf-8', method='xml')).toprettyxml(indent="   ")

        with open("all.xml", "wb") as f:
            f.write(mydata.encode('utf-8'))

    def parseInXMLStudent(self) -> None:
        data = ET.Element('Students')

        for student in self._studentList:
            items = ET.SubElement(data, 'Student')
            id = ET.SubElement(items, 'ID')
            name = ET.SubElement(items, 'name')
            surname = ET.SubElement(items, 'surname')

            name.text = student.getName()
            surname.text = student.getSurname()
            id.text = str(student.getID())

        mydata = minidom.parseString(ET.tostring(data)).toprettyxml(indent="   ")

        with open("students.xml",  "wb") as f:
            f.write(mydata.encode('utf-8'))


    def parseInXMLTutor(self) -> None:
        data = ET.Element('Tutors')

        for tutor in self._tutorList:
            items = ET.SubElement(data, 'Tutor')
            id = ET.SubElement(items, 'ID')
            name = ET.SubElement(items, 'name')
            surname = ET.SubElement(items, 'surname')
            patronymic = ET.SubElement(items, 'patronymic')

            name.text = tutor.getName()
            surname.text = tutor.getSurname()
            patronymic.text = tutor.getPatronymic()
            id.text = str(tutor.getID())

        mydata = minidom.parseString(ET.tostring(data)).toprettyxml(indent="   ")

        with open("tutors.xml",  "wb") as f:
            f.write(mydata.encode('utf-8'))

    def parseOutJsonStudent(self, pth) -> None:
        if os.path.isfile(pth) and pth.split('.')[-1] == "json":
            with open(pth) as f:
                dict = json.load(f)
                for i in range(len(dict)):
                    su = Student()
                    su.setName(dict[i]['name'])
                    su.setSurname(dict[i]['surname'])
                    su.setID(dict[i]['ID'])
                    c.addStudent(su)


        else:
            print("Файла не существует или он не является .json")


    def parseOutJsonTutor(self, pth) -> None:
        if os.path.isfile(pth) and pth.split('.')[-1] == "json":
            with open(pth) as f:
                dict = json.load(f)
                for i in range(len(dict)):
                    tu = Tutor()
                    tu.setName(dict[i]['name'])
                    tu.setSurname(dict[i]['surname'])
                    tu.setPatronymic(dict[i]['patronymic'])
                    tu.setID(dict[i]['ID'])
                    c.addTutor(tu)
        else:
            print("Файла не существует или он не является .json")

    def parseOutXMLStudent(self, pth) -> None:
        if os.path.isfile(pth) and pth.split('.')[-1] == "xml":
            tree = ET.parse(pth)
            root = tree.getroot()
            for elem in root:
                su = Student()
                su.setID(elem[0].text)
                su.setName(elem[1].text)
                su.setSurname(elem[2].text)
                c.addStudent(su)

        else:
            print("Файла не существует или он не является .xml")

    def parseOutXMLTutor(self, pth) -> None:
        if os.path.isfile(pth) and pth.split('.')[-1] == "xml":
            tree = ET.parse(pth)
            root = tree.getroot()
            for elem in root:
                tu = Tutor()
                tu.setID(elem[0].text)
                tu.setName(elem[1].text)
                tu.setSurname(elem[2].text)
                tu.setPatronymic(elem[3].text)
                c.addTutor(tu)
        else:
            print("Файла не существует или он не является .xml")

    @property
    def studTutorMap(self):
        return self._studTutorMap


def Menu():
    print("1 - Добавить студента")
    print("2 - Добавить преподавателя")
    print("3 - Записать данные в Json")
    print("4 - Записать данные в XML")
    print("5 - Считать данные из Json")
    print("6 - Считать данные из XML")
    print("7 - Вывести данные")
    print("8 - Вывести данные JSON")
    print("9 - Вывести данные XML")
    print("0 - Закончить программу")


def validate_name(name: str) -> bool:
    return bool(re.match(r'^[a-zA-Zа-яёА-ЯЁ]+$', name))

def validate_num(name: str) -> bool:
    return bool(re.match(r'^\d+$', name))

n = -1
c = Cathedra()
while n != '0':
    Menu()
    n = input()
    while n < '0' or n > '9':
        print("Ошибка! Введите правильное число")
        n = input()
    if n == '1':
        s = Student()
        if len(c.getListTutor()) == 0:
            print("Без преподавателя нельзя добавить студента")
            continue
        print("Введите имя студента:")
        stud_name = str(input())

        while validate_name(stud_name) == False:
            print("Ошибка! Введите правильное имя")
            stud_name = str(input())
            validate_name(stud_name)

        s.setName(stud_name)

        print("Введите фамилию студента:")
        stud_surname = str(input())

        while validate_name(stud_surname) == False:
            print("Ошибка! Введите правильную фамилию")
            stud_surname = str(input())
            validate_name(stud_surname)

        s.setSurname(stud_surname)


        print("Введите номер студента:")
        stud_id = str(input())

        while validate_num(stud_id) == False:
            print("Ошибка! Введите правильный номер")
            stud_id = str(input())
            validate_num(stud_id)

        students = c.getListStudent()
        for student in students:
            while student[-1] == int(stud_id):
                print("ID повторяюся. Введите заново:")
                stud_id = str(input())
                while validate_num(stud_id) == False:
                    print("Ошибка! Введите правильный номер")
                    stud_id = str(input())
                    validate_num(stud_id)

        print("К каком преподавателю добавить?")
        print("Список:")
        prepods = c.getListTutor()
        for prepod in prepods:
            print(prepod[-1])

        flag = True
        s.setID(int(stud_id))
        while flag:
            prepodID = str(input())
            for prepod in prepods:
                if int(prepodID) == prepod[-1]:
                    c.studTutorMap.setdefault(prepodID, []).append(stud_id)
                    flag = False
                    break
            if flag:
                print("Такого преподавателя нет")

        print(c.studTutorMap)
        c.addStudent(s)

    elif n == '2':
        t = Tutor()

        print("Введите имя преподавателя:")
        tutor_name = str(input())

        while validate_name(tutor_name) == False:
            print("Ошибка! Введите правильное имя")
            tutor_name = str(input())
            validate_name(tutor_name)

        t.setName(tutor_name)

        print("Введите фамилию преподавателя:")
        tutor_surname = str(input())

        while validate_name(tutor_surname) == False:
            print("Ошибка! Введите правильную фамилию")
            tutor_surname = str(input())
            validate_name(tutor_surname)

        t.setSurname(tutor_surname)

        print("Введите отчество преподавателя:")
        tutor_patronymic = str(input())

        while validate_name(tutor_patronymic) == False:
            print("Ошибка! Введите правильное отчество")
            tutor_patronymic = str(input())
            validate_name(tutor_patronymic)

        t.setPatronymic(tutor_patronymic)

        print("Введите номер преподавателя:")
        tutor_id = str(input())

        while validate_num(tutor_id) == False:
            print("Ошибка! Введите правильный номер")
            tutor_id = str(input())
            validate_num(tutor_id)

        tutors = c.getListTutor()
        for tutor in tutors:
            while tutor[-1] == int(tutor_id):
                print("ID повторяюся. Введите заново:")
                tutor_id = str(input())
                while validate_num(tutor_id) == False:
                    print("Ошибка! Введите правильный номер")
                    tutor_id = str(input())
                    validate_num(tutor_id)

        t.setID(int(tutor_id))
        c.addTutor(t)

    elif n == '3':
        c.parseInJSONStudent()
        c.parseInJSONTutor()
    elif n == '4':
        c.parseInXMLStudent()
        c.parseInXMLTutor()

    elif n == '5':
        print("1 - Считать данные из Json для Студентов")
        print("2 - Считать данные из Json для Преподавателей")
        choise_json_out = str(input())
        while choise_json_out < '0' or choise_json_out > '2':
            print("Ошибка! Введите правильное число")
            choise_json_out = str(input())

        print("Введите имя файла:")
        pth = str(input())

        if choise_json_out == '1':
            c.parseOutJsonStudent(pth)
        elif choise_json_out == '2':
            c.parseOutJsonTutor(pth)


    elif n == '6':

        print("1 - Считать данные из XML для Студентов")
        print("2 - Считать данные из XML для Преподавателей")
        choise_xml_out = str(input())
        while choise_xml_out < '0' or choise_xml_out > '2':
            print("Ошибка! Введите правильное число")
            choise_xml_out = str(input())

        print("Введите имя файла:")
        pth = str(input())

        if choise_xml_out == '1':
            c.parseOutXMLStudent(pth)
        elif choise_xml_out == '2':
            c.parseOutXMLTutor(pth)


    elif n == '7':
        print('Студенты: ',*c.getListStudent())
        print('Преподаватели: ',*c.getListTutor())

    elif n == '8':
        c.parseInJSONAll()

    elif n == '9':
        c.parseInXMLAll()
