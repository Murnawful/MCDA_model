import model_functions as mf
import domination as dm
from math import *

f = open('eval_strategy.txt', 'w')
f.write(" Strategy (f_canon, f_assault, nb in assault)   Allied victims   Duration  Canon damage  Civilians victims")
f.write("\n")

g = open('pareto_set.txt', 'w')
g.write(" Strategy (f_canon, f_assault, nb in assault)   Allied victims   Duration  Canon damage  Civilians victims")
g.write("\n")

victory_strategy_list = []

####################################
## Inputs for strategy evaluation ##
####################################
total_enemy_nb = 7700
total_allied_nb = 150000
civilians = 50000

begin_siege = 0  # 6th april 1453
limit_date = 56  # 31th may 1453

victory_threshold = 3300

###################################
####### Strategy evaluation #######
###################################
for f_canon in range(1, 112, 1):
    f_canon = f_canon / 2
    for f_assault in range(2, 56, 1):
        for allies_in_assault in range(1000, 150000, 1000):

            current_time = begin_siege
            current_allies = total_allied_nb
            current_enemies = total_enemy_nb
            current_civilians = civilians

            next_time_canon = 0
            next_time_assault = 0

            wall_state = 100
            canon_state = 100

            is_war_over = False
            is_war_won = False

            while not is_war_over or not is_war_won:
                next_time = min(next_time_canon, next_time_assault, limit_date)
                current_time = next_time
                if next_time == limit_date:
                    is_war_over = True
                    break
                elif next_time == next_time_canon:
                    next_event = 'canon'
                else:
                    next_event = 'assault'

                if next_event == 'canon':
                    current_civilians -= min(current_civilians, int(ceil(mf.canon_effect_on_civil(wall_state))))
                    current_enemies -= min(current_enemies, int(floor(mf.canon_effect_on_enemy_soldiers(wall_state))))
                    current_allies -= min(current_allies, int(ceil(mf.canon_effect_on_allied_soldiers(canon_state))))
                    canon_state -= min(canon_state, mf.canon_deterioration(canon_state))
                    wall_state -= min(wall_state, mf.canon_effect_on_wall(wall_state))

                    next_time_canon += f_canon

                if next_event == 'assault':
                    soldiers_sent = min(allies_in_assault, current_allies)
                    remaining_defenders = current_enemies

                    ennemy_deaths = floor(mf.assault_effect_on_ennemy_soldiers(wall_state, soldiers_sent,
                                                                               remaining_defenders) * soldiers_sent)
                    current_enemies -= min(ennemy_deaths, current_enemies)

                    allied_deaths = ceil(mf.assault_effect_on_allied_soldiers(wall_state, soldiers_sent,
                                                                              remaining_defenders) * remaining_defenders)
                    current_allies -= min(allied_deaths, soldiers_sent)

                    next_time_assault += f_assault

                if current_allies == 0:
                    is_war_over = True
                    break

                if current_enemies <= victory_threshold:
                    is_war_won = True
                    break

            if not is_war_over and is_war_won:
                strategy = (f_canon, f_assault, allies_in_assault)
                allied_victims = total_allied_nb - current_allies
                assault_duration = current_time
                canon_damage = canon_state
                civilians_victims = civilians - current_civilians

                f.write(str(strategy) + "  " + str(allied_victims) + "  " + str(assault_duration) + "  " + str(
                    canon_damage) + "  " + str(civilians_victims))
                f.write("\n")
                b = [strategy, allied_victims, assault_duration, canon_damage, civilians_victims]
                victory_strategy_list.append(b)

print("Evaluation done")

###################################
##### Pareto set construction #####
###################################
dominated = [0] * len(victory_strategy_list)

for i in range(len(victory_strategy_list)):
    if dominated[i] == 0:
        for j in range(len(victory_strategy_list)):
            if dominated[j] == 0 and not (i == j):
                dom = dm.is_dominating_strat(victory_strategy_list[i], victory_strategy_list[j])
                if dom == 1:
                    dominated[j] = 1
                elif dom == 2:
                    dominated[i] = 1

print("Pareto output ready")

pareto_set = []
for i in range(len(victory_strategy_list)):
    if dominated[i] == 0:
        pareto_set.append(victory_strategy_list[i])

for elem in pareto_set:
    strategy = elem[0]
    allied_victims = elem[1]
    assault_duration = elem[2]
    canon_damage = elem[3]
    civilians_victims = elem[4]

    g.write(str(strategy) + " $ " + str(allied_victims) + " $ " + str(assault_duration) + " $ " + str(
        canon_damage) + " $ " + str(civilians_victims))
    g.write("\n")

###################################
########## Closing files ##########
###################################
f.close()
g.close()
