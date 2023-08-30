import socket
from lib.pynputMacFixed.lib.pynput.keyboard import Controller, Listener, HotKey
import logging
from lib import specialKeys
import threading

keyboard = Controller()


class ClientStart:
    def start(self, port, ip):
        self.hotkey_combination = '<ctrl>+<shift>+q'
        
        self.SEPARATOR = "{|}"
        self.host = ip
        self.port = port 
        
        logging.basicConfig(level=logging.DEBUG)
        
        # create the client socket
        self.s = socket.socket()
        self.BUFFER_SIZE = 30
        
        
        print("[!] Keyboard share client enabled")
        self.connect()
        self.ping()
        threading.Thread(target=self.hotkey_listener).start()
        self.reciver()
        
        
    def connect(self):
        print(f"[+] Connecting to {self.host}:{self.port}")
        self.s.connect((self.host, self.port))
        print("[+] Connected.")
        
    def ping(self):
        logging.debug("[!] Version was sent")
        self.s.sendall(b'Version: 0.1d')
        
    def reciver(self):
        while True:
            self.received = self.s.recv(self.BUFFER_SIZE).rstrip(b'\x00').decode()
            logging.debug(f"Received data without padding: " + self.received)
                
            action, key = self.received.split(self.SEPARATOR)
            
            if len(key) > 1:
                key = specialKeys.getKey.get(key)
            
            if action == "press":
                self.press(key)
            if action == "release":
                self.release(key)
            
            logging.debug('Key {0} was {1}'.format(key, action))
                
    def press(self, key):
        keyboard.press(key)
        
    def release(self, key):
        keyboard.release(key)
        
        
    ## HOTKEY
            
    def hotkey_listener(self):
        self.hotkey = HotKey(
            HotKey.parse(self.hotkey_combination),
            self.send_hotkey)
        with Listener(
            on_press=self.for_canonical(self.hotkey.press),
            on_release=self.for_canonical(self.hotkey.release)) as self.hotkey_listener:
            self.hotkey_listener.join()
            
    def send_hotkey(self):
        self.s.sendall(b'hotkey')
        print("[!] Send hotkey to server.")
        
    def for_canonical(self, f):
        return lambda k: f(self.hotkey_listener.canonical(k))
