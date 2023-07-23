import requests

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

    # data_create = create_task_response.json()
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


def create_task(payload):
    return requests.put(ENDPOINT + '/create-task', json=payload)


def update_task(payload):
    return requests.put(ENDPOINT + '/update-task', json=payload)


def get_task(task_id):
    return requests.get(ENDPOINT + f'/get-task/{task_id}')


def new_task_payload():
    return {
        "content": "some test content",
        "user_id": "test_user",
        "is_done": False,
    }
