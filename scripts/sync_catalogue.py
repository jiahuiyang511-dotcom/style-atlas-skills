"""Render repository navigation from the shared source catalogue."""
import json
from pathlib import Path
from collections import OrderedDict
from html import escape

ROOT = Path(__file__).resolve().parents[1]
START, END = '<!-- style-catalogue:start -->', '<!-- style-catalogue:end -->'

def render(data):
    groups, nodes = OrderedDict(), OrderedDict()
    for item in data['styles']:
        chain = item['classification']['path']
        group = ' / '.join(n['label'] for n in chain)
        groups.setdefault(group, []).append(item)
        for i, node in enumerate(chain):
            key = '/'.join(n['id'] for n in chain[:i+1])
            nodes.setdefault(key, (i, node['label']))
    text = '## 来源目录\n\n'
    def tree(parent=''):
        rendered=''
        for key, (depth, label) in nodes.items():
            if key.rpartition('/')[0]==parent:
                rendered += '  ' * depth + '- ' + label + '\n' + tree(key)
        return rendered
    text += tree()
    text += '\n分类只显示已收录内容。Worlds（S 赛）与 MSI 属于英雄联盟国际赛事下的并列系列；其他赛事、品牌和电影等来源可按实际收录继续登记。\n\n## 选择需要的工具\n\n'
    for group, items in groups.items():
        # Shared MSI proportions prevent longer labels/tags from shrinking thumbnails.
        text += '### ' + group + '\n\n<table width="100%">\n<thead><tr><th width="230">主视觉</th><th width="220">Skill</th><th width="550">关键词</th></tr></thead>\n<tbody>\n'
        for item in items:
            entry = item['skillPath'] + '/SKILL.md'
            entry = escape(entry, quote=True)
            thumb = escape(item['thumbnail'], quote=True)
            name = escape(item['name'], quote=True)
            skill = escape(Path(item['skillPath']).name)
            tags = escape('、'.join(item['tags']))
            text += f'<tr><td width="230"><a href="{entry}"><img src="{thumb}" alt="{name} 原作主视觉" width="160" height="90"></a></td><td width="220"><a href="{entry}">{skill}</a></td><td width="550">{tags}</td></tr>\n'
        text += '</tbody>\n</table>\n\n'
    text += '## 下载\n\n| 来源分类 | 风格 | 独立下载 |\n| --- | --- | --- |\n'
    for group, items in groups.items():
        for item in items:
            link=f'[下载完整 Skill ZIP]({item["skillZip"]})' if item.get('skillZip') else '待发布'
            text += f'| {group} | {item["name"]} | {link} |\n'
    text += '\n[全部发布版本](https://github.com/jiahuiyang511-dotcom/style-atlas-skills/releases) · 各版本附 SHA256SUMS.txt。历史链接保留，每种风格可独立更新版本。\n'
    return text

def sync():
    data = json.loads((ROOT/'catalog.json').read_text('utf-8'))
    p = ROOT/'README.md'; text=p.read_text('utf-8')
    section=START+'\n'+render(data)+'\n'+END
    if START in text and END in text:
        text=text[:text.index(START)]+section+text[text.index(END)+len(END):]
    else:
        begin=text.index('## 选择需要的工具');end=text.index('## 使用', begin)
        text=text[:begin]+section+'\n\n'+text[end:]
    old='这里包含 MSI 2021、2022、2023、2024、2025、2026 六套独立风格 Skill，用于将已提炼的视觉关系应用到具体设计任务。本仓库包含上述六套专属风格 Skill；完整研究包与网站内容生产工作流保留本地。'
    text=text.replace(old,'Style Atlas 按视觉来源组织可复用的设计工具，持续收录赛事、品牌、电影等不同板块。英雄联盟国际赛事是其中一个板块，MSI 是其下的一个赛事系列；当前已收录六套 MSI 风格。完整研究包与网站内容生产工作流保留本地。')
    if '## 维护与扩展' not in text:
        text += '\n## 维护与扩展\n\n来源结构见 [LIBRARY_STRUCTURE.md](LIBRARY_STRUCTURE.md)，机器可读索引见 [catalog.json](catalog.json)。新增风格时登记分类、届次、Skill 路径、原作缩略图及实际下载链接，运行 `python scripts/sync_catalogue.py` 更新本页；打包器直接读取目录索引，无需改写赛事年份清单。已有 Skill 目录、详情网址和历史版本下载链接保留。\n'
    p.write_text(text,encoding='utf-8',newline='\n')

if __name__=='__main__':sync()

