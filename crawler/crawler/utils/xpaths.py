x_home_team_name = "//div[@class='game-team'][1]//h3//a/text()"
x_away_team_name = "//div[@class='game-team'][2]//h3//a/text()"
x_date = "//div[@class='details']//div[@class='left']//text()"
x_game_tables = "//table[@class='game-table']"

x_home_s5 = "//table[@class='game-table'][1]//tr[td//i[@class='ico-star']]//a//strong/text()"
x_home_bench = "//table[@class='game-table'][1]//tr[@class='row_stat']//td[@class='zawodnik']//a/text()"

x_away_s5 = "//table[@class='game-table'][2]//tr[td//i[@class='ico-star']]//a//strong/text()"
x_away_bench = "//table[@class='game-table'][2]//tr[@class='row_stat']//td[@class='zawodnik']//a/text()"

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

x_home_team_2pkt_throws = "//div[@id='tabpagesmatch']/div[1]/table[1]/tbody/tr[14]/td[4]"
x_away_team_2pkt_throws = "//div[@id='tabpagesmatch']/div[1]/table[2]/tbody/tr[14]/td[4]"
