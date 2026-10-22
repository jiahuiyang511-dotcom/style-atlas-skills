# Style Atlas Skills · 视觉风格工具库

将已提炼的视觉风格用于 AI 设计与绘图 Prompt。

这里包含 MSI 2021、2022、2023、2024、2026 五套独立风格 Skill，用于将已提炼的视觉关系应用到具体设计任务。本仓库的首批发布范围只包含这五套风格 Skill；完整研究包与网站内容生产工作流保留本地。

[Style Atlas 展示网站](https://style-atlas-msi-2026.jiahuizz3.chatgpt.site/)

网站当前仍限制访问；本仓库内容可以独立使用，不要求访问网站。网站分享权限需另行配置。

## 选择需要的工具

| 主视觉 | Skill | 关键词 |
| --- | --- | --- |
| <a href="skills/msi-2021-visual-style/SKILL.md"><img src="skills/msi-2021-visual-style/assets/reference/official-03.jpg" alt="MSI 2021 主视觉预览" width="160" height="90"></a> | [msi-2021-visual-style](skills/msi-2021-visual-style/SKILL.md) | 灰阶撕接、窄高文字、倾斜放大口号与荧光绿注释 |
| <a href="skills/msi-2022-visual-style/SKILL.md"><img src="skills/msi-2022-visual-style/assets/reference/primer-02.jpg" alt="MSI 2022 主视觉预览" width="160" height="90"></a> | [msi-2022-visual-style](skills/msi-2022-visual-style/SKILL.md) | 笔记方格、柔和多色场、紧缩变形标题与像素阶梯 |
| <a href="skills/msi-2023-visual-style/SKILL.md"><img src="skills/msi-2023-visual-style/assets/reference/primer-02.png" alt="MSI 2023 主视觉预览" width="160" height="90"></a> | [msi-2023-visual-style](skills/msi-2023-visual-style/SKILL.md) | 红米白黑、几何字与签名笔迹、截断斜带与极窄大字 |
| <a href="skills/msi-2024-visual-style/SKILL.md"><img src="skills/msi-2024-visual-style/assets/reference/msi24-brand-expression-1-black-16x9.jpg" alt="MSI 2024 主视觉预览" width="160" height="90"></a> | [msi-2024-visual-style](skills/msi-2024-visual-style/SKILL.md) | 黑红锚点、宽重紧排字体、局部光谱异常边界与数据层级 |
| <a href="skills/msi-2026-visual-style/SKILL.md"><img src="skills/msi-2026-visual-style/assets/references/008.jpg" alt="MSI 2026 主视觉预览" width="160" height="90"></a> | [msi-2026-visual-style](skills/msi-2026-visual-style/SKILL.md) | 纸灰、红色硬边形态、规则信息与自由笔触的组合关系 |

## 下载

[打开最新版下载页](https://github.com/jiahuiyang511-dotcom/style-atlas-skills/releases/latest) · [全部版本](https://github.com/jiahuiyang511-dotcom/style-atlas-skills/releases)

| 风格 | 独立下载 |
| --- | --- |
| MSI 2021 | [下载完整 Skill ZIP](https://github.com/jiahuiyang511-dotcom/style-atlas-skills/releases/download/v1.0.0/msi-2021-visual-style.zip) |
| MSI 2022 | [下载完整 Skill ZIP](https://github.com/jiahuiyang511-dotcom/style-atlas-skills/releases/download/v1.0.0/msi-2022-visual-style.zip) |
| MSI 2023 | [下载完整 Skill ZIP](https://github.com/jiahuiyang511-dotcom/style-atlas-skills/releases/download/v1.0.0/msi-2023-visual-style.zip) |
| MSI 2024 | [下载完整 Skill ZIP](https://github.com/jiahuiyang511-dotcom/style-atlas-skills/releases/download/v1.0.0/msi-2024-visual-style.zip) |
| MSI 2026 | [下载完整 Skill ZIP](https://github.com/jiahuiyang511-dotcom/style-atlas-skills/releases/download/v1.0.0/msi-2026-visual-style.zip) |

发布附件中包含 SHA256SUMS.txt，供核对下载完整性。

## 使用

从本项目 Releases 下载对应 Skill ZIP，解压并保留整个 Skill 目录，包含 SKILL.md、references、assets 和已有 scripts。按所用智能体工具的 Skill 安装方式导入；不要只复制入口文件，否则可能缺少规则、模板和参考图。

例如：

> 使用 msi-2023-visual-style，为原创夜跑品牌设计一张 3:4 活动海报。标题为“夜行计划”，保留时间地点区。先建立信息层级和构图，再制作，并核对文字与风格关系。

只有文字能力时可交付设计方案；制作实际图片需要当前工具具备图像生成或设计能力。Skill 本身不包含模型或图像服务。这些风格 Skill 的使用不要求连接作者的网站。

## 更新与下载

源文件按 Skill 分目录维护；正式 ZIP 放 Releases 附件，不反复提交压缩包。下载时优先选定明确版本。网站可链接到对应版本的附件。后续新增风格沿用相同目录结构，并更新打包脚本中的风格清单。发布新 Release 时，GitHub Actions 会自动生成独立 ZIP 和校验文件；也可以在 Actions 中手动重新打包最近一次发布。

## 来源与边界

这些是独立研究与设计转译工具，并非赛事或品牌的官方 Skill。原图、商标及其他第三方素材仍归相应权利人；出处保留在各 Skill 的 references 中。具体字体、色号和动态行为的已验证范围以各 Skill 为准。参考图用于研究依据，制作时使用用户品牌和原创内容。

本次整理没有为原内容新增开源许可证，使用与再分发范围请参阅 [来源说明](SOURCE_NOTICE.md)。
