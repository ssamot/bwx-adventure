#!/usr/bin/python
# vim: et sw=2 ts=2 sts=2

from advent import *
# for cloud9
from advent import Game, Location, Connection, Object, Animal, Robot, Pet, Player, Verb, Say, SayOnNoun, SayOnSelf, Consumable
from advent import NORTH, SOUTH, EAST, WEST, UP, DOWN, RIGHT, LEFT, IN, OUT, FORWARD, BACK, NORTH_WEST, NORTH_EAST, SOUTH_WEST, SOUTH_EAST, NOT_DIRECTION

# comment this line out to skip the devtools for environments like trinket
#import advent_devtools

# An actor in the game
class SV(Player):

  def __init__(self):
    Player.__init__(self)
    self.add_verb(BaseVerb(self.act_use, 'use'))


  def act_eat(self, actor, noun, words):
    d = actor.location.find_object(actor, noun)
    if not d:
      return False
    t = d[noun]

    if isinstance(t, Food):
      t.consume(actor, noun, words)
      self.set_flag(t.name)
    else:
      self.output("%s can't eat the %s." % (actor.name.capitalize(), noun))

    return True

  def act_use(self, actor, noun, words):
    d = actor.location.find_object(actor, noun)
    if not d:
      return False
    t = d[noun]

    if isinstance(t, Usable):
      t.use(actor, noun, words)
      self.set_flag(t)
    else:
      self.output("%s can't use the %s." % (actor.name.capitalize(), noun))

    return True

class Usable(Object):
  def __init__(self, name, desc, verb, replacement = None):
    Object.__init__(self, name, desc)
    self.verb = verb
    verb.bind_to(self)
    self.use_term = "use"
    self.replacement = replacement

  def use(self, actor, noun, words):
    if not actor.location.replace_object(actor, self.name, self.replacement):
      return False

    self.output("%s %s%s %s." % (actor.name.capitalize(), self.use_term,
                                 actor.verborverbs, self.description))
    self.verb.act(actor, noun, words)
    return True


class BloodExtractor(Usable):
  def __init__(self, name, desc, verb, player):
    Object.__init__(self, name, desc)
    self.verb = verb
    verb.bind_to(self)
    self.use_term = "use"
    self.player = player

  def use(self, actor, noun, words):


    if not game.player.flag(happypills.name):
        self.output("Death from boredom after twelve continous hours of blood transfusion")
        self.player.terminate()
    else:
        self.output("12 hours pass - you gain 10 Acceptatrons, but you now fill depressed. "
                    "You need to find more of these happy pills!")
        game.player.unset_flag(happypills.name)
        self.player.add_to_inventory(Object("Acceptatrons", "10 pure, undiluted acceptatrons"))




    self.verb.act(actor, noun, words)
    return True




game = Game("Non-Compulsory Slaving-Volunteering")



lobby = Location(
"Lobby",

"The heavy smog of the slave-volunteering ship Vromarion is hurting your lungs. "
"Captain must be cheap, air filters are expensive. 'Welcome to cruise-ship Vromarion', a pleasant voice explains. "
"'You are a first generation volunteer. "
"Given a choice of death by thirst and hunger or volunteering for just 56 years,  you chose (out of your own free volition) the later. "
"We start volunteering on the decks at exactly 7am, one hour before robot operations commence. "
"You arrived late, thus there will be no formal induction."
"the transporter to the right will move you to blood operations. You can choose to go right. Please hurry!'", "on")

blood_room = Location(
"Blood donations",
"You are teleported in the middle of what is probably a mile-wide and two-miles long room full of little 'igloos'. Your iCommunicator beams:"
"'Welcome volunteer!  Volunteering in a simple, gentle act of love. "
"We provide 'Happypills50K' for free, please use liberally. Feel free to go in your very own, personal blood room(TM)!'"

, "on")

personal_blood_room = Location(
"Blood Room igloo",
"Your personal blood room is rather spartan; only the bare necessities for 12 hours of happy labour. Your iCommunicator beams:"
"'Lay in bed and volunteer your blood. Have some pills if you want."
, "on")



hero = SV()
game.add_actor(hero)
game.add_location(lobby)
game.add_location(blood_room)

#--------------------------------------------------------------------
game.add_location(personal_blood_room)
happypills = Food("happypills50K",
                       "happypills50K: A pill a day takes the boredom away",
                       Say("Happy pills make me happy!"))
personal_blood_room.add_object(happypills)

happypills = Food("happypills50K",
                       "happypills50K: A pill a day takes the boredom away",
                       Say("Happy pills make me happy!"))

blood_extractor = BloodExtractor("BE50K", "An infernally-looking machine that extracts blood", Say("This looks rather funny...?"), hero)
icommunicator_messages = Object("LocationMessage", "'Did you know you could change your cruise-ship for just 10 more years of volunteering?"
                                                   " Maybe Vromarion is not your thing? Trobatron Megacruises might just be the thing for you'", fixed = True)

personal_blood_room.add_object(icommunicator_messages)
hero.set_location(lobby)



personal_blood_room.add_object(blood_extractor)


game.connect(lobby,blood_room, RIGHT)
game.connect(blood_room,personal_blood_room, IN)



# def update():
#   game.entering_location(lobby)


# # and let's add a test to check the code we wrote above:
test_script = Script("test",
"""
> go right
> go in
> look at LocationMessage
> eat happypills50K
> use BE50K
> use BE50K
> end
""")
hero.add_script(test_script)


game.run()

