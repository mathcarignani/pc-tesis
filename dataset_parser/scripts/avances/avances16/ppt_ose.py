

import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import matplotlib.patches as mpatches


import numpy as np

plt.rcdefaults()
fig = plt.figure(figsize=(13, 4), facecolor=(1, 1, 1))
ax = fig.add_subplot(1, 1, 1)
# fig.patch.set_facecolor('white')

# Example data
people = ('Tom', 'Dick', 'Harry', 'Slim', 'Jim')
y_pos1, y_pos2 = 0.5, 2.5

y_pos = [y_pos1, y_pos2]
# performance = 3 + 10 * np.random.rand(len(people))
# error = np.random.rand(len(people))

ax.grid(b=True, color='silver', zorder=0, linestyle='-.')

height = 0.8
align = 'edge'
ax.barh([y_pos2], [98.8], height=height, align=align, color='royalblue', zorder=3)

ax.barh([y_pos1], [45.2 + 14.2 + 39.4], height=height, align=align, color='sandybrown', zorder=3)
ax.barh([y_pos1], [45.2 + 14.2], height=height, align=align, color='greenyellow', zorder=3)
ax.barh([y_pos1], [45.2], height=height, align=align, color='cornflowerblue', zorder=3)

# fmt = lambda x: "{:.0f}%".format(x)
# xticklabels = [fmt(i) for i in [0, 20, 40, 60, 80, 100]]
# plt.xticks([0, 20, 40, 60, 80, 100], [fmt(i) for i in [0, 20, 40, 60, 80, 100]])
# plt.tick_params(axis='both', which='major', labelsize=16)
# ax.set_xticklabels(xticklabels, weight='bold')

# ax.set_xlim(left=-1, right=8)  # 8 thresholds
ax.set_ylim(bottom=0, top=4)

y_text = 0.7
fontsize = 28
text_fontsize = 26
top_y_text = y_text + y_pos2 - y_pos1
top_y_title = top_y_text + 0.8
bottom_y_text = y_text
bottom_y_title = bottom_y_text - 0.7

ax.text(43 - 0.2, top_y_title, 'TOTAL', fontsize=text_fontsize, fontweight='bold')
ax.text(43, top_y_text, '98,8%', fontsize=fontsize, fontweight='bold')

ax.text(16 - 15, bottom_y_title, 'RED Y TRATAMIENTO', fontsize=text_fontsize, fontweight='bold')
ax.text(16, bottom_y_text, '45,2%', fontsize=fontsize, fontweight='bold')

ax.text(46 + 2.5, bottom_y_title, 'RED', fontsize=text_fontsize, fontweight='bold')
ax.text(46, bottom_y_text, '14,2%', fontsize=fontsize, fontweight='bold')

ax.text(72.5 - 6.5, bottom_y_title, 'POZO / FOSA', fontsize=text_fontsize, fontweight='bold')
ax.text(72.5, bottom_y_text, '39,4%', fontsize=fontsize, fontweight='bold')



ax.set_yticks([])
ax.set_yticklabels([])
ax.axis('off')
# ax.invert_yaxis()  # labels read top-to-bottom
# ax.set_xlabel('%')
# ax.set_title('COBERTURA DE SANEAMIENTO')
# ax.set_axis_bgcolor("white")

# plt.show()
plt.savefig('graphv3.png', bbox_inches = 'tight')
plt.close()











# LEGEND

# plt.rcdefaults()
# fig = plt.figure(figsize=(2.61, 2), facecolor=(1, 1, 1))
# ax = fig.add_subplot(1, 1, 1)
#
# colors = ['royalblue', 'white', 'cornflowerblue', 'greenyellow', 'sandybrown']
# lines = [Line2D([0], [0], color=c, linewidth=15, linestyle='-') for c in colors]
# labels = ['Total', '', 'Red y tratamiento', 'Red', 'Pozo/Fosa']
#
# fig.clear()
# fig.legend(lines, labels, bbox_to_anchor=(0.522, 0.4, 0.5, 0.5), markerscale=6)
#
#
# plt.savefig('graphv3-legend.png') #, bbox_inches = 'tight')
# plt.close()

