# perturbator

Tool to apply change patterns to your Business Process Models

## Dependencies:
`python3`
`pip3`

## Setup
`pip3 install perturbator`

## Insert Element
### Documentation
`perturbator insert-element --help`

### Options:

  `--insert-to`     BPMN File Path in which element has to be inserted      [required]

  `--element-type`   Type of element to be inserted                         [required]

  `--output-file`   Path of BPMN file in which to output                    [required]

  `--insert-at`     ID of the FLOW where the process has to be inserted     [required]

### Sample Command:
`perturbator insert-element --insert-to ~/Desktop/input1.bpmn --element-type task --insert-at flow11  --output-file ~/Desktop/output.bpmn`


## Delete/Skip Element
### Documentation
`perturbator delete-element --help`

### Options:

  `--delete-from`   BPMN File Path from which element has to be skipped     [required]

  `--element-id`    ID of Element to be deleted                             [required]

  `--output-file`   Path of BPMN file in which to output                    [required]

### Sample Command:
`perturbator delete-element --delete-from ~/Desktop/input1.bpmn --element-id task11 --output-file ~/Desktop/output.bpmn`


## Insert Process Fragment (Serial)
### Documentation
`perturbator insert-process-fragment-serial --help`

### Options:

  `--insert-to`     BPMN File Path in which process has to be inserted      [required]

  `--insert-from`   BPMN File Path from which process has to be inserted    [required]

  `--output-file`   Path of BPMN file in which to output                    [required]

  `--insert-at`     ID of the FLOW where the process has to be inserted     [required]

### Sample Command:
`perturbator insert-process-fragment-serial --insert-to ~/Desktop/input1.bpmn --insert-at flow12 --insert-from ~/Desktop/input2.bpmn --output-file ~/Desktop/output.bpmn `


## Insert Process Fragment (Parallel Branch)
### Documentation
`perturbator insert-process-fragment-parallel --help`

### Options:

  `--insert-to`     BPMN File Path in which process has to be inserted      [required]

  `--insert-from`   BPMN File Path from which process has to be inserted    [required]

  `--output-file`   Path of BPMN file in which to output                    [required]

  `--branch-start`  ID of the FLOW where the branching starts               [required]

  `--branch-end`    ID of the FLOW where the branching starts               [required]

### Sample Command:
`perturbator insert-process-fragment-parallel --insert-to ~/Desktop/input1.bpmn --insert-from ~/Desktop/input2.bpmn --output-file ~/Desktop/output.bpmn --branch-start flow11 --branch-end flow13`


## Insert Process Fragment (Conditional Branch)
### Documentation
`perturbator insert-process-fragment-conditional --help`

### Options:

  `--insert-to`     BPMN File Path in which process has to be inserted      [required]

  `--insert-from`   BPMN File Path from which process has to be inserted    [required]

  `--output-file`   Path of BPMN file in which to output                    [required]

  `--branch-start`  ID of the FLOW where the branching starts               [required]

  `--branch-end`    ID of the FLOW where the branching starts               [required]

### Sample Command:
`perturbator insert-process-fragment-conditional --insert-to ~/Desktop/input1.bpmn --insert-from ~/Desktop/input2.bpmn --output-file ~/Desktop/output.bpmn --branch-start flow11 --branch-end flow13`


## Delete/Skip Process Fragment
### Documentation
`perturbator delete-process-fragment --help`

### Options:

  `--delete-from`   BPMN File Path from which process fragment has to be deleted    [required]

  `--output-file`   Path of BPMN file in which to output                            [required]

  `--branch-start`  ID of the FLOW where the branching starts                       [required]

  `--branch-end`    ID of the FLOW where the branching starts                       [required]

### Sample Command:
`perturbator delete-process-fragment --delete-from ~/Desktop/input1.bpmn  --output-file ~/Desktop/output.bpmn --branch-start flow11 --branch-end flow13`

## Run commands in batches
Add commands in a text format in any text file and execute to trigger multiple steps in one go

### Sample Command:
`perturbator execute-from-file --command-file ~/Desktop/commands.txt`

### Format of commands in file:

```
insert 'task' to process in file '~/Desktop/input1.bpmn' at flow 'flow11' and output in '~/Desktop/output.bpmn'
delete element with id 'task11' from process in file '~/Desktop/output.bpmn' and output in '~/Desktop/output.bpmn'


serial insert process from '~/Desktop/input2.bpmn' to process in file '~/Desktop/output.bpmn' at flow 'flow12' and output in '~/Desktop/output.bpmn'
conditionally insert process from '~/Desktop/input2.bpmn' to process in file '~/Desktop/input1.bpmn' between 'flow11' and 'flow13' and output in '~/Desktop/output.bpmn'
parallel insert process from '~/Desktop/input2.bpmn' to process in file '~/Desktop/input1.bpmn' between 'flow11' and 'flow13' and output in '~/Desktop/output.bpmn'
delete process fragment from process in file '~/Desktop/input1.bpmn' between 'flow11' and 'flow13' and output in '~/Desktop/output.bpmn'
```
