import requests
import uuid

ENDPOINT = 'https://todo.pixegami.io'


def test_can_call_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200


def test_create_task():
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    data = create_task_response.json()
    task_id = data['task']['task_id']
    get_task_response = get_task(task_id)
    assert create_task_response.status_code == 200
    get_task_data = get_task_response.json()
    assert get_task_data['content'] == payload['content']
    assert get_task_data['user_id'] == payload['user_id']


def test_update_task():
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    task_id = create_task_response.json()['task']['task_id']
    updated_payload = {
        "user_id": payload["user_id"],
        "task_id": task_id,
        "content": "updated content",
        "is_done": True,
    }
    update_task_response = update_task(updated_payload)
    assert update_task_response.status_code == 200
    get_updated_task = get_task(task_id)
    assert get_updated_task.status_code == 200
    get_task_data = get_updated_task.json()
    assert get_task_data['content'] == updated_payload['content']
    assert get_task_data['is_done'] == updated_payload['is_done']


def test_list_user_tasks():
    n = 3
    payload = new_task_payload()
    user_id = payload['user_id']
    for task in range(n):
        create_tasks_response = create_task(payload)
        assert create_tasks_response.status_code == 200
    list_tasks_response = list_tasks(user_id)
    assert list_tasks_response.status_code == 200
    data = list_tasks_response.json()
    tasks = data['tasks']
    assert len(tasks) == n


def test_delete_task():
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    task_id = create_task_response.json()['task']['task_id']
    delete_task_response = delete_task(task_id)
    assert delete_task_response.status_code == 200
    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 404


def create_task(payload):
    return requests.put(ENDPOINT + '/create-task', json=payload)


def update_task(payload):
    return requests.put(ENDPOINT + '/update-task', json=payload)


def get_task(task_id):
    return requests.get(ENDPOINT + f'/get-task/{task_id}')


def list_tasks(user_id):
    return requests.get(ENDPOINT + f'/list-tasks/{user_id}')


def delete_task(task_id):
    return requests.delete(ENDPOINT + f'/delete-task/{task_id}')


def new_task_payload():
    user_id = f'test_user_{uuid.uuid4().hex}'
    content = f'test_content_{uuid.uuid4().hex}'
    return {
        "content": content,
        "user_id": user_id,
        "is_done": False,
    }
