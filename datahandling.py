'''
Created on 1 Jun 2017

@author: piers-linux
'''
from peewee import IntegerField, SqliteDatabase, BooleanField, CharField, DateField, DecimalField, Model,\
    RawQuery
from playhouse.shortcuts import dict_to_model
from datetime import datetime
import sqlite3

db = SqliteDatabase('beardstats.db')
db.connect()


class Persistence(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''

    def initialise_db(self):
        Expected.create_table()
        Player.create_table()
        PlayerTank.create_table()
        Tank.create_table()
               
    def delete_expecteds(self):
        query = Expected.delete()
        query.execute()
                       
    def delete_players(self):
        query = Player.delete()
        query.execute()
    
    def delete_tables(self):
        self.delete_tanks()
        self.delete_tank_stats()
        self.delete_players()
    
    def delete_tanks(self):
        query = Tank.delete()
        query.execute()
    
    def delete_tank_stats(self):
        query = PlayerTank.delete().where(PlayerTank.date == datetime.today())
        query.execute()
    
    def delete_player_tank_stats(self, playerid):
        query = PlayerTank.delete().where(PlayerTank.player_id == playerid, PlayerTank.date == datetime.today())
        query.execute()
           
    def save(self, model, objects):
        for obj in objects:
            db_model = dict_to_model(model, obj)
            db_model.save()
                       
    def select_tanks(self):
        for t in Tank.select():
            print (t.name)


class PlottableData(object):
    
    def __init__(self):
        '''
        Constructor
        '''
        db = sqlite3
        
    def select_updated_damage(self):
        j = []
        rq = RawQuery(PlayerTimeDamage, 'SELECT CAST(p.player_id + t.tank_id + julianday(pt.date) AS integer) AS id, p.name AS player_name, t.name AS tank_name, pt.battles, pt.damage_dealt/battles AS avgDamage, pt.date FROM Player AS p JOIN PlayerTank AS pt ON p.player_id = pt.player_id JOIN Tank AS t ON pt.tank_id = t.tank_id JOIN (SELECT player_id, tank_id, count(*) FROM PlayerTank GROUP BY player_id, tank_id, damage_dealt HAVING COUNT(*) <  3) AS d ON d.player_id = p.player_id AND d.tank_id = t.tank_id GROUP BY p.name, t.name, pt.battles, pt.damage_dealt/battles' )
        for t in rq.execute():
            j.append({'player_name':t.player_name, 'tank_name':t.tank_name, 'date':t.date, 'avgDamage':t.avgDamage})
        
        print(j)
        
    
class BaseModelDH(Model):    
    class Meta:
        database = db
        
class Tank(BaseModelDH):
    tank_id = IntegerField(default=0)
    name = CharField(default='')
    short_name = CharField(default='')
    type = CharField(default='')
    tier = IntegerField(default='')
    nation = CharField(default='')
    is_premium = BooleanField(default='')
        
class PlayerTank(BaseModelDH):
    tank_id = IntegerField(default=0)
    player_id = IntegerField(default=0)
    spotted = IntegerField(default=0)
    piercings_received = IntegerField(default=0)
    hits = IntegerField(default=0)
    damage_assisted_track = IntegerField(default=0)
    wins = IntegerField(default=0)
    losses = IntegerField(default=0)
    no_damage_direct_hits_received = IntegerField(default=0)
    capture_points = IntegerField(default=0)
    battles = IntegerField(default=0)
    damage_dealt = IntegerField(default=0)
    explosion_hits = IntegerField(default=0)
    damage_received = IntegerField(default=0)
    piercings = IntegerField(default=0)
    shots = IntegerField(default=0)
    explosion_hits_received = IntegerField(default=0)
    damage_assisted_radio = IntegerField(default=0)
    xp = IntegerField(default=0)
    direct_hits_received = IntegerField(default=0)
    frags = IntegerField(default=0)
    survived_battles = IntegerField(default=0)
    dropped_capture_points = IntegerField(default=0)
    date = DateField(default=datetime.today())

class Expected(BaseModelDH):
    tank_id = IntegerField(default=0)
    expDamage = DecimalField(default=0)
    expDefence = DecimalField(default=0)
    expFrags = DecimalField(default=0)
    expSpots = DecimalField(default=0)
    expWinRate = DecimalField(default=0)

class Player(BaseModelDH):
    player_id = IntegerField(default=0)
    name = CharField(default='')

    
class PlayerTimeDamage(BaseModelDH):
    player_name = CharField
    tank_name = CharField
    battles = IntegerField
    avgDamage = DecimalField
    date = DateField
