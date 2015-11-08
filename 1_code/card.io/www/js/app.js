// Ionic Starter App

// angular.module is a global place for creating, registering and retrieving Angular modules
// 'starter' is the name of this angular module example (also set in a <body> attribute in index.html)
// the 2nd parameter is an array of 'requires'
// 'starter.controllers' is found in controllers.js
angular.module('starter', ['ionic', 'starter.controllers', 'starter.services', 'ngCookies', 'angular-md5', 'ngIOS9UIWebViewPatch'])

.run(function($ionicPlatform, $rootScope, $cookieStore, $location, $http, AuthenticationService) {
  
  $ionicPlatform.ready(function() {
    // Hide the accessory bar by default (remove this to show the accessory bar above the keyboard
    // for form inputs)
    if (window.cordova && window.cordova.plugins.Keyboard) {
      cordova.plugins.Keyboard.hideKeyboardAccessoryBar(true);
      cordova.plugins.Keyboard.disableScroll(true);

    }
    if (window.StatusBar) {
      // org.apache.cordova.statusbar required
      StatusBar.styleDefault();
    }
  });

  // keep user logged in after page refresh
  $rootScope.globals = $cookieStore.get('globals') || {};
  if ($rootScope.globals.currentUser) {
    $http.defaults.headers.common['Authorization'] = 'Basic ' + $rootScope.globals.currentUser.authdata; // jshint ignore:line
  }

  $rootScope.$on('$locationChangeStart', function (event, next, current) {
    // redirect to login page if not logged in and trying to access a restricted page
    var unrestrictedPages = ['/login', '/register'];
    var restrictedPage = unrestrictedPages.indexOf($location.path()) === -1;
    var loggedIn = AuthenticationService.IsLoggedIn();
    if (restrictedPage && !loggedIn) {
      $location.path('app/login');
    }
  });

})

.config(function($stateProvider, $urlRouterProvider) {
  $stateProvider

  .state('app', {
    url: '/app',
    abstract: true,
    templateUrl: 'templates/menu.html',
    controller: 'AppCtrl'
  })

  .state('app.login', {
    cache: false,
    url: '/login',
    views: {
      'menuContent': {
        templateUrl: 'templates/login.html',
        controller: 'LogInCtrl'
      }
    }
  })

  .state('app.home', {
    url: '/home',
    views: {
      'menuContent': {
        templateUrl: 'templates/home.html'
      }
    }
  })

  .state('app.profile', {
    cache: false,
    url: '/profile',
    views: {
      'menuContent': {
        templateUrl: 'templates/profile.html',
        controller: 'ProfileCtrl'
      }
    }
  })

  .state('app.settings', {
    url: '/settings',
    views: {
      'menuContent': {
        templateUrl: 'templates/settings.html',
        controller: 'SettingsCtrl'
      }
    }
  })

  .state('app.addWorkout', {
    cache: false,
    url: '/add/workout',
    views: {
      'menuContent': {
        templateUrl: 'templates/addWorkout.html',
        controller: 'AddWorkoutCtrl'
      }
    }
  })

  .state('app.addFood', {
    cache: false,
    url: '/add/food',
    views: {
      'menuContent': {
        templateUrl: 'templates/addFood.html',
        controller: 'AddFoodCtrl'
      }
    }
  })

  .state('app.browse', {
    url: '/browse',
    views: {
      'menuContent': {
        templateUrl: 'templates/browse.html'
      }
    }
  })

  .state('app.workouts', {
    url: '/workouts',
    views: {
      'menuContent': {
        templateUrl: 'templates/workouts.html',
        controller: 'WorkoutsCtrl'
      }
    }
  })

  .state('app.foods', {
    url: '/foods',
    views: {
      'menuContent': {
        templateUrl: 'templates/foods.html',
        controller: 'FoodsCtrl'
      }
    }
  })

  .state('app.workout', {
    url: '/workouts/:workoutId',
    views: {
      'menuContent': {
        templateUrl: 'templates/workout.html',
        controller: 'WorkoutsCtrl'
      }
    }
  })

  .state('app.food', {
    cache: false,
    url: '/workouts/:foodId',
    views: {
      'menuContent': {
        templateUrl: 'templates/food.html',
        controller: 'FoodsCtrl'
      }
    }
  });

  // if none of the above states are matched, use this as the fallback
  $urlRouterProvider.otherwise('/app/home');
});
