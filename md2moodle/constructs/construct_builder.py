"""Construct Builder - where the information that comes in via JSON gets
translated into classes that will parse and act on the text.

If there is a new construct type, or new rule, this is where it should go.
"""

from md2moodle.parsing.tokens import Token, Token_type_enum
from md2moodle.constructs.elements import Default_element, Prefix_inline_element
from md2moodle.constructs.action import Action, Action_type

from md2moodle.rule_reader.file_reader import File_reader


class Construct_builder:
    def __init__(self, path: str):
        self.constructs: list = []
        rule_reader = File_reader(path)
        self.rules = rule_reader.get_rules()
        self.built = False

    def _build_token(self, token_dict):
        return Token(token_dict["type"], token_dict["pattern"])

    def _build_action(self, action_dict):
        return Action(Action_type[action_dict["type"]], **action_dict)

    def build(self):
        if self.built == False:
            for rule in self.rules:

                # DEFAULT
                if rule["element_type"] == "default":
                    start_tag = Token(
                        token_type=Token_type_enum.START_TAG,
                        pattern=rule["tokens"]["start_tag"],
                    )

                    end_tag = Token(
                        token_type=Token_type_enum.END_TAG,
                        pattern=rule["tokens"]["end_tag"],
                    )

                    element = Default_element(
                        name=rule["name"],
                        start_tag=start_tag,
                        end_tag=end_tag,
                        actions=rule["actions"],
                    )

                    element.start_tag.add_parent(element)
                    element.end_tag.add_parent(element)

                # PREFIX INLINE
                elif rule["element_type"] == "standalone_prefix":
                    if len(rule["tokens"]) > 1:
                        raise Exception(
                            "standalone elements should have only one token"
                        )

                    prefix = Token(
                        token_type=Token_type_enum.PREFIX,
                        pattern=rule["tokens"]["prefix"],
                    )

                    element = Prefix_inline_element(
                        name=rule["name"], prefix=prefix, actions=rule["actions"]
                    )

                    element.prefix.add_parent(element)

                self.constructs.append(element)
            self.built = True
        return self.constructs
