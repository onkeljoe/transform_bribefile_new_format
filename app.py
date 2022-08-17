import json
from pathlib import Path

# read file list
bribefiles = [file for file in Path(
    "./oldfiles/").glob("bribe-data-*.json")]
Path("./newfiles").mkdir(parents=True, exist_ok=True)


for fileinfo in bribefiles:
    # read files
    print(fileinfo)
    with open(fileinfo) as json_file:
        data = json.load(json_file)

    # create new format
    for bribe in data["bribedata"]:
        if "reward" not in bribe:
            rewardlist = []
            for fix in bribe.get("fixedreward") or ():
                nextval = {"type": "fixed", "token": fix["token"], "amount": fix["amount"],
                           "isfixed": fix["isfixed"], "percentagethreshold": 0, "rewardcap": 0}
                rewardlist.append(nextval)
            for per in bribe.get("percentreward") or ():
                nextval = {"type": "percent", "token": per["token"], "amount": per["amount"], "isfixed": per["isfixed"],
                           "percentagethreshold": bribe.get("percentagethreshold") or 0, "rewardcap": bribe.get("rewardcap") or 0}
                rewardlist.append(nextval)
            for vote in bribe.get("pervotereward") or ():
                nextval = {"type": "pervote", "token": vote["token"], "amount": vote["amount"],
                           "isfixed": vote["isfixed"], "percentagethreshold": 0, "rewardcap": bribe.get("rewardcap") or 0}
                rewardlist.append(nextval)
            bribe["reward"] = rewardlist
        else:
            print("reward already exists")

    # write copies of files
    with open("./newfiles/" + Path(fileinfo).name, 'w') as outfile:
        json.dump(data, outfile, indent=2, ensure_ascii=False)
