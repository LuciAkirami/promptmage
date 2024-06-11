"""This module contains the PromptStore class, which implements the storage and retrieval of prompts with different backends."""

from typing import List
from loguru import logger

from promptmage.storage import StorageBackend
from promptmage.prompt import Prompt
from promptmage.exceptions import PromptNotFoundException


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
        try:
            return self.backend.get_prompt(prompt_id)
        except PromptNotFoundException:
            logger.error(
                f"Prompt with ID {prompt_id} not found, returning an empty prompt."
            )
            # return an empty prompt if the prompt is not found
            return Prompt(
                name=prompt_id,
                version=1,
                system="You are a helpful assistant.",
                user="",
                template_vars=[],
            )

    def get_prompts(self) -> List[Prompt]:
        """Retrieve all prompts from the backend."""
        return self.backend.get_prompts()

    def delete_prompt(self, prompt_id: str):
        """Delete a prompt from the backend."""
        logger.info(f"Deleting prompt with ID: {prompt_id}")
        self.backend.delete_prompt(prompt_id)
