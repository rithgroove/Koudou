from .time_stamp import TimeStamp

def init():
	global timestamp
	timestamp = TimeStamp()
	print("Finish initializing global var")