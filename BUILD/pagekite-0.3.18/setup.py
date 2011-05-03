#!/usr/bin/env python
#from pagekite.version import VERSION
from distutils.core import setup
import os
import os.path
import sys
from glob import glob


#libpath = "./"
#scriptspath = "%s/scripts" % libpath
#pluginspath = "%s/plugins" % libpath

#########################################################################

setup(name="pagekite",
      version="0.3.18",
      description="PageKite is a system for running publicly visible servers (generally web servers) on machines without a direct connection to the Internet behind restrictive firewalls.",
      author="Bjarni R. Einarsson",
      author_email="bre@pagekite.net",
      url="http://pagekite.net",
      scripts=['pagekite.py'],
#      package_dir={'./': './'},
#      packages=["pagekite"],
      license="GPL v2+",
      long_description="""
PageKite is a system for running publicly visible servers (generally web servers) on machines without a direct connection to the Internet, such as mobile devices or computers behind restrictive firewalls.
Without PageKite, this is a vexingly difficult problem. In spite of the fact that powerful computers and high-speed Internet connections are now the norm in many places, technicalities generally conspire to make servers on home or mobile machines largely unreachable from the wider Internet - and therefore useless.
These technicalities - firewalls, NAT, IP addresses, DNS - are the problems PageKite simplifies and solves.
      """
      )
#      data_files=[
#                  (scriptspath, glob("scripts/*")),
#                  (pluginspath, glob("plugins/*")),
#                  ],
