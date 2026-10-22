"""Prepare a design brief and unreviewed checklist. Python stdlib; no image API."""
import argparse,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def prepare(data):
    if not isinstance(data,dict):raise ValueError('Input must be a JSON object')
    for key in ('material','brand','size'):
        if not isinstance(data.get(key),str) or not data[key].strip():raise ValueError(f'{key}: non-empty text required')
    copy=data.get('copy')
    if not isinstance(copy,list) or not copy or any(not isinstance(x,str) or not x.strip() for x in copy):raise ValueError('copy: non-empty list of exact text required')
    if data.get('mode','design') not in ('design','plan','review'):raise ValueError('mode: choose design, plan or review')
    if not isinstance(data.get('assumptions',[]),list):raise ValueError('assumptions: list required')
    for key in ('context','requirements','layout','presentation'):
        if key in data and not isinstance(data[key],str):raise ValueError(f'{key}: text required')
    sources=json.loads((ROOT/'references/sources.json').read_text(encoding='utf-8'))
    selected=[x['id'] for x in sources if x.get('role')=='core']
    values=[data['material'],data['brand'],'\n'.join(copy),data['size'],data.get('requirements') or '未提供额外要求；不要自行添加性能或认证。']
    prompt=(ROOT/'references/prompt-template.txt').read_text(encoding='utf-8')
    for k,v in zip(('物料类型','品牌或产品','主要文案','尺寸','其他要求'),values):prompt=prompt.replace('{{'+k+'}}',v)
    profiles=json.loads((ROOT/'references/prompt-profiles.json').read_text(encoding='utf-8'))
    material=data['material'].lower();profile=next((p for p in profiles if any(k in material for k in p['keywords'])),profiles[-1])
    extra={'使用场景':data.get('context') or '按物料用途判断，避免增加无关场景','构图指令':data.get('layout') or '按主要文案顺序建立主次；清楚分开识别、主体与细节','呈现方式':data.get('presentation') or '平面为完整设计；实体为主要设计面清晰可读的视觉概念','物料适配':profile['guidance']}
    for k,v in extra.items():prompt=prompt.replace('{{'+k+'}}',v)
    brief='\n'.join(['# 设计简报','',f"模式：{data.get('mode','design')}",f"物料：{data['material']}",f"品牌：{data['brand']}",f"尺寸：{data['size']}",f"场景：{data.get('context') or '未提供；执行时说明假设'}",'','## 准确文案',*['- '+x for x in copy],'','## 用户要求',data.get('requirements') or '无额外要求','','## 假设',*['- '+str(x) for x in data.get('assumptions',[])],'','## 待设计决定','按 references/adaptation.md 确定阅读顺序、对齐轴、物料分区、裁切边界、留白与色彩职责。本脚本不替代版式设计。','','## 候选核心证据',', '.join(selected),'查看本地原图后，记录实际采用的 ID。'])
    review={'status':'not_reviewed','evidence_used':[],'checks':[{'dimension':x,'status':'not_verified','evidence':'','revision':''} for x in ['文案与事实','阅读锚点','色彩角色','图形关系','纹理','物料适配','来源与原创']],'production_verified':False}
    return brief,prompt,review

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--input',required=True,type=Path);p.add_argument('--output',required=True,type=Path);a=p.parse_args()
    try:result=prepare(json.loads(a.input.read_text(encoding='utf-8-sig')))
    except (OSError,ValueError) as e:p.error(str(e))
    names=('design-brief.md','prompt.txt','review.json')
    if any((a.output/n).exists() for n in names):p.error('Output exists; choose a new folder to preserve prior work.')
    a.output.mkdir(parents=True,exist_ok=True)
    for n,v in zip(names,result):(a.output/n).write_text(json.dumps(v,ensure_ascii=False,indent=2) if isinstance(v,dict) else v,encoding='utf-8')
    print('Prepared brief, prompt and unreviewed checklist. No image generated or approved.')
if __name__=='__main__':main()
