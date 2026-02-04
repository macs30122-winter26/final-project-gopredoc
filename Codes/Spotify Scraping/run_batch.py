"""
Batch execution script - generate all crawling commands
Usage: python run_batch.py
"""

from config import ALL_REGIONS, START_YEAR, START_MONTH, END_YEAR, END_MONTH


def generate_commands():
    """Generate all crawling commands"""
    commands = []

    for region in ALL_REGIONS:
        for year in range(START_YEAR, END_YEAR + 1):
            start_m = START_MONTH if year == START_YEAR else 1
            end_m = END_MONTH if year == END_YEAR else 12

            for month in range(start_m, end_m + 1):
                commands.append(f"python scraper.py {region} {year} {month}")

    return commands


def main():
    commands = generate_commands()

    print(f"Total months to crawl: {len(commands)}")
    print(f"Number of regions: {len(ALL_REGIONS)} (1 global + {len(ALL_REGIONS) - 1} countries)")
    print(f"Time range: {START_YEAR}-{START_MONTH:02d} ~ {END_YEAR}-{END_MONTH:02d}")
    print()


    with open('commands.txt', 'w') as f:
        for cmd in commands:
            f.write(cmd + '\n')

    print("All commands have been saved to commands.txt")
    print()
    print("Example commands:")
    for cmd in commands[:5]:
        print(f"  {cmd}")
    print("  ...")
    print()
    print("How to run:")
    print("  1. Run manually: python scraper.py global 2024 1")
    print("  2. Run sequentially: copy and execute commands from commands.txt one by one")


if __name__ == '__main__':
    main()
