# 期刊核验与风险审查

## 动态字段

逐刊核验：正式名称、官网、出版社/学会、Aims & Scope、文章类型、Web of Science/SCIE、MEDLINE/PubMed、Scopus、DOAJ 等收录、JIF及年份、JCR类别/分区、中科院分区及版本与大类/小类、OA模式、APC/版面费与币种、主要投稿限制、伦理/注册/数据政策、当前收稿状态、审稿/出版周期、变更/停刊/剔除和风险信息。

每个关键事实记录：结论、年份或版本、核验日期、直接链接、来源类型。优先使用：

1. 期刊、出版社、学会及权威索引数据库；
2. 官方作者指南、收费页、编辑政策；
3. 可信第三方数据库或机构图书馆；
4. 投稿者社区与经验帖。

第三方指标不得冒充 JCR 官方指标。付费或无法访问的数据库不要声称已核验。不同来源冲突时并列呈现并降低置信度。

## 收录双标签

PubMed 可检索、MEDLINE 索引、WoS/SCIE 收录必须分别核验、分别记录，不得合并为一个 SCI 判定。优先用 PubMed 官方 E-utilities `esearch`（db=pubmed，按 ISSN/EISSN 检索文献数）确认该刊在 PubMed 是否有文献；用 `medline[sb]` 子集确认 MEDLINE；NLM FTP 的 `J_Entrez.gz` / `J_Medline.gz` 主表只作离线基线，因含历史停刊与更名刊，不能单独证明当前在版。SCIE 以 Master Journal List 或 JCR 当前状态为准。三者结论冲突时并列报告并降低置信度。

候选池与版本锚点见 [catalog_anchor.json](catalog_anchor.json)。锚点是初筛索引，不能替代本节逐刊核验。

## 相似论文

为重点候选检索近 2–3 年 1–3 篇代表性文章，核验题名、年份、DOI或官方链接。比较疾病/问题、设计、数据、技术路线、样本和文章类型。它只证明范围/读者适配，不证明容易录用。

## 投稿者反馈

分别标记官方周期、第三方统计和投稿者自报。尽量使用多个独立样本，注明数量与时间，讨论幸存者、极端案例和学科差异。单个案例不得支撑普遍结论。

## 风险清单

检查数据库当前收录、指标压制或剔除、异常自引、频繁更名/转手/扩刊、可疑特刊、克隆网站、用户单位不认可名单、最新预警、撤稿与同行评审透明度。历史预警和目录必须注明年份，不能当永久状态。

严格执行 [隐私与本地处理](privacy-local-processing.md)。不向外部服务提交全文、摘要原句、表格、图片、患者信息、作者身份、拒稿信或审稿材料。相似论文检索仅使用宽泛学科词和文章类型，不使用可反查稿件的独特短语。

## 2026-11-08 实测：第三方批量取数的边界与替代源

- LetPub 搜索页 `index.php?page=journalapp&view=search&searchissn=<带连字符 ISSN>` 一次返回 12 列结果行：ISSN、刊名与 journalid、综合评分、IF/h-index/CiteScore、新锐期刊分区表、学科领域、SCI 收录、是否 OA、录用比例、审稿周期、近期文章、查看数。详情页另有 2025-2026 自引率、APC 金额、其他费用、网友分享经验的平均审稿速度与平均录用比例、期刊简介原文、历年预警名单状态。能用列表页就不要逐刊开详情页。
- 平台对单 IP 连续 4–5 次请求即返回 743 字节拦截页（含“请求页面的速度过快”），冷却期长；2 线程 0.9 秒间隔、单线程 0.6 秒间隔均触发。全量 3501 本逐刊抓取不可在单会话完成。`www.letpub.com.cn` 可用，`letpub.com.cn` 常返回 502；本机代理也偶发 502，用 `requests.Session` 连接复用可消除代理侧 502，但不能消除平台限流。拦截页绝不能判为平台未收录。
- 2026-03-24 起原中科院分区表由新锐学术以《新锐期刊分区表》名义发布（xr-scholar.com），预警机制并入分区体系并标注 Under Review；Under Review 是风险跟踪标记，不等同机构发布的预警名单，不得据此无据删刊。官网查询与名单需登录，前端 SPA 资源与 API 未公开，无可靠批量下载通道。
- 官方可批量替代：NLM Catalog efetch（出版社、国家、出版周期、创刊年）；OpenAlex sources（homepage_url、apc_usd、is_oa、国家代码、publisher，可按 50 个 ISSN 批量 filter）；OpenAlex works `group_by=primary_location.source.issn,type`（实际发表类型分布）；OpenAlex topics（收稿范围兜底，必须注明不是官网 Aims & Scope）。
- PubMed 年发文量用 `esearch`（db=pubmed，`"ISSN"[ISSN] OR "EISSN"[ISSN] AND YYYY[dp]`）；抽样验证加括号与不加括号计数一致；0 篇写数字 0，不写“未找到”。无 API key 时实测约 96 条/分钟，3–6 并发与连接复用提升有限，且并发过高会出现 esearchresult 缺失。
- 审稿费、彩图费、超页费、不收录文章类型在 NLM Catalog、OpenAlex、LetPub 均无结构化字段；期刊官网直连抽样可达率不足三成（403 为主）。只能逐刊人工核验官网作者指南，批量阶段写“已核验某几个来源，均未列该项”，不填估算值。

## 2026-11-08 追加：近 1 年文章类型占比的批量取数

- OpenAlex 无 key 请求计入全局共享日预算，耗尽后返回 HTTP 429 `Insufficient budget`，`Retry-After` 可达约 20 小时；`mailto`、降并发、换直连/代理通道均不恢复。group_by 与复杂 filter 同样计入预算。全量 3501 刊长跑前必须先小额探测预算余量，不要跑到中途才发现。
- 替代源 Europe PMC REST `search`（EMBL-EBI 官方，PubMed/MEDLINE 镜像）：`query` 支持 `ISSN:"xxxx-xxxx"`、`FIRST_PDATE:[YYYY-MM-DD TO YYYY-MM-DD]`、`PUB_TYPE:"Review"`、短语 OR 与 `NOT`；`format=json&pageSize=1` 取 `hitCount` 即可做布尔计数，不下载全文。实测 12–16 并发稳定，单请求约 1–3 秒，无日预算限制。
- `resultType=core` 单刊单页可达 3–7 MB、10–60 秒，全量下载过重；`resultType=lite` 单页约 0.8 MB/1000 篇，含 `pubType`（分号分隔字符串）、`title`、`id`，不含摘要。
- ★ 2026-11-08 二次实测修正：按刊逐页取 `lite` 全量**可行且更准**。本池 3501 刊近 1 年约 67 万篇、约 4000 个分页请求，48 并发约 30 分钟跑完。逐篇 `pubType` 判定文章类型远优于布尔 `hitCount` 近似；摘要缺失部分仍用服务器侧 `TITLE_ABS:` 布尔补干/湿实验判定，两者分母要统一。
- 文章类型互斥分类：综述优先（PUB_TYPE Review / Systematic Review / Meta-Analysis），其余按 BIO 词组与 WET 词组的命中/不命中拆成纯生信、生信+湿实验、纯湿实验，剩余为其他。这是关键词启发式，不是人工精读，也不是期刊官网收稿类型；必须逐格注明来源与关键词表。
- Europe PMC 只覆盖 PubMed/MEDLINE/PMC；未被覆盖的期刊在该源下为 0，不等于该刊无发文。与 OpenAlex 口径不可混用。

## 2026-11-08 追加：文章类型判定 v3 口径与两轮核查

- **综述按文章类型字段判定，不靠枚举**：逐篇读 `pubType`，凡类型名含 `review` 即综述，覆盖 `Review`、`review-article`、`systematic-review`、`Systematic Review`、`scoping review` 等全部变体；`meta-analysis` 按学术惯例并入。布尔 `PUB_TYPE:*review*` 实测与精确枚举计数相同，但逐篇可留证、可复算，优先级更高。注意 `book review` 按字面也会落入综述，须在口径中声明。
- **非研究类必须单列**：Editorial / Letter / Comment / Correction / Published Erratum / Retraction / News / Discussion / Expression of Concern / Article-Commentary 等从「其他」中拆出，否则「其他」的含义不纯，占比不可解释。
- **干湿实验用字段限定**：Europe PMC 支持 `TITLE_ABS:"phrase"`；全字段检索会命中 MeSH 词与参考文献（实测同一刊 `"western blot"` 全字段 21 篇、`TITLE_ABS` 19 篇）。检索式还要显式 `NOT` 掉综述与非研究类。
- **分母用逐篇去重记录数**：索引 `hitCount` 与 `cursorMark` 实际取回记录数存在微小差异（抽样可见 8240 vs 8213，约 0.3%）。分母改用 `n_fetched`，并把 `hitCount` 留作交叉校验列，六类占比才能严格合计 100%。
- **两轮核查的最小组合**：① 第一轮＝全量机检，逐行与本地真相源（原始表、各 API 落盘 JSONL）对齐 + 结构/版式/逻辑/禁用符/占位符判据；② 第二轮＝独立复算（不同代码路径重算占比）+ 独立数据源金标准（如 `resultType=core` 的 `pubTypeList` 与 `lite` 的 `pubType` 互验）+ 分层抽样实时回源（Europe PMC 总数、PubMed 年发文量、NLM 收录号、原表 IF）。两轮都要落 JSON 报告与请求 URL。
- **核查判据要区分"真缺陷"与"判据误报"**：初检常见误报来自——原始表用 `N/A` 表示「无印刷版/电子版 ISSN」、第三方字段尾部拼接广告文案、NLM 出版社名尾部标点被 trim、同一 ISSN 在原表对应多个 WoS 门类、取值优先级（详情页 > 列表页 > 旧搜索页）。这些要先诊断再改判据，不能靠放宽阈值掩盖；真正的缺陷（如冻结窗格被改写、已抓数据未回填）必须修文件并复跑。

## 2026-11-08 第五轮：结构变更后的核查与 LetPub 滑动窗口

- **零覆盖列的判据要显式定义**：不是看单元格是否为空，而是看「有效信息覆盖率」——`未找到/待核实`、`N/A`、`已核验…均未列该项` 都算无信息；数字 0 是真实值，算有效（否则占比列会被误删）。删列后必须重排序号、重设冻结窗格与自动筛选、按表头名而非列号重建所有下游脚本与报告。
- **删行后一切按主键对齐**：旧核查脚本若用 `zip(rows, pool)` 假定顺序一致，删行后会整片错位。所有回查改为按 `pool_key`（ISSN/EISSN/刊号三键取并集，兼容纯电子刊 D 列 N/A）定位，再做逐列比对。
- **结构变更必须做「独立重放」**：从变更前的备份表按主键重建映射，逐行逐列验证除声明允许变化的字段外全部一致；同时独立重算每列覆盖率，确认被删列确为 0、保留列 >0。这比只在新表上跑判据更能挡住串位与错列。
- **LetPub 限流是滑动窗口而非固定间隔**：实测单 IP 连续 10 个详情页请求正常（每个约 430 KB），第 11 个起返回 651/639 字节「请求页面的速度过快」并持续拦截；两个 host 轮换、并发 2/4 均不能突破。可行策略＝单线程 1s 间隔 + 每 10 请求主动冷却 22s + 遇拦截短退避 12s，约 6–7 刊/分钟；全量 3000+ 刊需数小时，应限时抓取并如实标注未抓完，绝不能把拦截页记为「平台未收录」。
- **详情页一次可补多列**：`index.php?journalid=<id>&page=journalapp&view=detail` 的表格行含 `2025-2026自引率`、`平均录用比例`、`平均审稿速度`、`《新锐期刊分区表》`、`期刊分区表预警名单`、投稿网址、出版商/国家/周期/年份。解析 `td` 必须用 `get_text()`，用 `str(td)` 会把 HTML 标签混进值。
- **历史报告行不要删，但要标注**：多轮核查报告累积在同一 sheet 时，旧版的「45 列 PASS」会误导读者。在「轮次说明」行写明当前交付行列数与历史行的关系，并给长文本行设置 wrap + 自适应行高。

## 2026-11-08 第六轮：跨 IF 区间扩展、端点级配额、格式零改动交付

- **扩展区间必须与原池严格不重叠**：IF 分段边界写死（如 0.1<=IF<0.5、5<IF<=10 与既有 0.5<=IF<=5），按 ISSN/EISSN/刊名三键去重并显式验证交集为 0；预警剔除与近 1 年零文章剔除各留独立 sheet，行内写明剔除依据。
- **OpenAlex 配额是端点级而非全站级**：共享免费日预算耗尽时，批量 `/sources?filter=issn:` 与 `/works?group_by=` 返回 429 `Insufficient budget`，但单刊 `/sources/issn:XXXX-XXXX` 仍 200 稳定（实测并发 6 全绿，可取官网、APC、is_oa、topics）。长跑前逐端点小额探测，别因一个端点 429 就整线停摆。用替代源顶替某列时，必须在单元格内与口径 sheet 双处标注来源与时间窗差异。
- **LetPub 后台"跑几小时零产出"两大根因**：① 本机代理 ProxyError / 502 空壳页被误判成平台封禁，触发 300–660s 长冷却；② 多进程共用同一滑动窗口限流桶互踩。修法：curl 子进程 + 显式代理出口，严格区分「网络/代理故障（短重试）」与「响应含 请求页面的速度过快（长退避）」；把全部 IF 区间合并成单通道、断点续跑，只写 JSONL 不碰 xlsx。
- **用户手工调过格式且明令"不要动"时，不要往主表追加行**：另建派生表。跨工作簿复制样式必须逐属性（font/fill/border/alignment/number_format/protection），直接搬 `_style` 会因样式表索引不同报错；主表行的原行高按行携带、随排序带走；主表 MD5 全程比对并写进机检判据。
- **派生表的状态/备注列必须由同行真实字段生成**：本轮出现「第 11/18/19/32 列已有 LetPub 值，备注却写 LetPub=未抓取」的自相矛盾，原因是备注读了独立 `status` 字段。改为按实际命中字段名生成状态，无数据才写未抓取。
- **派生表核查要加"原表全行逐格保留"判据**：按主键对齐，除序号列外 42 列全等、差异 0 例；再加行数、IF 降序、序号连续、格式 6 项、剔除名单不在表内。第二轮仍做独立重放 + 分层抽样实时回源 + 金标准抽样。

## 2026-11-08 第七轮：用户要求「不要新建，都合并到同一个表格」

- **派生表不是终点**：即使派生表两轮机检全绿，用户仍可能要求全部并回原表。应默认只维护一个交付文件；确需中间表时明确标为临时并预留合并路径。
- **字节级合并的可行做法**：解析 `sheet1.xml` 的 `sheetData`，把每个 `<row>` 节点当作不可分割单元搬运（行高 `ht` 写在 row 上、样式 `s` 写在 cell 上，会随行自动保留，无需重建行高映射）；只重写 row 的 `r`、cell 的 `r="XX#"`、A 列序号，再按 IF 重排。新行用 `inlineStr`，`sharedStrings.xml` 不动。同步更新 `<dimension>`、`<autoFilter ref>` 与 `workbook.xml` 里 `_xlnm._FilterDatabase` 的范围，三者必须一致。
- **不新建 sheet 也能装下说明信息**：把口径说明追加进已有「口径与来源」、剔除清单追加进已有「无文章剔除清单」、轮次说明追加进已有「两轮核查报告」；只追加行，既有行字节不变，历史报告行保留但必须新增一行写明当前真实行数。
- **合并前先对齐列类型**：原表 IF 列 3236 行全是文本（JCR 原始串），新表是数字。直接合并会产生同列类型混杂，排序/筛选/审计判据全失效；用真相源的原始字符串字段统一，并让审计用 `float()` 解析而非 `isinstance`。
- **字节级合并的完整判据**：原表全行 42 列逐格保留、抽样数百行样式逐格、原行行高随行、新增行值逐格对齐中间表、仅 N 个预期 ZIP 条目变化、其余 sheet 原有行逐行逐格不变、其余 definedNames 未动、共享字符串/样式/批注逐字节相同。第二轮再加「原表行抽样实时回源」验证搬运无损。
- **防再建守卫与回写兼容**：合并后给生成分表的脚本加运行守卫；增量回写脚本必须按刊号遍历定位，不能硬编码行号，且回写第三方列时要同步更新同行「备注」的状态文本，否则又会出现「有值却写未抓取」。

## 2026-11-08 第八轮：在用户手工改过的表上追加颜色标记

- **先查 mtime / MD5，再动手**：用户说「我修改的不要动」时，文件可能刚被 Excel/WPS 重存过，与上一轮交付的指纹已不同（本轮用户把冻结 AL3 改成 C2、重调了 3883 行行高）。第一步必须备份当前版本作为新基线，重新记录冻结/筛选/行高/列宽/批注，不能沿用上一轮的基线快照。
- **只加颜色 = 只加 fill + 复制 xf + 改单元格 s**：在 `styles.xml` 的 `<fills>` 末尾追加纯色 fill，在 `<cellXfs>` 末尾追加「复制原 xf、仅改 `fillId` 并置 `applyFill="1"`」的 xf，再把目标单元格 `s` 指向新 xf。字体/边框/对齐/数字格式/行高全部原样，比 openpyxl 重存安全得多。只对目标列改 `s`，其余 ZIP 条目解压内容可做到逐字节不变。
- **ZIP 压缩字节不同不等于内容被改**：Excel/WPS 保存的 deflate 级别与 Python zlib 默认不同，`writestr` 重写后压缩尺寸会变（本轮 2.27 MB → 1.74 MB），但 28 个未改条目解压后逐字节相同。自检判据应落在「解压内容逐字节一致」，不要误报为格式被破坏。
- **幂等必须处理「已着色的 s 索引」**：重跑时扫到的单元格 `s` 已指向新增的色标 xf，若直接拿它当基础索引会再追加一批 xf（本轮曾多出 18 个）。做法：把 `xf_map`（基础 s:色号 → 新 xf 索引）落盘，重跑时建 `idx2base` 把当前 s 归一回基础 s，并验证已有 xf 的 `fillId` / `applyFill` 后复用。判据：重跑新增 fill/xf 均为 0、文件 MD5 不变。
- **图例放进已有 sheet，不新建**：颜色含义必须自解释；在「口径与来源」末尾追加带色块的 `inlineStr` 行，同步改 `<dimension>`，既有行字节不动。浅色底配原有黑字，用 WCAG 对比度 ≥4.5 做机检（本轮 11 色为 14.12–18.82:1），再做真实底色渲染的目视复核。
- **判据不要脱离数据分布**：要求「每个 IF 档至少 3 个样本」在本表 ≥10 分只有 2 本时必然假 FAIL；改成每档 ≥1，并把边界整值样本单列核对。
- **颜色标记后要复验增量回写脚本**：按刊号定位的字节级回写会保留单元格 `s` 属性，颜色不会丢；但回写会把目标 `<c>` 换成 `inlineStr`，使「sheet1.xml 除 s 外逐字节不变」这类判据失效。因此颜色交付与增量回写不要在同一轮叠加，或先把审计基准切换为着色版。

## 2026-11-08 第九轮：改换色标（分区高对比 + IF 整数段）

- **用户每重存一次，样式索引都可能被 Excel 重排**：本轮用户第二次保存后 `cellXfs` 从 14 个变 44 个、基础 s 索引全部换号，旧脚本里「s<14 是基础样式」「xf_map 中 s<14」的假设全部失效。正确做法：对每个目标单元格取当前 `xf`，用 `norm_xf`（去掉 `fillId` 与 `applyFill`）算签名，按 `(签名, 目标 fillId)` 建映射；同签名的多个 xf 共享同一个新彩色 xf。这样既保住字体/边框/对齐/数字格式，又天然幂等（重跑时已着色的 xf 归一化后签名不变，直接命中自己）。
- **替换已有图例要先反查 sharedStrings**：Excel 重存会把 `inlineStr` 图例改成 `t="s"` + `<v>索引</v>`，XML 里搜不到中文，`'颜色标记图例' in xml` 会漏判。做法：先在 `xl/sharedStrings.xml` 找含「颜色标记图例」的 `<si>` 下标，再到 sheet3 里找引用该下标的 `<row>` 得到起始行；新图例仍写 `inlineStr`，重跑走文本定位。删除旧图例区时断言行号连续，避免误删业务行。
- **色标差异要落成可判定的数值判据**：分区「对比明显」= 四色两两 RGB 欧氏距离 ≥100（本轮最小 112.4）；IF 相邻整数段可区分 = 相邻色 RGB 距离 ≥25（本轮最小 26.6）；黑字可读 = WCAG 对比度 ≥4.5（本轮 15 色 5.78–18.60:1）。只靠肉眼说「明显」不够。
- **分档规则用 `floor(IF)`，不要沿用不等宽区间**：用户要「0.1–0.9 一档、1.0–1.9 一档，以此类推」就是按整数部分分段，边界值 `0.9/1.0/1.9/2.0` 必须单列核对；段数由表中最大 IF 决定，色表要能自动扩展（本轮 0–10 共 11 段）。
- **图例也要过禁用符号与排版判据**：把直角引号「」『』纳入机检；固定 30pt 行高下说明文字若换成两行会贴底，目视复核后压成一行再终检。机检全绿不等于视觉不难看。

## 2026-11-11 第十轮：单源判零误剔的整体修正、投稿刊豁免与实体清理

- **「近 1 年零文章」不等于「无文章」**：交付表曾用 `Europe PMC FIRST_PDATE:[近1年] 逐篇去重=0` 剔除 341 本，清单自身 E/F/G 列却显示 162 本三年 PubMed 有发文、26 本 ≥100 篇、8 本 2025 单年 ≥100 篇。实测 `AMERICAN BIOLOGY TEACHER`（ISSN 0002-7685）PubMed 2023/2024/2025 = 129/130/133 篇，而 Europe PMC 全时段仅 42 篇；`Asian Journal of Surgery` 三年 6086 篇被剔，却在同一轮视频补刊中并入主表。根因是单一源 + 单一时间窗，不是学术判断。清单命名「无文章剔除清单」必须改写为「某源某时间窗未检出」，否则误导读者。
- **回补判据必须双口径**：当前版 JCR/WoS 仍收录（本例 JCR2026 表 162/162 命中）AND PubMed 2023/2024/2025 至少一年有发文 → 判定误剔并回补；仅 PubMed 三年全为 0 的 179 行保留剔除，原 sheet 作为历史证据不删改。别用「EPMC 布尔命中数」替代官方收录状态。
- **本人投稿刊无条件豁免**：投稿台账 + ORCID 已发表记录共 40 本，哪怕 EPMC 近 1 年为 0 也必须保留；被误剔的（如 `Bratislava Medical Journal`）先回补再复核。豁免规则要同时写进 SKILL.md 主文件与口径 sheet，避免下游脚本又把剔除规则套上去。
- **去重按三键而非单键**：按「刊名 norm + ISSN/EISSN/刊号」比对主表；刊号写 `N/A` 的纯电子刊（如 `Food Science and Human Wellness`，EISSN 2213-4530、IF 7.3）必须按刊名回退查 JCR 表，否则会漏。本轮 162 本 → 159 本回补 + 3 本原已在表 = 全覆盖。
- **回补行的数据装配**：B–J 取 JCR2026 表、K 取 CAS 四源、L/M/N 取 PubMed 年度发文、第三方静态字段沿用旧版台账并在 AE 证据等级注明来源与日期；近 3 年 EPMC 逐篇（AI–AP）未重采一律写「待核实」，V/W 写明误剔根因，绝不推测补全。回补仍走字节级插入（原行整体搬运、仅改行号/序号、按 IF 降序、同步 dimension/autoFilter/workbook 三处范围）。
- **双重 HTML 实体在两层**：旧 NLM 文本里的 `&amp;` / `&lt;` / `&gt;` / `&quot;` 既存于 `sharedStrings.xml` 的 `<si>`，也存于新增行的 `inlineStr`；XML 源码形态是 `&amp;amp;` / `&amp;lt;` 等。清理只能字节级替换两个 ZIP 条目为单层 XML 实体，不可用 openpyxl 重存。判据里 `&#` 不能当实体标志——URL 片段 `...?journalCode=uteh20&#.U2c1-lfkIdU` 是合法 URL；要用 `&#\d+;` / `&#x[0-9a-fA-F]+;` 正则。
- **归一化比对要用精确替换，不要用 `html.unescape`**：后者会把 URL 查询串里的 `&copy` / `&times` 等无分号片段误判为实体，导致「除实体外零改动」假 FAIL。用 4 种实体的定点 `replace`（最多两轮）归一化 PRE 值，再与 POST 逐格比较，才能证明除实体外零改动。
- **复核证据文件要逐行落结论**：每个误剔刊写明「复核结论 + 最终主表行号」，分布可核（本轮 162 = 159 本轮回补 + 3 本原已在主表），并在总览列出实际回补数、跳过数与跳过原因明细。最终自检把「原行除序号/实体还原外零改动」「仅预期 ZIP 条目变化」「全表实体清零」「两个明细 sheet 逐行有结论」一起判，本轮 41/41 PASS 才交付。

## 2026-11-11 第十一轮：v1.3.0 下游同步与抖音全量采集的正确姿势

- **三条硬规则必须同步到下游脚本，而不只写进 SKILL.md**：视频补刊脚本仍以「EPMC 近3年逐篇<3 单源判零」剔除 16 本，其中 4 本 JCR2026 在版且 PubMed 三年有发文，属误剔。改判据为「生物医学口径 + PubMed 近3年至少一年有发文，投稿刊豁免」，并把分布为空时 W/AP 列写的「无文章」改成「待核实（EPMC 未取到逐篇 pubType，不判为零文章）」。旧规则文本保留作历史留痕，但机检要判「旧逻辑已废止 + 新判据已写入 + 脚本语法通过」。
- **更正错误结论比补数据优先**：上一轮把抖音 9 号作品不可枚举归因为「服务端绑定 session 用户」，是错的。留档 JSON 要保留原文并加「复核状态=已推翻」+ 正确路线，不能静默覆盖，也不能让错误结论继续留在证据簿口径说明里。更正用「末尾追加说明行」，既有行零改动。
- **抖音 PC 用户页全量枚举的两个关键**：① 登录态打开目标用户页后，**被动监听页面 SDK 自己发出的** `/aweme/v1/web/aweme/post/` 响应，绝不手动 `fetch` 改 `sec_user_id`（改参会破坏签名绑定，服务端回退到登录账号本人作品）；② 用户页是内部虚拟滚动列表，`window.scrollTo` / `document.body.scrollHeight` 无效，必须遍历 `overflow:auto|scroll` 且 `scrollHeight > clientHeight` 的容器逐个 `scrollTop = scrollHeight`。本轮 9 号 2293 条台账作品实采 2300 条、全部 `has_more=false`、接口作者与台账逐号一致。
- **新证据源先做零成本文案层扫描，再决定是否全量下载**：2300 条 desc 对 JCR2026 全表 36240 本刊名做连续短语逐字匹配，只命中 8 本（7 本已在主表，唯一缺失刊属非生物医学 B 类维持剔除）→ 文案层零新增补刊。刊名在中文短视频文案里多是俗称，须画面 OCR 才能提取；播放地址 2300/2300 齐全，可后续批量下载，但不推测补全。
- **综合自检要跨文件**：一份脚本同时判主表回补（原 4382 行零改动、仅 3 ZIP 条目、IF 降序、W 列零「无文章」、sheet3 既有 1–154 零改动 + 新增 8 行）、规则同步、抖音全量采集（9 号 done / has_more / 覆盖率 / ID 唯一 / 作者一致）、证据簿追加（既有 11 sheet 逐格零改动）。本轮 51/51 + 29/29 PASS，机检后另出 3 张渲染图做目视复核才交付。

## 2026-11-11 第十二轮：画面层证据的小样本验证、全量链路固化与旧判据治理

- **小样本先算单位产出，且必须复核这个数本身**：30 条分层样本（9 号覆盖）下载 29/30 成功、112 MB、792 帧、5156 条 OCR 文本行。首版「跨帧拼接 + 模糊匹配」报命中 36 刊、主表缺失 7 刊 → 单位产出 0.2414 本/条；改用「单帧内连续短语」精确判据后只剩 3 刊、缺失 1 刊，再查该 1 刊实为长刊名拆行造成的子串假命中 → **真实新增补刊 0 本**。全量 mp4 在约 80 条处即叫停（约 3.5 小时 / 8 GB 的无效开销），改走 2300 张封面图约 110 MB 的低成本筛查。教训：量化指标若建立在宽松判据上，比不量化更危险，会驱动一次高成本的错误扩量。
- **短刊名子串必假命中**：OCR 常把长刊名拆成多行，如画面里 `International Journal of | Medical Sciences` 被首行错识为 `Sntetnntionel Cournal of`，白名单里的短刊 `Medical Sciences` 于是精确命中，但主表其实已有 `International Journal of Medical Sciences`。消歧规则：凡「主表缺失」的短刊名是主表中某个更长刊名的后缀，直接判为拆行/OCR 截断假命中；`Preventive Medicine` 一类通用词命中也要人工看原文是否为期刊名展示。
- **OCR 证据必须逐帧全文落盘**：首版脚本只把 `sample[:6]` 和命中计数写入结果文件，导致 7 本「主表缺失」无法回溯是哪条视频哪一帧出现——证据链不可复核，属缺陷。正确产物是 `*_ocr_full.jsonl`（每帧 lines 全文）＋ 命中证据（aweme_id / 帧号 / 原文）。**跨帧拼接 `compact(' '.join(all_lines))` 会产生假命中**，精确判据必须限定在单帧内连续短语；模糊匹配只作线索，不能单独作为并入依据。
- **全量脚本放项目内，不依赖 `/tmp`**：`playwright-core`(14 MB)、Vision `ocrbin`、登录脚本、采集脚本、验收脚本、一键 shell 全部固化到 `抖音采集/tools/`；cookie chmod 600。一键链路四段：语法/依赖预检 → headless 登录态自检（post 响应 `status_code=0` 且 `aweme_list` 非空）→ 采集 / `--verify-only` → 17 项数据验收。验收实证 17/17 PASS。
- **登录过期分支不能靠动真实 cookie 来测**：直接 `cp`/`mv` 凭据文件会被本机沙箱按敏感文件策略拦截（exit 13），且中途失败可能把 cookie 留在临时名。改法：脚本支持 `DY_COOKIE` 环境变量覆盖路径，用 `[]` 伪造凭据演练过期分支（实测输出 `LOGIN_EXPIRED`、RC=3、给出登录命令），真实凭据全程不读不写，恢复分支再跑一次 17/17 全绿。
- **「grep 零命中」不是合格的清理验收口径**：宽口径扫描命中 66 处，其中绝大多数是历史 sheet 名、审计统计键、回补脚本里的根因说明，按「历史证据不删改」必须保留。正确口径是「执行型单源判零代码 = 0」：本轮定位到 2 个旧脚本仍会以 `n_fetched==0` 剔除，给它们各加 1 行 DEPRECATED 头注释 + `LEGACY_REPRO=1` 入口闸门（历史原文一字未删），实测直接运行均被拦、RC=1、`py_compile` 通过；活跃链路 `merge_video_candidates.py` / `merge_submitted.py` 无任何剔除动作。分类结论写进 `p3_legacy_grep.json` 的「复核结论」字段。
- **封面层是低成本高产出的一层，但「产出」必须逐本走双口径**：2300 张封面（2299 张有文字）Vision OCR 命中 450 刊，主表已有 332 本、短刊名拆行假命中 12 本，消歧后主表缺失 106 本；按生物医学门类筛出 21 本走「JCR2026 在版 + PubMed 2023/2024/2025 三年发文」双口径，11 本通过并回补（主表 4386 → 4397 数据行）、10 本三年零发文不并入、85 本非生物医学不并入。画面层 30 条小样本真实 0 本、封面层 11 本——「某层零产出」不等于「整条证据链零产出」，但每层结论必须分别留痕，且绝不能拿首版 0.2414 的虚高单位产出去扩量。3 本近3年仅 1 篇的刊在 V 列写明「活跃度存疑、后续须复核是否为新刊/更名刊」，W 与 AI-AP 未重采一律写「待核实」，不推测补全。

## 2026-11-11 第十三轮：双口径拦不住的三类假命中、撤回与三层单位产出

- **`compact(全文)` 子串匹配是隐蔽的数据污染源**：v1 封面层把整张封面的 OCR 全文压成无分隔字符串后做 `刊名 in 全文` 判断。三类假命中都通过了 JCR2026 + PubMed 三年双口径，因为**这些刊名本身是真刊**：① 更长刊名前缀 `Journal of Ultrasound` ← 原文 `JOURNAL OF ULTRASOUND IN MEDICINE`（长刊已在主表）；② 单词内部子串 `Urological Science` ← `NEUROLOGICAL SCIENCES`（`neurologicalsciences` 去掉首尾字符恰为 `urologicalscience`）；③ 跨相邻刊名行拼接 `Medicine Advances` ← `…Therapeutic | Medicine | Advances | in Medical | Sciences`（实为 Experimental and Therapeutic Medicine 与 Advances in Medical Sciences 两刊的 OCR 拆行）。教训：**双口径只证明「这本刊真实存在且活跃」，不证明「这张封面提到它」**；证据边界必须在原文局部判定，不能用全局白名单前缀（否则 JCR 里任何更生僻的长刊名都会误杀真命中，如 `Journal of Clinical Medicine` 被 `Journal of Clinical Medicine Research-Canada` 误杀）。
- **v2 严格判据（可判定、可复跑）**：以 Vision OCR 的 `lines` 为原子，剥掉行首编号（`9. Health Policy…`），只合并相邻 1–4 行，合并串须**精确等于** JCR 刊名 compact；左右扩一行若精确等于另一本刊名则剔除；两个不同刊名命中区间重叠则双双剔除。2300 张封面离线重扫：v1 450 刊 → v2 362 刊（剔除 88 本）；11 本回补中 3 本撤回、8 本保留，主表 4397 → 4394 数据行。删行须同步重排行号与 A 列序号、更新 dimension/autoFilter/definedName，机检按「刊名序列」而非行号比对。
- **错误数据进主表后的处置次序**：先备份 → 撤回错误行（不是改写其单元格内容）→ sheet3 说明区**追加**更正行（既有说明一字不改）→ 证据簿追加复核 sheet 与口径说明 → 旧脚本加 `LEGACY_REPRO=1` 闸门防再次污染 → v1 结果文件按历史证据保留。更正说明也要按版式限长（本轮 4 行先写了 350 字，目视必溢出，压缩到 ≤123 字）。
- **v2 仍需继承 v1 的后缀消歧**：严格边界判据拦住了前缀/内部子串/跨行拼接，但短刊名若是主表某更长刊名的后缀（长度差 ≥ 6），仍会以独立行命中（本轮 35 刊 / 105 条命中对，如 `Medical Sciences` ← `International Journal of Medical Sciences`）。处理方式是加「疑似主表长刊名后缀」字段与独立线索清单，不删改已交付的 v2 命中数与证据簿快照——既让机制自动挡住，也不破坏已审计的一致性。
- **三层证据各自算单位产出**：画面层 30 条 mp4 逐帧 OCR 真实 0 本；封面层 2300 张 v2 有效 8 本（另 886 条视频–期刊反查对可回源）；口播层 30 条拼接 14.1 分钟一次 ASR、56 段，严格英文词窗只命中 `Scientific Reports`（已在主表）→ 真实 0 本、停止全量扩量。口播几乎不念刊名，只说「第一本 IF 4.9」「水刊之王」「mdpi 旗下综合医学刊」，与封面层互补性低。**某层为 0 不等于全链为 0，也不允许拿别层的产出为该层扩量背书。**

## 2026-11-11 第十四轮：启发式标记误伤、重采回填与一键链路纳入证据验收

- **「疑似」不是结论，一刀切排除必然误伤**：v1 把 12 本「疑似长刊名拆行」整体踢出 106 本候选池，其中 4 本主表缺失刊（`ARTIFICIAL INTELLIGENCE`、`General Psychiatry`、`Journal of Medical Science`、`Medical Sciences`）在 v2 严格边界复核后仍在 362 刊命中明细内。逐本回源 + 双口径重核后：`General Psychiatry`（IF 9.9 / PSYCHIATRY / ESCI，PubMed 三年 70/73/62，EPMC 布尔 217）属独立命中且通过双口径 → 回补主表；其余 3 本分别因非生物医学 / 全为长刊名拆行 / PubMed 三年 0 篇（EPMC 布尔却 1101，两源不一致，不推测补全）不并入。教训：启发式标记只能缩小复核范围，必须逐本留结论与理由。
- **回源原文判定「拆行 vs 独立命中」的四类可判定判据**：① 左扩 1–3 / 右扩 0–2 行合并 compact 精确等于 JCR 或主表更长刊名；② 全封面 compact 中更长刊名的结束位置**正好等于**命中区间结束且起点在其之前（要用 units 累积偏移 `cum` 精确定位；只判「全封面含该长刊名」会把「封面别处另有一本长刊名」误判成拆行，首版 35 本因此多判 7 条）；③ 左扩行与更长刊名 compact 相似度 ≥0.88，抓 OCR 错字与复数丢失（如 `INTERNATIONAL | JOURNAL OF | MEDICAL SCIENCE` 实为 `International Journal of Medical Sciences`）；④ 封面别处出现完整长刊名只记线索、不硬判。本轮 105 条证据逐条落判定，35 本结论：保留 26 / 排除 3 / 部分排除 6。
- **大刊逐篇重采要按刊数而非行数估时**：8 本回补刊近 3 年 EPMC 逐篇重采，小刊 1 页 9 秒（General Psychiatry 217 篇），`Journal of Clinical Medicine` 26551 篇需 28 页、整批 18 分钟。合计 36048 篇。回填只改 W / AI–AO / AP 九列，`V` 列的封面层画面证据原样保留；O/Q/R/S/T/U/X–AC/AF/AG 等第三方静态字段未采集，仍写「待核实」，不编造。W/AP 由 pubType 分布生成时，分布为空写「未取得记录，不判为零文章」，绝不写「无文章」。
- **一次 patch 同时做「回填 + 插入」**：插入新刊会重排全表行号，若按固定行号回填必然错位。正确做法是先在当前 XML 上按刊名定位 8 行替换九列，再按 IF 降序插入新行并整体 `renumber_row`，同步 dimension / autoFilter / workbook.xml definedName、sheet3 追加说明行；审计按**刊名序列**而非行号比对「原 4394 行非目标列零改动」，并判「8 行 × 9 列全部替换 = 72」「仅 3 个 ZIP 条目变化」「sharedStrings/styles 逐字节不变」。本轮 26/26 PASS。
- **一键链路要把证据验收一并纳入**：`run_pipeline.sh --verify-only` 除 9 号采集验收外增挂只读验收脚本，把 v2 边界（450→362、剔除 88）、视频反查（886 行 / 495 视频 / 362 刊、抽样 20 条）、口播 ASR（30 条 / 56 段 / 单位产出 0.0）、35 本复核、4 本双口径、主表 4395 行与证据簿 26 sheet 一起判，45/45 PASS 才输出 `PIPELINE_OK`。三分支实测：正常 RC=0、伪造空 cookie 演练 `LOGIN_EXPIRED` RC=3、恢复 RC=0；真实凭据全程不读不写。机检全绿后仍出 4 张渲染图 + 2 张放大裁剪做目视复核（细字号挤压、中文、说明行 ≤123 字）。

## 2026-11-11 第十五轮：标识符缺陷推翻「零发文」、静态字段实证补齐、SOP 检查表

- **两源矛盾先查查询式，不要先解释数据源**：第十四轮把 `Medical Sciences` 判为「PubMed 三年 0 篇 vs EPMC 布尔 1101，两源不一致」，本轮把 OR 拆开逐支复现实测：`20763271[ISSN]`=1、`2076-3271[ISSN]`=1660、`"Medical Sciences"[Journal]`=0、`"Med Sci (Basel)"[Journal]`=1660；EPMC `ISSN:"20763271"`=0、`ISSN:"2076-3271"`=1101。根因是 `verify_missing4.py` 用 `nk()` 去掉 ISSN 连字符、并把 JCR 全称作 PubMed 精确 TA（本刊 NLM MedlineTA 为 `Med Sci (Basel)`）。**既不是 JOURNAL 字段噪声，也不是未被 MEDLINE 索引**：EPMC 1101 的 100 篇 `resultType=core` 样本 100/100 的 journal title 均为 `Medical sciences (Basel, Switzerland)`；NLM Catalog 记录 `MEDLINE v9n1, Mar. 2021-`。正确年度发文 2023=72 / 2024=76 / 2025=344，合计 492。第十四轮说明行原文保留，追加「复核状态=已推翻」。
- **主表未受污染的证明要单独给**：全表 L/M/N 来自 `pubmed_counts.py`，其 `norm()` 已把 8 位 ISSN 还原成带连字符形式，故「查询缺陷」仅限 `verify_missing4.py` 这一条支线；补做 General Psychiatry 带连字符复验得 70/73/62，与主表已填值一致。发现某个脚本的标识符错误时，必须先界定受影响范围，不能顺势推翻整表数据。
- **活跃度成立 ≠ 证据成立，处置理由要换成能被复核的那一条**：修正后该刊按「JCR2026 在版 + 生物医学 + 独立封面命中 + PubMed 有发文」双口径本应可补，但把 6 条「独立命中」逐条回源：2 条是长刊名截断（`Internatio | Medical Sciences`）或栏目文字（`Letlers | MEDICAL SCIENCES | BALKAN MEDHCAL XOURNAL`），2 条的「JCR Q2 / 中科院 4 区」与 JCR2026 Q1 矛盾，其余 3 条只有刊名与版面费、无 ISSN/出版社等可判别信息 → 判「封面证据不足，仍不并入」。结论强度不得超过证据深度：数据错了要改，结论可以不改，但理由必须换成实证撑得住的那一条。
- **第三方静态字段的冲突要并列、不要择一**：第 313 行 `General Psychiatry` 的 14 格由实证补齐：NLM Catalog（BMJ 出版、2018 创刊、PubMed/PMC 收录）、DOAJ（APC USD 2,700 / GBP 2,250 / EUR 2,590、OA 起始 2018）、OpenAlex（`is_oa=true`、homepage、GB）、LetPub（录用率 37%、首次决定 29 天、Continuous publication、出版国 China、创刊年 1959）、Crossref / DOI 落地（Wiley、`10.1002/gps3`）、`gpsych.bmj.com` 301 跳 Wiley 且两站直连 403。出版社、国别、创刊年三处多源冲突全部并列标注，不编造「前身/迁刊」沿革；无数据的 O/U 写「未核到 + 已查源」；未取得独立投稿系统网址就直写未取得。
- **旧审计不迁就新数据，新轮次另起审计**：本轮只改 sheet1.xml / sheet3.xml 两个 ZIP 条目，行数、workbook.xml、styles、sharedStrings、冻结 C71 全部不动，故 `audit_round14.py` 27/27 与 `verify_round14.py` 45/45 仍全绿，无需改判据。第十五轮另起 `audit_round15.py` 与 `verify_round15.py` 判新事实（15 格零待核实、sheet3 183–192、两源归因、skill 版本），并挂进 `run_pipeline.sh --verify-only`。历史自检若因后续合法改动而失效，正确做法是新增该轮审计，而不是放松旧判据。skill 升 v1.4.3，新增「一键链路验收检查表」12 段与两条硬规则（标识符可复现、静态字段不得停在模糊态）。

## 2026-11-11 第十六轮：标识符缺陷全库界定、封面证据终局翻转、自检单一入口治理

- **修完单刊不等于修完缺陷，必须界定污染范围**：第十五轮只在 `Medical Sciences` 一本上证明「去连字符 ISSN + JCR 全称作 TA」会得假 0 篇。第十六轮扫 149 个 py，24 个发出 `[ISSN]` / `ISSN:` / `[Journal]` 查询；逐项给结论：`pubmed_counts.py`、`collect_top.py`、`expand_collect.py`、`nlm_meta.py`、`article_types_3y.py` 等 13 个经 `norm()` / `dash()` / `fullmatch` 已带连字符，`collect_one_light.py` 常量 `1752-1947` 带连字符，`collect_submitted.py` 取 `submitted_pool.json` 原值（8 个带连字符）安全；`verify_missing4.py` / `verify_cover_candidates.py` / `verify_pilot30_candidates.py` 三个核验脚本有缺陷。用 3 本「原值本就正常」的刊作对照（Journal of Clinical Medicine 24582、Am J Transl Res 2236、Urological Science 1），带连字符重算逐篇一致 → **主表 L/M/N 未污染，污染只落在补刊决策支线**。发现某个脚本的标识符错误时，先给「受影响脚本清单 + 是否污染已交付数据的逐项结论」，再动手改数据。
- **假零发文重算 4 条翻转，但翻转 ≠ 可并入**：`cover_verified_candidates.json` 中 10 条「PubMed 近3年零发文」+3 条对照共 13 条重算，4 条翻转：Psychedelic Medicine 0→102、Hong Kong Physiotherapy Journal 0→61、CURRENT PSYCHOLOGY 0→414、Indian Journal of Otolaryngology 0→3016。逐本回 `douyin_full_cover_hits_v2.json` 再筛：前两本中的 Psychedelic Medicine 与 Indian J Otolaryngol 被 v2 严格边界判「无独立期刊名边界」（前者封面其实是 `ANNALS OF THE NEW YORK ACADEMY OF SCIENCES` 加文章标题 `psychedelic medicine`）→ 终局不补；`CURRENT PSYCHOLOGY`（1 张）与 `Hong Kong Physiotherapy Journal`（2 张）在 v2 命中明细中且无后缀标记 → 回补。**活跃度判据修复只能把刊送回候选池，不能替代封面证据判据。**
- **把「证据不足」翻成「证据成立」需要外部锚点，不能用单条字符串相似度**：82 张含 `MEDICAL SCIENC` 的封面逐条回源分类 = 71 长刊名拆行 / 截断 + 10 栏目文字或无判别信息 + 1 可判定独立命中。唯一 A 类作品 `7685699622974639406` 同时写「MDPI 旗下」「影响因子 5.9」「官宣 18 天出结果」「版面费 1w」「MEDICAL SCIENCES」，与 MDPI 官网（JCR Q1、first decision ≈18.3 days、APC CHF 1600、monthly、ISSN 2076-3271）及 JCR2026 行 4434（IF 5.9 / Q1 / ESCI / MEDICINE GENERAL & INTERNAL）逐项吻合。第十五轮把这归为「仅刊名+金额无可判别信息」是漏看了出版社与 IF 锚点。第十五轮 O/S/T 列原文保留，第十六轮在 U–W 追加「已推翻 / 已回补行 741 / 依据」。
- **两源差异与多源冲突一律并列**：`CURRENT PSYCHOLOGY` PubMed 三年 414 篇（380/18/16）vs EPMC 近3年逐篇 40 篇，差异 10 倍，写入 AE 列并列不择一、不作推测解释；Medical Sciences 的 APC 官网 CHF 1,600 与 DOAJ CHF 1,400 并列；NLM `Quarterly, 2013-` 与 MDPI 官网 `monthly` 并列；NLM 国别 Switzerland 与 OpenAlex CH 并列。3 本新行 42 列全部「实证值 + 来源」或「未核到 + 已查源」，零「待核实」。
- **历史快照审计的退役要制度化，不能让一键链路长期挂红**：第十六轮按 IF 降序插入 3 行（主表 4396→4399、sheet3 192→203、证据簿 26→31 sheet），round14/15 的绝对行数/行号/MD5/链路段落数判据必然失效。按第十五轮「不放松旧判据」的约定，不改旧脚本，改为：① 新增 `audit_round16.py` / `verify_round16.py` 继承其实质判据（原 4395 行按刊名逐格零改动、仅 3 个 ZIP 条目变化、styles/sharedStrings 逐字节不变、冻结 C71、既有 24 sheet 零改动）；② `verify_all.py` 单一入口自动发现 `verify_round*.py` / `audit_round*.py`，`MIN_ACTIVE_ROUND=16`，历史套需 `--include-legacy` 显式复现；③ `run_pipeline.sh --verify-only` 的 `[3b]` 只调一次 `verify_all.py`。入口建成时曾在写入前实测 `ALL_CHECKS OK 163/163 PASS (4 suites)`；扩展后活跃集合升级为第 16 轮两套，判据实质不减。skill 升 v1.4.4，新增两条硬规则（标识符缺陷全库界定、结论翻转需外部锚点）与检查表第 13/14 段。

## 2026-11-12 第十七轮：残留缺陷脚本修复、两源差异归因、持久基线与历史自检分类

- **「已发现缺陷」不等于「已修完缺陷」，必须把同类脚本全部修掉并出 diff**：第十六轮界定出 3 个有 ISSN 缺陷的核验脚本，但只修了 `verify_missing4.py`，`verify_cover_candidates.py` 与 `verify_pilot30_candidates.py` 仍在用 `nk()` 去连字符 + JCR 全称作 `[Journal]` TA。第十七轮把两脚本统一改为 `norm()` 带连字符 ISSN、移除 TA 分支，产物另存 `*_round17.json`（原产物零改动），并出逐行 diff：106 本候选中可并入 11→15，4 条翻转（Psychedelic 102 / HKPJ 61 / Curr Psychol 414 / Indian J Otolaryngol 3016），其中 2 条已在主表、2 条经 v2 严格边界终局不补；对修正后仍为 0 篇的 6 本再用 NLM MedlineTA 补验全部 0 篇，残留误伤 0。**修脚本时必须同时保留旧产物作 diff 基线，否则无法界定影响范围。** 另修掉一个自身缺陷：NLM esummary 的 `titlemainlist` 是 list of dict，直接当字符串拼进 `[Journal]` 会让补验形同虚设。
- **两源数量级差异先对齐日期字段，不要写「索引范围不同」**：`CURRENT PSYCHOLOGY` 第十六轮写「PubMed 414 vs EPMC 40，口径/索引范围不同，不择一」——这是推测。第十七轮给四条可复现查询：PubMed `[pdat]` 380/18/16=414、三年 OR=407、`"Curr Psychol"[Journal]` 三年=407；EPMC `FIRST_PDATE:[2023-11-10 TO 2026-11-10]`=40、`PUB_YEAR:[2023 TO 2025]`=404、无窗口=1062、`FIRST_PDATE` 2023 全年=227、2022 全年=483；PubMed `2023[epdat]`=227 与 EPMC 2023 在线数精确相等；core 样本 10/10 为 MED 源、双 ISSN 齐全、MedlineTA=Curr Psychol，NLM Catalog 记录在版。结论：**差异 100% 来自正式卷期年 vs 在线首发日期 + 窗口起点，不是索引缺失/改名/停收**。同口径下两源 407 vs 404 一致。「不择一」是回避判断，不是结论；AE2506 已换成查询式与数字。
- **审计基线绝不能放 `/tmp`**：第十七轮开机后发现 `/tmp/*.pre_roundN.xlsx` 全部被系统清理，`audit_round12/13/14/15/16.py` 集体 `FileNotFoundError`，第十六轮还全绿的活跃审计一夜变红。这不是数据回归，是环境依赖缺陷。修法：项目内建 `基线备份/`，存第十七轮改动前的两件 xlsx + `round17_baseline_manifest.json`（字节数/MD5/mtime），新增 `audit_round17.py` 以持久基线判「仅 sheet1.xml / sheet3.xml 两个 ZIP 条目变化、除 AE2506 外原 4399 行逐格零改动、既有 30 个 sheet 零改动」。**任何「逐格零改动」判据的真相源必须与被审计文件同生命周期。**
- **历史快照失效要分类，不能一刀切忽略**：`verify_all.py --include-legacy` 现按 `verify_all_legacy_baseline.json` 的失效签名逐套判 EXPECTED（已知主动退役提示 / `/tmp` 备份已清理 / 已登记的绝对快照 FAIL）/ SUSPECT（基线外新 FAIL、新异常、无 RESULT、无基线）/ RECOVERED（历史套意外全绿，疑数据回滚）。只有活跃套 FAIL 或历史套 SUSPECT/RECOVERED 才让退出码非零。8 套历史全部 EXPECTED；`--self-test` 5/5；演练删掉基线里 `verify_round14.py` 的 FAIL 集合后立即判 SUSPECT 并 rc=1，还原后复绿，报告写入 `verify_all_legacy_report.json`。**「让链路变绿」不能靠放松判据，只能靠证明失效属预期 + 保证新问题仍能被判出。**
- **本轮改动边界**：主表 4399 行不变，只改 AE2506 一格（265→498 字）与 sheet3 追加 204–210 共 7 行；证据簿 31→35 sheet、口径说明 53→59 行；`run_pipeline.sh` 预检改指第 17 轮两套并加 `--self-test`；skill 升 v1.4.5（新增 2 条硬规则、检查表第 15/16 段）。活跃集合 `MIN_ACTIVE_ROUND=17`，round16 因 `/tmp` 依赖退役。两套新自检：`verify_round17.py` 85 项、`audit_round17.py` 37 项。

## 2026-11-12 第十八轮：措辞扫描判据自陷、行窗口上限漏检、基线自动落盘模板化

- **扫「推测措辞」最容易误伤的是规则声明与证据原文**：本轮扫主表 9 sheet + 证据簿 35 sheet 共 22,580 格，首版判据把 29 格判成 A 类「需替换」，逐一看全是误判：主表「严禁推测」「不作推测补全」「不推测、不编造」是否定式规则声明；`逐帧画面证据`「大概率是引用操纵」、`B站逐帧画面证据`「状态信号存疑」、`抖音9号全量作品`「大概率是时空特征没融合」是 OCR/ASR/文案**逐字落盘原文**，改一个字就破坏证据链；「非 WoS 发文量，口径不同」是口径定义；「封面层·活跃度存疑」是既有栏目标签。修法：加 `NEGATION` 否定语境正则 + `RAW_SHEETS` 白名单（凡证据原文层一律跳过整改）+ 把「两源差异已归因 + 查询式」判为已量化归因。修正后 A 类 **0**，且逐格分类计数可复核。**治理措辞之前，先证明被改的格不是「禁止性表述」或「原文照录」。**
- **「无独立期刊名边界」常常只是行窗口上限的影子**：`recover_cover_hits.py` 的 v2 判据是 `for k in range(1, 5)`（相邻 1–4 行合并后 compact 精确等于 JCR 刊名）。`Indian Journal of Otolaryngology and Head & Neck Surgery` 在作品 `7643793123566554395` 的封面被 OCR 拆成 5 行「Indian Journal of / Otolaryngology / and / Head & Neck / Surgery」，恰超窗口上限，`v1被剔除` 因而回退写成「无独立期刊名边界」。以 5–8 行窗口重扫 88 条被剔除刊，只新命中 2 刊：`Archives of Disease in Childhood-Fetal and Neonatal Edition`（5 行，已在主表）与本刊（5 行，左右扩行无歧义）。**残留误伤 0**，但旧结论必须标注已推翻，不能继续用「无边界」当理由。判据上限是工具限制，不是世界事实。
- **结论翻转的门槛要按硬规则卡住，不能因为「找到完整刊名」就回补**：本刊双口径成立（JCR2026 行 33633 / IF 0.5 / Q4 / ESCI，PubMed 三年 3016 篇），独立刊名边界也成立；但封面可读的判别符只有「编辑官宣无版面费」1 条。Springer 官网实测 `Publishing model: Hybrid`、Print ISSN 2231-3796 / Electronic ISSN 0973-7707、IF 0.5 (2025)、首次决定中位数 7 天、ESCI 收录，页面未列 APC 金额 → 订阅路径 0 APC 只是部分吻合，OA 路径仍收费，该条既不可复核也不满足 v1.4.4 的 ≥2 条独立判别符门槛 → **终局不补**，理由改为「独立边界成立但证据强度不足」。另一本 `Psychedelic Medicine` 的 5 张封面全是 `ANNALS OF THE NEW YORK ACADEMY OF SCIENCES` 期刊封面，命中串出自封面所列论文标题 `Artificial intelligence and psychedelic medicine`，属文章标题假命中 → 终局不补。Liebert 官网重定向到 SAGE 错误页，未取到字段就直写未取到，不推断。
- **基线自动化要连 ZIP 结构一起管住**：把第十七轮手工备份升级为 `baseline_snapshot.py`（`snapshot(NN, files)` / `verify(NN)`，幂等、清单含字节/MD5/mtime/源路径、禁 /tmp）与 `patch_roundNN_template.py`（dry-run → snapshot → 写后逐 ZIP 条目比对）。第十八轮 `--write` 首版把 xlsx 的 8 个目录条目（`_rels/`、`xl/worksheets/` 等）丢掉，ZIP 清单从 30 变 22，`audit_round18.py` 直接 KeyError；修法是在写回时 `zout.writestr(i, b'' if i.is_dir() else data)` 并加「清单完全一致」断言。恢复 round18 基线重跑后 60/60。**用 zipfile 做字节级补丁时，目录条目属于必须逐字节保留的结构。**
- **本轮改动边界与自检**：主表 4399 行不变、sheet1 逐字节零改动，仅 sheet3 追加 211–217（7 行）；证据簿 35→39 sheet、口径说明 59→65 行、既有 34 个非说明 sheet 逐格零改动。`audit_round18.py` 60/60、`verify_round18.py` 挂在 `verify_all.py`（`MIN_ACTIVE_ROUND=18`）；round17 两套退役并登记失效签名；6 张渲染图 + 2 张放大裁剪目视通过。skill 升 v1.4.6（新增 3 条硬规则、检查表第 17/18 段）。

## 2026-11-12 第十九轮：候选池绑定核查——skill 说的和用的不是同一份数据

- **「确认你是这么做的吧」必须先证伪，不能顺势点头**：使用者问「生物医药择刊是否按期刊明细选刊」。实测 `SKILL.md` v1.4.6 工作流第 2 步写的是「先用 `references/catalog_anchor.json` 与 `references/jcr_2026_candidates.tsv` 生成初筛清单」，候选池是 JCR2026 原表派生的 **4181 本 TSV**（源为用户提供的 `科睿唯安2026年度JCR期刊分区表.xlsx`），全 skill 目录 `grep -rln "候选池主表"` 结果 **NONE**，两个 scripts 里也没有任何读主表的代码。`references/catalog_anchor.json` 的 `decisions_2026_11_07` 更明写「第二轮逐刊明细须经使用者明确确认后启动」——即当时是**刻意未纳入**。所以正确答案是「不是」，不是「是，一直如此」。**审计这类确认题，判据是「规则文本 + 代码引用 + 历史决定」三处一致，缺一处就不能点头。**
- **主表不是 JCR 原表的副本，不能用 4181 本反向覆盖**：候选池主表 是「JCR2026 全表 + 抖音/B 站文案/画面/口播三层证据补刊 + 逐本剔除复核」形成的已审定明细，9 sheet / `逐刊明细` 4399 行 × 42 列（A:AP，4398 条数据，IF 降序，G 列 `影响因子(2026 JCR表)` 685.2→0.1），含 W 列文章类型、AE 列归因、剔除与活跃度口径。TSV 只有 14 个静态字段。把 TSV 当主源会丢掉 18 轮的证据链与剔除结论，还可能把 `AIP Advances`、`IEEE SENSORS JOURNAL` 这类已判非生物医学误报重新引回 → 修法必须让 TSV 降级为「交叉校验与补缺索引」，且冲突时以主表为准、并列标注差异、不择一。
- **修法要落到可判定判据，不能只改一句叙述**：本次改了 6 处——`SKILL.md`（version→1.4.7、工作流第 2 步改写、新增「生物医药候选池唯一来源」节、「不可妥协的证据规则」加「候选池不得旁路」硬规则、检查表第 19 段）、`references/output-template.md`（第 6 节加「候选池与口径」必填：绝对路径 + sheet + 行列 + 指纹 + 读取日期 + 每本候选的主表行号 + 主表外候选默认 0）、`references/matching-and-ranking.md`（三档候选必须来自主表、池外刊不得当低门槛保底）、`references/catalog_anchor.json`（**保留** `decisions_2026_11_07` 原文，追加 `decisions_2026_11_12` 启用状态与 `primary_candidate_pool`）、新增 `scripts/candidate_pool_check.py`。历史决定原文一律保留，只追加新状态——沿用第十八轮「旧结论不抹掉」的规则。
- **自检脚本首版两个假绿，靠注入演练抓出来**：① IF 列是文本字符串，`float(v)` 取数 0 个，却因空列表 `all()` 为真让「IF 降序」判 PASS → 改 `tonum()` 解析并要求 `nums` 非空，实测 4397/4398 数值可读、首末 685.2/0.1；② 首版用「全文是否含主表路径」判「工作流第 2 步绑定主表」，抹掉工作流节的路径后别处仍有同串，**注入演练 RC=0 恒绿** → 改按 `## ` 分节精确判，再注入时 `FAIL | 工作流第 2 步绑定主表`、RC=1。最终 `candidate_pool_check.py` **24/24 PASS**，注入演练判 FAIL，`python3 -m json.tool` 与 `py_compile` 均通过。**凡「规则是否写对」的自检，必须做一次「把规则抹掉」的反向演练，否则判据恒绿等于没判。**
- **边界**：本轮只改 skill 文本与自检脚本，主表 候选池主表 与证据簿**零改动**（2,494,073 B / MD5 `a9c0195044c0`）。字段名一律以当次读盘表头为准，禁止硬编码列名；报告仍须逐刊联网核验，主表静态字段不得冒充当前状态。

## 2026-11-12 第十九轮（续）：三项常驻落地、v3 参数化、注入演练的两次假绿

- **「参数化」不能只改默认值，还得证明旧产物一字节没动**：`recover_cover_hits.py` 的 `for k in range(1, 5)` 改成 `range(1, WINDOW_MAX + 1)`，`WINDOW_MAX=COVER_WINDOW_MAX`（默认 4）、`OUT_SUFFIX=COVER_OUT`（默认空＝纯分析，只有显式 `COVER_OUT=v2` 才允许重写 `cover_hit_video_map.jsonl`）。实测默认跑：封面 2300、命中 362、剔除 88、相对磁盘 v2 新增 0，与 v2 完全等价；`COVER_WINDOW_MAX=8 COVER_OUT=v3` 出 364 命中 / 86 剔除 / 新增恰 2 刊（`Archives of Disease in Childhood-Fetal and Neonatal Edition`、`Indian Journal of Otolaryngology and Head & Neck Surgery`），与第十八轮 5–8 行重扫结论逐本一致；`Psychedelic Medicine` 未被误收。写前/写后对 v1、v2、映射三件做字节+MD5+mtime 比对，**零改动**。**分析产物必须只写新文件**，否则「窗口放宽」会把已审定的 v2 判定悄悄覆盖掉。
- **验收脚本要把「零漏检」写成集合判据，而不是一句结论**：`verify_cover_v3.py` 40/40（含 `--recheck-default`）。硬判据包括：v2 命中集合 ⊆ v3、原 362 刊逐本 `命中封面数` 不减、`v3 剔除 ⊆ v2 剔除`（无新增漏检）、88→86 的差集恰好等于 v3 新增刊集合、无清单外新命中、新增刊集合 == 第十八轮 probe 污染范围；再加证据簿 sheet「第十八轮·P2v2窗口污染范围」的「扫描 88 条 / 残留误伤 0」与两本终局处置，以及持久清单 `基线备份/cover_v2_fingerprint.json`（v1/v2/映射/主表/证据簿五件的字节+MD5+mtime）。`--self-test` 三种注入（窗口上限改 4、删一条新增刊、改 v2 指纹）均判 FAIL。
- **注入演练第一次假绿：CLI 参数解析没生效**：`verify_all.py` 新增 `--patch-dir DIR --binding-only` 用于指向伪造补丁目录，首版只解析 `--patch-dir=DIR`（等号形式），而演练命令用空格传参 → 静默回落到默认 `跨平台采集/`，「抹掉 `baseline_snapshot` 调用」后仍输出 `BINDING_OK`、RC=0。**插入静态判据后的第一件事必须是验证注入路径真的切过去了**（打印目录或让假目录里少一个文件导致判据数变化）。修成同时支持等号/空格形式后：调用完整 PASS 8/8、抹掉调用 FAIL 7/8 且 RC=1、完整汇总路径 `ALL_CHECKS FAIL` 且 RC=1。
- **注入演练第二次假绿：「删调用」只删掉了导入**：首版注入用字符串替换 `man = snapshot(18, [MAIN, EVI]`，原文不匹配导致调用仍在，只有「导入」一条 FAIL，演练却仍算通过。改成正则 `\bsnapshot\(\s*18\s*,` 全局替换，并断言「导入 / 调用 / 调用早于 xlsx 写入」**三条判据同时 FAIL** 才算演练通过。**注入演练必须断言具体判据名，不能只判「有一个 FAIL」。**
- **新增自测用例不得改写历史套断言的输出串**：`verify_round17.py` 用 `'SELFTEST OK (5 cases)' in out` 判 `P3 self-test 5/5`。首版把 `--self-test` 输出改成 `SELFTEST OK (5 classify cases + 2 binding cases)` → 历史套新增 3 条 FAIL（该判据 + 「报告 EXPECTED=历史套数」+「报告 SUSPECT=0」级联），`verify_round17.py` 判 SUSPECT。修法：保持 `SELFTEST OK (5 cases)` 一字不改，另起一行 `BINDING_SELFTEST OK (2 cases)`，10 套历史立即回到全 EXPECTED、汇总 148/148。**不制造无谓的历史失效**优于事后登记失效签名；向后兼容是新增判据的默认义务。
- **本轮改动边界与自检**：新增 `verify_cover_v3.py`、`cover_v2_fingerprint.json`；改 `recover_cover_hits.py`、`verify_all.py`、`run_pipeline.sh`、skill 六件。主表 候选池主表（2,494,073 B / `a9c0195044c0`）与证据簿（5,264,637 B / `791f7740ad97`）**零改动**。`run_pipeline.sh --verify-only` 三分支 RC=0/3/0、`PIPELINE_OK`；`verify_all.py` 活跃 148/148、`--include-legacy` 10 套全 EXPECTED、`--self-test` 5/5 + binding 2/2、`--binding-only` 8/8。skill 升 v1.4.8（新增 4 条硬规则、检查表第 20 段）。

## 2026-11-12 第十九轮（第三批）：活跃套发现盲区、窗口上限充分性、端到端报告演练

- **自动发现的 glob 本身就是盲区**：`verify_all.py` 只匹配 `verify_round*.py` / `audit_round*.py`，`verify_cover_v3.py`（不带轮次编号）虽然已挂在 `[3c]` 常驻，却始终不在 `verify_all.py --list` 的活跃集合里——「常驻」和「纳入单一入口」是两件事。修法不是改文件名，而是把发现逻辑抽成 `discover_suites()`，把该脚本作为 `active` 的显式成员追加；**即使注入的路径不存在也保留在列表里**，让 `run_suite` 判 FAIL，若用 `if p.exists()` 过滤就会静默跳过、注入演练恒绿。注入四段实证：伪造脚本（输出 `RESULT 1/2`）RC=1、路径缺失（python 报 can't open file）RC=1、`--include-legacy` 同样 RC=1、还原 RC=0；活跃行数 3→4、判据 148→187。`--self-test` 新增的 `SUITE_SELFTEST` 检查的是 `discover_suites()` 的**返回**，不是「常量里写了这个名字」——后者又是恒绿。
- **「N 已够用」必须靠 N+4 实测，不能靠直觉**：窗口 4 → 8 新增 2 刊后，不能就此断言 8 是上限。用 `COVER_WINDOW_MAX=12 COVER_OUT=v12` 再跑一次纯分析，逐项比对：命中集合 364→364（双向差集均为空）、剔除集合 86→86（对称差 0）、新增刊集合完全相同、逐本命中封面数下降 0 本、无清单外新命中 → 才写「8 已是充分上限」。`verify_cover_v3.py --window-bound` 把这套判据做成 11 条可判定检查（50/50），并支持 `--v12 PATH` 注入；`--self-test` 7/7（含改上限、删一条命中两个新注入），CLI 注入 `49/50 V3_FAIL` RC=1。**纯分析产物必须只写新文件**，v1/v2/映射/主表/证据簿五件由 `基线备份/cover_v2_fingerprint.json` 逐件比对零改动。
- **报告端演练要从「内存构造」升级到「输出链落盘」**：第十九轮上半场的 `--smoke` 只在内存里造结构化清单，能证明判据写得对，不能证明「按 skill 工作流真的产出的报告」也过得了校验。本批新增 `--full-smoke`：从主表 `逐刊明细` 实读行 2 / 313 / 741 的真实刊名（`CA-A CANCER JOURNAL FOR CLINICIANS`、`General Psychiatry`、`Medical Sciences`），生成脱敏稿件画像 → 三档候选 → 报告第 6 节「候选池与口径」（绝对路径、sheet、4399×42、MD5 `a9c0195044c0`、读取日期、逐本行号回指、主表外候选 0），落盘到项目内 `演练报告/` 且**幂等**（内容相同不改写，实测复跑「报告改写=False 清单改写=False」）。校验器 `--report` 扩展支持 `.json`（43/43，连带查同目录 md）、`.md`（33/33，读同目录清单做行号逐本比对）、`.docx`。注入抹掉 MD5 / 删一个行号 / 改路径，三条都判到**具体判据名**；另外把落盘报告真的改掉再跑 `--report` → `ALL_CHECKS FAILED 32/33`、RC=1，恢复 → RC=0。**演练产物必须显式标注「非交付 / 不构成投稿建议」**，否则容易被误当真实择刊报告。
- **新增自测输出仍要向后兼容**：本批又给 `--self-test` 加了 `SUITE_SELFTEST OK (2 cases)` 一行，`SELFTEST OK (5 cases)` 保持原样不动，`verify_round17.py` 的 `P3 self-test 5/5` 继续 PASS，`--include-legacy` 10 套历史仍全 EXPECTED。上批定的规则在本批再次生效。
- **本批改动边界**：新增 `douyin_full_cover_hits_v12.json`、`演练报告/择刊演练报告.md`、`演练报告/择刊演练_候选池清单.json`；改 `verify_all.py`、`verify_cover_v3.py`、`run_pipeline.sh`、`scripts/candidate_pool_check.py`、SKILL.md（v1.4.9，3 条硬规则 + 检查表第 21 段）、`references/journal-verification.md`。主表 2,494,073 B / `a9c0195044c0`、证据簿 5,264,637 B / `791f7740ad97` 零改动。`run_pipeline.sh [3c]` 常驻加 `--full-smoke` 与 `--window-bound`，三分支 RC=0/3/0。

## 2026-11-12 第十九轮（第四批）：模板七项字段、主表指纹硬判据、带参活跃套与第三次注入假绿

- **「模板写了」不等于「报告会写」**：上半场把第 6 节七项必填字段做进了演练报告（`演练报告/择刊演练报告.md`），正式模板 `references/output-template.md` 第 6 节却只有散落的叙述句——「唯一初筛源」「必写：文件大小、mtime、MD5…」「每本候选刊必须写主表行号」混在五个 bullet 里，没有任何一条可以逐项判定的锚点；`candidate_pool_check.py` 对模板的判据只有两条全文 `in` 检查，抹掉表格里任何一行都会恒绿。修法：模板新增 `F1`–`F7` 七行锚点表（F1 绝对路径 / F2 sheet / F3 行列数 / F4 MD5 指纹 / F5 读取日期 / F6 逐本主表行号 / F7 主表外候选 0），校验器按行取锚点 + 同时核对该行的语义 token；每次基础自检在内存里跑七次「删掉某一行」，断言**仅对应那一条判据 FAIL**，另加一条「原模板全绿」。实证：基础自检 24→**43/43**；`--template` CLI 注入 7 次全部 RC=1，FAIL 判据名精确对应 `模板七项必填 F1 候选池绝对路径`…`F7 主表外候选`，还原 RC=0。**规则类自检的判据粒度必须细到「删掉这一条就只有这一条红」。**
- **主表被改动原来根本挡不住**：`candidate_pool_check.py` 第 1 段只把实读 MD5 打印在 `主表非空` 的 detail 里，没有任何「MD5 == 登记值」的断言；主表被换成另一份可正常读取的 xlsx，基础自检仍全绿，只有报告端「清单 MD5 与实读不一致」会红——而报告端清单是择刊时新生成的，MD5 也会跟着实读，等于两端都不设防。修法：登记值从项目内持久清单 `基线备份/cover_v2_fingerprint.json` 的 `文件['候选池主表']['MD5'][:12]` 读取，新增硬判据 `主表指纹与已审定基线一致`；合法数据更新必须显式更新持久清单。注入演练用 ZIP 尾部追加 1 字节的副本（实测 openpyxl 仍可读出 9 sheet / 4399×42 / B2 刊名，MD5 `a9c0195044c0`→`9f5bf502a621`）：`--main 副本 --report 伪造清单.json` 同时判 `主表指纹与已审定基线一致` 与 `报告·MD5 与实读一致` 两条 FAIL、RC=1；只跑基础自检仅第一条 FAIL；恢复 RC=0、真主表 MD5 不变。
- **注入演练多出的两条 FAIL 暴露了判据漂移**：首版 `--main` 注入还额外判 `工作流第 2 步绑定主表`、`候选池唯一来源节绑定主表` FAIL——这两条用的是 `MAIN_STR in wf/pool`，注入后 `MAIN_STR` 变成副本路径，SKILL.md 里当然没有。**规则文本判据必须用 `DEFAULT_MAIN_STR`（固定真主表路径）比对**，不能随数据注入漂移；否则注入演练的 FAIL 集合被噪声污染，无法证明「只有指纹判据挡住」。修后 FAIL 集合精确为 2 条（含报告）/ 1 条（仅基础自检）。
- **带参活跃套的第三次假绿：常量定义了，主流程没用**：`verify_all.py` 把 `--window-bound`（50/50）与 `--full-smoke`（24/24）纳入 `active`，元素统一为 `(路径, 参数, 显示名)` 三元组，`run_suite` 拼 `[解释器, 路径] + 参数`，`--list` 打印显示名；`--full-smoke` 分支补一行 `RESULT 24/24` 供 `parse()` 汇总。活跃套 3→5、判据 **187→261/261**、`--include-legacy` 10 套仍全 EXPECTED。但 `--v12` 注入首版只定义了 `V12` 常量、主流程 `discover_suites()` 无参调用没接默认值 → `--v12 伪造产物` 时 `--window-bound` 仍 50/50、整体 RC=0 恒绿；`PARAM_SELFTEST` 当时只检查显式 `discover_suites(v12=fake)` 的构造结果，也判 PASS。**修法双重**：① `discover_suites()` 内 `if v12 is None: v12 = V12`，无参默认调用自动吃 CLI；② 自测新增「主流程默认 `discover_suites()` 的返回必须含 `--v12` 路径」判据，`PARAM_SELFTEST` 5→6 cases。修后注入 `RESULT 49/50`、RC=1；`--full-suite` 伪造脚本 RC=1、`--bound-suite` 缺失 RC=1、还原 RC=0。**这是同一类事故第三次（第一次 `--patch-dir` 只认等号、第二次删调用没删干净、这次常量没接默认值）：注入开关必须验证到达「实际执行路径」，不是到达「某个变量」。**
- **本批边界与自检**：改 `references/output-template.md`、`scripts/candidate_pool_check.py`、`SKILL.md`（v1.4.10，3 条硬规则 + 检查表第 22 段）、`verify_all.py`、`run_pipeline.sh`（预检四段自测标记、`[3b]` 文案带参套）、本核验文档；备份 `基线备份/*.pre_r19c` 四件。`--self-test` 5/5 + binding 2/2 + suite 2/2 + param 6/6；`run_pipeline.sh --verify-only` 三分支 RC=0/3/0、`PIPELINE_OK`。主表 候选池主表 2,494,073 B / `a9c0195044c0`、证据簿 5,264,637 B / `791f7740ad97`、剔除清单 29,192 B / `a26f25147840` **零改动**；演练报告与候选池清单幂等（内容不变不改写）。

## 2026-11-13 第二十轮：Word 报告恒绿、指纹更新后门、注入演练一键化

- **「支持 .docx」不等于「检查了 .docx」**：`check_docx()` 原来只判四个关键词（`候选池与口径` / 主表文件名 / `主表行号` / `MD5`）是否出现在全文里。抹掉 F1 绝对路径、写错 F4 的 MD5、删掉 F6 行号、把 F7 改成 1，全部仍判 PASS——这是第四类假绿（前三次：`--patch-dir` 只认等号、删调用没删干净、`--v12` 常量没接默认值）。修法：按 `w:p` 取段落，从「候选池与口径」段定位到第 7 节「隐私说明」段，**逐项按值判**：F1 绝对路径等于默认主表、F2 sheet、F3 4399×42、F4 MD5 与实读一致、F5 日期、F6 行号集合与候选池清单逐本一致、F7 池外 0，外加三档刊名与档位逐本出现。原样 `--report R.docx` **66/66**，`--docx-smoke` 八段注入 **22/22**。
- **第五类假绿：路径里的日期把 F5 判据骗过**：第一版 F5 用 `re.search(r'\d{4}-\d{2}-\d{2}', sec)` 对整节匹配，而主表绝对路径含 `2026-10-03-11-11-38`，抹掉 `F5 读取日期：2026-11-13` 后仍匹配 `2026-10-03` → `bad=[]`、注入演练判 FAIL（即判据恒绿）。修法：按「读取日期」所在行单独判，`check_md_report()` 同病同治，并新增 `FULL 注入4：抹掉 F5 读取日期须 FAIL`。**凡「某字段是否存在」的判据，必须把作用域收缩到该字段所在行/单元格，不能对整节全文匹配**——路径、版本串、历史日期都会成为假阳性来源。
- **指纹更新通道最大风险是「静默洗白」**：v1.4.10 加了 `主表指纹与已审定基线一致` 硬判据；若再开一个自动更新口子，篡改主表后自检可能自己把基线改成新值，前后都全绿，等于把唯一硬判据废掉。设计必须五重约束：① 只在显式 `--update-fingerprint` 时执行，基础自检另起子进程实证「指纹不一致时不会自动洗白清单」（副本字节前后一致）；② `--reason` 非空；③ 写前备份旧清单 + 追加 `*_history.jsonl`（时间/原因/旧新 MD5/主表源/备份路径）；④ 其他四件指纹逐件实读比对，**任一漂移即整体拒绝**，禁止借更新重写整份基线；⑤ 主表指纹无变化时不写盘。副本演练四分支 RC=**1/1/0/0/1**（不一致 FAIL / 无 reason FAIL / 显式更新 OK / 复检 OK / 漂移拒绝），真清单 mtime `Nov 12 20:45:46` 与 MD5 零改动。
- **注入演练要一键化，且注入构造必须「结构正确」**：历次手工跑的注入段无法复现、也没进链路。新增 `抖音采集/tools/injection_drill.py`，十段注入 + 一段还原，`INJECTION_DRILL OK 12/12`，挂 `run_pipeline.sh --verify-only` 的 `[3d]` 独立 RC。首版 D3 用空 `{}` 当伪造 v12 → `verify_cover_v3.py` 直接 `KeyError: '命中明细'`、**无 RESULT 输出**，虽然 RC=1 但那是演练构造错误，不是「窗口上限判据挡住了」；改为复制真 v12 产物、只把 `命中明细[0]['期刊']` 改成假刊名，才得到 `RESULT 48/50` 的可判定 FAIL。**注入演练判 RC=1 不够，还要证明目标判据确实掉分。**
- **演练产物与边界**：`--full-smoke` 现在幂等生成 `演练报告/择刊演练报告.docx`（已存在且机检全绿则不重建，避免 Word 生成时间戳导致每次改写）；`patch_docx()` 重写 zip 时保留目录条目（第十八轮经验复用）。本轮改 `scripts/candidate_pool_check.py`（新增 `--fingerprint` / `--update-fingerprint` / `--reason` / `--docx-smoke` / `--no-recursive-drill`）、新增 `抖音采集/tools/injection_drill.py`、改 `run_pipeline.sh`（预检加 docx 依赖与 `--list` 检查、`[3c-2]`、`[3d]`）、`SKILL.md` v1.4.11（3 条硬规则 + 检查表第 23 段）、`references/output-template.md`、本核验文档。`verify_all.py` 活跃 **275/275** + `--include-legacy` 10 套历史全 EXPECTED、自测 5/5 + 2/2 + 2/2 + 6/6；`run_pipeline.sh --verify-only` 三分支 RC=**0/3/0**、`PIPELINE_OK`；`--report` md 53/53、json 63/63、docx 66/66；基础自检 44/44、`--full-smoke` 38/38、`--docx-smoke` 22/22。三件成品零改动：主表 2,494,073 B / `a9c0195044c0`、证据簿 5,264,637 B / `791f7740ad97`、剔除清单 29,192 B / `a26f25147840`；备份 `基线备份/*.pre_round20` 四件。

## 2026-11-13 第二十一轮：单一入口覆盖盲区与回执绑定

- **「单一入口」名不副实**：第二十轮把 12 段注入演练固化进 `injection_drill.py` 并挂 `run_pipeline.sh [3d]`，但 `verify_all.py` 只跑 `verify_round*/audit_round*` 活跃套 + `patch_baseline_binding`。也就是说，**只跑单一入口时，注入演练的 12 段结论完全不在判据里**；而演练里所有「注入须 RC=1」都是针对当时的代码，代码一改没有任何东西会提醒重跑。这不是判据写错，是判据覆盖不到——属于覆盖盲区型的假绿，比前五类（参数没接、导入没删干净、常量没接默认值、全文关键词、整节日期正则）更隐蔽。
- **解法是「结果留痕 + 值级复核」，不是把演练塞进活跃套**：演练内部会多次调用 `verify_all.py`（D1/D3/D4/D5/D11），若把 `injection_drill.py` 直接纳入活跃套必然递归。改为：演练结束把 13 段结论（名称 / 通过 / 详情）+ 还原段 `ALL_CHECKS OK` + **11 件被验收文件 MD5** 写成 `演练报告/injection_drill_receipt.json`；`verify_all.py` 的 `drill_receipt_binding` 调 `injection_drill.py --receipt-check`（只读、不回调单一入口），逐项判状态 / 结果 `13/13` / 段目数量 / 段目全绿 / 段目前缀齐全 / 还原段可判定 / 条目数 / **每件 MD5 与当前实读一致**。任何被验收的数据或判据脚本改了而没重跑演练，单一入口立刻红。`--drill-receipt PATH` 让伪造/缺失回执可被端到端注入。
- **监控清单要精心划界，否则 bootstrap 死锁**：若把 `verify_all.py` / `run_pipeline.sh` / `injection_drill.py` 三件基础设施也纳入 MD5 快照，那么「改绑定脚本 → 回执失效 → 演练的 D11 调 `verify_all.py` 判红 → 演练永远写不出 OK 回执」。这三件改由 `--receipt-check` 的**静态绑定**覆盖（链路真执行行、RC 计入汇总、单一入口含 `drill_receipt_binding` 与 `--drill-receipt`、演练脚本含回执实现），并在 `run_pipeline.sh` 预检里再独立 grep 一遍，防「看门人自己被杀」。演练报告 md/json/docx 也不进快照（读取日期跨天会幂等重写），其内容由 D6/D9/D11 与 `--report` / `--docx-smoke` 逐项机检覆盖。预检**只做静态绑定不做动态 MD5 复核**，否则「回执失效 → 预检红 → 进不了 `[3d]` 刷新」又是一个死锁；动态复核交给严格模式的 `verify_all.py` 与链路末尾 `[3e]`。
- **两阶段 bootstrap，避免手写假回执**：先在 `verify_all.py` 尚未部署绑定判据时跑一次演练产出真回执（D10b 检测到 `drill_receipt_binding` 不存在就自动跳过端到端注入，并把 `e2e=OFF(bootstrap)` 写进 detail，不是静默跳过）；再部署判据，重跑演练时 `e2e=ON`，R1 指纹漂移与 R5 回执缺失两次端到端注入才启用。整个 bootstrap 没有手写过一份「合成全绿回执」当真回执；`probe_receipt()` 只用于 D10b 的注入基底，落在临时目录。演练崩溃或失败也必须把真回执写成 `FAILED`（`except` 加异常段 + `finally` 兜底），绝不沿用上一次 OK。
- **第六类假绿：`py_compile` 行冒充执行行**：`链路存在注入演练实际执行行` 首版用 `'injection_drill.py' in line and 'python3 ' in line`，实测匹配到的是预检里 `python3 -m py_compile ... "$T/injection_drill.py"` 那一行；把 `[3d]` 真执行行注释掉，判据仍 PASS。收紧为正则 `python3\s+"\$T/injection_drill\.py"` 并显式排除 `py_compile` / `--list` / `--receipt-check`，另加一条「演练 RC 计入汇总」判据；D10b 新增 P1：复制链路到临时目录、注释掉真执行行、用 `--pipeline-src` 注入，实证精确判 `FAIL | 链路存在注入演练实际执行行`。**教训：静态绑定判「A 真的执行了 B」，必须判执行形态，不能判文件名字面量出现。**
- **本轮边界与自检**：改 `抖音采集/tools/injection_drill.py`（回执写盘 / `--receipt-check` / `--pipeline-src` / D10b / 异常兜底）、`抖音采集/tools/verify_all.py`（`--drill-receipt` + `drill_receipt_binding` + 汇总 `+ 2 binding`）、`抖音采集/tools/run_pipeline.sh`（预检 3 条静态绑定、`[3e]`、`RC8`）、`SKILL.md` v1.4.12（2 条硬规则 + 检查表第 24 段）、本核验文档；新增 `演练报告/injection_drill_receipt.json`；备份 `基线备份/*.pre_round21` 五件。`--receipt-check` 14/14、`INJECTION_DRILL OK 13/13`（e2e=ON）、`verify_all.py` 活跃 **289/289** + `--include-legacy` 10 套全 EXPECTED、自测 5/5 + 2/2 + 2/2 + 6/6、`run_pipeline.sh --verify-only` 三分支 RC=**0/3/0**、`PIPELINE_OK`。三件成品零改动：主表 `a9c0195044c0`、证据簿 `791f7740ad97`、剔除清单 `a26f25147840`。
