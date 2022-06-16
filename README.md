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


* The reference numbers (year-event number) are substantially inaccurate. For example, you can see reference numbers don't match years.

![Reference-Date Discrepancies](images/reference-date_discrepencies.png "Reference-Date Discrepancies")


* At last count there are a whopping 1224 different ***types of victims***; broadly categorized as:
    - Definite misentries (Speedboat, SUPICIOUS APPROACH) 
    - Vague entries (VESSEL, ALL SHIPPING, Anchored, At anchor,  KIDNAPPED, MEN)
    - Improbable entries (warship, PHILIPPINE NAVY, SOUTH KOREAN COAST GUARD -- but there was the USS COLE, which actually *was* attacked)
    - What appears to be an attempt at standardization (e.g. bulk carrier, fishing vessel)
    - Specific vessel names

<br>

* There were 327 different types of hostilities, mostly misspellings or inconsistent capitalization entries but a few gems such as:
    - Ethiopia, Tunisia, Iran, IRANIAN NAVAL FORCES, VIETNAMESE PATROL BOATS, HAITIAN AUTHORITIES, CUBAN GUNBOAT and CHINA. I think it's safe to say when a boat is the controlled waters of a particular country and naval vessel of that country has members board a vessel, it's an official action. They might be corrupt but they are authorized by the government to be there.
    - STOWAWAYS, Tuna boat, Attackers, HAPPY LADY
    - Poachers?!?!

This is odd because everyone uses the definitions of [piracy as defined by the United Nations Convention on the Law of the Sea (UNCLOS)](https://www.un.org/Depts/los/piracy/piracy.htm) including NGA and the Office of Naval Intelligence (ONI) but it isn't reflected in the categories of the database. My sense is this is a low priority issue and that the database was established before UNCLOS.

<br>
<br>


# So, let's make it better

For now, here's the roadmap:
-  [ ] First, clean up the dataset. This consists of:
    - [x] Remove the excess spaces in the description column.
    - [x] Fix the 'reference' column values as they are all sorts of messed up.
    - [x] Add lat/long columns in decimal degrees for ease of poltting
- [x] Contact NGA and see if this would be of benefit or interest to them (***in progress***) (see below)
    - [ ] Regularize the 'victim' columns values  - ~~easy first pass would be to trust the data ruthlessly pare down the columns~~
    - [ ] Regularize the 'hostility' columns values - ~~easy first pass would be to trust the data ruthlessly pare down the columns but also add ones for military action and protestors~~
  
While it's a quick start, I really don't think regex is really going to cut it for categories. I think a good NLP model *should* and one-shot models have shown good results. The collection has evolved over time from priracy to now including more threats to shipping. For example one the picture there are few in the Black Sea that are solely due to the Russia-Ukraine war. 
    
 * Attempted Boarding – Close approach or hull-to-hull contact with report that boarding
paraphernalia were employed or visible in the approaching boat.
 * Blocking – Hampering safe navigation, docking, or undocking of a vessel as a means of protest.
 * Boarding – Unauthorized embarkation of a vessel by persons not part of its complement without
successfully taking control of the vessel.
 * Fired Upon – Weapons discharged at or toward a vessel.
 * Hijacking – Unauthorized seizure and retention of a vessel by persons not part of its complement.
 * Kidnapping – Unauthorized forcible removal of persons belonging to the vessel from it.
 * Hijacking/Kidnapping Combination – Unauthorized seizure and retention of a vessel by persons not
part of its complement who forcefully remove crew members from vessel when disembarking.
 * Robbery – Theft from a vessel or from persons aboard the vessel.
 * Suspicious Approach

There is no cateory for "attacked by military forces", nor is there one for killings or stoaways -- all of which have happened. This is where planing for the future is needed and why I've reached out to NGA for clarity.
 
- [ ] NLP model to set the hostility column. (***in progress***)
- [ ] NLP model to set the victim column. 
- [ ] Check against the [International Chamber of Commerce's Criminal Crime Services dataset](www.icc-ccs.org)

- [ ] Post dataset to Kaggle so others can get some benefit.
- [ ] Do a bit of analysis to see what trends can be seen. This will also be useful for a Kaggle dataset.
- [ ] Dash site 


Update 15 Jun. Recieved email from NGA. It seemed a mix of low priority, non-comittal, and "this is the way it's always been done". Asked for clarification. If this goes nowhere, I'll make changes and provide them but focus on getting it on Kaggle first.
