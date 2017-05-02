x_teams_name = "//div[@class='game-team']//h3//a/text()"
x_game_tables = "//table[@class='game-table']"
x_starting_players = ".//tr[td//i[@class='ico-star']]//a//strong/text()"
x_bench_players = ".//tr[@class='row_stat']//td[@class='zawodnik']//a/text()"
x_play_by_play = \
    "//div[@class='tab tab0 current']//table[@id='playbyplay']//tbody//tr//td[1] | \
    //div[@class='tab tab0 current']//table[@id='playbyplay']//tbody//tr//td[3]  | \
    //div[@class='tab tab0 current']//table[@id='playbyplay']//tbody//tr//td[5]"
