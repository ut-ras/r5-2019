
import threading
import json


class MutexController:
    """Mutex Controller to pass to TaskServer; instantiate with the desired
    semaphores, then pass the handler method as the direct_handler argument.

    Parameters
    ----------
    semaphores : {str: threading.Semaphore} or [str]
        If dictionary, then the passed semaphores are used; if a list,
        semaphores are created with each item as a key.

    Raises
    ------
    TypeError:
        Argument does not follow the specified format
    """

    def __init__(self, semaphores):

        # Dictionary mode
        if type(semaphores) == dict:
            self.semaphores = semaphores

        # List mode
        elif type(semaphores) in [list, tuple]:
            self.semaphores = {s: threading.Semaphore() for s in semaphores}

        else:
            raise TypeError(
                "Argument must be dictionary of threading.Semaphore or list "
                "of strings")

    def __return(self, label, status):
        """Helper function to return json response"""
        return json.dumps({
            "mutex": label,
            "status": status
        })

    def handler(self, t):
        """Handler method to pass as 'direct_handler'

        Parameters
        ----------
        t : Task
            Task object to handle

        Returns
        -------
        str or None
            Json response if valid; else None.
        """

        # Check if label type is 'mutex'
        if t.label != 'mutex':
            return None

        # Check if mutex name is valid
        name = t.meta.get("name")
        if name not in self.semaphores:
            return self.__return(name, False)

        # Process:
        # Acquire
        if t.meta.get("operation") == "acquire":
            return self.__return(name, self.semaphores[name].acquire(False))
        # Release
        else:
            self.semaphores[name].release()
