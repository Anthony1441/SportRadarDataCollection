import os
import argparse
import http.client

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("apiKey", help = "Your SportRadar API key")
    parser.add_argument("gameIDsFile", help = "CSV of game IDs with columns (game_name, game_id)")
    parser.add_argument("-saveDir",  default = "pbp_data_csv", help = "Output directory")
    args = parser.parse_args()

    if os.path.exists(args.saveDir):
        print(f"{args.saveDir} already exists, choose another save location.")
        exit()

    if not os.path.exists(args.gameIDsFile):
        print(f"{args.gameIds} does not exist.")
        exit()

    json_dir = os.path.join(args.saveDir, "json_files")
    os.makedirs(json_dir)
    
    with open(args.gameIDsFile, 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines, 1):
            info = line.rstrip().split(',')
            
            if len(info) != 2:
                print(f"{args.gameIds} is not in the correct format.")
                exit()

            game_name, game_id = info[0], info[1]
            print(f"[{i} of {len(lines)}] Downloading {game_name}...")
            try:
                conn = http.client.HTTPSConnection("api.sportradar.us")
                conn.request("GET", f"/nfl/official/trial/v7/en/games/{game_id}/pbp.json?api_key={args.apiKey}")
                data = conn.getresponse().read()
                with open(os.path.join(json_dir, f"{game_name}_{game_id}.json"), 'w') as out:
                    out.write(data.decode("utf-8"))
            except:
                print(f"Error downloading {game_name} ({game_id}), continuing...")
    
    json_files = os.listdir(json_dir)
    for i, file_name in enumerate(json_files, 1):
        inp_path = os.path.join(json_dir, file_name)
        out_path  = os.path.join(args.saveDir, f"{os.path.splitext(file_name)[0]}.csv")
        print(f"[{i} of {len(json_files)}] Converting {file_name} to CSV format...")
        os.system(f"python pbp_table.py {inp_path} {out_path}")