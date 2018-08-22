from locust import HttpLocust, TaskSet, task
import random
import json
import time
from faker import Faker
fake = Faker()

max_id=1
test_index='esbench_test'
json_headers={'content-type': 'application/json'}
multi_json_headers={'content-type': 'application/x-ndjson'}

def fake_product():
  doc = {
    'name': fake.name(),
    'description': fake.sentence(),
    'code': fake.itin(),
    'brand': fake.company(),
    'price': random.random() * 100.0,
    'count_available': random.randint(0,10),
  }
  return doc

def fake_update():
  return {
    'price':random.random() * 100.0,
    'count_available': random.randint(0,10),
  }

class UpdateLoadTasks(TaskSet):
  def on_start(self):
    while True:
      try:
        if self.client.get("/_cluster/health", name="wait_for_startup").status_code == 200:
          return
        time.sleep(5)
      except Exception as err:
        print(err)

  @task(1)
  def create(self):
    global max_id
    id=max_id
    doc = fake_product()
    response = self.client.put(
        "/%s/test/%i" % (test_index, id),
        data=json.dumps(doc),
        headers=json_headers,
        name="create")
    if response.status_code > 300:
      print(response.content)
    else:
      max_id+=1


  @task(1)
  def fetch(self):
    if max_id == 1:
      self.create()
    else:
      id = random.randint(1, max_id-1)
      response = self.client.get("/%s/test/%i" % (test_index, id), name="fetch")
      if response.status_code > 300:
        print(response.content)

  @task(30)
  def bulk_update(self):
    if max_id < 10:
      self.create()
    else:
      updates=[
        "{ \"update\": {\"_index\":\"%s\", \"_type\": \"test\", \"_id\":%i} }\n{\"doc\":%s}" % 
        (test_index, random.randint(1, max_id-1), json.dumps(fake_update())) for i in range(1,20)
      ]
      update_body="\n".join(updates)+"\n"
      # print(update_body)
      response = self.client.post("/_bulk",
        data=update_body,
        headers=json_headers,
        name="bulk_update")
      if response.status_code > 300:
        print(response.content)

class WebsiteUser(HttpLocust):
    min_wait = 20
    max_wait = 50
    task_set = UpdateLoadTasks