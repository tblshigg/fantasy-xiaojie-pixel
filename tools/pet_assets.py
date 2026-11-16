"""Inspect, extract, preview, and package the existing pixel companion artwork.

These tools manipulate generated pixels only. Format validation does not replace
visual review or the host application's pet validation/moderation.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
import zipfile

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ATLAS = ROOT / "assets/fantasy-xiaojie-v2.png"
CELL = (192, 208)
STATES = ["idle", "running-right", "running-left", "waving", "jumping", "failed", "waiting", "running", "review", "look-row-9", "look-row-10"]
COUNTS = [6, 8, 8, 4, 5, 8, 6, 6, 6, 8, 8]
DURATIONS = [[280,110,110,140,140,320], [120]*7+[220], [120]*7+[220], [140]*3+[280], [140]*4+[280], [140]*7+[240], [150]*5+[260], [120]*5+[220], [150]*5+[280], [180]*8, [180]*8]


def read_atlas(path: Path) -> tuple[Image.Image, int]:
    with Image.open(path) as source:
        if source.format not in {"PNG", "WEBP"}:
            raise ValueError("Use a transparent PNG or WebP sprite sheet.")
        image = source.convert("RGBA")
    if image.size not in {(1536,1872), (1536,2288)}:
        raise ValueError(f"Unsupported dimensions: {image.size}; expected v1 1536x1872 or v2 1536x2288.")
    return image, image.height // 208


def cell(image: Image.Image, row: int, col: int) -> Image.Image:
    return image.crop((192*col,208*row,192*(col+1),208*(row+1)))


def validate(path: Path) -> dict:
    image, row_count = read_atlas(path)
    errors = []
    used = 0
    for row in range(row_count):
        for col in range(8):
            alpha = cell(image,row,col).getchannel("A")
            visible = sum(alpha.histogram()[1:])
            if col < COUNTS[row]:
                used += 1
                if visible < 400:
                    errors.append(f"Required row {row}, frame {col} is empty or too sparse.")
                if alpha.getextrema()[0] == 255:
                    errors.append(f"Row {row}, frame {col} has a fully opaque background.")
            elif visible:
                errors.append(f"Unused row {row}, frame {col} must be transparent.")
    size = path.stat().st_size
    if not 0 < size <= 20*1024*1024:
        errors.append("Encoded file must be between 1 byte and 20 MiB.")
    return {"ok":not errors, "file":path.name, "sprite_version":2 if row_count==11 else 1, "width":image.width, "height":image.height, "frames":used, "encoded_bytes":size, "sha256":hashlib.sha256(path.read_bytes()).hexdigest(), "errors":errors, "scope":"Format and integrity only; inspect actual motion and host compatibility separately."}


def extract(path: Path, output: Path) -> None:
    image, rows = read_atlas(path)
    for row in range(rows):
        folder = output / STATES[row]
        folder.mkdir(parents=True,exist_ok=True)
        for col in range(COUNTS[row]):
            cell(image,row,col).save(folder/f"{col:02d}.png")


def panel(frame: Image.Image, label: str) -> Image.Image:
    canvas = Image.new("RGB",(240,248),"#f5f1eb")
    canvas.paste(frame,(24,32),frame)
    ImageDraw.Draw(canvas).text((12,10),label,fill="#54434b")
    return canvas


def save_gif(frames: list[Image.Image], durations: list[int], output: Path) -> None:
    frames[0].save(output,save_all=True,append_images=frames[1:],duration=durations,loop=0,disposal=2,optimize=False)


def previews(path: Path, output: Path, video: bool) -> None:
    image, rows = read_atlas(path)
    output.mkdir(parents=True,exist_ok=True)
    all_frames, all_times = [], []
    for row in range(min(rows,9)):
        frames=[panel(cell(image,row,col),STATES[row]) for col in range(COUNTS[row])]
        save_gif(frames,DURATIONS[row],output/f"{STATES[row]}.gif")
        all_frames.extend(frames)
        all_times.extend(DURATIONS[row])
    save_gif(all_frames,all_times,output/"all-states.gif")
    jump=[panel(cell(image,0,0),"idle / jump / idle")]*2+[panel(cell(image,4,c),"idle / jump / idle") for c in range(5)]+[panel(cell(image,0,0),"idle / jump / idle")]*2
    save_gif(jump,[280,280]+DURATIONS[4]+[280,280],output/"idle-jump-idle.gif")
    if rows == 11:
        look=[panel(cell(image,9+i//8,i%8),f"look {i*22.5:g}") for i in range(16)]
        save_gif(look,[180]*16,output/"look-loop.gif")
    contact=Image.new("RGB",(8*192,rows*232),"#f5f1eb")
    draw=ImageDraw.Draw(contact)
    for row in range(rows):
        for col in range(COUNTS[row]):
            frame=cell(image,row,col)
            contact.paste(frame,(col*192,row*232+24),frame)
            draw.text((col*192+6,row*232+6),f"{STATES[row]} {col}",fill="#54434b")
    contact.save(output/"contact-sheet.png")
    stills=Image.new("RGB",(960,248),"#f5f1eb")
    for i,(row,col,label) in enumerate([(0,0,"Idle"),(3,1,"Wave"),(4,2,"Jump"),(7,2,"Thinking")]):
        stills.paste(panel(cell(image,row,col),label),(240*i,0))
    stills.save(output/"four-states.png")
    if video:
        try:
            import imageio_ffmpeg
        except ImportError as exc:
            raise ValueError("Video export needs: python -m pip install -r requirements-video.txt") from exc
        encoded=[frame.resize((480,496),Image.Resampling.NEAREST) for frame in all_frames]
        writer=imageio_ffmpeg.write_frames(str(output/"all-states.mp4"),(480,496),fps=20,codec="libx264",pix_fmt_out="yuv420p")
        writer.send(None)
        try:
            for frame,ms in zip(encoded,all_times):
                for _ in range(max(1,round(ms/50))):
                    writer.send(frame.tobytes())
        finally:
            writer.close()


def package(output: Path) -> dict:
    allowed_dirs={"assets","previews","sources","prompts","metadata","tools","docs"}
    allowed_files={"README.md","README.en.md","LICENSE","NOTICE.md","CHANGELOG.md","requirements.txt","requirements-video.txt","install.html",".gitignore",".gitattributes"}
    selected=[]
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.resolve()==output.resolve():
            continue
        rel=path.relative_to(ROOT)
        if "__pycache__" in rel.parts or path.suffix==".pyc":
            continue
        if rel.parts[0] in allowed_dirs or rel.as_posix() in allowed_files:
            selected.append((path,rel.as_posix()))
    output.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(output,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for path,name in selected:
            entry=zipfile.ZipInfo(f"fantasy-xiaojie-pixel/{name}",date_time=(2026,11,16,0,0,0))
            entry.compress_type=zipfile.ZIP_DEFLATED
            entry.external_attr=0o100644 << 16
            archive.writestr(entry,path.read_bytes())
    return {"ok":True,"archive":output.name,"files":len(selected),"bytes":output.stat().st_size,"sha256":hashlib.sha256(output.read_bytes()).hexdigest()}


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--atlas",type=Path,default=DEFAULT_ATLAS)
    commands=parser.add_subparsers(dest="command",required=True)
    commands.add_parser("validate",help="Check sprite dimensions, used/unused cells, transparency, size and hash.")
    for name in ["extract","previews","package"]:
        sub=commands.add_parser(name)
        sub.add_argument("--output",type=Path,required=True)
        if name=="previews":
            sub.add_argument("--video",action="store_true")
    args=parser.parse_args()
    try:
        if args.command=="validate":
            result=validate(args.atlas)
        elif args.command=="extract":
            extract(args.atlas,args.output)
            result={"ok":True,"output":str(args.output)}
        elif args.command=="previews":
            previews(args.atlas,args.output,args.video)
            result={"ok":True,"output":str(args.output)}
        else:
            result=package(args.output)
        print(json.dumps(result,ensure_ascii=False,indent=2))
        return 0 if result["ok"] else 1
    except (OSError,ValueError) as exc:
        print(json.dumps({"ok":False,"error":str(exc)},ensure_ascii=False),file=sys.stderr)
        return 1


if __name__=="__main__":
    raise SystemExit(main())
