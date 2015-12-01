'use strict';

/**
 * @ngdoc overview
 * @name healthAnalyticsSiteApp
 * @description
 * # healthAnalyticsSiteApp
 *
 * Main module of the application.
 */
angular
  .module('healthAnalyticsSiteApp', [
    'ngCookies',
    'ngMessages',
    'ngResource',
    'ngRoute'
  ])
  .config(function ($routeProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'views/main.html',
        controller: 'MainCtrl',
        controllerAs: 'main'
      })
      .when('/about', {
        templateUrl: 'views/about.html',
        controller: 'AboutCtrl',
        controllerAs: 'about'
      })
      .when('/activity', {
        templateUrl: 'views/activity.html',
        controller: 'ActivityCtrl',
        controllerAs: 'act'
      })
      .when('/community', {
        templateUrl: 'views/community.html',
        controller: 'CommunityCtrl',
        controllerAs: 'comm'
      })
      .when('/export', {
        templateUrl: 'views/export.html',
        controller: 'ExportCtrl',
        controllerAs: 'export'
      })
      .when('/contact', {
        templateUrl: 'views/contact.html',
        controller: 'ContactCtrl',
        controllerAs: 'contact'
      })
      .otherwise({
        redirectTo: '/'
      });
  });
