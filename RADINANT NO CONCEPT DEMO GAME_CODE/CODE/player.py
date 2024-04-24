import pygame

from CODE.entities import Entity


class Player(Entity):
    def __init__(self, x, y, amount, image_folders, image_type, image_size=None):
        super().__init__(x, y, amount, image_folders, image_type, image_size)

        self.movement_count = [0, 0]
        self.movement_bool = [[False, False], [False, False]]

        self.jump_bool = [False, False]
        self.jump_count = [0, 0, 0]  # the third num is needed for check stage jump if the first jump was completed

        self.image_list_index = 0
        self.image_index = [0, 0]

        self.amount_counter = 0
        self.animate_bool = True

# MOVEMENT ------ #
    def movement(self, speed):
        self.keys = pygame.key.get_pressed()

        if self.keys[pygame.K_LEFT] or self.keys[pygame.K_a] and not self.movement_bool[0][1]:
            self.movement_bool = [[True, False], [True, False]]
            self.movement_count[1] = 0
            self.movement1_process(speed, 1, 1), self.movement2_process(speed, 1)
        elif self.keys[pygame.K_RIGHT] or self.keys[pygame.K_d] and not self.movement_bool[0][0]:
            self.movement_bool = [[False, True], [False, True]]
            self.movement_count[1] = 0
            self.movement1_process(speed, 2, 1), self.movement2_process(speed, 2)
        else:
            self.movement_count[0] = 0
            self.movement_bool[0] = [False, False]

            if self.movement_bool[1][0]:
                self.movement1_process(speed, 1, 2)
            elif self.movement_bool[1][1]:
                self.movement1_process(speed, 2, 2)

            if self.movement_count[1] >= 10:
                self.movement_bool[1] = [False, False]

        # print(self.movement_count)

    def movement1_process(self, speed, surface, variant):
        self.movement_count[1] += 1

        for i in range(1, 10):
            if self.movement_count[0] == i if variant == 1 else self.movement_count[1] == i:
                if surface == 1:
                    self.x -= speed * i if i == 1 else (i / 1.5) if variant == 1 else (((i / i) / i) * 15)
                elif surface == 2:
                    self.x += speed * i if i == 1 else (i / 1.5) if variant == 1 else (((i / i) / i) * 15)

    def movement2_process(self, speed, surface):
        self.movement_count[0] += 1

        if self.movement_count[0] >= 10:
            if surface == 1:
                self.x -= speed * (9 / 1.5)
            if surface == 2:
                self.x += speed * (9 / 1.5)

# JUMP ------ #
    def jump(self, amount, cycle):

        if self.keys[pygame.K_w] or self.keys[pygame.K_UP] or self.keys[pygame.K_SPACE]:
            self.jump_bool[0] = True

        if self.jump_bool[0]:
            self.jump_count[0] += 1
            if self.jump_count[0] == 1:
                self.jump_bool[1] = True
                self.gravity_count = 0
                self.jump_count[1] += 1

            for n in range(1, cycle):
                if self.jump_count[0] == n:
                    self.y -= amount * (n * n if n <= 2 else (n/5) if n <= 4 else (n/10) if n <= 7 else (n/20) if n <= 8 else (n/30))
                    if self.jump_count[0] > 1:
                        self.jump_bool[1] = False

        if not (self.keys[pygame.K_w] or self.keys[pygame.K_UP] or self.keys[pygame.K_SPACE]):
            if self.jump_count[1] == 1:
                if self.jump_count[0] >= cycle:
                    self.jump_count[0] = 0
                    self.jump_bool[0] = False
                    if not self.gravity_bool:
                        self.jump_count[1] = 0
            elif self.jump_count[1] == 2:
                self.jump_count[2] += 1
                if self.jump_count[2] >= cycle:
                    self.jump_reset_parameters()
            self.jump_reset_parameters()

    def jump_reset_parameters(self):

        if not self.gravity_bool:
            self.jump_count = [0, 0, 0]
            self.jump_bool = [False, False]
            self.gravity_count = 0

# ANIMATE ------ #

    def animate(self, left_bool, right_bool, jump_bool):
        self.animate1_process(self.animate_bool)

        if left_bool and not jump_bool:
            if self.image_index[1] == 0:
                self.image_index[1] = 1
                self.image_index[0] = self.image_index[1]
            self.animate2_set_image_index(1, True)
        elif right_bool and not jump_bool:
            if self.image_index[1] == 1:
                self.image_index[1] = 0
                self.image_index[0] = self.image_index[1]
            self.animate2_set_image_index(1, True)
        elif jump_bool:
            self.animate2_set_image_index(2)
            if self.jump_bool[1] and self.jump_count[1] == 1:
                self.image_index[0] = self.image_index[1]
                self.amount_counter = 0
            elif self.image_index[0] == 2 or self.image_index[0] == 3:
                self.animate_bool = False
        else:
            self.animate2_set_image_index(0, True)

    def animate1_process(self, bool):

        if bool:
            self.amount_counter += 1
            if self.amount_counter >= self.amount[self.image_list_index]:
                self.amount_counter = 0
                self.image_index[0] += 2
            if self.image_index[0] >= len(self.image_lists[self.image_list_index]):
                self.image_index[0] = self.image_index[1]

    def animate2_set_image_index(self, list_index, animate_bool=None):
        self.image_list_index = list_index
        if animate_bool is not None:
            self.animate_bool = animate_bool

        if self.image_index[0] >= len(self.image_lists[self.image_list_index]):
            self.image_index[0] = self.image_index[1]
