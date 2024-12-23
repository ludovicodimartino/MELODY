# Example queries
Below, we describe what we believe are the most interesting queries we performed on our graph database.  
Through these queries, we aimed to uncover some insights from the data and gather statistics that could be useful, for instance, to song producers and professionals in the music industry.

## Top 10 songs
This query extracts the most popular songs in the whole database. The popularity of a song is based on the number of times it appears in the first 10 positions of a Billboard.

    PREFIX mel: <http://www.dei.unipd.it/~gdb/ontology/melody#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    SELECT ?title ?artistName (COUNT(?position) AS ?totalAppearancesInTheFirst10Pos)WHERE {
        ?song a mel:Song ;
                mel:name ?title ;
                mel:classified ?membership ;
                mel:sungBy/mel:name ?artistName .

        ?membership a mel:Membership ;
                    mel:position ?position ;
                    mel:classifiedIn ?billboard .
                
        FILTER(?position <= "10"^^xsd:positiveInteger) . 
    }
    GROUP BY ?title ?artistName
    ORDER BY DESC (?totalAppearancesInTheFirst10Pos)
    LIMIT 10

| Song Title | Artist Name | Appearances
|------------|------------|-----------|
| Shape of You |Ed Sheeran |33|
How Do I Live |LeAnn Rimes |32|
Smooth (As Made Famous By SantanaFeaturing Rob Thomas)| The Karaoke Crew |30|
That’s What I Like| Bruno Mars |28|
Perfect|Ed Sheeran |27|
God’s Plan| Drake| 26|
Truly Madly Deeply| Savage Garden |26|
Apologize| OneRepublic| 25|
Counting Stars| OneRepublic |25|
Trap Queen| Fetty Wap |25|

## Evolution of songs duration over the years
This query examines the evolution of song duration over the years. Specifically, for each year, we calculated the
average song duration of the songs featured in the Billboard Hot 100. Since the exact release year of each song is
not in the database (see the [Ontology design diagram](../OntologyDesign/melody_ontology.png)), we used the year in which the song first appeared on the
Billboard chart as a proxy for its release year.

    PREFIX mel: <http://www.dei.unipd.it/~gdb/ontology/melody#>

    SELECT ?year ((AVG(?duration)/1000)/60 AS ?avgDurationMinutes) WHERE {
        {
            SELECT ?song (MIN(?billboardYear) AS ?year) WHERE {
                ?song a mel:Song ;
                        mel:name ?songTitle ;
                        mel:classified ?membership .

                ?membership a mel:Membership ;
                                mel:classifiedIn ?billboard .

                ?billboard a mel:BillboardHot100 ;
                            mel:date ?date .

                BIND(YEAR(?date) AS ?billboardYear) .
            }
            GROUP BY ?song
        }
        
        ?song mel:duration ?duration .
    }
    GROUP BY ?year
    ORDER BY DESC (?year)

![](./songDuration.png)

## Song by key
This query counts the number of songs in each musical key. The results are quite interesting, as we observe a significant number of songs in the key of C and very few in D# minor.

    PREFIX mel: <http://www.dei.unipd.it/~gdb/ontology/melody#>

    SELECT ?key ?count (((?count*100)/?tot_songs) AS ?percentage) WHERE {
        {
            SELECT ?key (COUNT(*) AS ?count) WHERE {
                ?song a mel:Song ;
                        mel:key ?key .
            }
            GROUP BY ?key
        }
        {
            SELECT (COUNT(*) AS ?tot_songs) WHERE {
                ?song a mel:Song .
            }
        }
    }
    ORDER BY DESC (?count)

![](./songByKey.png)

## Major vs minor scale
As you can observe from the ASK query below, the number of major key songs is more than twice the number of minor key songs. This might suggest that songs in the major scale are more likely to appear on the Billboard charts. However, this is purely speculative, since we do not have information about songs not in the Billboard Hot 100 charts.

    PREFIX mel: <http://www.dei.unipd.it/~gdb/ontology/melody#>

    ASK WHERE {
        {
            SELECT (COUNT(*) AS ?minorKeySongs) WHERE {
                ?song a mel:Song ;
                        mel:key ?key .
                
                FILTER(REGEX(?key, "m$")) .
            }
        }
        {
            SELECT (COUNT(*) AS ?majorKeySongs) WHERE {
                ?song a mel:Song ;
                        mel:key ?key .
                
                FILTER(REGEX(?key, "^(?!.*m$)")) .
            }
        }
        FILTER(?majorKeySongs > ?minorKeySongs*2) .
    }


    # ANSWER: YES

## Song titles word-cloud
To analyze the most frequently occurring words in song titles, we wrote a query that concatenates all the song titles into a single string, converting uppercase letters to lowercase.

    PREFIX mel: <http://www.dei.unipd.it/~gdb/ontology/melody#>

    SELECT (GROUP_CONCAT(LCASE(?songTitle); SEPARATOR=" ") AS ?allSongTitles) WHERE {
        ?song a mel:Song ;
                mel:name ?songTitle .
    }

![](./wordcloud.png)

## Occurrences of the word *love* in song titles
This query counts the number of song titles in which occurs the word *love*. 

    PREFIX mel: <http://www.dei.unipd.it/~gdb/ontology/melody#>
    SELECT (COUNT(*) AS ?songWithLOVEInTheTitle) WHERE {
        ?song a mel:Song ;
                mel:name ?songTitle .
        
        FILTER(REGEX(LCASE(?songTitle), "\\blove\\b")) .
    }

    # ANSWER: 1643