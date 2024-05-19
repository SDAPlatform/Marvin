import json
import datetime
from datetime import datetime
import platform

from typing import Optional

from phi.tools.toolkit import Toolkit
from phi.tools import Toolkit
from phi.utils.log import logger
from phi.knowledge.base import AssistantKnowledge

class MarvinCore(Toolkit):
    def __init__(
        self,
        knowledge_base: AssistantKnowledge,
        fixed_max_results: Optional[int] = None,
        timeout: Optional[int] = 10,
    ):
        super().__init__(name="MarvinCore")
        self.knowledge_base: Optional[AssistantKnowledge] = knowledge_base
        self.timeout: Optional[int] = timeout
        self.fixed_max_results: Optional[int] = fixed_max_results
        self.register(self.save_knowledge)
        self.register(self.get_current_datetime)
        self.register(self.get_current_os)
        


    def save_knowledge(self, knowledge: str) -> str:
        """Use this function to save all details about user , any specefic detail of user and his sibilings like facts, gender, cermonies, personal information (including but not limited to name ) and others must be saved with this function. think of it as the encyclopedia of the user
        every detail in the function should be specefic , use other tools to resolve for people name and/or date and time, datetime should be specefic and not like relative words

        Args:
            knowledge(str): The knowledge you have learnt in one sentence.

        Returns:
            'true' when it is finished saving the knowledge.
        """
        self.knowledge_base.load_text(knowledge)
        logger.debug(f"saving knowledge : {knowledge}")
        return json.dumps(True, indent=2)
    
    def get_current_datetime(self) -> str:
        """Use this function whenever you need to know the current date and time.
        Args:
            nothing

        Returns:
            date and time in this format "YYYY-MM-DD HH:MM:SS.microseconds"
        """

        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        logger.debug(f"informing time to assistance ")
        return json.dumps(formatted_datetime, indent=2)
    
    def get_current_os(self) -> str:
        """Get the current operating system.
        Returns:
            The name of the current operating system.
        """
        current_os = platform.system()
        logger.debug("Retrieving current operating system.")
        return json.dumps(current_os, indent=2)

