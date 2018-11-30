import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)

cnt=0
xComponent=[]

line,  = ax1.plot([0], [0])
text = ax1.text(0.97,0.97, "", transform=ax1.transAxes, ha="right", va="top")

plt.ylim(0,25)
plt.xlim(0,100)
last_time = {0: time.time()}

def animateinit(): #tells our animator what artists will need re-drawing every time
    return line,text

def animate(i):



    line.set_data(range( len(xComponent) ) ,xComponent)
    new_time = time.time()
    text.set_text("{0:.2f} fps".format(1./(new_time-last_time[0])))
    last_time.update({0:new_time})
    return line,text #return the updated artists

#inform the animator what our init_func is and enable blitting
ani = animation.FuncAnimation(fig, animate, interval=0,init_func=animateinit, blit=True)
plt.show()
