angular.module('starter.controllers', ['starter.services'])

.controller('AppCtrl', function($scope, $ionicModal, $timeout, $rootScope, $ionicHistory, $location, md5, UserService, AuthenticationService) {

  // With the new view caching in Ionic, Controllers are only called
  // when they are recreated or on app start, instead of every page change.
  // To listen for when this page is active (for example, to refresh data),
  // listen for the $ionicView.enter event:
  //$scope.$on('$ionicView.enter', function(e) {
  //});
  // Gravatar size
  $scope.gSize = 200;

  $scope.$watch( AuthenticationService.IsLoggedIn, function ( IsLoggedIn ) {
    $scope.isLoggedIn = IsLoggedIn;
    $scope.currentUser = AuthenticationService.CurrentUser();
    if($scope.currentUser && $scope.currentUser.birth_date) {
      $scope.currentUser.birth_date = new Date($scope.currentUser.birth_date);// theDate.year(), theDate.month(), theDate.date()
    }
  });

  $scope.isUserLogged = function(){
    var user = $rootScope.globals.currentUser;
    console.log(user);
    if(user){
      return true;
    } else {
      return false;
    }
  }

  $scope.doLogOut = function() {
    AuthenticationService.ClearCredentials();
    $ionicHistory.nextViewOptions({disableBack: true});
    $location.path('app/login');
  }

  $scope.user = function() { 
    if($rootScope.globals.currentUser) {
      return $rootScope.globals.currentUser.user;
    } else {
      return {};
    }
  }

  
  
  $scope.gravatarUrl = function() {
    return 'http://www.gravatar.com/avatar/' + md5.createHash($scope.currentUser.email.toLowerCase()) + '?s=' + $scope.gSize;
  }

  $scope.genderList = [
    {text: 'Male', value: 'male'},
    {text: 'Female', value: 'female'}
  ]

  /*
  $scope.getName = function () {
    if(plugins.appPreferences) {
      plugins.appPreferences.fetch(function(value){
        $scope.$apply(function(){$scope.name = value;});
        alert("I got this value: " + $scope.name);
      }, function(err){
        console.log(err);
      }, 'name');
    } else {
      return "Manuel";
    }
  };
  $scope.setName = function () {
    if(plugins.appPreferences) {
      plugins.appPreferences.store(function () {
        console.log('successfully saved!');
        alert("I saved: " + $scope.loginData.username);
        }, 
        function(){
          console.log('error setting reference...');
        }, 
        'name', 
        $scope.loginData.username
      );
    } else {
      console.log('nothing...');
    }
  };
  $scope.touchId = function(){
    $cordovaTouchID.checkSupport().then(function() {
      console.log('TouchID Available, using....');
      $cordovaTouchID.authenticate("Login plz").then(function() {
        alert('authenticated!');
      }, function () {
        alert('Something happened....');
      });
    }, function (error) {
      alert(error); // TouchID not supported
    });
  };
  */

})

.controller('PlaylistsCtrl', function($scope) {
  $scope.playlists = [
  { title: 'Reggae', id: 1 },
  { title: 'Chill', id: 2 },
  { title: 'Dubstep', id: 3 },
  { title: 'Indie', id: 4 },
  { title: 'Rap', id: 5 },
  { title: 'Cowbell', id: 6 }
  ];
})

.controller('LogInCtrl', function($scope, $ionicModal, $rootScope, $timeout, $location, $ionicHistory, $ionicPopup, UserService, AuthenticationService, FlashService) {
  $scope.loginData = {};
  $scope.registerData = {};

  $scope.$watch( $scope.registerData.birth_date, function ( birth_date ) {
    $scope.registerData.birth_date = new Date(birth_date);
  });

  // Perform the login action when the user submits the login form
  $scope.doLogin = function() {
    console.log('Doing login', $scope.loginData);
    $timeout(function() {
      AuthenticationService.Login($scope.loginData.email, $scope.loginData.password, function (response) {
        if (response.success) {
          AuthenticationService.SetCredentials($scope.loginData.email, $scope.loginData.password, response.user);
          $ionicHistory.nextViewOptions({disableBack: true});
          $location.path('app/home');
        } else {
          FlashService.Error(response.message);
          // An alert dialog
          $ionicPopup.alert({
            title: 'Login Failed.',
            template: 'The email or password may be incorrect.'
          });
        }
      });
    }, 1000);
  };


  // Perform the register action when the user submits the register form
  $scope.doRegister = function() {
    console.log('Doing register', $scope.registerData);
    $timeout(function() {
      $scope.registerData.username = $scope.registerData.email;
      $scope.registerData.birth_date = new Date($scope.registerData.birth_date);
      UserService.Create($scope.registerData);
      $scope.closeRegisterModal();
    }, 1000);
  };

  // Create the register modal that we will use later
  $ionicModal.fromTemplateUrl('templates/register.html', {
    scope: $scope
  }).then(function(modal) {
    $scope.modal = modal;
  });
  $scope.openRegisterModal = function() {
    $scope.modal.show();
  };
  $scope.closeRegisterModal = function() {
    $scope.modal.hide();
  };
  $scope.$on('$destroy', function() {
    $scope.modal.remove();
  });
  $scope.$on('modal.hidden', function() {
    $scope.registerData = {};
  });

})

.controller('ProfileCtrl', function($scope, $rootScope, UserService) {
  $scope.editing = false;

  // Perform the login action when the user submits the login form
  $scope.toggleEdit = function() {
    $scope.editing = !$scope.editing;
    if ($scope.editing) {
      console.log('Edit Profile ...');
    } else {
      console.log('Edit Profile Done ...');
    }
    
  };

  // Perform the login action when the user submits the login form
  $scope.saveProfile = function() {
    console.log('do nothing...');
  };

})

.controller('SettingsCtrl', function($scope, $stateParams) {
})

.controller('AddWorkoutCtrl', function($scope, $stateParams) {
  $scope.workoutTypes = [
    {text: 'Run', value: 'run'},
    {text: 'Walk', value: 'Walk'},
    {text: 'Bike', value: 'bike'},
  ];
  var now = moment();
  var name = 'Run on ' + (now.month()+1) + '/' + now.date() + '/' + now.year();
  $scope.workoutData = {name: name, type: 'run', date: new Date(now.year(), now.month(), now.date()), distance: 0.0, duration: 0.0};
})

.controller('AddFoodCtrl', function($scope, $stateParams) {
  var now = moment();
  $scope.foodData = {type: 'lunch', food: "coffee", serving: '0.5', date: new Date(now.year(), now.month(), now.date())};

  $scope.foodTypes = [
    {text: 'Pizza', value: 'pizza', calories: 215},
    {text: 'Coffee', value: 'coffee', calories: 130},
    {text: 'Cake', value: 'cake', calories: 600}
  ];

  $scope.mealTypes = [
    {text: 'Breakfast', value: 'breakfast'},
    {text: 'Lunch', value: 'lunch'},
    {text: 'Dinner', value: 'dinner'},
    {text: 'Snack', value: 'snack'},
    {text: 'Other', value: 'other'}
  ];

  $scope.servingTypes = [
    {text: 'A Lot', value: '3'},
    {text: 'Moderate', value: '2'},
    {text: 'Normal', value: '1'},
    {text: 'Quick Snack', value: '0.5'}
  ];
})

.controller('PlaylistCtrl', function($scope, $stateParams) {
});
