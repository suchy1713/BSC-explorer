import mysql.connector
import pandas as pd
from pypika import Table, Order, functions
from pypika import MySQLQuery as Query
user = 'root'
password = '24082408'
host = 'localhost'
database = 'bsc-explorer'

class db():
    def __init__(self):
        self.tables = {
            'clubs': Table('clubs'),
            'events': Table('events'),
            'games': Table('games'),
            'teams': Table('teams'),
            'opposition': Table('teams'),
            'positions': Table('positions'),
            'players': Table('players'),
            'formations': Table('formations'),
            'opposition_formations': Table('formations').as_('opposition_formation')
        }

    def get_connection(self):
        return mysql.connector.connect(
            user='root',
            password='24082408',
            host='localhost',
            database='bsc-explorer'
        )
    
    def get_seasons(self):
        query = Query.from_(self.tables['clubs']).select(self.tables['clubs'].season).distinct().orderby('season', order=Order.desc)
        
        cnx = self.get_connection()
        seasons = pd.read_sql(query.get_sql(), cnx)
        cnx.close()

        return seasons

    def get_leagues_by_season(self, season):
        query = Query.from_(self.tables['games']).select(self.tables['games'].competition).where(self.tables['games'].season == season).distinct().orderby('competition')
        
        cnx = self.get_connection()
        leagues = pd.read_sql(query.get_sql(), cnx)
        cnx.close()

        return leagues

    def get_clubs_by_league_and_season(self, league, season):
        query = Query.from_(self.tables['clubs']).select(
            self.tables['clubs'].id,
            self.tables['clubs'].name,
            self.tables['clubs'].season,
            self.tables['clubs'].color,
            self.tables['clubs'].competition
        ).where(
            self.tables['clubs'].competition == league
        ).where(
            self.tables['clubs'].season == season
        )
        
        cnx = self.get_connection()
        clubs = pd.read_sql(query.get_sql(), cnx)
        cnx.close()

        return clubs

    def get_coaches_by_clubid(self, club_id):
        query = Query.from_(self.tables['teams']).select(
            self.tables['teams'].coach
        ).where(
            self.tables['teams'].clubId == club_id
        ).distinct()
        
        cnx = self.get_connection()
        coaches = pd.read_sql(query.get_sql(), cnx)
        cnx.close()

        return coaches

    def get_color_by_clubid(self, club_id):
        query = Query.from_(self.tables['clubs']).select(
            self.tables['clubs'].color
        ).where(
            self.tables['clubs'].Id == club_id
        )
        
        cnx = self.get_connection()
        colors = pd.read_sql(query.get_sql(), cnx)
        cnx.close()

        return colors['Color'].values[0]

    def get_players_by_clubid(self, club_id):
        query = Query.from_(self.tables['teams']).join(
            self.tables['positions']
        ).on(
            self.tables['teams'].id == self.tables['positions'].teamId
        ).join(
            self.tables['players']
        ).on(
            self.tables['positions'].playerId == self.tables['players'].id
        ).select(
            self.tables['players'].id,
            self.tables['players'].name
        ).where(
            self.tables['teams'].clubId == club_id
        ).distinct().orderby(self.tables['players'].name)
        
        cnx = self.get_connection()
        players = pd.read_sql(query.get_sql(), cnx)
        cnx.close()

        return players

    def get_possession_by_clubid(self, club_id):
        query = Query.from_(self.tables['teams']).join(
            self.tables['formations']
        ).on(
            self.tables['formations'].id == self.tables['teams'].formationId
        ).select(
            self.tables['formations'].possession
        ).where(
            self.tables['teams'].clubId == club_id
        ).distinct().orderby(self.tables['formations'].possession)

        cnx = self.get_connection()
        possession_vals = pd.read_sql(query.get_sql(), cnx)
        cnx.close()

        return possession_vals

    def get_opposition_teams_by_clubid(self, club_id):
        query = Query.from_(self.tables['teams']).join(
            self.tables['opposition']
        ).on(
            self.tables['teams'].oppositionId == self.tables['opposition'].id
        ).join(
            self.tables['clubs']
        ).on(
            self.tables['clubs'].id == self.tables['opposition'].clubId
        ).select(
            self.tables['clubs'].id,
            self.tables['clubs'].name
        ).where(
            self.tables['teams'].clubId == club_id
        ).distinct().orderby(self.tables['clubs'].name)

        cnx = self.get_connection()
        teams = pd.read_sql(query.get_sql(), cnx)
        cnx.close()

        return teams

    def get_opposition_formations_by_clubid(self, club_id):
        query = Query.from_(self.tables['teams']).join(
            self.tables['opposition']
        ).on(
            self.tables['teams'].oppositionId == self.tables['opposition'].id
        ).join(
            self.tables['formations']
        ).on(
            self.tables['formations'].id == self.tables['opposition'].formationId
        ).select(
            self.tables['formations'].vector,
            self.tables['formations'].label
        ).where(
            self.tables['teams'].clubId == club_id
        ).distinct().orderby(self.tables['formations'].label)

        cnx = self.get_connection()
        formations = pd.read_sql(query.get_sql(), cnx)
        cnx.close()

        return formations

    def get_dates_by_clubid(self, club_id):
        query = Query.from_(self.tables['teams']).join(
            self.tables['games']
        ).on(
            self.tables['teams'].gameId == self.tables['games'].id
        ).select(
            self.tables['games'].gameDate
        ).where(
            self.tables['teams'].clubId == club_id
        ).orderby(self.tables['games'].gameDate)

        cnx = self.get_connection()
        dates = pd.read_sql(query.get_sql(), cnx, parse_dates=['gameDate'])
        cnx.close()

        return dates

    def get_dates_to_exclude_by_players(self, players, club):
        query = Query.from_(self.tables['players']).join(
            self.tables['positions']
        ).on(
            self.tables['players'].id == self.tables['positions'].playerId
        ).join(
            self.tables['teams']
        ).on(
            self.tables['positions'].teamId == self.tables['teams'].id
        ).join(
            self.tables['games']
        ).on(
            self.tables['teams'].gameId == self.tables['games'].id
        ).join(
            self.tables['clubs']
        ).on(
            self.tables['teams'].clubId == self.tables['clubs'].id
        ).select(
            self.tables['games'].gameDate
        ).where(
            self.tables['players'].id.isin(players)
        ).where(
            self.tables['teams'].clubId == club
        ).distinct()

        cnx = self.get_connection()
        dates = pd.read_sql(query.get_sql(), cnx, parse_dates=['gameDate'])
        cnx.close()

        return dates['gameDate'].values

    def get_dates_to_include_by_players(self, players, club):
        query = Query.from_(self.tables['players']).join(
            self.tables['positions']
        ).on(
            self.tables['players'].id == self.tables['positions'].playerId
        ).join(
            self.tables['teams']
        ).on(
            self.tables['positions'].teamId == self.tables['teams'].id
        ).join(
            self.tables['games']
        ).on(
            self.tables['teams'].gameId == self.tables['games'].id
        ).join(
            self.tables['clubs']
        ).on(
            self.tables['teams'].clubId == self.tables['clubs'].id
        ).groupby(
            self.tables['games'].gameDate
        ).select(
            self.tables['games'].gameDate,
            functions.Count(self.tables['games'].gameDate).as_('dates_count')
        ).where(
            self.tables['players'].id.isin(players)
        ).where(
            self.tables['teams'].clubId == club
        )

        cnx = self.get_connection()
        dates = pd.read_sql(query.get_sql(), cnx, parse_dates=['gameDate'])
        cnx.close()

        return dates.loc[dates['dates_count'] == len(players)]['gameDate'].values

    def get_formations(self, club, coaches, players_to_include, players_to_exclude, possession_vals, opp_formation, start_date, end_date):
        query = Query.from_(self.tables['games']).join(
            self.tables['teams']
        ).on(
            self.tables['teams'].gameId == self.tables['games'].id
        ).join(
            self.tables['formations']
        ).on(
            self.tables['teams'].formationId == self.tables['formations'].id
        ).join(
            self.tables['opposition']
        ).on(
            self.tables['opposition'].id == self.tables['teams'].oppositionId
        ).join(
            self.tables['clubs']
        ).on(
            self.tables['opposition'].clubId == self.tables['clubs'].id
        ).join(
            self.tables['opposition_formations']
        ).on(
            self.tables['opposition'].formationId == self.tables['opposition_formations'].id
        ).select(
            self.tables['formations'].id,
            self.tables['formations'].vector,
            self.tables['formations'].label,
            self.tables['formations'].minutes,
            self.tables['formations'].possession
        ).where(
            self.tables['teams'].clubId == club
        ).where(
            self.tables['teams'].coach.isin(coaches)
        ).where(
            self.tables['formations'].possession >= possession_vals[0]/100
        ).where(
            self.tables['formations'].possession <= possession_vals[1]/100
        ).where(
            self.tables['opposition_formations'].vector.isin(opp_formation)
        ).where(
            self.tables['games'].gameDate >= start_date
        ).where(
            self.tables['games'].gameDate <= end_date
        )

        if len(players_to_include) > 0:
            dates_to_include = self.get_dates_to_include_by_players(players_to_include, club)
            query = query.where(
                self.tables['games'].gameDate.isin(list(dates_to_include.astype(str)))
            )
        if len(players_to_exclude) > 0:
            dates_to_exclude = self.get_dates_to_exclude_by_players(players_to_exclude, club)
            query = query.where(
                ~self.tables['games'].gameDate.isin(list(dates_to_exclude.astype(str)))
            )

        cnx = self.get_connection()
        formations = pd.read_sql(query.get_sql(), cnx, parse_dates=['gameDate'])
        cnx.close()

        return formations

    def get_events_by_formations(self, formation_ids):
        query = Query.from_(self.tables['events']).select(
            self.tables['events'].star
        ).where(
            self.tables['events'].formationId.isin(list(formation_ids))
        )

        cnx = self.get_connection()
        events = pd.read_sql(query.get_sql(), cnx)
        cnx.close()

        return events

    def get_players_by_formations(self, formation_ids):
        query = Query.from_(self.tables['positions']).select(
            self.tables['players'].name,
            self.tables['positions'].position,
            self.tables['formations'].minutes,
        ).join(
            self.tables['players']
        ).on(
            self.tables['positions'].playerId == self.tables['players'].id
        ).join(
            self.tables['formations']
        ).on(
            self.tables['positions'].formationId == self.tables['formations'].id
        ).where(
            self.tables['positions'].formationId.isin(list(formation_ids))
        )

        cnx = self.get_connection()
        events = pd.read_sql(query.get_sql(), cnx)
        cnx.close()

        return events
