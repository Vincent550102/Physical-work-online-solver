# include <stdio.h>
# include <math.h>
from math import *
from flask import Flask, render_template, request, redirect, abort
app = Flask(__name__)


def cal(L1, cross_sectional_area, density_L1, density_L2, block_mass, L2):
    n1 = 0
    n2 = 0
    # L1 = float(input('輸入數據:\nL1 (cm) = '))
    L1 /= 100
    # cross_sectional_area = float(input('\ncross-sectional area 截面積 (cm^2) = '))
    cross_sectional_area /= 10000

    # density_L1 = float(input('\ndensity of L1 (g/cm^3) = '))
    density_L1 *= 1000

    # density_L2 = float(input('\ndensity of L2 (g/cm^3) = '))
    density_L2 *= 1000

    # block_mass = float(input('\nmass of the block (kg) = '))
    # L2 = float(input('\nL2 (cm) = '))
    L2 /= 100

    ratio = (L1 * sqrt(density_L1)) / (L2 * sqrt(density_L2))

    # double compare
    correct_n1 = 0
    correct_n2 = 0
    temp = 100
    if (ratio == 1):
        correct_n1 = 1
        correct_n2 = 1
    elif (ratio < 1):
        for n1 in range(1, 11):  # (n1=1; n1 <= 10 & & n2 <= 10; n1 + +, n2=0):
            n2 = n1
            if n1 > 10 or n2 > 10:
                break

            while 1:
                n2 += 1
                if n1 > 10 or n2 > 10 or n1 >= n2:
                    break

                compare = n1 / n2
                if (ratio == compare):
                    temp = ratio - compare
                    correct_n1 = n1
                    correct_n2 = n2
                elif (ratio > compare):
                    if (temp >= ratio - compare):
                        temp = ratio - compare
                        correct_n1 = n1
                        correct_n2 = n2
                else:
                    if (temp >= compare - ratio):
                        temp = compare - ratio
                        correct_n1 = n1
                        correct_n2 = n2

    else:
        for n2 in range(1, 11):  # (n1=1; n1 <= 10 & & n2 <= 10; n1 + +, n2=0):
            n1 = n2
            if n1 > 10 or n2 > 10:
                break

            while 1:
                n1 += 1
                if n1 > 10 or n2 > 10 or n1 <= n2:
                    break

                compare = n1 / n2

                if (ratio == compare):
                    temp = ratio - compare
                    correct_n1 = n1
                    correct_n2 = n2
                elif (ratio > compare):
                    if (temp >= ratio - compare):
                        temp = ratio - compare
                        correct_n1 = n1
                        correct_n2 = n2
                elif (temp >= compare - ratio):
                    temp = compare - ratio
                    correct_n1 = n1
                    correct_n2 = n2

    int_n1 = correct_n1
    int_n2 = correct_n2
    highest_common_factor = 0
    for i in range(100, 0, -1):
        if(int_n1 % i == 0 and int_n2 % i == 0):
            highest_common_factor = i
            break
    int_n1 /= highest_common_factor
    int_n2 /= highest_common_factor

    answer_a = (((sqrt((block_mass * 9.8) / (density_L1 * cross_sectional_area)) * int_n1) / (2 * L1)) +
                ((sqrt((block_mass * 9.8) / (density_L2 * cross_sectional_area)) * int_n2) / (2 * L2))) / 2

    answer_b = int_n1 + int_n2 + 1
    return str(answer_a), str(answer_b)


@ app.route('/', methods=['POST'])
def ind():
    # L1, cross_sectional_area,density_L1,density_L2,block_mass,L2
    try:
        L1 = float(request.values['L1'])
        cross_sectional_area = float(request.values['cross_sectional_area'])
        density_L1 = float(request.values['density_L1'])
        density_L2 = float(request.values['density_L2'])
        block_mass = float(request.values['block_mass'])
        L2 = float(request.values['L2'])

        answer_a, answer_b = cal(L1, cross_sectional_area,
                                 density_L1, density_L2, block_mass, L2)
        return render_template('index.html', **locals())
    except:
        answer_a, answer_b = "你的參數", "還沒打完"
        return render_template('index.html', **locals())


@ app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='localhost', port=8080)
    pass
