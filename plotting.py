import matplotlib.pyplot as plt
import numpy as np

K = 83          # binary put strike
HEDGE_SHARES = [0, 40, 83, 95.4, 150]     # shares purchased
S0 = 83        # price paid for the stock
HEDGE_PRICE = 0.02 # prediction market hsare price

for hedge_share in HEDGE_SHARES:
    premium = hedge_share * HEDGE_PRICE
    S = np.linspace(0, 200, 1000)
    stock = S
    binary_put = np.where(S < K, hedge_share, 0)
    portfolio = stock + binary_put

    plt.figure()
    plt.plot(S, stock, "--", label="Stock")
    plt.plot(S, binary_put, "--", label="Binary put")
    plt.plot(S, portfolio, label="Portfolio")
    plt.xlabel("Stock price at expiry")
    plt.ylabel("Payout")
    plt.legend()
    plt.savefig(f"plots/payout_hedge_shares{hedge_share}.png")
    plt.close()

    plt.figure()
    plt.plot(S, stock - S0, "--", label="Stock")
    plt.plot(S, binary_put - premium, "--", label="Binary put")
    plt.plot(S, portfolio - S0 - premium, label="Portfolio")
    plt.axhline(0, color="black", linewidth=0.5)
    plt.xlabel("Stock price at expiry")
    plt.ylabel("Profit")
    plt.legend()
    plt.savefig(f"plots/profit_hedge_shares{hedge_share}.png")
    plt.close()

# 3D: profit vs stock price at expiry and number of put shares (each pays $1)
n = np.linspace(0, max(HEDGE_SHARES), 100)
S_grid, n_grid = np.meshgrid(S, n)
profit = S_grid - S0 + n_grid * (np.where(S_grid < K, 1, 0) - HEDGE_PRICE)

fig = plt.figure()
ax = fig.add_subplot(projection="3d")
ax.plot_surface(S_grid, n_grid, profit, cmap="viridis")
ax.set_xlabel("Stock price at expiry")
ax.set_ylabel("Put shares")
ax.set_zlabel("Profit")
plt.savefig("plots/profit_3d.png")

# Heatmap: same data, color = profit (red = loss, blue = gain)
plt.figure()
plt.pcolormesh(S_grid, n_grid, profit, cmap="RdBu", vmin=-profit.max(), vmax=profit.max())
plt.colorbar(label="Profit")
plt.contour(S_grid, n_grid, profit, levels=[0], colors="black")  # breakeven line
plt.xlabel("Stock price at expiry")
plt.ylabel("Put shares")
plt.savefig("plots/profit_heatmap.png")

plt.show()  # opens a window - drag to rotate the 3D plot
