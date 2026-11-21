from pynput import keyboard
import socket




def client_program():
    print("trying to connect to server")
    # get the host ip
    host = socket.gethostbyname(socket.gethostname())  # as both codes are running on same pc
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    host = s.getsockname()[0]
    s.close()
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    print("waiting for keyboard input")
    print("waiting for keyboard input")
    print("Use W/A/S/D to move, Q to quit.")

    def on_press(key):
        try:
            letter = key.char.lower()
        except AttributeError:
            return

        if letter in ('w', 'a', 's', 'd', 'q'):
            client_socket.sendall(letter.encode())
            print("Sent:", letter)

        if letter == 'q':
            return False

    try:
        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()
    finally:
        client_socket.close()
    

    


if __name__ == '__main__':
    client_program()