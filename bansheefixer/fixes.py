class Fixer(object):
    def apply(self, wl):
        self.apply_artist(wl)
        self.apply_album(wl)
        for t in wl:
            self.apply_track(t)

        return wl

    def apply_track(self, track):
        True

    def apply_artist(self, artist):
        True

    def apply_album(self, album):
        True

class FixerGroup(object):
    def __init__(self, *args):
        self._fixes = args

    def apply(self, wl):
        for f in self._fixes:
            f.apply(wl)

        return wl

class TrackNumberInTitle(Fixer):
    def __init__(self, seperator=" "):
        self._seperator = seperator

    def apply_track(self, track):
        tex = track.Title.split(self._seperator, 1)
        if len(tex) == 2:
            try:
                tn = int(tex[0])
                track.Title = tex[1]
                track.TrackNumber = tn
            except ValueError:
                print(repr(track) + " doesn't have a track number in the title")
        else:
            print(repr(track) + " doesn't have a track number in the title")

class TrackNumberInTitleSmart(Fixer):
    def __init__(self, strip_chars=".- "):
        self._chars = strip_chars


    def apply_track(self, track):
        tn = None
        for i in range(len(track.Title)-1):
            st = track.Title[0:i+1]
            try:
                tn = int(st)
            except ValueError:
                break

        # substract on, because the last char made it fail
        i = i - 0

        if tn is not None:
            track.Title = track.Title[i:].strip(self._chars)
            track.TrackNumber = tn


class TrackAndDiscNumberInTitle(Fixer):
    def __init__(self, disc_seperator="-", track_seperator=" "):
        self._disc_seperator = disc_seperator
        self._track_seperator = track_seperator

    def apply_track(self, track):
        tex = track.Title.split(self._track_seperator, 1)
        if len(tex) == 2:
            tex[0] = tex[0].split(self._disc_seperator)
            try:
                tn = int(tex[0][1])
                track.DiscNumber = tex[0][0]
                track.Title = tex[1]
                track.TrackNumber = tn
            except ValueError:
                print(repr(track) + " doesn't have a track number in the title")
        else:
            print(repr(track) + " doesn't have a track number in the title")

class StripFromTitle(Fixer):
    def __init__(self, to_strip):
        self._to_strip = to_strip

    def apply_track(self, t):
        t.Title = t.Title.lstrip(self._to_strip)

class CapitalizeTitle(Fixer):
    def apply_track(self, track):
        track.Title = track.Title.title()

class VinylCaptionsInTitle(Fixer):
    def __init__(self, seperator = " ", remove_caption=False, set_track_number=True):
        self._remove_caption = remove_caption
        self._set_track_number = set_track_number
        self._seperator = seperator

    def apply(self, wl):
        tmp = [(t.Title.split(self._seperator, 1)[0], t) for t in wl]
        tmp.sort()
        i = 1
        for t in tmp:
            t[1].TrackNumber = i
            i = i + 1
