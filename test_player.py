
class Player:
    def test_player(self):
        player_obj = Player('https://worldofwarcraft.com/en-us/character/us/bleeding-hollow/drblank')
        assert(player_obj is not None)
