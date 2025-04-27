import seaborn as sns
import pandas as pd
import fastf1
import fastf1.plotting
from matplotlib import pyplot as plt

race = fastf1.get_session(2025, 2, 'R')
race.load()
import mplcursors
from matplotlib.ticker import MultipleLocator

# Dynamically determine the winner of the race
winner_driver = race.results.loc[race.results['Position'] == 1, 'DriverNumber'].iloc[0]
winner_driver_name = race.results.loc[race.results['Position'] == 1, 'Abbreviation'].iloc[0]  # Get the winner's abbreviation

# Use all drivers' laps
combined_laps = race.laps.copy()
combined_laps['Driver'] = combined_laps['Driver'].astype(str)  # Ensure Driver column is string type

# Convert lap times to seconds
combined_laps['LapTimeSeconds'] = combined_laps['LapTime'].dt.total_seconds()

# Calculate the mean lap time of the winner
winner_laps = race.laps.pick_drivers(winner_driver)
winner_mean_lap_time_seconds = winner_laps['LapTime'].dt.total_seconds().mean()

# Calculate the difference between the mean lap time of the winner and the current lap time
combined_laps['DifferenceFromWinnerMean'] = combined_laps['LapTimeSeconds'] - winner_mean_lap_time_seconds

# Calculate the cumulative sum of the differences for each driver
combined_laps['CumulativeDifference'] = combined_laps.groupby('Driver')['DifferenceFromWinnerMean'].cumsum()

# Define a custom style for drivers using get_driver_style
unique_drivers = combined_laps['Driver'].unique()
driver_styles = {
    driver: fastf1.plotting.get_driver_style(driver, style=['color', 'linestyle'], session=race)
    for driver in unique_drivers
}

# Increase the width of the plot
fig, ax = plt.subplots(figsize=(12, 8), facecolor="black")  # Set width to 12 inches and height to 8 inches

# Plot the cumulative difference for all drivers
lines = []  # Store line objects for mplcursors
for driver in unique_drivers:
    driver_data = combined_laps[combined_laps['Driver'] == driver]
    style = driver_styles[driver]
    line, = ax.plot(driver_data['LapNumber'], driver_data['CumulativeDifference'],
                    label=driver, color=style['color'], linestyle=style['linestyle'], linewidth=2)
    lines.append(line)

# Add hover functionality with mplcursors
cursor = mplcursors.cursor(lines, hover=True)
@cursor.connect("add")
def on_add(sel):
    driver_data = combined_laps[combined_laps['Driver'] == sel.artist.get_label()]
    lap_number = int(sel.index)
    lap_info = driver_data.iloc[lap_number]
    sel.annotation.set_text(
        f"Driver: {lap_info['Driver']}\n"
        f"Lap: {lap_info['LapNumber']}\n"
        f"Compound: {lap_info['Compound']}\n"
        f"Cumulative Gap: {lap_info['CumulativeDifference']:.2f}s"
    )
    sel.annotation.get_bbox_patch().set(fc="black", alpha=0.8)

ax.set_xlabel("Lap Number", color="white")
ax.set_ylabel(f"SUM - Gap to {winner_driver_name} Mean Lap Time (s)", color="white")  # Add the winner's name to the y-axis label

# Add a horizontal line at 0 for reference
ax.axhline(0, color="gray", linestyle="--", linewidth=1)

# Set y-axis limits and tick marks
ax.set_ylim(0, None)  # Start y-axis at 0
ax.yaxis.set_major_locator(MultipleLocator(5))  # Show tick marks every 5 seconds

# Customize the plot appearance for better visibility
ax.tick_params(colors="white")  # Set tick colors to white
ax.spines["top"].set_color("white")
ax.spines["right"].set_color("white")
ax.spines["left"].set_color("white")
ax.spines["bottom"].set_color("white")

# Turn on major grid lines
plt.grid(color="gray", which="major", axis="both")
sns.despine(left=True, bottom=True)

# Add the legend
ax.legend(bbox_to_anchor=(1.0, 1.02))

plt.tight_layout()
plt.show()