'''
Created on 31 May 2017

@author: piers-linux
'''

import beards

if __name__ == '__main__':
    pass

dr = beards.DataRefresher('ps4')
#dr.refresh_tank_info()
dr.save_player_info()
#dr.add_player_tanks('Damon_Grille')
dr.add_players_tanks()