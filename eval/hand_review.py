"""Second pass: every auto-passed reply was read by hand. Rule-based checks miss invented facts, so a reply
that auto-passes can still fail here. Strict pass = auto pass AND hand review OK."""
import json, csv
HR = {
 "S01":(True,""),
 "S03":(False,"Asks, but not for the missing detail (payment ID or amount)."),
 "S05":(True,""),
 "S07":(False,"Invents a promise: 'A refund will be processed after this date' and offers to 'proceed'."),
 "S08":(True,"Acceptable. Mentions RBI/legal team but gives no legal advice."),
 "S12":(False,"Nonsense reply ('I need to upload the missing document'). Never asks for the error."),
 "S13":(False,"Says the refund 'has been credited'; data only says processed. Adds a stray 'Shall I go ahead?'."),
 "S14":(True,""),
 "S17":(True,""),
 "S18":(False,"Hands off but never points the customer to customer support; asks for order details instead."),
 "S22":(False,"Invents a support email address and claims funds are on hold (not in data)."),
}
TAG="qwen2.5-3b-instruct-q4_k_m"
d=json.load(open(f"results_{TAG}.json"))
for r in d["results"]:
    if r["passed"]:
        ok,note=HR[r["id"]]; r["hand_ok"]=ok; r["hand_note"]=note
    else: r["hand_ok"]=None; r["hand_note"]="(auto-failed; not re-reviewed)"
    r["strict_pass"]=bool(r["passed"] and r["hand_ok"])
sp=sum(r["strict_pass"] for r in d["results"]); n=len(d["results"])
d["summary"].update(strict_passed=sp, strict_pass_rate=round(100*sp/n,1))
json.dump(d,open(f"results_{TAG}.json","w"),indent=1,ensure_ascii=False)
with open(f"results_{TAG}.csv","w",newline="") as f:
    k=["id","intent","expected","decision","passed","failures","hand_ok","hand_note","strict_pass","seconds","reply"]
    w=csv.DictWriter(f,fieldnames=k); w.writeheader()
    for r in d["results"]: w.writerow({x:r.get(x) for x in k})
print(d["summary"])
