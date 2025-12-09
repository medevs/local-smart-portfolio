"""
Input guardrails for protecting the LLM from prompt injection and abuse.
Implements security best practices for AI applications.
"""

import re
from typing import Tuple, Optional, List
from dataclasses import dataclass
from enum import Enum

from app.utils.logger import logger


class ThreatLevel(Enum):
    """Threat level classification for detected issues."""
    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class GuardrailResult:
    """Result of a guardrail check."""
    is_safe: bool
    threat_level: ThreatLevel
    reason: Optional[str] = None
    detected_patterns: Optional[List[str]] = None


class InputGuardrails:
    """
    Input validation and sanitization for LLM queries.
    Detects and blocks potential prompt injection attempts.
    """

    # Patterns that indicate prompt injection attempts
    INJECTION_PATTERNS = [
        # Instruction override attempts
        (r"ignore\s+(all\s+)?(previous|prior|above|earlier)\s+(instructions?|prompts?|rules?)", ThreatLevel.HIGH),
        (r"disregard\s+(your|the|all)\s+(system|initial|original)\s+(prompt|instructions?)", ThreatLevel.HIGH),
        (r"forget\s+(everything|all|your)\s+(you|about|instructions?)", ThreatLevel.HIGH),

        # Role manipulation
        (r"you\s+are\s+now\s+", ThreatLevel.HIGH),
        (r"act\s+as\s+(if\s+you\s+are\s+|a\s+)", ThreatLevel.MEDIUM),
        (r"pretend\s+(to\s+be|you'?re)", ThreatLevel.MEDIUM),
        (r"roleplay\s+as", ThreatLevel.MEDIUM),
        (r"assume\s+the\s+role\s+of", ThreatLevel.MEDIUM),

        # System prompt extraction
        (r"(what|show|tell|reveal|display)\s+(is|me|us)?\s*(your|the)\s+(system|initial|original)\s+(prompt|instructions?)", ThreatLevel.HIGH),
        (r"(print|output|echo)\s+(your|the)\s+(system|initial)\s+(prompt|instructions?)", ThreatLevel.HIGH),

        # Jailbreak markers
        (r"\[INST\]", ThreatLevel.CRITICAL),
        (r"<<SYS>>", ThreatLevel.CRITICAL),
        (r"\[/INST\]", ThreatLevel.CRITICAL),
        (r"<</SYS>>", ThreatLevel.CRITICAL),
        (r"<\|im_start\|>", ThreatLevel.CRITICAL),
        (r"<\|im_end\|>", ThreatLevel.CRITICAL),

        # Known jailbreak names
        (r"\bDAN\b", ThreatLevel.MEDIUM),
        (r"\bJailbreak", ThreatLevel.MEDIUM),
        (r"developer\s+mode", ThreatLevel.MEDIUM),

        # Prompt leaking techniques
        (r"repeat\s+(back|after|everything)", ThreatLevel.MEDIUM),
        (r"say\s+\"[^\"]*system", ThreatLevel.MEDIUM),
    ]

    # Maximum input length (characters)
    MAX_INPUT_LENGTH = 10000

    # Minimum input length (for meaningful queries)
    MIN_INPUT_LENGTH = 2

    def __init__(self):
        # Compile patterns for efficiency
        self.compiled_patterns = [
            (re.compile(pattern, re.IGNORECASE), level)
            for pattern, level in self.INJECTION_PATTERNS
        ]

    def check_input(self, text: str) -> GuardrailResult:
        """
        Check input text for potential security issues.

        Args:
            text: User input to validate

        Returns:
            GuardrailResult with safety status and details
        """
        # Check length constraints
        if len(text) > self.MAX_INPUT_LENGTH:
            return GuardrailResult(
                is_safe=False,
                threat_level=ThreatLevel.MEDIUM,
                reason=f"Input too long (max {self.MAX_INPUT_LENGTH} characters)",
            )

        if len(text.strip()) < self.MIN_INPUT_LENGTH:
            return GuardrailResult(
                is_safe=False,
                threat_level=ThreatLevel.LOW,
                reason="Input too short",
            )

        # Check for injection patterns
        detected = []
        max_threat = ThreatLevel.NONE

        for pattern, threat_level in self.compiled_patterns:
            if pattern.search(text):
                detected.append(pattern.pattern)
                if threat_level.value > max_threat.value:
                    max_threat = threat_level

        if detected:
            logger.warning(
                f"Potential prompt injection detected. "
                f"Threat: {max_threat.value}, Patterns: {len(detected)}"
            )
            return GuardrailResult(
                is_safe=False,
                threat_level=max_threat,
                reason="Potential prompt injection detected",
                detected_patterns=detected,
            )

        # Check for excessive special characters (potential obfuscation)
        special_ratio = len(re.findall(r'[^\w\s]', text)) / max(len(text), 1)
        if special_ratio > 0.3:
            return GuardrailResult(
                is_safe=False,
                threat_level=ThreatLevel.LOW,
                reason="Excessive special characters detected",
            )

        return GuardrailResult(
            is_safe=True,
            threat_level=ThreatLevel.NONE,
        )

    def sanitize_input(self, text: str) -> str:
        """
        Sanitize input text by removing potentially dangerous content.

        Args:
            text: User input to sanitize

        Returns:
            Sanitized text
        """
        # Remove null bytes
        text = text.replace('\x00', '')

        # Normalize whitespace
        text = ' '.join(text.split())

        # Remove control characters (except newlines and tabs)
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)

        # Truncate if too long
        if len(text) > self.MAX_INPUT_LENGTH:
            text = text[:self.MAX_INPUT_LENGTH]

        return text


class OutputGuardrails:
    """
    Output validation to prevent sensitive information leakage.
    """

    # Patterns that shouldn't appear in outputs
    SENSITIVE_PATTERNS = [
        r"api[_\s]?key\s*[:=]\s*['\"][^'\"]+['\"]",
        r"password\s*[:=]\s*['\"][^'\"]+['\"]",
        r"secret\s*[:=]\s*['\"][^'\"]+['\"]",
        r"token\s*[:=]\s*['\"][^'\"]+['\"]",
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",  # Email
    ]

    def __init__(self):
        self.compiled_patterns = [
            re.compile(pattern, re.IGNORECASE)
            for pattern in self.SENSITIVE_PATTERNS
        ]

    def check_output(self, text: str) -> GuardrailResult:
        """
        Check output text for sensitive information.

        Args:
            text: LLM output to validate

        Returns:
            GuardrailResult with safety status
        """
        for pattern in self.compiled_patterns:
            if pattern.search(text):
                logger.warning("Sensitive information detected in output")
                return GuardrailResult(
                    is_safe=False,
                    threat_level=ThreatLevel.HIGH,
                    reason="Potential sensitive information in output",
                )

        return GuardrailResult(
            is_safe=True,
            threat_level=ThreatLevel.NONE,
        )

    def redact_sensitive(self, text: str) -> str:
        """
        Redact sensitive information from output.

        Args:
            text: Text to redact

        Returns:
            Redacted text
        """
        for pattern in self.compiled_patterns:
            text = pattern.sub("[REDACTED]", text)
        return text


# Singleton instances
_input_guardrails: Optional[InputGuardrails] = None
_output_guardrails: Optional[OutputGuardrails] = None


def get_input_guardrails() -> InputGuardrails:
    """Get singleton InputGuardrails instance."""
    global _input_guardrails
    if _input_guardrails is None:
        _input_guardrails = InputGuardrails()
    return _input_guardrails


def get_output_guardrails() -> OutputGuardrails:
    """Get singleton OutputGuardrails instance."""
    global _output_guardrails
    if _output_guardrails is None:
        _output_guardrails = OutputGuardrails()
    return _output_guardrails


def validate_chat_input(message: str) -> Tuple[bool, Optional[str]]:
    """
    Convenience function to validate chat input.

    Args:
        message: User message to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    guardrails = get_input_guardrails()
    result = guardrails.check_input(message)

    if not result.is_safe:
        return False, result.reason

    return True, None
