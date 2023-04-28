def plotter():
	global xdata
	global fdata
	f, (ax1, ax2) = plt.subplots(2, 1, sharex='all', sharey='none')
	print("Plotting!")
	while(True):
		#start_new_thread(plotter, (f, ax1, ax2 ))
		y = xdata.copy()
		y2 = fdata.copy()
		x = list(range(0,len(y)))
		ax1.clear()
		ax2.clear()
		ax1.plot(x,y)  # 5 seconds rolling window
		ax2.plot(x,y2)
		ax2.set_xlabel('time [s]')
		ax1.set_ylabel('Position [m]')
		ax2.set_ylabel('Force [N]')
		plt.pause(1/plotRefereshRate)