CREATE TABLE IF NOT EXISTS Events (
    ID          int NOT NULL AUTO_INCREMENT,
    PlayerId    int NOT NULL,
    ReceiverId  int,
    PlayerPosition    varchar(255),
    ReceiverPosition  varchar(255),
    FormationId int NOT NULL,
    TimeMinutes float,
    StartX      float,
    StartY      float,
    EndX        float,
    EndY        float,
    EventType   varchar(255),
    OutcomeType varchar(255),
    Xt          float,
    ScoringProb float,
    BlockedX    float,
    BlockedY    float,
    GoalMouthY  float,
    GoalMouthZ  float,
    CardType    varchar(255),
    IsTouch     boolean,
    IsGoal      boolean,
    IsShot      boolean,
    IsDefAction boolean,
    PRIMARY KEY (ID)
);

CREATE TABLE IF NOT EXISTS Players (
    ID          int NOT NULL,
    Name        varchar(255),
    PRIMARY KEY (ID)
);

CREATE TABLE IF NOT EXISTS Clubs (
    ID          varchar(255) NOT NULL,
    Name        varchar(255),
    Short       varchar(255),
    Season      varchar(255),
    Competition varchar(255),
    Color       varchar(255),
    PRIMARY KEY (ID)
);

CREATE TABLE IF NOT EXISTS Formations (
    ID          int NOT NULL AUTO_INCREMENT,
    Vector      varchar(255),
    Label       varchar(255),
    Minutes     float,
    Possession  float,
    PRIMARY KEY (ID)
);

CREATE TABLE IF NOT EXISTS Games (
    ID          varchar(255) NOT NULL,
    GameDate    date,
    Season      varchar(255),
    Competition varchar(255),
    HomeTeamId  int NOT NULL,
    AwayTeamId  int NOT NULL,
    PRIMARY KEY (ID)
);

CREATE TABLE IF NOT EXISTS Teams (
    ID          int NOT NULL AUTO_INCREMENT,
    ClubId      varchar(255) NOT NULL,
    FormationId int NOT NULL,
    GameId      varchar(255) NOT NULL,
    OppositionId int NOT NULL,
    Coach       varchar(255),
    PRIMARY KEY (ID)
);

CREATE TABLE IF NOT EXISTS Positions (
    ID          int NOT NULL AUTO_INCREMENT,
    PlayerId    int NOT NULL,
    FormationId int NOT NULL,
    TeamId      int NOT NULL,
    Position    varchar(255),
    PRIMARY KEY (ID)
);