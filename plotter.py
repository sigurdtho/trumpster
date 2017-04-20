#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

trumpster = [-0.0111, -0.0151, -0.1166, -0.055, 0.0439, 0.1588, 0.0323, -0.0156, 0.0108, -0.0675, 0.16, -0.2587, 0.1799, 0.0431, 0.0747]

human = [-0.15, -0.1, 0.0, -0.23, -0.3, 0.2, 0.05, -0.2, -0.2, -0.5, -0.2, -0.4, 0.2, 0.0, 0.0]


fig = plt.figure(1)
ax = fig.add_subplot(111)
ax.plot(x, trumpster, label="Trumpster")
ax.plot(x, human, label="Human")
ax.grid('on')
ax.set_ylim([-1, 1])
ax.set_xlabel('article id')
ax.set_ylabel('sentiment score')
ax.legend()

fig.savefig('sent.pdf')
