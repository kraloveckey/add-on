# Implement multithreading using the following module.
from concurrent.futures import ThreadPoolExecutor
# To connect to ports we will use socket.
import socket

def portscan(host):
	ports=list(range(1, 65535))
	portsopened=[]
	# Function to test one port.
	def scanner(port):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.settimeout(0.5)
		try:
			con = s.connect((host, port))
			portsopened.append(port)
			con.close()
		except:
			pass
	with ThreadPoolExecutor(max_workers=5000) as pool:
		pool.map(scanner, ports)
	return(portsopened)
