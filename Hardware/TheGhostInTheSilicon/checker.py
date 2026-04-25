import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('led_capture.csv')

plt.figure(figsize=(15, 3))
plt.plot(df['Time'][:5000], df['GPIO_LED'][:5000], drawstyle='steps-post')
plt.title('GPIO_LED Logic Analyzer Capture')
plt.xlabel('Time (s)')
plt.ylabel('Logic Level')
plt.ylim(-0.2, 1.2)
plt.grid(True)
# plt.show() # we are on Termux so this will not work
plt.savefig('plot.png', dpi=300, bbox_inches='tight')
print("Plot successfully saved as my_plot.png")
