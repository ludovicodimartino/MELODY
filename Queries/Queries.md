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

## One-Hit Wonders (The Musical Comets)
This query aims to identify artists who experienced a short moment of glory in the Top 50 of the Billboard charts. The query searchs for artists who had at least one song reach the Top 50 but never appeared in the Billboard charts again with any other song, even outside the Top 50.

    PREFIX mel: <http://www.dei.unipd.it/~gdb/ontology/melody#>

    SELECT ?artistName ?songName ?minPosition WHERE{
        ?song mel:name ?songName ;
                    mel:sungBy/mel:name ?artistName;
        {
            SELECT ?artistName ?songName (MIN(?position) AS ?minPosition)
                WHERE {

                ?song mel:name ?songName ;
                    mel:sungBy/mel:name ?artistName;
                mel:classified ?membership.

                ?membership a mel:Membership ;
                            mel:position ?position ;
                            mel:classifiedIn ?billboard .
                FILTER(?position < 51)
                }
            GROUP BY ?artistName ?songName
            HAVING(COUNT(?songName) = 1)
        }
        FILTER NOT EXISTS {
            ?song2 mel:name ?songName2 ;
                    mel:sungBy/mel:name ?artistName;
                    mel:classified ?membership2 .
        ?membership2 a mel:Membership ;
                            mel:position ?position2 ;
                            mel:classifiedIn ?billboard2 .
        FILTER(?position2 >= 51)
       }
    }

| Song Title                                        | Artist Name(s)                                           | Peak Position |
| ------------------------------------------------- | -------------------------------------------------------- | -------------: |
| Christmas (Baby Please Come Home)                 | Darlene Love                                              | 50            |
| Wasted Love                                       | Matt McAndrew                                             | 14            |
| Don't Go Breaking My Heart                        | Ultra Trax                                                | 50            |
| Hold Up My Heart                                  | Brooke White                                              | 47            |
| Lucky                                             | Ultra Trax                                                | 27            |
| Hey soul sister                                   | Glee Cast Karaoke's band                                 | 29            |
| (There's No Place Like) Home for the Holidays     | Mitchell Ayres \& His Orchestra                          | 41            |
| We Might Be Dead By Tomorrow                      | Soko                                                      | 9             |
| White Christmas                                   | Ken Darby Singers, Bing Crosby, John Scott Trotter \& His Orchestra | 48            |
| My Baby’s Got A Smile On Her Face                 | Craig Wayne Boyd                                          | 34            |
| "River Deep, Mountain High"                       | Ultra Trax                                                | 41            |
| 3AM (as made famous by Eminem)                    | Radio Killers                                             | 32            |
| Wonderful Christmastime                           | Jimmy Fallon                                              | 47            |
| Wonderful Summer                                  | Robin Ward                                                | 43            |

## Comeback Songs
This query explores the phenomenon of "comeback" songs, tracks that initially appeared on the Billboard charts, disappeared, and then made a reappearance at least a decade later.

    PREFIX mel: <http://www.dei.unipd.it/~gdb/ontology/melody#>

    SELECT DISTINCT ?songName ?artist ?earliestYear (YEAR(?date2) AS ?returnYear) (?returnYear - ?earliestYear AS ?distance)
    WHERE {
    ?song mel:name ?songName ;
            mel:classified ?membership2 .

    ?membership2 a mel:Membership ;
                mel:classifiedIn ?billboard2 .
    ?billboard2 mel:date ?date2 .

    {
        SELECT ?songName ?artist (MIN(YEAR(?date1)) AS ?earliestYear)
        WHERE {
        ?song mel:name ?songName ;
                mel:classified ?membership1 ;
                mel:sungBy ?art.
        ?art mel:name ?artist.
        ?membership1 a mel:Membership ;
                    mel:classifiedIn ?billboard1 .
        ?billboard1 mel:date ?date1 .
        }
        GROUP BY ?songName ?artist
    }

    FILTER (YEAR(?date2) > ?earliestYear)
    FILTER (YEAR(?date2) - ?earliestYear >= 10)
    }
    ORDER BY DESC(?distance) ?songName ?artist ?earliestYear ?returnYear


## Album Excellence
This query identifies albums with a significant concentration of Grammy-nominated or winning songs, calculating the percentage of tracks within albums that contain more than two songs and that feature at least two Grammy-recognized songs.

    PREFIX mel: <http://www.dei.unipd.it/~gdb/ontology/melody#>

    SELECT distinct ?albumName ?totTracks ?artistName
        (COUNT(distinct ?song) as ?songPerAlbum)
        ((COUNT(distinct ?song) / ?totTracks) * 100 AS ?grammyPercentage)
        (GROUP_CONCAT(distinct ?songName; SEPARATOR=", ") AS ?grammySongs)
    WHERE {
        ?song a mel:Song;
            mel:winner|mel:candidated ?grammy;
            mel:name ?songName;
            mel:sungBy ?artist.
        ?artist mel:name ?artistName.
        ?album mel:containsSong ?song;
            mel:name ?albumName;
            mel:totalTracks ?totTracks.
        FILTER(?totTracks>2)
    }
    GROUP BY ?albumName ?artistName ?totTracks
    HAVING(?songPerAlbum >1)
    ORDER BY DESC(?grammyPercentage)