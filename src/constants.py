NUM_BLOCKS = 26
# mon 8am + 105 hours = fri 5pm
# 105 = 4 * 24hr + (17hr - 8hr)
WEEK_HOURS = 24 * 4 + (17 - 8)

# fri 5pm + 63 hours = mon 8am
WEEKEND_HOURS = 24 * 2 + 24 - (17 - 8)

BLOCK_SIZE = 2

NUM_WEEKENDS = BLOCK_SIZE * NUM_BLOCKS
