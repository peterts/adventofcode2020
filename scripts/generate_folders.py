from pathlib import Path

if __name__ == "__main__":
    for i in range(1, 26):
        folder_for_day = Path(__file__).parents[1] / "data" / f"day{i}"
        folder_for_day.mkdir(exist_ok=True, parents=True)
        (folder_for_day / "sample1.txt").write_text("")
        (folder_for_day / "sample2.txt").write_text("")
