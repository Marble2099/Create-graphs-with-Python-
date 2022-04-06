from datetime import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as dtf
import csv

with open('CPU.csv', 'r') as cpu_input:
    time_list = []
    cpu_util_list = []
    cpu_queue = []
    spamreader = csv.reader(cpu_input, delimiter=';', quotechar='|')
    for row in spamreader:
        try:
            time_list.append(row[0])
            cpu_util_list.append(float(row[1].replace(',', '.')))
            cpu_queue.append(float(row[2]))
        except ValueError:
            continue

    time_list.pop(0)

a = [dt.strptime(d, '%H:%M:%S') for d in time_list]

x = dtf.date2num(a)
N = len(x)

fig, ax = plt.subplots(figsize=(6.496063, 3.93701))
fig.subplots_adjust(right=0.75)
twin = ax.twinx()

locator = dtf.AutoDateLocator(minticks=N//10, maxticks=N//5)
formatter = dtf.ConciseDateFormatter(locator)

ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(formatter)
plt.setp(ax.get_xticklabels(), rotation=90)

#1 линия
color = 'tab:blue'
ax.set_xlabel('Продолжительность теста, чч:мм')
ax.set_ylabel('Утилизация CPU, %')
lns1 = ax.plot(x, cpu_util_list, color=color)
ax.tick_params(axis='y', labelcolor=color)
ax.set_ylim(0, 100)

#2 линия
color = 'tab:green'
twin.set_ylabel('Длина очереди, шт')  # we already handled the x-label with ax1
lns2 = twin.plot(x, cpu_queue, color=color)
twin.tick_params(axis='y', labelcolor=color)
lns = lns1+lns2
labs = [l.get_label() for l in lns]
ax.legend(handles=lns1+lns2, labels=['Утилизация CPU'] + ['Длина очереди CPU'], loc='upper left')
twin.set_ylim(0, 10)

#красная черта
L = [i for i in range(N)]
A = ['12:09'] * N
b = [dt.strptime(c, '%H:%M') for c in A]
z = dtf.date2num(b)
p1, = ax.plot(z, L, color='red')

fig.tight_layout()  # otherwise the right y-label is slightly clipped

plt.title('Утилизация CPU')
plt.show()

