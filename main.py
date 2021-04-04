from environment import EnvGame
from agent import Agent
import pickle

if __name__=='__main__':
    grid_dim = [200, 200]
    env = EnvGame(grid_dim[0], grid_dim[1])
    agent = Agent(grid_dim[0], grid_dim[1], env.snake_block)
    episodes = 500
    score_max = 0
    for e in range(episodes):
        statevalue = env.start()
        d1, _ = agent.updatenewstate(statevalue['head'], statevalue['food'], statevalue['snakeList'], statevalue['game_over'], statevalue['food_acquired'])
        steps = 0
        org_state = None
        if e != 0 and e%100 == 0:
            agent.epsilon /= 2
            print("epsilon value : " + str(agent.epsilon))
        while not statevalue['game_over']:
            action = agent.nextaction(org_state)
            #a = input()
            #action = agent.nextKeyAction(a)
            #print(action)
            steps += 1
            if steps > 1:
                agent.QLearn(reward, org_state)
                #print(reward)
            statevalue = env.step(action)
            if not statevalue['food_acquired']:
                d2, _ = agent.updatenewstate(statevalue['head'], statevalue['food'], statevalue['snakeList'], statevalue['game_over'], statevalue['food_acquired'])
            else:
                d2, org_state = agent.updatenewstate(statevalue['head'], statevalue['new_food'], statevalue['snakeList'], statevalue['game_over'], statevalue['food_acquired'])
            if agent.prev_state == 'food acquired_':
                agent.prev_state = org_state
            #print(agent.state)
            reward = (d1[0] - d2[0] + d1[1] - d2[1])/agent.snake_block
            d1 = d2
            if statevalue['game_over']:
                reward = -100
                score = len(statevalue['snakeList'])
            elif statevalue['food_acquired']:
                reward = 100
            #print(agent.state + " from " + agent.prev_state + " with " + a + " reward : " + str(reward))
        agent.QLearn(reward, org_state)
        score_max = max(score_max, score)
        with open('qvalues.txt', 'wb') as file:
            pickle.dump(agent.qvalues, file)
        file.close()
        print("episodes completed : " + str(e) + " score_max : " + str(score_max))
        print(agent.qvalues)

