import time
import pandas as pd
import matplotlib.pyplot as plt
from NWMRetro.NWMRetro import get_streamflow_by_reach

# Set up query for Otter Creek
reach = 22221703
start_time = '2011-08-28'
end_time = '2011-09-10'

# Make query
print('Initiating Query...')
t1 = time.perf_counter()
get_streamflow_by_reach(reach, start_time, end_time, make_csv=True)
print(f'Query Completed in {round(time.perf_counter() - t1, 2)} seconds!')

# Plot results
data = pd.read_csv(f'NWM{reach}.csv', index_col=0, parse_dates=True)
fig, ax = plt.subplots()
ax.plot(data, c='darkorange')
dates = pd.date_range(start_time, end_time, freq='3D')
ax.set_xticks(dates)
ax.set_title(f'Discharge for Reach {reach}')
ax.set_ylabel('Discharge (cms)')
cms2cfs = lambda x: x * 35.3147
cfs2cms = lambda x: x / 35.3147
secax = ax.secondary_yaxis('right', functions=(cms2cfs, cfs2cms))
secax.set_ylabel('Discharge (cfs)')
fig.tight_layout()
fig.savefig(f'NWM{reach}.png', dpi=300)