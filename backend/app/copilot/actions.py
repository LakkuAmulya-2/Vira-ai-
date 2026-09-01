def propose_actions(message:str,context:dict)->list[dict]:
    m=message.lower();actions=[]
    if any(x in m for x in ["apply","application","deadline"]):
        actions.append({"action_type":"APPLICATION_PLAN","title":"Review application plan","requires_confirmation":False,"payload":{}})
    if any(x in m for x in ["submit","pay","payment","send application"]):
        actions.append({"action_type":"EXTERNAL_ACTION","title":"External submission requires explicit confirmation","requires_confirmation":True,"payload":{"reason":"High-impact external action"}})
    if context.get("applications"):
        actions.append({"action_type":"PROACTIVE_SCAN","title":"Check upcoming deadlines","requires_confirmation":False,"payload":{}})
    return actions
