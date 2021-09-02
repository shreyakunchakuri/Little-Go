#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from copy import deepcopy
import numpy as np

def read_input():
    fileopen = open("input2.txt","r")
    fileopen.seek(0)
    player = int(fileopen.readline())
    for i in range(0,5):
        line = fileopen.readline()
        row_list = [int(x) for x in line.rstrip('\n')]
        prev_state.append(row_list)
    for i in range(0,5):
        line = fileopen.readline()
        row_list = [int(x) for x in line.rstrip('\n')]
        state.append(row_list)
    fileopen.close()
    return player,prev_state,state

def print_output(t_state,action,p_board):
    fileclose = open("output.txt","w")
    #if 0<=action[0]<5 and 0<=action[1]<5 and t_state[action[0]][action[1]] == 0:
    if position_validity(p_board,t_state,player,action[0],action[1]):
        string_output = str(action[0])+","+str(action[1])
        fileclose.write(string_output)
    else:
        fileclose.write("PASS")
    fileclose.close()

def check_died(player,prev_state,state):
    for i in range(0,5):
        for j in range(0,5):
            if(prev_state[i][j] == player and state[i][j] != player):
                dead_players.append((i,j))

def string_neighbours(lib_board,i,j):
    neigh = [(i+1,j),(i-1,j),(i,j+1),(i,j-1)]
    neighbours = []
    for n in neigh:
        if(0<=i<5 and 0<=j<5):
            neighbours.append(n)
    return neighbours

def neighbours_8(b_board,i,j):
    neigh = [(i+1,j),(i+1,j+1),(i-1,j),(i-1,j-1),(i,j+1),(i-1,j+1),(i,j-1),(i+1,j-1)]
    neighbours = []
    for n in neigh:
        if(0<=i<5 and 0<=j<5):
            neighbours.append(n)
    return neighbours

def string_members_func(lib_board,i,j):
    neighbours = string_neighbours(lib_board,i,j)
    string_members = []
    for neigh in neighbours:
        if(0<=neigh[0]<5 and 0<=neigh[1]<5):
            if(lib_board[neigh[0]][neigh[1]] == lib_board[i][j]):
                string_members.append(neigh)
    return string_members
    
def string_dfs(lib_board,i,j):
    dfs_frontier_list = [(i,j)]
    dfs_explored_list = []
    while(dfs_frontier_list):
        mem = dfs_frontier_list.pop()
        dfs_explored_list.append(mem)
        string_members = string_members_func(lib_board,mem[0],mem[1])
        for member in string_members:
            if member not in dfs_frontier_list and member not in dfs_explored_list:
                dfs_frontier_list.insert(0,member)
    return dfs_explored_list
              
def liberty(cboard,turn,i,j):
    liberty_board = copy_board(cboard)
    string_members = string_dfs(liberty_board,i,j)
    for member in string_members:
        member_neighbours = string_neighbours(liberty_board,member[0],member[1])
        for neigh in member_neighbours:
            if(0<=neigh[0]<5 and 0<=neigh[1]<5):
                if(cboard[neigh[0]][neigh[1]] == 0):
                    return True
    return False

def compare_board(board1,board2):
    for i in range(0,5):
        for j in range(0,5):
            if board1[i][j] !=board2[i][j]:
                return False
    return True

def copy_board(board_to_be_copied):
    copied_board = deepcopy(board_to_be_copied)
    return copied_board
    
def KO_rule(present_board,previous_board,d_players):
    if len(d_players) !=0 and compare_board(previous_board,present_board):
        return False
    return True

def find_dead_players(test_board,player_type):
    dead_players = []
    for i in range(0,5):
        for j in range(0,5):
            if test_board[i][j] == player_type:
                if not liberty(test_board,player_type,i,j):
                    dead_players.append((i,j))
    return dead_players

def remove_dead_string(test_board,player_type,d_players):
    for d in d_players:
        test_board[d[0]][d[1]] = 0
    return test_board

def remove_dead_players(test_board,player_type):
    dead_players = find_dead_players(test_board,player_type)
    if dead_players:
        test_board = remove_dead_string(test_board,player_type,dead_players)
        test_board = board_updation(test_board)
        return dead_players,test_board
    return [],test_board

def board_updation(new_board):
    updated_board = new_board
    return updated_board
    
def position_validity(p_board,board,turn,i,j):
    if((0<=i<5) and (0<=j<5) and state[i][j]==0):
        d_players = []
        testing_board = copy_board(board)
        if liberty(testing_board,turn,i,j):
            if KO_rule(p_board,testing_board,d_players):
                return True
        testing_board = copy_board(board)
        test2 = apply_move(testing_board,turn,i,j)
        d_players,testing_board = remove_dead_players(test2,3-turn)
        if liberty(testing_board,turn,i,j):
            if KO_rule(p_board,testing_board,d_players):
                return True
    return False

def apply_move(test_board,player_type,i,j):
    test_board[i][j] = player_type
    test_board = board_updation(test_board)
    return test_board
    
def print_board(board):
    print('-' * len(board) * 2)
    for i in range(0,5):
        for j in range(0,5):
            if board[i][j] == 0:
                print(' ', end=' ')
            elif board[i][j] == 1:
                print('X', end=' ')
            else:
                print('O', end=' ')
        print()
    print('-' * len(board) * 2)
    
def game_over():
    if no_of_moves >= maximum_moves:
        return True
    else:
        return False
    
def eval_func(eval_board):
    score1 = 0
    score2 = 0
    for i in range(0,5):
        for j in range(0,5):
            if(eval_board[i][j] == 1):
                score1 = score1+1
            elif(eval_board[i][j] == 2):
                score2 = score2+1
    score1 = score1
    score2 = score2 + komi
    score = (score1 - score2) if player == 1 else (score2 - score1)
    return score

def get_value(temp_dict, val):
    T_keys = list(temp_dict.keys())
    T_values = list(temp_dict.values())
    #print(temp_dict)
    action = (0,0)
    for i in range(0,len(temp_dict)):
        if T_values[i] == val:
            action = T_keys[i]
            break;
    return action

def moves(p_board,t_board,turn):
    V_moves = []
    nei_moves = []
    visited = [[0,0,0,0,0],
               [0,0,0,0,0],
               [0,0,0,0,0],
               [0,0,0,0,0],
               [0,0,0,0,0]]
    for i in range(0,5):
        for j in range(0,5):
            if(0<=i<5 and 0<=j<5 and t_board[i][j] == turn):
                n_moves = neighbours_8(t_board,i,j)
                for ne in n_moves:
                    if(0<=ne[0]<5 and 0<=ne[1]<5 and visited[ne[0]][ne[1]] == 0):
                        nei_moves.append(ne)
                        visited[ne[0]][ne[1]] = 1
    for nei in nei_moves:
        if(t_board[nei[0]][nei[1]] == 0):
            if(position_validity(p_board,t_board,turn,nei[0],nei[1])):
                V_moves.append((nei[0],nei[1]))
    for i in range(0,5):
        for j in range(0,5):
            if(t_board[i][j] == 0 and visited[i][j] == 0):
                if(position_validity(p_board,t_board,turn,i,j)):
                    V_moves.append((i,j))
    return V_moves

def unmove(t_board,i,j):
    t_board[i][j] = 0
    s_board = board_updation(t_board)
    return s_board

def undead(d_board,d_dead_players,d_turn):
    for p in d_dead_players:
        d_board[p[0]][p[1]] = d_turn
    d_board = board_updation(d_board)
    return d_board

def max_value(previous_board,mboard,tplayer,alpha,beta,co):
    global   alpha_beta_count
    turn = player
    dict_utilities = {}
    alpha_beta_count = alpha_beta_count + 1
    if(alpha_beta_count == 4):
        value = eval_func(mboard)
        dict_utilities = {co : value}
        return dict_utilities,value
    value = np.NINF
    val = np.NINF
    valid_moves = moves(previous_board,mboard,turn)
    #print(valid_moves)
    for v in valid_moves:
        pre_board = mboard
        mboard = apply_move(mboard,turn,v[0],v[1])
        dummy_board = copy_board(mboard)
        dummy_dead_players,dummy_board = remove_dead_players(dummy_board,3-turn)
        U_dict,val = min_value(pre_board,dummy_board,turn,alpha,beta,v)
        dummy_board = undead(dummy_board,dummy_dead_players,3-turn)
        mboard = unmove(mboard,v[0],v[1])
        value = max(value,val)
        alpha_beta_count = alpha_beta_count-1
        dict_utilities.update(U_dict)
        if value >= beta:
            act = get_value(dict_utilities,value)
            dict_to_send = {act : value}
            return dict_to_send,value
        alpha = max(alpha,value)
    act = get_value(dict_utilities,value)
    dict_to_send = {act : value}
    return dict_to_send,value

def min_value(previous_board,mboard,tplayer,alpha,beta,co):
    global alpha_beta_count
    turn = 3-player
    dict_utilities = {}
    alpha_beta_count = alpha_beta_count + 1
    if(alpha_beta_count == 4):
        value = eval_func(mboard)
        dict_utilities = {co : value}
        return dict_utilities,value
    value = np.inf
    val = np.inf
    valid_moves = moves(previous_board,mboard,turn)
    for v in valid_moves:
        pre_board = mboard
        mboard = apply_move(mboard,turn,v[0],v[1])
        dummy_board = copy_board(mboard)
        dummy_dead_players,dummy_board = remove_dead_players(dummy_board,3-turn)
        U_dict,val = max_value(pre_board,dummy_board,turn,alpha,beta,v)
        dummy_board = undead(dummy_board,dummy_dead_players,3-turn)
        mboard = unmove(mboard,v[0],v[1])
        value = min(value,val)
        dict_utilities.update(U_dict)
        alpha_beta_count = alpha_beta_count-1
        if value <= alpha:
            act = get_value(dict_utilities,value)
            dict_to_send = {act : value}
            return dict_to_send,value
        beta = min(beta,value)
    act = get_value(dict_utilities,value)
    dict_to_send = {act : value}
    return dict_to_send,value

def play_game(prev_state,state,player):
    if prev_state == state and state == default_board:
        return (2,2)
    alpha = np.NINF
    beta = np.inf
    U_dict,Value = max_value(previous_state,state,player,alpha,beta,(2,2))
    action = get_value(U_dict,Value)
    return action

if __name__ == "__main__":
    
    default_board = [[0,0,0,0,0],
                 [0,0,0,0,0],
                 [0,0,0,0,0],
                 [0,0,0,0,0],
                 [0,0,0,0,0]]
    board = [[0,0,0,0,0],
             [0,0,0,0,0],
             [0,0,0,0,0],
             [0,0,0,0,0],
             [0,0,0,0,0]]
    
    previous_board = [[0,0,0,0,0],
                      [0,0,0,0,0],
                      [0,0,0,0,0],
                      [0,0,0,0,0],
                      [0,0,0,0,0]]
    
    player = 0
    dead_players = []
    size = 5
    player1_move = False 
    no_of_moves = 0 
    maximum_moves = size * size - 1
    komi = size/2
    verbose = False 
    prev_state = []
    state = []
    alpha_beta_count=0  
    
    N = 5
    player,prev_state,state = read_input()
    board = state
    previous_state = prev_state
    tplayer = player
    if player == 1:
        player1_move = True
    check_died(player,prev_state,state)
    action = play_game(prev_state,state,player)
    print_output(state,action,previous_state)
    print(action[0],action[1])
     

