"""This module contains the PromptStore class, which implements the storage and retrieval of prompts with different backends."""

from typing import List
from loguru import logger

from promptmage.storage import StorageBackend
from promptmage.prompt import Prompt


class PromptStore:
    """A class that stores and retrieves prompts with different backends."""

    def __init__(self, backend):
        self.backend: StorageBackend = backend

    def store_prompt(self, prompt: Prompt):
        """Store a prompt in the backend."""
        logger.info(f"Storing prompt: {prompt}")
        self.backend.store_prompt(prompt)

    def get_prompt(self, prompt_id: str) -> Prompt:
        """Retrieve a prompt from the backend."""
        logger.info(f"Retrieving prompt with ID: {prompt_id}")
        return self.backend.get_prompt(prompt_id)

    def get_prompts(self) -> List[Prompt]:
        """Retrieve all prompts from the backend."""
        return self.backend.get_prompts()
