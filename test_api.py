"""Checks request validation and the response shape without using a real API key."""

import importlib.util
import json
import sys
import types
import unittest


class FakeOpenAIError(Exception):
    pass


fake_openai = types.ModuleType("openai")
fake_openai.APIConnectionError = FakeOpenAIError
fake_openai.APIStatusError = FakeOpenAIError
fake_openai.APITimeoutError = FakeOpenAIError
fake_openai.OpenAI = object
sys.modules.setdefault("openai", fake_openai)

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


if __name__ == "__main__":
    unittest.main()
