<br>

#  <p align="center">International Maritime Piracy and Robbery at Sea </p>

Below is a map plotting all of the reported international piracy and robbery at sea incidents since 1979.

![reported piracy and robbery at sea incidents](images/updated_events.png "All international piracy and robbery at sea events since 1979")

The data comes from the National Geospatial Intelligence Anti-Shipping Message ([NGA ASAM](https://msi.nga.mil/Piracy)) database. The reports are aggregated from several sources (news sources, police reports, insurance companies, etc). The database includes:
- Robbery at sea (activities within a country's territorial waters) e.g., Lake Chad
- Maritime Piracy (Activities in international waters)
- Actions that hinder shipping in general. e.g., protestors, military actions, etc

That last point is important and what makes this database different from the [International Maritime Organization](https://gisis.imo.org/Public/) which also has a database but no API at this point. Overall the NGA ASAM database looks like this.

![raw data](images/imported_raw_data.png "pandas dataframe of NGA ASAM database")
<br>
<br>
# NGA ASAM is good but ...
After spending some time with the data I noticed a few things I thought hindered analysis. For example:


1. The reference numbers (year-event number) are substantially inaccurate. For example, you can see reference numbers don't match years. They also don't the USG fiscal year -- or any coherent method. This was true for both when the database was started but was true a couple of years ago too.

![Reference-Date Discrepancies](images/reference-date_discrepencies.png "Reference-Date Discrepancies")


2. At the time of writing there are a whopping 1224 different ***types of victims***; broadly categorized as:
    - Definite misentries (Speedboat, SUPICIOUS APPROACH)
    - Vague entries (VESSEL, ALL SHIPPING, Anchored, At anchor,  KIDNAPPED, MEN)
    - Improbable entries (warship, PHILIPPINE NAVY, SOUTH KOREAN COAST GUARD -- but, then again, the USS COLE *actually was* attacked)
    - What appears to be an attempt at standardization (e.g. bulk carrier, fishing vessel).
    - Specific vessel names
<br>

3. There were 327 different types of hostilities, much of which was due to misspellings or inconsistent capitalization entries but there were a few gems such as:
    - Ethiopia, Tunisia, Iran, IRANIAN NAVAL FORCES, VIETNAMESE PATROL BOATS, HAITIAN AUTHORITIES, CUBAN GUNBOAT and CHINA. I think it's safe to say when a boat is in the controlled waters of a particular country and a naval vessel of that country has boarded the vessel, it's an official action.
    - STOWAWAYS, Tuna boat, Attackers
    - HAPPY LADY (which was the name of the victim vessel)
    - Poachers?!?!

This is odd because everyone uses the definitions of [piracy as defined by the United Nations Convention on the Law of the Sea (UNCLOS)](https://www.un.org/Depts/los/piracy/piracy.htm) including NGA and the Office of Naval Intelligence (ONI). These definitions are in the annex of every [Worldwide Threat to Shipping](https://www.oni.navy.mil/ONI-Reports/Shipping-Threat-Reports/Worldwide-Threat-to-Shipping/) report published by ONI.
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

Much of this isn't reflected in the categories of the database. Additionally, it's reasonable to wonder what the database now represents. It was originally meant to be piracy and robbery at sea. But it is now more generalized and includes a broader range of threats to shipping and travel by sea in general. But, even if we did stick with the original categories, it still wouldn't be sufficient for several reasons:<br>
* It doesn't allow for multiple entries
* It doesn't include for range of crimes, including murder
* It doesn't account for governmental actions (eg. Russian shelling of a port)
* It doesn't cover things like stowaways which meet the definition of a boarding but lacks intent of piracy.

My sense is this is a low-priority issue for NGA.
<br>
<br>


# So, let's make it better

For now, here's the roadmap:
-  [x] First, clean up the dataset. This consists of:
    - [x] Remove the excess spaces in the description column.
    - [x] Fix the 'reference' column values as they are all sorts of messed up.
    - [x] Convert the single lat/long position to decimal degrees columns for ease of plotting
    - [ ] Important: Fix the mapping of subregions to navAreas. Subreg 22 is listed as part of navArea XII, XV, and XVI. Subreg 24 is listed as part of navArea II, VI, V, and VI. 37, 57, 61, 62, 63, 71, 73, 74, and 83 all have problems. To do that I need shape or GeoJSON files of navAreas at a minimum but preferably navAreas and the subregions.


- [x] Contact NGA and see if this would be of benefit or interest to them (***in progress***) (see below)
    - [ ] Fix the 'victim' columns values  - ~~easy first pass would be to trust the data ruthlessly pare down the columns~~
    - [ ] Fix the 'hostility' columns values - ~~easy first pass would be to trust the data ruthlessly pare down the columns but also add ones for military action and protestors~~

While it's a quick start, I don't think regex is going to cut it for categories. I think a good NLP model *should* and one-shot models have shown good results. The collection has evolved from piracy to now including a broader set of threats to shipping. For example, few reports in the Black Sea/Sea of Azov are solely due to the Russia-Ukraine war.

There is no category for "attacked by military forces", nor is there one for killings or stowaways -- all of which have happened. This is where planning for the future is needed and why I've reached out to NGA for clarity.

- [ ] NLP model to set the hostility column. (***in progress***)
- [ ] NLP model to set the victim column.
- [ ] Check against the [International Chamber of Commerce's Criminal Crime Services dataset](www.icc-ccs.org)

- [ ] Post the dataset to Kaggle so others can get some benefit.
- [ ] Do a bit of analysis to see what trends can be seen. This will also be useful for a Kaggle dataset.
- [ ] Dash site (**in progress**)
- [ ] Datsette of finished database shared back to NGA in the event they might find it useful.

Update 15 Jun. Received email from NGA. It seemed a mix of low priority, noncommittal, and "this is the way it's always been done". Asked for clarification. If this goes nowhere, I'll make changes and provide it to them for their review and possible use but I'll focus on getting it on Kaggle first. An option I'm seriously considering is a two-part solution. The first would be to keep the dataset as it is. The second (and I think more useful) is to one-shot the hostilities but leave the victims as the vessel type can be tricky.
