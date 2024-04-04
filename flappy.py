import pygame
import neat
import os
import time
import random

pygame.init()
pygame.font.init()

gen = 0

# loading ui image elements
BIRD_IMG = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird1.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird2.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bg.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")))

STAT_FONT = pygame.font.SysFont("comicsans",50)

# window height
WIN_WIDTH = BG_IMG.get_width() -100
WIN_HEIGHT = 650


class Bird:

    # image array
    IMGS = BIRD_IMG
    # limit when looking down
    MAX_ROTATION = 25
    # limit for tilt
    ROT_VEL = 20
    # limit for image change
    ANIMATION_TIME = 5
    
    def __init__(self,x,y):
        self.x = x
        self.y = y

        self.tilt = 0
        self.tick_count = 0
        self.vel = 0

        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]


    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y


    def move(self):
        self.tick_count += 1

        # arc movement
        d = self.vel * self.tick_count + 1.5 * self.tick_count**2

        # setting limits for displacement
        if d >= 16:
            d = 16
        
        if d < 0:
            d -= 2
        
        self.y = self.y + d

        # tilt up
        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        # tilt down
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):

        self.img_count +=1

        # for changing bird image every 5 seconds
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        
        elif self.img_count < self.ANIMATION_TIME *2:
            self.img = self.IMGS[1]
        
        elif self.img_count < self.ANIMATION_TIME *3:
            self.img = self.IMGS[2]
        
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        
        elif self.img_count < self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0
        
        # making sure bird image doesnt change when falling
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2
        
        # rotating bird based on tilt
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft= (self.x,self.y)).center)

        win.blit(rotated_image,new_rect.topleft)

    
    
    def get_mask(self):
        # bird mask for collision
        return pygame.mask.from_surface(self.img)



class Pipe:
    GAP = 200
    VEL = 5

    def __init__(self, x) :
        self.x = x
        self.height = 0
        self.gap = Pipe.GAP
        self.passed = False


        self.top = 0
        self.bottom = 0
        self.PIPE_Top = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_Bottom = PIPE_IMG

        self.set_height()

    def set_height(self):
        # setting height of gap, random
        self.height = random.randrange(50,450)
        # starting location of top pipe
        self.top = self.height - self.PIPE_Top.get_height()
        # starting location of bottom pipe
        self.bottom = self.height + self.GAP

    def move(self):
        # moving pipe to the left
        self.x -= self.VEL

    def draw(self, win):
        
        # drawing top
        win.blit(self.PIPE_Top,(self.x, self.top))
        # drawing bottom
        win.blit(self.PIPE_Bottom,(self.x, self.bottom))

    def collide(self, bird, win):
        # returns true if collision happens
        # compares mask overlapping of pipes and bird
        # pixel wise overlapping

        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_Top)
        bottom_mask = pygame.mask.from_surface(self.PIPE_Bottom)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if b_point or t_point:
            return True
        
        return False



class Base:
    # floor image must be moving
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self,y):
        
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):

        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self,win):
        win.blit(self.IMG,(self.x1,self.y))
        win.blit(self.IMG,(self.x2,self.y))



def draw_window(win,birds,pipes,base,score,gen):

    #if gen == 0:
    #    gen = 1

    """drawing display window
    win: pygame window surface
    bird: a Bird object
    pipes: List of pipes
    score: score of the game 
    gen: current generation
    """    
    win.blit(BG_IMG,(0,0))

    # draw pipes
    for pipe in pipes:
        pipe.draw(win)
    
    # draw score
    text = STAT_FONT.render("score: " + str(score),1, (0,0,0))
    win.blit(text,(WIN_WIDTH - 10 - text.get_width(), 5))
    
    # draw generation number
    text = STAT_FONT.render("Gen: " + str(gen-1),1,(0,0,0))
    win.blit(text,(10,10))

    # draw base
    base.draw(win)
    
    # draw bird
    for bird in birds:
        bird.draw(win)
    
    pygame.display.update()


def main(genomes, config):

    # acts as fitness function
    # generates all objects
    # calculates the score based on distance

    global gen
    gen += 1
    
    # lists that hold bird objects, nets is the neural net
    # ge is the genomes for the neat algo 
    birds = []
    nets =[]
    ge = []

    for _,g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g,config)
        nets.append(net)
        birds.append(Bird(200,310))

        # start with fitness level of 0
        g.fitness = 0 
        ge.append(g)

    base = Base(730)
    pipes = [Pipe(WIN_WIDTH)]
    
    score = 0



    win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    clock = pygame.time.Clock()

    run = True
    while run and len(birds) > 0:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()   
                    

        # pipe index
        pipe_ind = 0
        # figure out if we use 1st or 2nd pipe on the screen
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_Top.get_width():
                pipe_ind = 1
          

            
        for x, bird in enumerate(birds):
            bird.move()        

            # give fitness for staying alive, in every frame
            ge[x].fitness += 0.1

            # figure out if jump or no jump based on bird, top and bottom pipe locations
            output = nets[x].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))
            
            # tanh range is -1 to 1
            # thaswhy threshold 0.5
            if output[0] > 0.5:
                bird.jump()

        rem=[]
        add_pipe = False
        for pipe in pipes:
            pipe.move()

            # checking for collision
            for x, bird in enumerate(birds):
                if pipe.collide(bird,win):
                    ge[x].fitness -= 1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

            # set pipe flag as passed
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True

            # if pipe is passed, add to remove list
            if pipe.x + pipe.PIPE_Top.get_width() < 0:
                rem.append(pipe)    

        if add_pipe:
            score += 1    
            
            # reward for passing
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(420))
            # mistake was forgetting to reset add_pipe flag
            # hence pipe was generated in every frame
            # overlapping
            add_pipe = False

        for r in rem:
            # check to see if pipe to be removed
            # has been generated
            if r in pipes:
                pipes.remove(r)

        # checking if bird hit floor,
        # if hit then remove that bird        
        for x, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 730:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)

        base.move()
    

        draw_window(win,birds,pipes,base,score,gen)

        
    

def run(config_path):
    """
    runs NEAT algo
    trains the neural net
    config path: absolute location of config file
    """
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,neat.DefaultSpeciesSet,neat.DefaultStagnation,config_path)
    
    # creating the population based on config
    p = neat.Population(config)

    # shows progress in terminal
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # running it upto nth gens
    winner = p.run(main,20)

    # displaying best result
    print('Best genome: ' + str(winner))

    #time.sleep(2)



if __name__ == "__main__":
    # finding config path location, by finding local working dir
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir,'config.txt')
    run(config_path)