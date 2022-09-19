import os
import sys
from enum import Enum


def set_current_directory():
    # determine if application is a script file or frozen exe
    if getattr(sys, 'frozen', False):
        application_path = os.path.abspath(sys.executable)
    elif __file__:
        application_path = os.path.abspath(__file__)

    directory = os.path.dirname(application_path)
    # set current directory
    os.chdir(directory)
    return directory


class Task:
    def __init__(self, instance_name, process_name, parameters):
        self.instance_name = instance_name
        self.process_name = process_name
        self.parameters = parameters

    def translate_to_line(self):
        return 'instance="{instance}" process="{process}" {parameters}\n'.format(
            instance=self.instance_name,
            process=self.process_name,
            parameters=' '.join('{}="{}"'.format(parameter, value) for parameter, value in self.parameters.items()))


class OptimizedTask(Task):
    def __init__(self, task_id, instance_name, process_name, parameters, predecessors, require_predecessor_success):
        super().__init__(instance_name, process_name, parameters)
        self.id = task_id
        self.predecessors = predecessors
        self.require_predecessor_success = require_predecessor_success
        self.successors = list()

    @property
    def has_predecessors(self):
        return len(self.predecessors) > 0

    @property
    def has_successors(self):
        return len(self.successors) > 0


class ExecutionMode(Enum):
    NORM = 1
    OPT = 2

    @classmethod
    def _missing_(cls, value):
        for member in cls:
            if member.name.lower() == value.lower():
                return member
        # default
        return cls.NORM
