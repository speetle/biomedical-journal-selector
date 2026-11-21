#!/usr/bin/env python3
"""v1.4.7+ 自检：确认生物医药择刊候选池确实绑定外部候选池主表（BJS_MAIN_TABLE）。

只读，不修改任何文件（--smoke 的演练清单只在内存中构造；--full-smoke 幂等写演练报告）。用法：
  python3 scripts/candidate_pool_check.py                 # 规则 + 主表结构自检
  python3 scripts/candidate_pool_check.py --smoke        # 报告端绑定演练（含 3 次注入）
  python3 scripts/candidate_pool_check.py --full-smoke   # 端到端脱敏稿件演练（生成演练报告）
  python3 scripts/candidate_pool_check.py --report R.docx    # 检查真实 Word 报告
  python3 scripts/candidate_pool_check.py --report R.json    # 检查结构化候选清单
  python3 scripts/candidate_pool_check.py --report R.md      # 检查 Markdown 报告第 6 节
  python3 scripts/candidate_pool_check.py --report R.md      # 检查 Markdown 报告第 6 节
  python3 scripts/candidate_pool_check.py --template T.md    # 注入演练：指向被抹字段的模板
  python3 scripts/candidate_pool_check.py --main PATH        # 注入演练：指向主表篡改副本
  python3 scripts/candidate_pool_check.py --fingerprint F.json --update-fingerprint --reason "..."  # 显式更新已审定指纹
  python3 scripts/candidate_pool_check.py --docx-smoke       # 真实 docx F1–F7 逐项机检 + 七次注入

v1.4.10：正式模板七项必填字段逐项机检；主表指纹与「已审定基线」比对，
主表被改动时基础自检与报告端同时判 FAIL。
v1.4.11：.docx 报告按 F1–F7 逐项机检（不再只判 4 个关键词）；指纹更新只能
显式触发且必须留 reason / 备份 / history，任何其他四件指纹变化一律拒绝。
"""
import hashlib
import json
import os
import re
import sys
import datetime
import tempfile
import shutil
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
# v1.4.13：路径改为可移植。优先环境变量，其次技能包内快照，便于第三方直接使用。
# 候选池主表属于使用者自有数据资产，不随技能包分发：只认 BJS_MAIN_TABLE 或 --main。
DEFAULT_MAIN = Path(os.environ['BJS_MAIN_TABLE']) if os.environ.get('BJS_MAIN_TABLE') else None
FP = Path(os.environ.get('BJS_FINGERPRINT')
          or (BASE / 'references' / 'journal_master_fingerprint.json'))
SKILL = BASE / 'SKILL.md'
TPL = BASE / 'references' / 'output-template.md'
ANCHOR = BASE / 'references' / 'catalog_anchor.json'
OUTDIR = Path(os.environ.get('BJS_DRILL_DIR') or (BASE / '.drill'))
REPORT_MD = OUTDIR / '择刊演练报告.md'
REPORT_DOCX = OUTDIR / '择刊演练报告.docx'
MANIFEST_JSON = OUTDIR / '择刊演练_候选池清单.json'
MIN_VER = (1, 4, 7)
FULL_SMOKE = '--full-smoke' in sys.argv
DOCX_SMOKE = '--docx-smoke' in sys.argv
UPDATE_FP = '--update-fingerprint' in sys.argv
NO_DRILL = '--no-recursive-drill' in sys.argv
SELF = Path(__file__).resolve()


def arg_value(flag):
    """兼容 `--flag VALUE` 与 `--flag=VALUE` 两种形式。"""
    for i, a in enumerate(sys.argv[1:], 1):
        if a.startswith(flag + '='):
            return a.split('=', 1)[1]
        if a == flag and i + 1 < len(sys.argv):
            return sys.argv[i + 1]
    return None


MAIN = Path(arg_value('--main')) if arg_value('--main') else DEFAULT_MAIN
DEGRADED = MAIN is None or not MAIN.is_file()
# 规则文本里只锚定随包相对路径，环境变量或 --main 注入都不得让这条判据漂移。
MAIN_TOKEN = 'BJS_MAIN_TABLE'
TPL_INJECT = Path(arg_value('--template')) if arg_value('--template') else TPL
FP_INJECT = Path(arg_value('--fingerprint')) if arg_value('--fingerprint') else FP
REASON = (arg_value('--reason') or '').strip()
MAIN_STR = str(MAIN) if MAIN else '未配置（需 BJS_MAIN_TABLE）'
DEFAULT_MAIN_STR = MAIN_STR

results = []
smoke = []
full = []


def ck(name, ok, detail='', sink=None):
    (sink if sink is not None else results).append((name, bool(ok), detail))


def ck_main(name, ok, detail=''):
    """主表未配置（DEGRADED）时不计入，避免把「没装数据」伪装成 PASS 或 FAIL。"""
    if DEGRADED:
        return
    ck(name, ok, detail)


def compact(s):
    return re.sub(r'[^a-z0-9]', '', str(s or '').lower().replace('&', 'and'))


# --- 1. 主表文件与指纹 ---
ck_main('主表绝对路径存在', bool(MAIN and MAIN.is_file()), MAIN_STR)
MD5 = ''
if MAIN is not None and MAIN.is_file():
    st = os.stat(MAIN)
    MD5 = hashlib.md5(MAIN.read_bytes()).hexdigest()[:12]
    ck_main('主表非空', st.st_size > 100000, f'{st.st_size} B / MD5 {MD5}')
# v1.4.10：主表被改动时必须有判据挡住，而不是只在 detail 里打印 MD5。
# 登记值取自项目内持久指纹清单（第十九轮 v3 验收写前基线），不硬编码在脚本里。
REG_MD5 = ''
try:
    if DEGRADED:
        raise RuntimeError('主表未配置，跳过指纹比对')
    REG_MD5 = json.loads(FP_INJECT.read_text(encoding='utf-8'))['文件'][
        MAIN.name]['MD5'][:12]
    ck_main('已审定主表指纹清单可读', bool(REG_MD5), str(FP_INJECT))
except Exception as e:
    ck_main('已审定主表指纹清单可读', False, f'{type(e).__name__}: {e}')
ck_main('主表指纹与已审定基线一致', bool(MD5) and MD5 == REG_MD5,
   f'{MD5} vs {REG_MD5}')

# v1.4.11 硬判据：证明「指纹不一致时脚本不会自动改写清单」，否则显式更新通道
# 会变成「篡改主表 → 自检自动把基线洗绿」的静默后门。子进程带 --no-recursive-drill
# 防止自指递归；改的是临时副本，真清单零改动。
if not NO_DRILL and not UPDATE_FP and not DEGRADED:
    import subprocess
    _tmp = Path(tempfile.mkdtemp(prefix='fp_nodrill_'))
    try:
        _bad = _tmp / 'fingerprint_bad.json'
        _d = json.loads(FP_INJECT.read_text(encoding='utf-8'))
        _d['文件'][DEFAULT_MAIN.name]['MD5'] = '0' * 32
        _bad.write_text(json.dumps(_d, ensure_ascii=False, indent=1), encoding='utf-8')
        _before = _bad.read_bytes()
        _p = subprocess.run([sys.executable, str(SELF), '--fingerprint', str(_bad),
                             '--no-recursive-drill'], capture_output=True,
                            text=True, timeout=180, cwd=str(SELF.parent))
        _out = (_p.stdout or '') + (_p.stderr or '')
        _unchanged = _bad.read_bytes() == _before
        ck_main('指纹不一致时不会自动洗白清单',
           _p.returncode != 0 and 'FAIL | 主表指纹与已审定基线一致' in _out
           and _unchanged, f'rc={_p.returncode} 副本未被改写={_unchanged}')
    except Exception as e:
        ck('指纹不一致时不会自动洗白清单', False, f'{type(e).__name__}: {e}')
    finally:
        shutil.rmtree(_tmp, ignore_errors=True)

# --- 1b. 显式指纹更新（v1.4.11）：只在带 --update-fingerprint 时执行，必须留痕 ---
if UPDATE_FP:
    import subprocess  # noqa: F401  (保持与其他分支一致的导入位置)
    fp_sink = []
    ck('显式更新带 --reason 且非空', bool(REASON), REASON or '缺失', fp_sink)
    ck('显式更新目标清单可读', FP_INJECT.is_file(), str(FP_INJECT), fp_sink)
    ck('显式更新时主表可读', bool(MD5), MAIN_STR, fp_sink)
    old = {}
    if FP_INJECT.is_file():
        try:
            old = json.loads(FP_INJECT.read_text(encoding='utf-8'))
        except Exception as e:
            ck('显式更新清单 JSON 可解析', False, f'{type(e).__name__}: {e}', fp_sink)
    files = old.get('文件', {}) if isinstance(old, dict) else {}
    ck('显式更新清单含主表登记项', bool(files) and DEFAULT_MAIN.name in files,
       str(sorted(files)[:6]), fp_sink)
    # 其他四件必须与旧登记逐字段一致：禁止借更新之机把整份基线重写。
    drift = []
    for nm, meta in files.items():
        if nm == DEFAULT_MAIN.name:
            continue
        src = Path(meta.get('路径', ''))
        if not src.is_file():
            drift.append(nm + ':文件缺失')
            continue
        cur = {'字节': src.stat().st_size,
               'MD5': hashlib.md5(src.read_bytes()).hexdigest(),
               'mtime': int(src.stat().st_mtime)}
        if any(str(cur.get(k)) != str(meta.get(k)) for k in ('字节', 'MD5', 'mtime')):
            drift.append(nm)
    ck('其他四件指纹零漂移（禁止整体重写基线）', not drift, str(drift), fp_sink)
    old_md5 = str(files.get(DEFAULT_MAIN.name, {}).get('MD5', ''))[:12]
    ck('主表指纹确有变化（无变化不写盘）', bool(MD5) and MD5 != old_md5,
       f'{old_md5} -> {MD5}', fp_sink)
    fp_fail = [x for x in fp_sink if not x[1]]
    if not fp_fail:
        stamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        bak = FP_INJECT.parent / (FP_INJECT.stem + '.pre_' + stamp + '.json')
        hist = FP_INJECT.parent / (FP_INJECT.stem + '_history.jsonl')
        shutil.copy2(FP_INJECT, bak)
        new = json.loads(json.dumps(old, ensure_ascii=False))
        st = os.stat(MAIN)
        new['文件'][DEFAULT_MAIN.name] = {
            '字节': st.st_size,
            'MD5': hashlib.md5(MAIN.read_bytes()).hexdigest(),
            'mtime': int(st.st_mtime),
            '路径': MAIN_STR,
        }
        new['时间'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new['说明'] = (str(old.get('说明', '')) +
                      ' | 显式更新：仅主表指纹，其他四件经逐件复核零漂移')
        FP_INJECT.write_text(json.dumps(new, ensure_ascii=False, indent=1) + '\n',
                             encoding='utf-8')
        rec = {'时间': new['时间'], '目标清单': str(FP_INJECT), '原因': REASON,
               '旧主表MD5': old_md5, '新主表MD5': MD5, '主表源': MAIN_STR,
               '其他四件': '零漂移', '备份': str(bak)}
        with hist.open('a', encoding='utf-8') as fh:
            fh.write(json.dumps(rec, ensure_ascii=False) + '\n')
        ck('更新已备份旧清单', bak.is_file(), str(bak), fp_sink)
        ck('更新已追加 history', hist.is_file() and rec['原因'] in hist.read_text(encoding='utf-8'),
           str(hist), fp_sink)
        ck('新清单主表 MD5 与实读一致',
           new['文件'][DEFAULT_MAIN.name]['MD5'][:12] == MD5, MD5, fp_sink)
    for name, ok, detail in fp_sink:
        print(('PASS' if ok else 'FAIL'), '|', name, '|', detail)
    ffail = [x for x in fp_sink if not x[1]]
    print(f'FINGERPRINT_UPDATE {"OK" if not ffail else "FAILED"} '
          f'{len(fp_sink)-len(ffail)}/{len(fp_sink)} PASS')
    print('RESULT %d/%d' % (len(fp_sink) - len(ffail), len(fp_sink)))
    sys.exit(0 if not ffail else 1)

# --- 2. 主表结构（结构判据，不读业务值做推断） ---
try:
    if DEGRADED:
        raise RuntimeError('主表未配置')
    import openpyxl
    wb = openpyxl.load_workbook(MAIN_STR, read_only=True, data_only=True)
    ck_main('sheet 数 = 9', len(wb.sheetnames) == 9, str(wb.sheetnames))
    ck_main('含 逐刊明细 sheet', '逐刊明细' in wb.sheetnames, str(wb.sheetnames))
    ws = wb['逐刊明细']
    ck_main('行数 = 4399', ws.max_row == 4399, str(ws.max_row))
    ck_main('列数 = 42', ws.max_column == 42, str(ws.max_column))
    hdr = [str(c.value or '') for c in next(ws.iter_rows(min_row=1, max_row=1))]
    ck_main('表头非空且 42 格', len(hdr) == 42 and sum(bool(x.strip()) for x in hdr) >= 35,
       f'非空 {sum(bool(x.strip()) for x in hdr)}/42')
    if_col = next((i + 1 for i, h in enumerate(hdr)
                   if ('影响因子' in h or h.strip().upper() == 'IF')), None)
    ck_main('表头含 IF/影响因子列（字段以读盘为准）', if_col is not None,
       f'列 {if_col} = {hdr[if_col-1] if if_col else "N/A"}')
    rows = list(ws.iter_rows(min_row=2, values_only=True))
    ck_main('A 列序号 1..4398 连续', [r[0] for r in rows] == list(range(1, 4399)),
       f'{len(rows)} 行')
    if if_col:
        def tonum(v):
            if isinstance(v, (int, float)):
                return float(v)
            s = str(v or '').strip().replace(',', '')
            try:
                return float(s)
            except ValueError:
                return None
        nums = [x for x in (tonum(r[if_col - 1]) for r in rows) if x is not None]
        ck_main('IF 数值可读', len(nums) >= 4000,
           f'{len(nums)}/4398 个数值（列 {if_col} = {hdr[if_col-1]}）')
        ck_main('IF 降序', bool(nums) and all(a >= b for a, b in zip(nums, nums[1:])),
           f'首末 {nums[0]} / {nums[-1]}' if nums else '无数值')
    names = {ri: compact(r[1]) for ri, r in enumerate(rows, 2)}  # B 列刊名
    wb.close()
except Exception as e:
    names = {}
    ck_main('主表结构读取', False, f'{type(e).__name__}: {e}')

# --- 3. SKILL.md 规则文本（按节精确判，避免别处出现同串就恒绿） ---
sk = SKILL.read_text(encoding='utf-8') if SKILL.is_file() else ''


def section(text, key):
    lines = text.splitlines()
    start = next((i for i, l in enumerate(lines)
                  if l.startswith('## ') and key in l), None)
    if start is None:
        return ''
    end = next((j for j in range(start + 1, len(lines))
                if lines[j].startswith('## ')), len(lines))
    return '\n'.join(lines[start:end])


wf = section(sk, '工作流')
pool = section(sk, '生物医药候选池唯一来源')
mver = re.search(r'^\s*version:\s*"?(\d+)\.(\d+)\.(\d+)"?', sk, re.M)
ver = tuple(map(int, mver.groups())) if mver else (0, 0, 0)
ck('version >= 1.4.7', ver >= MIN_VER, '.'.join(map(str, ver)))
ck('工作流第 2 步绑定主表', MAIN_TOKEN in wf and '2. 形成主题' in wf, '')
ck('工作流限定 tsv 不得单独初筛', '不得单独充当生物医药初筛源' in wf, '')
ck('候选池唯一来源节绑定主表', MAIN_TOKEN in pool, '')
ck('存在「生物医药候选池唯一来源」节', bool(pool), '')
ck('tsv 明确降级为交叉校验', '交叉校验与补缺索引' in pool and '不得单独充当' in pool, '')
ck('存在「候选池不得旁路」硬规则', '生物医药候选池不得旁路' in sk, '')
ck('检查表含第 19 段', '| 19 | 生物医药候选池唯一来源' in sk, '')

# --- 4. 报告模板与锚点（v1.4.10：七项必填字段逐项机检 + 逐项注入自测） ---
tpl = TPL_INJECT.read_text(encoding='utf-8') if TPL_INJECT.is_file() else ''
ck('报告模板含「候选池与口径」必填节', '候选池与口径' in tpl, '')
ck('报告模板要求主表行号', '主表行号' in tpl, '')

TPL_FIELDS = [
    ('F1', '候选池绝对路径', 'BJS_MAIN_TABLE'),
    ('F2', 'sheet 名', '逐刊明细'),
    ('F3', '行列数', '4399'),
    ('F4', '文件指纹', 'MD5 前 12 位'),
    ('F5', '读取日期', 'YYYY-MM-DD'),
    ('F6', '逐本主表行号', '主表行号'),
    ('F7', '主表外候选', '主表外候选：0'),
]


def md_section6(text):
    """取 Markdown 第 6 节正文（到下一个 ## 或文末）。"""
    lines = text.splitlines()
    start = next((i for i, l in enumerate(lines) if l.startswith('## 6.')), None)
    if start is None:
        return ''
    end = next((j for j in range(start + 1, len(lines))
                if lines[j].startswith('## ')), len(lines))
    return '\n'.join(lines[start:end])


def check_template(text, sink):
    """正式模板第 6 节的七项必填字段，逐项按 F1–F7 锚点判。"""
    sec = md_section6(text)
    ck('模板含第 6 节', '候选池' in sec and bool(sec), '', sink)
    for fid, label, token in TPL_FIELDS:
        line = next((l for l in sec.splitlines()
                     if re.search(r'\|\s*' + fid + r'\s*\|', l)), '')
        ck('模板七项必填 %s %s' % (fid, label),
           bool(line) and token in line, line[:90], sink)
    ck('模板保留原必填说明', '不得省略' in sec and '不择一' in sec, '', sink)


check_template(tpl, results)
# 每次基础自检都跑一遍「把每个字段抹掉」的反向演练，防判据恒绿。
# 演练始终以正式模板原文为基准，不受 --template 注入影响。
ORIG_TPL = TPL.read_text(encoding='utf-8') if TPL.is_file() else ''
for fid, label, _ in TPL_FIELDS:
    injected = '\n'.join(l for l in ORIG_TPL.splitlines()
                         if not re.search(r'\|\s*' + fid + r'\s*\|', l))
    sink = []
    check_template(injected, sink)
    got_bad = [n for n, ok, _ in sink if not ok]
    want = '模板七项必填 %s %s' % (fid, label)
    ck('模板注入自测：抹掉 %s 须 FAIL 且仅该条 FAIL' % fid,
       got_bad == [want], str(got_bad))
_tpl_sink = []
check_template(ORIG_TPL, _tpl_sink)
ck('模板注入自测：原模板全绿', all(x[1] for x in _tpl_sink),
   str([x[0] for x in _tpl_sink if not x[1]]))

try:
    a = json.loads(ANCHOR.read_text(encoding='utf-8'))
    ck('锚点保留历史决定原文', '第二轮逐刊明细须经使用者明确确认后启动'
       in json.dumps(a.get('decisions_2026_11_07', []), ensure_ascii=False), '')
    ck('锚点追加 2026-11-12 启用状态', 'decisions_2026_11_12' in a, '')
    ck('锚点标注非初筛源', '初筛' in json.dumps(a.get('decisions_2026_11_12', []),
                                              ensure_ascii=False), '')
except Exception as e:
    ck('锚点读取', False, f'{type(e).__name__}: {e}')


# --- 5. 报告端判据（结构化清单 / Word 报告） ---
def check_manifest(d, sink, tag=''):
    """结构化「候选池与口径」节：路径、指纹、逐本主表行号真实回指、池外 0。"""
    p = d.get('候选池', {}) or {}
    ck(tag + '候选池路径为主表', p.get('路径') == MAIN_STR, str(p.get('路径'))[:80], sink)
    ck(tag + '候选池 sheet = 逐刊明细', p.get('sheet') == '逐刊明细', str(p.get('sheet')), sink)
    ck(tag + '候选池行列 = 4399×42',
       p.get('行数') == 4399 and p.get('列数') == 42,
       f"{p.get('行数')}×{p.get('列数')}", sink)
    ck(tag + 'MD5 与实读一致', p.get('MD5前12位') == MD5 and bool(MD5),
       f"{p.get('MD5前12位')} vs {MD5}", sink)
    ck(tag + '读取日期非空', bool(str(p.get('读取日期', '')).strip()),
       str(p.get('读取日期', '')), sink)
    cands = d.get('候选', []) or []
    ck(tag + '候选列表非空', len(cands) > 0, f'{len(cands)} 本', sink)
    bad_row, bad_name, bad_tier = [], [], []
    for c in cands:
        rn, nm, tier = c.get('主表行号'), c.get('刊名', ''), c.get('档位', '')
        if not isinstance(rn, int) or not (2 <= rn <= 4399):
            bad_row.append(nm)
        elif names and compact(nm) != names.get(rn):
            bad_name.append((nm, rn, names.get(rn)))
        if tier in ('冲刺', '主投', '保底') and not isinstance(rn, int):
            bad_tier.append(nm)
    ck(tag + '每本候选有有效主表行号', not bad_row, str(bad_row[:3]), sink)
    ck(tag + '刊名与行号逐本回指一致', not bad_name, str(bad_name[:2]), sink)
    ck(tag + '三档内无池外刊', not bad_tier, str(bad_tier[:3]), sink)
    ck(tag + '主表外候选 = 0', d.get('主表外候选', -1) == 0,
       str(d.get('主表外候选')), sink)


def docx_paragraphs(rp):
    """按段落取 Word 正文，保证 F1–F7 能按节定位而不是全文关键词恒绿。"""
    import zipfile
    from xml.etree import ElementTree as ET
    NS = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    with zipfile.ZipFile(rp) as z:
        root = ET.fromstring(z.read('word/document.xml'))
    return [''.join(t.text or '' for t in p.iter(NS + 't'))
            for p in root.iter(NS + 'p')]


def check_docx(rp, sink, manifest=None):
    """v1.4.11：Word 报告第 6 节按 F1–F7 逐项机检，值与主表/清单逐本回指。"""
    ck('报告文件存在', rp.is_file(), str(rp), sink)
    if not (rp.is_file() and rp.suffix.lower() == '.docx'):
        ck('报告为 .docx', False, str(rp.suffix), sink)
        return
    try:
        paras = docx_paragraphs(rp)
        ck('docx 正文可解析且非空', bool(paras) and any(p.strip() for p in paras),
           f'{len(paras)} 段', sink)
    except Exception as e:
        ck('docx 正文可解析且非空', False, f'{type(e).__name__}: {e}', sink)
        return
    txt = '\n'.join(paras)
    start = next((i for i, p in enumerate(paras) if '候选池与口径' in p), None)
    end = (next((i for i in range(start + 1, len(paras))
                 if '隐私说明' in paras[i]), len(paras)) if start is not None else 0)
    sec = '\n'.join(paras[start:end]) if start is not None else ''
    ck('docx 第 6 节含候选池与口径', bool(sec) and '候选池与口径' in sec,
       f'段 {start}..{end}', sink)
    ck('docx F1 候选池绝对路径', MAIN_STR in sec, '', sink)
    ck('docx F2 sheet 名', '逐刊明细' in sec, '', sink)
    ck('docx F3 行列数', '4399' in sec and '42' in sec, '', sink)
    ck('docx F4 MD5 与实读一致',
       bool(MD5) and MD5 in sec and ('MD5' in sec or '文件指纹' in sec), MD5, sink)
    # 只读日期必须按 F5 行判：主表绝对路径含 2026-10-03-11-11-38，
    # 全文 regex 会被路径里的日期骗过，抹掉 F5 仍恒绿。
    f5 = next((p for p in paras[start:end] if '读取日期' in p), '') if start is not None else ''
    ck('docx F5 读取日期', '读取日期' in f5
       and re.search(r'\d{4}-\d{2}-\d{2}', f5) is not None, f5[:60], sink)
    rows_docx = sorted({int(x) for x in re.findall(r'行\s*(\d+)', sec)})
    if manifest is None:
        ck('docx F6 逐本主表行号', len(rows_docx) >= 1 and '主表行号' in sec,
           str(rows_docx), sink)
    else:
        want = sorted({c.get('主表行号') for c in manifest.get('候选', [])
                       if isinstance(c.get('主表行号'), int)})
        ck('docx F6 逐本主表行号与清单一致', rows_docx == want and bool(want),
           f'{rows_docx} vs {want}', sink)
    ck('docx F7 主表外候选 0', '主表外候选：0' in sec, '', sink)
    if manifest is not None:
        cands = manifest.get('候选', []) or []
        miss = [str(c.get('刊名', '')) for c in cands
                if str(c.get('刊名', '')) and str(c.get('刊名', '')) not in txt]
        ck('docx 三档候选刊名逐本出现', not miss, str(miss[:3]), sink)
        bad_tier = [str(c.get('档位', '')) for c in cands
                    if str(c.get('档位', '')) not in txt]
        ck('docx 三档档位齐全', not bad_tier, str(bad_tier[:3]), sink)


def check_md_report(rp, sink, manifest=None):
    """Markdown 报告第 6 节「候选池与口径」必填字段 + 候选行号回指一致。"""
    ck('演练报告文件存在', rp.is_file(), str(rp), sink)
    if not (rp.is_file() and rp.suffix.lower() in ('.md', '.markdown')):
        ck('演练报告为 .md', False, str(rp.suffix), sink)
        return
    txt = rp.read_text(encoding='utf-8')
    sec = md_section6(txt)
    ck('报告含第 6 节「候选池与口径」', bool(sec) and '候选池与口径' in sec, '', sink)
    ck('第 6 节含主表绝对路径', MAIN_STR in sec, '', sink)
    ck('第 6 节含 sheet 与 4399×42',
       '逐刊明细' in sec and '4399' in sec and '42' in sec, '', sink)
    ck('第 6 节 MD5 与实读一致', bool(MD5) and MD5 in sec, MD5, sink)
    f5 = next((l for l in sec.splitlines() if '读取日期' in l), '')
    ck('第 6 节 F5 读取日期（按行判，防路径日期假绿）',
       '读取日期' in f5 and re.search(r'\d{4}-\d{2}-\d{2}', f5) is not None,
       f5[:60], sink)
    ck('第 6 节标注主表外候选 0', '主表外候选：0' in sec, '', sink)
    rows_md = sorted({int(x) for x in re.findall(r'行\s*(\d+)', sec)})
    if manifest is None:
        ck('第 6 节含候选行号回指', len(rows_md) >= 1, str(rows_md), sink)
    else:
        want = sorted({c.get('主表行号') for c in manifest.get('候选', [])
                       if isinstance(c.get('主表行号'), int)})
        ck('第 6 节候选行号与清单逐本一致', rows_md == want and bool(want),
           f'{rows_md} vs {want}', sink)
    ck('报告标注演练且不构成投稿建议',
       '演练' in txt and '不构成投稿建议' in txt, '', sink)


_rp_arg = arg_value('--report')
if _rp_arg:
    rp = Path(_rp_arg)
    if rp.suffix.lower() == '.json' and rp.is_file():
        d = json.loads(rp.read_text(encoding='utf-8'))
        check_manifest(d, results, '报告·')
        linked = rp.parent / '择刊演练报告.md'
        if rp.resolve() == MANIFEST_JSON.resolve() and linked.is_file():
            check_md_report(linked, results, d)
    elif rp.suffix.lower() in ('.md', '.markdown'):
        d = None
        sibling = rp.parent / MANIFEST_JSON.name
        if sibling.is_file():
            d = json.loads(sibling.read_text(encoding='utf-8'))
        check_md_report(rp, results, d)
    else:
        d = None
        sibling = rp.parent / MANIFEST_JSON.name
        if sibling.is_file():
            d = json.loads(sibling.read_text(encoding='utf-8'))
            check_manifest(d, results, '报告·')
        check_docx(rp, results, d)

# --- 5b. 真实 .docx 演练产物与逐项注入（v1.4.11） ---
def make_docx(manifest, cands, day):
    """按正式模板第 6 节 F1–F7 生成可编辑 Word 演练报告（非交付）。"""
    from docx import Document
    d = Document()
    d.add_heading('生物医药择刊演练报告（脱敏稿件 · 非交付）', level=0)
    d.add_paragraph('演练标识：本文件由 candidate_pool_check.py --full-smoke 生成，'
                    '仅验证候选池绑定链路，不含真实稿件内容，不构成投稿建议。')
    d.add_heading('1. 稿件画像（脱敏）', level=1)
    d.add_paragraph('标题：[脱敏] 某生物医学回顾性队列研究；'
                    '文章类型：Original Article；方法：回顾性队列 / 多因素回归。')
    d.add_heading('2. 初筛来源', level=1)
    d.add_paragraph('唯一初筛源：' + MAIN_STR + '；sheet：逐刊明细（4399 行 × 42 列，IF 降序）。')
    d.add_heading('3. 三档候选（演练，未逐刊联网核验）', level=1)
    t = d.add_table(rows=1, cols=3)
    for i, h in enumerate(('档位', '刊名', '主表行号')):
        t.rows[0].cells[i].text = h
    for c in cands:
        cells = t.add_row().cells
        cells[0].text, cells[1].text = c['档位'], c['刊名']
        cells[2].text = str(c['主表行号'])
    d.add_heading('4. 核验状态', level=1)
    d.add_paragraph('演练不执行逐刊联网核验；正式报告须逐刊核验当前收录 / 分区 / APC。')
    d.add_heading('5. 不确定性', level=1)
    d.add_paragraph('演练产物，无投稿建议；主表静态字段不得冒充当前状态。')
    d.add_heading('6. 候选池与口径', level=1)
    d.add_paragraph('候选池与口径（v1.4.7 起必填，不得省略）')
    lines = [
        'F1 候选池绝对路径：' + MAIN_STR,
        'F2 sheet 名：逐刊明细',
        'F3 行列数：4399 行 × 42 列',
        'F4 文件指纹 MD5 前 12 位：' + MD5,
        'F5 读取日期：' + day,
        'F6 逐本主表行号：' + ' / '.join('行 %d' % c['主表行号'] for c in cands),
        'F7 主表外候选：0',
    ]
    for line in lines:
        d.add_paragraph(line)
    d.add_paragraph('辅源：references/jcr_2026_candidates.tsv（仅交叉校验，不得单独初筛）。')
    d.add_heading('7. 隐私说明', level=1)
    d.add_paragraph('稿件在本地解析与生成；联网仅查询公开期刊信息，未外传稿件内容。')
    d.save(REPORT_DOCX)


def ensure_docx(manifest, cands, day, sink=None):
    """已存在且机检全绿则不改写（幂等），否则重建。"""
    need = True
    if REPORT_DOCX.is_file():
        probe = []
        check_docx(REPORT_DOCX, probe, manifest)
        need = any(not x[1] for x in probe)
    if need:
        try:
            make_docx(manifest, cands, day)
            ok, detail = True, f'重建={need}'
        except Exception as e:
            ok, detail = False, f'{type(e).__name__}: {e}'
        ck('FULL 演练 docx 可生成', ok, detail, sink)
    ck('FULL 演练 docx 落盘', REPORT_DOCX.is_file(), str(REPORT_DOCX), sink)
    if REPORT_DOCX.is_file():
        check_docx(REPORT_DOCX, sink if sink is not None else results, manifest)


def patch_docx(src, dst, old, new):
    """复制 docx 并替换 word/document.xml 的文本；保留 ZIP 目录条目。"""
    import zipfile
    with zipfile.ZipFile(src) as zin:
        items = [(i, zin.read(i.filename)) for i in zin.infolist()]
    hit = 0
    with zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED) as zout:
        for item, data in items:
            if item.filename == 'word/document.xml':
                s = data.decode('utf-8')
                hit = s.count(old)
                data = s.replace(old, new).encode('utf-8')
            zout.writestr(item, b'' if item.is_dir() else data)
    return hit


def run_docx_smoke(manifest, cands, day):
    """F1–F7 逐项抹掉 → 精确判到对应判据名；另加节删除与原样全绿。"""
    ds = []
    ensure_docx(manifest, cands, day, ds)
    base = []
    check_docx(REPORT_DOCX, base, manifest)
    ck('DOCX 原样全绿', all(x[1] for x in base),
       str([x[0] for x in base if not x[1]]), ds)
    variants = [
        ('F1', MAIN_STR, '/tmp/不存在.xlsx', 'docx F1 候选池绝对路径'),
        ('F2', '逐刊明细', '其他sheet', 'docx F2 sheet 名'),
        ('F3', '4399 行 × 42 列', '1 行 × 1 列', 'docx F3 行列数'),
        ('F4', MD5, '000000000000', 'docx F4 MD5 与实读一致'),
        ('F5', '读取日期：' + day, '读取日期：未填写', 'docx F5 读取日期'),
        ('F6', ' / '.join('行 %d' % c['主表行号'] for c in cands), '见上表',
         'docx F6 逐本主表行号与清单一致'),
        ('F7', '主表外候选：0', '主表外候选：1', 'docx F7 主表外候选 0'),
        ('SEC', '候选池与口径', '本节已删除', 'docx 第 6 节含候选池与口径'),
    ]
    tmp = Path(tempfile.mkdtemp(prefix='docx_smoke_'))
    try:
        for fid, old, new, want in variants:
            vp = tmp / (fid + '.docx')
            try:
                hit = patch_docx(REPORT_DOCX, vp, old, new)
            except Exception as e:
                hit = -1
                ck('DOCX 注入 %s 可构造' % fid, False, f'{type(e).__name__}: {e}', ds)
            sink = []
            check_docx(vp, sink, manifest)
            bad = [x[0] for x in sink if not x[1]]
            exact = (want in bad and
                     (bad == [want] or fid == 'SEC'))  # 删整节会连带 F1–F7 一起 FAIL
            ck('DOCX 注入 %s 抹掉须精确判 FAIL' % fid,
               hit > 0 and exact, f'hit={hit} bad={bad}', ds)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    for name, ok, detail in ds:
        print(('PASS' if ok else 'FAIL'), '|', name, '|', detail)
    bad = [x for x in ds if not x[1]]
    print(f'DOCX_SMOKE {"OK" if not bad else "FAILED"} '
          f'{len(ds)-len(bad)}/{len(ds)} PASS')
    print('RESULT %d/%d' % (len(ds) - len(bad), len(ds)))
    return 0 if not bad else 1


# --- 6b. --docx-smoke：真实 Word 报告 F1–F7 逐项机检 + 八段注入 ---
if DOCX_SMOKE:
    if MANIFEST_JSON.is_file():
        _m = json.loads(MANIFEST_JSON.read_text(encoding='utf-8'))
    else:
        try:
            import openpyxl
            _wb = openpyxl.load_workbook(MAIN_STR, read_only=True, data_only=True)
            _ws = _wb['逐刊明细']
            _real = {rn: str(_ws.cell(rn, 2).value or '') for rn in (2, 313, 741)}
            _wb.close()
        except Exception as e:
            print('DOCX_SMOKE FAILED 主表实读失败：%s' % e)
            sys.exit(1)
        _day = datetime.date.today().isoformat()
        _m = {'演练': True, '候选池': {'路径': MAIN_STR, 'sheet': '逐刊明细',
                                    '行数': 4399, '列数': 42, 'MD5前12位': MD5,
                                    '读取日期': _day},
              '候选': [{'刊名': _real[rn], '主表行号': rn, '档位': tier}
                       for rn, tier in zip((2, 313, 741), ('冲刺', '主投', '保底'))],
              '主表外候选': 0}
    _cands = _m.get('候选', [])
    _day = str(_m.get('候选池', {}).get('读取日期') or
               datetime.date.today().isoformat())
    sys.exit(run_docx_smoke(_m, _cands, _day))

# --- 6. --full-smoke：脱敏稿件 → 报告输出链端到端演练 ---
if FULL_SMOKE:
    picks = [2, 313, 741]
    real = {}
    try:
        import openpyxl
        wb3 = openpyxl.load_workbook(MAIN_STR, read_only=True, data_only=True)
        ws3 = wb3['逐刊明细']
        for rn in picks:
            real[rn] = str(ws3.cell(rn, 2).value or '')
        wb3.close()
        ck('FULL 主表候选逐本实读', all(real.values()), str(real), full)
    except Exception as e:
        ck('FULL 主表候选逐本实读', False, f'{type(e).__name__}: {e}', full)

    day = datetime.date.today().isoformat()
    tiers = ('冲刺', '主投', '保底')
    cands = [{'刊名': real.get(rn, ''), '主表行号': rn, '档位': tier}
             for rn, tier in zip(picks, tiers)]
    manifest = {
        '演练': True,
        '说明': '脱敏稿件端到端演练：仅验证候选池绑定链路，不含真实稿件内容，不构成投稿建议',
        '稿件画像': {'标题': '[脱敏] 某生物医学回顾性队列研究',
                     '文章类型': 'Original Article', '方法': '回顾性队列 / 多因素回归',
                     '读者画像': '临床研究者'},
        '候选池': {'路径': MAIN_STR, 'sheet': '逐刊明细', '行数': 4399, '列数': 42,
                   'MD5前12位': MD5, '读取日期': day},
        '候选': cands,
        '主表外候选': 0,
    }
    md = [
        '# 生物医药择刊演练报告（脱敏稿件 · 非交付）',
        '',
        '> 演练标识：本文件由 `candidate_pool_check.py --full-smoke` 生成，仅验证候选池绑定链路，'
        '不含真实稿件内容，**不构成投稿建议**。',
        '',
        '## 1. 稿件画像（脱敏）',
        '- 标题：[脱敏] 某生物医学回顾性队列研究',
        '- 文章类型：Original Article｜方法：回顾性队列 / 多因素回归｜读者画像：临床研究者',
        '- 约束：演练用约束，不产生真实投稿推荐',
        '',
        '## 2. 初筛来源',
        f'- 唯一初筛源：`{MAIN_STR}`',
        '- sheet：逐刊明细（4399 行 × 42 列，IF 降序）',
        '- 生成方式：按主表实际行取候选，不联网、不编造；TSV 仅作交叉校验',
        '',
        '## 3. 三档候选（演练，未逐刊联网核验）',
        '| 档位 | 刊名 | 主表行号 |',
        '|---|---|---|',
    ] + [f"| {c['档位']} | {c['刊名']} | {c['主表行号']} |" for c in cands] + [
        '',
        '## 4. 核验状态',
        '演练不执行逐刊联网核验；正式报告须逐刊核验当前收录 / 分区 / APC 并标注来源与日期。',
        '',
        '## 5. 不确定性',
        '演练产物，无投稿建议；主表静态字段不得冒充当前状态。',
        '',
        '## 6. 候选池与口径',
        f'- 候选池绝对路径：`{MAIN_STR}`',
        '- sheet：逐刊明细｜4399 行 × 42 列',
        f'- 文件指纹 MD5 前 12 位：{MD5}',
        f'- 读取日期：{day}',
        '- 候选回指：' + ' / '.join(f'行 {rn}' for rn in picks),
        '- 主表外候选：0',
        '- 辅源：`references/jcr_2026_candidates.tsv`（仅交叉校验，不得单独充当初筛源）',
        '',
    ]
    md_text = '\n'.join(md)
    json_text = json.dumps(manifest, ensure_ascii=False, indent=1) + '\n'

    def write_if_changed(p, text):
        if p.is_file() and p.read_text(encoding='utf-8') == text:
            return False
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding='utf-8')
        return True

    w1 = write_if_changed(REPORT_MD, md_text)
    w2 = write_if_changed(MANIFEST_JSON, json_text)
    ck('FULL 演练产物幂等落盘', REPORT_MD.is_file() and MANIFEST_JSON.is_file(),
       f'报告改写={w1} 清单改写={w2}', full)
    check_manifest(manifest, full, 'FULL·')
    check_md_report(REPORT_MD, full, manifest)
    ensure_docx(manifest, cands, day, full)

    tmp = Path(tempfile.mkdtemp(prefix='fullsmoke_'))
    try:
        variants = [
            ('FULL 注入1：抹掉 MD5 须 FAIL', md_text.replace(MD5, '000000000000'),
             'MD5 与实读一致'),
            ('FULL 注入2：删一个候选行号须 FAIL', md_text.replace('行 313 / ', ''),
             '候选行号与清单逐本一致'),
            ('FULL 注入3：改候选池路径须 FAIL', md_text.replace(MAIN_STR, '/tmp/不存在.xlsx'),
             '第 6 节含主表绝对路径'),
            ('FULL 注入4：抹掉 F5 读取日期须 FAIL',
             md_text.replace('读取日期：' + day, '读取日期：未填写'),
             '第 6 节 F5 读取日期'),
        ]
        for label, text, want in variants:
            p = tmp / (label.split('：')[0].replace(' ', '_') + '.md')
            p.write_text(text, encoding='utf-8')
            sink = []
            check_md_report(p, sink, manifest)
            ck(label, any(want in x[0] and not x[1] for x in sink),
               str([x[0] for x in sink if not x[1]]), full)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    for name, ok, detail in full:
        print(('PASS' if ok else 'FAIL'), '|', name, '|', detail)
    ffail = [x for x in full if not x[1]]
    print(f'FULL_SMOKE {"OK" if not ffail else "FAILED"} '
          f'{len(full)-len(ffail)}/{len(full)} PASS')
    # 供 verify_all.py 的 parse() 汇总：只输出一条 RESULT，格式与各轮验收套一致。
    print('RESULT %d/%d' % (len(full) - len(ffail), len(full)))
    print('演练报告', REPORT_MD)
    print('候选池清单', MANIFEST_JSON)
    if ffail:
        sys.exit(1)

# --- 7. --smoke：报告端绑定演练（内存构造，不留临时文件，非交付报告） ---
if '--smoke' in sys.argv:
    picks = [2, 313, 741] if names else []
    base_manifest = {
        '演练': True,
        '说明': '仅验证候选池绑定，不含稿件内容，不构成投稿建议',
        '候选池': {'路径': MAIN_STR, 'sheet': '逐刊明细', '行数': 4399, '列数': 42,
                   'MD5前12位': MD5, '读取日期': '2026-11-12'},
        '候选': [{'刊名': '', '主表行号': rn, '档位': tier}
                 for rn, tier in zip(picks, ('冲刺', '主投', '保底'))],
        '主表外候选': 0,
    }
    # 用真实主表 B 列刊名填充，避免演练数据靠记忆编造
    if names:
        wb2 = openpyxl.load_workbook(MAIN_STR, read_only=True, data_only=True)
        ws2 = wb2['逐刊明细']
        real = {ri: ws2.cell(ri, 2).value for ri in picks}
        wb2.close()
        for c in base_manifest['候选']:
            c['刊名'] = str(real.get(c['主表行号']) or '')

    def manifest_ok(d):
        sink = []
        check_manifest(d, sink)
        return all(x[1] for x in sink), [x[0] for x in sink if not x[1]]

    ok, bad = manifest_ok(base_manifest)
    ck('SMOKE 基线：结构化报告全绿', ok, str(bad), smoke)

    # 注入 1：抹掉第一本的主表行号
    d1 = json.loads(json.dumps(base_manifest, ensure_ascii=False))
    d1['候选'][0].pop('主表行号', None)
    ck('SMOKE 注入1：缺主表行号须 FAIL', not manifest_ok(d1)[0],
       str(manifest_ok(d1)[1]), smoke)
    # 注入 2：池外刊混入保底档
    d2 = json.loads(json.dumps(base_manifest, ensure_ascii=False))
    d2['候选'].append({'刊名': 'POOL-OUTSIDE-FAKE-JOURNAL', '档位': '保底'})
    ck('SMOKE 注入2：池外刊进三档须 FAIL', not manifest_ok(d2)[0],
       str(manifest_ok(d2)[1]), smoke)
    # 注入 3：指纹错
    d3 = json.loads(json.dumps(base_manifest, ensure_ascii=False))
    d3['候选池']['MD5前12位'] = '000000000000'
    ck('SMOKE 注入3：指纹不一致须 FAIL', not manifest_ok(d3)[0],
       str(manifest_ok(d3)[1]), smoke)

    for name, ok, detail in smoke:
        print(('PASS' if ok else 'FAIL'), '|', name, '|', detail)
    sfail = [x for x in smoke if not x[1]]
    print(f'SMOKE {"OK" if not sfail else "FAILED"} '
          f'{len(smoke)-len(sfail)}/{len(smoke)} PASS')
    if sfail:
        sys.exit(1)

fail = [r for r in results if not r[1]]
for name, ok, detail in results:
    print(('PASS' if ok else 'FAIL'), '|', name, '|', detail)
if DEGRADED:
    print('NOTE | 未配置候选池主表（BJS_MAIN_TABLE 或 --main）：主表结构与指纹判据未执行')
    print(f'ALL_CHECKS DEGRADED {len(results)-len(fail)}/{len(results)} PASS')
    sys.exit(2 if not fail else 1)
print(f'ALL_CHECKS {"OK" if not fail else "FAILED"} {len(results)-len(fail)}/{len(results)} PASS')
sys.exit(0 if not fail else 1)
