#!/usr/bin/python

# for https://squaredle.app

from collections import deque

# global
word_list = set()

move_list = { (0,1)   : 'D',
			  (0,-1)  : 'U',
			  (1,0)   : 'R',
			  (-1,0)  : 'L',
			  (-1,-1) : 'UL',
			  (1,1)   : 'DR',
			  (1,-1)  : 'UR',
			  (-1,1)  : 'DL'}

class Node:

	def __init__(self):
		self.children = dict()

	def insert(self,value):
		if len(value) > 0:
			if value[0] not in self.children:
				self.children[value[0]] = Node()
			self.children[value[0]].insert(value[1:])

	def test(self,char):
		if char in self.children.keys():
			return True
		return False

	def walk(self,char):
		if self.test(char):
			return self.children[char]
		return None

def build_prefix_map(words):
	root = Node()
	for entry in words:
		root.insert(entry)
	return root

def words_from_pos(index,dims,letters,prefix_map):
	found = set()
	x,y = index%dims[0],index//dims[0]
	q = deque()
	q.append(((x,y),letters[index],'',set(((x,y),)),prefix_map))
	while len(q) > 0:
		pos,built,moves,seen,location = q.popleft()
		x,y = pos
		if built in word_list and len(built) > 3:
			found.add((built,moves[1:]))
		for dx,dy in move_list.keys():
			nx,ny = x+dx,y+dy
			if nx >= 0 and nx < dims[0] and ny >= 0 and ny < dims[1] and (nx,ny) not in seen and location.test(letters[ny*dims[0]+nx]):
				next_seen = seen.copy()
				next_seen.add((nx,ny))
				q.append(((nx,ny),built+letters[ny*dims[0]+nx],moves+','+move_list[(dx,dy)],next_seen,location.walk(letters[ny*dims[0]+nx])))
	return sorted(found)

def solve(puzzle,dims,prefix_map):
	for idx in range(len(puzzle)):
		print(f"{idx} : ({idx%dims[0]},{idx//dims[0]}) {puzzle[idx]}")
		print(words_from_pos(idx,dims,puzzle,prefix_map))

if __name__ == "__main__":

	with open("enable1.txt","r") as infile:
		word_list = { line.strip().upper() for line in infile }
	
	root = build_prefix_map(word_list)

	solve("CDHEEYOTENTFANRA",(4,4),root)

	#solve("VRLTOGANIKSGMLAEUOLBRDWPF",(5,5),root)
