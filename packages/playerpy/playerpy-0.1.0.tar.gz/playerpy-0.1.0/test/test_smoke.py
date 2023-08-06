from vi3o import Video
from playerpy import Player
from py.test import raises
from pathlib import Path

mydir = Path(__file__).parent
test_mkv = mydir / "t.mkv"


def test_not_a_video():
    with raises(ValueError):
        Player(test_mkv)

def smoke_test():
    video = Video(test_mkv)
    player = Player(test_mkv)
    assert hasattr(player, "play")
