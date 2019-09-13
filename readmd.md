# International Maritime Piracy


## Background & Motivation
Around 2012, the US population became aware that pirates really were, shall we say, a thing. that they weren't swashbuckling anti-heros 

## Data
The data came from the National Geospatial-Intelligence Agency (NGA)



## Exploratory Data Analysis



## Issues / Lesssons Learned


### 1) Virtual Environments for Python Basically Suck:
I initially went with a conda virtual environment because without environments, python can easily become a hodge-podge of conflicting packages and multiple versions of python on the machine and read that conda environments were much better. However, I was greeted with the following:

    requests.exceptions.SSLError: HTTPSConnectionPool(host='msi.nga.mil', port=443): Max retries exceeded with url: /NGAPortal/msi/query_results.jsp?MSI_queryType=ASAM&MSI_generalFilterType\=All&MSI_generalFilterValue=-999&MSI_additionalFilterType1=None&MSI_additionalFilterType2=-999&MSI_additionalFilterValue1=-999&MSI_additionalFilterValue2=-999&MSI_outputOptionType1=SortBy&MSI_outputOptionType2=-999&MSI_outputOptionValue1=Date_DESC&MSI_outputOptionValue2=-999&MSI_MAP=-999 (Caused by SSLError(SSLError("bad handshake: Error([('SSL routines','tls_process_server_certificate', 'certificate verify failed')])")))

My first thought was this has something to with Requests and BeautifulSoup not being able to handle SSH traffic because of outdated information about them. A little more research and I found that wasn't the case. Then I thought perhaps I was being shut down for looking like a computer, so I added in a User Agent statement. 

Eventually I found out that while python 3.7 is my system python, it wasn't for the conda environment even though the conda download was for 3.7. Once that was fixed... still no love.

### 2) Long URLs need to be triple quoted
    /NGAPortal/msi/query_results.jsp?MSI_queryType%20%20%20%20=ASAM&MSI_generalFilterType=All&MSI_generalFilterValue=-999&MSI_additional%20%20%20%20FilterType1=None&MSI_additionalFilterType2=-999&MSI_additionalFilterValue1%20%20%20%20=-999&MSI_additionalFilterValue2=-999&MSI_outputOptionType1=SortBy&MSI_%20%20%20%20outputOptionType2=-999&MSI_outputOptionValue1=%20%20%20%20Date_DESC&MSI_outputOptionValue2=-999&MSI_MAP=-999 (Caused by SSLError(SSLError("bad handshake: Error([('SSL routines', 'tls_process_server_certificate', 'certificate verify failed')])"))) (scraping_the_pirates) Alexs-MacBook-Pro:Capstone Projects alex$ 


### 3) Web Scraping Means "I Hope This Isn't Just One Giant Table"
My data is like a beautiful model:





... who is insane and lives off cocaine and champagne



Beautiful Soup handles HTML that has unique identifiers well. But that's not true for tabular data which mine consisted completely from.


### 3) Web Scraping Is Messy
I ended up using a combination  OpenOffice which has good regex support.

After cleaning the data, I saved as tab-delimited as commas, semicolons, dashes were all already in use but tabs weren't.

Was a huge time suck. So I went back to using regex. The problem was that I still couldn't 
figure how to remove blank lines. so I used grep and sed

````
    sed '/^$/d' file.txt > no_empty_lines.txt
````
