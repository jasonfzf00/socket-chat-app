import socket
import threading
import shutil
import sys

stop_event = threading.Event()
LOCK = threading.Lock()

def exception_handling(s):
    stop_event.set()
    s.shutdown(socket.SHUT_RDWR)

def print_message(message):
    """ Allow printing message while user still typing """
    with LOCK:
        for line in str.splitlines(message):
            print(
                "\u001B[s"             # Save current cursor position
                "\u001B[A"             # Move cursor up one line
                "\u001B[999D"          # Move cursor to beginning of line
                "\u001B[S"             # Scroll up/pan window down 1 line
                "\u001B[L",            # Insert new line
                 end="")     
            print(line, end="")        # Print message line
            print("\u001B[u", end="")  # Move back to the former cursor position
        term_size = shutil.get_terminal_size()
        rows, columns = term_size.lines, term_size.columns
        print(f"\033[{rows};1H")
        print(":", end="", flush=True)  # Flush message

def receive_messages(s):
    while not stop_event.is_set():
        try:
            message = s.recv(1024).decode()
            if message:
                print_message(message)
        except Exception as e:
            exception_handling(s)
            break

def send_messages(s):
    while True:
        try:
            inp = input(': ').strip()
            if not inp:
                print("Please enter text!")
                continue
            s.sendall(inp.encode())

            if inp == "exit":
                stop_event.set()
                print("communication end！")
                break
        except KeyboardInterrupt:
            exception_handling(s)
            break
        except Exception as e:
            exception_handling(s)
            break

def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <host> <port>")
        sys.exit(1)

    host, port = sys.argv[1:3]
    
    ip_port = (host, port)

    s = socket.socket()
    s.connect(ip_port)
    print(s.recv(1024).decode())
    
    receive_thread = threading.Thread(target=receive_messages,args=(s,))
    # receive_thread.daemon = True 
    receive_thread.start()

    send_messages(s)
    receive_thread.join()
    s.close()
    
if __name__=="__main__":
    main()