#Will be excuted by the cron
import sys
from os.path import dirname, abspath, join
here = join(dirname(abspath(__file__)), "..")
sys.path.append(here)

from external_sources.meetup import populate_meetup_data

populate_meetup_data()
