ZNC AdvancedHighlights
==================

About
==================
AdvancedHighlights is a ZNC module that allows you to define fairly complex rules that will trigger a query sent to you (in essence, a highlight) on certain irc messages.

Installing
==================
1) Install pygeoip and pyyaml python modules as these are required for AdvancedHighlights to function
* sudo apt-get install python3-setuptools
* sudo easy_install3 pygeoip
* sudo easy_install3 pyyaml

2) Install AdvancedHighlights
* Download the latest AdvancedHighlights by running **git clone git://github.com/Azelphur/AdvancedHighlights.git**
* Move the files into your ZNC modules directory (usually ~/.znc/modules) by typing **mv AdvancedHighlights/* ~/.znc/modules**

3) Log in to your ZNC web panel and load the AdvancedHighlights module, then create a configuration in the Advanced Highlights section

FAQ
==================
Q: I can't see AdvancedHighlights in my module list!

A: You probably don't have modpython loaded, make sure to do that.


Q: I can't see modpython either!

A: You probably built ZNC without python support, rebuild ZNC using ./configure --enable-python

Q: I get an ImportError even though I've installed the dependencies!

A: You need to restart ZNC after installing new python modules otherwise it won't see them.

Q: I like you and want to send you money

A: You can send money to paypal azelphur@azelphur.com or BTC address 1HCmvBfk8Pg51xXgEoDU2UXKVv6VatMKEC

Matchers
==================
To match messages, you have a number of "matchers", you can use them in any combination to achieve what ever goal you are looking for.
Any matcher name preceeded by "!" will match the opposite, for example "geoip" will only match people from the listed countries, while "!geoip" will only match messages NOT from the listed countries.

word
-------------------------------
matches a single word or combination of words.

* *match* - Word(s) to match

* *case_sensitive* - True or False on whether the match should be cAsE sEnSiTiVe

**Example** this example will match "I like my bacon done crispy" but not "Ilikebacon"
<pre>
word:
  case_sensitive: false
  match: bacon
</pre>

text
-------------------------------
matches any text in the message, not to be confused with word.

* *match* - Word(s) to match

* *case_sensitive* - True or False on whether the match should be cAsE sEnSiTiVe

**Example** this example will match anything with "bacon" in it.
<pre>
text:
  case_sensitive: false
  match: bacon
</pre>

channels
-------------------------------
matches a list of channel(s)

**Example** this example will match to #chat and #bacon
<pre>
channels:
  - "#chat"
  - "#bacon"
</pre>

geoip
-------------------------------
Will do a GeoIP lookup on the hostname of the user and match what country they are in.

**Example** this example will match only users who GeoIP to Great Britain or the United States.
<pre>
geoip:
  - GB
  - US
</pre>

nick
-------------------------------
This will match a list of nicknames

**Example** this example will only match fred and bob.
<pre>
nick:
  - fred
  - bob
</pre>
