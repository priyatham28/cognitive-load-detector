name: Bug report
description: Report a reproducible problem in the FLZK demo service
labels: bug
body:
  - type: markdown
    attributes:
      value: |
        Thanks for helping improve the project! Provide as much detail as you can.
  - type: input
    id: summary
    attributes:
      label: Summary
      placeholder: Quick description of the bug
    validations:
      required: true
  - type: textarea
    id: repro
    attributes:
      label: Steps to reproduce
      description: Include commands, payloads, or configuration
      placeholder: "1. ..."
    validations:
      required: true
  - type: textarea
    id: expectation
    attributes:
      label: Expected behaviour
    validations:
      required: true
  - type: textarea
    id: actual
    attributes:
      label: Actual behaviour
    validations:
      required: true
  - type: textarea
    id: logs
    attributes:
      label: Logs / screenshots
      optional: true
  - type: input
    id: env
    attributes:
      label: Environment
      placeholder: Python version, OS, etc.
