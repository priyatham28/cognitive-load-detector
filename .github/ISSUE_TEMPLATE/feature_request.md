name: Feature request
description: Suggest an enhancement for the FLZK demo service
labels: enhancement
body:
  - type: markdown
    attributes:
      value: "We love ambitious ideas!"
  - type: input
    id: title
    attributes:
      label: Feature title
    validations:
      required: true
  - type: textarea
    id: problem
    attributes:
      label: Problem statement
      description: What pain point does this solve?
    validations:
      required: true
  - type: textarea
    id: proposal
    attributes:
      label: Proposed solution
      description: Outline the change, API, or UX.
    validations:
      required: true
  - type: textarea
    id: alternatives
    attributes:
      label: Alternatives considered
  - type: textarea
    id: notes
    attributes:
      label: Additional context / references
