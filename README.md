<br>

#  <p align="center">International Maritime Piracy and Robbery at Sea </p>

Below is map plotting all of the reported international piracy and robbery at sea incidents since 1979.

![reported piracy and robbery at sea incidents](images/updated_events.png "All international piracy and robbery at sea events since 1979")

The data comes from the National Geospatial Intelligence Anti-Shipping Message ([NGA ASAM](https://msi.nga.mil/Piracy)) database. The reports are aggregated from a number of sources (news sources, police reports, insurance companies, etc). The database includes:
- Robbery at sea (activities within a country's territorial waters) e.g., Lake Chad
- Maritime Piracy (Activities in international waters)
- Actions that hinder shipping in general. e.g., protestors, military actions, etc

That last point is important and what makes this database different from the [International Maritime Organization](https://gisis.imo.org/Public/) which also has a database but no API at the point. Overall the NGA ASAM database looks like this.

![raw data](images/imported_raw_data.png "pandas dataframe of NGA ASAM database")
<br>
<br>
# NGA ASAM is good but ...
After spending a bit of time with the data I noticed few things that I thought were interesting but were things hinder analysis. For example:


1. The reference numbers (year-event number) are substantially inaccurate. For example, you can see reference numbers don't match years. They also don't the USG fiscal year -- or any coherent method.

![Reference-Date Discrepancies](images/reference-date_discrepencies.png "Reference-Date Discrepancies")


2. At last count there are a whopping 1224 different ***types of victims***; broadly categorized as:
    - Definite misentries (Speedboat, SUPICIOUS APPROACH)
    - Vague entries (VESSEL, ALL SHIPPING, Anchored, At anchor,  KIDNAPPED, MEN)
    - Improbable entries (warship, PHILIPPINE NAVY, SOUTH KOREAN COAST GUARD -- but then again there was the USS COLE, which *actually was* attacked)
    - What appears to be an attempt at standardization (e.g. bulk carrier, fishing vessel).
    - Specific vessel names
<br>

3. There were 327 different types of hostilities, mostly misspellings or inconsistent capitalization entries but a few gems such as:
    - Ethiopia, Tunisia, Iran, IRANIAN NAVAL FORCES, VIETNAMESE PATROL BOATS, HAITIAN AUTHORITIES, CUBAN GUNBOAT and CHINA. I think it's safe to say when a boat is the controlled waters of a particular country and a naval vessel of that country has boards the vessel, it's an official action.
    - STOWAWAYS, Tuna boat, Attackers, HAPPY LADY
    - Poachers?!?!

This is odd because everyone uses the definitions of [piracy as defined by the United Nations Convention on the Law of the Sea (UNCLOS)](https://www.un.org/Depts/los/piracy/piracy.htm) including NGA and the Office of Naval Intelligence (ONI). These definitions are in the annex of every [Worldwide Threat to Shipping](https://www.oni.navy.mil/ONI-Reports/Shipping-Threat-Reports/Worldwide-Threat-to-Shipping/) report published by ONI
<blockquote>

 * Attempted Boarding – Close approach or hull-to-hull contact with report that boarding paraphernalia were employed or visible in the approaching boat.
 * Blocking – Hampering safe navigation, docking, or undocking of a vessel as a means of protest.
 * Boarding – Unauthorized embarkation of a vessel by persons not part of its complement without successfully taking control of the vessel.
 * Fired Upon – Weapons discharged at or toward a vessel.
 * Hijacking – Unauthorized seizure and retention of a vessel by persons not part of its complement.
 * Kidnapping – Unauthorized forcible removal of persons belonging to the vessel from it.
 * Hijacking/Kidnapping Combination – Unauthorized seizure and retention of a vessel by persons not part of its complement who forcefully remove crew members from vessel when disembarking.
 * Robbery – Theft from a vessel or from persons aboard the vessel.
 * Suspicious Approach – All other unexplained activity in close proximity of an unknown vessel.
</blockquote>

Much of this isn't clearly reflected in the categories of the database. Additionally, there is the question if the

  My sense is this is a low priority issue and that the database was established before UNCLOS.

Even if we did stick with the original categories, it still wouldn't be sufficient for several reasons:<br>
* It doesn't allow for multiple entries
* It doesn't include for murder
* It doesn't account for governmental actions (eg. Russian shelling of a port)
* It doesn't cover things like stowaways which meet the definition of a boarding but lacks intent of piracy.
<br>
<br>


# So, let's make it better

For now, here's the roadmap:
-  [x] First, clean up the dataset. This consists of:
    - [x] Remove the excess spaces in the description column.
    - [x] Fix the 'reference' column values as they are all sorts of messed up.
    - [x] Convert the single lat/long position to two decimal degrees columns for ease of plotting

- [x] Contact NGA and see if this would be of benefit or interest to them (***in progress***) (see below)
    - [ ] Regularize the 'victim' columns values  - ~~easy first pass would be to trust the data ruthlessly pare down the columns~~
    - [ ] Regularize the 'hostility' columns values - ~~easy first pass would be to trust the data ruthlessly pare down the columns but also add ones for military action and protestors~~

While it's a quick start, I really don't think regex is really going to cut it for categories. I think a good NLP model *should* and one-shot models have shown good results. The collection has evolved over time from piracy to now including more threats to shipping. For example one the picture there are few in the Black Sea that are solely due to the Russia-Ukraine war.



There is no category for "attacked by military forces", nor is there one for killings or stowaways -- all of which have happened. This is where planing for the future is needed and why I've reached out to NGA for clarity.

- [ ] NLP model to set the hostility column. (***in progress***)
- [ ] NLP model to set the victim column.
- [ ] Check against the [International Chamber of Commerce's Criminal Crime Services dataset](www.icc-ccs.org)

- [ ] Post dataset to Kaggle so others can get some benefit.
- [ ] Do a bit of analysis to see what trends can be seen. This will also be useful for a Kaggle dataset.
- [ ] Dash site
- [ ] Datsette of finished database shared back to NGA in the event they might find it useful.

Update 15 Jun. Received email from NGA. It seemed a mix of low priority, noncommittal, and "this is the way it's always been done". Asked for clarification. If this goes nowhere, I'll make changes and provide them but focus on getting it on Kaggle first.  An option I'm seriously considering is a two or three part solution. The first would be to keep the dataset as it is. The second (and I think more useful) is to one-shot the hostilities but leave the victims as the vessel type can be tricky. The third depends on either all or part of the dataset being corrected by hand which would all for a dataset that would be suitable for supervised learning projects.

Update 5 Sept. Returning to project after hiatus.
