# Biomedical Journal Selector / 生物医学智能择刊

一个开放的 Agent Skill：读取完整论文或摘要，评估稿件质量，核验 SCI/SCIE、中文核心、科技核心、CSCD 与正规普刊，并为每本候选期刊分别判断：

- 适合吗；
- 够得着吗；
- 值得投吗；
- 通过编辑初筛并送外审的概率；
- 已送外审后最终接收的概率；
- 从今天提交开始的总体接收概率。

概率是结构化决策辅助估计，不是期刊官方承诺或录用保证。

## 特点

- 全文和摘要两种模式；
- 动态信息要求联网核验、标注年份、来源与核验日期；
- 区分官方数据、第三方统计和投稿者自报；
- 区分北大核心、中国科技核心、CSCD及单位内部目录；
- 冲刺、主投、保底投稿梯队；
- 概率区间、置信度、证据层级及数学一致性检查；
- 不内置会快速过时的期刊名单。

## 仓库结构

```text
SKILL.md
agents/openai.yaml
references/
scripts/probability_check.py
```

## 安装

### Codex 或兼容 Agent Skills 的主机

将本仓库克隆或复制到技能目录，并调用 `$biomedical-journal-selector`。若主机支持 GitHub CLI 的 Skill 预览功能，可先预览仓库后再安装；请以对应主机的当前文档为准。

### WorkBuddy

从 GitHub Releases 下载 `biomedical-journal-selector-workbuddy.zip` 与 `SHA256SUMS`，校验后在 WorkBuddy 的“专家·Skills·Connectors → Skills → 添加 Skill”中上传原始 ZIP。ZIP 根目录直接包含 `SKILL.md`，不要再次套一层文件夹压缩。

## 使用示例

```text
使用 $biomedical-journal-selector 分析这篇全文。我希望投稿 SCI，中科院二区或三区，预算不超过 15000 元，半年内见刊。请核验最新信息，并为每本期刊给出三阶段录用概率。
```

```text
使用 $biomedical-journal-selector 根据摘要做初步择刊。请分别推荐冲刺、主投和保底期刊，并明确哪些判断必须等全文才能确认。
```

## 隐私

未发表论文可能包含敏感知识产权或个人信息。运行本 Skill 时，只向外部搜索服务提交最少必要的主题、设计和方法特征，不上传患者信息、作者身份或完整未发表稿件。

## 发布 WorkBuddy Marketplace

通用 `SKILL.md` 保持 Agent Skills/Codex 兼容；`scripts/package_workbuddy.py` 在打包时加入 WorkBuddy 要求的中英文描述、版本和作者字段。运行 `python3 scripts/package_workbuddy.py` 即可生成可上传 ZIP 与 SHA-256 校验和。Marketplace 发布仍需发布者在 WorkBuddy Open Platform 完成主体认证、测试和审核；详见官方 Open Platform 文档。

## 许可证

MIT License。详见 [LICENSE](LICENSE)。
