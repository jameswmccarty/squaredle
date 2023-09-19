#!/usr/bin/python

# for https://squaredle.app

from collections import deque

dims = (4,4)
letters = "CDHEEYOTENTFANRA" 

word_list = set()
with open("enable1.txt","r") as infile:
	word_list = { line.strip().upper() for line in infile }

move_list = { (0,1)   : 'D',
			  (0,-1)  : 'U',
			  (1,0)   : 'R',
			  (-1,0)  : 'L',
			  (-1,-1) : 'UL',
			  (1,1)   : 'DR',
			  (1,-1)  : 'UR',
			  (-1,1)  : 'DL' }

def words_from_pos(index):
	found = set()
	x,y = index%dims[0],index//dims[0]
	q = deque()
	q.append(((x,y),letters[index],'',set(((x,y),))))
	while len(q) > 0:
		pos,built,moves,seen = q.popleft()
		x,y = pos
		if built in word_list and len(built) > 3:
			found.add((built,moves))
		for dx,dy in ((0,1),(0,-1),(1,0),(-1,0),(-1,-1),(1,1),(1,-1,),(-1,1)):
			nx,ny = x+dx,y+dy
			if nx >= 0 and nx < dims[0] and ny >= 0 and ny < dims[1] and (nx,ny) not in seen:
				next_seen = seen.copy()
				next_seen.add((nx,ny))
				q.append(((nx,ny),built+letters[ny*dims[0]+nx],moves+','+move_list[(dx,dy)],next_seen))
	return found

for idx in range(len(letters)):
	print(idx,': (',idx%dims[0],',',idx//dims[0],')',letters[idx])
	print(words_from_pos(idx))
