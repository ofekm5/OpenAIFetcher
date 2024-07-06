import time

def test_ask_and_fetch_answer(client):
    question_data = {"question": "What is the capital of France?"}
    ask_response = client.post("/ask", json=question_data)
    assert ask_response.status_code == 201
    question_id = ask_response.get_json()["questionID"]

    max_retries = 10
    retry_count = 0
    while retry_count < max_retries:
        fetch_response = client.get(f"/answer?questionID={question_id}")
        if fetch_response.status_code == 200:
            data = fetch_response.get_json()
            if "answer" in data:
                assert data["answer"] == "Paris"
                break
        elif fetch_response.status_code == 404:
            time.sleep(3)
            retry_count += 1
        else:
            assert False, f"Unexpected status code: {fetch_response.status_code}"

    if retry_count == max_retries:
        assert False, "Failed to get a valid answer within the retry limit"

    assert retry_count < max_retries, "Polling exceeded retry limit"
