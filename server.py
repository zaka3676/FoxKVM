import socket
import logging
import threading
from lib import specialKeys
from lib.pynput import keyboard

class serverStart():
    def Start(self, port):
        print("serverStart was started")
        self.hotkey_combination = '<ctrl>+<shift>+q'
        self.switch = False
        self.listener_stop_event = threading.Event()
        self.listener = None # Initialize listener instance
        
        self.SEPARATOR = "{|}"

        self.host = "0.0.0.0"
        self.port = port
        self.BUFFER_SIZE = 14

        self.s = socket.socket()
        logging.basicConfig(level=logging.DEBUG)
        self.bind()
        self.run()
        threading.Thread(target=self.hotkey_listener).start()
        

    def bind(self):
        self.s.bind((self.host, self.port))
        self.s.listen(5)
        print(f"[*] Listening as {self.host}:{self.port}")
    
    def run(self):
        self.client_socket, self.address = self.s.accept()
        print(f"[+] {self.address} is connected.")
        threading.Thread(target=self.reciver).start()
                
    def reciver(self):
        while True:
            self.received = self.client_socket.recv(self.BUFFER_SIZE).decode()
            print(f"[!] Received from {self.address}: " + self.received)
            if self.received == 'hotkey':
                self.toggle_listener()
        
            
        ## HOTKEY
            
    def hotkey_listener(self):
        self.hotkey = keyboard.HotKey(
            keyboard.HotKey.parse(self.hotkey_combination),
            self.toggle_listener)
        with keyboard.Listener(
            on_press=self.for_canonical(self.hotkey.press),
            on_release=self.for_canonical(self.hotkey.release)) as self.hotkey_listener:
            self.hotkey_listener.join()
            
    def toggle_listener(self):
        if self.switch:
            self.switch = False
            self.listener_stop_event.set()  # Signal listener to stop
            if self.listener:
                self.listener.join()
        else:
            self.switch = True
            self.listener_stop_event.clear()  # Clear the event flag
            self.listener = threading.Thread(target=self.on_press_listener)
            self.listener.start()
        print("[!] Switch was set to " + str(self.switch))
        
    def for_canonical(self, f):
        return lambda k: f(self.hotkey_listener.canonical(k))
    
        ## LISTENER FUNCTIONALITY
        
    def on_press_listener(self):
        with keyboard.Listener(suppress=True, on_press=self.on_press, on_release=self.on_release) as self.listener:
            self.listener_stop_event.wait()
            
    def send_event(self, event_type, key):
        if key != None:
            if hasattr(key, "char"):
                strKey = key.char
            else:
                strKey = specialKeys.getId.get(key)

            data = f'{event_type}{self.SEPARATOR}{strKey}'.encode().ljust(self.BUFFER_SIZE, b'\x00')
            self.client_socket.sendall(data)

            logging.debug('Key {0} was {1} and sent'.format(key, event_type))
        
    def on_press(self, key):
        self.send_event("press", key)

    def on_release(self, key):
        self.send_event("release", key)
            
#test = serverStart()
#test.Start(5001)