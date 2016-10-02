import inspect
import pprint
import configparser
import argparse
import soundcloud
import json
import math
import pymysql.cursors

def load_following(user_id):
    paginate = False
    following = client.get('/users/'+str(user_id)+'/followings', limit=page_size, linked_partitioning=1)
    for user in following.collection:
        with connection.cursor() as cursor:
            sql = "INSERT INTO "+"doujin_following"+" VALUES({},{},UTC_TIMESTAMP())".format(user.id,user_id)
            cursor.execute(sql)
        connection.commit()
    if(following.next_href):
        paginate = True
    while(paginate):
        following = client.get(following.next_href)
        for user in following.collection:
            with connection.cursor() as cursor:
                sql = "INSERT INTO "+"doujin_following"+" VALUES({},{},UTC_TIMESTAMP())".format(user.id,user_id)
                cursor.execute(sql)
            connection.commit()
        if(following.next_href is not None):
            paginate = True
        else:
            paginate = False

def user_mutuals(user_id):
    with connection.cursor() as cursor:
        sql = "SELECT DISTINCT t1.followed_by_id FROM doujin_following t1 INNER JOIN doujin_following t2 WHERE t1.followed_id = t2.followed_by_id AND t1.followed_by_id = t2.followed_id AND t1.followed_id = {}".format(user_id)
        cursor.execute(sql)
        mutuals_results = cursor.fetchall()
        mutuals = []
        for mutual in mutuals_results:
            mutuals.append(mutual["followed_by_id"])
        return mutuals


client = soundcloud.Client(client_id='f9d25e71eec3e001319c19fb9f19b77d')

sqlhost= "localhost"
sqluser= "fogflock"
sqlpassword= "yourwaifuistrash"
sqldatabase= "fogflock"
sceneinput = []
connection = pymysql.connect(host='localhost',user=sqluser,password=sqlpassword,db=sqldatabase,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
scene_ids = []
loops = 3
page_size = 200
userslist = ""
relevance_threshold = 0.8
myuser = ""
#Initial Input
userinputs = ["pearlgreymusic"]

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--users", type=str, dest="userslist", help="Soundcloud Usernames")
parser.add_argument("-m", "--me", type=str, dest="me", help="Your soundcloud")
parser.add_argument("-l", "--loops", type=int, dest="loops", help="loops")
parser.add_argument("-t", "--threshold", type=float, dest="relevance_threshold", help="threshold")
args = parser.parse_args()

if(args.me):
    myuser = args.me
if(args.loops):
    loops = args.loops
if(args.relevance_threshold):
    relevance_threshold = args.relevance_threshold
if(args.userslist):
    userinputs = args.userslist.split()

print("Users: {}\nLoops: {}\nThreshold:{}".format(userinputs,loops,relevance_threshold))
client = soundcloud.Client(client_id='79b15454f84bc616792fc99d6b9104e8')
#resetting
with connection.cursor() as cursor:
    sql = "DELETE FROM doujin_scene"
    cursor.execute(sql)
    sql = "DELETE FROM doujin_following"
    cursor.execute(sql)
connection.commit()
#loading initial user inputs
for username in userinputs:
    user = client.get('/users/'+username+'/')
    user_id = user.id
    print(username + ": "+ str(user_id))

    if(True):
        with connection.cursor() as cursor:
            sql = "INSERT INTO "+"doujin_scene"+" VALUES({},'{}',UTC_TIMESTAMP(),UTC_TIMESTAMP(),0,0,NULL,'{}','{}',{},0,'{}')".format(user_id,username,user.avatar_url,user.permalink_url,user.followers_count,user.username.replace("'","''"))
            cursor.execute(sql)
        connection.commit()

for i in range(loops):
    with connection.cursor() as cursor:
        sql = "SELECT sc_id,sc_username FROM doujin_scene WHERE scanned=FALSE"
        cursor.execute(sql)
        scene_ids = cursor.fetchall()
    for sc in scene_ids:
        sceneinput.append(sc['sc_id'])
    doirepeat = True
    #Part where it loads in the followers
    while(doirepeat):
        doirepeat = False
        with connection.cursor() as cursor:
            sql = "SELECT sc_id,sc_username FROM doujin_scene WHERE scanned=FALSE"
            cursor.execute(sql)
            scene_ids = cursor.fetchall()
        for sc in scene_ids:
            print(sc['sc_id'])
            try:
                load_following(sc['sc_id'])
                with connection.cursor() as cursor:
                    sql = "UPDATE doujin_scene SET scanned=TRUE, time_updated=UTC_TIMESTAMP() WHERE sc_id={}".format(sc['sc_id'])
                    cursor.execute(sql)
                connection.commit()
            except:
                print("error")
                #delete the data that was inputted in nyaa
                with connection.cursor() as cursor:
                    sql = "DELETE FROM doujin_following WHERE followed_by_id = {}".format(sc['sc_id'])
                    cursor.execute(sql)
                connection.commit()
                doirepeat = True

    with connection.cursor() as cursor:
        sql = "SELECT sc_id,sc_username FROM doujin_scene"
        cursor.execute(sql)
        scene_ids = cursor.fetchall()
    for sc in scene_ids:
        sceneinput.append(sc['sc_id'])

    doirepeat = True
    while(doirepeat):
        doirepeat = False
        for sc in scene_ids:
            print(sc['sc_id'])
            my_mutuals = user_mutuals(sc['sc_id'])
            rel_index = (len(list(set(my_mutuals) & set(sceneinput)))+1)/len(sceneinput)
            print("relevancy index of "+sc['sc_username']+" = "+str(rel_index))
            with connection.cursor() as cursor:
                sql = "UPDATE doujin_scene SET scanned=TRUE, relevancy={}, time_updated=UTC_TIMESTAMP(), mutuals ='{}' WHERE sc_id={}".format(rel_index,str(set(my_mutuals) & set(sceneinput)),sc['sc_id'])
                cursor.execute(sql)
            connection.commit()

    relevancy_total = 0;
    with connection.cursor() as cursor:
        sql = "SELECT SUM(relevancy) FROM doujin_scene"
        cursor.execute(sql)
        relevancy_total_results = cursor.fetchall()
        print(relevancy_total_results)
        for result in relevancy_total_results:
            relevancy_total = result['SUM(relevancy)']

    with connection.cursor() as cursor:
        sql = "SELECT followed_id, SUM(relevancy) FROM fogflock.relevancy GROUP BY followed_id ORDER BY SUM(relevancy) DESC LIMIT 33"
        cursor.execute(sql)
        top_results = cursor.fetchall()

    newnames = []

    print(relevancy_total)
    for result in top_results:
        following = client.get('/users/'+str(result['followed_id']))
        relevancy_percent = result['SUM(relevancy)']/relevancy_total
        if(relevancy_percent > (relevance_threshold**(i+1)+relevance_threshold)/(2)):
            print(following.username+" "+str(result['followed_id'])+": "+str(relevancy_percent))
            newnames.append(following.permalink)
        else:
            break
    print("rescan with the accounts: "+str(newnames))

    if(i < loops-1):
        for username in newnames:
            user = client.get('/users/'+username+'/')
            user_id = user.id
            print(username + ": "+ str(user_id))

            if(True):
                with connection.cursor() as cursor:
                    sql = "INSERT IGNORE INTO "+"doujin_scene"+" VALUES({},'{}',UTC_TIMESTAMP(),UTC_TIMESTAMP(),0,0,NULL,'{}','{}',{},{},'{}')".format(user_id,username,user.avatar_url,user.permalink_url,user.followers_count,i+1,user.username.replace("'","''"))
                    cursor.execute(sql)
                connection.commit()
with connection.cursor() as cursor:
    sql = "SELECT sc_id, sc_username, relevancy, avatar_url, permalink_url, followers_count, level, mutuals, sc_display_name FROM doujin_scene WHERE level = 0"
    cursor.execute(sql)
    outputstuff1 = cursor.fetchall()
    sql = "SELECT sc_id, sc_username, relevancy, avatar_url, permalink_url, followers_count, level, mutuals, sc_display_name FROM doujin_scene WHERE level > 0 ORDER BY relevancy DESC LIMIT 100"
    cursor.execute(sql)
    outputstuff2 = cursor.fetchall()
    outputstufftotal = outputstuff1 + outputstuff2
    with open('data.json', 'w') as outfile:
        json.dump(outputstufftotal, outfile)
connection.commit()

connection.close()
