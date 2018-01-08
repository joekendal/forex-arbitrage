import requests, json, math


CURRENCIES = {'GBP', 'USD', 'JPY', 'EUR'}
API_KEY = ''

class Node(object):
	def __init__(self, currency_id, CURRENCIES):
		super(Node, self).__init__()
		self.id = currency_id
		self.childs = []
		for id in CURRENCIES:
			if id == self.id:
				pass
			else:
				self.childs.append(id)
		self.rates = []
		for child in self.childs:
			url = 'https://v3.exchangerate-api.com/pair/{}/{}/{}'.format(API_KEY, self.id, child)
			response = requests.get(url)
			data = response.json()
			self.rates.append((child, math.log(data['rate'])))
		self.rates = dict(self.rates)


def pull_data():
	nodes = []
	for currency_id in CURRENCIES:
		node = Node(currency_id, CURRENCIES)
		node = (node.id, node.rates)
		nodes.append(node)

	return nodes

currencies = pull_data()
currencies = dict(currencies)

def initialize(graph, source):
	destination = {}
	predecessor = {}
	for node in graph:
		destination[node] = float('Inf')
		predecessor[node] = None
	destination[source] = 0
	return destination, predecessor


def relax(node, neighbour, graph, destination, predecessor):
	if destination[neighbour] > destination[node] + graph[node][neighbour]:
		destination[neighbour] = destination[node] + graph[node][neighbour]
		predecessor[neighbour] = node

def retrace_negative_loop(p, start):
	arbitrageLoop = [start]
	next_node = start
	while True:
		next_node = p[next_node]
		if next_node not in arbitrageLoop:
			arbitrageLoop.append(next_node)
		else:
			arbitrageLoop.append(next_node)
			arbitrageLoop = arbitrageLoop[arbitrageLoop.index(next_node):]
			return arbitrageLoop

def bellman_ford(graph, source):
	destination, predecessor = initialize(graph, source)
	for i in range(len(graph)-1):
		for u in graph:
			for v in graph[u]:
				relax(u, v, graph, destination, predecessor)

	for u in graph:
		for v in graph[u]:
			return(retrace_negative_loop(predecessor, source))

	return None

paths = []

graph = currencies

for key in graph:
	path = bellman_ford(graph, key)
	if path not in paths and not None:
		paths.append(path)

for path in paths:
	if path == None:
		pass
	elif len(path) < 4:
		pass
	else:
		x = 100000
		print("x = {} {}".format(x, path[0]))

		for i,value in enumerate(path):
			if i+1 < len(path):
				start = path[i]
				end = path[i+1]
				rate = math.exp(-graph[start][end])
				x *= rate
				print("\t{}->{} @{} = {} {}".format(start, end, rate, x, end))
	print("\n")

