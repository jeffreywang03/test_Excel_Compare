import datetime
import queue
import logging
import signal
import os
import time
import threading
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk, VERTICAL, HORIZONTAL, N, S, E, W
from tkinter.filedialog import askopenfilename
import ExcelCompare

logger = logging.getLogger(__name__)


class QueueHandler(logging.Handler):
	#Class to send logging records to a queue. It can be used from different threads
	#The ConsoleUi class polls this queue to display records in a ScrolledText widget
	def __init__(self, log_queue):
		super().__init__()
		self.log_queue = log_queue

	def emit(self, record):
		self.log_queue.put(record)




class ConsoleUi:
	"""Poll messages from a logging queue and display them in a scrolled text widget"""

	def __init__(self, frame):
		self.frame = frame
		# Create a ScrolledText wdiget
		self.scrolled_text = ScrolledText(frame, state='disabled', height=12)
		self.scrolled_text.grid(row=0, column=0, sticky=(N, S, W, E))
		self.scrolled_text.configure(font='TkFixedFont')
		#self.scrolled_text.tag_config('INFO', foreground='black')
		#self.scrolled_text.tag_config('DEBUG', foreground='gray')
		#self.scrolled_text.tag_config('WARNING', foreground='orange')
		#self.scrolled_text.tag_config('ERROR', foreground='red')
		#self.scrolled_text.tag_config('CRITICAL', foreground='red', underline=1)
		# Create a logging handler using a queue
		self.log_queue = queue.Queue()
		self.queue_handler = QueueHandler(self.log_queue)
		formatter = logging.Formatter('%(asctime)s: %(message)s')
		self.queue_handler.setFormatter(formatter)
		logger.addHandler(self.queue_handler)
		# Start polling messages from the queue
		self.frame.after(100, self.poll_log_queue)

	def display(self, record):
		msg = self.queue_handler.format(record)
		self.scrolled_text.configure(state='normal')
		self.scrolled_text.insert(tk.END, msg + '\n', record.levelname)
		self.scrolled_text.configure(state='disabled')
		# Autoscroll to the bottom
		self.scrolled_text.yview(tk.END)

	def poll_log_queue(self):
		# Check every 100ms if there is a new message in the queue to display
		while True:
			try:
				record = self.log_queue.get(block=False)
			except queue.Empty:
				break
			else:
				self.display(record)
		self.frame.after(100, self.poll_log_queue)

class FormUi:

	def __init__(self, frame):

		self.frame = frame

		ttk.Label(self.frame, text='File 1:').grid(column=0, row=0, sticky=W)
		self.button = ttk.Button(self.frame, text='Browse', width=30, command=self.openFile).grid(column=0, row=1, sticky=(W))
		logging.info("Button 1: %s" % filename)

		ttk.Label(self.frame, text='File 2:').grid(column=0, row=3, sticky=W)
		self.button = ttk.Button(self.frame, text='Browse', width=30, command=self.openFile).grid(column=0, row=4, sticky=(W)) 


		self.button = ttk.Button(self.frame, text='Submit', command=self.submit).grid(padx=50, pady=10)
		self.button = ttk.Button(self.frame, text='Exit', command=self.close).grid(padx=50, pady=20)

	def openFile(self):
		cwd = os.getcwd()
		filename = askopenfilename(initialdir = cwd, title = "Select the Background Report CSV file", filetypes = (("csv files", "*.csv"),))
		logger.info("File Selected: \n\n%s" % filename)

	def submit(self):
		logger.info("Testing...")
		#print(summ.Summation(5,8))

	def close(self):
		exit()

class App:

	def __init__(self, root):
		self.root = root
		root.title('Logging Handler')
		root.columnconfigure(0, weight=1)
		root.rowconfigure(0, weight=1)
		# Create the panes and frames
		vertical_pane = ttk.PanedWindow(self.root, orient=VERTICAL)
		vertical_pane.grid(row=0, column=0, sticky="nsew")
		horizontal_pane = ttk.PanedWindow(vertical_pane, orient=HORIZONTAL)
		vertical_pane.add(horizontal_pane)
		
		form_frame = ttk.Labelframe(horizontal_pane, text="Files")
		form_frame.columnconfigure(1, weight=1)
		horizontal_pane.add(form_frame, weight=1)

		console_frame = ttk.Labelframe(horizontal_pane, text="Console")
		console_frame.columnconfigure(0, weight=1)
		console_frame.rowconfigure(0, weight=1)
		horizontal_pane.add(console_frame, weight=1)

		#third_frame = ttk.Labelframe(vertical_pane, text="Third Frame")
		#vertical_pane.add(third_frame, weight=1)

		# Initialize all frames
		self.form = FormUi(form_frame)
		self.console = ConsoleUi(console_frame)
		#self.third = ThirdUi(third_frame)
		#self.clock = Clock()
		#self.clock.start()
		self.root.protocol('WM_DELETE_WINDOW', self.quit)
		self.root.bind('<Control-q>', self.quit)
		signal.signal(signal.SIGINT, self.quit)

	def quit(self, *args):
		#self.clock.stop()
		self.root.destroy()



def main():
	logging.basicConfig(level=logging.DEBUG)
	root = tk.Tk()
	app = App(root)
	app.root.mainloop()

if __name__ == '__main__':
	main()