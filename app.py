from money_matrix import money_matrix_panel
from reporting5 import reporting5_panel
from slack import slack_panel
from cid10 import get10_cid

money_matrix_panel()    # Open and get ready MM panel for trans.
reporting5_panel()      # Open and get ready Reporting5 panel for trans.
slack_panel()           # Open Slack
get10_cid()             # Copy customer id from MM and past it in Reporting5.
