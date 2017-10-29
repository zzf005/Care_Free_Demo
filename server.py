import socket
import asyncore
import threading

MAX_RECV = 1024
clientList = []

class Build_Server(asyncore.dispatcher):   
    def __init__(self, port):
        #asyncore.dispatcher的constructor
        asyncore.dispatcher.__init__(self)
        #client socket
        self.clientSocket = None
        #server port
        self.port = port
        #建立等待的socket
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(('127.0.0.1', self.port))
        self.listen(5)
  
    def handle_accept(self):
        #接受client socket的連線
        self.clientSocket = None
        self.clientSocket, address = self.accept()
        print ('New client from : ' + address[0])
        #將和client連線的socket加上一些功能 (自訂socket)
        self.clientSocket = clientList.append(Client_Socket(self.clientSocket))


#自訂的client連線socket
class Client_Socket(asyncore.dispatcher):
    def __init__(self, socket):
        asyncore.dispatcher.__init__(self, socket)
        #要送出的data
        self.sendData = ""
        #self.handle_write()
       
   #從client收到的data
    def handle_read(self):
        self.RecvData = str(self.recv(MAX_RECV)).split("'")
        if len(self.RecvData) > 0:
            print (self.RecvData[1])
            if ("status_danger" in self.RecvData[1]):
               self.sendData = "status_danger"
               cmd = self.sendData
               self.send_cmd(cmd)
            elif ("status_norm" in self.RecvData[1]):
               self.sendData = "status_norm"
               cmd = self.sendData
               self.send_cmd(cmd)
            elif ("bpm_over" in self.RecvData[1]):
               self.sendData = "bpm_over"
               cmd = self.sendData
               self.send_cmd(cmd)
            elif ("bpm_norm" in self.RecvData[1]):
               self.sendData = "bpm_norm"
               cmd = self.sendData
               self.send_cmd(cmd)
               
   #送出data到client
    def send_cmd(self, cmd):
        for i in range(len(clientList)):
            clientList[i].handle_write(cmd)
   
    def handle_write(self, cmd):
        try:
            self.send(bytes(cmd, 'ascii'))
            print(cmd)
        except:
            #print("send error")
            pass
        
   #不自動執行handle_write
    def writable(self):
        return False
  
    def handle_close(self):
        print ("close connection")
        self.close()
        clientList.pop()
        
        
#產生等待client連線的thread
class Forward_Server(threading.Thread):
    def __init__(self,port):
        self.forward_Server = Build_Server(port)
        threading.Thread.__init__ ( self )
      
    def run(self):
        print ("Listen Client ...")
        asyncore.loop()
         
 
if __name__ == "__main__":
    port = 8787
   #產生等待client連線的thread
    listen_thread = Forward_Server(port)
    listen_thread.start()
    listen_thread.join()