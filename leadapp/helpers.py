from userapp.models import User, AgentProfile

def get_agent(req_user:User):
    agent_profile = AgentProfile.objects.filter(user = req_user).first()

    return agent_profile