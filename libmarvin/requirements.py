import difflib
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
        return {"name": self.name, "unset_msg": self.unset_msg, "set_msg": self.set_msg, "value": self.value,
                "auto_prompt": self.auto_prompt, "options": self.options}

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

    def process_request(self, *args, **kwargs):

        # iterate over requirements
        for requirement in self.requirements:  # type: Requirement

            # if the requirement has no value, we check for if kwargs set it
            if not requirement.value:

                logging.info("examing unmet requirement: %s" % requirement.name)

                # if a requirement "key" is in the kwargs
                if requirement.name in kwargs:

                    logging.info("requirement kwarg: %s is passed" % requirement.name)

                    # if its a multiple choice requirement
                    if requirement.options:

                        logging.info("Searching for close_match in options: %s" % requirement.options)

                        closest_match = difflib.get_close_matches(kwargs[requirement.name], requirement.options)
                        if closest_match:
                            requirement.set(closest_match[0])
                        else:
                            response = "Invalid selection: %s is not in %s" % requirement.options
                            return response
                    else:
                        # set the requirement to the value of the kwarg
                        requirement.set(kwargs[requirement.name])

                    # respond with the set_msg and formatting int he dictionary for any {key} references
                    response = requirement.set_msg.format(**requirement.get())
                else:
                    logging.info("%s not in kw: %s" % (requirement.name, kwargs))
            else:
                # requirement has a value, write it to the response TODO FIXME maybe not do this?
                response = requirement.set_msg.format(**requirement.get())

        # find the next unset value and return a prompt for it
        for requirement in self.requirements:  # type: Requirement
            logging.info("checking for unset requirement: %s" % requirement.name)

            # if the requirement has no value, we check for if kwargs set it
            if not requirement.value and requirement.auto_prompt:
                logging.info("requirement %s not met" % requirement.name)
                return "%s, %s" % (response, requirement.unset_msg.format(**requirement.get()))

        logging.info("No unmet requirements")
        return "All requirements fullfilled"
