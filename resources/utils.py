import logging
from random import randint

from django.db import models

logger = logging.getLogger(__name__)


class CreateUniqueCode:
    """
    Utility class for generating unique asset codes.

    This class provides methods to generate unique codes for resources
    with proper error handling and logging.
    """

    @staticmethod
    def generate_unique_code(model_class: models.Model, max_attempts: int = 1000):
        """
        Generate a unique asset code for the given model.

        Args:
            model_class: The Django model class to generate code for
            max_attempts: Maximum number of attempts to generate unique code

        Returns:
            str: A unique asset code

        Raises:
            Exception: If unable to generate unique code after max_attempts
        """
        try:
            for attempt in range(max_attempts):
                random_number = randint(1, 999)
                create_number = f"20000{random_number:03d}"

                if not model_class.objects.filter(asset_code=create_number).exists():
                    logger.info(f"Generated unique code: {create_number}")
                    return create_number

            logger.error(
                f"Failed to generate unique code after {max_attempts} attempts"
            )
            raise Exception(
                "Unable to generate unique code. Please contact administrator."
            )

        except Exception as e:
            logger.error(f"Error generating unique code: {e}")
            raise Exception("Error generating unique code. Please try again.")
