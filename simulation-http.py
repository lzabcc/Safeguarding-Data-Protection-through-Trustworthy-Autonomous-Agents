import pygame
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import json
from Config import *
from Classes import *
from Function import *
import socket

global result_info
result_info=["Listening","Listening"]
def main():
    pygame.init()

    WIDTH, HEIGHT = 1200, 900
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(Programme_name)

    service_box = pygame.Rect(50, 100, 200, 450)
    agent_box = pygame.Rect(500, 250, 150, 200)
    user_box = pygame.Rect(850, 100, 200, 300)

    # service
    service_buttons = [
        Service("Bank", RED, (service_box.left + 100, service_box.top + 50)),
        Service("Hospital", GREEN, (service_box.left + 100, service_box.top + 150)),
        Service("School", BLUE, (service_box.left + 100, service_box.top + 250)),
        Service("Amazon", BLACK, (service_box.left + 100, service_box.top + 350))
    ]

    # user
    user_buttons = [
        User("U1", '18', "Newcastle", BLACK, (user_box.left + 100, user_box.top + 100)),
        User("U2", '20', "London", BLACK, (user_box.left + 100, user_box.top + 200))
    ]

    # Agent
    agent_buttons = [
        Agent("A1", BLUE, (agent_box.left + 75, agent_box.top + 60)),
        Agent("A2", GREEN, (agent_box.left + 75, agent_box.top + 140))
    ]

    send_button = Button(WHITE, 850, 600, 150, 55, 'Send')
    trajectory_button = Button(WHITE, 850, 700, 150, 55, 'Trajectory')

    # menu rect
    #menu_items = ["Name", "Age", "Address"]#,"marital_status","occupation","education"]
    menu_items = ["marital_status","occupation","education"]
    selected_item = menu_items[0]
    menu_rects = {
        "requester": pygame.Rect(75, 600, 150, 55),
        "info": pygame.Rect(250, 600, 180, 55),
        "agent": pygame.Rect(450, 600, 150, 55),
        "requestee": pygame.Rect(625, 600, 150, 55)
    }
    menu_open = {"requester": False, "info": False, "agent": False, "requestee": False}

    selected_service = service_buttons[0]
    selected_user = user_buttons[0]
    selected_agent = agent_buttons[0]

    image = pygame.transform.scale(pygame.image.load("mail.png"), (50, 50))

    drawn_lines = []

    msg_pos = (service_buttons[0].position[0] + 30, service_buttons[0].position[1])

    global state
    global result_info

    state = "idle"
    state_start_time = None

    run = True
    custom_sentence = "Please Click Send Button"
    font_color = BLACK
    draw_trajectory = False

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN and state == "idle":
                if send_button.is_over(pos):
                    state = "sending_to_user"
                    msg_pos = (selected_service.position[0], selected_service.position[1])
                    custom_sentence = f"Sending {selected_item} from {selected_service.name} to {selected_user.name}"
                    font_color = BLACK

                elif trajectory_button.is_over(pos):
                    draw_trajectory = True

                else:
                    for key, rect in menu_rects.items():
                        if rect.collidepoint(pos):
                            menu_open[key] = not menu_open[key]
                            break
                    for service_button in service_buttons:
                        if service_button.is_clicked(pos):
                            selected_service = service_button
                            break
                    for user_button in user_buttons:
                        if user_button.is_clicked(pos):
                            selected_user = user_button
                            break
                    for agent_button in agent_buttons:
                        if agent_button.is_clicked(pos):
                            selected_agent = agent_button

            if event.type == pygame.MOUSEBUTTONUP:
                for key, rect in menu_rects.items():
                    if menu_open[key]:
                        for i in range(len(menu_rects.items())):
                            

                            item_rect = pygame.Rect(rect.x, rect.y + 50 + i * 50, 150, 50)
                            if item_rect.collidepoint(pos):
                                if key == "requester":
                                    selected_service = service_buttons[i]
                                elif key == "info":
                                    selected_item = menu_items[i]
                                elif key == "agent":
                                    selected_agent = agent_buttons[i]
                                elif key == "requestee":
                                    selected_user = user_buttons[i]
                                menu_open[key] = False
                                break

        win.fill((255, 255, 255))

        # Result input
        custom_sentence_box = pygame.Rect(265, 800, 500, 50)

        font = pygame.font.Font(None, 30)
        text_custom_sentence = font.render(custom_sentence, True, font_color)
        win.blit(text_custom_sentence, (custom_sentence_box.x + 10, custom_sentence_box.y + 10))

        win.blit(font.render(result_info[1], True, (0, 0, 0)), (10, 10))

        pygame.draw.rect(win, BLACK, service_box, 2)
        pygame.draw.rect(win, BLACK, agent_box, 2)
        pygame.draw.rect(win, BLACK, user_box, 2)

        font = pygame.font.Font(None, 36)
        text1 = font.render("Service", True, BLACK)
        text2 = font.render("Agent", True, BLACK)
        text3 = font.render("User", True, BLACK)
        win.blit(text1, (service_box.centerx - text1.get_width() // 2, service_box.top - 30))
        win.blit(text2, (agent_box.centerx - text2.get_width() // 2, agent_box.top - 30))
        win.blit(text3, (user_box.centerx - text3.get_width() // 2, user_box.top - 30))

        for key, rect in menu_rects.items():
            pygame.draw.rect(win, (0, 0, 0), rect, 2)
            font = pygame.font.SysFont(None, 36)
            text = font.render(menu_titles[key], True, (0, 0, 0))
            text_rect = text.get_rect(center=(rect.x + rect.width // 2, rect.y - 20))
            win.blit(text, text_rect)

        def draw_buttons_with_text(buttons, font, win):
            for button in buttons:
                button.draw(win)
                text = font.render(button.name, True, BLACK)
                text_rect = text.get_rect(center=button.position)
                win.blit(text, text_rect)

        for service_button in service_buttons:
            service_button.draw(win)
            service_name = service_button.name
            text_service = font.render(service_name, True, BLACK)
            text_service_rect = text_service.get_rect(center=(service_button.position[0], service_button.position[1] + 35))
            win.blit(text_service, text_service_rect)
            
        draw_buttons_with_text(user_buttons, font, win)
        draw_buttons_with_text(agent_buttons, font, win)

        send_button.draw(win, BLACK)
        trajectory_button.draw(win, BLACK)

        for key, rect in menu_rects.items():
            pygame.draw.rect(win, BLACK, rect, 2)
            if key == "requester":
                text_surface = font.render(selected_service.name, True, BLACK)
            elif key == "info":
                text_surface = font.render(selected_item, True, BLACK)
            elif key == "agent":
                text_surface = font.render(selected_agent.name if selected_agent else "Agent", True, BLACK)
            elif key == "requestee":
                text_surface = font.render(selected_user.name, True, BLACK)
            text_rect = text_surface.get_rect(center=(rect.x + rect.width // 2, rect.y + rect.height // 2))
            win.blit(text_surface, text_rect)
            if menu_open[key]:
                for i, item in enumerate(menu_items if key == "info" else [button.name for button in service_buttons if
                                                                           key == "requester"] + [button.name for button in
                                                                                                  agent_buttons if
                                                                                                  key == "agent"] + [
                                                                              button.name for button in user_buttons if
                                                                              key == "requestee"]):
                    if key == 'info':
                        pygame.draw.rect(win, BLACK, (rect.x, rect.y + 50 + i * 50, 180, 50), 1)
                        text_surface = font.render(item, True, BLACK)
                        text_rect = text_surface.get_rect(center=(rect.x + 90, rect.y + 75 + i * 50))
                        win.blit(text_surface, text_rect)
                    else:
                        pygame.draw.rect(win, BLACK, (rect.x, rect.y + 50 + i * 50, 150, 50), 1)
                        text_surface = font.render(item, True, BLACK)
                        text_rect = text_surface.get_rect(center=(rect.x + 75, rect.y + 75 + i * 50))
                        win.blit(text_surface, text_rect)

        current_time = pygame.time.get_ticks()



        def drawline(start,msg,drawn_lines):
            line = (start, msg)
            drawn_lines.append(line)

            font = pygame.font.SysFont(None, 20)
            text = font.render(selected_item, True, BLACK)
            win.blit(image, (msg_pos[0] - 30, msg_pos[1] - 30))

        if state == "sending_to_user":
            if result_info == '' or result_info ==["Listening","Listening"]:
                local_res=existRule(selected_item)
                if local_res is not False:
                    result_info=local_res.replace('\n','').split(', ')
                    print(result_info)
                else:
                    result_info=[local_res,'unknown']

            draw_trajectory = False
            drawn_lines = []

            start_pos = (selected_service.position[0] + 20, selected_service.position[1])
            end_pos = (selected_user.position[0], selected_user.position[1])

            drawline(start_pos,msg_pos,drawn_lines)
            if start_pos[1] < end_pos[1]:
                msg_pos = (msg_pos[0] + msg_speed * (end_pos[0] - start_pos[0]) / get_distance(start_pos, end_pos),
                           msg_pos[1] + msg_speed * (end_pos[1] - start_pos[1]) / get_distance(start_pos, end_pos))
            else:
                msg_pos = (msg_pos[0] + msg_speed * (end_pos[0] - start_pos[0]) / get_distance(start_pos, end_pos),
                           msg_pos[1] - msg_speed * (-end_pos[1] + start_pos[1]) / get_distance(start_pos, end_pos))

            if msg_pos[0] >= end_pos[0]:
                state = "display_user_message"
                state_start_time = pygame.time.get_ticks()
                custom_sentence = f"request has arrived {selected_user.name}"
            else:
                custom_sentence = f"{service_names[selected_service.name]} has sent request to {selected_user.name}"

        elif state == "display_user_message" and current_time - state_start_time >= 1000:
            state = "sending_to_agent"
            msg_pos = (selected_user.position[0], selected_user.position[1])
            custom_sentence = f" request has arrived {selected_user.name}"

        elif state == "sending_to_agent":
            if not selected_agent:
                selected_agent = get_agent(selected_item, agent_buttons)

            start_pos = (selected_user.position[0], selected_user.position[1])
            end_pos = (selected_agent.position[0], selected_agent.position[1])

            drawline(start_pos,msg_pos,drawn_lines)

            if start_pos[1] < end_pos[1]:
                msg_pos = (msg_pos[0] - msg_speed * (-end_pos[0] + start_pos[0]) / get_distance(start_pos, end_pos),
                           msg_pos[1] + msg_speed * (end_pos[1] - start_pos[1]) / get_distance(start_pos, end_pos))
            else:
                msg_pos = (msg_pos[0] - msg_speed * (-end_pos[0] + start_pos[0]) / get_distance(start_pos, end_pos),
                           msg_pos[1] - msg_speed * (-end_pos[1] + start_pos[1]) / get_distance(start_pos, end_pos))

            if msg_pos[0] <= end_pos[0]:
                state = "display_agent_message"
                state_start_time = pygame.time.get_ticks()
                custom_sentence = f"request has arrived {selected_agent.name}"
            else:
                custom_sentence = f"{selected_user.name} has sent request to {selected_agent.name}"

        elif state == "display_agent_message" and current_time - state_start_time >= 1000:
            state = "sending_to_service"
            msg_pos = (selected_agent.position[0], selected_agent.position[1])
            custom_sentence = f" request has arrived {selected_agent.name}"

        elif state == "sending_to_service":
            if result_info !='':
                judge_result =result_info[1]
            else:
                judge_result = "Judgement encounter something wrong"

            start_pos = (selected_agent.position[0], selected_agent.position[1])
            end_pos = (selected_service.position[0], selected_service.position[1])

            drawline(start_pos,msg_pos,drawn_lines)    
        
            if start_pos[1] < end_pos[1]:
                msg_pos = (msg_pos[0] - msg_speed * (-end_pos[0] + start_pos[0]) / get_distance(start_pos, end_pos),
                           msg_pos[1] + msg_speed * (end_pos[1] - start_pos[1]) / get_distance(start_pos, end_pos))
            else:
                msg_pos = (msg_pos[0] - msg_speed * (-end_pos[0] + start_pos[0]) / get_distance(start_pos, end_pos),
                           msg_pos[1] - msg_speed * (-end_pos[1] + start_pos[1]) / get_distance(start_pos, end_pos))

            if msg_pos[0] <= end_pos[0]:
                state = "display_service_message"
                state_start_time = pygame.time.get_ticks()
                if judge_result == 'Unauthorized' or judge_result == 'Unauthorized Agent' or judge_result == 'Judgement encounter something wrong' or judge_result =='agent decline':
                    font_color = RED
                else:
                    font_color = GREEN
                custom_sentence = f"Result: {service_names[selected_service.name]} ask {selected_user.name} for {selected_item}, {selected_agent.name} reply, message is {judge_result}."
            else:
                custom_sentence = f"{selected_agent.name} has sent request to {service_names[selected_service.name]}"

        elif state == "display_service_message" and current_time - state_start_time >= 1000:
            server_address = ('127.0.0.1', 8001)
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect(server_address)
            except OSError as e:
                print(f"Connect to port {server_address[1]} failed: {e}")
            data = "Simulation done, waiting"
            try:
                sock.sendall(data.encode())
            except OSError as e:
                print(f"Send failed: {e}")
            sock.close()

            state = "idle"
            result_info=["Listening","Listening"]

        if draw_trajectory:
            for line in drawn_lines:
                pygame.draw.aaline(win, BLACK, line[0], line[1], 2)

        pygame.display.update()
    pygame.quit()
    sys.exit()

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello from Python Server!')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        received_text = post_data.decode('utf-8')
        print(f"Received from Java: {received_text}")
        global result_info
        message = received_text  
        li = []
        if message !="":
            try:
                data = json.loads(message)
                for item in data:
                    li.append(item.get('message'))
            except json.JSONDecodeError as e:
                print("Error decoding JSON:", e)
            except Exception as e:
                print("An error occurred:", e)    
        result_info=li
        global state
        state = "sending_to_user"
        self.send_response(200)
        self.end_headers()
        response = b'ACK from Python'
        self.wfile.write(response)
        #write to local
        temp = str(li).replace('\'','').replace('[','').replace(']','')+('\n')
        if existRule(temp) is False:           
            with open('rule.txt', 'a') as file:
                file.write(temp)


            
def run_server(port, server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd on port {server_address[1]}...')
    httpd.serve_forever()

if __name__ == "__main__":

    server_thread_8000 = threading.Thread(target=run_server, args=(8000,))
    server_thread_8000.daemon = True
    server_thread_8000.start()

    main()
