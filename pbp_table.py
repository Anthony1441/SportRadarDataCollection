import sys
import json

# Check command line arguments
if len(sys.argv) != 3:
    print("USAGE: python pbp_table.py INPUT_FILE OUTPUT_FILE")
    exit()

############################# CONSTANTS ############################
MAX_STATS_LEN       = 15
NUM_STATS_FIELDS    = 36
MAX_DETAILS_LEN     = 15
MAX_DETAILS_PLAYERS = 10
NUM_PLAYER_FIELDS   = 6
NUM_TEAM_FIELDS     = 5
NUM_DETAILS_FIELDS  = 57 + NUM_PLAYER_FIELDS * MAX_DETAILS_PLAYERS
NULL                = "NULL"
SAVE_FIELD_NAMES    = False
####################################################################

# Setup the header
header = "type,id,sequence,clock,scoring_play,home_points,away_points,play_type,wall_clock,description,fake_punt,fake_field_goal,screen_pass," + \
         "men_in_box,play_direction,running_lane,run_pass_option,players_rushed,pocket_location,pass_route" + \
         "blitz,left_tightends,right_tightends,hash_mark,gb_at_snap,huddle,play_action,created_at,updated_at," + \
         "start_situation_clock,start_situation_down,start_situation_yfd,start_situation_possession_id,start_situation_possession_name," + \
         "start_situation_possession_market,start_situation_possession_alias,start_situation_possession_sr_id,start_situation_location_id," + \
         "start_situation_location_name,start_situation_location_market,start_situation_location_alias,start_situation_location_sr_id,start_situation_location_yardline," + \
         "end_situation_clock,end_situation_down,end_situation_yfd,end_situation_possession_id,end_situation_possession_name,end_situation_possession_market," + \
         "end_situation_possession_alias,end_situation_possession_sr_id,end_situation_location_id,end_situation_location_name,end_situation_location_alias," + \
         "end_situation_location_sr_id,end_situation_location_yardline,end_situation_location_market,"

for i in range(1, MAX_STATS_LEN + 1):
    header += f"stats_type_{i},stats_attempt_{i},stats_yards_{i},stats_net_yards_{i},stats_inside_20_{i},stats_hang_time_{i},stats_player_id_{i},stats_touchback_{i},stats_onside_attempt_{i},status_onside_success_{i}," + \
              f"stats_squib_kick_{i},stats_firstdown_{i},stats_goaltogo_{i},stats_broken_tackles_{i},stats_kneel_down_{i},stats_scramble_{i},stats_yards_after_contact_{i}," + \
              f"stats_on_target_throw_{i},stats_batted_pass_{i},stats_hurry_{i},stats_knockdown_{i},stats_penalty_{i},stats_complete_{i},stats_att_yards_{i},stats_pocket_time_{i},stats_made_{i}," + \
              f"stats_player_name_{i},stats_player_jersey_{i},stats_player_position_{i},stats_player_st_id_{i},stats_player_role_{i},stats_team_id_{i},stats_team_name_{i},stats_team_market_{i},stats_team_alias_{i},stats_team_sr_id_{i},"

for i in range(1, MAX_DETAILS_LEN + 1):
    header += f"details_category_{i},details_description_{i},details_sequence_{i},details_direction_{i},details_yards_{i},details_result_{i}," + \
              f"details_start_location_alias_{i},details_start_location_yardline_{i},details_end_location_alias_{i},details_end_location_yardline_{i}," + \
              f"detail_ast_tackle_{i},detail_ast_sack_{i},detail_blitz_{i},detail_block_{i},detail_def_target_{i},detail_fumble_{i},detail_forced_fumble_{i}," + \
              f"detail_interception_{i},detail_missed_tackles_{i},detail_nullified_{i},detail_pass_defended_{i},detail_qb_hit_{i},detail_sack_{i},detail_sack_yards_{i}," + \
              f"detail_tackle_{i},detail_attempt_{i},detail_blocked_{i},detail_missed_{i},detail_returned_{i},detail_aborted_{i},detail_endzone_{i},detail_inside_20_{i}," + \
              f"detail_made_{i},detail_hurry_{i},detail_touchdown_{i},detail_faircatch_{i},detail_incompletion_type_{i},detail_target_{i},detail_knockdown_{i}," + \
              f"detail_dropped_{i},detail_reception_{i},detail_catachable_{i},detail_return_{i},detail_tlost_{i},detail_tlost_yards_{i}," + \
              f"detail_def_comp_{i},detail_broken_tackles_{i},detail_forced_{i},detail_down_{i},detail_batted_down_{i}," + \
              f"detail_yards_after_catch_{i},detail_lateral_{i},detail_safety_{i},detail_kickoff_{i},detail_recovery_{i},detail_primary_{i},detail_bounds_{i},"
    for j in range(1, MAX_DETAILS_PLAYERS + 1):
        header += f"details_{i}_player_{j}_id,details_{i}_player_{j}_name,details_{i}_player_{j}_jersey,details_{i}_player_{j}_positions,details_{i}_player_{j}_sr_id,details_{i}_player_{j}_role,"     

NUM_HEADER_FIELDS = len(header.split(','))

if SAVE_FIELD_NAMES:
    with open("FieldNames.txt", 'w') as f:
        for field in header.split(','):
            f.write(f"{field}\n")

max_num_players = 0
max_num_stats   = 0
max_num_details = 0
events_ignored = []

with open(sys.argv[1], 'r') as input_file, open(sys.argv[2], 'w') as out:
    inp = json.load(input_file)
    out.write(header + '\n')

    num_plays_processed = 0

    for period in inp["periods"]:
        for section in period["pbp"]:
            if not "events" in section:
                continue
            
            for event in section["events"]:
                if event["type"] == "play":

                    line = [ 
                            event.get("type", NULL),
                            event.get("id", NULL),
                            event.get("sequence", NULL),
                            event.get("clock", NULL),
                            event.get("scoring_play", NULL),
                            event.get("home_points", NULL),
                            event.get("away_points", NULL),
                            event.get("play_type", NULL),
                            event.get("wall_clock", NULL),
                            event.get("description", NULL).replace(',', '_'), # In case any commas are in the description
                            event.get("fake_punt", NULL),
                            event.get("fake_field_goal", NULL),
                            event.get("screen_pass", NULL),
                            event.get("men_in_box", NULL),
                            event.get("play_direction", NULL),
                            event.get("running_lane", NULL),
                            event.get("run_pass_option", NULL),
                            event.get("players_rushed", NULL),
                            event.get("pocket_location", NULL),
                            event.get("pass_route", NULL),
                            event.get("blitz", NULL),
                            event.get("left_tightends", NULL),
                            event.get("right_tightends", NULL),
                            event.get("hash_mark", NULL),
                            event.get("gb_at_snap", NULL),
                            event.get("huddle", NULL),
                            event.get("play_action", NULL),
                            event.get("created_at", NULL),
                            event.get("updated_at", NULL)
                           ]
                        
                    # Key checks
                    if "start_situation" not in event:
                        line += [NULL] * 14

                    elif "possession" not in event["start_situation"]:
                        line += [
                                 event["start_situation"].get("clock", NULL),
                                 event["start_situation"].get("down", NULL),
                                 event["start_situation"].get("yfd", NULL)
                                ]
                        line += [NULL] * 11

                    else:
                        line += [
                                 event["start_situation"].get("clock", NULL),
                                 event["start_situation"].get("down", NULL),
                                 event["start_situation"].get("yfd", NULL),
                                 event["start_situation"]["possession"].get("id", NULL),
                                 event["start_situation"]["possession"].get("name", NULL),
                                 event["start_situation"]["possession"].get("market", NULL),
                                 event["start_situation"]["possession"].get("alias", NULL),
                                 event["start_situation"]["possession"].get("sr_id", NULL),
                                 event["start_situation"]["location"].get("id", NULL),
                                 event["start_situation"]["location"].get("name", NULL),
                                 event["start_situation"]["location"].get("market", NULL),
                                 event["start_situation"]["location"].get("alias", NULL),
                                 event["start_situation"]["location"].get("sr_id", NULL),
                                 event["start_situation"]["location"].get("yardline", NULL)
                                ]

                    if "end_situation" not in event:
                        line += [NULL] * 14
                    elif "possession" not in event["start_situation"]:
                        line += [
                                  event["end_situation"].get("clock", NULL),
                                  event["end_situation"].get("down", NULL),
                                  event["end_situation"].get("yfd", NULL)
                                ]
                        line += [NULL] * 11
                    else:
                        line += [
                                event["end_situation"].get("clock", NULL),
                                event["end_situation"].get("down", NULL),
                                event["end_situation"].get("yfd", NULL),
                                event["end_situation"]["possession"].get("id", NULL),
                                event["end_situation"]["possession"].get("name", NULL),
                                event["end_situation"]["possession"].get("market", NULL),
                                event["end_situation"]["possession"].get("alias", NULL),
                                event["end_situation"]["possession"].get("dr_id", NULL),
                                event["end_situation"]["location"].get("id", NULL),
                                event["end_situation"]["location"].get("name", NULL),
                                event["end_situation"]["location"].get("alias", NULL),
                                event["end_situation"]["location"].get("sr_id", NULL),
                                event["end_situation"]["location"].get("yardline", NULL),
                                event["end_situation"]["location"].get("market", NULL),
                            ]
                        
                    # Handle list of statistics
                    if "statistics" in event:
                        for stats in event["statistics"]:
                            line += [ 
                                    stats.get("stat_type", NULL),
                                    stats.get("attempt", NULL),
                                    stats.get("yards", NULL),
                                    stats.get("net_yards", NULL),
                                    stats.get("inside_20", NULL),
                                    stats.get("hang_time", NULL),
                                    stats.get("touchback", NULL),
                                    stats.get("onside_attempt", NULL),
                                    stats.get("onside_success", NULL),
                                    stats.get("squib_kick", NULL),
                                    stats.get("firstdown", NULL),
                                    stats.get("goaltogo", NULL),
                                    stats.get("broken_tackles", NULL),
                                    stats.get("kneel_down", NULL),
                                    stats.get("scramble", NULL),
                                    stats.get("yards_after_contact", NULL),
                                    stats.get("on_target_throw", NULL),
                                    stats.get("batted_pass", NULL),
                                    stats.get("hurry", NULL),
                                    stats.get("knockdown", NULL),
                                    stats.get("penalty", NULL),
                                    stats.get("complete", NULL),
                                    stats.get("att_yards", NULL),
                                    stats.get("pocket_time", NULL),
                                    stats.get("made", NULL)
                                    ]

                            if "player" in stats:
                                line += [
                                         stats["player"].get("id", NULL),
                                         stats["player"].get("name", NULL),
                                         stats["player"].get("jersey", NULL),
                                         stats["player"].get("position", NULL),
                                         stats["player"].get("sr_id", NULL),
                                         stats["player"].get("role", NULL)
                                        ]
                            else:
                                 line += [NULL] * NUM_PLAYER_FIELDS

                            if "team" in stats:
                                line += [
                                         stats["team"].get("id", NULL),
                                         stats["team"].get("name", NULL),
                                         stats["team"].get("market", NULL),
                                         stats["team"].get("alias", NULL),
                                         stats["team"].get("sr_id", NULL)
                                        ]
                            else:
                                line += [NULL] * NUM_TEAM_FIELDS
    
                    # Fill out any remaining unpopulated stats fields with NULL
                    line += [NULL] * NUM_STATS_FIELDS * (MAX_STATS_LEN - len(event.get("statistics", [])))

                    if len(event.get("statistics", [])) > max_num_stats:
                        max_num_stats = len(event["statistics"])
                
                    # Handle list of details
                    if "details" in event:
                        for detail in event["details"]:
                            line += [
                                    detail.get("category", NULL),
                                    detail.get("description", NULL).replace(',', '_'),
                                    detail.get("sequence", NULL),
                                    detail.get("direction", NULL),
                                    detail.get("yards", NULL),
                                    detail.get("result", NULL),
                                    detail["start_location"].get("alias", NULL),
                                    detail["start_location"].get("yardline", NULL),
                                    detail["end_location"].get("alias", NULL),
                                    detail["end_location"].get("yardline", NULL),
                                    detail.get("ast_tackle", NULL),
                                    detail.get("ast_sack", NULL),
                                    detail.get("blitz", NULL),
                                    detail.get("block", NULL),
                                    detail.get("def_target", NULL),
                                    detail.get("fumble", NULL),
                                    detail.get("forced_fumble", NULL),
                                    detail.get("interception", NULL),
                                    detail.get("missed_tackles", NULL),
                                    detail.get("nullified", NULL),
                                    detail.get("pass_defended", NULL),
                                    detail.get("qb_hit", NULL),
                                    detail.get("sack", NULL),
                                    detail.get("sack_yards", NULL),
                                    detail.get("tackle", NULL),
                                    detail.get("attempt", NULL),
                                    detail.get("blocked", NULL),
                                    detail.get("missed", NULL),
                                    detail.get("returned", NULL),
                                    detail.get("aborted", NULL),
                                    detail.get("endzone", NULL),
                                    detail.get("inside_20", NULL),
                                    detail.get("made", NULL),
                                    detail.get("hurry", NULL),
                                    detail.get("touchdown", NULL),
                                    detail.get("faircatch", NULL),
                                    detail.get("incompletion_type", NULL),
                                    detail.get("target", NULL),
                                    detail.get("knockdown", NULL),
                                    detail.get("dropped", NULL),
                                    detail.get("reception", NULL),
                                    detail.get("catchable", NULL),
                                    detail.get("return", NULL),
                                    detail.get("tlost", NULL),
                                    detail.get("tlost_yards", NULL),

                                    detail.get("def_comp", NULL),
                                    detail.get("broken_tackles", NULL),
                                    detail.get("forced", NULL),
                                    detail.get("down", NULL),
                                    detail.get("batted_pass", NULL),
                                    detail.get("yards_after_catch", NULL),
                                    detail.get("lateral", NULL),
                                    detail.get("safety", NULL),
                                    detail.get("kickoff", NULL),
                                    detail.get("recovery", NULL),
                                    detail.get("primary", NULL),
                                    detail.get("bounds", NULL)
                                    ]

                            for player in detail["players"]:
                                line += [ 
                                        player.get("id", NULL),
                                        player.get("name", NULL),
                                        player.get("jersey", NULL),
                                        player.get("position", NULL),
                                        player.get("sr_id", NULL),
                                        player.get("role", NULL)
                                        ]

                            # Fill out any remaining unpopulated player fields with NULL
                            line += [NULL] * NUM_PLAYER_FIELDS * (MAX_DETAILS_PLAYERS - len(detail.get("players", [])))

                            if len(detail.get("players", [])) > max_num_players:
                                max_num_players = len(detail["players"])

                    # Fill out any remaining unpopulated detail fields with NULL
                    line += [NULL] * NUM_DETAILS_FIELDS * (MAX_DETAILS_LEN - len(event.get("details", [])))

                    if len(event.get("details", [])) > max_num_details:
                        max_num_details = len(event["details"])

                    # Ensure the number of fields in the header matches the number of line fields
                    if (NUM_HEADER_FIELDS != len(line)):
                        print(NUM_HEADER_FIELDS, len(line))

                    assert NUM_HEADER_FIELDS == len(line)
                    line = ','.join([str(l) for l in line]) + '\n'
                    out.write(line)
                    num_plays_processed += 1

                # Currently ignoring non-play events such as TV breaks or start/end game
                else:
                    events_ignored.append(event.get('event_type', "NO_TYPE_GIVEN"))

    print(f"\n\n------------------------------- Results -------------------------------")
    print(f"{num_plays_processed} plays saved.")
    print(f"{len(events_ignored)} events were ignored ({', '.join(events_ignored)})")
    print(f"Number of columns in output {NUM_HEADER_FIELDS}")
    print(f"Maximum number of stats: {max_num_stats}")
    print(f"Maximum number of details: {max_num_details}")
    print(f"Maximum number of players in detail: {max_num_players}\n")