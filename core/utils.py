import logging

logger = logging.getLogger(__name__)


class CleanData(str):
    """
    Utility class for cleaning string data.
    """

    def created_clean(self):
        """
        Clean string data by converting to lowercase and removing spaces.

        Returns:
            str: Cleaned string
        """
        try:
            return "".join(self.lower().split())
        except Exception as e:
            logger.error(f"Error cleaning data: {e}")
            return str(self)
