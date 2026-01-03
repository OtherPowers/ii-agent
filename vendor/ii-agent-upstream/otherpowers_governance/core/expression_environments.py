from enum import Enum


class ExpressionEnvironment(str, Enum):
    """
    Describes *how* intelligence is allowed to express itself,
    not how much power it has.
    """

    EXPANDED = "expanded_expression"
    STANDARD = "standard_expression"
    LEARNING = "learning_expression"
    EMERGENT = "emergent_expression"
    OBSERVATIONAL = "observational_expression"
    UNCLASSIFIED = "unclassified_expression"

