import threading
import pygame
import socket
import sys
import random

name = "test"
posx = 200
posy = 100
bucket_speed = 35
playing = True
game_over = False
game_started = False

def GameThread():
    pygame.init()
    background = (0, 0, 0)
    shapeColor = (0, 51, 204)
   
    
    fps = pygame.time.Clock()
    screen_size = screen_width, screen_height = 600, 400
    
    rect1 = pygame.Rect(0, 0, 80, 35)
    #falling ball
    ball_radius =12
    ball_x = random.randint(ball_radius, screen_width - ball_radius)
    ball_y = -ball_radius
    ball_speed = 3
    score = 0
    font = pygame.font.SysFont(None,32)
    screen = pygame.display.set_mode(screen_size)

    pygame.display.set_caption('CCN Final Project')
    button_rect = pygame.Rect(200,260,200,50)
    title_font = pygame.font.SysFont(None, 60)
    button_font = pygame.font.SysFont(None, 35)
    
    colorRect = (shapeColor)
    
    global posx 
    global posy 
    global bucket_speed
    global game_over
    global game_started

    while playing:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and button_rect.collidepoint(event.pos):

                    if not game_started or game_over:
                        game_started = True
                        game_over = False

                        score = 0
                        ball_speed = 3
                        bucket_speed = 25

                        posx = 300
                        posy = 350

                        ball_x = random.randint(
                            ball_radius, screen_width - ball_radius
                        )
                        ball_y = -ball_radius

        screen.fill(background)

        # Move the ball only while the game is active
        if game_started and not game_over:
            ball_y += ball_speed

            # Game Over when the ball reaches the bottom
            if ball_y + ball_radius >= screen_height:
                game_over = True
                print("GAME OVER! Final Score:", score)

        rect1.center = (posx, posy)
        #recttangle around the falling ball
        ball_rect = pygame.Rect(
            ball_x - ball_radius,
            ball_y - ball_radius,
            ball_radius * 2,
            ball_radius * 2
        )
        #check whetehr the ball touches the basket
        if game_started and not game_over and rect1.colliderect(ball_rect):
            score +=1
            print("caught score:",score)

            #ball speed increase after every 4 catches
            if score % 4 == 0:
                ball_speed +=1
                bucket_speed +=7
                print("ball speed increased to:", ball_speed)
                print("bucket speed:", bucket_speed)

            #spwan a new ball
            ball_x = random.randint(ball_radius,screen_width - ball_radius)
            ball_y = -ball_radius

        # Draw the bucket body
        pygame.draw.polygon(screen, colorRect, [
            (rect1.left, rect1.top),
            (rect1.right, rect1.top),
            (rect1.right - 10, rect1.bottom),
            (rect1.left + 10, rect1.bottom)
        ])

        # Draw falling ball
        pygame.draw.circle(
            screen,
            (255, 165, 0),
            (int(ball_x), int(ball_y)),
            ball_radius
        )

        # Draw the bucket rim
        pygame.draw.rect(screen, (0, 30, 100),
                        (rect1.left - 5, rect1.top, 90, 8),
                        border_radius=3)

        

        # Display the score
        score_text = font.render(f"Score: {score}", True, (0, 51, 102))
        screen.blit(score_text, (screen_width - 130, 15))         


        # Start screen
        if not game_started:
            screen.fill(background)

            title = title_font.render(
                "BUCKET CATCH", True, (0, 51, 204)
            )
            screen.blit(title, title.get_rect(center=(300, 160)))

            pygame.draw.rect(
                screen, (0, 51, 204), button_rect, border_radius=10
            )

            start_text = button_font.render(
                "START", True, (255, 255, 255)
            )
            screen.blit(
                start_text,
                start_text.get_rect(center=button_rect.center)
            )

        # Game Over screen
        elif game_over:
            game_over_text = title_font.render(
                "GAME OVER", True, (255, 0, 0)
            )

            screen.blit(
                game_over_text,
                game_over_text.get_rect(center=(300, 145))
            )

            final_score_text = button_font.render(
                f"Final Score: {score}", True, (0, 51, 102)
            )

            screen.blit(
                final_score_text,
                final_score_text.get_rect(center=(300, 205))
            )

            pygame.draw.rect(
                screen, (0, 51, 204), button_rect, border_radius=10
            )

            restart_text = button_font.render(
                "RESTART", True, (255, 255, 255)
            )

            screen.blit(
                restart_text,
                restart_text.get_rect(center=button_rect.center)
            )

        pygame.display.update()
        fps.tick(60)


def ServerThread():
    global posy
    global posx
    global bucket_speed
    global game_over
    global game_started

    # get the hostname
    host = socket.gethostbyname(socket.gethostname())
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    host = s.getsockname()[0]
    s.close()
    print(host) # has the ip address fo
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together
    print("Server enabled...")
    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))    
    global playing
    while playing:        
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        
        print("from connected user: " + str(data))
        for key in data:
            if(key == 'q'):
                playing = False
                print("quitting game")
            elif game_started and  not game_over:
                if key == 'a':
                    posx = max(40, posx - bucket_speed)

                if key == 'd':
                    posx = min(560, posx + bucket_speed)
           
    conn.close()  # close the connection



t2 = threading.Thread(target=ServerThread, )
t2.start()

GameThread()