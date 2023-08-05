import json
import socket
import select
from .utils import createLogger
logger = createLogger('sockserver', savefile=False, stream=True)

__version__ = "0.1.3"

class EventHandler:
    def fileno(self):
        """Return the associated file descriptor"""
        raise ValueError('Not Implemented must implement')

    def handle_receive(self):
        'Perform the receive operation'
        pass

    def handle_send(self):
        'Send outgoing data'
        pass

    def handle_except(self):
        pass

    def is_valid(self):
        return True

class SocketClient(EventHandler):
    """
    1. 通过继承该类进行客户端编写，
    2. 通过 parser 回调函数进行消息读取

    Args:
        sock: socket
        address: client socket address recved from server,
            useful when other want to communicate or 
            identify the client

        except_callback: function(client: SocketClient)
    """
    def __init__(self, sock, address, **kwargs):
        self.sock = sock
        self.sock.setblocking(False)
        self.address = address
        self._isValid = True

        self._parse = None
        self._server = None
        self.except_callback = kwargs.get("except_callback", None)
    @staticmethod
    def createTcpClient(serverAddr):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sc = SocketClient(sock, ("127.0.0.1", 0))
        sc.sock.setblocking(True)
        sc._server = serverAddr
        return sc

    def connect(self):
        if self._server is None:
            return
        try:
            self.sock.connect(self._server)
        except:
            logger.warning(f"Error connecting {self._server}")
            self.handle_except()
        finally:
            pass

    def shutdown(self):
        self.sock.close()

    def __del__(self):
        self.sock.close()

    @property
    def parser(self):
        return self._parse

    @parser.setter
    def parser(self, parse):
        """传入一个解析器即可
        ```py
        # data is a dict
        def parse(data, socketClient): print(data, socketClient)

        client.parser = parse
        ```
        """
        try:
            parse('"test"', self)
            self._parse = parse
        except:
            logger.critical(f"[TC] ***** Error testing parser, it will be ignored ****")

    def is_valid(self):
        return self._isValid

    def fileno(self):
        return self.sock.fileno()

    def __repr__(self):
        return f'<Socket Client, {self.sock.fileno()}, {self.address}>'

    def handle_receive(self):
        """Handle receive data, default processor
        subclass could replace this methods to receive binary data
        """
        msg = None
        try:
            msg = self.sock.recv(1024)
            if not msg:
                self.handle_except()
                return
        except socket.error:
            self.handle_except()
        except Exception as e:
            logger.warning(f"[TC] recv {e}")
        
        if msg is None: return

        if self._parse:
            try:
                self._parse(msg.decode(), self)
            except Exception as e:
                logger.warning(f"[TC] parse {e}")
        else:
            logger.debug(msg)

    def handle_send(self):
        pass
    def handle_except(self):
        """注意不要在 callback 中重新创建 client，否则函数调用堆栈将会溢出
        """
        self.sock.close()
        self._isValid = False
        if self.except_callback:
            self.except_callback(self)

import sys

class BaseServer():
    """ One can easily extend the base server for Tcp/Udp connection
    """
    def __init__(self):
        self._recvList = []
        self._sendList = []
        self._exceptList = []
        self.running = False

    def stop(self):
        self.running = False

    def serve_forever(self):
        self.running = True
        while self.running:
            self.serve_once(0.1)
    
    def serve_once(self, timeout=0.001):
        can_recv, can_send, exc = select.select(self._recvList, self._sendList, self._exceptList, timeout)
        for h in can_recv:
            h.handle_receive()
        for h in can_send:
            h.handle_send()
        for h in exc:
            h.handle_except()
        # self.checkClients() # upper level call it

class TcpSocketServer(EventHandler, BaseServer):
    """
    Args:
        ip address
        port
    """
    ClientClass = SocketClient
    def __init__(self, ip, port, maxconn = 500):
        super().__init__()
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._clients = {}
        # key: address tuple, value SocketClient
        self._recvList.append(self)
        # self._sendList = []
        self._exceptList.append(self)
        self._clientAdded = None
        self._clientRemoved = None
        try:
            self._server.bind((ip, port))
            logger.info(f"[TSS] Server Listening: {ip}:{port}")
        except Exception as e:
            logger.critical(f"[TS] Unable to listening {ip}:{port}")
            sys.exit(1)

        self._server.listen(maxconn)
        self._server.setblocking(False)
        self.maxconn = maxconn

    def setClientAddedCallback(self, p):
        """ callback """
        self._clientAdded = p

    def setClientRemovedCallback(self, p):
        """ callback """
        self._clientRemoved = p

    def fileno(self):
        return self._server.fileno()

    def needs_receive(self):
        return True

    def serve_forever(self):
        self.running = True
        count = 0
        while self.running:
            self.serve_once()
            count += 1
            if count == 6000:
                self.checkClients()

    def shutdown(self):
        self.removeAll()
        self._server.close()

    def __del__(self):
        self.removeAll()
        self._server.close()

    def checkClients(self):
        clients = list(self._clients.values())
        for c in clients:
            if not c.is_valid():
                self.removeClient(c)

    def removeAll(self):
        clients = list(self._clients.values())
        for c in clients:
            c.shutdown()
            self.removeClient(c)

    def removeClient(self, client):
        """
        Args
            client: SocketClient
        """
        if client == self: return

        logger.info(f"[TS] Removeing {client.address}")
        if client in self._recvList:
            try:
                self._recvList.remove(client)
            except: pass
        if client in self._exceptList:
            try:
                self._exceptList.remove(client)
            except: pass
        if client in self._sendList:
            try:
                self._sendList.remove(client)
            except: pass
        if client.address in self._clients:
            try:
                self._clients.pop(client.address, None)
            except: pass
            
        if self._clientRemoved:
            try:
                self._clientRemoved(client)
            except Exception as e:
                logger.warning(f"[TS] remove callback failed {e}")
    
    def _addClient(self, sock, address):
        """添加一个 客户端 socket，不可手动添加
        """

        c = TcpSocketServer.ClientClass(sock, address, except_callback=self.removeClient)
        self._clients[address] = (c)
        self._recvList.append(c)
        # self._sendList.append(c)
        self._exceptList.append(c)
        if self._clientAdded:
            self._clientAdded(c)
        else:
            logger.debug(f"[TS] client added {address}")

    def handle_receive(self):
        """接收到TCP连接
        """
        (sock, address) = self._server.accept()
        if len(self._clients) >= self.maxconn:
            # 超出最大连接数
            sock.close()
            return
        if address not in self._clients:
            self._addClient(sock, address)
        else:
            self._clients[address].sock = sock
            self._clients[address].address = address
            self._clients[address]._isValid = True
        logger.info(f'[TS] Accept From {address}, Clients Count: {len(self._clients)}')

from datetime import datetime
import threading

class UdpSocketClient(EventHandler):
    def __init__(self, port, ip = "127.0.0.1", name="default", **kwargs):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((ip, port))
        self.sock.setblocking(False)
        self.address = (ip, port)
        self.bufferSize = kwargs.get("bufferSize", 1024)
        self._isValid = True
        self.name = name
        self._parse = None
        self._peer = None
    @property
    def parser(self):
        return self._parse

    @parser.setter
    def parser(self, parse):
        """传入一个解析器即可
        ```
        def parse(data, recver): 
            print(data, "From", recver)

        client.parser = parse
        ```
        """
        self._parse = parse

    def send(self, msg):
        """
        Args
            msg bytes
        """
        if self._peer:
            self.sock.sendto(msg, self._peer)

    def is_valid(self):
        return self._isValid

    def fileno(self):
        return self.sock.fileno()

    def handle_receive(self):
        """Handle receive data, default processor
        subclass could replace this methods to receive binary data
        """
        bytesAdressPair = self.sock.recvfrom(self.bufferSize)
        # message = bytesAdressPair[0]
        self._peer = bytesAdressPair[1]
        if not bytesAdressPair:
            self._isValid = False
            return
        if self._parse:
            try: 
                self._parse(bytesAdressPair, self.name)
            except Exception as e:
                logger.warning(f"[UC] {e}")

    def handle_send(self):
        pass

    def handle_except(self):
        self.sock.close()
        self._isValid = False

class UdpSocketServer(BaseServer):
    """支持绑定到多个UDP端口上，使用 processor 进行回调

    Args:
        port udpsocket will bind into
    """
    def __init__(self, **kwargs):
        super().__init__()
        self._listeners = {}
        self.bufferSize = kwargs.get("bufferSize", 1024)
        self._processors = {}

    def addProcessor(self, processor, name="default"):
        if name not in self._processors:
            self._processors[name] = processor
            # logger.debug(f"[USS] add processor for {name}")
        else:
            logger.warning("[USS] dumplicated add processor.")

    def createListener(self, port, name="default", ip="127.0.0.1", processor = None):
        if name in self._listeners.keys():
            return
        logger.info(f"[USS] Server Listening for '{name}': {ip}:{port}")
        listener = UdpSocketClient(port, ip, bufferSize=self.bufferSize, name=name)
        listener.parser = self.recvfrom
        self._listeners[name] = listener
        self._recvList.append(listener)
        self._exceptList.append(listener)
        if processor is not None:
            self.addProcessor(processor, name)
        # self._sendList.append(listener)

    def sendto(self, name, msg):
        self._listeners[name].sendto(msg)

    def broadcast(self, msg):
        for c in self._listeners.values():
            c.sendto(msg)

    def recvfrom(self, byteAddrPair, name):

        if name in self._processors:
            # process will executed
            process = self._processors[name]
            message = byteAddrPair[0]
            address = byteAddrPair[1]
            process(message.decode(), address)
        else:
            logger.debug(f"No processor for{name}, {byteAddrPair}")
