import sys

# Detect Pyodide (browser)
BROWSER_MODE = sys.platform == "emscripten"

# Desktop-only imports (flexible)
if not BROWSER_MODE:
    try:
        from src.ByteCodeReader import Reader
    except ImportError:
        from ByteCodeReader import Reader


class Commands:
    ADDITION = 'ADDITION'
    ADDITION_REGISTER = 'ADDITION_REGISTER'
    SUBTRACT = 'SUBTRACT'
    SUBTRACT_REGISTER = 'SUBTRACT_REGISTER'
    MULTIPLY = 'MULIPLY'
    MULTIPLY_REGISTER = 'MULTIPLY_REGISTER'
    DIVIDE = 'DIVIDE'
    DIVIDE_REGISTER = 'DIVIDE_REGISTER'
    COMPARE = 'COMPARE'
    COMPARE_REGISTER = 'COMPARE_REGISTER'
    LOGICAL_OPERATIONS = 'LOGICAL_OPERATION'
    STORE = 'STORE'
    PRINT = 'PRINT'
    COMMENT = 'COMMENT'
    MARK = 'MARK'
    IF = 'IF'
    WHILE = 'WHILE'
    FOR = 'FOR'
    LOOP_END = 'LOOP_END'
    DECIMAL_CONVERT = 'DECIMAL_CONVERT'


class VmExecuter:
    def __init__(self, force_buffer=False):
        # When force_buffer is True, all output goes to output_buffer (no printing to terminal)
        self.force_buffer = force_buffer
        self.Registers = {
            'COMPAREFLAG': 0,
            'LOGIC_FLAG': False,
            'BINARY_FLAG': "",
            'HEXADECIMAL_FLAG': ""
        }
        self.Markers = {}
        self.LoopStack = []
        self.output_buffer = []

    # ---------------- OUTPUT ----------------

    def _write(self, text):
        # Force buffer mode overrides everything
        if getattr(self, "force_buffer", False):
            self.output_buffer.append(str(text))
            return

        # Browser mode also uses buffer
        if BROWSER_MODE:
            self.output_buffer.append(str(text))
        else:
            print(text)

    def get_output(self):
        return "\n".join(self.output_buffer)

    # ---------------- HELPERS ----------------

    def eval_operand(self, token):
        if token is None:
            return None
        token_str = str(token)
        if token_str in self.Registers:
            return self.Registers[token_str]
        try:
            return int(token_str)
        except:
            return token_str

    def eval_int(self, token):
        return int(self.eval_operand(token))

    def eval_condition(self, left_tok, op_tok, right_tok):
        left = self.eval_operand(left_tok)
        right = self.eval_operand(right_tok)
        op = str(op_tok).strip()

        try:
            if isinstance(left, str) and left.isdigit():
                left = int(left)
            if isinstance(right, str) and right.isdigit():
                right = int(right)
        except:
            pass

        if op in ('==', 'EQ', '='):
            return left == right
        if op in ('!=', 'NE'):
            return left != right
        if op in ('>', 'GT'):
            return left > right
        if op in ('<', 'LT'):
            return left < right
        if op in ('>=', 'GTE'):
            return left >= right
        if op in ('<=', 'LTE'):
            return left <= right
        if op.upper() == 'AND':
            return bool(left) and bool(right)
        if op.upper() == 'OR':
            return bool(left) or bool(right)

        return left == right

    def find_matching_end(self, bytecode, start_ip):
        depth = 0
        ip = start_ip
        while ip < len(bytecode):
            instr = bytecode[ip]
            if not instr:
                ip += 1
                continue
            name = str(instr[0]).upper()
            if name in (Commands.IF, Commands.WHILE, Commands.FOR):
                depth += 1
            elif name == Commands.LOOP_END:
                if depth == 0:
                    return ip
                depth -= 1
            ip += 1
        return None

    # ---------------- EXECUTION ----------------

    def execute(self, bytecode):
        ip = 0

        while ip < len(bytecode):
            instruction = bytecode[ip]
            if not instruction:
                ip += 1
                continue

            name = str(instruction[0]).upper()

            # --- ARITHMETIC ---
            if name == Commands.ADDITION:
                self.Registers[instruction[3]] = int(instruction[1]) + int(instruction[2])
                ip += 1

            elif name == Commands.ADDITION_REGISTER:
                self.Registers[instruction[3]] = int(self.Registers[instruction[1]]) + int(self.Registers[instruction[2]])
                ip += 1

            elif name == Commands.SUBTRACT:
                self.Registers[instruction[3]] = int(instruction[1]) - int(instruction[2])
                ip += 1

            elif name == Commands.SUBTRACT_REGISTER:
                self.Registers[instruction[3]] = int(self.Registers[instruction[1]]) - int(self.Registers[instruction[2]])
                ip += 1

            elif name == Commands.MULTIPLY:
                self.Registers[instruction[3]] = int(instruction[1]) * int(instruction[2])
                ip += 1

            elif name == Commands.MULTIPLY_REGISTER:
                self.Registers[instruction[3]] = int(self.Registers[instruction[1]]) * int(self.Registers[instruction[2]])
                ip += 1

            elif name == Commands.DIVIDE:
                self.Registers[instruction[3]] = int(instruction[1]) // int(instruction[2])
                ip += 1

            elif name == Commands.DIVIDE_REGISTER:
                self.Registers[instruction[3]] = int(self.Registers[instruction[1]]) // int(self.Registers[instruction[2]])
                ip += 1

            # --- COMPARE ---
            elif name == Commands.COMPARE:
                self.Registers['COMPAREFLAG'] = 1 if int(instruction[1]) == int(instruction[2]) else 0
                ip += 1

            elif name == Commands.COMPARE_REGISTER:
                self.Registers['COMPAREFLAG'] = 1 if int(self.Registers[instruction[1]]) == int(self.Registers[instruction[2]]) else 0
                ip += 1

            # --- LOGICAL ---
            elif name == Commands.LOGICAL_OPERATIONS:
                op = instruction[1].upper()
                r1 = self.Registers[instruction[2]]
                r2 = self.Registers[instruction[3]] if len(instruction) > 3 else None
                if op == 'AND':
                    self.Registers['LOGIC_FLAG'] = bool(r1) and bool(r2)
                elif op == 'OR':
                    self.Registers['LOGIC_FLAG'] = bool(r1) or bool(r2)
                elif op == 'NOT':
                    self.Registers['LOGIC_FLAG'] = not bool(r1)
                ip += 1

            # --- STORE ---
            elif name == Commands.STORE:
                self.Registers[instruction[1]] = self.eval_operand(instruction[2])
                ip += 1

            # --- PRINT ---
            elif name == Commands.PRINT:
                val = self.eval_operand(instruction[1] if len(instruction) > 1 else None)
                self._write(val)
                ip += 1

            # --- COMMENT ---
            elif name == Commands.COMMENT:
                ip += 1

            # --- MARK ---
            elif name == Commands.MARK:
                self.Markers[str(instruction[1])] = ip
                ip += 1

            # --- IF ---
            elif name == Commands.IF:
                left, op, right = instruction[1], instruction[2], instruction[3]
                cond = self.eval_condition(left, op, right)
                self.LoopStack.append({'type': 'IF', 'start_ip': ip})
                if cond:
                    ip += 1
                else:
                    end_ip = self.find_matching_end(bytecode, ip + 1)
                    self.LoopStack.pop()
                    ip = end_ip + 1

            # --- WHILE ---
            elif name == Commands.WHILE:
                left, op, right = instruction[1], instruction[2], instruction[3]
                cond = self.eval_condition(left, op, right)
                self.LoopStack.append({
                    'type': 'WHILE',
                    'start_ip': ip,
                    'left_token': left,
                    'op': op,
                    'right_token': right
                })
                if cond:
                    ip += 1
                else:
                    end_ip = self.find_matching_end(bytecode, ip + 1)
                    self.LoopStack.pop()
                    ip = end_ip + 1

            # --- FOR ---
            elif name == Commands.FOR:
                reg = instruction[1]
                start = instruction[2]
                end = instruction[3]
                step = instruction[4] if len(instruction) > 4 else '1'

                self.Registers[reg] = self.eval_operand(start)

                self.LoopStack.append({
                    'type': 'FOR',
                    'start_ip': ip,
                    'reg': reg,
                    'end_token': end,
                    'step_token': step
                })

                step_val = self.eval_int(step)
                curr = self.eval_int(reg)
                end_val = self.eval_int(end)

                if (step_val > 0 and curr <= end_val) or (step_val < 0 and curr >= end_val):
                    ip += 1
                else:
                    end_ip = self.find_matching_end(bytecode, ip + 1)
                    self.LoopStack.pop()
                    ip = end_ip + 1

            # --- LOOP_END ---
            elif name == Commands.LOOP_END:
                if not self.LoopStack:
                    ip += 1
                    continue

                ctx = self.LoopStack[-1]

                if ctx['type'] == 'IF':
                    self.LoopStack.pop()
                    ip += 1

                elif ctx['type'] == 'WHILE':
                    cond = self.eval_condition(ctx['left_token'], ctx['op'], ctx['right_token'])
                    if cond:
                        ip = ctx['start_ip'] + 1
                    else:
                        self.LoopStack.pop()
                        ip += 1

                elif ctx['type'] == 'FOR':
                    reg = ctx['reg']
                    step_val = self.eval_int(ctx['step_token'])
                    self.Registers[reg] = int(self.Registers[reg]) + step_val

                    curr = self.eval_int(reg)
                    end_val = self.eval_int(ctx['end_token'])

                    if (step_val > 0 and curr <= end_val) or (step_val < 0 and curr >= end_val):
                        ip = ctx['start_ip'] + 1
                    else:
                        self.LoopStack.pop()
                        ip += 1

            # --- DECIMAL_CONVERT ---
            elif name == Commands.DECIMAL_CONVERT:
                val = self.eval_operand(instruction[1])
                t = str(instruction[2]).upper()
                if t == "BINARY":
                    self.Registers['BINARY_FLAG'] = bin(int(val))
                elif t == "HEXADECIMAL":
                    self.Registers['HEXADECIMAL_FLAG'] = hex(int(val))
                ip += 1

            else:
                self._write(f"error at line {ip+1}")
                ip += 1

        return self.get_output() if BROWSER_MODE or self.force_buffer else None

    # ---------------- DESKTOP AUTO-LOAD ----------------

    def run(self, filename='src\\ByteCode.txt'):
        if BROWSER_MODE:
            raise RuntimeError("run() is desktop-only.")
        bytecode = Reader.read_file_lines(filename)
        return self.execute(bytecode)


if __name__ == "__main__" and not BROWSER_MODE:
    vm = VmExecuter()
    vm.run()