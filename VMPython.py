from sqlite3 import Binary

from ByteCodeReader import Reader

bytecode = Reader.read_file_lines('ByteCode.txt') #used for reading bytecode file
output = Reader.find_in_nested_list(bytecode) #used for listing positions of values in bytecode

class Commands:
    #done
    ADDITION = 'ADDITION' #normal operation using numeric values
    ADDITION_REGISTER = 'ADDITION_REGISTER' #operation using values from registers
    #done
    SUBTRACT = 'SUBTRACT' #normal operation using numeric values
    SUBTRACT_REGISTER = 'SUBTRACT_REGISTER' #operation using values from registers
    #done
    MULTIPLY = 'MULIPLY' #normal operation using numeric values
    MULTIPLY_REGISTER = 'MULTIPLY_REGISTER' #operation using values from registers
    #done
    DIVIDE = 'DIVIDE' #normal operation using numeric values
    DIVIDE_REGISTER = 'DIVIDE_REGISTER' #operation using values from registers
    #done
    COMPARE = 'COMPARE' #comparison operation using numeric values
    COMPARE_REGISTER = 'COMPARE_REGISTER' #comparison operation using registers
    #done
    LOGICAL_OPERATIONS = 'LOGICAL_OPERATION' #logical operations AND, OR, NOT, XOR using values from registers
    #done
    STORE = 'STORE' #stores value in register
    #done
    PRINT = 'PRINT' #print value or use to print preset values for output and debugging
    #done
    COMMENT = 'COMMENT' #ignores the line as comment
    #done
    MARK = 'MARK' #marks a position in the code
    #done
    IF = 'IF' #if statement
    #done
    WHILE = 'WHILE' #while loop
    #done
    FOR = 'FOR' #for loop
    #done
    LOOP_END = 'LOOP_END' #used to show the end of a loop
    #done
    DECIMAL_CONVERT = 'DECIMAL_CONVERT' #converts decimal into binary or hexadecimal

class VMPython:
    def execute():

        Registers = {'COMPAREFLAG': 0, 'LOGIC_FLAG': False, 'BINARY_FLAG': "", 'HEXADECIMAL_FLAG': ""}  # Initialize flags for usage
        Markers = {}  # To store marked positions for jumps
        LoopStack = []  # Stack for loop/if contexts

        def eval_operand(token):
            # Return integer or original value of token: lookup in registers if present, else parse as int if possible.
            if token is None:
                return None
            token_str = str(token)
            # If token matches a register name, return its stored value
            if token_str in Registers:
                return Registers[token_str]
            # try parse int
            try:
                return int(token_str)
            except:
                # not a number or a register - return as-is (strings allowed for PRINT etc.)
                return token_str

        def eval_int(token):
            # Return integer value, whether token is a register name or literal. Raise ValueError if not int-convertible.
            val = eval_operand(token)
            return int(val)

        def eval_condition(left_tok, op_tok, right_tok):
            left = eval_operand(left_tok)
            right = eval_operand(right_tok)
            op = str(op_tok).strip()
            # normalize boolean-like values
            try:
                # attempt numeric comparison when possible
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
            # logical ops
            if op.upper() == 'AND':
                return bool(left) and bool(right)
            if op.upper() == 'OR':
                return bool(left) or bool(right)
            # fallback - equality
            return left == right

        def find_matching_end(start_ip):
            # Find the matching LOOP_END for a block that starts at start_ip.
            # Accounts for nested IF/FOR/WHILE blocks.
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
                    else:
                        depth -= 1
                ip += 1
            return None  # not found

        ip = 0
        while ip < len(bytecode):

            instruction = bytecode[ip]
            if not instruction:
                ip += 1
                continue

            instruction_name = str(instruction[0]).upper()
               
            if instruction_name == Commands.ADDITION:  # Addition operations
                value1 = int(instruction[1])
                value2 = int(instruction[2])
                register = instruction[3]
                register_value = value1 + value2
                Registers.update({register: register_value})
                ip += 1
            
            elif instruction_name == Commands.ADDITION_REGISTER: # Addition operations using registers
                value1 = int(Registers.get(instruction[1]))
                value2 = int(Registers.get(instruction[2]))
                register = instruction[3]
                register_value = value1 + value2
                Registers.update({register: register_value})
                ip += 1

            elif instruction_name == Commands.SUBTRACT: #subtraction operations
                value1 = int(instruction[1])
                value2 = int(instruction[2])
                register = instruction[3]
                register_value = value1 - value2
                Registers.update({register: register_value})
                ip += 1

            elif instruction_name == Commands.SUBTRACT_REGISTER: #subtraction operations using registers
                value1 = int(Registers.get(instruction[1]))
                value2 = int(Registers.get(instruction[2]))
                register = instruction[3]
                register_value = value1 - value2
                Registers.update({register: register_value})
                ip += 1

            elif instruction_name == Commands.MULTIPLY: #multiplication operations
                value1 = int(instruction[1])
                value2 = int(instruction[2])
                register = instruction[3]
                register_value = value1 * value2
                Registers.update({register: register_value})
                ip += 1

            elif instruction_name == Commands.MULTIPLY_REGISTER:
                value1 = int(Registers.get(instruction[1]))
                value2 = int(Registers.get(instruction[2]))
                register = instruction[3]
                register_value = value1 * value2
                Registers.update({register: register_value})
                ip += 1

            elif instruction_name == Commands.DIVIDE:
                value1 = int(instruction[1])
                value2 = int(instruction[2])
                register = instruction[3]
                register_value = value1 // value2
                Registers.update({register: register_value})
                ip += 1

            elif instruction_name == Commands.DIVIDE_REGISTER:
                value1 = int(Registers.get(instruction[1]))
                value2 = int(Registers.get(instruction[2]))
                register = instruction[3]
                register_value = value1 // value2
                Registers.update({register: register_value})
                ip += 1

            elif instruction_name == Commands.COMPARE:
                value1 = int(instruction[1])
                value2 = int(instruction[2])
                # simple comparison result stored in CompareFlag (0 false, 1 true)
                Registers['COMPAREFLAG'] = 1 if value1 == value2 else 0
                ip += 1

            elif instruction_name == Commands.COMPARE_REGISTER:
                value1 = int(Registers.get(instruction[1]))
                value2 = int(Registers.get(instruction[2]))
                Registers['COMPAREFLAG'] = 1 if value1 == value2 else 0
                ip += 1

            elif instruction_name == Commands.LOGICAL_OPERATIONS:
                op = instruction[1].upper()
                r1 = Registers.get(instruction[2])
                r2 = Registers.get(instruction[3]) if len(instruction) > 3 else None
                if op == 'AND':
                    Registers['LOGIC_FLAG'] = bool(r1) and bool(r2)
                elif op == 'OR':
                    Registers['LOGIC_FLAG'] = bool(r1) or bool(r2)
                elif op == 'NOT':
                    Registers['LOGIC_FLAG'] = not bool(r1)
                ip += 1

            elif instruction_name == Commands.STORE:
                register = instruction[1]
                value = instruction[2]
                # allow storing evaluated operand (so you can STORE x 5 or STORE x y)
                Registers.update({register: eval_operand(value)})
                ip += 1

            elif instruction_name == Commands.PRINT:
                # PRINT <register_or_value>
                arg = instruction[1] if len(instruction) > 1 else None
                val = eval_operand(arg)
                print(val)
                ip += 1

            elif instruction_name == Commands.COMMENT:
                # ignore
                ip += 1

            elif instruction_name == Commands.MARK:
                # MARK <name>
                if len(instruction) > 1:
                    name = str(instruction[1])
                    Markers[name] = ip
                ip += 1

            elif instruction_name == Commands.IF:
                # IF <left_register_or_value> <op> <right_register_or_value>
                left = instruction[1]
                op = instruction[2]
                right = instruction[3]
                cond = eval_condition(left, op, right)
                # push IF context so we know how to handle LOOP_END
                LoopStack.append({'type': 'IF', 'start_ip': ip})
                if cond:
                    ip += 1
                else:
                    # skip to matching LOOP_END
                    end_ip = find_matching_end(ip + 1)
                    if end_ip is None:
                        raise Exception("IF without matching LOOP_END at ip {}".format(ip))
                    # pop the IF context (we won't wait for LOOP_END)
                    LoopStack.pop()
                    ip = end_ip + 1

            elif instruction_name == Commands.WHILE:
                # WHILE <left_reg_or_value> <op> <right_reg_or_value>
                left = instruction[1]
                op = instruction[2]
                right = instruction[3]
                cond = eval_condition(left, op, right)
                # push WHILE context with token references so we re-evaluate each iteration
                LoopStack.append({'type': 'WHILE', 'start_ip': ip, 'left_token': left, 'op': op, 'right_token': right})
                if cond:
                    ip += 1
                else:
                    # skip to matching LOOP_END and pop context
                    end_ip = find_matching_end(ip + 1)
                    if end_ip is None:
                        raise Exception("WHILE without matching LOOP_END at ip {}".format(ip))
                    LoopStack.pop()
                    ip = end_ip + 1

            elif instruction_name == Commands.FOR:
                # FOR <loop_register> <start_reg_or_value> <end_reg_or_value> <step_reg_or_value?>
                reg = instruction[1]
                start_token = instruction[2]
                end_token = instruction[3]
                step_token = instruction[4] if len(instruction) > 4 else '1'
                # initialize loop register from evaluated start token
                Registers[reg] = eval_operand(start_token)
                # push FOR context with token references (so end/step can be registers that change)
                LoopStack.append({
                    'type': 'FOR',
                    'start_ip': ip,
                    'reg': reg,
                    'end_token': end_token,
                    'step_token': step_token
                })
                # decide whether to enter loop by evaluating current value vs end
                try:
                    step_val = eval_int(step_token)
                    curr_val = eval_int(reg)
                    end_val = eval_int(end_token)
                except Exception as e:
                    # if conversion fails, treat values as equal/non-numeric boolean check
                    step_val = 1
                    curr_val = eval_operand(reg)
                    end_val = eval_operand(end_token)
                if (int(step_val) > 0 and int(curr_val) <= int(end_val)) or (int(step_val) < 0 and int(curr_val) >= int(end_val)):
                    ip += 1
                else:
                    # skip to matching LOOP_END and pop context
                    end_ip = find_matching_end(ip + 1)
                    if end_ip is None:
                        raise Exception("FOR without matching LOOP_END at ip {}".format(ip))
                    LoopStack.pop()
                    ip = end_ip + 1

            elif instruction_name == Commands.LOOP_END:
                if not LoopStack:
                    # unmatched LOOP_END, just continue
                    ip += 1
                    continue
                ctx = LoopStack[-1]
                if ctx['type'] == 'IF':
                    # end of IF block: simply pop
                    LoopStack.pop()
                    ip += 1
                elif ctx['type'] == 'WHILE':
                    # re-evaluate condition from stored tokens; if true jump back to start+1; else pop and continue after LOOP_END
                    left = ctx['left_token']
                    op = ctx['op']
                    right = ctx['right_token']
                    cond = eval_condition(left, op, right)
                    if cond:
                        # jump back to instruction right after the WHILE start
                        ip = ctx['start_ip'] + 1
                    else:
                        LoopStack.pop()
                        ip += 1
                elif ctx['type'] == 'FOR':
                    # increment register using evaluated step token, and re-evaluate end token each iteration
                    reg = ctx['reg']
                    step_token = ctx['step_token']
                    end_token = ctx['end_token']
                    try:
                        step_val = eval_int(step_token)
                    except:
                        step_val = int(eval_operand(step_token))
                    # increment loop register
                    try:
                        Registers[reg] = int(Registers.get(reg)) + int(step_val)
                    except:
                        # fallback if stored as non-int convertible
                        Registers[reg] = eval_operand(reg)
                    # re-evaluate current and end values from tokens (allows end to be a register that changes)
                    try:
                        curr = eval_int(reg)
                        end_val = eval_int(end_token)
                    except:
                        curr = eval_operand(reg)
                        end_val = eval_operand(end_token)
                    if (int(step_val) > 0 and int(curr) <= int(end_val)) or (int(step_val) < 0 and int(curr) >= int(end_val)):
                        # loop again: jump back to instruction after FOR
                        ip = ctx['start_ip'] + 1
                    else:
                        # done
                        LoopStack.pop()
                        ip += 1
            elif instruction_name == Commands.DECIMAL_CONVERT:
                # DECIMAL_CONVERT <register> <type>
                val = eval_operand(instruction[1])
                target_type = str(instruction[2]).upper()
                if target_type.upper() == "BINARY":
                    binary = bin(int(val))
                    Registers.update({'BINARY_FLAG': binary})
                    ip += 1
                elif target_type.upper() == "HEXADECIMAL":
                    hexadecimal = hex(int(val))
                    Registers.update({'HEXADECIMAL_FLAG': hexadecimal})
                    ip += 1
                    
            else:
                # unknown instruction: skip or raise error
                print(f"WARNING: Unknown instruction {instruction_name} at ip {ip+1}")
                ip += 1