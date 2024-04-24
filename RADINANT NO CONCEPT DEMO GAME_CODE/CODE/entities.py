import pygame, os

pygame.init()


class Entity:
    def __init__(self, x, y, amount, image_folders, image_type, image_size=None):
        self.x = x
        self.y = y

        self.amount = amount

        self.image_folders = image_folders
        self.image_type = image_type
        self.image_size = image_size

        self.gravity_count = 0
        self.gravity_bool = True

    def load_images(self):
        self.image_lists = []

        for image_folder in self.image_folders:
            image_list = []
            image_append = os.listdir(image_folder)
            image_append.sort()

            for filename in image_append:
                if filename.endswith(self.image_type):
                    image_path = os.path.join(image_folder, filename)
                    images = pygame.image.load(image_path).convert_alpha()

                    if self.image_size is not None:
                        resized_images = pygame.transform.scale(images, (self.image_size[0], self.image_size[1]))
                        image_list.append(resized_images)
                        image_list.append(pygame.transform.flip(resized_images, True, False))
                    else:
                        image_list.append(images)
                        image_list.append(pygame.transform.flip(images, True, False))
            self.image_lists.append(image_list)

    def collision(self):
        self.collision_rect_lists = []

        for list in self.image_lists:
            self.collision_rect_list = []

            for image in list:
                self.collision_rect_list.append(image.get_rect())
            self.collision_rect_lists.append(self.collision_rect_list)

    def gravity(self, bool):
        self.gravity_bool = bool

        if self.gravity_bool:
            self.gravity_count += 0.5
            self.gravity_amount = min(10, self.gravity_count)
            self.y += self.gravity_amount
            if self.gravity_count > 15:
                self.gravity_count = 16

            self.gravity_amount = 0
        elif not self.gravity_bool:
            self.gravity_amount = 0