import platform
arch=platform.processor()
if arch == 'x86_64':
    from libfpga.xdma import *
elif arch == 'aarch64':
    from libfpga.mpsoc import *
else:
    print('libfpga : Architecutre %s is not supported' % arch)
