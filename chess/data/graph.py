import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('../games.csv', sep=';')
game_score = df.iloc[0]
precision = 30
print(game_score)
x = np.linspace(1,  len(df.columns)-precision, len(df.columns)-precision)
y = np.zeros(len(x))
z = np.zeros(len(x))
for i in range(1, len(df.columns) - precision):
    wins = 0
    loses = 0
    for j in range(precision):
        if game_score.iloc[i + j][0] == '1':
            wins += 1
        if game_score.iloc[i + j][4] == '1':
            loses += 1
    y[i] = wins / precision * 100
    z[i] = 100 - (loses / precision * 100)

fig, ax = plt.subplots()
ax.plot(x, y, color='green')
ax.plot(x, z, color='red')

ax.fill_between(x, y, color='green', alpha=0.1)

ax.fill_between(x, z, 100, color='red', alpha=0.1)

ax.fill_between(x, y, z, color='blue', alpha=0.1)

plt.xlabel('Game')
plt.ylabel('Percentage')
plt.title('Winning percentage')
plt.legend(['Win', 'Lose'])
plt.show()
