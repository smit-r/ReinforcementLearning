import random
import pygame


class Agent:
    def __init__(self, height, width, snake_block):
        self.action = None
        self.prev_action = None
        self.actions = ['l', 'r', 'u', 'd']
        self.state = None
        self.prev_state = None
        self.qvalues = {'food acquired_': [0,0,0,0]}
        self.height = int(height/snake_block)
        self.width = int(width/snake_block)
        self.corners = [[0,0], [0,height-snake_block], [width-snake_block,0], [width-snake_block,height-snake_block]]
        #self.qv = np.zeros((2*self.height-1, 2*self.width-1, 5, len(self.actions)))
        self.snake_block = snake_block
        self.gamma = 0.1
        self.epsilon = 0.1
        self.alpha = 0.1
        self.policy = {'q1':[0.25,0.25,0.25,0.25], 'q2':[0.25,0.25,0.25,0.25], 'q3':[0.25,0.25,0.25,0.25], 'q4':[0.25,0.25,0.25,0.25], 'lf':[0.25,0.25,0.25,0.25], 'rf':[0.25,0.25,0.25,0.25], 'uf':[0.25,0.25,0.25,0.25], 'bf':[0.25,0.25,0.25,0.25]}
        self.episodes = 0

    def nextaction(self, org_state):
        self.prev_action = self.action
        state = self.state if self.state != 'food acquired_' else org_state
        if random.random() <= 1 - self.epsilon:
            self.action = self.argmaxqv(self.qvalues[state])
        else:
            self.action = self.actions[random.randint(0,3)]
        #if self.state == "food acquired_":
            #print("action : " + self.action + " in state : " + state)
        return self.action

    def nextKeyAction(self, a):
        self.prev_action = self.action
        self.action = a
        return self.action

    def argmaxqv(self, qv):
        top = float("-inf")
        top_values = []
        for i in range(len(qv)):
            if qv[i] > top:
                top = qv[i]
                top_values = [i]
            if qv[i] == top:
                top_values.append(i)
        a = random.choice(top_values)
        return self.actions[a]

    def updatenewstate(self, head, food, snakeList, gameover, foodacquired):
        disx = abs(int((head[0] - food[0])))
        disy = abs(int((head[1] - food[1])))
        bl = snakeList[1:-1]
        nb = []
        b = ''
        if len(bl) > 0:
            if [head[0]+self.snake_block, head[1]] in bl:
                nb.append('r')
            if [head[0], head[1]+self.snake_block] in bl:
                nb.append('d')
            if [head[0]-self.snake_block, head[1]] in bl:
                nb.append('l')
            if [head[0], head[1]-self.snake_block] in bl:
                nb.append('u')
        if head[0] == 0:
            b = 'l'
            nb.append(b)
        elif head[0] == self.width*self.snake_block - self.snake_block:
            b = 'r'
            nb.append(b)
        elif head[1] == 0:
            b = 'u'
            nb.append(b)
        elif head[1] == self.height*self.snake_block - self.snake_block:
            b = 'd'
            nb.append(b)
        if head[0] > food[0] and head[1] < food[1]:
            s = 'q1'
        elif head[0] < food[0] and head[1] < food[1]:
            s = 'q2'
        elif head[0] < food[0] and head[1] > food[1]:
            s = 'q3'
        elif head[0] > food[0] and head[1] > food[1]:
            s = 'q4'
        elif head[0] == food[0]:
            s = "q12" if head[1] < food[1] else "q34"
        elif head[1] == food[1]:
            s = "q23" if head[0] < food[0] else "q41"
        if head in self.corners:
            s = 'c' + str(self.corners.index(head))
            b = ''
        if gameover:
            s = 'game over'
            nb = []
            b = ''
            self.prev_action = self.action
        nb.sort()
        nbs = ''
        for n in nb:
            nbs += n
        s = s + nbs #+ "_" + b
        if s not in self.qvalues.keys():
            self.qvalues[s] = [0,0,0,0]
            print("state added : " + s)
        if foodacquired:
            org_state = s
            s = 'food acquired_'
        else:
            org_state = None
        self.prev_state = self.state
        self.state = s
        return [disx, disy], org_state

    def updateState(self, head, food, game_over, food_acquired):
        if head[0] > food[0] and head[1] < food[1]:
            s = 'q1'
        elif head[0] < food[0] and head[1] < food[1]:
            s = 'q2'
        elif head[0] < food[0] and head[1] > food[1]:
            s = 'q3'
        elif head[0] > food[0] and head[1] > food[1]:
            s = 'q4'
        #if head[0] == 0 or head[0] == self.width - self.snake_block or head[1] == 0 or head[1] == self.height - self.snake_block:
        #    s = s + 'b'
        if head[1] == food[1]:
            if head[0] < food[0]:
                s = 'lf'
            elif head[0] > food[0]:
                s = 'rf'
            else:
                s = 'q1'
        if head[0] == food[0]:
            if head[1] < food[1]:
                s = 'uf'
            else:
                s = 'df'
        if game_over:
            s = 'game over'
            self.prev_action = self.action
        if food_acquired:
            s = 'food'
        self.prev_state = self.state
        self.state = s

    def QLearn(self, reward, org_state):
        if self.state == 'game over':
            self.qvalues[self.prev_state][self.actions.index(self.action)] += self.alpha*(reward - self.qvalues[self.prev_state][self.actions.index(self.action)])
            #print(self.state + " with action : " + self.action + " from : " + self.prev_state)
            return
        #if self.state == 'food acquired_':
            #print(self.state + " with action : " + self.prev_action + " from : " + self.prev_state + " and next action : " + self.action + " from : " + org_state)
        self.qvalues[self.prev_state][self.actions.index(self.prev_action)] += self.alpha*(self.gamma*max(self.qvalues[self.state]) + reward - self.qvalues[self.prev_state][self.actions.index(self.prev_action)])


