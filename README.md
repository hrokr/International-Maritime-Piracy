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
    - Definite misentries (Thieves, pirates, SUPICIOUS [sic] APPROACH) 
    - Vague entries (KIDNAPPED, MEN)
    - Improbable entries (warship, PHILIPPINE NAVY, SOUTH KOREAN COAST GUARD -- but there was the USS COLE, which actually *was* attacked)
    - What appears to be an attempt at standardization (e.g. bulk carrier, fishing vessel)
    - Specific vessel names

<br>

* There were 327 different types of hostilities, mostly misspellings or inconsistent capitalization entries but a few gems such as:
    - Ethiopia, Tunisia, Iran, IRANIAN NAVAL FORCES, VIETNAMESE PATROL BOATS, HAITIAN AUTHORITIES, CUBAN GUNBOAT and CHINA. I think it's safe to say when a boat is the controlled waters of a particular country and naval vessel of that country has members board a vessel, it's an official action. They might be corrupt but they are authorized by the government to be there.
    - STOWAWAYS, Tuna boat, Attackers, HAPPY LADY 

This is odd because everyone uses the definitions of [piracy as defined by the United Nations Convention on the Law of the Sea (UNCLOS)](https://www.un.org/Depts/los/piracy/piracy.htm) including NGA and the Office of Naval Intelligence (ONI) but it isn't reflected in the categories of the database. My sense is this is a low priority issue and that the database was established before UNCLOS.

<br>
<br>


# So, let's make it better

For now, here's the roadmap:
-  [ ] First, clean up the dataset. This consists of:
    - [x] Remove the excess spaces in the description column.
    - [x] Fix the 'reference' column values as they are all sorts of messed up.
    - [ ] ~~Regularize the 'victim' columns values  - easy first pass would be to trust the data ruthlessly pare down the columns~~

    - [ ] ~~Regularize the 'hostility' columns values - easy first pass would be to trust the data ruthlessly pare down the columns but also add ones for military action and protestors~~
      - Attempted Boarding – Close approach or hull-to-hull contact with report that boarding
paraphernalia were employed or visible in the approaching boat.
      - Blocking – Hampering safe navigation, docking, or undocking of a vessel as a means of protest.
      - Boarding – Unauthorized embarkation of a vessel by persons not part of its complement without
successfully taking control of the vessel.
      - Fired Upon – Weapons discharged at or toward a vessel.
      - Hijacking – Unauthorized seizure and retention of a vessel by persons not part of its complement.
      - Kidnapping – Unauthorized forcible removal of persons belonging to the vessel from it.

While it's a quick start, I really don't think regex is really going to cut it for categories. I think a good NLP model *might* though. 
This can be done by hand or by using a ...
 
- [ ] NLP model to set the hostility and possibly victim columns. (***in progress***)
- [x] Contact NGA and see if this would be of benefit or interest to them (***in progress***)
- [ ] Check against the [International Chamber of Commerce's Criminal Crime Services dataset](www.icc-ccs.org)

- [ ] Post dataset to Kaggle so others can get some benefit.
- [ ] Do a bit of analysis to see what trends can be seen. This will also be useful for a Kaggle dataset.
- [ ] Dash site 

