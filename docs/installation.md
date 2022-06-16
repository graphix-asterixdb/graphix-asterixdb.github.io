---
layout: default
title: Installation
nav_order: 2
---

# Installation
{: .no_toc }

There are three ways to get Graphix running on top of your AsterixDB instance.
If you have no previous AsterixDB instance, you can get a start by [Using a Pre-Built Package](#using-a-pre-built-package) or [Building Graphix + AsterixDB from Source](#building-graphix--asterixdb-from-source).
If you have a previous AsterixDB instance and want to execute Graphix queries on said instance, you can get a start by [Updating AsterixDB for Graphix](#upgrading-asterixdb-for-graphix).

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{: toc }

## Using a Pre-Built Package

1. Ensure that you have Java 11 installed in your environment.
2. Download the pre-built Graphix package [here](https://drive.google.com/file/d/1yQUvaesLo5YwvlsqseA5iMHxiLM1CEZo/view?usp=sharing).
3. Create a configuration file that will signal to AsterixDB that you want to use Graphix.
    ```bash
    cd apache-asterixdb-*-SNAPSHOT/bin

    echo -e "
    [nc/asterix_nc]
    txn.log.dir=target/tmp/asterix_nc/txnlog
    core.dump.dir=target/tmp/asterix_nc/coredump
    iodevices=target/tmp/asterix_nc/iodevice
    
    [nc]
    address=127.0.0.1
    command=asterixnc
    
    [cc]
    address=127.0.0.1
    
    [extension/org.apache.asterix.graphix.extension.GraphixQueryTranslatorExtension]
    enabled=true
    [extension/org.apache.asterix.graphix.extension.GraphixLangExtension]
    enabled=true
    [extension/org.apache.asterix.graphix.extension.GraphixMetadataExtension]
    enabled=true 
    " > cc.conf
    ```
4. Navigate to the binaries folder and start a 1-node AsterixDB cluster with the Graphix configuration file from before.
    ```bash
    cd apache-asterixdb-*-SNAPSHOT/bin

    # Start a single node-controller.
    ./asterixncservice -logdir - &

    # Start a cluster-controller with Graphix enabled.
    ./asterixcc -config-file cc.conf &

    # Wait for our 1-node cluster to become active.
    ./asterixhelper wait_for_cluster -timeout 90
    ```
5. AsterixDB should now be up and running with Graphix!
    To quickly verify your Graphix installation, navigate to the query interface at [localhost:19006](https://localhost:19006) and issue the following metadata query:
    ```
    FROM    `Metadata`.`Graph` AS G,
            `Metadata`.`GraphDependency` GD,
            GD.Dependencies D 
    SELECT  *;
    ```
    If no errors are raised, then Graphix is sucessfully installed.   

## Building Graphix + AsterixDB from Source

1. Clone the AsterixDB git repository: [https://github.com/apache/asterixdb](https://github.com/apache/asterixdb).
    ```bash
    git clone https://github.com/apache/asterixdb.git 
    ```
2. Navigate to the `asterixdb` folder within the AsterixDB repository and clone the Graphix git repository: [https://github.com/apache/asterixdb-graph](https://github.com/apache/asterixdb-graph).
    The Graphix repository **must** be within this `asterixdb` folder and **must** be named as `asterix-opt`.
    ```bash
    cd asterixdb/asterixdb  
    git clone https://github.com/apache/asterixdb-graph.git asterix-opt
    ```
3. Run the following Maven command to build AsterixDB + Graphix.
    This may take a while, so get some coffee!
    ```bash
    cd asterixdb 
    mvn clean package -DskipTests
    ```
4. AsterixDB should now be packaged (and Graphix installed)!
    Navigate to binaries folder and start a 1-node AsterixDB cluster with a Graphix configuration file.
    ```bash
    PROJECT_SOURCE=$(pwd)
    cd asterixdb/asterix-server/target/asterix-server-*-SNAPSHOT-binary-assembly/apache-asterixdb-*-SNAPSHOT/bin

    # Start a single node-controller.
    ./asterixncservice -logdir - &

    # Start a cluster-controller with Graphix enabled.
    ./asterixcc -config-file "${PROJECT_SOURCE}/asterixdb/asterix-opt/asterix-graphix/src/main/resources/cc.conf" &

    # Wait for our 1-node cluster to become active.
    ./asterixhelper wait_for_cluster -timeout 90
    ```
5. AsterixDB should now be up and running with Graphix!
    To quickly verify your Graphix installation, navigate to the query interface at [localhost:19006](https://localhost:19006) and issue the following metadata query:
    ```
    FROM    `Metadata`.`Graph` AS G,
            `Metadata`.`GraphDependency` GD,
            GD.Dependencies D 
    SELECT  *;
    ```
    If no errors are raised, then Graphix is sucessfully installed.

## Upgrading AsterixDB for Graphix

Coming soon... :-)
