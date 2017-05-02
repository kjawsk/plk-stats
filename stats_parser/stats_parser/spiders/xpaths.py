x_teams_name = "//div[@class='game-team']//h3//a/text()"
x_game_tables = "//table[@class='game-table']"
x_starting_players = ".//tr[td//i[@class='ico-star']]//a//strong/text()"
x_bench_players = ".//tr[@class='row_stat']//td[@class='zawodnik']//a/text()"
x_play_by_play_q1 = \
    "//div[@class='tab tab0 current']//table[@id='playbyplay']//tbody//tr//td[1] | \
    //div[@class='tab tab0 current']//table[@id='playbyplay']//tbody//tr//td[3]  | \
    //div[@class='tab tab0 current']//table[@id='playbyplay']//tbody//tr//td[5]"

x_play_by_play_q2 = \
    "//div[@id='playbyplay-wrapper']//div[@class='tab tab1']//table[@id='playbyplay']//tbody//tr//td[1] | \
     //div[@id='playbyplay-wrapper']//div[@class='tab tab1']//table[@id='playbyplay']//tbody//tr//td[3]  | \
     //div[@id='playbyplay-wrapper']//div[@class='tab tab1']//table[@id='playbyplay']//tbody//tr//td[5]"

x_play_by_play_q3 = \
    "//div[@class='tab tab2']//table[@id='playbyplay']//tbody//tr//td[1] | \
    //div[@class='tab tab2']//table[@id='playbyplay']//tbody//tr//td[3]  | \
    //div[@class='tab tab2']//table[@id='playbyplay']//tbody//tr//td[5]"

x_play_by_play_q4 = \
    "//div[@class='tab tab3']//table[@id='playbyplay']//tbody//tr//td[1] | \
    //div[@class='tab tab3']//table[@id='playbyplay']//tbody//tr//td[3]  | \
    //div[@class='tab tab3']//table[@id='playbyplay']//tbody//tr//td[5]"

x_play_by_play = {
    1: x_play_by_play_q1,
    2: x_play_by_play_q2,
    3: x_play_by_play_q3,
    4: x_play_by_play_q4}
