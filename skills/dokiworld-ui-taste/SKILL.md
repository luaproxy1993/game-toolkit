---
name: dokiworld-ui-taste
description: >-
  Apply Leonxlnx taste-skill standards to Dokiworld SillyTavern extension UI
  (连接室 HUD, 探索页, 心跳抉择, 付费弹层). Use when styling, redesigning, or
  polishing Dokiworld frontend in ST/SillyTavern, or when user mentions
  taste-skill + Dokiworld together.
---

# Dokiworld UI × Taste Skill

Premium **otome-lite game overlay** inside SillyTavern — not a marketing landing page.

## Required companion skills (read before editing CSS/JS UI)

1. `design-taste-frontend` — brief inference, three dials, anti-slop defaults
2. `imagegen-frontend-mobile` — app-native hierarchy, safe areas, multi-screen consistency
3. `high-end-visual-design` — double-bezel, hairlines, spring motion, banned cheap patterns
4. `redesign-existing-projects` — audit-first when touching existing `style.css`

Install source: https://github.com/Leonxlnx/taste-skill

## Design Read (declare before coding)

**Reading this as:** in-chat game overlay for romance/otome players, with a premium anime connection-room language, leaning toward soft structuralism + editorial luxury (warm dark violet, rose gold accents, not AI-purple SaaS gradients).

### Dials for Dokiworld

| Dial | Value | Rationale |
|------|-------|-----------|
| DESIGN_VARIANCE | 7 | Asymmetric floating panels, not centered hero blocks |
| MOTION_INTENSITY | 5 | Subtle spring on choice cards; no scroll-jacking |
| VISUAL_DENSITY | 4 | HUD readable; choices compact but not cramped |

## Target files

- `ST/SillyTavern/public/scripts/extensions/third-party/game-progress-video/style.css`
- `ST/SillyTavern/public/scripts/extensions/third-party/game-progress-video/dokiworld.js` (structure only)
- `manifest.json` display name: Dokiworld

## Anti-slop rules (Dokiworld-specific)

**Ban:**
- Full-width bottom sheets covering chat messages (use draggable side panel)
- Generic Inter/Roboto stacks (inherit `var(--SmartThemeFont)` / ST theme)
- Thick gray borders, harsh `box-shadow: 0 8px 28px rgba(0,0,0,.35)` on everything
- Purple-blue startup gradient clichés as the only brand move
- Glassmorphism on scrolling chat area

**Require:**
- **Double-bezel** on choice cards, explore cards, paywall modal (outer shell + inner core)
- **Hairline** borders `rgba(255,255,255,0.08)` not 1px solid gray
- **Spring easing** `cubic-bezier(0.32, 0.72, 0, 1)` on hover/active
- **Floating islands** — HUD, choices, video panel feel detached from chat canvas
- **Texture** — subtle noise or radial mesh at 3% opacity on panel backgrounds
- **Typography** — eyebrow labels (Episode, 心跳抉择), strong stat numerals, muted captions
- **Touch** — min 44px tap targets on choice buttons; `active:scale(0.98)`

## Component checklist

| Component | Taste contract |
|-----------|----------------|
| `#doki-hud` | Floating island, concentric radius, bond nodes as machined pills |
| `#doki-choices` | Draggable; header = `drag-grabber`; vertical stack; never cover last message by default (right rail) |
| `#doki-explore` | Card grid with cover art ratio 3:4; featured badge; one clear CTA |
| `#doki-paywall` | Editorial luxury: gold accent, blurred preview, single primary unlock CTA |
| `#gpv-panel` | Match Dokiworld palette; video cards with inner bezel |

## Pre-flight before shipping CSS

- [ ] No new UI blocks chat input or send button at default positions
- [ ] Choices panel draggable (`#doki-choicesheader` + `drag-grabber`)
- [ ] Palette consistent across HUD / choices / explore / paywall / gpv-panel
- [ ] Motion uses transform/opacity only
- [ ] Hard refresh tested in SillyTavern (Cmd+Shift+R)

## Update taste-skill

```bash
npx skills add https://github.com/Leonxlnx/taste-skill -y
# project: cd ST/SillyTavern && npx skills add ...
# global agents: ~/.agents/skills/
```