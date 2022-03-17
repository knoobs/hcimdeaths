# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 17:30:56 2021

@author: kneub
"""

class Urls:
    IM_PERSONAL   = "https://secure.runescape.com/m=hiscore_oldschool_ironman/hiscorepersonal?user1="
    HCIM_PERSONAL = "https://secure.runescape.com/m=hiscore_oldschool_hardcore_ironman/hiscorepersonal?user1="
    IM_PAGE       = "https://secure.runescape.com/m=hiscore_oldschool_ironman/overall?table=0&page="
    HCIM_PAGE     = "https://secure.runescape.com/m=hiscore_oldschool_hardcore_ironman/overall?table=0&page="
    HCIM_SKILL_PAGE = "https://secure.runescape.com/m=hiscore_oldschool_hardcore_ironman/overall?table="
    HCIM_BOSS_PAGE  = "https://secure.runescape.com/m=hiscore_oldschool_hardcore_ironman/overall?category_type=1&table="

class Channels:
    GENERAL = 279862546285199361
    BOT_CHANNEL = 461283138962849812

class UserAgents:
    DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
    
class Constants:
    MAX_RANK = 1000
    PRINTS = True
    IGNORED_PLAYERS = ['gandara'] # lowercase
    PVM_DICT = {'Bounty Hunter - Hunter'            : 1,
                'Bounty Hunter - Rogue'             : 2,
                'Clue Scrolls (all)'                : 3,
                'Clue Scrolls (beginner)'           : 4,
                'Clue Scrolls (easy)'               : 5,
                'Clue Scrolls (medium)'             : 6,
                'Clue Scrolls (hard)'               : 7,
                'Clue Scrolls (elite)'              : 8,
                'Clue Scrolls (master)'             : 9,
                'Mimic'                             : 10,
                'LMS - Rank'                        : 11,
                'Soul Wars Zeal'                    : 12,
                'Wintertodt'                        : 13,
                'Tempoross'                         : 14,
                'Hespori'                           : 15,              
                'Obor'                              : 16,
                'Bryophyta'                         : 17,      
                'Deranged Archaeologist'            : 18,
                'Barrows Chests'                    : 19,   
                'Giant Mole'                        : 20,             
                'Sarachnis'                         : 21, 
                'Zulrah'                            : 22,
                'Vorkath'                           : 23,
                'Zalcano'                           : 24,
                
                'Skotizo'                           : 25,       
                'Dagannoth Prime'                   : 26,
                'Dagannoth Rex'                     : 27,
                'Dagannoth Supreme'                 : 28,
                'Kalphite Queen'                    : 29,
                'Grotesque Guardians'               : 30,
                'Abyssal Sire'                      : 31,
                'Kraken'                            : 32,
                'Cerberus'                          : 33,               
                'Thermonuclear Smoke Devil'         : 34,
                'Alchemical Hydra'                  : 35,
                
                'Crazy Archaeologist'               : 36,
                'Chaos Fanatic'                     : 37,
                'King Black Dragon'                 : 38,
                'Chaos Elemental'                   : 39,
                'Scorpia'                           : 40,
                'Venenatis'                         : 41,
                'Callisto'                          : 42,
                "Vet'ion"                           : 43,
               
                "K'ril Tsutsaroth"                  : 44,
                'General Graardor'                  : 45,
                'Commander Zilyana'                 : 46,
                "Kree'Arra"                         : 47,
                'Nex'                               : 48,
                
                
                'Corporeal Beast'                   : 49,
                'Nightmare'                         : 50,          
                "Phosani's Nightmare"               : 51,
                

                'The Gauntlet'                      : 52,
                'The Corrupted Gauntlet'            : 53,
                'Chambers of Xeric'                 : 54,
                'Chambers of Xeric: Challenge Mode' : 55,
                'Theatre of Blood'                  : 56,
                'Theatre of Blood: Hard Mode'       : 57,

                'TzTok-Jad'                         : 58,
                'TzKal-Zuk'                         : 59}
    
    NEW_PVM_DICT = {
                'Clue Scrolls (beginner)'           : 4,
                'Clue Scrolls (easy)'               : 5,
                'Clue Scrolls (medium)'             : 6,
                'Clue Scrolls (hard)'               : 7,
                'Clue Scrolls (elite)'              : 8,
                'Clue Scrolls (master)'             : 9,
                'Mimic'                             : 10,
                'LMS - Rank'                        : 11,
                'Soul Wars Zeal'                    : 12,
                'Wintertodt'                        : 13,
                'Tempoross'                         : 14,
                'Hespori'                           : 15,              
                'Obor'                              : 16,
                'Bryophyta'                         : 17,      
                'Deranged Archaeologist'            : 18,
                'Barrows Chests'                    : 19,   
                'Giant Mole'                        : 20,             
                'Sarachnis'                         : 21, 
                'Zulrah'                            : 22,
                'Vorkath'                           : 23,
                'Zalcano'                           : 24,
                
                'Skotizo'                           : 25,       
                'Dagannoth Prime'                   : 26,
                'Dagannoth Rex'                     : 27,
                'Dagannoth Supreme'                 : 28,
                'Kalphite Queen'                    : 29,
                'Grotesque Guardians'               : 30,
                'Abyssal Sire'                      : 31,
                'Kraken'                            : 32,
                'Cerberus'                          : 33,               
                'Thermonuclear Smoke Devil'         : 34,
                'Alchemical Hydra'                  : 35,
                
                'Crazy Archaeologist'               : 36,
                'Chaos Fanatic'                     : 37,
                'King Black Dragon'                 : 38,
                'Chaos Elemental'                   : 39,
                'Scorpia'                           : 40,
                'Venenatis'                         : 41,
                'Callisto'                          : 42,
                "Vet'ion"                           : 43,
               
                "K'ril Tsutsaroth"                  : 44,
                'General Graardor'                  : 45,
                'Commander Zilyana'                 : 46,
                "Kree'Arra"                         : 47,
                'Nex'                               : 48,
                
                
                'Corporeal Beast'                   : 49,
                'Nightmare'                         : 50,          
                "Phosani's Nightmare"               : 51,
                

                'The Gauntlet'                      : 52,
                'The Corrupted Gauntlet'            : 53,
                'Chambers of Xeric'                 : 54,
                'Chambers of Xeric: Challenge Mode' : 55,
                'Theatre of Blood'                  : 56,
                'Theatre of Blood: Hard Mode'       : 57,

                'TzTok-Jad'                         : 58,
                'TzKal-Zuk'                         : 59}
    
    
    SKILL_DICT={'Overall'       : 0,
                'Attack'        : 1,
                'Defence'       : 2,
                'Strength'      : 3,
                'Hitpoints'     : 4,
                'Ranged'        : 5,
                'Prayer'        : 6,
                'Magic'         : 7,
                'Cooking'       : 8,
                'Woodcutting'   : 9,
                'Fletching'     : 10,
                'Fishing'       : 11,
                'Firemaking'    : 12,
                'Crafting'      : 13,
                'Smithing'      : 14,
                'Mining'        : 15,
                'Herblore'      : 16,
                'Agility'       : 17,
                'Thieving'      : 18,
                'Slayer'        : 19,   
                'Farming'       : 20,
                'Runecraft'     : 21,
                'Hunter'        : 22,
                'Construction'  : 23 }
    X_SEP = 126
    X_0 = 94
    Y_SEP = 62
    Y_0 = 40
    X_SEP_BOSS = 140
    SKILL_COORDS={'Overall'       : (X_0+2*X_SEP-28, Y_0+7*Y_SEP+18),
                'Attack'        : (X_0+0*X_SEP, Y_0+0*Y_SEP),
                'Defence'       : (X_0+0*X_SEP, Y_0+2*Y_SEP),
                'Strength'      : (X_0+0*X_SEP, Y_0+1*Y_SEP),
                'Hitpoints'     : (X_0+1*X_SEP, Y_0+0*Y_SEP),
                'Ranged'        : (X_0+0*X_SEP, Y_0+3*Y_SEP),
                'Prayer'        : (X_0+0*X_SEP, Y_0+4*Y_SEP),
                'Magic'         : (X_0+0*X_SEP, Y_0+5*Y_SEP),
                'Cooking'       : (X_0+2*X_SEP, Y_0+3*Y_SEP),
                'Woodcutting'   : (X_0+2*X_SEP, Y_0+5*Y_SEP),
                'Fletching'     : (X_0+1*X_SEP, Y_0+5*Y_SEP),
                'Fishing'       : (X_0+2*X_SEP, Y_0+2*Y_SEP),
                'Firemaking'    : (X_0+2*X_SEP, Y_0+4*Y_SEP),
                'Crafting'      : (X_0+1*X_SEP, Y_0+4*Y_SEP),
                'Smithing'      : (X_0+2*X_SEP, Y_0+1*Y_SEP),
                'Mining'        : (X_0+2*X_SEP, Y_0+0*Y_SEP),
                'Herblore'      : (X_0+1*X_SEP, Y_0+2*Y_SEP),
                'Agility'       : (X_0+1*X_SEP, Y_0+1*Y_SEP),
                'Thieving'      : (X_0+1*X_SEP, Y_0+3*Y_SEP),
                'Slayer'        : (X_0+1*X_SEP, Y_0+6*Y_SEP),
                'Farming'       : (X_0+2*X_SEP, Y_0+6*Y_SEP),
                'Runecraft'     : (X_0+0*X_SEP, Y_0+6*Y_SEP),
                'Hunter'        : (X_0+1*X_SEP, Y_0+7*Y_SEP),
                'Construction'  : (X_0+0*X_SEP, Y_0+7*Y_SEP) }
    SKIPPED_BOSSES = ['Clue Scrolls (all)',
                      'Bounty Hunter - Hunter',
                      'Bounty Hunter - Rogue']
