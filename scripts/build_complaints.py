"""Builds data/complaints.csv from the raw pulls in raw/ plus hand-assigned tags.
Tags were assigned by reading each item. One item per author; duplicates excluded."""
import json, csv, re, collections
ACC = "2026-11-11"
P,M,U = "payer","merchant","unclear"
X = {  # id suffix: (role, intent, support_friction, no_reason_given)
'461422':(P,'payer_refund',0,0),'352725':(P,'payer_refund',0,0),'795778':(M,'login_access',1,0),
'311707':(P,'payer_refund',0,0),'193570':(P,'payer_refund',0,0),'241741':(P,'payer_refund',1,0),
'912532':(P,'payer_refund',1,0),'336708':(M,'settlement_hold',1,1),'658175':(P,'payer_refund',0,0),
'353851':(M,'activation_kyc',0,0),'208450':(M,'other',1,0),'277607':(P,'payer_refund',0,0),
'180027':(P,'payer_refund',0,0),'619234':(P,'payer_refund',0,0),'437771':(P,'payer_refund',0,0),
'378764':(P,'payer_refund',1,0),'454250':(M,'activation_kyc',0,1),'809311':(M,'activation_kyc',0,0),
'489990':(M,'activation_kyc',1,0),'340957':(M,'activation_kyc',0,0),'895571':(M,'account_suspended',0,0),
'211109':(M,'activation_kyc',0,0),'786803':(M,'dispute_chargeback',0,0),'555491':(M,'settlement_hold',1,0),
'615470':(M,'settlement_hold',0,0),'394892':(M,'account_suspended',1,1),'712350':(M,'account_suspended',1,1),
'538163':(M,'account_suspended',0,0),'316886':(M,'account_suspended',0,1),'157587':(M,'account_suspended',0,1),
'472811':(M,'account_suspended',0,1),'150940':(M,'account_suspended',0,0),'953265':(M,'account_suspended',1,1),
'356601':(M,'activation_kyc',1,0),'193625':(P,'payer_refund',0,0),'609277':(M,'activation_kyc',1,0),
'865189':(M,'settlement_delay',0,0),'096636':(M,'settlement_delay',0,0),'680223':(M,'settlement_delay',0,0),
'189784':(M,'settlement_delay',0,0),'865274':(M,'settlement_hold',0,0),'555349':(M,'settlement_delay',0,0),
'492756':(M,'account_suspended',0,1),'540300':(M,'intl_payments',0,0),'019456':(P,'payer_refund',0,0),
'519487':(M,'dispute_chargeback',0,0),'439828':(P,'payer_refund',0,0),'498734':(P,'payer_refund',0,0),
'339438':(P,'payer_refund',0,0),'190535':(M,'account_suspended',1,0),'883816':(M,'support_contact',1,0),
'122260':(M,'activation_kyc',1,0),'447902':(P,'payer_refund',0,0),'137037':(M,'integration_tech',1,0),
'573134':(P,'payer_refund',1,0),'941318':(M,'settlement_delay',1,0),'179726':(P,'payer_refund',1,0),
'478542':(M,'settlement_delay',1,0),'481673':(U,'support_contact',1,0),'261467':(M,'login_access',1,0),
'982978':(M,'account_suspended',0,1),'164397':(P,'payer_refund',1,0),'566865':(M,'account_suspended',1,0),
'504713':(M,'support_contact',1,0),'859490':(M,'support_contact',1,0),
}
PL = {0:(U,'login_access',1,0),1:(P,'payer_refund',1,0),2:(M,'account_suspended',0,0),3:(P,'payer_refund',1,0),
4:(M,'account_suspended',1,1),5:(U,'login_access',0,0),6:(M,'activation_kyc',1,0),7:(U,'other',0,0),
8:(M,'settlement_delay',0,0),9:(M,'intl_payments',0,0),12:(M,'login_access',0,0),13:(U,'login_access',0,0),
14:(P,'payer_refund',1,0),15:(M,'activation_kyc',0,0),16:(M,'activation_kyc',1,0),18:(M,'activation_kyc',1,0),
19:(U,'login_access',0,0),20:(M,'activation_kyc',0,0),21:(M,'activation_kyc',0,0),22:(M,'activation_kyc',0,0),
23:(U,'login_access',0,0),25:(M,'activation_kyc',0,0),26:(U,'support_contact',1,0),27:(M,'settlement_delay',1,0),
28:(M,'login_access',0,0),29:(M,'account_suspended',1,1),31:(M,'activation_kyc',0,0),32:(M,'account_suspended',0,1),
33:(M,'activation_kyc',0,0),34:(P,'payer_refund',0,0),35:(M,'support_contact',1,0),36:(M,'settlement_hold',0,0),
37:(P,'payer_refund',1,0),38:(M,'account_suspended',1,0),39:(U,'login_access',0,0)}
RD = [  # (date, url, who, excerpt, role, intent, sf, nr)
("2025-07-02","https://www.reddit.com/r/smallbusinessindia/comments/1lpo22w/razorpay_settlement_on_hold_issue/","post u/Pretty-Tradition3698","Out of no where they are holding settlements for days and asking for business model, invoices etc.",M,'settlement_hold',0,0),
("2026-08-13","https://www.reddit.com/r/Razorpay_Community/comments/1vndttg/funds_on_hold_compliance/","post u/FindingOtherwise2918","Razorpay flagged 3 payments... asked for customer testimony, shipping info, and invoice... is the ordeal over? Are there any more steps left?",M,'settlement_hold',0,1),
("2025-09-23","https://www.reddit.com/r/Razorpay/comments/1no9ofr/razorpay_kyc_verification_not_done_even_after_one/","post u/Adventurous_Plant232","Razorpay KYC verification not done even after one month. What to do? I have already raised a complaint",M,'activation_kyc',1,0),
("2025-11-05","https://www.reddit.com/r/Razorpay/comments/1ooq9ah/razorpay_suspended_my_account_and_20000_customer/","post (date = first visible reply)","My account was suddenly suspended for 'review'... payments show as successful... I've raised a support ticket and emailed them, but haven't received a clear update",M,'account_suspended',1,1),
("2025-11-05","https://www.reddit.com/r/Razorpay/comments/1ooq9ah/razorpay_suspended_my_account_and_20000_customer/","comment u/boxhell","They suspended my account. And my 16000 is stuck. They have said my account is now closed and money would be given after 120 days.",M,'account_suspended',0,0),
("2025-11-05","https://www.reddit.com/r/Razorpay/comments/1ooq9ah/razorpay_suspended_my_account_and_20000_customer/","comment u/Realistic-Plant3957","They paused the settlement. It's so hard to reach them; I created a support ticket, and they take so much time to respond.",M,'settlement_hold',1,0),
("2025-12-03","https://www.reddit.com/r/Razorpay/comments/1ooq9ah/razorpay_suspended_my_account_and_20000_customer/","comment u/Ill-Olive-8469","After 11 days of registration... my RazorPay account is suspended due to some suspicious activities... no customer care number, no support service",M,'account_suspended',1,1),
("2025-12-05","https://www.reddit.com/r/india/comments/1647v4a/funds_stuck_in_razorpay/","comment u/Middle_Goal5573","Razorpay accepted 3 payments on the last day of November, but it has yet to deposit the amount in my bank. There is no support number, their chatbot is horrible.",M,'settlement_delay',1,0),
("2025-10-31","https://www.reddit.com/r/StartUpIndia/comments/1okk2t4/razorpay_settlement_of_txn_not_received/","post (date = first visible reply)","It has been two days since the customer paid... shown as captured but still not 'settled'. Razorpay is not responding to emails either.",M,'settlement_delay',1,0),
("2024-10-15","https://www.reddit.com/r/indianstartups/comments/1g3bye3/using_razorpay_has_been_a_complete_disaster_for/","post (date = first visible reply)","My funds were inexplicably blocked... a continuous loop of 'we need this' or 'we need that'... even after providing everything",M,'settlement_hold',1,0),
("2024-10-15","https://www.reddit.com/r/indianstartups/comments/1g3bye3/using_razorpay_has_been_a_complete_disaster_for/","comment u/bluemountaintree","They blocked my account simply because i used it to carry a few small test transactions",M,'account_suspended',0,1),
]
def redact(s):
    s=re.sub(r'\S+@\S+\.\w+','[email]',s)
    s=re.sub(r'\b[A-Za-z0-9]{14}\b(?=.*)',lambda m:'[id]' if re.search(r'\d',m.group()) and re.search(r'[A-Z]',m.group()) else m.group(),s)
    s=re.sub(r'\+?\d[\d\s-]{8,}\d','[number]',s)
    s=re.sub(r'https://t\.co/\S+','',s)
    return re.sub(r'\s+',' ',s.replace('&amp;','&')).strip()
def clip(s,n=240): return s if len(s)<=n else s[:n].rsplit(' ',1)[0]+'…'
rows=[]
for r in json.load(open('../raw/x_all.json')):
    k=r['id'][-6:]
    if k in X:
        ro,it,sf,nr=X[k]; rows.append(['X',r['date'],r['url'],ro,it,sf,nr,clip(redact(r['text']))])
low=[x for x in json.load(open('../raw/play_newest.json')) if x['score']<=2 and len(x['text'])>=60][:40]
for i,(ro,it,sf,nr) in PL.items():
    x=low[i]; rows.append([f"Play Store ({x['score']}★)",x['date'][:10],"https://play.google.com/store/apps/details?id=com.razorpay.payments.app&reviewId="+x['id'],ro,it,sf,nr,clip(redact(x['text']))])
for d,u,who,ex,ro,it,sf,nr in RD: rows.append([f"Reddit ({who})",d,u,ro,it,sf,nr,ex])
with open('../data/complaints.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['n','source','date','url','author_role','intent','support_friction','no_reason_given','excerpt','accessed'])
    for i,r in enumerate(rows,1): w.writerow([i]+r+[ACC])
S=collections.Counter(r[0].split(' ')[0] for r in rows); print('total',len(rows),dict(S))
print('roles',collections.Counter(r[3] for r in rows))
print('intent all',collections.Counter(r[4] for r in rows).most_common())
mer=[r for r in rows if r[3]=='merchant']
print('merchant intents',len(mer),collections.Counter(r[4] for r in mer).most_common())
print('support_friction all',sum(r[5] for r in rows),'merchant',sum(r[5] for r in mer))
print('no_reason merchant',sum(r[6] for r in mer), 'of suspend/hold/reject', sum(1 for r in mer if r[4] in('account_suspended','settlement_hold','activation_kyc')))
ah=[r for r in mer if r[4] in('account_suspended','settlement_hold')]; print('hold+susp',len(ah),'noreason',sum(r[6] for r in ah))
print('dates',min(r[1] for r in rows),max(r[1] for r in rows))
for src in ['X','Play','Reddit']:
    sub=[r for r in rows if r[0].startswith(src)]; print(src,min(r[1] for r in sub),max(r[1] for r in sub))
