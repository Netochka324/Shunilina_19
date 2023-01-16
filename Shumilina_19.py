import sys
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QPushButton
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from math import pi, sqrt, factorial


class Calculator(QWidget):
    text_default = '0 '
    text_rez = 'Результат: '
    text_rez_ost = 26-len(text_rez)

    def __init__(self):
        super().__init__()
        # количество кнопок
        self.n, self.m = 6, 5
        # инициация переменных
        self.clean, self.backspace, self.sqrt, self.div, self.inverse, self.num_7, self.num_8, self.num_9, self.mul, \
        self.x_power_2, self.num_4, self.num_5, self.num_6, self.add, self.x_power_3, self.num_1, self.num_2, \
        self.num_3, self.dif, self.x_power_y, self.num_0, self.comma, self.pi, self.absolut, self.fact, \
        self.ravno, self.mem_store, self.mem_add, self.mem_restore, self.mem_clean = [None] * self.n * self.m

        self.memory = 0

        self.initUI()  # метод для делегирования создания GUI
        self.my_input = ''  # результат вычисления
        self.operand_1 = 0  # первое число в вычислении
        self.operand_2 = 0  # второе число в вычислении
        self.operation = ''  # операция между числами

    def initUI(self):  # внешний вид калькулятора
        # переменные для кнопок
        oper = [
            [self.clean, self.backspace, self.sqrt, self.div, self.inverse],
            [self.num_7, self.num_8, self.num_9, self.mul, self.x_power_2],
            [self.num_4, self.num_5, self.num_6, self.add, self.x_power_3],
            [self.num_1, self.num_2, self.num_3, self.dif, self.x_power_y],
            [self.num_0, self.comma, self.pi, self.absolut, self.fact],
            [self.ravno, self.mem_store, self.mem_add, self.mem_restore, self.mem_clean]
        ]
        # значки кнопок
        oper_text = [
            ['C', '←', '√', '/', '1/x'],
            ['7', '8', '9', '*', 'x^2'],
            ['4', '5', '6', '+', 'x^3'],
            ['1', '2', '3', '-', 'x^y'],
            ['0', '.', 'pi', '|x|', 'x!'],
            ['=', 'MS', 'M+', 'MR', 'MC']
        ]
        # функции кнопок
        oper_func = [
            [self.clean_, self.back_, self.sqrt_, self.div_, self.inverse_],
            [self.seven, self.eight, self.nine, self.mul_, self.x_power_2_],
            [self.four, self.five, self.six, self.add_, self.x_power_3_],
            [self.one, self.two, self.three, self.dif_, self.x_power_y_],
            [self.zero, self.comma_, self.pi_, self.absolut_, self.fact_],
            [self.ravno_, self.mem_store_, self.mem_add_, self.mem_restore_, self.mem_clean_]
        ]

        # параметры для кнопок
        self.a, self.b = [40, 30]
        # расстояние между кнопками
        self.delta = 5
        # отступ слева и справа
        self.x0 = 10
        self.y0 = self.x0

        # высота окошка ввода
        self.h0 = 40
        # окно программы
        self.A = self.a * self.m + self.delta * (self.m - 1) + 2 * self.x0
        self.B = (self.b + self.delta) * self.n + self.h0 * 2 + 3 * self.y0
        self.setGeometry(0, 0, self.A, self.B)
        self.setWindowTitle('Calculator')

        # окно ввода
        self.label_inn = QLabel(self)  # создаем первое поле для ввода/вывода результата
        self.label_inn.setStyleSheet("background-color: lightblue; "
                                     "border: 2px solid black;")
        self.label_fontsize = 11
        self.label_inn.setFont(QtGui.QFont('Times', self.label_fontsize))
        self.label_inn.setText(self.text_default)  # установили начальное значение в окне
        self.label_inn.resize(self.A - 2 * self.x0, self.h0)  # размер окна
        self.label_inn.move(self.x0, self.h0 + self.y0 * 2)
        self.label_inn.setAlignment(Qt.AlignVCenter | Qt.AlignRight)

        # окно результата
        self.label_rez = QLabel(self)  # создаем первое поле для ввода/вывода результата
        self.label_rez.setStyleSheet("background-color: white; "
                                     "border: 2px solid black;")
        self.label_rez.setFont(QtGui.QFont('Times', self.label_fontsize, italic=True))
        self.label_rez.setText(self.text_rez)  # установили начальное значение в окне
        self.label_rez.resize(self.A - 2 * self.x0, self.h0)  # размер окна
        self.label_rez.move(self.x0, self.y0)
        self.label_rez.setAlignment(Qt.AlignVCenter | Qt.AlignRight)

        x, y = self.x0, self.h0 * 2 + self.y0 * 3
        # Создаем кнопки
        for i in range(self.n):
            for j in range(self.m):
                oper[i][j] = QPushButton(oper_text[i][j], self)
                oper[i][j].setStyleSheet("QPushButton::pressed"
                                         "{background-color : blue;")
                oper[i][j].resize(self.a, self.b)
                oper[i][j].move(x, y)
                x += self.a + self.delta
            x = self.x0
            y += self.b + self.delta
        # цвета кнопок
        oper[0][0].setStyleSheet("border: 2px solid red;"
                                 "color: red;")
        oper[0][1].setStyleSheet("border: 2px solid red;"
                                 "color: red;")
        oper[5][0].setStyleSheet("border: 2px solid blue;"
                                 "color: blue;")

        for i in range(1, self.m):
            oper[5][i].setStyleSheet("background-color : lightgrey;"
                                     "border: 2px solid grey;")

        # связи кнопок и функций
        for i in range(self.n):
            for j in range(self.m):
                oper[i][j].clicked.connect(oper_func[i][j])

    def enter_value(self):
        if self.label_inn.text() == self.text_default:
            self.label_inn.setText('')
        self.label_inn.setText(str(self.label_inn.text()) + str(self.my_input))

    def one(self):
        self.my_input = 1
        self.enter_value()

    def two(self):
        self.my_input = 2
        self.enter_value()

    def three(self):
        self.my_input = 3
        self.enter_value()

    def four(self):
        self.my_input = 4
        self.enter_value()

    def five(self):
        self.my_input = 5
        self.enter_value()

    def six(self):
        self.my_input = 6
        self.enter_value()

    def seven(self):
        self.my_input = 7
        self.enter_value()

    def eight(self):
        self.my_input = 8
        self.enter_value()

    def nine(self):
        self.my_input = 9
        self.enter_value()

    def zero(self):
        self.my_input = 0
        self.enter_value()

    def pi_(self):
        self.my_input = pi
        self.enter_value()

    def add_(self):
        self.operation = '+'
        self.operand_1 = float(self.label_inn.text())
        self.label_inn.setText(self.text_default)

    def dif_(self):
        if not self.operand_1 or self.operand_1 and self.operation:
            self.my_input = '-'
            self.enter_value()
        else:
            self.operation = '-'
            self.operand_1 = float(self.label_inn.text())
            self.label_inn.setText(self.text_default)

    def mul_(self):
        self.operation = '*'
        self.operand_1 = float(self.label_inn.text())
        self.label_inn.setText(self.text_default)

    def div_(self):
        self.operation = '/'
        self.operand_1 = float(self.label_inn.text())
        self.label_inn.setText(self.text_default)

    def inverse_(self):
        self.operation = '1/x'
        self.operand_1 = float(self.label_inn.text())

    def x_power_2_(self):
        self.operation = 'x^2'
        self.operand_1 = float(self.label_inn.text())

    def x_power_3_(self):
        self.operation = 'x^3'
        self.operand_1 = float(self.label_inn.text())

    def x_power_y_(self):
        self.operation = 'x^y'
        self.operand_1 = float(self.label_inn.text())
        self.label_inn.setText(self.text_default)

    def comma_(self):
        if not self.operand_1 or self.operand_1 and not self.operand_2:
            self.my_input = '0.'
        else:
            self.my_input = '.'
        self.enter_value()

    def sqrt_(self):
        self.operation = '√'
        self.operand_1 = float(self.label_inn.text())

    def absolut_(self):
        self.operation = '|x|'
        self.operand_1 = float(self.label_inn.text())

    def fact_(self):
        self.operation = 'x!'
        self.operand_1 = float(self.label_inn.text())

    def mem_store_(self):
        self.memory = float(self.label_inn.text())
        self.label_inn.setText(self.text_default)

    def mem_add_(self):
        self.memory += float(self.label_inn.text())
        self.label_inn.setText(self.text_default)

    def back_(self):
        self.my_input = ''
        self.label_inn.setText(self.label_inn.text()[:-1])
        if not self.label_inn.text():
            self.label_inn.setText('0')
        self.enter_value()

    def mem_restore_(self):
        self.my_input = self.memory
        self.enter_value()

    def mem_clean_(self):
        self.memory = 0

    def clean_(self):
        self.operand_1, self.operand_2 = 0, 0
        self.label_inn.setText(self.text_default)

    def ravno_(self):
        if self.operand_1:

            if self.operation not in ['x^2', 'x^3', '√', '1/x', '|x|', 'x!'] and self.label_inn.text():
                self.operand_2 = float(self.label_inn.text())

                if self.operation == '/':
                    if self.operand_2 == 0:
                        self.label_rez.setText('На ноль делить нельзя!')
                    else:
                        self.label_rez.setText(self.text_rez + self.check_rez(str(self.operand_1 / self.operand_2)))
                elif self.operation == '+':
                    self.label_rez.setText(self.text_rez + self.check_rez(str(self.operand_1 + self.operand_2)))
                elif self.operation == '-':
                    self.label_rez.setText(self.text_rez + self.check_rez(str(self.operand_1 - self.operand_2)))
                elif self.operation == '*':
                    self.label_rez.setText(self.text_rez + self.check_rez(str(self.operand_1 * self.operand_2)))
                elif self.operation == 'x^y':
                    self.label_rez.setText(self.text_rez + self.check_rez(str(pow(self.operand_1, self.operand_2))))

            elif self.operation in ['x^2', 'x^3', '√', '1/x', '|x|', 'x!']:
                if self.operation == 'x^2':
                    self.label_rez.setText(self.text_rez + self.check_rez(str(pow(self.operand_1, 2))))
                elif self.operation == 'x^3':
                    self.label_rez.setText(self.text_rez + self.check_rez(str(pow(self.operand_1, 3))))
                elif self.operation == '√':
                    if self.operand_1 < 0:
                        self.label_rez.setText('Ошибка ввода!')
                    else:
                        self.label_rez.setText(self.text_rez + self.check_rez(str(sqrt(self.operand_1))))
                elif self.operation == '|x|':
                    self.label_rez.setText(self.text_rez + self.check_rez(str(abs(self.operand_1))))
                elif self.operation == 'x!':
                    if self.operand_1 < 0:
                        self.label_rez.setText('Неверное основание факториала!')
                    else:
                        self.label_rez.setText(self.text_rez + self.check_rez(str(factorial(int(self.operand_1)))))
                elif self.operation == '1/x':
                    if self.operand_1 == 0:
                        self.label_rez.setText('На ноль делить нельзя!')
                    else:
                        self.label_rez.setText(self.text_rez + self.check_rez(str(1 / self.operand_1)))

    def check_rez(self, text):
        new = text
        e = 0
        if 'e+' in new:
            num, e = new.split('e+')
            e = int(e)
            delta = len(new)-self.text_rez_ost
            new = num[:-delta]
            e += delta
        elif 'e-' in new:
            num, e = new.split('e-')
            e = -int(e)
            delta = len(new)-self.text_rez_ost
            new = num[:-delta]
            e -= delta
        while len(new) > self.text_rez_ost and '.' in new:
            cel, znak = new.split('.')
            lishn = len(new) - self.text_rez_ost
            if lishn < len(znak):
                new = new[: -lishn]
            else:
                new = cel
        else:
            if len(new) > self.text_rez_ost:
                e = 1
                new = new[:-1]
                while len(new) > self.text_rez_ost - len('e+' + str(e)):
                    e += 1
                    new = new[:-1]
        if not e:
            return new
        elif e < 0:
            return new + 'e' + str(e)
        return new + 'e+' + str(e)


app = QApplication(sys.argv)
my_calculator = Calculator()
my_calculator.show()
sys.exit(app.exec())
# ДЗ на понедельник:
# Добавить кнопки и функции:
# степень, корень, возведение в квадрат, корень квадратный.
# Изменить внешний вид окна калькулятора и лейбла.
