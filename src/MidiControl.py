import  os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import  pygame.midi
import  time
from    SparkClass import *
from    SparkReaderClass import *
from    SparkCommsClass import *

from    MidiConfig import *

from    sys import platform

print()
if platform == "win32":
    #for Windows
    import socket
    print ("Midi Control on Windows")
else:
    #for Raspberry Pi
    import bluetooth
    print ("Midi Control on Raspberry Pi or Linux")

 
#
# Spark presets and options
#

spark_noisegates =  ["bias.noisegate"]
spark_compressors = ["LA2AComp","BlueComp","Compressor","BassComp","BBEOpticalComp"]
spark_drives =      ["Booster","DistortionTS9","Overdrive","Fuzz","ProCoRat","BassBigMuff",
                     "GuitarMuff","MaestroBassmaster","SABdriver"]
spark_amps=         ["RolandJC120","Twin","ADClean","94MatchDCV2","Bassman","AC Boost","Checkmate",
                     "TwoStoneSP50","Deluxe65","Plexi","OverDrivenJM45","OverDrivenLuxVerb",
                     "Bogner","OrangeAD30","AmericanHighGain","SLO100","YJM100","Rectifier",
                     "EVH","SwitchAxeLead","Invader","BE101","Acoustic","AcousticAmpV2","FatAcousticV2",
                     "FlatAcoustic","GK800","Sunny3000","W600","Hammer500"]
spark_modulations = ["Tremolo","ChorusAnalog","Flanger","Phaser","Vibrato01","UniVibe",
                     "Cloner","MiniVibe","Tremolator","TremoloSquare"]
spark_delays =      ["DelayMono","DelayEchoFilt","VintageDelay","DelayReverse",
                     "DelayMultiHead","DelayRe201"]
spark_reverbs =     ["bias.reverb"]

spark_effects =     {"Noisegate":   spark_noisegates, 
                     "Compressor":  spark_compressors,
                     "Drive":       spark_drives,
                     "Amp":         spark_amps, 
                     "Mod":         spark_modulations, 
                     "Delay":       spark_delays, 
                     "Reverb":      spark_reverbs}



effects_current = {"Noisegate": "bias.noisegate", 
                   "Compressor": "LA2AComp",
                   "Drive": "Booster",
                   "Amp": "RolandJC120", 
                   "Mod": "Cloner", 
                   "Delay": "Vintage Delay", 
                   "Reverb": "bias.reverb"}

# check midi command table

def validate_map(map):
    err = 0
    for a_cmd in map:

        cmd = map[a_cmd][0]


        # test all the commands are ok
        if cmd not in ["HardwarePreset","ChangeParam","ChangeEffect","EffectOnOff","ChangePreset"]:
            print (">>> %s is not a valid command to Spark" % cmd)
            err += 1
        
        # check the effect types (not needed for HardwarePreset)
        if cmd in ["ChangeParam","ChangeEffect","EffectOnOff"]:
            eff_type = map[a_cmd][1]
            eff_name = map[a_cmd][2]
            if eff_type not in effects_current:
                print (">>> %s is not a valid effect" % eff_type)
                err += 1
            else:
                if cmd in ["ChangeEffect"]:
                    if eff_name not in spark_effects[eff_type]:
                        print (">>> %s is not a valid effect name" % eff_name)
                        err += 1
        if cmd == "ChangePreset":
            pres = map[a_cmd][1]
            if pres not in spark_presets:
                print (">>> %s is not a valid preset" % pres)
    return err  

    
# Spark communications functions

def send_receive(b):
    comms.send_it(b)
#    a=comms.read_it(100)
    a=comms.get_data()
    
def send_preset(pres):
    for i in pres:
        comms.send_it(i)
        #a=comms.read_it(100)
        a=comms.get_data()
    
    comms.send_it(change_user_preset[0])
    a= comms.get_data()
    #a=comms.read_it(100)
    
def just_send(b):
    comms.send_it(b)

#
# Connect to the Spark
#

print ()
print ("BLUETOOTH TO SPARK")
print ("==================")

 
commands = { 0x80: "NoteOff",
             0x90: "NoteOn",
             0xB0: "CC",
             0xC0: "PgmChg" }
             

# check the commands for basic validity

print ()
print ("Checking the midi command table")

errors = validate_map(midi_map)
if errors > 0:
    print ("Need to fix the midi command table quitting")
    quit()


    
print ("Trying to connect to Spark")

if platform == "win32":
    #for Windows
    comms = SparkComms("bt_socket")
    comms.connect(my_spark)
else:
    #for Raspberry Pi
    comms = SparkComms("bluetooth")
    comms.connect(my_spark)
    
# for later
reader = SparkReadMessage()

print("Sending Silver Ship preset")
msg = SparkMessage()
change_user_preset = msg.change_hardware_preset(0x7f)
b = msg.create_preset(spark_presets["Silver Ship"])
send_preset(b)

#
# Find the Midi device
#

print ()
print ("SETTING UP MIDI")
print ("===============")
print ("Starting MIDI")
pygame.midi.init()    

# list all midi devices
i=-1
for x in range( 0, pygame.midi.get_count() ):
    inf = pygame.midi.get_device_info(x)
    if inf[1]== midi_device_name and inf[2] == 1:
        i = x
 
# open a specific midi device
if i>0:
    inp = pygame.midi.Input(i)
    print ("Found MIDI input")
else:
    print ("Could not find MIDI device")
    quit()
    
# Start the main routine
    
    


# run the event loop

print()
print ("RUNNING THE COMMANDER")
print ("=====================")

while True:
    if inp.poll():

        midi_in =inp.read(1000)
        for midi_data in midi_in:
            mi = midi_data[0]
            m_cmd = (mi[0] & 0xf0)
            m_val = mi[1]
            m_param = 0
            
            if m_cmd in commands:
                m_str = commands[m_cmd] + "-%d" % m_val
            else:
                m_str = ""
                
            m_param_val= mi[2] / 127

            if m_str in midi_map.keys():
                s_cmd = midi_map [m_str]
            else:
                s_cmd = ["None"]
                print ("Unknown midi command %s" % m_str)

            this_cmd = s_cmd[0]
            if this_cmd == "HardwarePreset":
                hw_preset = s_cmd[1]
                print("Change to hw preset %d" % hw_preset)
                b=msg.change_hardware_preset(hw_preset)
                send_receive(b[0])
                
                # so now we need to know what was in that preset
                comms.send_preset_request(hw_preset)
                dat = comms.get_data()
                reader.set_message(dat)
                reader.read_message()
                asdict = eval(reader.python)

                # changed preset so update our local view of it
                pedals = asdict["Pedals"]
                effects_current["Noisegate"]  = pedals[0]["Name"]
                effects_current["Compressor"] = pedals[1]["Name"]
                effects_current["Drive"]      = pedals[2]["Name"]
                effects_current["Amp"]        = pedals[3]["Name"]
                effects_current["Mod"]        = pedals[4]["Name"]
                effects_current["Delay"]      = pedals[5]["Name"]
                effects_current["Reverb"]     = pedals[6]["Name"]                
            elif this_cmd == "ChangeParam":
                effect_type = s_cmd[1]
                current_effect = effects_current[effect_type]
                param_num = s_cmd[2]
                print ("Change %s (%s) param number %d to %f" % (effect_type, current_effect, param_num, m_param_val))
                b=msg.change_effect_parameter(current_effect, param_num, m_param_val)
                just_send(b[0])
            elif this_cmd == "ChangeEffect":
                effect_type = s_cmd[1]
                new_effect = s_cmd[2]
                current_effect = effects_current[effect_type]
                effects_current[effect_type] = new_effect
                print ("Change %s from %s to %s" % (effect_type, current_effect, new_effect))
                b=msg.change_effect(current_effect, new_effect)
                send_receive(b[0])
            elif this_cmd == "EffectOnOff":
                effect_type = s_cmd[1]
                new_value = s_cmd[2]
                current_effect = effects_current[effect_type]
                print ("Change %s (%s) to %s" % (effect_type, current_effect, new_value))
                b=msg.turn_effect_onoff(current_effect, new_value)
                send_receive(b[0])
            elif this_cmd == "ChangePreset":
                new_preset_name = s_cmd[1]
                new_preset = spark_presets[new_preset_name]
                print ("Change to new preset ", new_preset["Name"])
                b = msg.create_preset(new_preset)
                send_preset(b)
                
                pedals = new_preset["Pedals"]
                effects_current["Noisegate"]  = pedals[0]["Name"]
                effects_current["Compressor"] = pedals[1]["Name"]
                effects_current["Drive"]      = pedals[2]["Name"]
                effects_current["Amp"]        = pedals[3]["Name"]
                effects_current["Mod"]        = pedals[4]["Name"]
                effects_current["Delay"]      = pedals[5]["Name"]
                effects_current["Reverb"]     = pedals[6]["Name"]                   
    pygame.time.wait(10)


if cs is not None:
    cs.close()
