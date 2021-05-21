def is_dominating_strat(strat1, strat2):
    if strat1[1] <= strat2[1] and strat1[2] <= strat2[2] and strat1[3] >= strat2[3] and strat1[4] <= strat2[4]:
        return 1
    elif strat1[1] >= strat2[1] and strat1[2] >= strat2[2] and strat1[3] <= strat2[3] and strat1[4] >= strat2[4]:
        return 2
    else:
        return 0
