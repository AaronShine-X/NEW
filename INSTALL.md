# 安装小红 Skill

将本仓库克隆或下载后，把仓库内容放入 Codex 技能目录：

```text
~/.codex/skills/小红/
├── SKILL.md
├── references/
└── scripts/
```

使用腾讯文档相关能力时，目标环境需另行安装并配置腾讯文档工具。真实工作簿名、sheet ID、token、cookie 和账号信息只应保存在私有本地配置或目标环境凭据中，不要提交到本仓库。

可复制 `config/tencent-docs.example.json` 为 `config/tencent-docs.local.json`，再在本地填写真实腾讯文档路由。`config/*.local.json` 已被 `.gitignore` 排除。
