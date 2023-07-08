from datetime import datetime as dt
import matplotlib.pyplot as plt
import time



fig, ax = plt.subplots(facecolor='black') 
plt.rcParams['toolbar'] = 'None' # Remove tool bar (upper bar)
fig.canvas.window().statusBar().setVisible(False) # Remove status bar (bottom bar)

manager = plt.get_current_fig_manager()
manager.full_screen_toggle()



number_of_days = 71

daycounter = 0
previous_day = 21

while True:
    ax.clear()
    
    current_day = dt.now().day
    
    if current_day != previous_day:
        daycounter += 1
        previous_day = current_day
    
    plt.text(0.45, 0.5, str(number_of_days - daycounter), color='white', fontsize=100)
    ax.set_facecolor("black")
    
    plt.pause(0.5)