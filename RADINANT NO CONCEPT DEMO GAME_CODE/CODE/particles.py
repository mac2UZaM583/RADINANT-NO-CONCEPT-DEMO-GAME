import random, pygame


class Particles:
    def __init__(self, bool, count, quantity):
        self.bool = bool
        self.count = count
        
        self.particles = []
        
        for i in range(0, quantity):
            i = []
            self.particles.append(i)

    def particle1(self, x, y, speed, size, screen, range1, decrease, bool, quantity):
        if bool:
            for i in range(range1):
                self.particles[quantity - 1].append([[x, y], [random.randint(-speed, speed) / (speed / (speed / 6)), random.randint(-speed, speed) / (speed / (speed / 6))], random.randint(size[0], size[1])])

        for particle in self.particles[quantity - 1]:
            particle[0][0] += particle[1][0] * ((particle[2] / decrease) / 2)
            particle[0][1] += particle[1][1] * ((particle[2] / decrease) / 2)
            particle[2] -= 0.4 / decrease
            pygame.draw.circle(screen, [255, 255, 255], particle[0], particle[2])
            if particle[2] <= 0:
                self.particles[quantity - 1].remove(particle)