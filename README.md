# <p align="center">International Maritime Piracy and Robbery at Sea </p>

<center>Below are all of the reported international piracy and robbery at sea incidents since 1979.</center>
<br>

![reported piracy and robbery at sea incidents](images/updated_events.png "All international piracy and robbery at sea events since 1979")

## Table of Contents

- [Top Image](# )
- [Description](#description)
- [Status](#status)
- [Background & Discussion](#background)
- [NGA ASAM is good but ...](#nga-asam-is-good-but)
  1. [The reference numbers (year-event number) are substantially inaccurate](#nga-asam-is-good-but)
  2. [A whopping 1224 different ***types of victims***](#nga-asam-is-good-but)
  3. [There were 327 different types of hostilities](#nga-asam-is-good-but)
  4. [Other issues](#nga-asam-is-good-but)

- [Roadmap](#roadmap)
- [Updates](#updates)

<br><br>
[Top](#table-of-contents)

## Description

International Maritime Piracy (IMP) gets National Geospatial Intelligence Anti-Shipping Message ([NGA ASAM](https://msi.nga.mil/Piracy)) database and cleans the data.

<br><br>
[Top](#table-of-contents)

## Status: Fix needed due to NGA's move to geodatabase

The dataset was formerly available for download as csv or json but is now available as either an ArcGIS Shapefile or a file geodatabase which requires a refactoring of the code.

<br><br>
[Top](#table-of-contents)

## Background & Discussion

As noted before, the data comes from the National Geospatial Intelligence Anti-Shipping Message ([NGA ASAM](https://msi.nga.mil/Piracy)) database. The reports are aggregated from several sources (news sources, police reports, insurance companies, etc) And include the following:

- Robbery at sea (activities within a country's territorial waters) e.g., Lake Chad
- Maritime Piracy (Activities in international waters)
- Actions that hinder shipping in general. e.g., protestors, military actions, etc

That last point is important and what makes this database different from the [International Maritime Organization](https://gisis.imo.org/Public/) which also has a database but no API at this point. However, there is a unique challenge that has come about. in that everyone uses the definitions of [piracy as defined by the United Nations Convention on the Law of the Sea (UNCLOS)](https://www.un.org/Depts/los/piracy/piracy.htm) including NGA and the Office of Naval Intelligence (ONI). These definitions are in the annex of every [Worldwide Threat to Shipping](https://www.oni.navy.mil/ONI-Reports/Shipping-Threat-Reports/Worldwide-Threat-to-Shipping/) report published by ONI.
<blockquote>

- Attempted Boarding – Close approach or hull-to-hull contact with report that boarding paraphernalia were employed or visible in the approaching boat.
- Blocking – Hampering safe navigation, docking, or undocking of a vessel as a means of protest.
- Boarding – Unauthorized embarkation of a vessel by persons not part of its complement without successfully taking control of the vessel.
- Fired Upon – Weapons discharged at or toward a vessel.
- Hijacking – Unauthorized seizure and retention of a vessel by persons not part of its complement.
- Kidnapping – Unauthorized forcible removal of persons belonging to the vessel from it.
- Hijacking/Kidnapping Combination – Unauthorized seizure and retention of a vessel by persons not part of its complement who forcefully remove crew members from vessel when disembarking.
- Robbery – Theft from a vessel or from persons aboard the vessel.
- Suspicious Approach – All other unexplained activity in close proximity of an unknown vessel.

</blockquote>

Overall the NGA ASAM database looks like this.
![raw data](images/imported_raw_data.png "pandas dataframe of NGA ASAM database")

<br><br>
[Top](#table-of-contents)

## NGA ASAM is good but

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

    Much of this isn't reflected in the categories of the database. Additionally, it's reasonable to wonder what the database now represents. It was originally meant to be piracy and robbery at sea. But it is now more generalized and includes a broader range of threats to shipping and travel by sea in general. But, even if we did stick with the original categories, it still wouldn't be sufficient for several reasons:<br>

4. Other issues

    - It doesn't allow for multiple entries
    - It doesn't include for range of crimes, including murder
    - It doesn't account for governmental actions (eg. Russian shelling of a port)
    - It doesn't cover things like stowaways which meet the definition of a boarding but lacks intent of piracy.

<br> <br>
[Top](#table-of-contents)

## So, let's make it better

For now, here's the roadmap:

- [x] First, clean up the dataset. This consists of:
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
- [ ] Datsette of finished database shared back to NGA in the event they might find it useful.

<br> <br>
[Top](#table-of-contents)

## Updates

15 Jun 2022 --
<blockquote>
Sorry for the delay in responding.  I’ll try my best to explain these, but this system has been around a lot longer than I have been working in it.

1) The reference numbers are not linked with the date of the event.  They are based on when it was entered into the database.  When I started working on this I inherited a little over a year of backlog.  So, when I started entering incidents into the database in mid-2020, most of them entered in during 2020 were events that happened in 2019.  Prior to that, I don’t know what the gaps are with having someone dedicated to entering in events.

2) As for positions – we enter in the positions as provided in the source message.  The bulk of our source messages are in degrees and minutes.

3) Again, I only know the process for selecting Hostility Type since I took over.  The current process is to use a dropdown list, which I have attached.

4) Like the Hostility Type, the Victim Type is currently a dropdown list, also attached.  Those who had worked on this in the past are long gone.

</blockquote>

1 Jan 2024 --
<blockquote>
  GMTDS currently does not include NAVAREAS, though we have started to make progress in this regard, in coordination with IHO partners. For the time being, I'd recommend reviewing IHO's Navigation Warnings. That should help you to identify what you need from the IHO Web Catalogue.

If you have any follow-up questions, please don't hesitate

</blockquote>

<br> <br>
[Top](#table-of-contents)
