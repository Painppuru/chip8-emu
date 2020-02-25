import random


class chip8(object):
    def __init__(self):
        self.memory = [0] * 4096
        self.V = [0] * 16
        self.I = 0
        self.pc = 0
        self.stack = []
        self.opcode = 0
        self.key = [0] * 16

    def get_opcode(self):
        return ((self.memory[self.pc] << 8) + self.memory[self.pc + 1])

    def exevute_opcode(self):
        self.opcode = self.get_opcode()

        result = (self.opcode & 0xF000)

        if result == 0x0000:
            second = (self.opcode & 0x00F0)
            if second == 0x00C0:  # scroll the screen down N lines
                pass

            elif second == 0x00E0:
                last = (self.opcode & 0x000F)
                if last == 0x0000:  # clear the screen
                    pass

                elif last == 0x000E:  # return from subroutine call
                    pass

            elif second == 0x00F0:
                last = (self.opcode & 0x000F)
                if last == 0x000B:  # return from subroutine call
                    pass

                elif last == 0x000C:  # scroll screen 4 pixels left
                    pass

                elif last == 0x000E:  # disable extended screen mode
                    pass

                elif last == 0x000F:  # enable extended screen mode (128 x 64)
                    pass

            self.pc += 2

        elif result == 0x1000:  # jump to address NNN
            self.pc = (self.opcode & 0x0FFF)

        elif result == 0x2000:  # jump to subroutine at address NNN
            self.stack.append(self.pc + 2)
            self.pc = (self.opcode & 0x0FFF)

        elif result == 0x3000:  # skip next istruction if register VX == constant RR
            x = self.V[((self.opcode & 0x0F00) >> 8)]
            r = (self.opcode & 0x00FF)
            if x == r:
                self.pc += 4

            else:
                self.pc += 2

        elif result == 0x4000:  # skip next intruction if register VX != constant RR
            x = self.V[((self.opcode & 0x0F00) >> 8)]
            r = (self.opcode & 0x00FF)
            if x != r:
                self.pc += 4

            else:
                self.pc += 2

        elif result == 0x5000:  # skip next instruction if register VX == register VY
            x = self.V[((self.opcode & 0x0F00) >> 8)]
            y = self.V[((self.opcode & 0x00F0) >> 4)]
            if x == y:
                self.pc += 4

            else:
                self.pc += 2

        elif result == 0x6000:  # move constant RR to register VX
            r = (self.opcode & 0x00FF)
            self.V[((self.opcode & 0x0F00) >> 8)] = r
            self.pc += 2

        elif result == 0x7000:  # add constant RR to register VX
            x = self.V[(self.opcode & 0x0F00)]
            r = (self.opcode & 0x00FF)
            self.V[((self.opcode & 0x0F00) >> 8)] = (x + r) & 0xFF
            self.pc += 2

        elif result == 0x8000:
            last = (self.opcode & 0x000F)

            if last == 0x0000:  # move register VY into VX
                y = self.V[((self.opcode & 0x00F0) >> 4)]
                self.V[((self.opcode & 0x0F00) >> 8)] = y

            elif last == 0x0001:  # or register VY with register VX, store result into register VX
                x = self.V[((self.opcode & 0x0F00) >> 8)]
                y = self.V[((self.opcode & 0x00F0) >> 4)]
                self.V[((self.opcode & 0x0F00) >> 8)] = (y | x)

            elif last == 0x0002:  # and register VY with register VX, store result into register VX
                x = self.V[((self.opcode & 0x0F00) >> 8)]
                y = self.V[((self.opcode & 0x00F0) >> 4)]
                self.V[((self.opcode & 0x0F00) >> 8)] = (y & x)

            elif last == 0x0003:  # exclusive or register VY with register VX, store result into register VX
                x = self.V[((self.opcode & 0x0F00) >> 8)]
                y = self.V[((self.opcode & 0x00F0) >> 4)]
                self.V[((self.opcode & 0x0F00) >> 8)] = (y ^ x)


            elif last == 0x0004:  # add register VY to VX, store result in register VX, carry stored in register VF
                x = self.V[((self.opcode & 0x0F00) >> 8)]
                y = self.V[((self.opcode & 0x00F0) >> 4)]
                self.V[0xF] = ((x + y) & 0x100) >> 8
                self.V[((self.opcode & 0x0F00) >> 8)] = ((x + y) & 0xFF)

            elif last == 0x0005:  # subtract register VY from VX, borrow stored in register VF
                x = self.V[((self.opcode & 0x0F00) >> 8)]
                y = self.V[((self.opcode & 0x00F0) >> 4)]
                if y > x:
                    self.V[0xF] = 0x1
                    self.V[((self.opcode & 0x0F00) >> 8)] = (((x + 0x100) - y) & 0xFF)
                else:
                    self.V[((self.opcode & 0x0F00) >> 8)] = ((x - y) & 0xFF)

            elif last == 0x0006:  # shift register VX right, bit 0 goes into register VF
                self.V[0xF] = (self.V[((self.opcode & 0x0F00) >> 8)] & 0x7)
                self.V[((self.opcode & 0x0F00) >> 8)] >>= 1

            elif last == 0x0007:  # subtract register VX from register VY, result stored in register VX
                x = self.V[((self.opcode & 0x0F00) >> 8)]
                y = self.V[((self.opcode & 0x00F0) >> 4)]
                if x > y:
                    self.V[0xF] = 0x1
                    self.V[((self.opcode & 0x0F00) >> 8)] = (((y + 0x100) - x) & 0xFF)
                else:
                    self.V[((self.opcode & 0x0F00) >> 8)] = ((y - x) & 0xFF)

            elif last == 0x000E:  # shift register VX left, bit 7 stored into register VF
                self.V[0xF] = (self.V[((self.opcode & 0x0F00) >> 8)] & 0x1)
                self.V[((self.opcode & 0x0F00) >> 8)] >>= 1

            self.pc += 2

        elif result == 0x9000:  # skip next instruction if register VX != register VY
            x = self.V[((self.opcode & 0x0F00) >> 8)]
            y = self.V[((self.opcode & 0x00F0) >> 4)]
            if x != y:
                self.pc += 4

            else:
                self.pc += 2

        elif result == 0xA000:  # Load index register (I) with constant NNN
            n = self.opcode & 0x0FFF
            self.I = n

        elif result == 0xB000:  # Jump to address NNN + register V0
            pass

        elif result == 0xC000:  # register VX = random number AND KK
            k = (self.opcode & 0x00FF)
            self.V[((self.opcode & 0x0F00) >> 8)] = random.randint & k

        elif result == 0xD000:
            pass

        elif result == 0xE000:
            last_two = (self.opcode & 0x00FF)
            if last_two == 0x009E:  # skip if key (register rk) pressed
                pass

            elif last_two == 0x00a1:  # skip if key (register rk) pressed
                pass

        elif result == 0xF000:
            last_two = (self.opcode & 0x00FF)
            if last_two == 0x0007:  # get delay timer into vr
                pass

            elif last_two == 0x000a:  # wait for for keypress,put key in register vr
                pass

            elif last_two == 0x0015:  # wait for for keypress,put key in register vr
                pass

            elif last_two == 0x0018:  # set the sound timer to vr
                pass

            elif last_two == 0x001e:  # add register vr to the index register
                pass

            elif last_two == 0x0029:  # point I to the sprite for hexadecimal character in vr
                pass

            elif last_two == 0x0030:  # point I to the sprite for hexadecimal character in vr
                pass

            elif last_two == 0x0033:  # store the bcd representation of register vr at location I,I+1,I+2
                pass

            elif last_two == 0x0055:  # store registers v0-vr at location I onwards
                pass

            elif last_two == 0x0065:  # load registers v0-vr from location I onwards
                pass
