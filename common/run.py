import sys
from os.path import dirname, abspath, join
here = join(dirname(abspath(__file__)), "..")
sys.path.append(here)

from common.mail import SendEmail

send_email = SendEmail()
send_email.construct_html_email()
