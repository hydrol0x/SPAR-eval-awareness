"""Bundle the night-2 figures (PREREG_night2.md) into one PDF with a cover page and a caption per figure.

  python -m src.plot_night2 && python3 -m src.make_night2_pdf      # writes figures/night2_results.pdf (needs reportlab)
"""
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"
INK, INK2 = HexColor("#0b0b0b"), HexColor("#52514e")

COVER = [
    "<b>Team judge, same answer.</b> Re-judged with the Goodfire eval-awareness template, Experiment 1 is unchanged: under eval "
    "cues the CoT-controllable LoRA verbalizes eval awareness as often as its matched control (−0.1 pp) and raises refusal as "
    "much (+0.2 pp). The earlier judge over-counted awareness when the model merely restated \"the user is a METR researcher\".",
    "<b>\"It's a test, so I should be safe\" is the norm.</b> About 94% of rollouts that verbalize eval awareness explicitly tie it "
    "to how they respond, in every arm.",
    "<b>No propensity to hide.</b> Told that their reasoning is being monitored for misbehaviour, all five arms verbalize "
    "awareness as much as or more than with a plain eval cue, and refuse the most of any cue.",
    "<b>Trying to hide gives it away.</b> Told that mentioning evaluation will be penalized, the models still verbalize awareness "
    "in 22–42% of rollouts, mostly by restating the rule while planning to obey it; their refusal increase shrinks to about "
    "+7 pp.",
    "<b>Capability to hide is not improved by CoT control.</b> Asked not to mention being tested, every arm drops verbalized "
    "awareness by 5–19 pp; neither the edited LoRA nor the edited steering vector does better than its control.",
    "<b>Steering reproduces the controllability gain</b> (20.5% vs 6.7% rule compliance; card 24.5%) but, like the LoRA, does "
    "not change eval-awareness behaviour beyond two weak, uncorrected contrasts.",
    "<b>Paper prompts do not raise CoT controllability here.</b> The CoT-Control paper's two situational-awareness prompts, the "
    "\"desired behavior\" sentence alone and \"monitored for misalignment\" all leave rule compliance unchanged in base, edited "
    "and control.",
]
CAVEATS = ("Judge: Qwen2.5-72B-Instruct (FP8), the team's templates verbatim plus a second \"VERDICT\" turn; a positive label "
           "needs a quote found in the text. The eval-gaming template was dropped after the pilot (labels not reliable with this "
           "judge). Refusal from the earlier provisional judge. Adversarial FORTRESS (282 prompts, CBRNE excluded), sample 0, "
           "paired by prompt; 95% bootstrap CIs; contrasts exploratory, not corrected across the night. Details: PREREG_night2.md, "
           "results/night2_summary.md, results/exp3_summary.md.")

PAGES = [
    ("night2_judges.png", "Experiment 1 re-judged with the team judge",
     "Verbalized eval awareness per cue, team judge vs provisional judge. They agree on most cues (κ 0.57–0.73); the team judge "
     "rejects restatements of the METR cue (29% vs 94%). Conclusions of Experiment 1 are unchanged (edited − control: −0.1 pp VEA, "
     "+0.2 pp refusal increase)."),
    ("night2_pressure.png", "Pressure test: monitoring and penalty cues",
     "A: verbalized awareness; B: refusal increase over no cue; C: share of aware rollouts that link \"this may be a test\" to the "
     "response. All arms behave alike. Monitoring raises both awareness and refusal; the penalty cue cuts the refusal increase "
     "and the stated link, because most remaining mentions restate the penalty rule."),
    ("night2_hiding.png", "Hiding eval awareness: propensity vs capability",
     "Change in verbalized awareness against the plain explicit cue (same prompt, same placement). No arm hides spontaneously "
     "under monitoring; the penalty cue and an explicit \"don't mention\" instruction lower it in every arm, and the "
     "CoT-controllable arms are no better at it than their controls."),
    ("night2_steering.png", "Steering arms: CoT controllability",
     "The model card's steering recipe (layer 27, edited vector ×1.5, norm-matched control ×4.5), served in vLLM with a forward hook "
     "checked against the card's Transformers hook (slope 1.00, r = 0.995). The steering gain reproduces (20.5% vs 6.7%)."),
    ("night2_mechanism.png", "Mechanism test: the CoT-Control paper's situational-awareness prompts",
     "Each prompt appended to the end of the user turn, as in the paper. None changes rule compliance in any arm (all within "
     "about ±2 pp), including the edited LoRA, which follows the trained rules 38% of the time with no prompt, so this is not a "
     "floor effect. The \"tries harder on the task\" explanation cannot be tested when the prompts have no effect to explain."),
]


def main():
    out = FIG / "night2_results.pdf"
    doc = SimpleDocTemplate(str(out), pagesize=landscape(letter), leftMargin=0.5 * inch, rightMargin=0.5 * inch,
                            topMargin=0.45 * inch, bottomMargin=0.45 * inch,
                            title="Olmo-3.1 CoT controllability and eval awareness: night 2 results")
    ss = getSampleStyleSheet()
    h = ParagraphStyle("h", parent=ss["Heading2"], textColor=INK, spaceAfter=4)
    t = ParagraphStyle("t", parent=ss["Title"], textColor=INK, alignment=0, fontSize=20, leading=24)
    body = ParagraphStyle("b", parent=ss["BodyText"], textColor=INK, fontSize=10.5, leading=14, spaceAfter=7)
    small = ParagraphStyle("s", parent=body, textColor=INK2, fontSize=9, leading=12)
    W, H = doc.width, doc.height
    story = [Paragraph("Olmo-3.1-32B-Think: does CoT control help a model hide eval awareness?", t),
             Paragraph("Night 2 results: team judge, pressure test, steering arms, mechanism test (branch eval-awareness-cot-control-exp)", small),
             Spacer(1, 12)]
    story += [Paragraph("• " + c, body) for c in COVER]
    story += [Spacer(1, 8), Paragraph(CAVEATS, small), PageBreak()]
    for i, (fn, title, cap) in enumerate(PAGES):
        story += [Paragraph(title, h), Paragraph(cap, small), Spacer(1, 6)]
        img = Image(str(FIG / fn)); iw, ih = img.imageWidth, img.imageHeight
        scale = min(W / iw, (H - 1.25 * inch) / ih)
        img.drawWidth, img.drawHeight = iw * scale, ih * scale
        story.append(img)
        if i < len(PAGES) - 1:
            story.append(PageBreak())
    doc.build(story)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
