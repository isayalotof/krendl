import pyttsx3


def speaker(text):
	engine = pyttsx3.init()
	engine.setProperty('rate', 180)
	engine.say(text)
	engine.runAndWait()
	engine.stop()