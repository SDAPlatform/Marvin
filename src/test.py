from pprint import pprint
from tools.email import MarvinEmailTool
email_tool = MarvinEmailTool('gmail_agent_oauth_client_creds.json')

res = email_tool.read_emails(2)

# pprint(snippets)
# pprint(bodies[1])
