#!/usr/bin/python

# for https://squaredle.app

from collections import deque

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
		self.end = False

	def test(self,char):
		return char in self.children.keys()

	def insert(self,value):
		if len(value) == 0:
			self.end = True
		elif len(value) > 0:
			if not self.test(value[0]):
				self.children[value[0]] = Node()
			self.children[value[0]].insert(value[1:])

	def walk(self,char):
		if self.test(char):
			return self.children[char]
		return None

def words_from_pos(index,dims,letters,prefix_map):
	found = set()
	x,y = index%dims[0],index//dims[0]
	q = deque()
	q.append(((x,y),letters[index],'',set(((x,y),)),prefix_map))
	while len(q) > 0:
		pos,built,moves,seen,location = q.popleft()
		x,y = pos
		if location.end and len(built) > 3:
			found.add((built,moves[1:]))
		for dx,dy in move_list.keys():
			nx,ny = x+dx,y+dy
			if nx >= 0 and nx < dims[0] and ny >= 0 and ny < dims[1]:
				next_letter = letters[ny*dims[0]+nx]
				if (nx,ny) not in seen and location.test(next_letter):
					q.append(((nx,ny),built+next_letter,moves+','+move_list[(dx,dy)],{*seen,(nx,ny)},location.walk(next_letter)))
	return sorted(found)

def solve(puzzle,dims,prefix_map):
	for idx,char in enumerate(puzzle):
		if prefix_map.test(char):
			print(f"{idx} : ({idx%dims[0]},{idx//dims[0]}) {puzzle[idx]}")
			print(words_from_pos(idx,dims,puzzle.upper(),prefix_map.walk(char)))

if __name__ == "__main__":

	root = Node()
	with open("enable1.txt","r") as infile:
		for line in infile:
			root.insert(line.strip().upper())

	#solve("CDHEEYOTENTFANRA",(4,4),root)

	solve("VRLTOGANIKSGMLAEUOLBRDWPF",(5,5),root)
	#solve("XYHWITSIINCELNSECNDSEYGUIROTTETLASPNEITXSBTHCATUTJOILICHLCIOINROTALANCTYAKUYRLTDIULNTERIZEXENOVEQUSA",(10,10),root)
