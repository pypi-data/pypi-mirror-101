# ircbgp

Small script to simulate bgp with students using IRC.


# What is needed

You need to design a topology and for each link between two ASes create an irc channel on a irc server.
You can now assign AS numbers to students and let them either interact with this bot and/or each other.

Kudos to Tobias Fiebig, who used this concept in a lecture and gave the inspiration to write a bot for
this.


# Why?

Just a proof of concept, however, the bot could already be useful to replace participants leaving the
lecture early.

# Usage

Use screen to start multiple bots in parallel or use separate terminals:

```
   $ screen ircbgpbot Florian 1 '#as1-as2'
   $ screen ircbgpbot Claudia 2 '#as1-as2,#as2-as3'
   $ screen ircbgpbot Tobias  3 '#as2-as3'
```

This would start three bots connecting to a irc server running on localhost, names Florian, Claudia and Tobias.
All three will start announcing their nickname and AS number (1-3) to the channels listed as last parameters.

Received announcements will then be forwarded to all other channels and the own AS-number appended(!) to the aspath.

Note: We are of course NOT implementing the whole BGP protocol and do not support things like withdrawals.

# Testing convergence

The command msg:nickname:Text message can be used to send a message to the nickname given, if it was announced
by somebody in the 'network'. Bots will print the message as debugging output.


