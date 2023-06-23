import socket
from _thread import *
from car import Car
import pickle
from pymongo import MongoClient
import pymongo.errors
import sys
import time
import random


# Check database connection
def checkDatabaseConnection():
    global database
    global databases

    try:
        if databaseMain.command('ping')['ok'] == 1 and databaseReplica.command('ping')['ok'] == 1:
            database = databaseMain
            databases = [databaseMain, databaseReplica]
        print("Connected to Mongodb Databases Successfully")
    except:
        try:
            if databaseMain.command('ping')['ok'] == 1:
                print("Successfully connected to MongoDB Main database!")
                database = databaseMain
                databases = [databaseMain]
        except:
            try:
                if databaseReplica.command('ping')['ok'] == 1:
                    print("Failed to connect to MongoDB Main database!")
                    print("Successfully connected to MongoDB Replica database!")
                    database = databaseReplica
                    databases = [databaseReplica]
            except:
                print("Failed to connect to MongoDB both Main and Replica databases!")
                sys.exit()

def get_from_db():
    playersInfo = []
    for x in database.player.find({}, {"_id": 0}):
        playersInfo.append(x)
    info = [tuple(playersInfo[0].values()),tuple(playersInfo[1].values()),tuple(playersInfo[2].values()),tuple(playersInfo[3].values()),tuple(playersInfo[4].values())]
    return info

# Get data of players from database
def get_updated_info(reconnecting_player):
    global prevInfo
    global info

    for x in database.player.find({"id":reconnecting_player}, {"_id": 0}):
        prevInfo = list(x.values())
    # Update the object with the updated values from db
    info[reconnecting_player].playerId = prevInfo[0]
    info[reconnecting_player].imgID = prevInfo[1]
    info[reconnecting_player].x = prevInfo[2]
    info[reconnecting_player].y = prevInfo[3]
    info[reconnecting_player].activePlayers = prevInfo[4]
    info[reconnecting_player].score = prevInfo[5]
    info[reconnecting_player].nickname = prevInfo[6]
    info[reconnecting_player].messages = prevInfo[7]
    info[reconnecting_player].time = prevInfo[8]
    info[reconnecting_player].reconnected = 1

def databaseWrite(data,player):
    checkDatabaseConnection()

    # Took data object recieved from client and store it to both databases Main and Replica >> Hnaaaaaaa el store started
    thisPlayer = data
    field = {"id": player}
    newInfo = {"$set": {"xPos": thisPlayer.x, "yPos": thisPlayer.y, "score": thisPlayer.score, "name": thisPlayer.nickname,"activePlayers": thisPlayer.activePlayers, "messages": thisPlayer.messages}}
    for d in databases:
        d.player.update_many(field, newInfo)

    # To save the messages list in all players at both databases so that when a disconnected player connects again, view the current messages
    for d in databases:
        for document in d.player.find():
            d.player.update_one({"_id": document["_id"]}, {"$set": {"messages": thisPlayer.messages}})

def threaded_client(conn, player, playerIp):
    global activePlayers
    global disconnectedPlayers
    global prevInfo
    global info

    car_object = info[player]
    conn.send(pickle.dumps(car_object))

    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            info[player] = data

            for x in range(len(info)):
                info[x].activePlayers = activePlayers

            sec = round(time.time() - startTime)
            if sec % 5 == 0:
                start_new_thread(databaseWrite, (data, player))

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = info[0], info[2], info[3], info[4]
                elif player == 2:
                    reply = info[0], info[1], info[3], info[4]
                elif player == 3:
                    reply = info[0], info[1], info[2], info[4]
                elif player == 4:
                    reply = info[0], info[1], info[2], info[3]
                else:
                    reply = info[1], info[2], info[3], info[4]

                print("Received: ", data)
                print("Sending : ", reply)

            conn.sendall(pickle.dumps(reply))
        except:
            break

    print("Player ", player+1, " Disconnected")
    info[player].active = 0
    # Take the id of the disconnected player
    disconnectedPlayers[player] = playerIp
    print("Disconnected Players IP Addresses",disconnectedPlayers)
    activePlayers -= 1

    # Save the disconnected player info to database
    checkDatabaseConnection()
    field = {"id": player}
    newInfo = {"$set": {"id":info[player].playerId, "carId":info[player].imgID,"xPos": info[player].x, "yPos": info[player].y, "score": info[player].score, "name": info[player].nickname,"activePlayers": info[player].activePlayers, "messages":info[player].messages, "time":info[player].time}}
    for d in databases:
        d.player.update_many(field, newInfo)
    conn.close()

def startServer():
    global currentPlayer
    global activePlayers
    global info

    server = "192.168.1.14"
    port = 6666

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind((server, port))
    except socket.error as e:
        str(e)

    s.listen(5)
    print("Waiting for a connection, Server Started")

    while True:

        conn, addr = s.accept()
        print("Connected to:", addr)

        # Get the IP address of the conencted player
        playerIp = addr[0].split(':')[0]

        for key, value in disconnectedPlayers.items():
            if playerIp == value:
                currentPlayer = key
                get_updated_info(key)

        start_new_thread(threaded_client, (conn, currentPlayer,playerIp))
        info[currentPlayer].active = 1
        currentPlayer += 1
        for value in disconnectedPlayers.values():
            if playerIp == value:
                currentPlayer -= 1
        allfields = {}
        activePlayers +=1

def init():
    global databaseMain
    global databaseReplica
    global databases
    global infoFromDb
    global currentPlayer
    global activePlayers
    global activePlayers
    global disconnectedPlayers
    global prevInfo
    global startTime
    global info

    connection_string = f"mongodb+srv://m:pZu532OuO1urq4yV@cluster0.lm8lset.mongodb.net/?retryWrites=true&w=majority"
    replica_connection_string = f"mongodb+srv://asuprojects111:db_m0ng0_repl1ca@cluster0.tgwobdr.mongodb.net/"

    client = MongoClient(connection_string, tlsAllowInvalidCertificates = True)
    databaseMain = client.carGame

    clientR = MongoClient(replica_connection_string, tlsAllowInvalidCertificates = True)
    databaseReplica = clientR.carGameReplica

    databases = [databaseMain, databaseReplica]

    # Disconnect Main Database
    # client.close()

    # Disconnect Replica Database
    # clientR.close()

    # Set active players to 0 at the beginning in both dbs main and replica
    forallfields = {}
    activePlayersStart = {"$set": {"activePlayers": 0, "score": 0, "name": None, "messages": []}}
    checkDatabaseConnection()
    for d in databases:
        d.player.update_many(forallfields, activePlayersStart)

    infoFromDb = get_from_db()

    obsL_x = [random.randrange(73, 188), random.randrange(188, 303), random.randrange(73, 188), random.randrange(188, 303), random.randrange(73, 188), random.randrange(188, 303), random.randrange(73, 188)]
    obsR_x = [random.randrange(330, 475), random.randrange(475, 620), random.randrange(330, 475), random.randrange(475, 620), random.randrange(330, 475), random.randrange(475, 620), random.randrange(330, 475)]
    obsL_img = [0, 1, 2, 3, 1, 0, 2]
    obsR_img = [1, 2, 3, 0, 3, 1, 0]

    info = [Car(infoFromDb[0][0], infoFromDb[0][1], 355, 400, obsL_x, obsR_x, obsL_img, obsR_img),
            Car(infoFromDb[1][0], infoFromDb[1][1], 490, 400, obsL_x, obsR_x, obsL_img, obsR_img),
            Car(infoFromDb[2][0], infoFromDb[2][1], 215, 400, obsL_x, obsR_x, obsL_img, obsR_img),
            Car(infoFromDb[3][0], infoFromDb[3][1], 600, 400, obsL_x, obsR_x, obsL_img, obsR_img),
            Car(infoFromDb[4][0], infoFromDb[4][1], 100, 400, obsL_x, obsR_x, obsL_img, obsR_img)]

    # Player Unique ID
    currentPlayer = 0
    activePlayers = 0
    disconnectedPlayers = {}
    prevInfo = []

    startTime = time.time()

    startServer()


if __name__ == "__main__":
    init()

