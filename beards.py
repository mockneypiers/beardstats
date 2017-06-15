'''
Created on 1 Jun 2017

@author: piers-linux
'''
import wargaming
import datahandling

class DataRefresher(object):
    '''
    classdocs
    '''
    PLAYER_LIST = {'mockney_piers',
                   'srogerson',
                   'nimrais',
                   'gunner_rich',
                   'ThatOneBounced',
                   'Jan_de_buldozer',
                   'GoldenCodpiece',
                   'LukeNukem-79',
                   'radinko245',
                   'Damon_Grille'}
    
    INITIALISE = False


    def __init__(self, server):
        '''
        Constructor
        '''
        self._players = {}
        self.wgapi = wargaming.API(server)
        self.db = datahandling.Persistence()
        if self.INITIALISE: self.db.initialise_db()
    
    def refresh_tank_info(self):
        tanks = self.wgapi.request_tanks()
        self.db.delete_tanks()      
        self.db.save(datahandling.Tank, tanks)
    
    def get_player_info(self,playername):
        player = self.wgapi.search_player(playername)
        print(player)
        
    def add_player_tanks(self, playername):
        playertanks = self.wgapi.request_tank_stats(playername, None)
        self.db.delete_player_tank_stats(self.wgapi._playerId)#TODO DELETE!!!!
        print(playertanks)
        self.db.save(datahandling.PlayerTank, playertanks)
        
    def add_players_tanks(self):
        self.db.delete_tank_stats() #TODO DELETE!!!!!!!
        for playername in self.PLAYER_LIST:
            playertanks = self.wgapi.request_tank_stats(playername, None)
            if playertanks is not None:
                print(playername)
                self.db.save(datahandling.PlayerTank, playertanks)

    def save_player_info(self):
        self.db.delete_players()
        players = []
        for playername in self.PLAYER_LIST:
            players.append(self.wgapi.get_player(playername))
            
        self.db.save(datahandling.Player, players)
