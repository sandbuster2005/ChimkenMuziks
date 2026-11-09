"""End-to-end tests of ChimkenMuziks, driven through MPRIS and the debug interface.

The app only answers over MPRIS while a song is playing, so playback tests use the
`playing_app` fixture (app started with a song). `app` is only for what works before
playback.

Tests marked `needs_library` require tests/param.template.txt (see conftest.py).
Tests marked `known_bug` are expected to fail today (strict xfail): when you fix the
behaviour they start "passing" and pytest reports it, so you can remove the marker.
"""
import pytest
import os
import time
from conftest import ROOT_IFACE, needs_library, wait_for





def known_bug(reason):
    return pytest.mark.xfail(strict=True, reason=reason)


# ---------------------------------------------------------------- startup / spec
def test_registers_on_bus(app):
    assert app.prop("Identity", ROOT_IFACE) == "ChimkenMuziks"


def test_root_capabilities(app):
    assert app.prop("CanQuit", ROOT_IFACE) is True
    assert app.prop("HasTrackList", ROOT_IFACE) is False


def test_loop_status_is_valid(app):
    assert app.prop("LoopStatus") in {"None", "Track", "Playlist"}


# ---------------------------------------------------------------- playback state
@needs_library
def test_started_song_is_reported(playing_app):
    md = playing_app.metadata
    assert playing_app.status == "Playing"
    assert md["xesam:title"] == "01_a"
    assert md["mpris:length"] > 0


def test_pause_and_resume(playing_app):
    playing_app.player_call("Pause")
    assert wait_for(lambda: playing_app.status == "Paused")
    playing_app.player_call("Play")
    assert wait_for(lambda: playing_app.status == "Playing")


@needs_library
def test_play_pause_toggles(playing_app):
    playing_app.player_call("PlayPause")
    assert wait_for(lambda: playing_app.status == "Paused")
    playing_app.player_call("PlayPause")
    assert wait_for(lambda: playing_app.status == "Playing")


@needs_library
def test_next_and_previous_via_mpris(playing_app):
    playing_app.player_call("Next")
    assert wait_for(lambda: playing_app.title == "02_b")
    playing_app.player_call("Previous")
    assert wait_for(lambda: playing_app.title == "01_a")


@needs_library
def test_track_end_advances(short_playing_app):
    # tracks last 20 s here; needs the player to be in "play in order" mode
    assert wait_for(lambda: short_playing_app.title == "02_b", timeout=45)


@known_bug("Stop is not implemented in the MPRIS server")
@needs_library
def test_stop(playing_app):
    playing_app.player_call("Stop")
    assert wait_for(lambda: playing_app.status == "Stopped")


@needs_library
def test_quit_exits_cleanly(playing_app):
    playing_app.root_call("Quit")
    assert wait_for(lambda: not playing_app.alive, timeout=5)
    assert playing_app.child.exitstatus == 0


# ---------------------------------------------------------------- debug input (the TUI's input)
@needs_library
def test_debug_input_next_song(playing_app):
    playing_app.send_input("n%")
    assert wait_for(lambda: playing_app.title == "02_b")


@needs_library
def test_debug_input_next_twice(playing_app):
    playing_app.send_input("n%")
    assert wait_for(lambda: playing_app.title == "02_b")
    playing_app.send_input("n%")
    assert wait_for(lambda: playing_app.title == "03_c")


# ---------------------------------------------------------------- what the TUI draws
@needs_library
def test_tui_shows_current_track(playing_app):
    # the TUI may show the tag title or the file name
    assert wait_for(
        lambda: "Track A" in playing_app.screen_text() or "01_a" in playing_app.screen_text()
    )
