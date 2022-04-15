---
layout: default
title: Getting Started
nav_order: 3
---

# Getting Started
{: .no_toc }

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{: toc }

## Starting a Sample Cluster

1. Head on over to the [Installation](../docs/installation.html) section and install AsterixDB + Graphix.
2. Navigate to the `asterix-server` folder in your AsterixDB installation directory, and locate the executables folder.
    ```bash
    cd ${ASTERIXDB_INSTALLATION_DIR}/asterixdb/asterix-server/target
    cd asterix-server-*-binary-assembly/apache-asterixdb-*-SNAPSHOT/bin
    ```
3. We are going to start a 1-node cluster using the Graphix extension. Start the NC service.
    ```bash
    ./bin/asterixncservice -logdir - &
    ```
4. Start our cluster controller, and use the sample Graphix `cc.conf`.
    ```bash
    GRAPHIX_CC_CONF=${ASTERIXDB_INSTALLATION_DIR}/asterix-graphix/src/main/resources/cc.conf
    ./bin/asterixcc -config-file ${GRAPHIX_CC_CONF} &
    ```
    The Graphix extension is enabled through the last lines of the `cc.conf`:
    ```properties
    [extension/org.apache.asterix.graphix.extension.GraphixQueryTranslatorExtension]
    enabled=true

    [extension/org.apache.asterix.graphix.extension.GraphixLangExtension]
    enabled=true

    [extension/org.apache.asterix.graphix.extension.GraphixMetadataExtension]
    enabled=true
    ```

## Building the Gelp Datasets

1. For our tutorial we use the "Gelp" example, where `Users` make `Reviews` about `Businesses`.
    To start, let's create a new dataverse and all of the aforementioned entities as datasets.
    ```
    DROP DATAVERSE    Gelp IF EXISTS;
    CREATE DATAVERSE  Gelp;
    USE               Gelp;
    
    CREATE TYPE       UsersType 
    AS                { user_id : bigint };
    CREATE DATASET    Users (UserType)
    PRIMARY KEY       user_id;
       
    CREATE TYPE       ReviewsType
    AS                { review_id : string };
    CREATE DATASET    Reviews (ReviewsType)
    PRIMARY KEY       review_id;

    CREATE TYPE       BusinessesType
    AS                { business_id : bigint };
    CREATE DATASET    Businesses (BusinessesType)
    PRIMARY KEY       business_id;
    ```
    In the example above, all three datasets only have their primary keys defined.
    All other fields associated with each entity exist as _open_ fields.
2. Let's now insert some data into our dataverse. We'll start with our `Businesses` dataset.
    ```
    INSERT INTO   Gelp.Businesses [
        { "business_id": "B1", "name": "Papa's Supermarket", "number": "909-123-6123" },
        { "business_id": "B2", "name": "Mother's Gas Station", "number": "111-724-1123" },
        { "business_id": "B3", "name": "Uncle's Bakery" }
    ];
    ```
    The three records inserted show two fields that were not defined in the `BusinessesType` data type: `name` and `number`.
    The last record illustrates the potential heterogenity enabled by AsterixDB's document data model, where some businesses may not have a number attached to them.
3. Having populated our `Businesses` dataset, let's now move onto our `Users`:
    ```
    INSERT INTO   Gelp.Users [
        { "user_id": 1, "name": "Mary", "friends": [ 4, 5 ] },
        { "user_id": 2, "name": "John", "friends": [ 5 ] },
        { "user_id": 4, "name": "Susan", "friends": [ 1 ] },
        { "user_id": 5, "name": "Larry", "friends": [ 1, 2 ] }
    ];
    ```
    Similar to our `Businesses` records, these `Users` records inserted include two fields that weren't defined in their dataset type: `name` and `friends`.
    A user may have a name and an array of `user_id` values denoting their friends.
    The potential `friends` array of a user depicts a common _denormalized_ form of modeling one-to-many relationships, again enabled by AsterixDB's document data model.
4. Finally, let's move onto our last dataset: `Reviews`.
    ```
    INSERT INTO   Gelp.Reviews [
        { "review_id": "R1", "user_id": 1, "business_id": "B3", "review_time": date("2022-03-01") },
        { "review_id": "R2", "user_id": 5, "business_id": "B3", "review_time": date("2022-03-01") },
        { "review_id": "R3", "user_id": 2, "business_id": "B1", "review_time": date("2022-03-02") },
        { "review_id": "R4", "user_id": 5, "business_id": "B1", "review_time": date("2022-03-03") }
    ];
    ```
    A review may include an associated user, business, and review time.

## Building the Gelp Graph

1. We now have a logical data model for Gelp, with three defined datasets:  

## Querying our Gelp Graph
1. Let's now query our data. Suppose that we want to find all businesses that users will go to with their friends.
    We can use the `review_time` from the `Reviews` dataset as a proxy for the "go to with" action, and formulate the following SQL++ query:
    ```
    FROM    Gelp.Users U,
            U.friends F,
            Gelp.Reviews R1,
            Gelp.Reviews R2,
            Gelp.Businesses B
    WHERE   R1.user_id = U.user_id AND 
            R2.user_id = F AND
            R1.business_id = B.business_id AND
            R2.business_id = B.business_id AND
            R1.review_time = R2.review_time
    SELECT  DISTINCT VALUE B;
    ```

## Stopping our Sample Cluster

1. Navigate to the `asterix-server` folder in your AsterixDB installation directory, and locate the executables folder.
```bash
cd ${ASTERIXDB_INSTALLATION_DIR}/asterixdb/asterix-server/target
cd asterix-server-*-binary-assembly/apache-asterixdb-*-SNAPSHOT/bin
```

2. To stop the cluster started in [Starting a Sample Cluster](./getting-started.html#starting-a-sample-cluster), run the following command:
```bash
./bin/asterixhelper shutdown_cluster_all
```
