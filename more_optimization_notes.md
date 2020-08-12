`activity/activity_manager.py`
```
    def move_people_to_active_subgroups(
        self,
        activities: List[str],
        date: datetime = datetime(2020, 2, 2),
        days_from_start=0,
    ):
        individual_policies = IndividualPolicies.get_active_policies(
            policies=self.policies, date=date
        )
        activities = self.apply_activity_hierarchy(activities)
        >>>>>>>
        for person in self.world.people.members:
            if person.dead or person.busy:
                continue
            allowed_activities = individual_policies.apply(
                person=person, activities=activities, days_from_start=days_from_start,
            ) >>> O(1e-6) per person
            DOMINANT:
            self.move_to_active_subgroup(allowed_activities, person) >>> O(>1e-5) per person
         <<<<<<<< this block about 30-50% of total step runtime
```
follow the money: `self.move_to_active_subgroup` O(>1e-5) -> `leisure.get_subgroup_for_person_and_housemates` O(>1e-5) ->

```
        if random() < prob_age_sex["does_activity"]:
            >>>>>>
            activity_idx = random_choice_numba(
                arr=np.arange(0, len(prob_age_sex["activities"])),
                prob=np.array(list(prob_age_sex["activities"].values())),
            )
            <<<<< ABOUT 1-3e-5

            >>>>>>
            activity = list(prob_age_sex["activities"].keys())[activity_idx]
            candidates = person.residence.group.social_venues[activity]
            candidates_length = len(candidates)
            if candidates_length == 0:
                return
            if candidates_length == 1:
                subgroup = candidates[0].get_leisure_subgroup(person)
            else:
                idx = 2000 % candidates_length
                subgroup = candidates[idx].get_leisure_subgroup(person)
            self.send_household_with_person_if_necessary(
                person, subgroup, prob_age_sex["drags_household"][activity]
            )
            person.subgroups.leisure = subgroup
            <<<<<<< ABOUT 1e-5
            return subgroup
```
That numba prob is very expensive!

Run1 (50 infect start)
======================
`Ttot_prob` = 9.35s
start: 19:02:42,425
end: 19:03:51,911
`Ttot` = 69s -> 13%

Run2 (50 infect start)
======================
`Ttot_prob` = 21s
start: 19:11:25,674
end: 19:14:44,203
`Ttot` = 200s -> 10%

Run3 (5000 infect start)
========================
`Ttot_prob` = 7.4s
start: 21:07:32,634
end: 21:10:20,432
`Ttot` = 168s -> 4%
