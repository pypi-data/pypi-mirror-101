import typer
from pathlib import Path
from datetime import datetime, timedelta

app = typer.Typer(add_completion=False)


def pretty_delta(delta: timedelta):
    if delta.seconds < 0:
        return "in the future"
    elif delta.seconds < 120:
        return f"{delta.seconds} seconds ago"
    elif delta.seconds < 60 * 120:
        return f"{delta.seconds // 60} minutes ago"
    else:
        return f"{delta.seconds // (60 * 60)} hours ago"


@app.command()
def main(
    destination: Path,
    markdown: bool = typer.Option(
        False,
        "-m",
        help="Print markdown to use image",
    ),
):
    pictures_path = Path.home() / "Pictures"
    screenshots = list(pictures_path.glob("Screenshot from *.png"))
    screenshots.sort()
    last_screenshot = screenshots[-1]
    last_date = datetime.strptime(
        last_screenshot.name, "Screenshot from %Y-%m-%d %H-%M-%S.png"
    )
    now = datetime.now()
    delta = now - last_date
    delta_text = pretty_delta(delta)
    if destination.suffix != last_screenshot.suffix:
        destination = destination.with_suffix(last_screenshot.suffix)
    print(f"Screenshot from {delta_text}")
    print(f"Move to: {destination}")
    confirm = input("Confirm [Y/n]: ")
    if confirm.lower() in {"y", "yes", ""}:
        last_screenshot.rename(destination)
    if markdown:
        if "docs" in destination.parts:
            docs_index = destination.parts.index("docs")
            docs_path = Path(*destination.parts[: docs_index + 1])
            relative_path = destination.relative_to(docs_path)
        else:
            relative_path = destination
        print("=" * 10)
        print(f'![Screenshot](/{relative_path} "Screenshot")')


if __name__ == "__main__":
    app()
