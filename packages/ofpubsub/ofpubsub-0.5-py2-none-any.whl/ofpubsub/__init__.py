import requests

class Kafka:
  def __init__(self, access_key, secret_key):
    self.access_key = access_key
    self.secret_key = secret_key
    self.url = "http://" + access_key + ":8080"

  def publish(self, topic, key, message):
    data = { 'records': [{ 'topic': topic, 'key': key, 'message': message} ]}
    headers = { 'is-system': 'true', 'secret-key': self.secret_key }
    return requests.post(self.url + "/topics/" + topic, json = data, headers = headers)
    

class RabbitMQ:
  def __init__(self, access_key, secret_key):
    self.access_key = access_key
    self.secret_key = secret_key
    self.url = "http://" + access_key + ":8080"

  def publish(self, topic, message):
    data = { 'queue': topic, 'content': message }
    headers = { 'is-system': 'true', 'secret-key': self.secret_key }
    return requests.post(self.url + "/publish", json = data, headers = headers)
    