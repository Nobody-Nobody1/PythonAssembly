# HOW TO USE
- Download the exe file in dist folder and run from file explorer since it's not signed
- use the run and debug for VmExecuter in vscode to run it by editing Bytecode.txt
- use the run and debug for Tkinter ide in vscode to get a code IDE and click file to provide options for editing Bytecode.txt
- has most of the same basic stuff as python and other languages
- Check VMPython.py in the class Commands for a full list of all commands

# MISTAKES
- SAVE CHANGES TO BYTECODE.TXT BEFORE EXECUTING IT IN THE CODE IDE

## Instruction set reference

Below are the supported commands, parameters and examples.

General token notation:
- `reg` or `register`: a register name (string). Registers are key/value entries in a dictionary inside the VM.
- `value`: numeric literal (e.g., `5`) or a register name (the VM will read the register value).
- `token`: may be a literal or a register name. The VM evaluates tokens at runtime when appropriate.

Arithmetic and register operations
- `["ADDITION", value1, value2, target_reg]`
  - Adds `value1 + value2` (both literals) and stores result in `target_reg`.
  - Example: `["ADDITION", "2", "3", "sum"]` → `sum = 5`
- `["ADDITION_REGISTER", reg1, reg2, target_reg]`
  - Adds values taken from `reg1` and `reg2`.
  - Example: `["ADDITION_REGISTER", "a", "b", "c"]`
- `["SUBTRACT", v1, v2, target_reg]`
- `["SUBTRACT_REGISTER", reg1, reg2, target_reg]`
- `["MULTIPLY", v1, v2, target_reg]`
- `["MULTIPLY_REGISTER", reg1, reg2, target_reg]`
- `["DIVIDE", v1, v2, target_reg]`
  - Integer (floor) division is used in the VM implementation.
- `["DIVIDE_REGISTER", reg1, reg2, target_reg]`

Storing and printing
- `["STORE", register, value_or_register]`
  - Stores the evaluated operand into `register`. Example: `["STORE", "x", "5"]` or `["STORE", "x", "y"]` to copy `y` into `x`.
- `["PRINT", register_or_value]`
  - Prints the evaluated operand to stdout.
  - Example: `["PRINT", "x"]` or `["PRINT", "hello"]` (strings are printed as-is).

Comments & markers
- `["COMMENT", ...]`
  - Ignored by the VM.
- `["MARK", name]`
  - Registers a marker at the current bytecode index (useful for future jump/GOTO additions).
  - Example: `["MARK", "loop_top"]`

Comparison and logical
- `["COMPARE", v1, v2]`
  - Compares two literals and stores result in `CompareFlag` (1 if equal, 0 otherwise).
- `["COMPARE_REGISTER", reg1, reg2]`
  - Compares values in registers and sets `CompareFlag`.
- `["LOGICAL_OPERATION", op, reg1, reg2?]`
  - Supported ops: `AND`, `OR`, `NOT`.
  - Example: `["LOGICAL_OPERATION", "AND", "flag1", "flag2"]`
  - Result stored in `LOGIC_FLAG` register.

Control flow / Blocks (register-aware)
The VM implements block-based control flow using matching `LOOP_END` tokens. Blocks are started with `IF`, `WHILE`, or `FOR`, and ended with `LOOP_END`.

- `["IF", left_token, op, right_token]`
  - Executes the block between `IF` and the matching `LOOP_END` only if the condition is true.
  - Supported operators: `==`, `=`, `EQ`, `!=`, `NE`, `>`, `<`, `>=`, `<=`, textual `GT`/`LT`/`GTE`/`LTE`, and logical `AND`/`OR` (for compound usage).
  - Example:
    ```
    ["IF", "x", "==", "0"]
    ["PRINT", "zero"]
    ["LOOP_END"]
    ```

- `["WHILE", left_token, op, right_token]`
  - Re-evaluates the condition each iteration. `left_token` and `right_token` can be register names or literals. The VM re-evaluates register tokens on each loop iteration, so changing a register inside the loop affects the loop.
  - Example:
    ```
    ["STORE", "x", "5"]
    ["WHILE", "x", ">", "0"]
    ["PRINT", "x"]
    ["SUBTRACT_REGISTER", "x", "1", "x"]
    ["LOOP_END"]
    ```

- `["FOR", loop_register, start_token, end_token, step_token?]`
  - The FOR instruction is register-aware:
    - `loop_register`: name of the register used as loop index (the VM will initialize this register to the evaluated `start_token`).
    - `start_token`, `end_token`, `step_token`: each may be a literal or a register name. The VM evaluates them when needed:
      - `start_token` is evaluated once to initialize the loop register.
      - `end_token` and `step_token` are re-evaluated each iteration, so they can be registers that change during the loop.
    - `step_token` defaults to `1` if omitted.
  - Example using registers:
    ```
    ["STORE", "start", "1"]
    ["STORE", "end", "3"]
    ["STORE", "step", "1"]
    ["FOR", "i", "start", "end", "step"]
    ["PRINT", "i"]
    ["LOOP_END"]
    ```
  - Example using literals:
    ```
    ["FOR", "i", "1", "5", "1"]
    ["PRINT", "i"]
    ["LOOP_END"]
    ```

- `["LOOP_END"]`
  - Ends `IF`, `WHILE`, or `FOR` blocks. Behavior:
    - For `IF`: simply marks the end of the conditional block.
    - For `WHILE`: re-evaluates the condition and jumps back if true.
    - For `FOR`: increments the loop register by `step` and re-evaluates the `end`/`step` tokens (both can be registers).

Notes about register usage in loops
- The VM prefers register names for `start`, `end`, and `step` tokens. If a token is a literal, it is used as a literal value.
- Because `end` and `step` are re-evaluated every iteration (when they are register names), you can change them inside the loop to dynamically affect iteration behavior.
- All numeric arithmetic in the VM uses integer conversion (and integer division for DIVIDE/DIVIDE_REGISTER).

---

## Example programs

1) FOR loop with registers (print 1..3)

ByteCode.txt:
```
["STORE", "start", "1"]
["STORE", "end", "3"]
["STORE", "step", "1"]
["FOR", "i", "start", "end", "step"]
["PRINT", "i"]
["LOOP_END"]
```

2) WHILE loop using register `x`

```
["STORE", "x", "5"]
["WHILE", "x", ">", "0"]
["PRINT", "x"]
["SUBTRACT_REGISTER", "x", "1", "x"]
["LOOP_END"]
```

3) IF example

```
["STORE", "x", "0"]
["IF", "x", "==", "0"]
["PRINT", "zero"]
["LOOP_END"]
```

---

## Debugging tips

- If nothing prints, verify `ByteCode.txt` is present and readable.
- If the VM raises a "without matching LOOP_END" exception, check that every `IF`, `WHILE`, and `FOR` has a corresponding `LOOP_END`, and that nested blocks are balanced.
- Use `PRINT` liberally to inspect register values inside loops and to print the full set of registers at the end of the program execution.

---

## Contributing

- Pull requests welcome.
- Make sure to credit me as the author
---

## License

- Meant to be used personally and all changes can be made given the original author (Nobody_Nobody1) is credited
---