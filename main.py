import pygame as pg

class GameObjects:
    rectangles: [pg.Rect] = []
    surfaces: [pg.Surface] = []
    rectangle_coordinates_old = []
    rectangles_movement = []

    def __init__(self):
        pass

    def add_object(self, rectangle: pg.Rect, surface: pg.Surface, initial_coordinates, speed):
        self.rectangles.append(rectangle)
        self.surfaces.append(surface)
        self.rectangle_coordinates_old.append(initial_coordinates)
        self.rectangles_movement.append(speed)

    # Step forward by 1 frame, simulates the movement and collision of rectangles
    def step(self, local_screen: pg.Surface):
        for i in range(len(self.rectangles)):
            self.rectangle_coordinates_old[i] = (
                self.rectangles[i].x,
                self.rectangles[i].y,
                self.rectangles[i].w,
                self.rectangles[i].h
            )
            if self.rectangles_movement[i] != (0, 0):
                self.rectangles[i] = self.rectangles[i].move((
                    self.rectangles_movement[i][0],
                    self.rectangles_movement[i][1]
                ))
                local_screen.fill((0, 0, 0), self.rectangle_coordinates_old[i])

                collisions = self.rectangles[i].collideobjectsall(self.rectangles)
                for collision in collisions:
                    distance_x = self.rectangles[i].center[0] - collision.center[0]
                    distance_y = self.rectangles[i].center[1] - collision.center[1]
                    if distance_y == 0 and distance_x == 0:
                        continue

                    print(self.rectangles_movement[i][0], distance_x)
                    diff_x = self.rectangles_movement[i][0] / distance_x
                    diff_y = self.rectangles_movement[i][1] / distance_y
                    if diff_x < 0:
                        # Source rectangle is moving into the collided rectangle on the x axis
                        self.rectangles_movement[i] = (0, 0)
                        if distance_x < 0:
                            # Must snap to left
                            self.rectangles[i].right = collision.left
                        elif distance_x > 0:
                            # Must snap to right
                            self.rectangles[i].left = collision.right
                    if diff_y < 0:
                        # Source rectangle is moving into the collided rectangle on the y axis
                        self.rectangles_movement[i] = (0, 0)
                        if distance_y < 0:
                            # Must snap to top
                            self.rectangles[i].bottom = collision.top
                        elif distance_y > 0:
                            # Must snap to bottom
                            self.rectangles[i].top = collision.bottom

            local_screen.blit(self.surfaces[i], self.rectangles[i])


pg.init()

clock = pg.time.Clock()

screen = pg.display.set_mode((800, 800))
game_objects = GameObjects()
game_objects.add_object(
    pg.Rect(0, 0, 200, 200),
    pg.Surface((200, 200)),
    (0, 0),
    (0, 0)
)
game_objects.surfaces[0].fill((255, 0, 0))
game_objects.add_object(
    pg.Rect(400, 400, 200, 200),
    pg.Surface((200, 200)),
    (0, 0),
    (0, 0)
)
game_objects.surfaces[1].fill((0, 255, 0))

PRIMARY_OBJECT = 0

running = True

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if pg.key.get_pressed()[pg.K_w]:
            game_objects.rectangles_movement[PRIMARY_OBJECT] = (0, -1)
        elif pg.key.get_pressed()[pg.K_s]:
            game_objects.rectangles_movement[PRIMARY_OBJECT] = (0, 1)
        elif pg.key.get_pressed()[pg.K_d]:
            game_objects.rectangles_movement[PRIMARY_OBJECT] = (1, 0)
        elif pg.key.get_pressed()[pg.K_a]:
            game_objects.rectangles_movement[PRIMARY_OBJECT] = (-1, 0)


    game_objects.step(screen)
    pg.display.flip()

    clock.tick(60)
