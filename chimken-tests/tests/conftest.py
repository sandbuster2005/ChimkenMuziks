"""Black-box test harness for ChimkenMuziks, driven through its D-Bus interfaces.

The real app is launched in a pseudo-terminal, inside a sandbox (own HOME and XDG
directories), under a private D-Bus session bus (see run_tests.sh). Tests talk to it
with `busctl` (the same tool you use by hand), over:
  - MPRIS (org.mpris.MediaPlayer2[.Player]) : transport controls and state
  - the debug interface (org.chimkenmuziks.debug, DebugInput) : keyboard-like input

The app only answers over MPRIS while a song is playing (its update_logic loop), so most
tests use the `playing_app` fixture, which starts the app with a song already playing.

Silent audio: the app must read VLC flags from an environment variable, see
VLC_ENV_VAR below (patch to apply where the app calls vlc.Instance(...)).

Environment variables (all optional):
  APP_REPO            path of the ChimkenMuziks checkout (default ~/ChimkenMuziks)
  APP_PARAM_TEMPLATE  param.txt template, "@MUSIC_DIR@" is replaced by the test music
                      folder (default tests/param.template.txt)
  APP_START_ARGS      arguments that make the app start playing; "{song}" is replaced
                      by the first test track (default: "--song {song}")
  APP_START_INPUT     debug inputs sent after startup, separated by ";" (use with
                      APP_START_ARGS="" to start playback without --song)
  DEBUG_OBJECT_PATH   D-Bus object path of the debug interface (default: the MPRIS path)
  TRACK_SECONDS       length of the generated tracks (default 300)
"""
import contextlib
import json
import os
import pathlib
import shlex
import shutil
import subprocess
import threading
import time

import pexpect
import pyte
import pytest

BUS_NAME = "org.mpris.MediaPlayer2.ChimkenMuziks"
PATH = "/org/mpris/MediaPlayer2"
ROOT_IFACE = "org.mpris.MediaPlayer2"
PLAYER_IFACE = "org.mpris.MediaPlayer2.Player"
DEBUG_IFACE = "org.chimkenmuziks.debug"
DEBUG_PATH = os.environ.get("DEBUG_OBJECT_PATH", PATH)

# The app has to pass the flags in this variable to vlc.Instance(...)
VLC_ENV_VAR = "CHIMKEN_VLC_ARGS"
VLC_ARGS = "--aout=dummy --no-video"

REPO = pathlib.Path(os.environ.get("APP_REPO", "~/ChimkenMuziks")).expanduser()
APP_PYTHON = REPO / ".env" / "bin" / "python"
PARAM_TEMPLATE = pathlib.Path(
    os.environ.get("APP_PARAM_TEMPLATE", pathlib.Path(__file__).parent / "param.template.txt")
)
START_ARGS = shlex.split(os.environ.get("APP_START_ARGS", "--song {song}"))
START_INPUT = [s for s in os.environ.get("APP_START_INPUT", "").split(";") if s]

# sine tones, alphabetical file order = expected playlist order
TRACKS = [("Track A", 440), ("Track B", 660), ("Track C", 880)]
TRACK_SECONDS = int(os.environ.get("TRACK_SECONDS", "300"))
SHORT_TRACK_SECONDS = 20  # end-of-track test only

# Tests that need the app to know about the test music folder
needs_library = pytest.mark.skipif(
    not PARAM_TEMPLATE.exists(),
    reason=f"{PARAM_TEMPLATE} missing: put a real param.txt there with the music "
           "folder replaced by @MUSIC_DIR@",
)


def wait_for(cond, timeout=5.0, interval=0.05):
    """Poll `cond` until it is truthy.

    Exceptions (D-Bus not ready yet...) count as "not yet", but the last one is printed
    when the wait times out, so a broken client is never mistaken for an unresponsive app.
    """
    end = time.time() + timeout
    last = None
    while time.time() < end:
        try:
            if cond():
                return True
            last = None
        except Exception as e:  # noqa: BLE001
            last = e
        time.sleep(interval)
    if last is not None:
        print("wait_for timed out, last error: %r" % (last,))
    return False


# --------------------------------------------------------------------------- D-Bus client
def _busctl(*args, timeout=5):
    cmd = ["busctl", "--user", "--json=short"]
    bus_address = os.environ.get("DBUS_SESSION_BUS_ADDRESS")
    if bus_address:
        cmd.append(f"--address={bus_address}")
    cmd.extend(args)

    r = subprocess.run(
        cmd,
        capture_output=True, text=True, timeout=timeout,
    )
    if "PlaybackStatus" not in cmd and not True:
        print(f"COMMAND: {' '.join(cmd)}")
        print(f"STDERR: {r.stderr}")
        print(f"STDOUT: {r.stdout}")


    if r.returncode != 0:
        raise RuntimeError("busctl %s failed: %s" % (" ".join(args), r.stderr.strip()))
    return r.stdout


def _busctl_text(*args, timeout=5):
    r = subprocess.run(["busctl", "--user", f"--address={os.environ.get('DBUS_SESSION_BUS_ADDRESS')}" , *args], capture_output=True, text=True,
                       timeout=timeout)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip())
    return r.stdout


def _unwrap(v):
    """busctl --json: every variant is {"type": sig, "data": value}; flatten recursively."""
    if isinstance(v, dict) and set(v) == {"type", "data"}:
        return _unwrap(v["data"])
    if isinstance(v, dict):
        return {k: _unwrap(x) for k, x in v.items()}
    if isinstance(v, list):
        return [_unwrap(x) for x in v]
    return v


def get_property(iface, name, path=PATH):
    out = _busctl("get-property", BUS_NAME, path, iface, name)
    return _unwrap(json.loads(out))


def dbus_call(method, iface, path=PATH, signature="", *values):
    return _busctl("call", BUS_NAME, path, iface, method, *([signature, *values] if signature else []))


# --------------------------------------------------------------------------- helpers
class App:
    """Handle on a running app: D-Bus helpers, the pty and a virtual screen."""

    def __init__(self, child, screen, cache_dir):
        self.child = child
        self.screen = screen
        self.cache_dir = cache_dir

    # --- state (always a fresh read)
    def prop(self, name, iface=PLAYER_IFACE, path=PATH):
        return get_property(iface, name, path)

    @property
    def status(self):
        return self.prop("PlaybackStatus")

    @property
    def metadata(self):
        return self.prop("Metadata")

    @property
    def title(self):
        return self.metadata.get("xesam:title")

    @property
    def alive(self):
        return self.child.isalive()

    # --- actions
    def player_call(self, method):
        dbus_call(method, PLAYER_IFACE)

    def root_call(self, method):
        dbus_call(method, ROOT_IFACE)

    def send_input(self, text):
        """Same as typing `text` in the TUI, through the debug interface (e.g. "n%")."""
        dbus_call("DebugInput", DEBUG_IFACE, DEBUG_PATH, "s", text)

    # --- diagnostics
    def screen_text(self):
        return "\n".join(self.screen.display)

    def log_tail(self, n=3000):
        logs = sorted((self.cache_dir / "ChimkenMuziks" / "log").glob("*.log"))
        return logs[-1].read_text(errors="replace")[-n:] if logs else "(no log written)"

    def bus_tree(self):
        parts = ["bus address: %s" % os.environ.get("DBUS_SESSION_BUS_ADDRESS")]
        for label, args in (("names on the bus", ("list", "--no-pager")),
                            ("objects of the app", ("tree", BUS_NAME))):
            try:
                parts.append("-- %s --\n%s" % (label, _busctl_text(*args)))
            except Exception as e:  # noqa: BLE001
                parts.append("-- %s --\n(failed: %s)" % (label, e))
        return "\n".join(parts)


def _is_gone():
    try:
        get_property(ROOT_IFACE, "Identity")
    except Exception:  # noqa: BLE001
        return True
    return False


@contextlib.contextmanager
def running_app(request, tmp_path, music_dir, args=()):
    """Start the app in its sandbox, yield an App, always clean up."""
    # --- sandbox: the app uses os.mkdir (not makedirs) for its dirs, so the XDG
    #     parents must exist. Do NOT pre-create the app's own data/cache dirs.
    home = tmp_path / "home"
    config, data, cache = home / ".config", home / ".local" / "share", home / ".cache"
    for d in (config, data, cache):
        d.mkdir(parents=True)

    # tell the app where the test music is
    if PARAM_TEMPLATE.exists():
        target = config / "ChimkenMuziks"
        target.mkdir()
        (target / "param.txt").write_text(
            PARAM_TEMPLATE.read_text().replace("@MUSIC_DIR@", str(music_dir))
        )

    env = {
        **os.environ,
        "HOME": str(home),
        "XDG_CONFIG_HOME": str(config),
        "XDG_DATA_HOME": str(data),
        "XDG_CACHE_HOME": str(cache),
        "TERM": "xterm-256color",
        VLC_ENV_VAR: VLC_ARGS,
        # sdbus (in the app) picks its bus from these: be explicit, never rely on defaults
        "DBUS_STARTER_BUS_TYPE": "session",
        "DBUS_SESSION_BUS_ADDRESS": os.environ["DBUS_SESSION_BUS_ADDRESS"],
    }
    child = pexpect.spawn(
        str(APP_PYTHON), ["lecteur.py", *args],
        cwd=str(request.getfixturevalue("app_src")), env=env, dimensions=(40, 120),
    )

    # A TUI redraws constantly: keep draining the pty so the app never blocks on write.
    screen = pyte.Screen(120, 40)
    stream = pyte.ByteStream(screen)
    stop = threading.Event()

    def drain():
        while not stop.is_set():
            try:
                stream.feed(child.read_nonblocking(65536, timeout=0.1))
            except pexpect.TIMEOUT:
                pass
            except pexpect.EOF:
                break

    threading.Thread(target=drain, daemon=True).start()
    a = App(child, screen, cache)

    try:
        if not wait_for(lambda: get_property(ROOT_IFACE, "Identity"), timeout=15):
            try:
                get_property(ROOT_IFACE, "Identity")
                err = "(works now, the app was just slow to start)"
            except Exception as e:  # noqa: BLE001
                err = repr(e)
            pytest.fail(
                "app never appeared on D-Bus (alive: %s).\nLast busctl error: %s\n"
                "D-Bus:\n%s\nScreen:\n%s\n\nLog:\n%s"
                % (child.isalive(), err, a.bus_tree(), a.screen_text(), a.log_tail()))
        yield a
    finally:
        rep = getattr(request.node, "rep_call", None)
        if rep is not None and rep.failed:  # shown in "Captured stdout teardown"
            print("---- D-Bus objects ----\n" + a.bus_tree())
            print("---- screen at failure ----\n" + a.screen_text())
            print("---- app log tail ----\n" + a.log_tail())
        stop.set()
        if child.isalive():
            child.terminate(force=True)
        child.close()
        wait_for(_is_gone, timeout=3)


# --------------------------------------------------------------------------- fixtures
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    setattr(item, "rep_" + call.when, outcome.get_result())


def _make_tracks(d, seconds):
    if not shutil.which("ffmpeg"):
        pytest.fail("ffmpeg is required to generate the test MP3s (sudo pacman -S ffmpeg)")
    for i, (title, freq) in enumerate(TRACKS, 1):
        subprocess.run(
            [
                "ffmpeg", "-v", "error", "-f", "lavfi",
                "-i", f"sine=frequency={freq}:duration={seconds}",
                "-metadata", f"title={title}", "-metadata", "artist=Test Artist",
                "-c:a", "libmp3lame", str(d / f"0{i}_{title[-1].lower()}.mp3"),
            ],
            check=True,
        )
    return d


@pytest.fixture(scope="session")
def music_dir(tmp_path_factory):
    """Long tracks: the app takes a while to start, nothing must end under a test's feet."""
    return _make_tracks(tmp_path_factory.mktemp("music"), TRACK_SECONDS)


@pytest.fixture(scope="session")
def short_music_dir(tmp_path_factory):
    """Short tracks, only for the end-of-track test."""
    return _make_tracks(tmp_path_factory.mktemp("music_short"), SHORT_TRACK_SECONDS)


@pytest.fixture(scope="session")
def app_src(tmp_path_factory):
    """Throwaway copy of the sources.

    The app moves appdata/param.txt and appdata/cache/data.db out of its working
    directory at startup, so it must never run from the real checkout.
    """
    if not APP_PYTHON.exists():
        pytest.exit(
            f"{APP_PYTHON} not found. Create the app venv first:\n"
            f"  cd {REPO} && python -m venv .env && .env/bin/pip install -r requirement",
            returncode=2,
        )
    if not shutil.which("busctl"):
        pytest.exit("busctl not found (it ships with systemd)", returncode=2)
    if not os.environ.get("DBUS_SESSION_BUS_ADDRESS"):
        pytest.exit("no D-Bus session bus: run the tests through ./run_tests.sh "
                    "(dbus-run-session)", returncode=2)
    dst = tmp_path_factory.mktemp("src") / "app"
    shutil.copytree(REPO, dst, ignore=shutil.ignore_patterns(".env", ".git", "__pycache__"))
    for stale in ("appdata/param.txt", "appdata/cache/data.db"):
        (dst / stale).unlink(missing_ok=True)
    return dst


@pytest.fixture
def app(request, tmp_path, music_dir):
    """App started without a song: only the bits that work before playback."""
    with running_app(request, tmp_path, music_dir) as a:
        yield a


@contextlib.contextmanager
def _playing(request, tmp_path, folder):
    first = sorted(folder.glob("*.mp3"))[0]
    args = [x.format(song=first) for x in START_ARGS]
    with running_app(request, tmp_path, folder, args=args) as a:
        for text in START_INPUT:  # e.g. the command that starts a song in normal mode
            if not wait_for(lambda: a.send_input(text) or True, timeout=10):
                pytest.fail("debug input %r never reached the app (D-Bus call failed)" % text)
            time.sleep(0.5)
        if not wait_for(lambda: a.status == "Playing" and a.title == "01_a", timeout=20):
            state = {}
            for name in ("PlaybackStatus", "Metadata"):
                try:

                    state[name] = a.prop(name)
                except Exception as e:  # noqa: BLE001  report what the app really publishes
                    state[name] = "<error: %r>" % (e,)

            pytest.fail(
                "app did not start playing '%s' (args: %s).\nMPRIS reports: %s\n"
                "D-Bus objects:\n%s\nScreen:\n%s\n\nLog:\n%s"
                % (first.name, args, state, a.bus_tree(), a.screen_text(), a.log_tail())
            )

        yield a


@pytest.fixture
def playing_app(request, tmp_path, music_dir):
    """App started with the first (long) test track already playing."""
    with _playing(request, tmp_path, music_dir) as a:
        yield a


@pytest.fixture
def short_playing_app(request, tmp_path, short_music_dir):
    """Same, with short tracks: only for tests that wait for a track to end."""
    with _playing(request, tmp_path, short_music_dir) as a:
        yield a
