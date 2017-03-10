import os
import json

'''
mcstas/mcxtrace configuration.
'''
configuration = {
    "MCCODE_VERSION": '2.3',
    "MCCODE_LIB_DIR": '/usr/share/mcstas/2.3/',
    "MCCODE": 'mcstas',
    "MCRUN": 'mcrun',
    "MCPLOT": 'mcplot-pyqtgraph',
    "MCDISPLAY": 'mcdisplay-webgl',
    "TOOL_NAME": 'mcgui',
    "PARTICLE": 'neutron',
    "BROWSER": 'xdg-open',
}

# Set environment variables according to the above
os.environ["MCSTAS"] = configuration["MCCODE_LIB_DIR"]
os.environ["PATH"] = os.path.join(configuration["MCCODE_LIB_DIR"],"bin") + os.pathsep + os.environ["PATH"]

'''
Compilation, parallelisation etc.
'''
compilation = {
    "CFLAGS": '-g -lm -O2',
    "NEXUSFLAGS": '-DUSE_NEXUS -lNeXus',
    "MPIFLAGS": '-DUSE_MPI -lmpi',
    "CC": 'gcc',
    "MPICC": 'mpicc',
    "MPIRUN": 'mpirun',
    "MPINODES": '4',
}

'''
Platform settings
'''
platform = {
    "EXESUFFIX": 'out',
}

def check_env_vars():
    ''' checks the OS environment variables '''
    global configuration
    global compilation

    # MCCODE_LIB_DIR
    if not os.getenv('MCSTAS_OVERRIDE') is None:
        configuration['MCCODE_LIB_DIR'] = os.getenv('MCSTAS_OVERRIDE')
    # CFLAGS
    if not os.getenv('MCSTAS_CFLAGS_OVERRIDE') is None:
        compilation['CFLAGS'] = os.getenv('MCSTAS_CFLAGS_OVERRIDE')
    # CC
    if not os.getenv('MCSTAS_CC_OVERRIDE') is None:
        compilation['CC'] = os.getenv('MCSTAS_CC_OVERRIDE')
    # MPICC
    if not os.getenv('MCSTAS_MPICC_OVERRIDE') is None:
        compilation['MPICC'] = os.getenv('MCSTAS_MPICC_OVERRIDE')

def load_user_config():
    ''' loads a json user config to the dictionaries in this module '''
    if os.name == 'nt':
        userdir =  os.path.join(os.path.expandvars("$USERPROFILE"),"AppData",configuration['MCCODE'],configuration['MCCODE_VERSION'])
    else:
        userdir =  os.path.join(os.path.expandvars("$HOME"),"." + configuration['MCCODE'],configuration['MCCODE_VERSION'])
    userconfig = os.path.join(userdir,"mccode_config.json")
    
    if not os.path.isfile(userconfig):
        print("user config does not exist: %s" % userconfig)
        return
    
    print("loading user configuration from " + userconfig)
    text = open(userconfig).read()
    obj = json.loads(text)
    global configuration
    configuration = obj['configuration']
    global compilation
    compilation = obj['compilation']
    global platform
    platform = obj['platform']

def save_user_config():
    ''' attempts to save the current values to a local .json file '''
    text = json.dumps({'configuration' : configuration, 'compilation' : compilation, 'platform' : platform})

    if os.name == 'nt':
        homedirconf =  os.path.join(os.path.expandvars("$USERPROFILE"),"AppData",configuration['MCCODE'])
    else:
        homedirconf =  os.path.join(os.path.expandvars("$HOME"),"." + configuration['MCCODE'])

    if not os.path.isdir(homedirconf):
        try:
            os.mkdir(homedirconf)
        except Exception as e:
            print("Directory %s could not be created: %s " % (homedirconf, e.__str__()))
            
    userdir = os.path.join(homedirconf,configuration['MCCODE_VERSION'])
    if not os.path.isdir(userdir):
        try:
            os.mkdir(userdir)
        except Exception as e:
            print("Directory %s could not be created: %s " % (userdir, e.__str__())) 
    userconfig = os.path.join(userdir,"mccode_config.json")
    f = None
    try:
        f = open(str(userconfig), 'w')
        f.write(text)
        print("userconfig saved to %s" % userconfig)
    except Exception as e:
        print("userconfig could not be saved to %s: %s" % (userconfig, e.__str__()))
    finally:
        if f:
            f.close()


def get_options():
    ''' values below are not enforced in the dicts, but probably used to populate certain gui menus '''
    if configuration['MCCODE'] == "mcstas":
        prefix = "mc"
        mcdisplay_lst = [prefix+"display-webgl",
                         prefix+"display-pyqtgraph",
                         prefix+"display-pyqtgraph --tof",
                         prefix+"display-mantid",
                         prefix+"display.pl",
                         prefix+"display.pl --format=Matlab",
                         prefix+"display.pl --format=VRML", 
                         prefix+"display.pl --format=Mantid",
                         prefix+"display-matplotlib"]
    else:
        prefix = "mx"
        mcdisplay_lst = [prefix+"display-webgl",
                         prefix+"display-pyqtgraph",
                         prefix+"display-pyqtgraph --tof",
                         prefix+"display.pl",
                         prefix+"display.pl --format=Matlab",
                         prefix+"display.pl --format=VRML", 
                         prefix+"display-matplotlib"]

    mcrun_lst =     [prefix+"run.pl", prefix+"run"]
    mcplot_lst =    [prefix+"plot-pyqtgraph",prefix+"plot.pl", prefix+"plot.pl --format=Gnuplot", prefix+"plot.pl --format=Matlab",
                     prefix+"plot-matlab"]

    return mcrun_lst, mcplot_lst, mcdisplay_lst

