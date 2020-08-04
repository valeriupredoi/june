#!/usr/bin/env python
# coding: utf-8

import numpy as np
import time
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_context('notebook')
from june import World 
from june.demography.geography import Geography
from june.demography import Demography
#from june.interaction import ContactAveraging
from june.interaction import Interaction
from june.infection import Infection
#from june.interaction.contact_averaging import ContactAveraging
from june.infection.transmission import TransmissionConstant
from june.groups import Hospitals, Schools, Companies, Households, CareHomes, Cemeteries, Universities
from june.groups.leisure import generate_leisure_for_config, Cinemas, Pubs, Groceries
from june.simulator import Simulator
from june.infection_seed import InfectionSeed
from june.policy import Policy, Policies
from june import paths
from june.hdf5_savers import load_geography_from_hdf5
from june.logger.read_logger import ReadLogger
from june.infection.infection import InfectionSelector
from june.world import generate_world_from_hdf5, generate_world_from_geography

geography = Geography.from_file({"super_area": ["E02003282", "E02001720", "E00088544", "E02002560", "E02002559", "E02004314",]})
geography.hospitals = Hospitals.for_geography(geography)
geography.schools = Schools.for_geography(geography)
geography.companies = Companies.for_geography(geography)
geography.care_homes = CareHomes.for_geography(geography)
geography.universities = Universities.for_super_areas(geography.super_areas)
world = generate_world_from_geography(geography, include_households=True, include_commute=True)

print("World length", len(world.people))
world.to_hdf5("world.hdf5")

world = generate_world_from_hdf5("world.hdf5")

# leisure
geography = load_geography_from_hdf5("world.hdf5")
world.cinemas = Cinemas.for_geography(geography)
world.pubs = Pubs.for_geography(geography)
world.groceries = Groceries.for_super_areas(world.super_areas,
                                            venues_per_capita=1/500)
world.cemeteries = Cemeteries()
selector = InfectionSelector.from_file()
interaction = Interaction.from_file()

print(interaction.beta)
# modify interactions (example x 2)
interaction.beta['household'] *= 2
print(interaction.beta)
interaction.alpha_physical
interaction.alpha_physical /= 2
interaction.alpha_physical

# # Seed the disease
# There are two options implemented in the seed at the moment, either you specify the number of cases and these are then homogeneously distributed by population to the different areas, or you use UK data on cases per region. For now use the first case.
seed = InfectionSeed(world.super_areas, selector,)

n_cases = 50
seed.unleash_virus(n_cases) # play around with the initial number of cases

# # Set policies
policies = Policies.from_file()

# # Run the simulation
# Since the timer configuration is a bit cumbersome, it is read from the config file at ``configs/config_example.yml
CONFIG_PATH = "configs/config_example.yaml"
leisure = generate_leisure_for_config(world=world,
                                      config_filename=CONFIG_PATH)
simulator = Simulator.from_file(
     world, interaction, selector, 
    config_filename = CONFIG_PATH,
    leisure = leisure,
    policies = policies
)


# Run the simulator
simulator.run()


# While the simulation runs (and afterwards) we can launch the visualization webpage by running
# ```python june/visualizer.py path/to/results``` 

# # Getting the results

# All results are stored in a json file specified in the ``save_path`` variable in the config file. We can also access it from ``world.logger`` directly.
import pandas as pd
read = ReadLogger()


# ## Hospital data and how it changed over time
hospitals_df = read.load_hospital_capacity()
hospitals_df.head(3)
hospitals_characteristics_df = read.load_hospital_characteristics()

hospitals_characteristics_df


# ## where did infections happen?
loc_df = read.get_locations_infections()

locations_per_day = read.locations_df.groupby(pd.Grouper(freq='D')).sum()

all_infection_places = set(locations_per_day.location.sum())

def n_infections(row, infection_place):
    return sum([row.counts[i] for i, x in enumerate(row.location) if x == infection_place])

for infection_place in all_infection_places:
    locations_per_day[str(infection_place)] = locations_per_day.apply(
        lambda x: n_infections(x, infection_place),
        axis=1
    )

locations_per_day = locations_per_day.drop(columns=['location',
                                                    'counts'])

locations_per_day = locations_per_day.div(
    locations_per_day.sum(axis=1), axis=0
)

locations_per_day.plot.area( alpha=0.5)
plt.legend(bbox_to_anchor=(1,1))
plt.ylabel('Percent of infections')

from matplotlib import cm
cmap = cm.get_cmap('Spectral') # Colour map (there are many others)

locations_per_day.plot(figsize=(30,8), logy=True, ylim=(1e-3, 1), cmap=cmap)

import matplotlib.ticker as mtick

ax = loc_df['percentage_infections'].sort_values().plot.bar()
ax.yaxis.set_major_formatter(mtick.PercentFormatter())
plt.ylabel('Percentage of infections at location')
plt.xlabel('location')
plt.yscale('log')


# ## rate of infection
r_df = read.get_r()
r_df.plot()
plt.axvspan(policies.social_distancing_start, 
            policies.social_distancing_end,
            facecolor='y', alpha=0.2)
plt.axhline(y=1, linestyle='dashed', color='gray')
plt.xlabel('Date')
plt.yscale('log')
plt.ylabel('R')


# ## World infection curves, and by super area
world_df = read.world_summary()
fig, ax = plt.subplots()
world_df['infected'].plot(ax=ax)
ax.axvspan(policies.social_distancing_start, 
            policies.social_distancing_end,
            facecolor='y', alpha=0.2)
ax.set_ylabel('# Infected')

world_df.plot()
plt.axvspan(policies.social_distancing_start, 
            policies.social_distancing_end,
            facecolor='y', alpha=0.2)
plt.legend(bbox_to_anchor=(1,1))

area_df = read.super_area_summary()

area_df[area_df.super_area == "E02003282"].plot()
plt.legend(bbox_to_anchor=(1,1))


# ## World infection curves
ages_df = read.age_summary([0,10,20,30,40,
                  50,60,70,80,90,100])
for name, group in ages_df.groupby('age_range'):
    group['infected'].plot(label=name)
plt.axvspan(policies.social_distancing_start, 
            policies.social_distancing_end,
            facecolor='y', alpha=0.2)
plt.legend(bbox_to_anchor=(1,1))

for name, group in ages_df.groupby('age_range'):
    group['dead_icu'].cumsum().plot(label=name)
plt.legend()

for name, group in ages_df.groupby('age_range'):
    group['susceptible'].plot(label=name)
plt.legend()

for name, group in ages_df.groupby('age_range'):
    group['hospital_admissions'].cumsum().plot(label=name)
plt.legend()

for name, group in ages_df.groupby('age_range'):
    group['intensive_care_admissions'].cumsum().plot(label=name)
plt.legend()

# ## Draw some of the symptoms trajectories
random_trajectories = read.draw_symptom_trajectories(window_length=600,
                                        n_people=10)

from june.infection import SymptomTag

symptoms_values = [tag.value for tag in SymptomTag]
symptoms_names = [tag.name for tag in SymptomTag]

for df_person in random_trajectories:
    df_person['symptoms'].plot()
plt.ylabel('Symptoms Trajectory')
_ = plt.yticks(symptoms_values, symptoms_names)
plt.xlabel('Date')

for df_person in random_trajectories:
    df_person['n_secondary_infections'].plot()
plt.ylabel('Number of secondary infections')
plt.xlabel('Date')
plt.show()
