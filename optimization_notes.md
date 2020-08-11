Notes
=====

A collection of first-pass possible optimization notes:
- don't use lists of numpy arrays - use multi-dim arrays
- `Simulator.do_timestep()`: for loop on `group_instances` / for loop on `group_type`:
  each `group_type` (company, pub, hosehold etc) on a separate thread: currently use `Pool()`
  will return  a `Maximum recursion depth reached` which means very high complexity in the
  routines -> use more iteration!
- a lot of `if` statements with no `else/elif/else` -> these take time, if there is no
  conditional just run them and account for cases in the function that runs under `if`
- `getattr()` is called 3000 times, `len()` 222 times -> think of `__slots__` and have a look
   at all those lists
- ran with no interactions in `do_timestep()`: usual runtime ~180s, this case ~160s, so interations
  are really cheap (`self.interaction.time_step_for_group`)
- there are 115 calls to `List()` or conversions via `list(x)`
