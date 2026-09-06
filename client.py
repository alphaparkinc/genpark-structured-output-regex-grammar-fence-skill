"""
Structured Output Formatting and Grammar Fence Stripper.
Zero external dependencies, standard library only.
"""

import re
import json
from typing import Dict, Any, Optional

class OutputGrammarFenceClient:
    """
    Cleans raw LLM outputs by removing markdown code fences and isolating structured payloads:
    - Extracts valid JSON from noisy markdown fences (```json ... ```)
    - Validates schema structure
    - Falls back gracefully to heuristic object extraction
    """

    def extract_json(self, raw_text: str) -> Dict[str, Any]:
        """Extracts and parses JSON object from text containing chat narrative or markdown fences."""
        text = raw_text.strip()

        # Try direct parse first
        try:
            return json.loads(text)
        except Exception:
            pass

        # Match ```json ... ``` or ``` ... ```
        fence_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text, re.IGNORECASE)
        if fence_match:
            candidate = fence_match.group(1).strip()
            try:
                return json.loads(candidate)
            except Exception:
                pass

        # Match outermost curly braces
        brace_match = re.search(r"(\{[\s\S]*\})", text)
        if brace_match:
            candidate = brace_match.group(1).strip()
            try:
                return json.loads(candidate)
            except Exception:
                pass

        raise ValueError("No valid JSON payload could be extracted from input text.")

    def enforce_schema_keys(self, data: Dict[str, Any], required_keys: list) -> bool:
        """Validates that all required top-level keys exist."""
        return all(k in data for k in required_keys)
