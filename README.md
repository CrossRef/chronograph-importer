# Chronograph MySQL Importer

The DOI Chronograph collects temporal data about DOIs. This is an experimental tool to fetch data directly from a local MySQL database, query the API and insert the data back. It needs configuring with:

* the name of your database
* username, password of database
* table in question
* initial select clause (can be for all DOIs or for a subset of your choosing)
* the name of the column that contains the DOI
* the mapping of Chronograph types to database row names
* the URL of the API

When you run it, it will query your MySQL table for DOIs, send each one to the API, then update your table in the specified columns with the resulting data.

## Types of data

Please see `src/chronograph/types.clj` in the Chronograph project for the latest. Here are the relevant ones (it currently only works for dates):

* **issued**  "Publisher Issue date"
* **deposited**  "Publisher first deposited with CrossRef"
* **updated**  "Publisher most recently updated CrossRef metadata"
* **first-resolution-test**  "First attempt DOI resolution test"
* **first-resolution**  "First DOI resolution"
* **crossmark-update-published**  "CrossMark Update to this DOI Published"

Not all will be relevant.

## To obtain

* open a terminal
* `cd` to a directory of your choosing, e.g. `cd ~/things`
* `git clone git@github.com:CrossRef/chronograph-importer.git`
* `cd chronograph-importer`

## To install

* `sudo pip install virtualenvwrapper`
* `mkvirtualenv chronograph-importer`
* `workon chronograph-importer`
* `pip install -r requirements.txt`

## To configure

* make a copy of `config.json.example` and call it `config.json` in the same directory
* change the keys to match your configuration

## To run

* `cd` to your directory, e.g. `cd ~/things/chronograph-importer`
* `workon chronograph-importer`
* `python importer.py`
