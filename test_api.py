"""Checks request validation and the response shape without using a real API key."""

import importlib.util
import json
import os
import sys
import unittest
from unittest.mock import Mock, patch

import types


class FakeRequestError(Exception):
    pass


fake_requests = types.ModuleType("requests")
fake_requests.Timeout = FakeRequestError
fake_requests.ConnectionError = FakeRequestError
fake_requests.HTTPError = FakeRequestError
fake_requests.post = lambda *args, **kwargs: None
sys.modules.setdefault("requests", fake_requests)

spec = importlib.util.spec_from_file_location("improve", "api/improve.py")
improve = importlib.util.module_from_spec(spec)
spec.loader.exec_module(improve)


class ApiTests(unittest.TestCase):
    def test_valid_input(self):
        self.assertEqual(improve.validate_payload({"draft": "  발표 준비 도와줘  ", "purpose": "학습", "format": "목록"}), ("발표 준비 도와줘", "학습", "목록"))

    def test_empty_and_oversized_input(self):
        for draft in ("   ", "a" * 1001):
            with self.subTest(draft_length=len(draft)), self.assertRaises(improve.RequestError):
                improve.validate_payload({"draft": draft})

    def test_invalid_option_type(self):
        with self.assertRaises(improve.RequestError):
            improve.validate_payload({"draft": "안녕", "purpose": []})

    def test_ai_result(self):
        payload = json.dumps({"improved_prompt": "목표와 독자를 밝히고 발표 개요를 작성해줘", "reasons": ["목표를 명시했어요", "형식을 정했어요"]})
        result = improve.parse_ai_result(payload)
        self.assertEqual(len(result["reasons"]), 2)
        self.assertIn("발표 개요", result["improved_prompt"])

    def test_invalid_ai_result(self):
        with self.assertRaises(improve.RequestError):
            improve.parse_ai_result("not json")

    def test_fenced_ai_result(self):
        payload = '```json\n{"improved_prompt":"더 명확하게 작성해줘","reasons":["목표를 추가했어요"]}\n```'
        self.assertEqual(improve.parse_ai_result(payload)["improved_prompt"], "더 명확하게 작성해줘")

    def test_codyssey_request_uses_server_key(self):
        completion = {"choices": [{"message": {"content": json.dumps({"improved_prompt": "발표 개요를 작성해줘", "reasons": ["목표를 밝혔어요"]})}}]}
        response = Mock(status_code=200)
        response.json.return_value = completion
        with patch.dict(os.environ, {"CODYSSEY_API_KEY": "test-only-key"}), patch.object(fake_requests, "post", return_value=response) as post:
            result = improve.improve("발표 준비", "학습", "목록")
        self.assertEqual(result["improved_prompt"], "발표 개요를 작성해줘")
        self.assertEqual(post.call_args.args[0], "https://copa.codyssey.kr/v1/chat/completions")
        self.assertEqual(post.call_args.kwargs["json"]["model"], "gpt-5-mini")
        self.assertEqual(post.call_args.kwargs["headers"]["Authorization"], "Bearer test-only-key")

    def test_missing_key_has_friendly_error(self):
        with patch.dict(os.environ, {"CODYSSEY_API_KEY": ""}), self.assertRaises(improve.RequestError) as caught:
            improve.improve("발표 준비", "", "")
        self.assertEqual(caught.exception.status, 503)


if __name__ == "__main__":
    unittest.main()
