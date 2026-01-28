import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# ======================
# SCIENTIFIC STYLE
# ======================

sns.set_theme(context="paper", style="white")

plt.rcParams.update({
    "figure.dpi": 300,
    "savefig.dpi": 600,
    "axes.linewidth": 0.8,
    "xtick.major.width": 0.8,
    "ytick.major.width": 0.8,
    "font.family": "DejaVu Sans"
})

# ======================
# KONFIGURACJA
# ======================

FIG_WIDTH = 16
FIG_HEIGHT = 20
Y_PADDING = 2

FONT_TITLE = 14
FONT_AXIS_LABEL = 14
FONT_TICKS_Y = 12
FONT_TICKS_X = 12
FONT_MONTH_LABELS = 12
FONT_LEGEND = 14
FONT_FOOTNOTE = 12

Y_MAJOR_STEP = 2.0
Y_MINOR_STEP = 1.0
LEFT_PAD_FRACTION = 0.002

# ======================
# ŚCIEŻKI
# ======================

FILES = {
    "2024": "C:/Users/topgu/Desktop/Malina/POGODA/NAPRAWIONE_1 luty do 31 pazdziernik 2024.csv",
    "2025": "C:/Users/topgu/Desktop/Malina/POGODA/NAPRAWIONE_1 luty do 31 pazdziernik 2025.csv"
}

# ======================
# FUNKCJA WCZYTANIA
# ======================

def load_weather(path):
    df = pd.read_csv(path, sep=";")
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)

    for col in ["Av Temp", "Min Temp", "Max Temp"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df.dropna(inplace=True)
    return df

data = {y: load_weather(p) for y, p in FILES.items()}

ymin = min(df["Min Temp"].min() for df in data.values()) - Y_PADDING
ymax = max(df["Max Temp"].max() for df in data.values()) + Y_PADDING

# ======================
# WYKRES
# ======================

fig, axes = plt.subplots(
    nrows=2, ncols=1,
    figsize=(FIG_WIDTH, FIG_HEIGHT),
    sharey=True
)

for i, (year, df) in enumerate(data.items()):
    ax = axes[i]

    monthly_avg = (
        df.set_index("Date")
          .resample("MS")["Av Temp"]
          .mean()
    )

    ax.fill_between(
        df["Date"], df["Min Temp"], df["Av Temp"],
        color="#4A90E2", alpha=0.25,
        label="Lowest daily temperature" if i == 0 else None
    )

    ax.fill_between(
        df["Date"], df["Av Temp"], df["Max Temp"],
        color="#E74C3C", alpha=0.25,
        label="Highest daily temperature" if i == 0 else None
    )

    ax.plot(
        df["Date"], df["Av Temp"],
        color="#2E8B57", linewidth=2.0,
        label="Average daily temperature" if i == 0 else None
    )

    ax.axhline(0, color="#3498DB", lw=1.5, ls="--", label="0°C" if i == 0 else None)
    ax.axhline(30, color="#C0392B", lw=1.5, ls="--", label="30°C" if i == 0 else None)

    ax.set_ylim(ymin, ymax)
    ax.yaxis.set_major_locator(mticker.MultipleLocator(Y_MAJOR_STEP))
    ax.yaxis.set_minor_locator(mticker.MultipleLocator(Y_MINOR_STEP))
    ax.tick_params(axis="y", labelsize=FONT_TICKS_Y)

    ax.grid(True, which="major", axis="y", alpha=0.35)
    ax.grid(True, which="minor", axis="y", alpha=0.15)

    months = monthly_avg.index
    ax.set_xticks(months)
    ax.set_xticklabels(
        [f"{d.strftime('%B')} ({monthly_avg[d]:.1f}°C)" for d in months],
        fontsize=FONT_MONTH_LABELS
    )

    xmin, xmax = df["Date"].min(), df["Date"].max()
    ax.set_xlim(xmin - (xmax - xmin) * LEFT_PAD_FRACTION, xmax)

    for d in months:
        ax.axvline(d, color="0.6", ls="--", lw=0.9, alpha=0.5)

    ax.set_title(f"({chr(97+i)}) {year}", loc="left", fontsize=FONT_TITLE)
    ax.set_ylabel("Temperature (°C)", fontsize=FONT_AXIS_LABEL)

# ======================
# X LABEL – PRZESUNIĘTY W DÓŁ
# ======================

#axes[-1].set_xlabel("Month", fontsize=FONT_AXIS_LABEL)
#axes[-1].xaxis.set_label_coords(0.5, -0.12)

# ======================
# LEGENDA – TUŻ POD DATE
# ======================

fig.legend(
    loc="lower center",
    bbox_to_anchor=(0.5, 0.065),
    ncol=5,
    frameon=False,
    fontsize=FONT_LEGEND,
    labelspacing=0.15,
    handletextpad=0.5,
    columnspacing=1.0
)

# ======================
# FOOTNOTE – TUŻ POD LEGENDĄ
# ======================

fig.text(
    0.5, 0.045,
    "Monthly average temperature is shown in parentheses next to month labels.",
    ha="center",
    fontsize=FONT_FOOTNOTE
)

# ======================
# LAYOUT + ZAPIS
# ======================

plt.tight_layout(rect=[0, 0.11, 1, 1])

OUTPUT_DIR = "C:/Users/topgu/Desktop/Art/OSTATNIE ARTYKULY/ZAGESZCZENIE/WYNIKI OBRAZOWANIE/WYKRESY POGODA"

plt.savefig(f"{OUTPUT_DIR}/weather_temperature_2024_2025.png", dpi=600)
plt.savefig(f"{OUTPUT_DIR}/weather_temperature_2024_2025.svg")
plt.show()
