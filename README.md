# Hinglishify

Hinglishify is a Codex skill that interprets DOCX and PDF documents into accurate, natural, Hindi-script Hinglish while preserving the source document's meaning, context, formatting, fonts, tables, images, headers, footers, and page design.

It is an interpreter rather than a literal translator. The objective is to make complex study material, technical documentation, books, and professional documents easier to read without changing what the author meant.

## Core principles

- Preserve the complete meaning, context, intent, tone, qualifications, and technical distinctions.
- Use natural Hindi grammar with familiar English technical vocabulary.
- Write Hindi words in Devanagari and preserve code, identifiers, commands, URLs, and product names exactly.
- Do not summarize, omit, expand, correct, or add information.
- Preserve fonts, font sizes, styles, tables, images, and page design.
- Render and visually inspect the complete output before delivery.
- Keep embedded images byte-identical unless the user explicitly authorizes diagram localization.

## Repository structure

```text
hinglishify/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   └── hinglish-style.md
└── scripts/
    └── audit_docx_pair.py
```

`SKILL.md` contains the interpretation and document-fidelity workflow. The style reference defines the default Hinglish register. The audit script compares fidelity-sensitive DOCX internals between the source and interpreted output.

## Installation

Copy this repository into your local Codex skills directory:

```bash
cp -R /path/to/Hinglishify-skill ~/.codex/skills/hinglishify
```

Restart or refresh Codex after installation.

## Usage

Attach a DOCX or PDF and invoke the skill:

```text
Use $hinglishify to interpret this document into accurate, easy-to-read Hinglish without changing its meaning, context, formatting, fonts, or images.
```

You can also state image-handling preferences explicitly:

```text
Use $hinglishify. Keep embedded diagrams exactly as they are, including any text baked into the images.
```

## DOCX fidelity audit

After producing an interpreted DOCX, compare it with the source:

```bash
python scripts/audit_docx_pair.py source.docx interpreted.docx
```

The audit checks embedded-media hashes and compares styles, numbering, settings, font tables, paragraphs, tables, drawings, and sections. It complements visual review; it does not replace rendering and inspecting every page.

## Current scope

- DOCX interpretation with layout-preservation and structural auditing
- Born-digital PDF interpretation using layout-aware reconstruction
- Scanned PDF handling through OCR, subject to the quality of the scan

Text embedded inside images remains unchanged by default. Interpreting that text requires explicit permission to modify image pixels.

## Limitations

Hinglish text can occupy a different amount of space from English text. Hinglishify first refines the wording into concise, equally accurate Hinglish without changing font settings. If accurate content cannot fit without a formatting change, the skill must report the constraint and obtain permission rather than shrinking, clipping, or omitting content.

Documents involving legal, medical, financial, safety-critical, or contractual decisions should receive qualified human review before use.

## Contributing

Useful contributions include new document-format support, stronger semantic-fidelity checks, improved handling of text boxes and footnotes, font-compatibility tests, and anonymized layout test cases.

Do not commit copyrighted books, paid course material, confidential documents, personal information, or source documents you do not have permission to redistribute.

