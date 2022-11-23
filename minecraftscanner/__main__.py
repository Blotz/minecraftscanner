#!/bin/python3

from itertools import count
from minecraftscanner.ip_scanner import scan, generate_ip_range
from minecraftscanner.database import Database

import multiprocessing
from multiprocessing import Pool

from sqlite3 import IntegrityError

def parse_server_json(db, server):
    """    
        ## Server info
        ip: str
        previewsChat: str
        enforcesSecureChat: str
        onlinePlayers: int
        maxPlayers: int
        version: str
        protocol: int
        description: str
        ## Player info
        uuid: str
        name: str
        ## Mods info
        ### Modpack
        projectID: int
        name: str
        version: str
        versionID: int
        isMetadata: bool
        ### Modlist
        modid: str
        version: str
    """
    ## Parse server info
    ip = server["ip"]

    if "previewsChat" in server:
        previewsChat = server["previewsChat"]
    else:
        previewsChat = False
    
    if "enforcesSecureChat" in server:
        enforcesSecureChat = server["enforcesSecureChat"]
    else:
        enforcesSecureChat = False
    
    onlinePlayers = server["players"]["online"]
    maxPlayers = server["players"]["max"]
    version = server["version"]["name"]
    protocol = server["version"]["protocol"]

    if "extra" in server["description"]:
        description = ""
        chunked_description = server["description"]["extra"]
        for chunk in chunked_description:
            description += chunk["text"]
    elif "text" in server["description"]:
        description = server["description"]["text"]
    else:
        description = server["description"]
    
    try:
        db.cursor.execute(
            "INSERT INTO servers (ip, previewsChat, enforcesSecureChat, onlinePlayers, maxPlayers, version, protocol, description) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (ip, previewsChat, enforcesSecureChat, onlinePlayers, maxPlayers, version, protocol, description)
        )
        db.connection.commit()
    except IntegrityError:
        print(f"ERROR - {ip} {previewsChat} {enforcesSecureChat} {onlinePlayers} {maxPlayers} {version} {protocol} {description}")
        return


    ## Parse player info
    if "sample" in server["players"]:
        for player in server["players"]["sample"]:
            uuid = player["id"]
            name = player["name"]
            if name!="" and uuid!="00000000-0000-0000-0000-000000000000":
                try:
                    db.cursor.execute(
                        "INSERT OR IGNORE INTO players (uuid, name) VALUES (?, ?)",
                        (uuid, name)
                    )
                    db.connection.commit()
                    db.cursor.execute(
                        "INSERT INTO server_players (server, player) VALUES (?, ?)",
                        (ip, uuid)
                    )
                    db.connection.commit()
                except IntegrityError:
                    print(f"ERROR - {ip} {uuid} {name}")
                    pass


    ## Parse modpack info
    if "modpackData" in server:
        projectID = server["modpackData"]["projectID"]
        name = server["modpackData"]["name"]
        version = server["modpackData"]["version"]
        versionID = server["modpackData"]["versionID"]
        isMetadata = server["modpackData"]["isMetadata"]
        try:
            db.cursor.execute(
                "INSERT OR IGNORE INTO modpacks (projectID, name, version, versionID, isMetadata) VALUES (?, ?, ?, ?, ?)",
                (projectID, name, version, versionID, isMetadata)
            )
            db.connection.commit()
            db.cursor.execute(
                "INSERT INTO server_modpacks (server, modpack) VALUES (?, ?)",
                (ip, projectID)
            )
        except IntegrityError:
            print(f"ERROR - {ip} {projectID} {name} {version} {versionID} {isMetadata}")
            pass

    # Parse modlist info
    if "modinfo" in server:
        for mod in server["modinfo"]["modList"]:
            modid = mod["modid"]
            version = mod["version"]
            try:
                db.cursor.execute(
                    "INSERT OR IGNORE INTO mods (modid, version) VALUES (?, ?)",
                    (modid, version)
                )
                db.connection.commit()
                db.cursor.execute(
                    "INSERT INTO server_mods (server, mod, version) VALUES (?, ?, ?)",
                    (ip, modid, version)
                )
            except IntegrityError:
                print(f"ERROR - {ip} {modid} {version}")
                pass

def main():
    print("Starting up!")
    ip_range = generate_ip_range()

    total = len(ip_range)
    counter = 0

    print(f"Scanning {total} IPs")

    with Pool(processes=multiprocessing.cpu_count()) as pool:
        results = pool.imap_unordered(scan, ip_range)
        
        try:
            for mc_status  in results:
                # print("############################")
                print(mc_status)
                counter += 1
                # Print percentage done
                print(f"{counter}/{total} - {round(counter/total*100, 2)}%")

                with Database("./mc_server.db") as db:
                    for server in mc_status:
                        parse_server_json(db, server)
                        db.connection.commit()
        except IndexError:
            pass
                

            
            
        

if __name__ == '__main__':
    main()
