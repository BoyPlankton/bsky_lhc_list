import sys
import yaml
import numpy as np
from atproto import Client
from datetime import datetime

def syncList(username, password, repo_did, list_did, handles):
  client = Client()
  client.login(session_string=session_string)
  client.login(username, password)

  list_results = client.app.bsky.graph.get_list(params={"list":list_did})

  list_dids = [x.subject.did for x in list_results.items]

  profile_results = client.get_profiles(actors=handles)

  handle_dids = [x.did for x in profile_results.profiles]

  arr1 = np.array(list_dids)
  arr2 = np.array(handle_dids)

  to_add = np.setdiff1d(arr2, arr1)
  to_remove = np.setdiff1d(arr1, arr2)

  for x in to_add:
    print(f"adding: {x}")
    client.app.bsky.graph.listitem.create(repo=repo_did, record={
      "subject": x,
      "list": list_did,
      "createdAt": datetime.utcnow().isoformat() + "Z"
    })

  for x in [x.uri.split('/')[4] for x in list_results.items if x.subject.did in to_remove]:
    print(f"removing: {x}")
    client.app.bsky.graph.listitem.delete(repo=repo_did, rkey=x)

def main():
    with open(sys.argv[1], 'r') as stream:
        data_loaded = yaml.safe_load(stream)

    syncList(
        sys.argv[2], 
        sys.argv[3], 
        data_loaded['repo_did'], 
        data_loaded['list_did'], 
        data_loaded['handles']
    )
    
if __name__ == "__main__":
    main()

