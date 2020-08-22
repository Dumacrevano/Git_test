import pygame
import random
import math
import sys

class Sim_board():
    def __init__(self,sizex, sizey, number_of_trial, failurerate):
        self.failure_rate = failurerate
        self.height = sizex*2
        self.width = sizey*2
        self.caption = "Task 1"
        self.background_colour = (255, 255, 255)
        self.screen_size = [self.width/2, self.height/2]
        self.screen = pygame.display.set_mode((self.width,self.height))
        self.canvas = pygame.Surface((self.width, self.height))
        self.number_of_trial = number_of_trial


    def rungame(self):
        pygame.display.set_caption(self.caption)
        self.canvas.fill(self.background_colour)
        self.p1_camera = pygame.Rect(0, 0, self.width/2, self.height/2)
        self.p2_camera = pygame.Rect(self.width/2, 0, self.width/2, self.height/2)
        p3_camera = pygame.Rect(0, self.height/2, self.width/2, self.height/2)
        p4_camera = pygame.Rect(self.width/2, self.height/2, self.width/2, self.height/2)
        self.p5_camera = pygame.Rect(0, self.height/2+40, self.width, self.height/2-40)
        self.sub1 = self.canvas.subsurface(self.p1_camera)
        self.sub2 = self.canvas.subsurface(self.p2_camera)
        sub3 = self.canvas.subsurface(p3_camera)
        sub4 = self.canvas.subsurface(p4_camera)
        self.sub5 = self.canvas.subsurface(self.p5_camera)
        pygame.draw.line(self.sub2, (0, 0, 0), (0, 0), (0, self.height/2), 10)
        pygame.draw.line(sub3, (0, 0, 0), (0, 0), (self.width/2, 0), 10)
        pygame.draw.line(sub4, (0, 0, 0), (0, 0), (self.width/2, 0), 10)
        self.screen.blit(self.sub1, (0, 0))
        self.screen.blit(self.sub2, (self.width/2, 0))
        self.screen.blit(sub3, (0, self.height/2))
        self.screen.blit(sub4, (self.width/2, self.height/2))
        self.screen.blit(self.sub5, (0 , self.height/2+40))

        fpsClock = pygame.time.Clock()

        #Pygame font initialization
        pygame.font.init()
        My_font = pygame.font.SysFont("Comic Sans MS", 20)

        # user input variables
        trial_amount = self.number_of_trial
        failure_percentage = self.failure_rate

        # initial variables
        current_trial = 0
        art_score = 0
        rt_score = 0
        tie_score = 0

        # main loop
        while trial_amount > current_trial:
            fpsClock.tick(10)

            current_trial += 1
            Trial_count = My_font.render("Trial Count:" + str(current_trial), False, (0, 0, 0))
            RT_score_count=My_font.render("RT_score:" + str(rt_score), False, (0, 0, 0))
            ART_score_count = My_font.render("ART_score:" + str(art_score), False, (0, 0, 0))
            tie_score_count= My_font.render("Tie_score:"+str(tie_score),False,(0,0,0))
            print("Trial " + str(current_trial))
            self.screen.blit(self.sub5, (0, self.height / 2+20))
            self.screen.blit(Trial_count, (50, int(self.height/2+100)))
            self.screen.blit(RT_score_count, (int(self.width/4-self.width/10), int(self.height/2+30)))
            self.screen.blit(ART_score_count, (int(self.width*3/4-self.width/10), int(self.height/2+30)))
            self.screen.blit(tie_score_count, (int(self.width/2-self.width/10), int(self.height/2+80)))
            self.sub5.fill((255,255,255))
            result = self.trial(failure_percentage)

            if (result[0] > result[1]):
                art_score += 1
            elif (result[0] < result[1]):
                rt_score += 1
            else:
                tie_score += 1

        print("ART: " + str(art_score))

        print("RT: " + str(rt_score))

        print("Tie: " + str(tie_score))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        # Flag = True
        # while Flag:
        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             Flag = False

    def euclidean_distance(self, coor1, coor2):
        return math.sqrt((coor1[0] - coor2[0]) ** 2 + (coor1[1] - coor2[1]) ** 2)

    def generate_coordinate(self, xlim, ylim):
        return [random.randint(0, xlim), random.randint(0, ylim)]

    def trial(self, failure_percentage):
        steps = 0

        # generate failure size
        total_screen_size = self.screen_size[0] * self.screen_size[1]
        total_failure_size = total_screen_size * failure_percentage
        failure_size = math.sqrt(total_failure_size)
        failure_size = round(math.sqrt(total_failure_size))
        print("failure_size: ", failure_size)


        # generate first point
        first_point = self.generate_coordinate(self.screen_size[0], self.screen_size[1])
        failure_coor = self.generate_coordinate(self.screen_size[0]-failure_size, self.screen_size[1]-failure_size)
        
        # initializing RT variables
        RT_point = first_point
        RT_flag = True
        RT_steps = 0

        RT_failure_rect = pygame.draw.rect(self.sub1, [255, 0, 0], [failure_coor[0], failure_coor[1], failure_size, failure_size], 0)
        ART_failure_rect = pygame.draw.rect(self.sub2, [255, 0, 0], [failure_coor[0], failure_coor[1], failure_size, failure_size], 0)
        print("Width :", RT_failure_rect.width)

        self.screen.blit(self.sub1, (0, 0))
        self.screen.blit(self.sub2, (self.width/2, 0))
        pygame.display.update()

        # initializing ART variables
        ART_point = first_point
        ART_flag = True
        ART_steps = 0
        prev_points = []

        while RT_flag or ART_flag:
            steps += 1

            # RT part
            if (RT_flag):
                print("RT:" + str(RT_point))
                RT_rect = pygame.draw.rect(self.sub1, [100, 255, 100], [RT_point[0], RT_point[1], 5, 5], 0)
                self.screen.blit(self.sub1, (0, 0))
                pygame.display.update()

                # end condition for RT
                # if (RT_point == failure_coor):  # is in region
                #     RT_flag = False
                #     RT_steps = steps

                if RT_rect.colliderect(RT_failure_rect):
                    RT_flag = False
                    RT_steps = steps
                    self.sub1.fill(self.background_colour)

                    self.screen.blit(self.sub1, (0, 0))

                else:
                    # generate next point
                    RT_point = self.generate_coordinate(self.screen_size[0], self.screen_size[1])



            # ART part
            if (ART_flag):
                print("ART:" + str(ART_point))
                ART_rect = pygame.draw.rect(self.sub2, [0, 0, 255], [ART_point[0], ART_point[1], 5, 5], 0)
                self.screen.blit(self.sub2, (self.width / 2, 0))
                pygame.display.update()

                # end condition for ART
                # if (ART_point == failure_coor):  # is in region
                #     ART_flag = False
                #     ART_steps = steps

                if ART_rect.colliderect(ART_failure_rect):
                    ART_flag = False
                    ART_steps = steps
                    self.sub2.fill(self.background_colour)
                    pygame.draw.line(self.sub2, (0, 0, 0), (0, 0), (0, self.height / 2), 10)
                    self.screen.blit(self.sub2, (self.width / 2, 0))

                else:
                    # find new candidate by generating 3 candidates
                    prev_points.append(ART_point)
                    candidates = []
                    for i in range(0,3):

                        candidates.append(self.generate_coordinate(self.screen_size[0], self.screen_size[1]))

                    # initialize variables
                    potential_candidate = []
                    min_dist = math.inf
                    max_dist = -math.inf

                    # loop through candidates to find ideal candidate
                    for i in candidates:

                        # loop through previous points and compare distance
                        for j in prev_points:
                            dist = self.euclidean_distance(i, j)

                            # compare distance between candidate and previous points
                            if dist < min_dist:
                                min_dist = dist

                        # compare distance between candidate
                        if min_dist > max_dist:
                            potential_candidate = i

                    ART_point = potential_candidate


        return [RT_steps, ART_steps]


#run1=Sim_board(200,0.2)
#un1.rungame()