<p align="center">
    <img src="https://cdn.albumoftheyear.org/images/title-2015.png?raw=true" alt="AOTY Logo" width="190" height="68"/>
</p>

# Album of the Year Top 100 Albums by Year Analysis

This is a side project I'm doing to explore trends in music of the top 100 albums from each year as rated by the users of [`albumoftheyear.org (AOTY)`](https://www.albumoftheyear.org/).

### Task 1: Data Collection

Since AOTY doesn't supply their data in an API I'm scraping it. Since AOTY has some Cloudflare protection against bots, I couldn't scrape the data from their website, so I used the cached versions from Google's web cache. I have since figured out a way around the Cloudflare protection but since it could be harmful in the wrong hands and possibly unethical I'm not uploading that part of the code.

A lot of the scraping should be similar as the cached version of the site since the page structure is still the same.

## Table of Contents

- [Data Description](#data-description)
- [Tools](#tools)
- [Deliverables](#deliverables)
  - [Task 1: Data Collection](#task-1-data-collection)
  - [Task 2: Data Wrangling](#task-2-data-wrangling)
  - [Task 3: Exploratory Data Analysis](#task-3-exploratory-data-analysis)
  - [Task 4: Data Visualization](#task-4-data-visualization)
  - [Task 5: Dashboard Creation](#task-5-dashboard-creation)
  - [Task 6: Presentation of Findings](#task-6-presentation-of-findings)
- [Stretch Goals](#stretch-goals)

## Data Description

Albumoftheyear.org (AOTY), a popular website for album ratings and reviews, contains lists of the best albums for each year from 1950 to now. I've compilied a dataset of the top 100 albums from each year based on users scores.

The dataset will be available as a .xlsx file here soon.

The below table lists the columns in the data.

<details>
 <summary><strong>View Table</strong></summary>
<table>
  <thead>
    <tr>
      <th>Column Name</th>
      <th>Column Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>rank</td>
      <td>
        Rank of the album in the list it appears in.
      </td>
    </tr>
    <tr>
      <td>artist_name</td>
      <td>
        Name of the artist or band that made the album.
      </td>
    </tr>
    <tr>
      <td>album_name</td>
      <td>Name of the album</td>
    </tr>
    <tr>
      <td>release_date</td>
      <td>The date the album was released.</td>
    </tr>
    <tr>
      <td>genres</td>
      <td>A list of the genres of the album.</td>
    </tr>
    <tr>
      <td>user_score</td>
      <td>
        The score the users gave the album.
      </td>
    </tr>
    <tr>
      <td>user_score_float</td>
      <td>The float version of the score according to AOTY.</td>
    </tr>
    <tr>
      <td>number_of_ratings</td>
      <td>
        Number of ratings the album has recieved from users.
      </td>
    </tr>
    <tr>
      <td>link_to_album</td>
      <td>
       A link to the album's page on AOTY.
      </td>
    </tr>
    <tr>
      <td>must_hear</td>
      <td>If the album is a "must hear" according to AOTY. Possible values: no, user, critic, or both. Meaning not a must hear, users think it's a must hear, critics think it's a must hear, or critics and users think it's a must hear.</td>
    </tr>
    <tr>
      <td>album_artwork_link</td>
      <td>
        A link to the album's artwork, hosted on AOTY.
      </td>
    </tr>
    <tr>
      <td>list_year</td>
      <td>
        What year is the album from (what list the album's part of).
      </td>
    </tr>
  </tbody>
</table>

</details>

## Tools

- [`python`](https://www.python.org/downloads/) v3.12.2
- [`pandas`](https://pandas.pydata.org/?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMML0187ENSkillsNetwork31430127-2021-01-01) for managing the data.
- [`numpy`](https://numpy.org/?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMML0187ENSkillsNetwork31430127-2021-01-01) for mathematical operations.
- [`beautiful soup`](https://beautiful-soup-4.readthedocs.io/en/latest/) for scraping data.

## Deliverables

### Task 1: Data Collection

- [ ] Scrape AOTY data

### Task 2: Data Wrangling

- [ ] Finding Missing Values
- [ ] Determine Missing Values
- [ ] Finding Duplicates
- [ ] Removing Duplicates
- [ ] Normalizing Data

### Task 3: Exploratory Data Analysis

- [ ] Distribution
- [ ] Outliers
- [ ] Correlation

### Task 4: Data Visualization

- [ ] Visualizing Distribution of Data
- [ ] Relationship
- [ ] Composition
- [ ] Comparison

### Task 5: Dashboard Creation

- [ ] Dashboards

### Task 6: Presentation of Findings

- [ ] Final Presentation

## Stretch Goals

- [x] None so far
