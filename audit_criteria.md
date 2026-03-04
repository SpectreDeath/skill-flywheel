# Skill Logic Audit Criteria

To ensure a skill has "solid logic" and functions as intended, it must meet the following criteria:

## 1. Semantic Alignment

* **Purpose matching Name**: The `## Purpose` section must directly support the skill's name.
* **Schema matching Purpose**: The `## Input Format` and `## Output Format` YAML schemas must actually describe data relevant to the skill's purpose. (e.g. A "Security Scan" skill should not have "App Store Deployment" schemas).
* **Capabilities matching Purpose**: The `## Capabilities` must be the actions required to fulfill the purpose.

## 2. Logical Flow (The Workflow)

* **Step-by-Step Feasibility**: Can a machine or human actually execute the `## Workflow` steps as written?
* **Input-to-Output Chain**: Do the inputs provided in the schema realistically lead to the outputs described?
* **Exit Conditions**: Is there a clear end to the workflow?

## 3. Robustness and Safety

* **Constraints**: Are the `## Constraints` specific and enforceable? (e.g. "ALWAYS use relative paths" vs "Be careful").
* **Error Handling**: Does the `## Error Handling` section address likely failures in the `## Workflow`?
* **Edge Cases**: Are there examples of non-standard usage?

## 4. Documentation Quality

* **Clarity**: Is the language unambiguous?
* **Examples**: Do the `## Examples` demonstrate actual usage of the described logic?
