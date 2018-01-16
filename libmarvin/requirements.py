import logging


class Requirement:
    name = None
    unset_msg = None
    set_msg = None
    value = None
    auto_prompt = None
    options = None

    def __init__(self, name: str, unset_msg: str, set_msg: str, value: object, auto_prompt=True, options=None):
        self.name = name
        self.unset_msg = unset_msg
        self.set_msg = set_msg
        self.value = value
        self.auto_prompt = auto_prompt
        self.options = options
        logging.info(self.get())

    def get(self):
        return {"name": self.name, "unset_msg": self.unset_msg, "set_msg": self.set_msg, "value": self.value, "auto_prompt": self.auto_prompt, "options": self.options}

    def set(self, value):
        self.value = value

    def __call__(self, *args, **kwargs):
        return self.value


class Requirements:
    confirmed = None
    requirements = None

    def __init__(self):
        self.confirmed = False
        self.requirements = []

    def confirm(self):
        self.confirmed = True

    def is_confirmed(self):
        return self.confirmed

    def new_requirement(self, name, unset_msg, set_msg, value, auto_prompt=True, options=None):
        self.requirements.append(Requirement(name, unset_msg, set_msg, value, auto_prompt=auto_prompt, options=options))

    def get_requirement(self, name):
        for r in self.requirements:
            if r.name == name:
                return r
        raise KeyError
