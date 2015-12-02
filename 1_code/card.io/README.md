# Card.io Mobile App

This README outlines the details of collaborating on this Ionic application.

## Prerequisites

You will need the following things properly installed on your computer.

* [Git](http://git-scm.com/)
* [Node.js](http://nodejs.org/) (with NPM)
* [Bower](http://bower.io/)
* [Ionic](http://ionicframework.com/getting-started/)

## Installation

* `git clone <repository-url>` this repository
* change into the <new directory>/card.io/
* `npm install`
* `bower install`

## Adding Platforms

* iOS: `ionic platform add ios` 
* Android: `ionic platform add android`

*Note: * To be able to install and run these applications you need to configure your environment for them, please follow [this](https://cordova.apache.org/docs/en/5.1.1/guide/platforms/index.html) guide that shows each platform.

### Building

* `ionic build <platform>`

### Run on device

* `ionic run -- <platform>`

*Note: * You need a device plugged into the machine and have the right libraries installed. 


### More notes about this application:

Calories calculated for running, cycling and walking are based on the following information:

* MET values found from : [here](https://sites.google.com/site/compendiumofphysicalactivities/Activity-Categories/running) and [here](http://prevention.sph.sc.edu/tools/docs/documents_compendium.pdf)
** Walking : 6.0 MET (using this for our app)
** running, (Taylor code 200) : 8.0 MET (using this for our app)
** running, 4 mph (15 min/mile) : 6.0 MET
** running, 5 mph (12 min/mile) : 8.3 MET
** running, 6 mph (10 min/mile) : 9.8 MET
** running, 7 mph (8.5 min/mile) : 11.0 MET
** running, 7.5 mph (8 min/mile) : 11.8 MET
** running, 8 mph (7.5 min/mile) : 11.8 MET
** running, 9 mph (6.5 min/mile) : 12.8 MET
** running, 10 mph (6 min/mile) : 14.5 MET
** running, 11 mph (5.5 min/mile) : 16.0 MET
** running, 12 mph (5 min/mile) : 19.0 MET
** running, 13 mph (4.6 min/mile) : 19.8 MET
** running, 14 mph (4.3 min/mile) : 23.0 MET
** bicycling, general : 7.5 MET (using this for our app)

* Calorie calculation formula can be found [here](http://www.mhhe.com/hper/physed/clw/webreview/web07/tsld007.htm).
** Calories = METS x weight (kg) x time (hours)