'''
Created on 30 May 2017

@author: piers-linux
'''
import requests


class API(object):
    '''
    classdocs
    '''
    APPLICATION_ID = 'da2659a8b76de46d60240c8d5de1d8cb'

    def __init__(self, wgserver):
        '''
        Constructor
        '''
        self._wgserver = wgserver
        self._API = 'https://api-{}-console.worldoftanks.com/wotx/'.format(wgserver)
        self._playerUrl = self._API + 'account/list/'
        self._tankUrl = self._API + 'encyclopedia/vehicles/'
        self._tankStatsUrl = self._API + 'tanks/stats/'
        self._playerId = 0
        self._playername = ''
        

    
    def request_tanks(self):
        tankopedia = []
        Vehicles = requests.get(self._tankUrl,
                                params={
                                    'application_id': self.APPLICATION_ID,
                                    'fields': None,
                                    'language': None
                                },
                                timeout=10).json()
                      
        for key, value in Vehicles['data'].items():
            TankDict = {'tank_id': int(key),
                        'name': value['name'],
                        'short_name': value['short_name'],
                        'type': value['type'],
                        'tier': value['tier'],
                        'nation': value['nation'],
                        'is_premium': value['is_premium']
                        }
            tankopedia.append(TankDict)
         
        return tankopedia
     
    def request_tank_stats(self, playername, tankname):
        playerTankStats = []
        self.search_player(playername)
        TankStats = requests.get(self._tankStatsUrl,
                                params={
                                    'application_id': self.APPLICATION_ID,
                                    'account_id': self._playerId,
                                    'tank_id': tankname
                                },
                                timeout=10).json()

        data = TankStats['data'][str(self._playerId)]
        if data == None:
            return(None)  
        
        for stat in data:
            TankStatsDict = {'tank_id': stat['tank_id'],
                             'player_id': self._playerId,
                             'spotted': stat['all']['spotted'],
                             'piercings_received': stat['all']['piercings_received'],
                             'hits': stat['all']['hits'],
                             'damage_assisted_track': stat['all']['damage_assisted_track'],
                             'wins': stat['all']['wins'],
                             'losses': stat['all']['losses'],
                             'no_damage_direct_hits_received': stat['all']['no_damage_direct_hits_received'],
                             'capture_points': stat['all']['capture_points'],
                             'battles': stat['all']['battles'],
                             'damage_dealt': stat['all']['damage_dealt'],
                             'explosion_hits': stat['all']['explosion_hits'],
                             'damage_received': stat['all']['damage_received'],
                             'piercings': stat['all']['piercings'],
                             'shots': stat['all']['shots'],
                             'explosion_hits_received': stat['all']['explosion_hits_received'],
                             'damage_assisted_radio': stat['all']['damage_assisted_radio'],
                             'xp': stat['all']['xp'],
                             'direct_hits_received': stat['all']['direct_hits_received'],
                             'frags': stat['all']['frags'],
                             'survived_battles': stat['all']['survived_battles'],
                             'dropped_capture_points': stat['all']['dropped_capture_points']
                             }
            playerTankStats.append(TankStatsDict)
         
        return playerTankStats
       
    def search_player (self, playername):
        self._playername = playername
        player = requests.get(self._playerUrl,
                              params={'search': self._playername,
                                      'application_id': self.APPLICATION_ID
                                      },
                              timeout=10)
        
        self._playerId = (player.json()['data'][0]['account_id'])
        return player.json()
    
    def get_player(self, playername):
        player = self.search_player(playername)['data'][0]
        print(player)
        return {'player_id': player['account_id'],
                'name': player['nickname']}

        