# Paper PPT Template

A Codex skill for turning research paper PDFs into Chinese presentation decks with a reusable 10-slide PowerPoint layout. It guides paper analysis, figure selection, concise slide writing, speaker notes, and visual checks. It is not tied to any research field.

## Use

Install this folder as `paper-ppt-template` in your Codex skills directory, then ask:

> 使用 paper-ppt-template，把这些论文 PDF 按模板做成 PPT，并加入逐页演讲备注。

The template contains generic placeholders only. Replace them with verified claims and figures from the supplied papers. For two papers, the default speaking time is about 6–7 minutes total unless the user specifies otherwise.

## Files

- `SKILL.md` — workflow and quality checks
- `assets/paper-template.pptx` — generic PowerPoint layout
- `upload_skill.py` — upload local skill updates to GitHub with `GITHUB_TOKEN` or `GH_TOKEN`

The template contains no presenter name, school, paper content, or personal speaker notes.

## Updating

```powershell
python upload_skill.py C:/Users/you/.codex/skills/paper-ppt-template --package-dir . --repo OWNER/paper-ppt-template --dry-run
python upload_skill.py C:/Users/you/.codex/skills/paper-ppt-template --package-dir . --repo OWNER/paper-ppt-template
```

## License

MIT. See `LICENSE`.