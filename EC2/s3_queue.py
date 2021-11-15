# s3 파일 생성시 sns, sqs를 통해 ec2로 전달


import threading
import time
import utils
import json
import subprocess

QUEUE_NAME = 'QUEUE_NAME'
QUEUE_ATTR_NAME = ''
SLEEP = 10

def Connect2sqs():
	return utils.connect2Service('sqs')

class SQSConsumer(threading.Thread):
	sqs = Connect2sqs()

	def __init__(self, threadID, name, counter):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.counter = counter

	def run(self):
		print("SQSConsumer Thread running!")
		maxRetry = 10000
		numMsgs = 0
		maxMsgs = self.getNumberOfMessages()
		count = 0
		print("No. of messages to consume: ", maxMsgs)
		while numMsgs < maxMsgs or count < maxRetry:
			time.sleep(SLEEP)
			numMsgs += self.consumeMessages()
			count += 1
			print("Iteration No.:", numMsgs)
		print("SQSConsumer Thread Stopped")

	def getQueue(self, sqsQueueName = QUEUE_NAME):
		queue = None
		try:
			queue = self.sqs.get_queue_by_name(QueueName=sqsQueueName)
		except Exception as err:
			print("Error Message {0}".format(err))
		return queue

	def getNumberOfMessages(self):
		numMessages = 0
		try:
			queue = self.getQueue()
			if queue:
				attribs = queue.attributes
				numMessages = int(attribs.get(QUEUE_ATTR_NAME))
			except Exception as err:
				print("Error Message {0}".format(err))
			return numMessages

	def consumeMessages(self, sqsQueueName=QUEUE_NAME):
		numMsgs = 0
		try:
			queue = self.getQueue()
			if queue:
				mesgs = queue.receive_messages(Attributes=['All'], MaxNumberOfMessages = 10, WaitTimeSeconds = 20)
				if not len(mesgs):
					print("Threr are no messages in Queue to display")
					return numMsgs
				for msg in mesgs:
					f = open("/root/test2.txt", 'a')
					attributes = msg.attributes
					senderId = attributes.get('SenderId')
					sentTimestamp = attributes.get('SentTimestamp')

					bd = msg.body
					event = eval(bd)
					jsonmsg = json.loads(event['Message']
					fileName = jsonmsg["Records"][0]["s3"]["object"]["key"])