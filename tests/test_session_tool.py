import sys
sys.path.append("C:/EIRA")

from tools.session_tool import create_session, save_message, get_messages, delete_session

TEST_USER = "test_user_123"
TEST_SESSION = "test_session_456"

def test_create_session():
    create_session(TEST_SESSION, "Test Chat", TEST_USER)
    messages = get_messages(TEST_SESSION)
    assert messages == []

def test_save_and_get_messages():
    save_message(TEST_SESSION, "user", "hello", "general", "test_model")
    save_message(TEST_SESSION, "assistant", "hi there", "general", "test_model")
    messages = get_messages(TEST_SESSION)
    assert len(messages) == 2
    assert messages[0]["role"] == "user"
    assert messages[1]["role"] == "assistant"

def test_delete_session():
    delete_session(TEST_SESSION, TEST_USER)
    messages = get_messages(TEST_SESSION)
    assert messages == []