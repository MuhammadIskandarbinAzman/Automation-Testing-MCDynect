# questions/question.py

from abc import ABC, abstractmethod

class Question(ABC):
    """
    Base class for all Questions in the Screenplay Pattern.
    Questions are used to query the state of the application.
    """
    
    @abstractmethod
    def answered_by(self, actor):
        """
        The logic to answer this question.
        
        Args:
            actor: The Actor who is answering the question
            
        Returns:
            The answer to the question
        """
        pass