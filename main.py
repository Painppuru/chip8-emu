import random
import pygame


class Screen(object):
    def __init__(self):
        self.display = []
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.width = 64
        self.height = 32
        self.scaling = 10
        self.clear()

    def clear(self):
        self.display = [[0] * self.width for y in range(self.height)]

    def start(self):
        self.screen = pygame.display.set_mode((self.width * self.scaling, self.height * self.scaling), pygame.RESIZABLE)
        pygame.display.set_caption("Chip-8 Emulator")
        self.refresh()

    def destroy(self):
        pygame.quit()

    def refresh(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.display[y][x] == 0:
                    color = self.black
                else:
                    color = self.white

                pygame.draw.rect(self.screen, color, (self.scaling * x, self.scaling * y, self.scaling, self.scaling))

        pygame.display.flip()

    def resize(self, x, y):
        xscale = x // self.width
        yscale = y // self.height
        self.scaling = min(xscale, yscale)
        self.start()


class Chip8(object):
    def __init__(self):
        self.memory = [0] * 4096
        self.V = [0] * 16
        self.I = 0
        self.pc = 0x200
        self.stack = []
        self.opcode = 0
        self.key = [0] * 16
        self.delay_timer = 0
        self.sound_timer = 0
        self.screen = Screen()
        self.load_fonts()
        self.speed = 1024

    def load_rom(self, rom_path):
        with open(rom_path, "rb") as rom:
            data = rom.read()
            for i in range(len(data)):
                self.memory[0x200 + i] = data[i]

    def start_game(self):
        self.screen.start()

        while True:
            self.listen()
            self.execute_opcode()
            self.screen.refresh()
            # pygame.time.delay(round((1 / self.speed) * 1000))

    def load_fonts(self):
        fonts = [
            0xF0, 0x90, 0x90, 0x90, 0xF0,  # 0
            0x20, 0x60, 0x20, 0x20, 0x70,  # 1
            0xF0, 0x10, 0xF0, 0x80, 0xF0,  # 2
            0xF0, 0x10, 0xF0, 0x10, 0xF0,  # 3
            0x90, 0x90, 0xF0, 0x10, 0x10,  # 4
            0xF0, 0x80, 0xF0, 0x10, 0xF0,  # 5
            0xF0, 0x80, 0xF0, 0x10, 0xF0,  # 6
            0xF0, 0x10, 0x20, 0x40, 0x40,  # 7
            0xF0, 0x90, 0xF0, 0x90, 0xF0,  # 8
            0xF0, 0x90, 0xF0, 0x10, 0xF0,  # 9
            0xF0, 0x90, 0xF0, 0x10, 0xF0,  # A
            0xE0, 0x90, 0xE0, 0x90, 0xE0,  # B
            0xF0, 0x80, 0x80, 0x80, 0xF0,  # C
            0xE0, 0x90, 0x90, 0x90, 0xE0,  # D
            0xF0, 0x80, 0xF0, 0x80, 0xF0,  # E
            0xF0, 0x80, 0xF0, 0x80, 0x80   # F
        ]

        for key, val in enumerate(fonts):
            self.memory[key] = val

    def listen(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.screen.destroy()

            elif event.type == pygame.VIDEORESIZE:
                self.screen.resize(event.w, event.h)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.key[0x1] = 1

                elif event.key == pygame.K_2:
                    self.key[0x2] = 1

                elif event.key == pygame.K_3:
                    self.key[0x3] = 1

                elif event.key == pygame.K_4:
                    self.key[0xC] = 1

                elif event.key == pygame.K_q:
                    self.key[0x4] = 1

                elif event.key == pygame.K_w:
                    self.key[0x5] = 1

                elif event.key == pygame.K_e:
                    self.key[0x6] = 1

                elif event.key == pygame.K_r:
                    self.key[0xD] = 1

                elif event.key == pygame.K_a:
                    self.key[0x7] = 1

                elif event.key == pygame.K_s:
                    self.key[0x8] = 1

                elif event.key == pygame.K_d:
                    self.key[0x9] = 1

                elif event.key == pygame.K_f:
                    self.key[0xE] = 1

                elif event.key == pygame.K_z:
                    self.key[0xA] = 1

                elif event.key == pygame.K_x:
                    self.key[0x0] = 1

                elif event.key == pygame.K_c:
                    self.key[0xB] = 1

                elif event.key == pygame.K_v:
                    self.key[0xF] = 1

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_1:
                    self.key[0x1] = 0

                elif event.key == pygame.K_2:
                    self.key[0x2] = 0

                elif event.key == pygame.K_3:
                    self.key[0x3] = 0

                elif event.key == pygame.K_4:
                    self.key[0xC] = 0

                elif event.key == pygame.K_q:
                    self.key[0x4] = 0

                elif event.key == pygame.K_w:
                    self.key[0x5] = 0

                elif event.key == pygame.K_e:
                    self.key[0x6] = 0

                elif event.key == pygame.K_r:
                    self.key[0xD] = 0

                elif event.key == pygame.K_a:
                    self.key[0x7] = 0

                elif event.key == pygame.K_s:
                    self.key[0x8] = 0

                elif event.key == pygame.K_d:
                    self.key[0x9] = 0

                elif event.key == pygame.K_f:
                    self.key[0xE] = 0

                elif event.key == pygame.K_z:
                    self.key[0xA] = 0

                elif event.key == pygame.K_x:
                    self.key[0x0] = 0

                elif event.key == pygame.K_c:
                    self.key[0xB] = 0

                elif event.key == pygame.K_v:
                    self.key[0xF] = 0

    def get_opcode(self):
        return ((self.memory[self.pc] << 8) + self.memory[self.pc + 1])

    def execute_opcode(self):
        self.opcode = self.get_opcode()

        result = (self.opcode & 0xF000)
        print(f'[PC:0x{self.pc:04x}] Instruction: 0x{self.opcode:04x}')

        if self.delay_timer > 0:
            self.delay_timer -= 1

        if result == 0x0000:
            second = (self.opcode & 0x00F0)
            if second == 0x00C0:  # scroll the screen down N lines
                pass

            elif second == 0x00E0:
                last = (self.opcode & 0x000F)
                if last == 0x0000:  # clear the screen
                    self.screen.clear()

                elif last == 0x000E:  # return from subroutine call
                    self.pc = self.stack.pop()

            elif second == 0x00F0:
                last = (self.opcode & 0x000F)
                if last == 0x000B:  # scroll screen 4 pixels right
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
            self.stack.append(self.pc)
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
            x = self.V[(self.opcode & 0x0F00) >> 8]
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
                self.V[0xF] = 0x1 if x > y else 0x0
                self.V[((self.opcode & 0x0F00) >> 8)] = ((x - y) & 0xFF)

            elif last == 0x0006:  # shift register VX right, bit 0 goes into register VF
                self.V[0xF] = (self.V[((self.opcode & 0x0F00) >> 8)] & 0x1)
                self.V[((self.opcode & 0x0F00) >> 8)] >>= 1

            elif last == 0x0007:  # subtract register VX from register VY, result stored in register VX
                x = self.V[((self.opcode & 0x0F00) >> 8)]
                y = self.V[((self.opcode & 0x00F0) >> 4)]
                self.V[0xF] = 0x1 if y > x else 0x0
                self.V[((self.opcode & 0x0F00) >> 8)] = ((y - x) & 0xFF)

            elif last == 0x000E:  # shift register VX left, bit 7 stored into register VF
                x = ((self.opcode & 0x0F00) >> 8)
                self.V[0xF] = (self.V[x] & 0x80) >> 7
                self.V[((self.opcode & 0x0F00) >> 8)] =(self.V[((self.opcode & 0x0F00) >> 8)] << 1) & 0xFF

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
            self.pc += 2

        elif result == 0xB000:  # Jump to address NNN + register V0
            n = self.opcode & 0x0FFF
            self.pc = (n + self.V[0]) & 0xFFFF

        elif result == 0xC000:  # register VX = random number AND KK
            k = (self.opcode & 0x00FF)
            self.V[((self.opcode & 0x0F00) >> 8)] = random.randint(0x00, 0xFF) & k
            self.pc += 2

        elif result == 0xD000:
            self.dxyn()
            self.pc += 2

        elif result == 0xE000:
            k = (self.opcode & 0x0F00) >> 8
            last_two = (self.opcode & 0x00FF)
            if last_two == 0x009E:  # skip if key (register rk) pressed
                if self.key[self.V[k]] == 1:
                    self.pc += 2

            elif last_two == 0x00a1:  # skip if key (register rk) pressed
                if self.key[self.V[k]] == 0:
                    self.pc += 2

            self.pc += 2

        elif result == 0xF000:
            r = (self.opcode & 0x0F00) >> 8
            last_two = (self.opcode & 0x00FF)
            if last_two == 0x0007:  # get delay timer into vr
                self.V[r] = self.delay_timer


            elif last_two == 0x000a:  # wait for for keypress,put key in register vr
                key_pressed = False
                while not key_pressed:
                    for key, val in enumerate(self.key):
                        if val == 1:
                            key_pressed = True
                            self.V[r] = key
                            break



            elif last_two == 0x0015:  # wait for for keypress,put key in register vr
                self.delay_timer = self.V[r]

            elif last_two == 0x0018:  # set the sound timer to vr
                self.sound_timer = self.V[r]

            elif last_two == 0x001e:  # add register vr to the index register
                self.I += self.V[r]


            elif last_two == 0x0029:  # point I to the sprite for hexadecimal character in vr
                self.I = self.V[r] * 5

            elif last_two == 0x0030:  # point I to the sprite for hexadecimal character in vr
                pass

            elif last_two == 0x0033:  # store the bcd representation of register vr at location I,I+1,I+2
                self.memory[self.I] = self.V[r] // 100
                self.memory[self.I + 1] = (self.V[r] - (self.memory[self.I] * 100)) // 10
                self.memory[self.I + 2] = (self.V[r] - (self.memory[self.I] * 100) - (self.memory[self.I + 1] * 10))

            elif last_two == 0x0055:  # store registers v0-vr at location I onwards
                for i in range(r + 1):
                    self.memory[self.I + i] = self.V[i]

                self.I += r + 1

            elif last_two == 0x0065:  # load registers v0-vr from location I onwards
                for i in range(r + 1):
                     self.V[i] = self.memory[self.I + i]

                self.I += r + 1

            self.pc += 2

    def dxyn(self):
        x = (self.opcode & 0x0F00) >> 8
        y = (self.opcode & 0x00F0) >> 4
        n = self.opcode & 0x000F
        self.V[0xF] = 0
        for i in range(n):
            line = self.memory[self.I + i]
            current_y = (self.V[y] + i) % self.screen.height

            for e in range(8):
                current_x = (self.V[x] + e) % self.screen.width
                bit = (line >> (7 - e)) & 0x1
                result = bit ^ self.screen.display[current_y][current_x]
                self.screen.display[current_y][current_x] = result

                if self.screen.display[current_y][current_x] == 0 and bit == 1:
                    self.V[0xF] = 1


if __name__ == '__main__':
    chip8 = Chip8()
    chip8.load_rom('tetris.rom')
    chip8.start_game()
