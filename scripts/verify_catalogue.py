"""Verify source catalogue expansion without adding fictional published entries."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile

ROOT=Path(__file__).resolve().parents[1]
def module(name):
    spec=importlib.util.spec_from_file_location(name,ROOT/'scripts'/f'{name}.py')
    loaded=importlib.util.module_from_spec(spec);spec.loader.exec_module(loaded);return loaded

packer=module('package_skills');renderer=module('sync_catalogue')
data=json.loads((ROOT/'catalog.json').read_text('utf-8'))
assert len(packer.catalogue_skills())==len(data['styles'])
fixture=copy.deepcopy(data['styles'][0]);fixture.update(id='worlds-fixture',skillPath='skills/worlds-fixture')
fixture['classification']['path'][-1]={'id':'worlds','label':'Worlds 全球总决赛'}
brand=copy.deepcopy(fixture);brand.update(id='brand-fixture',skillPath='skills/brand-fixture')
brand['classification']['path']=[{'id':'brands','label':'品牌视觉'},{'id':'sample','label':'测试品牌'}]
with tempfile.TemporaryDirectory() as folder:
    temp=Path(folder);packer.ROOT=temp
    for item in (fixture,brand):
        path=temp/item['skillPath'];path.mkdir(parents=True);(path/'SKILL.md').write_text('fixture','utf-8')
    expanded={'styles':[fixture,brand]}
    def save(): (temp/'catalog.json').write_text(json.dumps(expanded),'utf-8')
    save();assert packer.catalogue_skills()==('worlds-fixture','brand-fixture')
    packer.SKILLS=packer.catalogue_skills()
    assert len(packer.package(temp/'packages'))==2
    expanded['styles'].append(copy.deepcopy(fixture));save()
    try:packer.catalogue_skills();raise AssertionError('Duplicate accepted')
    except ValueError:pass
    expanded['styles']=[copy.deepcopy(fixture)];expanded['styles'][0]['skillPath']='skills/../../escape';save()
    try:packer.catalogue_skills();raise AssertionError('Traversal accepted')
    except ValueError:pass
rendered=renderer.render({'styles':[data['styles'][0],brand,fixture]})
assert rendered.index('    - Worlds')<rendered.index('- 品牌视觉')
assert '[brand-fixture]' in rendered
before=(ROOT/'README.md').read_bytes();renderer.sync();assert (ROOT/'README.md').read_bytes()==before
print(json.dumps({'catalogue_entries':len(data['styles']),'generic_packaging':'PASS','duplicate_rejection':'PASS','path_rejection':'PASS','tree_grouping':'PASS','readme_idempotence':'PASS'}))
