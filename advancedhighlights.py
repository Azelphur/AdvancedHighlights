import yaml
import znc
import pygeoip

default_config = """config:
  geoip: "/usr/share/GeoIP/GeoIP.dat" # Location of GeoIP.dat database for GeoIP
  doLast:
    - geoip # Do GeoIP last as DNS lookups take a long time and can create a backlog.
matches:
  "Bacon but only from England": # The name of the rule
    word: # Match a whole word (use text to match anything in the string)
      case_sensitive: false
      match: bacon
    channels: # Match only in these channels
      - "#baconcentral"
    geoip: # Match only users from Great Britain
      - GB
"""

class AdvancedHighlights():
    def __init__(self):
        self.config = None

    def loadConfig(self, config):
        self.config = config
        self.gi = pygeoip.GeoIP(self.config['config']['geoip'], pygeoip.MEMORY_CACHE)

    def text(self, args, data):
        if args['case_sensitive']:
            if args['match'] in data['text']:
                return True
        else:
            if args['match'].lower() in data['text'].lower():
                return True
        return False

    def word(self, args, data):
        if args['case_sensitive']:
            return ' ' + args['match'] + ' ' in ' ' + data['text'] + ' '
        else:
            return ' ' + args['match'].lower() + ' ' in ' ' + data['text'].lower() + ' '

    def channels(self, args, data):
        if data['channel'] in args:
            return True
        return False

    def geoip(self, args, data):
        host = data["host"]
        if host.find("gateway/web/freenode/ip.") != -1: # Check if it's a freenode web gateway
            host = host[host.find("gateway/web/freenode/ip.")+24:]
        elif "/" in host: # Make sure it's not a freenode fake host
            return False
        if self.gi.country_code_by_name(host) in args:
            return True
        return False

    def nick(self, args, data):
        if data["nick"] in args:
            return True
        return False

    def match(self, data):
        if self.config == None: return
        for match, filters in self.config['matches'].items():
            matched = True
            last = []

            for matcher, arguments in filters.items():

                match = False
                if matcher[0] == '!':
                    match = True
                    matcher = matcher[1:]
                if matcher in self.config['config']['doLast']:
                    last.append((matcher, arguments))
                    continue
                if getattr(self, matcher)(arguments, data) == match:
                    matched = False
                    break

            # Do expensive checks last if all other checks have passed
            if matched:
                for matcher, arguments in last:
                    match = False
                    if matcher[0] == '!':
                        match = True
                        matcher = matcher[1:]
                    if getattr(self, matcher)(arguments, data) == match:
                        matched = False
                        break

            if matched:
                return True, match
        return False, ''
    

class advancedhighlights(znc.Module):
    description = "Highly configurable highlights"

    def OnLoad(self, args, message):
        self.ah = AdvancedHighlights()
        self._reloadConfig()
        return True

    def OnChanMsg(self, nick, channel, message):
        matched, rule = self.ah.match({'text' : message.s, 'nick' : nick.GetNick(), 'host' : nick.GetHost(), 'channel' : channel.GetName()})
        if matched:
            self.PutModule("%s Matched %s rule on %s by saying %s" % (nick.GetNick(), rule, channel.GetName(), message.s))
        return znc.CONTINUE

    def GetWebMenuTitle(self):
        return "Advanced Highlights"

    def OnWebRequest(self, sock, pagename, tmpl):
        if pagename == "index" and "config" in self.nv:
            tmpl["config"] = self.nv["config"]
        else:
            if sock.IsPost():
                self.nv["config"] = sock.GetRawParam("config", True)
                tmpl["message"] = self._reloadConfig()
        return True

    def _reloadConfig(self):
        if "config" not in self.nv:
            self.nv["config"] = default_config
        try:
            self.ah.loadConfig(yaml.load(self.nv["config"]))
            return "Config Loaded sucessfully"
        except yaml.scanner.ScannerError as e:
            self.ah.loadConfig(None)
            return str(e)

