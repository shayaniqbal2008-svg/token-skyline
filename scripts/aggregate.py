"""Aggregate Claude Code token usage from ~/.claude/projects into usage.json for Token Skyline."""
import json,glob,os,collections
from datetime import datetime
tz=datetime.now().astimezone().tzinfo  # your local time zone
root=os.path.expanduser('~/.claude/projects')
seen=set(); days=collections.defaultdict(collections.Counter); hours=collections.Counter(); dproj=collections.defaultdict(collections.Counter); dmodel=collections.defaultdict(collections.Counter)
sess=collections.Counter(); sessday={}
for f in glob.glob(root+'/**/*.jsonl',recursive=True):
    rel=os.path.relpath(f,root); p=rel.split('/')[0]
    proj=p.split('-')[-1] or 'other'  # last part of the project folder name
    sub='/subagents/' in f; sid=rel.split('/')[1].replace('.jsonl','')
    for line in open(f,errors='ignore'):
        if '"usage"' not in line: continue
        try: d=json.loads(line)
        except: continue
        m=d.get('message') or {}; u=m.get('usage')
        if not isinstance(u,dict) or not d.get('timestamp'): continue
        key=(m.get('id'),d.get('requestId'))
        if key in seen: continue
        seen.add(key)
        t=datetime.fromisoformat(d['timestamp'].replace('Z','+00:00')).astimezone(tz)
        day=t.strftime('%Y-%m-%d')
        g=lambda k:u.get(k,0) or 0
        inp,out,cw,cr=g('input_tokens'),g('output_tokens'),g('cache_creation_input_tokens'),g('cache_read_input_tokens')
        tot=inp+out+cw+cr
        c=days[day]; c['i']+=inp;c['o']+=out;c['w']+=cw;c['r']+=cr;c['n']+=1
        if sub: c['s']+=tot
        hours[t.hour]+=tot; dproj[day][proj]+=tot
        mod=m.get('model','?').replace('claude-','')
        if mod!='<synthetic>': dmodel[day][mod]+=tot
        sess[sid]+=tot; sessday.setdefault(sid,day)
out={'days':[[k,days[k]['i'],days[k]['o'],days[k]['w'],days[k]['r'],days[k]['n'],days[k]['s'],dict(dproj[k]),dict(dmodel[k])] for k in sorted(days)],'hours':[hours[h] for h in range(24)],'sessions':len(sess),'topSession':max(sess.values()),'topSessionDay':sessday[max(sess,key=sess.get)]}
json.dump(out,open('usage.json','w'),separators=(',',':'))
tot=sum(sum(x[1:5]) for x in out['days']); print('total',tot,'out',sum(x[2] for x in out['days']),'msgs',sum(x[5] for x in out['days']),'sub',sum(x[6] for x in out['days']))
print(out['hours']); print(out['sessions'],out['topSession'],out['topSessionDay'])
for x in out['days']: print(x[0],sum(x[1:5]),x[7])
