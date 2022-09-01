import json
from pathlib import Path

# False: create files with old and new format included. True: create files with general "reward" only
NEW_FORMAT_ONLY = True

# read file list
bribefiles = [file for file in Path("./oldfiles/").glob("bribe-data-*.json")]
Path("./newfiles").mkdir(parents=True, exist_ok=True)
Path("./newfiles_only_reward").mkdir(parents=True, exist_ok=True)

for fileinfo in bribefiles:
    # read files
    print(fileinfo)
    with open(fileinfo) as json_file:
        data = json.load(json_file)

    # create new format
    for bribe in data["bribedata"]:
        newurl = bribe.get("poolurl") or ""
        bribe["poolurl"] = newurl.replace("#/", "")
        if "reward" not in bribe:
            rewardlist = []
            for fix in bribe.get("fixedreward") or ():
                nextval = {"type": "fixed", "token": fix["token"], "amount": fix["amount"],
                           "isfixed": fix["isfixed"]}
                rewardlist.append(nextval)
            for per in bribe.get("percentreward") or ():
                nextval = {
                    "type": "percent", "token": per["token"], "amount": per["amount"], "isfixed": per["isfixed"]}
                rewardlist.append(nextval)
            for vote in bribe.get("pervotereward") or ():
                nextval = {"type": "pervote", "token": vote["token"], "amount": vote["amount"],
                           "isfixed": vote["isfixed"]}
                rewardlist.append(nextval)
            bribe["reward"] = rewardlist
        else:
            for reward in bribe.get("reward"):
                reward.pop("rewardcap", None)
                reward.pop("percentagethreshold", None)

        # remove old keys, if no longer needed
        if NEW_FORMAT_ONLY:
            bribe.pop("fixedreward", None)
            bribe.pop("percentreward", None)
            bribe.pop("pervotereward", None)
            for reward in bribe.get("reward") or ():
                reward.pop("rewardcap", None)
                reward.pop("percentagethreshold", None)

    # write copies of files
    filepath = "./newfiles_only_reward/" if NEW_FORMAT_ONLY else "./newfiles/"
    with open(filepath + Path(fileinfo).name, 'w') as outfile:
        json.dump(data, outfile, indent=2, ensure_ascii=False)
