import sys
from bleak import BleakScanner, BleakClient
import asyncio
from time import sleep
import threading, queue
import socket
from datetime import datetime
import json
from bffacilities.utils import createLogger
import logging
logger = createLogger("bt", level=logging.DEBUG,\
    savefile=False, stream=True, timeformat="%H:%M:%S" )

if sys.platform == "win32":
    from Windows.Devices.Bluetooth.Advertisement import BluetoothLEAdvertisementFilter, BluetoothLEAdvertisement 
else:
    raise ValueError("Unsupported")

class BluetoothWrapper(object):
    """封装蓝牙操作
    """
    IO_DATA_CHAR_UUID_W   = "0000ffe1-0000-1000-8000-00805f9b34fb"
    IO_DATA_CHAR_UUID_W2  = "0000ffe2-0000-1000-8000-00805f9b34fb"

    def __init__(self, **kwargs):
        self._btMsgProcessors = []
        processor = kwargs.get("btMsgProcessor")
        if processor is not None:
            self._btMsgProcessors.append(processor)
        self.loop = asyncio.get_event_loop()
        self._msgToBtQueue = queue.Queue()
        self._cmdQueue = queue.Queue()

        self._btClient = None
        self._btConnected = False
        self._devices = { } # key address

    @property
    def is_connected(self):
        return self._btConnected
    @property
    def btMsgProcessor(self):
        return self._btMsgProcessors
    
    @btMsgProcessor.setter
    def btMsgProcessor(self, p):
        self._btMsgProcessors.append(p)
    
    def export_deviceInfo(self):
        data = []
        for device in self._devices.values():
            name = device.name if hasattr(device, "name") else None
                
            data.append({
                "address": device.address,
                "name": name,
                "rssi": device.rssi
            })
        data = json.dumps(data)
        return data

    def syncDeviceToOther(self):
        """should be rewrite by subclass
        """
        pass

    def _onRecvBtMsg(self, sender, data):
        """
        Args
            data bytes
        """
        # logger.debug(f"Recv BT & Send: {len(data)}, {self._peer}, {threading.get_ident()}")
        for p in self._btMsgProcessors:
            p(data)

    def listDevice(self, timeout = 10):
        async def _list(timeout):
            devices = await BleakScanner.discover(timeout=timeout)
            for d in devices:
                if d.address not in self._devices:
                    self._devices[d.address] = d
            self.syncDeviceToOther()
        self.loop.run_until_complete(_list(timeout))
    
    def findDevice(self, name = None, seconds = 5.0):
        self.loop.run_until_complete(self.monitDevice(name, seconds))

    async def monitDevice(self, name, seconds=0):
        """
        Args:
            name  device name such as "BTDEVICE1"
        """
        bleFilter = BluetoothLEAdvertisementFilter()
        if name:
            ad = BluetoothLEAdvertisement()
            ad.put_LocalName(name)
            bleFilter.put_Advertisement(ad)

        scanner = BleakScanner(AdvertisementFilter=bleFilter)
        scanner.register_detection_callback(self._detection_callback)
        # await scanner.set_scanning_filter()
        await scanner.start()
        if seconds <= 5:
            while self._btConnected:
                await asyncio.sleep(10)
        else:
            await asyncio.sleep(seconds)
        await scanner.stop()
        logger.info("[BT] Monit Device Done")

    def _detection_callback(self, device, advertisement_data):
        if len(advertisement_data.local_name) is 0:
            return
        if device.address not in self._devices:
            logger.info(f"First [{datetime.now()}] RSSI: {device.rssi}, {advertisement_data.local_name}, {device.address}")
        device.name = advertisement_data.local_name
        self._devices[device.address] = device
        self.syncDeviceToOther()

    async def _connect(self, address):
        """after function exits, bluetooth device will be disconnected
        """
        if self._btClient is not None:
            await self._btClient.disconnect()

        self._btClient = BleakClient(address)
        logger.info(f"[BT] Connecting Bluetooth: {address}")
        # service = await self._btClient.get_services()
        # model_number = await self._btClient.read_gatt_char(BluetoothWrapper.IO_DATA_CHAR_UUID_W )
        # print(f"Model Number {model_number}: {''.join(map(chr, model_number))}")
        try:
            self._btConnected = await self._btClient.connect()
            logger.info(f"[BT] Client {self._btClient} connected: {self._btConnected}")
            if self._btConnected:
                await self._btClient.start_notify(\
                    BluetoothWrapper.IO_DATA_CHAR_UUID_W, \
                    self._onRecvBtMsg)
        except Exception as e:
            self._btConnected = False
            logger.warning(f"[BT] Exception Connect: {e}")
        # finally:
            # await self._btClient.disconnect()


    async def _sendMsgToBt(self):
        if not self._msgToBtQueue.empty():
            sData = self._msgToBtQueue.get()
            await self._btClient.write_gatt_char(BluetoothWrapper.IO_DATA_CHAR_UUID_W, sData)
            logger.debug(f"SendData Bt {sData}")
        else:
            await asyncio.sleep(0)
    
    def sendMsgToBt(self):
        self.loop.run_until_complete(self._sendMsgToBt())

    async def _connectAndListen(self, address):
        await self._connect(address)
        try:
            while self._btConnected:
                await self._sendMsgToBt()
        except Exception as e:
            self._btConnected = False
            logger.warning(f"[BT] Exception Listen: {e}")
        finally:
            await self._btClient.disconnect()
        logger.info("[BT] connect process done")

    def connectToBLE(self, address, listen=True):
        """
        Args: 
            listen true, the event loop will run always and stop main thread
        """
        if listen:
            self.loop.run_until_complete(self._connectAndListen(address))
        else:
            self.loop.run_until_complete(self._connect(address))

    def disconnect(self):
        if self._btConnected:
            logger.info("[BT] Stoping bluetooth, wait for a moment")
            async def _stop():
                await self._btClient.disconnect()
            self.loop.run_until_complete(_stop())
            logger.info("[BT] bluetooth stopped")
        else:
            logger.warning("[BT] Not Connected")


    def _processCmd(self, cmd):
        """
        {
            "action": "listDevice",
            "timeout": "60", // seconds
        }

        {
            "action": "findDevice",
            "name": "CMPS", // or no name for find all device
            "timeout": 30, // default 30
        }

        {
            "action": "disconnect" // disconnect if a device has connected
        }

        {
            "action": "quit" // quit program
        }
        """
        logger.debug("Cmd", threading.get_ident())
        action = cmd["action"]
        if action == "connect":
            if "address" in cmd:
                self.connectToBLE(cmd["address"])
        elif action == "listDevice":
            self.listDevice(timeout= cmd.get("timeout", 10))
        elif action == "findDevice":
            self.findDevice(name=cmd.get("name"), seconds= cmd.get("timeout", 20))
        elif action == "disconnect":
            self.disconnect()
        elif action == "quit":
            self.disconnect()
            self._running = False
            logger.info("About to quit")
        else:
            logger.warning("Unsupported cmd", action)

    def processCmd(self):
        """注意，用于蓝牙接收和发送的操作，
        该方法应该在创建 BluetoothWrapper 的线程中调用
        """
        if not self._cmdQueue.empty():
            self.processCmd(self._cmdQueue.get()) 

class BluetoothMgr(BluetoothWrapper) :
    """
    @See bffacilities.socketserver.UdpSocketServer

    默认绑定到 UDP 12001 地址上，用于接收其他模块的控制信息

    """

    def __init__(self, port = 12001, broadcast = True, peer = None, updatePeer=True, **kwargs):
        super().__init__(**kwargs)
        self._bind = port
        self._sockSender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sockSender.bind(("", self._bind))
        self._sockSender.settimeout(1)
        self._sockSender.setblocking(True)

        self._running = True

        self._peer = peer
        self.updatePeer = updatePeer
        self._broadcast = broadcast
        
        self.btMsgProcessor = self.transferDataByUdp
    @property
    def is_running(self):
        return self._running

    def syncDeviceToOther(self):
        if self._peer is None:
            return
        data = self.export_deviceInfo()
        self._sockSender.sendto(data.encode() + b"\n\n", self._peer)

    def transferDataByUdp(self, data):
        if self._peer and self._broadcast:
            self._sockSender.sendto(data, self._peer)

    def startUdpServer(self):

        logger.info(f"[BT] Start Listening UDP {self._bind}, {threading.get_ident()}")
        # self._sockSender.sendto(b'test', ("127.0.0.1", 12000))
        while self._running:
            cmd = None
            try:
                data = self._sockSender.recvfrom(1024)
                if self.updatePeer:
                    self._peer = data[1]
                data = data[0]
                if data.startswith(b"{"):
                    try:
                        cmd = json.loads(data)
                    except: pass
                    if cmd is not None:
                        # self._processCmd(cmd)
                        # 避免直接在子线程运行 bt 相关的代码
                        self._cmdQueue.put(cmd)
                self._msgToBtQueue.put(data)
            except (socket.timeout , socket.error) as e:
                pass
            except Exception as e:
                logger.critical(f"[BT] Error: {e}" )
                sys.exit(1)
            sleep(0.02)

    def start(self):
        """start an loop in main thread 
        start another thread for udp server
        """
        try:
            # thread = threading.Thread(target = self.startUdpServer)
            # thread.daemon = True
            # thread.start()
            # asyncio.run_coroutine_threadsafe(self.startUdpServer, loop=self.loop)
            while self._running:
                self.processCmd()
                sleep(0.1)
        except (KeyboardInterrupt, SystemExit):
            self.stop()
    
    def stop(self):
        self.disconnect()
        self._running = False
        logger.info("==========Bt Mgr Quit===========")

    def start_one(self):
        thread = threading.Thread(target = self.startUdpServer)
        thread.daemon = True
        thread.start()

if __name__ == "__main__":
    btMgr = BluetoothMgr()
    btMgr.start()